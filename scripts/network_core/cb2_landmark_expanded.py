#!/usr/bin/env python3
"""EXTERNAL — CB2 expanded geometric landmark contact maps.

Governance: docs/synthesis/EXPERIMENT_CB2_LANDMARK_EXPANDED.md (pre-registered).
  - Geometric proximity labeling (RMSD Cα) to Dutta-6 + public cryo/crystal panel.
  - Per-PDB Gate0 drop with reason; continue with passing set.
  - NOT kinetic MSM; NOT P2 reopen; no Gi claims.
  - Geometric proximity ≠ MSM metastable identity.

Outputs:
  results/network_core/cb2_landmark_expanded.{md,json}
  data/external/cb2_landmark_expanded/MANIFEST.json (gate0 status updated)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from p1_dynamic_hub_validation import (  # noqa: E402
    CONTACT_DEF,
    _MAX_CUT,
    _SLACK,
    _VDW,
    res_label,
)

# Reuse helpers from Dutta-6 landmark runner
from cb2_landmark_contacts import (  # noqa: E402
    AA3_TO_1,
    EXPECT_N_ATOMS,
    UNIPROT_P34972,
    accumulate_frame_ca,
    accumulate_frame_contacts,
    build_protein_tables,
    choose_stratified,
    edges_from_counts,
    jaccard,
    kabsch_rmsd,
    list_zip_nc_by_state,
    nw_align,
    protein_seq_resids,
    sha256_file,
    softmax_neg_rmsd,
)

try:
    import MDAnalysis as mda
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required: {e}") from e

# ---------------------------------------------------------------------------
# Locked a priori (see EXPERIMENT_CB2_LANDMARK_EXPANDED.md)
# ---------------------------------------------------------------------------

PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_CB2_LANDMARK_EXPANDED.md"
DUTTA_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "main_figure_6"
EXPANDED_DIR = ROOT / "data" / "external" / "cb2_landmark_expanded"
MANIFEST_PATH = EXPANDED_DIR / "MANIFEST.json"
TRAJ_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO"
ZIP_PATH = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO.zip"
TOPOLOGY = TRAJ_DIR / "CB2-APO_inactive_pr_1-strip.prmtop"
CACHE_DIR = TRAJ_DIR / "_cache_landmark_expanded"
NC_DIR = CACHE_DIR / "nc"
MANIFEST_CACHE = CACHE_DIR / "extract_manifest.json"
OWN_MSM_NC = TRAJ_DIR / "_cache_own_msm" / "nc"
PRIOR_LANDMARK_NC = TRAJ_DIR / "_cache_landmark_contacts" / "nc"

DUTTA_FILES = {
    "dutta_inactive": "CB2_ref_inactive_3_b.pdb",
    "dutta_I1": "CB2_ref_inactive_I1_b.pdb",
    "dutta_I2": "CB2_ref_inactive_I2_b.pdb",
    "dutta_I3": "CB2_ref_inactive_I3_b.pdb",
    "dutta_I4": "CB2_ref_inactive_I4_b.pdb",
    "dutta_active": "CB2_ref_inactive_active_b.pdb",
}
DUTTA_PATH_ORDER = [
    "dutta_inactive",
    "dutta_I1",
    "dutta_I2",
    "dutta_I3",
    "dutta_I4",
    "dutta_active",
]
RCSB_ACCESSIONS = [
    "5ZTY",
    "6KPC",
    "6KPF",
    "6PT0",
    "8GUR",
    "8GUS",
    "8GUQ",
    "8GUT",
    "8X3L",
    "9U7L",
]
RCSB_META = {
    "5ZTY": "inactive / antagonist AM10257",
    "6KPC": "active crystal / E3R",
    "6KPF": "active + Gi / AM12033-class",
    "6PT0": "active + Gi / WIN 55,212-2",
    "8GUR": "active + Gi / CP55,940",
    "8GUS": "active + Gi / HU-308",
    "8GUQ": "active + Gi / Olorinab (βarr-biased)",
    "8GUT": "active + Gi / LEI-102",
    "8X3L": "active + G / entropy-driven",
    "9U7L": "active + PAM Ec21a + CP55,940",
}

N_PER_STATE_DEFAULT = 50
EXTRACT_SEED = 20260913
SOFT_TAU_A = 2.0
MIN_MATCHED_CA = 250
MIN_ALIGN_IDENTITY_TOPO = 0.98
MIN_ALIGN_IDENTITY_UNIPROT = 0.90
MIN_FRAMES_LANDMARK = 100
MIN_OCCUPIED_LANDMARKS = 3
MIN_GATE0_LANDMARKS = 3
P_IJ_THR = float(CONTACT_DEF["p_ij_edge_threshold"])
CA_CUTOFF_A = 8.0
CA_MIN_SEP = 2
THR_MEAN_J_STABLE = 0.80
THR_FRAC_CORE_STABLE = 0.60
THR_FRAC_SPECIFIC_B = 0.15
THR_PATH_TURNOVER_B = 0.20
THR_MEAN_J_DIFFUSE = 0.55
PRIOR_DUTTA6_MEAN_J = 0.8214
MAX_CACHE_BYTES = 8 * (1 << 30)
MAX_WALL_S = 6 * 3600

OUT_DIR = ROOT / "results" / "network_core"
OUT_JSON = OUT_DIR / "cb2_landmark_expanded.json"
OUT_MD = OUT_DIR / "cb2_landmark_expanded.md"


def edge_key(u: str, v: str) -> tuple[str, str]:
    return (u, v) if u <= v else (v, u)


def resid_to_uniprot(seq: str, resids: list[int]) -> dict[str, Any]:
    """Map construct resid → UniProt position (1-indexed) via NW to P34972."""
    up_aln, seq_aln = nw_align(UNIPROT_P34972, seq)
    up_i = 0
    seq_i = 0
    resid_to_up: dict[int, int] = {}
    up_to_resid: dict[int, int] = {}
    offsets: list[int] = []
    n_match = 0
    n_aligned = 0
    for ua, sa in zip(up_aln, seq_aln):
        if ua != "-":
            up_i += 1
        if sa != "-":
            resid = resids[seq_i]
            seq_i += 1
            if ua != "-":
                n_aligned += 1
                offsets.append(resid - up_i)
                resid_to_up[resid] = up_i
                up_to_resid[up_i] = resid
                if ua == sa:
                    n_match += 1
    identity = float(n_match) / float(n_aligned) if n_aligned else 0.0
    return {
        "resid_to_uniprot": resid_to_up,
        "uniprot_to_resid": up_to_resid,
        "alignment_identity": identity,
        "n_aligned": n_aligned,
        "median_offset_resid_minus_uniprot": int(np.median(offsets)) if offsets else None,
        "n_residues": len(resids),
    }


def identity_vs_topo(topo_seq: str, other_seq: str) -> float:
    if topo_seq == other_seq:
        return 1.0
    a, b = nw_align(topo_seq, other_seq)
    n_m = n_a = 0
    for x, y in zip(a, b):
        if x != "-" and y != "-":
            n_a += 1
            if x == y:
                n_m += 1
    return float(n_m) / float(n_a) if n_a else 0.0


def pick_cb2_chain(u: mda.Universe) -> tuple[str | None, mda.AtomGroup | None, dict[str, Any]]:
    """Select best CB2-like chain by UniProt identity / length."""
    protein = u.select_atoms("protein")
    if len(protein) == 0:
        return None, None, {"reason": "no_protein"}
    chain_ids = sorted({(getattr(a, "chainID", "") or "").strip() or "_" for a in protein})
    candidates: list[dict[str, Any]] = []
    for cid in chain_ids:
        if cid == "_":
            ag = protein
        else:
            ag = protein.select_atoms(f"chainID {cid}")
        if len(ag) == 0:
            continue
        # Build a tiny universe-like residue iteration via ag.residues
        seq_parts: list[str] = []
        resids: list[int] = []
        for r in ag.residues:
            if r.resname in ("ACE", "NME"):
                continue
            aa = AA3_TO_1.get(r.resname)
            if aa is None:
                continue
            seq_parts.append(aa)
            resids.append(int(r.resid))
        seq = "".join(seq_parts)
        if len(seq) < 100:
            continue
        up = resid_to_uniprot(seq, resids)
        prefer = 1.0 if cid in ("R", "A") else 0.0
        candidates.append(
            {
                "chainID": cid,
                "n_aa": len(seq),
                "identity_uniprot": up["alignment_identity"],
                "ag": ag,
                "seq": seq,
                "resids": resids,
                "up": up,
                "score": up["alignment_identity"] * 1000 + len(seq) + prefer * 50,
            }
        )
    if not candidates:
        # single-chain / no chainID — treat whole protein
        seq, resids = protein_seq_resids(u)
        if len(seq) < 100:
            return None, None, {"reason": "no_cb2_chain", "detail": "short_seq"}
        up = resid_to_uniprot(seq, resids)
        return "_", protein, {"seq": seq, "resids": resids, "up": up, "chainID": "_"}
    candidates.sort(key=lambda x: x["score"], reverse=True)
    best = candidates[0]
    return (
        best["chainID"],
        best["ag"],
        {
            "seq": best["seq"],
            "resids": best["resids"],
            "up": best["up"],
            "chainID": best["chainID"],
            "candidates": [
                {k: v for k, v in c.items() if k != "ag"} for c in candidates[:5]
            ],
        },
    )


def landmark_catalog() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for lid, fn in DUTTA_FILES.items():
        items.append(
            {
                "id": lid,
                "kind": "dutta",
                "path": DUTTA_DIR / fn,
                "state_ligand": f"Dutta Fig.6 {lid} (geometric)",
                "accession": None,
            }
        )
    for acc in RCSB_ACCESSIONS:
        path = EXPANDED_DIR / f"{acc}.pdb"
        items.append(
            {
                "id": acc,
                "kind": "rcsb",
                "path": path,
                "state_ligand": RCSB_META[acc],
                "accession": acc,
            }
        )
    return items


def gate0_numbering() -> dict[str, Any]:
    """Per-landmark Gate0; drop failures; shared UniProt Cα index among passers."""
    if not TOPOLOGY.is_file():
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
            "reason": "prmtop_missing",
            "path": str(TOPOLOGY),
        }

    u_topo = mda.Universe(str(TOPOLOGY))
    if int(u_topo.atoms.n_atoms) != EXPECT_N_ATOMS:
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
            "reason": f"topo_n_atoms={u_topo.atoms.n_atoms} expected={EXPECT_N_ATOMS}",
        }

    topo_seq, topo_resids = protein_seq_resids(u_topo)
    topo_up = resid_to_uniprot(topo_seq, topo_resids)
    topo_ca = u_topo.select_atoms("protein and name CA")
    topo_ca_by_resid = {int(r): i for i, r in enumerate(topo_ca.resids)}
    # UniProt → topo CA index
    topo_up_to_caidx: dict[int, int] = {}
    for resid, upos in topo_up["resid_to_uniprot"].items():
        if resid in topo_ca_by_resid:
            topo_up_to_caidx[upos] = topo_ca_by_resid[resid]

    dropped: list[dict[str, Any]] = []
    passed: dict[str, Any] = {}
    per_up_sets: dict[str, set[int]] = {}

    for item in landmark_catalog():
        lid = item["id"]
        path: Path = item["path"]
        if not path.is_file():
            dropped.append(
                {
                    "id": lid,
                    "reason": "download_missing",
                    "path": str(path),
                }
            )
            continue
        try:
            u_pdb = mda.Universe(str(path))
        except Exception as e:
            dropped.append({"id": lid, "reason": "load_fail", "detail": str(e)})
            continue

        chain_id, ag, meta = pick_cb2_chain(u_pdb)
        if ag is None:
            dropped.append({"id": lid, "reason": "no_cb2_chain", "detail": meta})
            continue

        seq = meta["seq"]
        resids = meta["resids"]
        up = meta["up"]
        id_topo = identity_vs_topo(topo_seq, seq)
        id_up = float(up["alignment_identity"])

        # Pass identity: topo≥0.98 OR uniprot≥0.90
        if id_topo < MIN_ALIGN_IDENTITY_TOPO and id_up < MIN_ALIGN_IDENTITY_UNIPROT:
            dropped.append(
                {
                    "id": lid,
                    "reason": "alignment_identity",
                    "identity_topo": id_topo,
                    "identity_uniprot": id_up,
                    "thresholds": {
                        "topo": MIN_ALIGN_IDENTITY_TOPO,
                        "uniprot": MIN_ALIGN_IDENTITY_UNIPROT,
                    },
                }
            )
            continue

        # Build UniProt positions with CA on this landmark chain
        ca = ag.select_atoms("name CA")
        ca_by_resid = {int(r): i for i, r in enumerate(ca.resids)}
        pdb_aa = {}
        for r in ag.residues:
            aa = AA3_TO_1.get(r.resname)
            if aa:
                pdb_aa[int(r.resid)] = aa

        matched_up: list[int] = []
        for resid, upos in up["resid_to_uniprot"].items():
            if resid not in ca_by_resid:
                continue
            if upos not in topo_up_to_caidx:
                continue
            # AA agreement vs UniProt letter
            aa_pdb = pdb_aa.get(resid)
            aa_up = UNIPROT_P34972[upos - 1] if 1 <= upos <= len(UNIPROT_P34972) else None
            if aa_pdb is None or aa_up is None or aa_pdb != aa_up:
                continue
            matched_up.append(upos)

        matched_up = sorted(set(matched_up))
        if len(matched_up) < MIN_MATCHED_CA:
            dropped.append(
                {
                    "id": lid,
                    "reason": "insufficient_matched_ca",
                    "n_matched": len(matched_up),
                    "threshold": MIN_MATCHED_CA,
                    "identity_topo": id_topo,
                    "identity_uniprot": id_up,
                    "chainID": chain_id,
                }
            )
            continue

        # Landmark CA coords keyed temporarily by full matched set (trimmed later)
        idx = []
        for upos in matched_up:
            # reverse: uniprot → pdb resid
            pdb_resid = up["uniprot_to_resid"].get(upos)
            if pdb_resid is None or pdb_resid not in ca_by_resid:
                continue
            idx.append((upos, ca_by_resid[pdb_resid]))
        if len(idx) < MIN_MATCHED_CA:
            dropped.append(
                {
                    "id": lid,
                    "reason": "insufficient_matched_ca_after_index",
                    "n_matched": len(idx),
                }
            )
            continue
        matched_up = [u for u, _ in idx]
        ca_idx = [i for _, i in idx]
        coords_full = ca.positions[ca_idx].astype(np.float64).copy()

        passed[lid] = {
            "id": lid,
            "kind": item["kind"],
            "file": path.name,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path),
            "state_ligand": item["state_ligand"],
            "accession": item["accession"],
            "chainID": chain_id,
            "n_atoms_file": int(u_pdb.atoms.n_atoms),
            "n_ca_chain": len(ca),
            "identity_topo_pdb": id_topo,
            "identity_uniprot": id_up,
            "uniprot_align": {
                "alignment_identity": id_up,
                "median_offset_resid_minus_uniprot": up[
                    "median_offset_resid_minus_uniprot"
                ],
                "n_aligned": up["n_aligned"],
                "n_residues": up["n_residues"],
            },
            "n_matched_ca": len(matched_up),
            "matched_uniprot_head": matched_up[:5],
            "matched_uniprot_tail": matched_up[-5:],
            "_matched_uniprot": matched_up,
            "_coords_by_uniprot": {u: coords_full[i] for i, u in enumerate(matched_up)},
        }
        per_up_sets[lid] = set(matched_up)

    if len(passed) < MIN_GATE0_LANDMARKS:
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING",
            "reason": "too_few_landmarks_pass_gate0",
            "n_passed": len(passed),
            "dropped": dropped,
            "needed": "≥3 landmarks must pass Gate0 without inventing resid maps.",
        }

    # Common UniProt set; if too small, drop landmarks with smallest private contribution
    common = set.intersection(*(per_up_sets[k] for k in passed))
    drop_order = sorted(passed.keys(), key=lambda k: len(per_up_sets[k]))
    while len(common) < MIN_MATCHED_CA and len(passed) > MIN_GATE0_LANDMARKS:
        # Drop landmark that most reduces intersection when removed? Prefer drop smallest set.
        victim = drop_order.pop(0)
        if victim not in passed:
            continue
        dropped.append(
            {
                "id": victim,
                "reason": "dropped_to_enlarge_common_ca_set",
                "n_matched_private": len(per_up_sets[victim]),
                "n_common_before": len(common),
            }
        )
        del passed[victim]
        del per_up_sets[victim]
        if not per_up_sets:
            break
        common = set.intersection(*(per_up_sets[k] for k in passed))

    if len(passed) < MIN_GATE0_LANDMARKS or len(common) < MIN_MATCHED_CA:
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING",
            "reason": "common_ca_set_too_small",
            "n_common": len(common),
            "n_passed": len(passed),
            "dropped": dropped,
            "needed": "Reconcile UniProt Cα maps; do not invent offsets.",
        }

    common_up = sorted(common)
    # Topo CA indices in common UniProt order
    topo_ca_idx = [topo_up_to_caidx[u] for u in common_up]
    landmark_coords: dict[str, np.ndarray] = {}
    order = list(passed.keys())
    # Stable order: dutta path first, then RCSB alpha
    order = [k for k in DUTTA_PATH_ORDER if k in passed] + sorted(
        [k for k in passed if k not in DUTTA_PATH_ORDER]
    )

    for lid in order:
        coords = np.asarray(
            [passed[lid]["_coords_by_uniprot"][u] for u in common_up], dtype=np.float64
        )
        landmark_coords[lid] = coords
        passed[lid]["n_matched_ca_common"] = len(common_up)
        # strip heavy internals for serialization later
        del passed[lid]["_matched_uniprot"]
        del passed[lid]["_coords_by_uniprot"]

    return {
        "ok": True,
        "verdict": "GATE0_PASS",
        "topo_n_atoms": int(u_topo.atoms.n_atoms),
        "topo_n_ca": len(topo_ca),
        "topo_uniprot_align": {
            "alignment_identity": topo_up["alignment_identity"],
            "median_offset_resid_minus_uniprot": topo_up[
                "median_offset_resid_minus_uniprot"
            ],
            "n_aligned": topo_up["n_aligned"],
            "n_residues": topo_up["n_residues"],
        },
        "common_uniprot_positions": {
            "n": len(common_up),
            "head": common_up[:10],
            "tail": common_up[-10:],
        },
        "n_matched_ca": len(common_up),
        "topo_ca_match_idx": topo_ca_idx,
        "landmark_order": order,
        "per_landmark": passed,
        "dropped": dropped,
        "landmark_coords": landmark_coords,
        "note": (
            "Geometric landmark labels are structural refs only; "
            "NOT MSM metastable identity. Dropped PDBs listed in dropped[]."
        ),
    }


def cache_nbytes() -> int:
    if not CACHE_DIR.is_dir():
        return 0
    total = 0
    for p in CACHE_DIR.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def _acquire_nc(member: str, zf: zipfile.ZipFile | None) -> Path:
    name = Path(member).name
    dest = NC_DIR / name
    if dest.is_file():
        return dest
    for src_dir in (
        PRIOR_LANDMARK_NC,
        OWN_MSM_NC,
        TRAJ_DIR / "_tm6_sample25",
        TRAJ_DIR / "_pilot_sample",
    ):
        src = src_dir / name
        if src.is_file():
            try:
                dest.hardlink_to(src)
            except OSError:
                shutil.copy2(src, dest)
            return dest
    if zf is None:
        raise FileNotFoundError(f"missing {name} and zip handle closed")
    with zf.open(member) as src, dest.open("wb") as dst:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            dst.write(chunk)
    return dest


def extract_stratified(n_per_state: int, skip_extract: bool) -> dict[str, Any]:
    NC_DIR.mkdir(parents=True, exist_ok=True)
    if skip_extract and MANIFEST_CACHE.is_file():
        man = json.loads(MANIFEST_CACHE.read_text(encoding="utf-8"))
        files = man.get("files") or {}
        ok_files = True
        for st in ("inactive", "active"):
            for name in files.get(st, []):
                if not (NC_DIR / name).is_file():
                    ok_files = False
                    break
        if ok_files and len(files.get("inactive", [])) == n_per_state:
            man["reused"] = True
            return man

    if not ZIP_PATH.is_file() and not PRIOR_LANDMARK_NC.is_dir() and not OWN_MSM_NC.is_dir():
        return {"ok": False, "reason": "zip_missing", "path": str(ZIP_PATH)}

    by_state = (
        list_zip_nc_by_state(ZIP_PATH) if ZIP_PATH.is_file() else {"inactive": [], "active": []}
    )
    if not by_state["inactive"]:
        for src_dir in (PRIOR_LANDMARK_NC, OWN_MSM_NC):
            if not src_dir.is_dir():
                continue
            for p in sorted(src_dir.glob("*-strip.nc")):
                if "_inactive_" in p.name:
                    by_state["inactive"].append(p.name)
                elif "_active_" in p.name:
                    by_state["active"].append(p.name)

    rng = np.random.default_rng(EXTRACT_SEED)
    chosen: dict[str, list[str]] = {}
    for st in ("inactive", "active"):
        chosen[st] = choose_stratified(by_state[st], n_per_state, rng)

    keep_names = {Path(m).name for members in chosen.values() for m in members}
    for orphan in NC_DIR.glob("*.nc"):
        if orphan.name not in keep_names:
            try:
                orphan.unlink()
            except OSError:
                pass

    extracted: dict[str, list[str]] = {"inactive": [], "active": []}
    sources: dict[str, int] = {"cache_copy": 0, "zip": 0, "already": 0}
    bytes_written = 0
    t0 = time.time()
    zf: zipfile.ZipFile | None = None
    try:
        if ZIP_PATH.is_file():
            zf = zipfile.ZipFile(ZIP_PATH, "r")
        for st in ("inactive", "active"):
            for member in chosen[st]:
                if time.time() - t0 > MAX_WALL_S:
                    return {
                        "ok": False,
                        "reason": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
                        "detail": "walltime during extract",
                        "partial": extracted,
                    }
                if cache_nbytes() > MAX_CACHE_BYTES:
                    return {
                        "ok": False,
                        "reason": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
                        "detail": "disk during extract",
                        "partial": extracted,
                        "cache_nbytes": cache_nbytes(),
                    }
                name = Path(member).name
                dest = NC_DIR / name
                existed = dest.is_file()
                before = dest.stat().st_size if existed else 0
                if existed:
                    sources["already"] += 1
                else:
                    prior = any(
                        (d / name).is_file()
                        for d in (
                            PRIOR_LANDMARK_NC,
                            OWN_MSM_NC,
                            TRAJ_DIR / "_tm6_sample25",
                            TRAJ_DIR / "_pilot_sample",
                        )
                    )
                    _acquire_nc(member, zf)
                    if prior:
                        sources["cache_copy"] += 1
                    else:
                        sources["zip"] += 1
                        bytes_written += dest.stat().st_size - before
                extracted[st].append(name)
    finally:
        if zf is not None:
            zf.close()

    man = {
        "ok": True,
        "n_per_state": n_per_state,
        "dir": str(NC_DIR.relative_to(ROOT)),
        "files": extracted,
        "pool_sizes": {k: len(v) for k, v in by_state.items()},
        "bytes_written_this_run": bytes_written,
        "cache_nbytes": cache_nbytes(),
        "sources": sources,
        "reused": False,
        "seed": EXTRACT_SEED,
    }
    MANIFEST_CACHE.write_text(json.dumps(man, indent=2), encoding="utf-8")
    return man


def compute_metrics(
    edges: dict[str, set[tuple[str, str]]],
    occupied: list[str],
    path_order: list[str] | None,
) -> dict[str, Any]:
    n_edges = {k: len(edges.get(k, set())) for k in edges}
    pair_j: dict[str, float] = {}
    js: list[float] = []
    for i, a in enumerate(occupied):
        for b in occupied[i + 1 :]:
            jv = jaccard(edges[a], edges[b])
            pair_j[f"{a}|{b}"] = jv
            js.append(jv)
    mean_j = float(np.mean(js)) if js else 0.0
    min_j = float(np.min(js)) if js else 0.0
    max_j = float(np.max(js)) if js else 0.0

    if occupied:
        core = set.intersection(*(edges[k] for k in occupied))
        union = set.union(*(edges[k] for k in occupied))
        frac_core = float(len(core) / len(union)) if union else 0.0
    else:
        frac_core = 0.0

    spec_fracs: list[float] = []
    n_state_specific: dict[str, int] = {}
    for k in occupied:
        others = (
            set.union(*(edges[t] for t in occupied if t != k)) if len(occupied) > 1 else set()
        )
        private = edges[k] - others
        n_state_specific[k] = len(private)
        spec_fracs.append(len(private) / max(len(edges[k]), 1))
    frac_spec = float(np.mean(spec_fracs)) if spec_fracs else 0.0

    path_steps: list[dict[str, Any]] = []
    turnovers: list[float] = []
    path_turn: float | None = None
    if path_order and all(k in occupied for k in path_order):
        for a, b in zip(path_order, path_order[1:]):
            appear = edges[b] - edges[a]
            disappear = edges[a] - edges[b]
            u = edges[a] | edges[b]
            frac = float((len(appear) + len(disappear)) / len(u)) if u else 0.0
            turnovers.append(frac)
            path_steps.append(
                {
                    "step": f"{a}→{b}",
                    "appear": len(appear),
                    "disappear": len(disappear),
                    "turnover": frac,
                }
            )
        path_turn = float(np.mean(turnovers)) if turnovers else 0.0

    return {
        "n_edges": n_edges,
        "pairwise_jaccard": pair_j,
        "mean_jaccard": mean_j,
        "min_jaccard": min_j,
        "max_jaccard": max_j,
        "frac_core": frac_core,
        "frac_state_specific": frac_spec,
        "n_state_specific": n_state_specific,
        "path_turnover_frac": path_turn,
        "path_steps": path_steps,
        "path_defined": path_turn is not None,
        "occupied_landmarks": occupied,
        "delta_mean_j_vs_dutta6_prior": mean_j - PRIOR_DUTTA6_MEAN_J,
    }


def assign_verdicts(
    mean_j: float,
    frac_core: float,
    frac_spec: float,
    path_turn: float | None,
    n_occupied: int,
    blocked: str | None,
) -> dict[str, str]:
    if blocked:
        return {
            "EXT_LANDMARK_EXPANDED_CONTACTS": blocked,
            "Q_MAPS": "NA",
            "EXT_LANDMARK_EXPANDED_SOFT_COMPARE_DUTTA6": "EXT_LANDMARK_EXPANDED_SOFT_COMPARE_DUTTA6_NA",
            "EXT_LANDMARK_EXPANDED_SOFT_COMPARE_PDB": "EXT_LANDMARK_EXPANDED_SOFT_COMPARE_PDB_NA",
            "EXT_LANDMARK_GEOMETRIC_NEQ_MSM": "TRUE",
            "P2_STATUS_UNCHANGED": "CLOSED_ABORTED_NOT_CONVERGENT",
        }
    path_ok_for_b = path_turn is not None and path_turn >= THR_PATH_TURNOVER_B
    if n_occupied < MIN_OCCUPIED_LANDMARKS:
        primary = "EXT_LANDMARK_EXPANDED_INDETERMINATE"
    elif mean_j >= THR_MEAN_J_STABLE and frac_core >= THR_FRAC_CORE_STABLE:
        primary = "EXT_LANDMARK_EXPANDED_STABLE"
    elif frac_spec >= THR_FRAC_SPECIFIC_B or path_ok_for_b:
        primary = "EXT_LANDMARK_EXPANDED_STATE_DEPENDENT"
    elif frac_spec < THR_FRAC_SPECIFIC_B and mean_j < THR_MEAN_J_DIFFUSE:
        primary = "EXT_LANDMARK_EXPANDED_DIFFUSE"
    else:
        primary = "EXT_LANDMARK_EXPANDED_INDETERMINATE"

    differs = mean_j < THR_MEAN_J_STABLE or path_ok_for_b
    q = "DIFFERS_SUBSTANTIALLY" if differs else "SIMILAR_OVERALL"

    soft_d6 = (
        "EXT_LANDMARK_EXPANDED_SOFT_AGREE_DUTTA6_STABLE"
        if primary == "EXT_LANDMARK_EXPANDED_STABLE"
        else "EXT_LANDMARK_EXPANDED_SOFT_DISAGREE_DUTTA6_STABLE"
    )
    soft_pdb = (
        "EXT_LANDMARK_EXPANDED_SOFT_AGREE_PDB_B"
        if primary == "EXT_LANDMARK_EXPANDED_STATE_DEPENDENT"
        else "EXT_LANDMARK_EXPANDED_SOFT_DISAGREE_PDB_B"
    )
    return {
        "EXT_LANDMARK_EXPANDED_CONTACTS": primary,
        "Q_MAPS": q,
        "EXT_LANDMARK_EXPANDED_SOFT_COMPARE_DUTTA6": soft_d6,
        "EXT_LANDMARK_EXPANDED_SOFT_COMPARE_PDB": soft_pdb,
        "EXT_LANDMARK_GEOMETRIC_NEQ_MSM": "TRUE",
        "P2_STATUS_UNCHANGED": "CLOSED_ABORTED_NOT_CONVERGENT",
    }


def update_manifest_gate0(gate: dict[str, Any]) -> None:
    if not MANIFEST_PATH.is_file():
        return
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    man["gate0"] = {
        "ok": gate.get("ok"),
        "verdict": gate.get("verdict"),
        "n_matched_ca": gate.get("n_matched_ca"),
        "landmark_order": gate.get("landmark_order"),
        "dropped": gate.get("dropped"),
        "per_landmark": {
            k: {
                "sha256": v.get("sha256"),
                "chainID": v.get("chainID"),
                "identity_topo_pdb": v.get("identity_topo_pdb"),
                "identity_uniprot": v.get("identity_uniprot"),
                "n_matched_ca_common": v.get("n_matched_ca_common"),
                "state_ligand": v.get("state_ligand"),
            }
            for k, v in (gate.get("per_landmark") or {}).items()
        },
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    # fill sha256 for rcsb files
    for entry in man.get("rcsb_panel") or []:
        fp = EXPANDED_DIR / entry["file"]
        if fp.is_file():
            entry["sha256"] = sha256_file(fp)
            entry["bytes"] = fp.stat().st_size
    MANIFEST_PATH.write_text(json.dumps(man, indent=2), encoding="utf-8")


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    g0 = payload.get("gate0") or {}
    m = payload.get("metrics_primary") or {}
    lines = [
        "# EXTERNAL — CB2 expanded geometric landmark contact maps",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_LANDMARK_EXPANDED.md`",
        f"**Git SHA:** `{payload.get('git_sha', 'unknown')}`",
        "",
        "## Epistemology",
        "",
        "- EXTERNAL **geometric** labeling: nearest of Gate0-pass landmarks (Dutta-6 + cryo/crystal panel).",
        "- **Geometric proximity ≠ MSM metastable identity.** Not kinetic MSM; not P2; no Gi claims.",
        "- Soft compare to prior Dutta-6 STABLE (Jaccard≈0.82) and PDB snapshot B.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_LANDMARK_EXPANDED_CONTACTS']}`**",
        f"- Q maps: `{v['Q_MAPS']}`",
        f"- Soft vs Dutta-6 STABLE: `{v['EXT_LANDMARK_EXPANDED_SOFT_COMPARE_DUTTA6']}`",
        f"- Soft vs PDB snapshot B: `{v['EXT_LANDMARK_EXPANDED_SOFT_COMPARE_PDB']}`",
        f"- `EXT_LANDMARK_GEOMETRIC_NEQ_MSM` = `{v['EXT_LANDMARK_GEOMETRIC_NEQ_MSM']}`",
        f"- P2 unchanged: `{v['P2_STATUS_UNCHANGED']}`",
        "",
        "## Gate 0 — numbering / alignment (per-PDB drop)",
        "",
        f"- Pass: `{g0.get('ok')}`  verdict=`{g0.get('verdict')}`",
        f"- Matched Cα (common UniProt): `{g0.get('n_matched_ca')}`",
        f"- Landmark order (pass): `{g0.get('landmark_order')}`",
        f"- Topo UniProt median offset (resid−UP): "
        f"`{(g0.get('topo_uniprot_align') or {}).get('median_offset_resid_minus_uniprot')}`",
        f"- Dropped: `{len(g0.get('dropped') or [])}`",
    ]
    for d in g0.get("dropped") or []:
        lines.append(f"  - `{d.get('id')}`: `{d.get('reason')}`")
    for lid in g0.get("landmark_order") or []:
        pl = (g0.get("per_landmark") or {}).get(lid) or {}
        lines.append(
            f"  - PASS `{lid}` chain=`{pl.get('chainID')}` "
            f"id_topo=`{pl.get('identity_topo_pdb')}` id_UP=`{pl.get('identity_uniprot')}` "
            f"— {pl.get('state_ligand')}"
        )
    lines += [
        "",
        "## Contact definition",
        "",
        "- Primary: `getcontacts_vdw_envelope_plus_alloviz_filters` — |AB| < Rvdw(A)+Rvdw(B)+0.5 Å",
        f"- Exclude sequential `|Δresid|==1`: `{CONTACT_DEF['exclude_sequential_protein']}`",
        f"- p_ij thr: `{P_IJ_THR}` within hard-assigned landmark frames",
        f"- Hard assign: argmin RMSD; soft τ=`{payload.get('soft_tau_A')}` Å (sensitivity)",
        "",
        "## Sampling",
        "",
    ]
    ex = payload.get("extract") or {}
    lines.append(
        f"- N_per_state=`{ex.get('n_per_state')}` seed=`{ex.get('seed')}` "
        f"cache=`{ex.get('dir')}` sources=`{ex.get('sources')}`"
    )
    occ = payload.get("occupancy") or {}
    order = g0.get("landmark_order") or list(occ.keys())
    if occ:
        lines += ["", "## Hard-assign occupancy", ""]
        for st in order:
            o = occ.get(st) or {}
            lines.append(
                f"- `{st}`: n_frames=`{o.get('n_frames')}` frac=`{o.get('frac')}` "
                f"mean_rmsd=`{o.get('mean_rmsd')}` LOW_N=`{o.get('low_n')}`"
            )
    if m:
        lines += [
            "",
            "## Pairwise Jaccard (primary VdW, occupied landmarks)",
            "",
            f"- mean=`{m.get('mean_jaccard'):.4f}`  min=`{m.get('min_jaccard'):.4f}`  "
            f"max=`{m.get('max_jaccard'):.4f}`",
            f"- frac_core=`{m.get('frac_core'):.4f}`  frac_state_specific=`{m.get('frac_state_specific'):.4f}`",
            f"- path_turnover_frac=`{m.get('path_turnover_frac')}`  "
            f"(Dutta-6 path defined=`{m.get('path_defined')}`)",
            f"- Δmean_j vs Dutta-6 prior (0.8214): `{m.get('delta_mean_j_vs_dutta6_prior')}`",
            "",
            "### n_edges",
            "",
        ]
        for st in order:
            lines.append(f"- `{st}`: `{m.get('n_edges', {}).get(st)}`")
        if m.get("path_steps"):
            lines += ["", "### Path turnover (Dutta-6 subset)", ""]
            for step in m.get("path_steps") or []:
                lines.append(
                    f"- `{step['step']}`: appear={step['appear']} disappear={step['disappear']} "
                    f"turnover={step['turnover']:.3f}"
                )
    soft = payload.get("soft_sensitivity") or {}
    if soft:
        lines += [
            "",
            "## Soft-weight sensitivity (does not drive primary)",
            "",
            f"- mean soft entropy (nats): `{soft.get('mean_entropy')}`",
            f"- soft mean_jaccard: `{soft.get('mean_jaccard')}`",
            f"- soft class (annotation): `{soft.get('soft_class_annotation')}`",
            f"- differs from hard primary class: `{soft.get('differs_from_hard')}`",
        ]
    lines += [
        "",
        "## Resumen PI (ES)",
        "",
        payload.get("pi_summary_es", ""),
        "",
        "## Forbidden",
        "",
        "- No Gi claims; no docking; no P2 CONVERGENT; landmark ≠ MSM state.",
        "",
    ]
    return "\n".join(lines) + "\n"


def write_blocked(verdict: str, detail: dict[str, Any], git_sha: str) -> dict[str, Any]:
    payload = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "branch": "feat/cb2-hubs-functional-topology-test",
        "git_sha": git_sha,
        "prereg": str(PREREG.relative_to(ROOT)),
        "gate0": detail,
        "verdicts": assign_verdicts(0, 0, 0, None, 0, verdict),
        "soft_tau_A": SOFT_TAU_A,
        "pi_summary_es": (
            f"Experimento landmark expandido **bloqueado** (`{verdict}`). "
            f"Motivo: {detail.get('reason')}. "
            f"{detail.get('needed', '')} "
            "PDBs droppeados documentados. Geometric ≠ MSM; P2 sin cambios."
        ),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    g0 = dict(payload["gate0"])
    g0.pop("landmark_coords", None)
    g0.pop("topo_ca_match_idx", None)
    payload["gate0"] = g0
    update_manifest_gate0(g0)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    return payload


def run(n_per_state: int, skip_extract: bool, tau: float, git_sha: str) -> dict[str, Any]:
    t_start = time.time()
    if not PREREG.is_file():
        raise SystemExit(f"Pre-registration missing: {PREREG}")

    print("[expanded] Gate 0 — numbering / alignment …", flush=True)
    gate = gate0_numbering()
    if not gate.get("ok"):
        print(
            f"[expanded] Gate 0 FAIL: {gate.get('verdict')} {gate.get('reason')}",
            flush=True,
        )
        return write_blocked(str(gate.get("verdict")), gate, git_sha)

    landmark_coords: dict[str, np.ndarray] = gate.pop("landmark_coords")
    topo_ca_match_idx = np.asarray(gate.pop("topo_ca_match_idx"), dtype=np.int32)
    lm_order: list[str] = gate["landmark_order"]
    print(
        f"[expanded] Gate 0 PASS: n_landmarks={len(lm_order)} "
        f"n_matched_ca={gate['n_matched_ca']} dropped={len(gate.get('dropped') or [])}",
        flush=True,
    )
    for d in gate.get("dropped") or []:
        print(f"[expanded]   DROP {d.get('id')}: {d.get('reason')}", flush=True)
    update_manifest_gate0({**gate, "ok": True})

    print(f"[expanded] extracting stratified {n_per_state}+{n_per_state} …", flush=True)
    extract = extract_stratified(n_per_state, skip_extract=skip_extract)
    if not extract.get("ok"):
        return write_blocked(
            "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
            {"ok": False, "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA", **extract},
            git_sha,
        )
    print(f"[expanded] extract sources={extract.get('sources')}", flush=True)

    u0 = mda.Universe(str(TOPOLOGY))
    tables = build_protein_tables(u0)
    labels = tables["unique_labels"]
    n_lab = tables["n_labels"]
    ca0 = u0.select_atoms("protein and name CA")

    ca_labels = [res_label(rn, int(ri)) for rn, ri in zip(ca0.resnames, ca0.resids)]
    ca_unique: list[str] = []
    ca_unique_index: dict[str, int] = {}
    ca_lab_idx = []
    for lab in ca_labels:
        if lab not in ca_unique_index:
            ca_unique_index[lab] = len(ca_unique)
            ca_unique.append(lab)
        ca_lab_idx.append(ca_unique_index[lab])
    ca_lab_idx_arr = np.asarray(ca_lab_idx, dtype=np.int32)
    ca_resnums = ca0.resids.astype(int)
    n_ca_lab = len(ca_unique)

    lm_targets = [landmark_coords[st] for st in lm_order]
    n_lm = len(lm_order)

    hard_counts = {st: np.zeros((n_lab, n_lab), dtype=np.int32) for st in lm_order}
    soft_counts = {st: np.zeros((n_lab, n_lab), dtype=np.float64) for st in lm_order}
    ca_counts = {st: np.zeros((n_ca_lab, n_ca_lab), dtype=np.int32) for st in lm_order}
    n_frames_lm = {st: 0 for st in lm_order}
    soft_mass = {st: 0.0 for st in lm_order}
    rmsd_sum = {st: 0.0 for st in lm_order}
    soft_entropy_sum = 0.0
    total_frames = 0
    assign_hist = np.zeros(n_lm, dtype=np.int64)

    nc_files: list[Path] = []
    for st in ("inactive", "active"):
        for name in extract["files"][st]:
            nc_files.append(NC_DIR / name)

    n_traj = len(nc_files)
    for ti, nc in enumerate(nc_files, start=1):
        if time.time() - t_start > MAX_WALL_S:
            return write_blocked(
                "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
                {
                    "ok": False,
                    "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
                    "reason": "walltime_during_analysis",
                    "processed_trajs": ti - 1,
                },
                git_sha,
            )
        print(f"[expanded] traj {ti}/{n_traj}: {nc.name}", flush=True)
        u = mda.Universe(str(TOPOLOGY), str(nc))
        if int(u.atoms.n_atoms) != EXPECT_N_ATOMS:
            return write_blocked(
                "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
                {
                    "ok": False,
                    "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_DATA",
                    "reason": f"{nc.name} n_atoms={u.atoms.n_atoms}",
                },
                git_sha,
            )
        heavy = u.select_atoms("protein").select_atoms("not name H*")
        cas = u.select_atoms("protein and name CA")
        if list(map(int, cas.resids)) != list(map(int, ca0.resids)):
            return write_blocked(
                "EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING",
                {
                    "ok": False,
                    "verdict": "EXT_LANDMARK_EXPANDED_BLOCKED_NUMBERING",
                    "reason": "traj_ca_resid_order_mismatch",
                    "file": nc.name,
                },
                git_sha,
            )

        for _ts in u.trajectory:
            mobile = cas.positions[topo_ca_match_idx].astype(np.float64)
            rmsds = np.asarray([kabsch_rmsd(mobile, tgt) for tgt in lm_targets], dtype=np.float64)
            hard_i = int(np.argmin(rmsds))
            hard_st = lm_order[hard_i]
            w = softmax_neg_rmsd(rmsds, tau)
            ent = float(-(w * np.log(np.clip(w, 1e-12, 1.0))).sum())
            soft_entropy_sum += ent

            hpos = heavy.positions
            tmp_f = np.zeros((n_lab, n_lab), dtype=np.float64)
            accumulate_frame_contacts(hpos, tables, tmp_f)
            hard_counts[hard_st] += tmp_f.astype(np.int32)
            accumulate_frame_ca(
                cas.positions, ca_resnums, ca_lab_idx_arr, n_ca_lab, ca_counts[hard_st]
            )
            n_frames_lm[hard_st] += 1
            rmsd_sum[hard_st] += float(rmsds[hard_i])
            assign_hist[hard_i] += 1

            for ki, st_k in enumerate(lm_order):
                soft_counts[st_k] += w[ki] * tmp_f
                soft_mass[st_k] += float(w[ki])

            total_frames += 1

        del u

    occupancy: dict[str, Any] = {}
    occupied: list[str] = []
    for st in lm_order:
        nf = int(n_frames_lm[st])
        low = nf < MIN_FRAMES_LANDMARK
        occupancy[st] = {
            "n_frames": nf,
            "frac": float(nf / total_frames) if total_frames else 0.0,
            "mean_rmsd": float(rmsd_sum[st] / nf) if nf else None,
            "low_n": low,
        }
        if not low:
            occupied.append(st)

    edges: dict[str, set[tuple[str, str]]] = {}
    edges_ca: dict[str, set[tuple[str, str]]] = {}
    for st in lm_order:
        edges[st] = edges_from_counts(hard_counts[st], n_frames_lm[st], labels, P_IJ_THR)
        edges_ca[st] = edges_from_counts(ca_counts[st], n_frames_lm[st], ca_unique, P_IJ_THR)

    path_order = DUTTA_PATH_ORDER if all(k in occupied for k in DUTTA_PATH_ORDER) else None
    metrics = compute_metrics(edges, occupied, path_order)
    ca_js = [jaccard(edges[st], edges_ca[st]) for st in occupied]
    metrics["mean_jaccard_primary_vs_ca"] = float(np.mean(ca_js)) if ca_js else None

    verdicts = assign_verdicts(
        metrics["mean_jaccard"],
        metrics["frac_core"],
        metrics["frac_state_specific"],
        metrics["path_turnover_frac"],
        len(occupied),
        None,
    )

    soft_edges: dict[str, set[tuple[str, str]]] = {}
    for st in lm_order:
        mass = soft_mass[st]
        se: set[tuple[str, str]] = set()
        if mass > 0:
            thr_count = P_IJ_THR * mass
            for i in range(n_lab):
                for j in range(i + 1, n_lab):
                    if float(soft_counts[st][i, j]) >= thr_count:
                        se.add(edge_key(labels[i], labels[j]))
        soft_edges[st] = se
    soft_occ = [st for st in lm_order if soft_mass[st] >= MIN_FRAMES_LANDMARK]
    soft_path = DUTTA_PATH_ORDER if all(k in soft_occ for k in DUTTA_PATH_ORDER) else None
    soft_metrics = compute_metrics(soft_edges, soft_occ, soft_path)
    soft_verdicts = assign_verdicts(
        soft_metrics["mean_jaccard"],
        soft_metrics["frac_core"],
        soft_metrics["frac_state_specific"],
        soft_metrics["path_turnover_frac"],
        len(soft_occ),
        None,
    )
    soft_sensitivity = {
        "mean_entropy": float(soft_entropy_sum / total_frames) if total_frames else None,
        "mean_jaccard": soft_metrics["mean_jaccard"],
        "frac_core": soft_metrics["frac_core"],
        "frac_state_specific": soft_metrics["frac_state_specific"],
        "path_turnover_frac": soft_metrics["path_turnover_frac"],
        "soft_class_annotation": soft_verdicts["EXT_LANDMARK_EXPANDED_CONTACTS"],
        "differs_from_hard": soft_verdicts["EXT_LANDMARK_EXPANDED_CONTACTS"]
        != verdicts["EXT_LANDMARK_EXPANDED_CONTACTS"],
        "soft_mass": {k: float(v) for k, v in soft_mass.items()},
    }
    if soft_sensitivity["differs_from_hard"]:
        verdicts["EXT_LANDMARK_SOFT_SENSITIVITY"] = "TRUE"

    dropped_ids = [d.get("id") for d in (gate.get("dropped") or [])]
    pi = (
        f"Landmark geométrico CB2 expandido (Dutta-6 + panel cryo/cristal): "
        f"Gate0 OK (landmarks={len(lm_order)}, Cα comunes={gate['n_matched_ca']}, "
        f"drop={dropped_ids or 'ninguno'}). "
        f"N={n_per_state}+{n_per_state} trajs, frames={total_frames}. "
        f"Veredicto duro: **{verdicts['EXT_LANDMARK_EXPANDED_CONTACTS']}** "
        f"(mean Jaccard={metrics['mean_jaccard']:.3f}, "
        f"Δ vs Dutta-6 prior={metrics['delta_mean_j_vs_dutta6_prior']:.3f}, "
        f"frac_core={metrics['frac_core']:.3f}, "
        f"path_turnover={metrics['path_turnover_frac']}). "
        f"Soft Dutta-6: {verdicts['EXT_LANDMARK_EXPANDED_SOFT_COMPARE_DUTTA6']}. "
        f"Soft PDB-B: {verdicts['EXT_LANDMARK_EXPANDED_SOFT_COMPARE_PDB']}. "
        f"Importante: proximidad geométrica ≠ identidad MSM; sin claims Gi. "
        f"P2 sin cambios. SHA `{git_sha}`."
    )

    gate_out = {k: v for k, v in gate.items() if k not in ("landmark_coords", "topo_ca_match_idx")}

    payload: dict[str, Any] = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "branch": "feat/cb2-hubs-functional-topology-test",
        "git_sha": git_sha,
        "prereg": str(PREREG.relative_to(ROOT)),
        "contact_def": {
            "name": CONTACT_DEF["name"],
            "slack_A": CONTACT_DEF["slack_A"],
            "exclude_sequential_protein": CONTACT_DEF["exclude_sequential_protein"],
            "p_ij_edge_threshold": P_IJ_THR,
        },
        "soft_tau_A": tau,
        "prior_dutta6_mean_jaccard": PRIOR_DUTTA6_MEAN_J,
        "gate0": gate_out,
        "extract": {k: extract[k] for k in extract if k != "zip_members"},
        "n_trajs": n_traj,
        "total_frames": total_frames,
        "occupancy": occupancy,
        "assign_hist": {lm_order[i]: int(assign_hist[i]) for i in range(n_lm)},
        "metrics_primary": metrics,
        "metrics_ca_secondary": {
            "n_edges": {st: len(edges_ca[st]) for st in lm_order},
            "mean_jaccard_vs_primary": metrics.get("mean_jaccard_primary_vs_ca"),
        },
        "soft_sensitivity": soft_sensitivity,
        "verdicts": verdicts,
        "wall_s": float(time.time() - t_start),
        "pi_summary_es": pi,
        "epistemology": {
            "geometric_neq_msm": True,
            "not_kinetic_msm": True,
            "not_dutta_pickles": True,
            "p2_unchanged": True,
            "no_gi_claims": True,
            "external_only": True,
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(
        f"[expanded] done verdict={verdicts['EXT_LANDMARK_EXPANDED_CONTACTS']} "
        f"wall_s={payload['wall_s']:.1f}",
        flush=True,
    )
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-per-state", type=int, default=N_PER_STATE_DEFAULT)
    ap.add_argument("--skip-extract", action="store_true")
    ap.add_argument("--tau", type=float, default=SOFT_TAU_A)
    ap.add_argument("--gate0-only", action="store_true", help="Run Gate0 and exit")
    args = ap.parse_args()

    import subprocess

    try:
        git_sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True)
            .strip()
        )
    except Exception:
        git_sha = "unknown"

    if args.gate0_only:
        gate = gate0_numbering()
        gate.pop("landmark_coords", None)
        gate.pop("topo_ca_match_idx", None)
        update_manifest_gate0(gate)
        print(json.dumps({k: gate[k] for k in gate if k != "per_landmark"}, indent=2))
        print("passed:", gate.get("landmark_order"))
        print("dropped:", [(d.get("id"), d.get("reason")) for d in gate.get("dropped") or []])
        return

    run(args.n_per_state, args.skip_extract, args.tau, git_sha)


if __name__ == "__main__":
    main()
