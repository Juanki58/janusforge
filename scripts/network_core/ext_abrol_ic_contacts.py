#!/usr/bin/env python3
"""EXTERNAL — Abrol Zenodo avg-frame IC contact inventory (Gi vs βarr2).

Governance: docs/synthesis/EXPERIMENT_EXT_ABROL_IC_CONTACTS.md
  - Average frames only; NOT MSM; NOT Gi functional claim; P3 remains BLOCKED.
  - Zip stays gitignored under data/external/abrol_heo_2024/.

Outputs:
  results/network_core/ext_abrol_ic_contacts.{md,json}
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

try:
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import capped_distance
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required (janus_p1): {e}") from e

try:
    from Bio import pairwise2
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"Biopython required (janus_p1): {e}") from e

# ---------------------------------------------------------------------------
# Locked a priori
# ---------------------------------------------------------------------------

UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

AA3_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "CYX": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "HID": "H",
    "HIE": "H",
    "HIP": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}

# IC windows in UniProt 1-based inclusive
IC_WINDOWS = [
    (60, 80, "ICL1_TM2"),
    (130, 150, "ICL2_DRY"),
    (215, 250, "ICL3_TM56"),
    (290, 320, "TM7_H8"),
]

HUBS_UNIPROT = [79, 83, 287, 291, 295, 302]

SYSTEMS = {
    "WT_Gi_Empty": "CB2R-WT-NoPhosphoC_Gi-Empty_avgframe569.pdb",
    "WT_Gi_GDP": "CB2R-WT-NoPhosphoC_Gi-GDP_avgframe1262.pdb",
    "WT_BARR2_NoP": "CB2R-WT-NoPhosphoC_BARR2_avgframe676.pdb",
    "WT_BARR2_P": "CB2R-WT-PhosphoC_BARR2_avgframe29.pdb",
}

ZIP_NAME = "PDB_avg_structures.zip"
DATA_DIR = ROOT / "data" / "external" / "abrol_heo_2024"
AVG_DIR = DATA_DIR / "avg_pdbs"
ZIP_PATH = DATA_DIR / ZIP_NAME
OUT_MD = ROOT / "results" / "network_core" / "ext_abrol_ic_contacts.md"
OUT_JSON = ROOT / "results" / "network_core" / "ext_abrol_ic_contacts.json"

CA_CUTOFF = 8.0
MIN_MAPPED_IC = 50
MIN_CONTACTS_FOR_DISTINCT = 20

_VDW = {
    "H": 1.20,
    "C": 1.70,
    "N": 1.55,
    "O": 1.52,
    "S": 1.80,
    "P": 1.80,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_extracted() -> dict[str, Any]:
    AVG_DIR.mkdir(parents=True, exist_ok=True)
    meta: dict[str, Any] = {"zip_present": ZIP_PATH.exists()}
    if not ZIP_PATH.exists():
        return meta
    meta["zip_sha256"] = sha256_file(ZIP_PATH)
    meta["zip_bytes"] = ZIP_PATH.stat().st_size
    want = set(SYSTEMS.values())
    with zipfile.ZipFile(ZIP_PATH) as z:
        for info in z.infolist():
            base = Path(info.filename).name
            if base in want:
                target = AVG_DIR / base
                if not target.exists():
                    target.write_bytes(z.read(info))
    meta["extracted"] = {k: (AVG_DIR / v).exists() for k, v in SYSTEMS.items()}
    return meta


def protein_seq_and_res(u: mda.Universe):
    prot = u.select_atoms("protein")
    residues = list(prot.residues)
    seq = "".join(AA3_TO_1.get(r.resname, "X") for r in residues)
    return seq, residues, prot


def map_cb2(seq: str) -> dict[int, int]:
    """local residue index -> UniProt 0-based index."""
    alis = pairwise2.align.localms(UNIPROT_P34972, seq, 2, -1, -10, -0.5, one_alignment_only=True)
    if not alis:
        return {}
    u_al, s_al = alis[0].seqA, alis[0].seqB
    mapping: dict[int, int] = {}
    ui = 0
    si = 0
    for a, b in zip(u_al, s_al):
        if a != "-" and b != "-":
            mapping[si] = ui
            ui += 1
            si += 1
        elif a == "-":
            si += 1
        else:
            ui += 1
    return mapping


def ic_local_indices(mapping: dict[int, int]) -> list[int]:
    ic_uni = set()
    for lo, hi, _ in IC_WINDOWS:
        for u in range(lo - 1, hi):
            ic_uni.add(u)
    return sorted(si for si, ui in mapping.items() if ui in ic_uni)


def heavy_atoms(res):
    return res.atoms.select_atoms("not name H* and not name HT*")


def contacts_vdw(cb2_res_list, effector_res_list) -> set[tuple[int, str]]:
    """Return set of (uniprot1-based, resname) on CB2 that contact effector."""
    # Build coordinate arrays with residue ownership
    coords = []
    owners = []  # (uniprot1, resname) for CB2 side only; effector owners ignored
    radii = []
    for uniprot1, res in cb2_res_list:
        for atom in heavy_atoms(res):
            el = atom.element if hasattr(atom, "element") else atom.name[0]
            el = el.upper()[:1]
            coords.append(atom.position)
            owners.append((uniprot1, res.resname))
            radii.append(_VDW.get(el, 1.70))
    n_cb2 = len(coords)
    for res in effector_res_list:
        for atom in heavy_atoms(res):
            el = atom.element if hasattr(atom, "element") else atom.name[0]
            el = el.upper()[:1]
            coords.append(atom.position)
            owners.append(None)
            radii.append(_VDW.get(el, 1.70))
    if n_cb2 == 0 or len(coords) == n_cb2:
        return set()
    xyz = np.asarray(coords, dtype=np.float64)
    # capped_distance with generous max
    max_cut = 5.0  # VdW+0.5 worst-case ~4.1; pad
    pairs = capped_distance(
        xyz[:n_cb2],
        xyz[n_cb2:],
        max_cutoff=max_cut,
        return_distances=True,
    )
    hit: set[tuple[int, str]] = set()
    if pairs[0].size == 0:
        # fallback Cα
        return contacts_ca(cb2_res_list, effector_res_list)
    idx_pairs, dists = pairs
    for (i, j), d in zip(idx_pairs, dists):
        if d <= radii[i] + radii[n_cb2 + j] + 0.5:
            hit.add(owners[i])
    if not hit:
        return contacts_ca(cb2_res_list, effector_res_list)
    return hit


def contacts_ca(cb2_res_list, effector_res_list) -> set[tuple[int, str]]:
    ca_cb2 = []
    own = []
    for uniprot1, res in cb2_res_list:
        ca = res.atoms.select_atoms("name CA")
        if len(ca) == 0:
            continue
        ca_cb2.append(ca[0].position)
        own.append((uniprot1, res.resname))
    ca_eff = []
    for res in effector_res_list:
        ca = res.atoms.select_atoms("name CA")
        if len(ca):
            ca_eff.append(ca[0].position)
    if not ca_cb2 or not ca_eff:
        return set()
    a = np.asarray(ca_cb2)
    b = np.asarray(ca_eff)
    pairs = capped_distance(a, b, max_cutoff=CA_CUTOFF, return_distances=False)
    return {own[i] for i, _ in pairs}


def analyze_system(label: str, pdb_name: str) -> dict[str, Any]:
    path = AVG_DIR / pdb_name
    out: dict[str, Any] = {"label": label, "pdb": pdb_name, "path": str(path)}
    if not path.exists():
        out["status"] = "MISSING_PDB"
        return out
    out["pdb_sha256"] = sha256_file(path)
    u = mda.Universe(str(path))
    seq, residues, _prot = protein_seq_and_res(u)
    mapping = map_cb2(seq)
    out["n_protein_res"] = len(residues)
    out["n_mapped_to_uniprot"] = len(mapping)
    if mapping:
        ident = sum(1 for si, ui in mapping.items() if seq[si] == UNIPROT_P34972[ui])
        out["identity"] = ident / len(mapping)
        out["mapped_uni_range"] = [min(mapping.values()) + 1, max(mapping.values()) + 1]
    else:
        out["identity"] = None
        out["status"] = "INDETERMINATE_NUMBERING"
        return out

    ic_locals = ic_local_indices(mapping)
    out["n_ic_mapped"] = len(ic_locals)
    if len(ic_locals) < MIN_MAPPED_IC:
        out["status"] = "INDETERMINATE_NUMBERING"
        return out

    cb2_idx = set(mapping.keys())
    cb2_ic = [(mapping[si] + 1, residues[si]) for si in ic_locals]
    effector = [residues[i] for i in range(len(residues)) if i not in cb2_idx]
    out["n_effector_res"] = len(effector)

    hit = contacts_vdw(cb2_ic, effector)
    out["contact_method"] = "vdw+0.5_or_ca8"
    out["n_contacts_residue"] = len(hit)
    out["cb2_contact_residues"] = sorted({u for u, _ in hit})
    out["cb2_contact_labels"] = [f"{rn}:{u}" for u, rn in sorted(hit, key=lambda x: x[0])]
    hubs_touch = sorted(u for u in out["cb2_contact_residues"] if u in HUBS_UNIPROT)
    out["hubs_touching_effector"] = hubs_touch
    out["status"] = "OK"
    return out


def jaccard(a: set[int], b: set[int]) -> float | None:
    if not a and not b:
        return None
    return len(a & b) / len(a | b)


def verdict_from(results: dict[str, dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    if not ZIP_PATH.exists():
        return "EXT_ABROL_IC_INDETERMINATE_MISSING_DATA", {}
    for lab, r in results.items():
        if r.get("status") != "OK":
            if r.get("status") == "MISSING_PDB":
                return "EXT_ABROL_IC_INDETERMINATE_MISSING_DATA", {}
            if r.get("status") == "INDETERMINATE_NUMBERING":
                return "EXT_ABROL_IC_INDETERMINATE_NUMBERING", {}

    gi = set(results["WT_Gi_Empty"]["cb2_contact_residues"])
    barr = set(results["WT_BARR2_P"]["cb2_contact_residues"])
    gi_gdp = set(results["WT_Gi_GDP"]["cb2_contact_residues"])
    barr_nop = set(results["WT_BARR2_NoP"]["cb2_contact_residues"])

    metrics = {
        "jaccard_GiEmpty_vs_BARR2P": jaccard(gi, barr),
        "jaccard_GiEmpty_vs_GiGDP": jaccard(gi, gi_gdp),
        "jaccard_BARR2NoP_vs_BARR2P": jaccard(barr_nop, barr),
        "n_GiEmpty": len(gi),
        "n_BARR2P": len(barr),
    }
    j = metrics["jaccard_GiEmpty_vs_BARR2P"]
    if j is None:
        return "EXT_ABROL_IC_INDETERMINATE_NUMBERING", metrics
    if len(gi) >= MIN_CONTACTS_FOR_DISTINCT and len(barr) >= MIN_CONTACTS_FOR_DISTINCT and j < 0.50:
        return "EXT_ABROL_IC_EFFECTOR_DISTINCT", metrics
    if j >= 0.70:
        return "EXT_ABROL_IC_EFFECTOR_SIMILAR", metrics
    return "EXT_ABROL_IC_EFFECTOR_PARTIAL", metrics


def write_report(payload: dict[str, Any]) -> None:
    lines = [
        "# EXTERNAL — Abrol Zenodo IC contact inventory (avg frames)",
        "",
        f"**Run UTC:** `{payload['run_utc']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_ABROL_IC_CONTACTS.md`",
        f"**Zenodo:** [10.5281/zenodo.14227795](https://doi.org/10.5281/zenodo.14227795) (record files via 14232007)",
        "",
        "## Verdict",
        "",
        f"**Primary:** `{payload['verdict']}`",
        "",
        f"**P3 project gate:** `BLOCKED` — this inventory does **not** complete P3.",
        "",
        "> Average frames of effector complexes ≠ apo MSM. No Gi functional claim.",
        "",
        "## Download / provenance",
        "",
        f"- Zip present: `{payload['download']['zip_present']}`",
    ]
    if payload["download"].get("zip_sha256"):
        lines.append(f"- Zip sha256: `{payload['download']['zip_sha256']}`")
        lines.append(f"- Zip bytes: `{payload['download']['zip_bytes']}`")
    lines += ["", "## Per-system IC contact residues (CB2 UniProt)", ""]
    lines.append("| System | Mapped IC | Effector res | n CB2 contact res | Hubs touching | Identity |")
    lines.append("|--------|----------:|-------------:|------------------:|---------------|---------:|")
    for lab, r in payload["systems"].items():
        if r.get("status") != "OK":
            lines.append(f"| {lab} | — | — | — | status={r.get('status')} | — |")
            continue
        hubs = ",".join(str(x) for x in r["hubs_touching_effector"]) or "—"
        lines.append(
            f"| {lab} | {r['n_ic_mapped']} | {r['n_effector_res']} | {r['n_contacts_residue']} | {hubs} | {r['identity']:.3f} |"
        )
    m = payload["metrics"]
    lines += [
        "",
        "## Jaccard (CB2 contact-residue sets)",
        "",
        f"- Gi_Empty vs BARR2_P: **{m.get('jaccard_GiEmpty_vs_BARR2P')}**",
        f"- Gi_Empty vs Gi_GDP: **{m.get('jaccard_GiEmpty_vs_GiGDP')}**",
        f"- BARR2_NoP vs BARR2_P: **{m.get('jaccard_BARR2NoP_vs_BARR2P')}**",
        "",
        "## Contact residue lists (UniProt)",
        "",
    ]
    for lab, r in payload["systems"].items():
        if r.get("status") != "OK":
            continue
        labs = ", ".join(r["cb2_contact_labels"][:40])
        more = "" if len(r["cb2_contact_labels"]) <= 40 else f" … (+{len(r['cb2_contact_labels'])-40})"
        lines.append(f"- **{lab}** ({r['n_contacts_residue']}): {labs}{more}")
    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {payload['verdict']}",
        "P3_PROJECT_GATE: BLOCKED",
        "Gi_FUNCTIONAL_CLAIM: FALSE",
        "P2_REOPEN: FALSE",
        "AVG_FRAME_NEQ_MSM: TRUE",
        "```",
        "",
        "## References",
        "",
        "1. Heo & Abrol, *BBRC* — [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100)",
        "2. Zenodo — [10.5281/zenodo.14227796](https://doi.org/10.5281/zenodo.14227796)",
        "",
        "---",
        "",
        "*Fin EXTERNAL Abrol IC inventory. Toward P3; P3 not done.*",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    download = ensure_extracted()
    if not download.get("zip_present"):
        payload = {
            "experiment": "EXTERNAL_ABROL_IC_CONTACTS",
            "run_utc": run_utc,
            "verdict": "EXT_ABROL_IC_INDETERMINATE_MISSING_DATA",
            "download": download,
            "systems": {},
            "metrics": {},
            "p3_project_gate": "BLOCKED",
            "gi_functional_claim": False,
            "p2_reopen": False,
        }
        write_report(payload)
        print(payload["verdict"])
        return 0

    results = {lab: analyze_system(lab, pdb) for lab, pdb in SYSTEMS.items()}
    verdict, metrics = verdict_from(results)
    payload = {
        "experiment": "EXTERNAL_ABROL_IC_CONTACTS",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_ABROL_IC_CONTACTS.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "download": download,
        "systems": results,
        "metrics": metrics,
        "ic_windows": IC_WINDOWS,
        "hubs": HUBS_UNIPROT,
        "p3_project_gate": "BLOCKED",
        "gi_functional_claim": False,
        "p2_reopen": False,
        "doi_zenodo": "10.5281/zenodo.14227795",
        "doi_paper": "10.1016/j.bbrc.2024.151100",
    }
    write_report(payload)
    print(verdict, metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
