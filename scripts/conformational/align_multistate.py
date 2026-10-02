#!/usr/bin/env python3
"""Align CB1/CB2 multistate receptors on TM1–TM7 Cα (Kabsch)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.conformational.pdb_utils import (  # noqa: E402
    ca_coords_by_resseq,
    kabsch_align,
    read_atoms,
    write_aligned_pdb,
)
from scripts.conformational.residue_maps import (  # noqa: E402
    STRUCTURES,
    iter_verified_structures,
    tm_ca_residues,
)
from src.screening.receptors import clean_protein_pdb, download_pdb  # noqa: E402

OUT_DIR = ROOT / "data/targets/multistate_aligned"
MANIFEST = OUT_DIR / "alignment_manifest.json"

REF_BY_RECEPTOR = {"cb2": "6PT0", "cb1": "5TGZ"}

# Chains for CB2 monomer isolation (human receptor only; no Gi/scFv/ligand).
CB2_MONOMER_CHAINS = {
    "6PT0": "R",
    "6KPF": "R",
    "8GUR": "R",
    "5ZTY": "A",
}


def _ensure_source(spec) -> Path:
    src = ROOT / spec.source_pdb
    if src.exists():
        return src
    subdir = "cb1" if spec.receptor == "cb1" else "cb2_multistate"
    raw = ROOT / f"data/targets/{subdir}/{spec.pdb_id}.pdb"
    download_pdb(spec.pdb_id, raw)
    chains = [spec.chain] if spec.chain else None
    clean_protein_pdb(raw.read_text(encoding="utf-8"), src, chains=chains)
    return src


def _matched_ca(
    ref_atoms,
    mob_atoms,
    receptor: str,
) -> tuple[np.ndarray, np.ndarray, list[int]]:
    tm_res = tm_ca_residues(receptor)
    ref_ca = ca_coords_by_resseq(ref_atoms, tm_res)
    mob_ca = ca_coords_by_resseq(mob_atoms, tm_res)
    shared = sorted(set(ref_ca) & set(mob_ca))
    if len(shared) < 30:
        raise RuntimeError(
            f"Too few shared TM Cα for {receptor}: {len(shared)} (need >=30)"
        )
    ref_pts = np.stack([ref_ca[r] for r in shared])
    mob_pts = np.stack([mob_ca[r] for r in shared])
    return ref_pts, mob_pts, shared


def align_structure(
    spec,
    ref_spec,
    ref_atoms,
) -> dict:
    src = _ensure_source(spec)
    chains = {spec.chain} if spec.chain else None
    mob_atoms = read_atoms(src, chains=chains)
    ref_pts, mob_pts, shared = _matched_ca(ref_atoms, mob_atoms, spec.receptor)
    rot, trans = kabsch_align(mob_pts, ref_pts)
    rmsd_before = float(
        np.sqrt(np.mean(np.sum((mob_pts - ref_pts) ** 2, axis=1)))
    )
    aligned_pts = mob_pts @ rot + trans
    rmsd_after = float(
        np.sqrt(np.mean(np.sum((aligned_pts - ref_pts) ** 2, axis=1)))
    )
    out_pdb = OUT_DIR / f"{spec.pdb_id}_aligned.pdb"
    write_aligned_pdb(src, out_pdb, rot, trans, chains=chains)
    return {
        "pdb_id": spec.pdb_id,
        "receptor": spec.receptor,
        "chain": spec.chain,
        "reference": ref_spec.pdb_id,
        "source_pdb": str(src.relative_to(ROOT)).replace("\\", "/"),
        "aligned_pdb": str(out_pdb.relative_to(ROOT)).replace("\\", "/"),
        "tm_ca_pairs": len(shared),
        "rmsd_before_A": round(rmsd_before, 3),
        "rmsd_after_A": round(rmsd_after, 3),
        "state_label": spec.state_label,
        "ligand_resname": spec.ligand_resname,
    }


def run_alignment() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    specs = [s for s in STRUCTURES if s.status == "VERIFIED"]
    ref_atoms_cache: dict[str, list] = {}
    entries: list[dict] = []
    blocked: list[dict] = []

    for spec in specs:
        ref_id = REF_BY_RECEPTOR[spec.receptor]
        ref_spec = next(s for s in specs if s.pdb_id == ref_id)
        if ref_spec.pdb_id not in ref_atoms_cache:
            ref_src = _ensure_source(ref_spec)
            ref_chains = {ref_spec.chain} if ref_spec.chain else None
            ref_atoms_cache[ref_spec.pdb_id] = read_atoms(ref_src, chains=ref_chains)
        ref_atoms = ref_atoms_cache[ref_spec.pdb_id]

        if spec.pdb_id == ref_id:
            src = _ensure_source(spec)
            out_pdb = OUT_DIR / f"{spec.pdb_id}_aligned.pdb"
            out_pdb.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            entries.append(
                {
                    "pdb_id": spec.pdb_id,
                    "receptor": spec.receptor,
                    "chain": spec.chain,
                    "reference": ref_id,
                    "source_pdb": str(src.relative_to(ROOT)).replace("\\", "/"),
                    "aligned_pdb": str(out_pdb.relative_to(ROOT)).replace("\\", "/"),
                    "tm_ca_pairs": len(tm_ca_residues(spec.receptor)),
                    "rmsd_before_A": 0.0,
                    "rmsd_after_A": 0.0,
                    "state_label": spec.state_label,
                    "ligand_resname": spec.ligand_resname,
                }
            )
        else:
            entries.append(align_structure(spec, ref_spec, ref_atoms))

    for spec in STRUCTURES:
        if spec.status == "BLOCKED":
            blocked.append(
                {
                    "pdb_id": spec.pdb_id,
                    "block_reason": spec.block_reason,
                }
            )

    manifest = {
        "method": "Kabsch superposition on shared TM1–TM7 Cα (GPCRdb spans)",
        "references": REF_BY_RECEPTOR,
        "aligned_structures": entries,
        "blocked": blocked,
        "level0_notes": {
            "5TGZ_ligand": "AM6538 (CCD ZDG) — antagonist/inactive CB1; not Taranabant",
            "5XRA_ligand": "AM11542 (CCD 8D3) — agonist/active CB1 (verified RCSB COMPND)",
            "5ZTY_ligand": "AM10257 (CCD 9JU) — inactive antagonist CB2 (not Gi-active)",
            "8GUR_ligand": "CP55,940 (CCD 9GF) — agonist CB2–G cryo-EM (Li et al. 2023); chain R",
            "6KPG": "Not used — 5XRA selected as verified CB1 active crystal",
            "5VEU": "BLOCKED — CYP3A5",
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()
    manifest = run_alignment()
    print(f"Aligned {len(manifest['aligned_structures'])} structures -> {OUT_DIR}")
    print(f"Manifest: {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
