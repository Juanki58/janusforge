#!/usr/bin/env python3
"""EXTERNAL — CB2 geometric landmark contact maps (Dutta Fig. 6 refs).

Governance: docs/synthesis/EXPERIMENT_CB2_LANDMARK_CONTACTS.md (pre-registered).
  - Geometric proximity labeling (RMSD Cα) to 6 PDB landmarks.
  - NOT kinetic MSM; NOT Dutta I1–I4 from pickles; NOT P2 reopen; no Gi.
  - Geometric proximity ≠ MSM metastable identity.

Outputs:
  results/network_core/cb2_landmark_contacts.{md,json}
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

try:
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import capped_distance
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required: {e}") from e

# ---------------------------------------------------------------------------
# Locked a priori (see EXPERIMENT_CB2_LANDMARK_CONTACTS.md)
# ---------------------------------------------------------------------------

PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_CB2_LANDMARK_CONTACTS.md"
PDB_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "main_figure_6"
MANIFEST_PDB = PDB_DIR / "MANIFEST.json"
TRAJ_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO"
ZIP_PATH = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO.zip"
TOPOLOGY = TRAJ_DIR / "CB2-APO_inactive_pr_1-strip.prmtop"
CACHE_DIR = TRAJ_DIR / "_cache_landmark_contacts"
NC_DIR = CACHE_DIR / "nc"
MANIFEST_CACHE = CACHE_DIR / "extract_manifest.json"
OWN_MSM_NC = TRAJ_DIR / "_cache_own_msm" / "nc"

STATE_ORDER = ["inactive", "I1", "I2", "I3", "I4", "active"]
STATE_FILES = {
    "inactive": "CB2_ref_inactive_3_b.pdb",
    "I1": "CB2_ref_inactive_I1_b.pdb",
    "I2": "CB2_ref_inactive_I2_b.pdb",
    "I3": "CB2_ref_inactive_I3_b.pdb",
    "I4": "CB2_ref_inactive_I4_b.pdb",
    "active": "CB2_ref_inactive_active_b.pdb",
}

UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

N_PER_STATE_DEFAULT = 50
EXTRACT_SEED = 20260913
SOFT_TAU_A = 2.0
EXPECT_N_ATOMS = 4566
MIN_MATCHED_CA = 250
MIN_ALIGN_IDENTITY = 0.98
MIN_FRAMES_LANDMARK = 100
MIN_OCCUPIED_LANDMARKS = 3
P_IJ_THR = float(CONTACT_DEF["p_ij_edge_threshold"])
CA_CUTOFF_A = 8.0
CA_MIN_SEP = 2
THR_MEAN_J_STABLE = 0.80
THR_FRAC_CORE_STABLE = 0.60
THR_FRAC_SPECIFIC_B = 0.15
THR_PATH_TURNOVER_B = 0.20
THR_MEAN_J_DIFFUSE = 0.55
MAX_CACHE_BYTES = 8 * (1 << 30)
MAX_WALL_S = 6 * 3600

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
    "HIE": "H",
    "HID": "H",
    "HIP": "H",
    "HIS": "H",
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

OUT_DIR = ROOT / "results" / "network_core"
OUT_JSON = OUT_DIR / "cb2_landmark_contacts.json"
OUT_MD = OUT_DIR / "cb2_landmark_contacts.md"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jaccard(a: set[tuple[str, str]], b: set[tuple[str, str]]) -> float:
    if not a and not b:
        return 0.0
    union = a | b
    return float(len(a & b) / len(union)) if union else 0.0


def edge_key(u: str, v: str) -> tuple[str, str]:
    return (u, v) if u <= v else (v, u)


def nw_align(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> tuple[str, str]:
    n, m = len(a), len(b)
    score = np.zeros((n + 1, m + 1), dtype=np.int32)
    ptr = np.zeros((n + 1, m + 1), dtype=np.uint8)
    for i in range(1, n + 1):
        score[i, 0] = i * gap
        ptr[i, 0] = 1
    for j in range(1, m + 1):
        score[0, j] = j * gap
        ptr[0, j] = 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            s = match if ai == b[j - 1] else mismatch
            diag = score[i - 1, j - 1] + s
            up = score[i - 1, j] + gap
            left = score[i, j - 1] + gap
            best, p = diag, 0
            if up > best:
                best, p = up, 1
            if left > best:
                best, p = left, 2
            score[i, j] = best
            ptr[i, j] = p
    i, j = n, m
    ra: list[str] = []
    rb: list[str] = []
    while i > 0 or j > 0:
        p = ptr[i, j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if i > 0 and j > 0 and p == 0:
            ra.append(a[i - 1])
            rb.append(b[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or p == 1):
            ra.append(a[i - 1])
            rb.append("-")
            i -= 1
        else:
            ra.append("-")
            rb.append(b[j - 1])
            j -= 1
    return "".join(reversed(ra)), "".join(reversed(rb))


def protein_seq_resids(u: mda.Universe) -> tuple[str, list[int]]:
    resids: list[int] = []
    aas: list[str] = []
    for r in u.residues:
        if r.resname in ("ACE", "NME"):
            continue
        aa = AA3_TO_1.get(r.resname)
        if aa is None:
            continue
        resids.append(int(r.resid))
        aas.append(aa)
    return "".join(aas), resids


def align_to_uniprot(seq: str, resids: list[int]) -> dict[str, Any]:
    up_aln, seq_aln = nw_align(UNIPROT_P34972, seq)
    up_i = 0
    seq_i = 0
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
                if ua == sa:
                    n_match += 1
    identity = float(n_match) / float(n_aligned) if n_aligned else 0.0
    return {
        "alignment_identity": identity,
        "n_aligned": n_aligned,
        "median_offset_resid_minus_uniprot": int(np.median(offsets)) if offsets else None,
        "n_residues": len(resids),
    }


def kabsch_rmsd(mobile: np.ndarray, target: np.ndarray) -> float:
    """RMSD after Kabsch superposition (Å). mobile/target shape (N, 3)."""
    p = mobile - mobile.mean(axis=0)
    q = target - target.mean(axis=0)
    c = p.T @ q
    v, _s, wt = np.linalg.svd(c)
    d = np.sign(np.linalg.det(v @ wt))
    u = v @ np.diag([1.0, 1.0, d]) @ wt
    rotated = p @ u
    diff = rotated - q
    return float(np.sqrt((diff * diff).sum() / len(p)))


def softmax_neg_rmsd(rmsds: np.ndarray, tau: float) -> np.ndarray:
    x = -rmsds / float(tau)
    x = x - x.max()
    e = np.exp(x)
    return e / e.sum()


def list_zip_nc_by_state(zip_path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"inactive": [], "active": []}
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            base = Path(name).name
            if not base.endswith("-strip.nc"):
                continue
            if "_inactive_" in base:
                out["inactive"].append(name)
            elif "_active_" in base:
                out["active"].append(name)
    for k in out:
        out[k] = sorted(out[k])
    return out


def choose_stratified(pool: list[str], n: int, rng: np.random.Generator) -> list[str]:
    if len(pool) < n:
        raise RuntimeError(f"pool size {len(pool)} < requested {n}")
    idx = np.linspace(0, len(pool) - 1, n, dtype=int)
    chosen = sorted(set(int(i) for i in idx))
    while len(chosen) < n:
        extra = int(rng.integers(0, len(pool)))
        if extra not in chosen:
            chosen.append(extra)
    return [pool[i] for i in sorted(chosen)[:n]]


def cache_nbytes() -> int:
    if not CACHE_DIR.is_dir():
        return 0
    total = 0
    for p in CACHE_DIR.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def _acquire_nc(member: str, zf: zipfile.ZipFile | None) -> Path:
    """Place member basename into NC_DIR via existing cache copy or zip extract."""
    name = Path(member).name
    dest = NC_DIR / name
    if dest.is_file():
        return dest
    for src_dir in (OWN_MSM_NC, TRAJ_DIR / "_tm6_sample25", TRAJ_DIR / "_pilot_sample"):
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

    if not ZIP_PATH.is_file() and not OWN_MSM_NC.is_dir():
        return {"ok": False, "reason": "zip_missing", "path": str(ZIP_PATH)}

    by_state = list_zip_nc_by_state(ZIP_PATH) if ZIP_PATH.is_file() else {"inactive": [], "active": []}
    if not by_state["inactive"] and OWN_MSM_NC.is_dir():
        # Fallback listing from own_msm cache only (should not be primary path)
        for p in sorted(OWN_MSM_NC.glob("*-strip.nc")):
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
                        "reason": "EXT_LANDMARK_BLOCKED_DATA",
                        "detail": "walltime during extract",
                        "partial": extracted,
                    }
                if cache_nbytes() > MAX_CACHE_BYTES:
                    return {
                        "ok": False,
                        "reason": "EXT_LANDMARK_BLOCKED_DATA",
                        "detail": "disk during extract",
                        "partial": extracted,
                        "cache_nbytes": cache_nbytes(),
                    }
                name = Path(member).name
                dest = NC_DIR / name
                existed = dest.is_file()
                before = dest.stat().st_size if existed else 0
                src_own = OWN_MSM_NC / name
                if existed:
                    sources["already"] += 1
                elif src_own.is_file() or any(
                    (d / name).is_file()
                    for d in (TRAJ_DIR / "_tm6_sample25", TRAJ_DIR / "_pilot_sample")
                ):
                    _acquire_nc(member, zf)
                    sources["cache_copy"] += 1
                else:
                    _acquire_nc(member, zf)
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
        "zip_members": {k: [Path(m).name for m in v] for k, v in chosen.items()},
        "pool_sizes": {k: len(v) for k, v in by_state.items()},
        "bytes_written_this_run": bytes_written,
        "cache_nbytes": cache_nbytes(),
        "sources": sources,
        "reused": False,
        "seed": EXTRACT_SEED,
    }
    MANIFEST_CACHE.write_text(json.dumps(man, indent=2), encoding="utf-8")
    return man


def build_protein_tables(u: mda.Universe) -> dict[str, Any]:
    sel = u.select_atoms("protein")
    heavy = sel.select_atoms("not name H*")
    elements: list[str] = []
    for atom in heavy:
        el = (atom.element if hasattr(atom, "element") else "").upper()
        if not el or el == "DUMMY":
            el = "".join(c for c in atom.name if c.isalpha())[:2].upper()
            if el.startswith("CL"):
                el = "CL"
            elif el.startswith("BR"):
                el = "BR"
            else:
                el = el[:1] if el else "C"
        if el not in _VDW:
            el = "C"
        elements.append(el)
    labels = [res_label(rn, int(ri)) for rn, ri in zip(heavy.resnames, heavy.resids)]
    unique_labels = sorted(set(labels), key=lambda x: (x.split(":")[0], int(x.split(":")[1])))
    label_index = {lab: i for i, lab in enumerate(unique_labels)}
    atom_lab_idx = np.asarray([label_index[lab] for lab in labels], dtype=np.int32)
    radii = np.asarray([_VDW[e] for e in elements], dtype=np.float64)
    protein_mask = np.ones(len(unique_labels), dtype=bool)
    resnums = np.asarray([int(lab.split(":")[1]) for lab in unique_labels], dtype=np.int32)
    return {
        "heavy": heavy,
        "unique_labels": unique_labels,
        "atom_lab_idx": atom_lab_idx,
        "radii": radii,
        "protein_mask": protein_mask,
        "resnums": resnums,
        "n_labels": len(unique_labels),
    }


def gate0_numbering() -> dict[str, Any]:
    """Verify PDB landmarks ↔ topo Cα correspondence. Fail closed on mismatch."""
    if not TOPOLOGY.is_file():
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_BLOCKED_DATA",
            "reason": "prmtop_missing",
            "path": str(TOPOLOGY),
        }
    for st, fn in STATE_FILES.items():
        if not (PDB_DIR / fn).is_file():
            return {
                "ok": False,
                "verdict": "EXT_LANDMARK_BLOCKED_DATA",
                "reason": "landmark_pdb_missing",
                "state": st,
                "path": str(PDB_DIR / fn),
            }

    u_topo = mda.Universe(str(TOPOLOGY))
    if int(u_topo.atoms.n_atoms) != EXPECT_N_ATOMS:
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_BLOCKED_ATOMCOUNT",
            "reason": f"topo_n_atoms={u_topo.atoms.n_atoms} expected={EXPECT_N_ATOMS}",
        }

    topo_seq, topo_resids = protein_seq_resids(u_topo)
    topo_up = align_to_uniprot(topo_seq, topo_resids)
    topo_ca = u_topo.select_atoms("protein and name CA")
    topo_ca_by_resid = {int(r): i for i, r in enumerate(topo_ca.resids)}

    per_landmark: dict[str, Any] = {}
    matched_resid_sets: list[set[int]] = []

    for st in STATE_ORDER:
        path = PDB_DIR / STATE_FILES[st]
        u_pdb = mda.Universe(str(path))
        pdb_seq, pdb_resids = protein_seq_resids(u_pdb)
        pdb_up = align_to_uniprot(pdb_seq, pdb_resids)
        identity_topo = 1.0 if pdb_seq == topo_seq else 0.0
        if pdb_seq != topo_seq:
            # NW identity topo↔pdb
            a, b = nw_align(topo_seq, pdb_seq)
            n_m = n_a = 0
            for x, y in zip(a, b):
                if x != "-" and y != "-":
                    n_a += 1
                    if x == y:
                        n_m += 1
            identity_topo = float(n_m) / float(n_a) if n_a else 0.0

        if identity_topo < MIN_ALIGN_IDENTITY:
            return {
                "ok": False,
                "verdict": "EXT_LANDMARK_BLOCKED_NUMBERING",
                "reason": "alignment_identity_below_threshold",
                "state": st,
                "identity_topo_pdb": identity_topo,
                "threshold": MIN_ALIGN_IDENTITY,
                "needed": (
                    "Provide explicit resid map PDB→topo (or matching construct PDBs). "
                    "Do not invent offsets."
                ),
            }

        if int(u_pdb.atoms.n_atoms) != EXPECT_N_ATOMS:
            return {
                "ok": False,
                "verdict": "EXT_LANDMARK_BLOCKED_ATOMCOUNT",
                "reason": f"pdb_n_atoms={u_pdb.atoms.n_atoms} expected={EXPECT_N_ATOMS}",
                "state": st,
            }

        # Prefer identical construct resid when sequences match
        pdb_ca = u_pdb.select_atoms("protein and name CA")
        pdb_ca_by_resid = {int(r): i for i, r in enumerate(pdb_ca.resids)}
        shared = sorted(set(topo_ca_by_resid) & set(pdb_ca_by_resid))
        # AA check on shared resids
        topo_aa = {int(r.resid): AA3_TO_1.get(r.resname, "?") for r in u_topo.residues}
        pdb_aa = {int(r.resid): AA3_TO_1.get(r.resname, "?") for r in u_pdb.residues}
        matched = [r for r in shared if topo_aa.get(r) == pdb_aa.get(r) and topo_aa.get(r) not in (None, "?")]
        if len(matched) < MIN_MATCHED_CA:
            return {
                "ok": False,
                "verdict": "EXT_LANDMARK_BLOCKED_NUMBERING",
                "reason": "insufficient_matched_ca",
                "state": st,
                "n_matched": len(matched),
                "threshold": MIN_MATCHED_CA,
                "needed": (
                    "Residue numbering differs between landmark PDBs and strip prmtop; "
                    "need a verified resid correspondence table before RMSD assignment."
                ),
            }
        matched_resid_sets.append(set(matched))
        per_landmark[st] = {
            "file": STATE_FILES[st],
            "sha256": sha256_file(path),
            "n_atoms": int(u_pdb.atoms.n_atoms),
            "n_ca": len(pdb_ca),
            "identity_topo_pdb": identity_topo,
            "uniprot_align": pdb_up,
            "n_matched_ca": len(matched),
            "matched_resids_head": matched[:5],
            "matched_resids_tail": matched[-5:],
        }

    # Intersection across all landmarks — identical index set
    common = set.intersection(*matched_resid_sets) if matched_resid_sets else set()
    if len(common) < MIN_MATCHED_CA:
        return {
            "ok": False,
            "verdict": "EXT_LANDMARK_BLOCKED_NUMBERING",
            "reason": "landmarks_disagree_on_matched_ca_set",
            "n_common": len(common),
            "needed": "Reconcile per-landmark resid maps to a shared Cα index set.",
        }
    matched_resids = sorted(common)
    # Verify each landmark has same count (by construction of intersection)
    n_matched = len(matched_resids)
    for st in STATE_ORDER:
        if per_landmark[st]["n_matched_ca"] != n_matched and len(matched_resid_sets[STATE_ORDER.index(st)]) != n_matched:
            # update to common count
            pass
        per_landmark[st]["n_matched_ca_common"] = n_matched

    # Build landmark Cα coordinate arrays in common resid order
    landmark_coords: dict[str, np.ndarray] = {}
    for st in STATE_ORDER:
        u_pdb = mda.Universe(str(PDB_DIR / STATE_FILES[st]))
        ca = u_pdb.select_atoms("protein and name CA")
        by_resid = {int(r): i for i, r in enumerate(ca.resids)}
        idx = [by_resid[r] for r in matched_resids]
        landmark_coords[st] = ca.positions[idx].astype(np.float64).copy()

    return {
        "ok": True,
        "verdict": "GATE0_PASS",
        "topo_n_atoms": int(u_topo.atoms.n_atoms),
        "topo_n_ca": len(topo_ca),
        "topo_uniprot_align": topo_up,
        "matched_resids": matched_resids,
        "n_matched_ca": n_matched,
        "per_landmark": per_landmark,
        "landmark_coords": landmark_coords,
        "note": (
            "Geometric landmark labels are structural refs only; "
            "NOT MSM metastable identity."
        ),
    }


def edges_from_counts(
    counts: np.ndarray, n_frames: int, labels: list[str], thr: float
) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    if n_frames <= 0:
        return edges
    n = len(labels)
    thr_count = thr * float(n_frames)
    for i in range(n):
        for j in range(i + 1, n):
            if float(counts[i, j]) >= thr_count:
                edges.add(edge_key(labels[i], labels[j]))
    return edges


def accumulate_frame_contacts(
    heavy_pos: np.ndarray,
    tables: dict[str, Any],
    counts: np.ndarray,
) -> None:
    radii = tables["radii"]
    atom_lab_idx = tables["atom_lab_idx"]
    protein_mask = tables["protein_mask"]
    resnums = tables["resnums"]
    exclude_seq = CONTACT_DEF["exclude_sequential_protein"]
    pairs = capped_distance(heavy_pos, heavy_pos, max_cutoff=_MAX_CUT, return_distances=True)
    if pairs[0].size == 0:
        return
    idx, dist = pairs
    mask = idx[:, 0] < idx[:, 1]
    idx = idx[mask]
    dist = dist[mask]
    lim = radii[idx[:, 0]] + radii[idx[:, 1]] + _SLACK
    hit = dist < lim
    idx = idx[hit]
    if idx.size == 0:
        return
    li = atom_lab_idx[idx[:, 0]]
    lj = atom_lab_idx[idx[:, 1]]
    same = li != lj
    li, lj = li[same], lj[same]
    seen: set[tuple[int, int]] = set()
    for a, b in zip(li.tolist(), lj.tolist()):
        if a > b:
            a, b = b, a
        key = (a, b)
        if key in seen:
            continue
        seen.add(key)
        if exclude_seq and protein_mask[a] and protein_mask[b]:
            if abs(int(resnums[a]) - int(resnums[b])) == 1:
                continue
        counts[a, b] += 1
        counts[b, a] += 1


def accumulate_frame_ca(
    ca_pos: np.ndarray,
    ca_resnums: np.ndarray,
    ca_lab_idx: np.ndarray,
    n_lab: int,
    counts: np.ndarray,
) -> None:
    pairs = capped_distance(ca_pos, ca_pos, max_cutoff=CA_CUTOFF_A, return_distances=False)
    if pairs.size == 0:
        return
    mask = pairs[:, 0] < pairs[:, 1]
    seen: set[tuple[int, int]] = set()
    for i, j in pairs[mask]:
        if abs(int(ca_resnums[i]) - int(ca_resnums[j])) < CA_MIN_SEP:
            continue
        a = int(ca_lab_idx[i])
        b = int(ca_lab_idx[j])
        if a == b:
            continue
        if a > b:
            a, b = b, a
        if (a, b) in seen:
            continue
        seen.add((a, b))
        counts[a, b] += 1
        counts[b, a] += 1


def assign_verdicts(
    mean_j: float,
    frac_core: float,
    frac_spec: float,
    path_turn: float,
    n_occupied: int,
    blocked: str | None,
) -> dict[str, str]:
    if blocked:
        return {
            "EXT_LANDMARK_CONTACTS": blocked,
            "Q_MAPS": "NA",
            "EXT_LANDMARK_SOFT_COMPARE_PDB": "EXT_LANDMARK_SOFT_COMPARE_NA",
            "EXT_LANDMARK_GEOMETRIC_NEQ_MSM": "TRUE",
            "P2_STATUS_UNCHANGED": "CLOSED_ABORTED_NOT_CONVERGENT",
        }
    if n_occupied < MIN_OCCUPIED_LANDMARKS:
        primary = "EXT_LANDMARK_CONTACTS_INDETERMINATE"
    elif mean_j >= THR_MEAN_J_STABLE and frac_core >= THR_FRAC_CORE_STABLE:
        primary = "EXT_LANDMARK_CONTACTS_STABLE"
    elif frac_spec >= THR_FRAC_SPECIFIC_B or path_turn >= THR_PATH_TURNOVER_B:
        primary = "EXT_LANDMARK_CONTACTS_STATE_DEPENDENT"
    elif frac_spec < THR_FRAC_SPECIFIC_B and mean_j < THR_MEAN_J_DIFFUSE:
        primary = "EXT_LANDMARK_CONTACTS_DIFFUSE"
    else:
        primary = "EXT_LANDMARK_CONTACTS_INDETERMINATE"

    q = (
        "DIFFERS_SUBSTANTIALLY"
        if (mean_j < THR_MEAN_J_STABLE or path_turn >= THR_PATH_TURNOVER_B)
        else "SIMILAR_OVERALL"
    )
    soft = (
        "EXT_LANDMARK_SOFT_AGREE_PDB_B"
        if primary == "EXT_LANDMARK_CONTACTS_STATE_DEPENDENT"
        else "EXT_LANDMARK_SOFT_DISAGREE_PDB_B"
    )
    return {
        "EXT_LANDMARK_CONTACTS": primary,
        "Q_MAPS": q,
        "EXT_LANDMARK_SOFT_COMPARE_PDB": soft,
        "EXT_LANDMARK_GEOMETRIC_NEQ_MSM": "TRUE",
        "P2_STATUS_UNCHANGED": "CLOSED_ABORTED_NOT_CONVERGENT",
    }


def compute_metrics(
    edges: dict[str, set[tuple[str, str]]],
    occupied: list[str],
) -> dict[str, Any]:
    n_edges = {k: len(edges.get(k, set())) for k in STATE_ORDER}
    pair_j: dict[str, float] = {}
    js: list[float] = []
    for i, a in enumerate(occupied):
        for b in occupied[i + 1 :]:
            j = jaccard(edges[a], edges[b])
            pair_j[f"{a}|{b}"] = j
            js.append(j)
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
        others = set.union(*(edges[t] for t in occupied if t != k)) if len(occupied) > 1 else set()
        private = edges[k] - others
        n_state_specific[k] = len(private)
        spec_fracs.append(len(private) / max(len(edges[k]), 1))
    frac_spec = float(np.mean(spec_fracs)) if spec_fracs else 0.0

    path_steps: list[dict[str, Any]] = []
    turnovers: list[float] = []
    for a, b in zip(STATE_ORDER, STATE_ORDER[1:]):
        if a not in occupied or b not in occupied:
            continue
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
                "appear_sample": [f"{x}–{y}" for x, y in sorted(appear)[:8]],
                "disappear_sample": [f"{x}–{y}" for x, y in sorted(disappear)[:8]],
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
        "occupied_landmarks": occupied,
    }


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    g0 = payload.get("gate0") or {}
    m = payload.get("metrics_primary") or {}
    lines = [
        "# EXTERNAL — CB2 geometric landmark contact maps",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_LANDMARK_CONTACTS.md`",
        f"**Git SHA:** `{payload.get('git_sha', 'unknown')}`",
        "",
        "## Epistemology",
        "",
        "- EXTERNAL **geometric** labeling: nearest of 6 Dutta Fig. 6 PDB landmarks (RMSD Cα).",
        "- **Geometric proximity ≠ MSM metastable identity.** Not kinetic MSM; not pickles; not P2; no Gi.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_LANDMARK_CONTACTS']}`**",
        f"- Q maps: `{v['Q_MAPS']}`",
        f"- Soft compare vs PDB snapshot B: `{v['EXT_LANDMARK_SOFT_COMPARE_PDB']}`",
        f"- `EXT_LANDMARK_GEOMETRIC_NEQ_MSM` = `{v['EXT_LANDMARK_GEOMETRIC_NEQ_MSM']}`",
        f"- P2 unchanged: `{v['P2_STATUS_UNCHANGED']}`",
        "",
        "## Gate 0 — numbering / alignment",
        "",
        f"- Pass: `{g0.get('ok')}`  verdict=`{g0.get('verdict')}`",
        f"- Matched Cα: `{g0.get('n_matched_ca')}`",
        f"- Topo UniProt median offset (resid−UP): "
        f"`{(g0.get('topo_uniprot_align') or {}).get('median_offset_resid_minus_uniprot')}`",
    ]
    if g0.get("reason"):
        lines.append(f"- Fail reason: `{g0.get('reason')}`")
        if g0.get("needed"):
            lines.append(f"- Mapping needed: {g0.get('needed')}")
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
    if occ:
        lines += ["", "## Hard-assign occupancy", ""]
        for st in STATE_ORDER:
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
            f"- path_turnover_frac=`{m.get('path_turnover_frac'):.4f}`",
            "",
            "### n_edges",
            "",
        ]
        for st in STATE_ORDER:
            lines.append(f"- `{st}`: `{m.get('n_edges', {}).get(st)}`")
        lines += ["", "### Path turnover", ""]
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
        "- No Gi; no docking; no P2 CONVERGENT; landmark ≠ MSM state.",
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
        "verdicts": assign_verdicts(0, 0, 0, 0, 0, verdict),
        "soft_tau_A": SOFT_TAU_A,
        "pi_summary_es": (
            f"Experimento landmark **bloqueado** (`{verdict}`). "
            f"Motivo: {detail.get('reason')}. "
            f"{detail.get('needed', '')} "
            "No se inventó mapping. Geometric ≠ MSM; P2 sin cambios."
        ),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Strip non-JSON landmark_coords if present
    g0 = dict(payload["gate0"])
    g0.pop("landmark_coords", None)
    payload["gate0"] = g0
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    return payload


def run(n_per_state: int, skip_extract: bool, tau: float, git_sha: str) -> dict[str, Any]:
    t_start = time.time()
    if not PREREG.is_file():
        raise SystemExit(f"Pre-registration missing: {PREREG}")

    print("[landmark] Gate 0 — numbering / alignment …", flush=True)
    gate = gate0_numbering()
    if not gate.get("ok"):
        print(f"[landmark] Gate 0 FAIL: {gate.get('verdict')} {gate.get('reason')}", flush=True)
        return write_blocked(str(gate.get("verdict")), gate, git_sha)

    landmark_coords: dict[str, np.ndarray] = gate.pop("landmark_coords")
    matched_resids: list[int] = gate["matched_resids"]
    print(
        f"[landmark] Gate 0 PASS: n_matched_ca={gate['n_matched_ca']} "
        f"topo_offset={gate['topo_uniprot_align'].get('median_offset_resid_minus_uniprot')}",
        flush=True,
    )

    print(f"[landmark] extracting stratified {n_per_state}+{n_per_state} …", flush=True)
    extract = extract_stratified(n_per_state, skip_extract=skip_extract)
    if not extract.get("ok"):
        return write_blocked(
            "EXT_LANDMARK_BLOCKED_DATA",
            {"ok": False, "verdict": "EXT_LANDMARK_BLOCKED_DATA", **extract},
            git_sha,
        )
    print(f"[landmark] extract sources={extract.get('sources')}", flush=True)

    # Topology universe + tables + CA index
    u0 = mda.Universe(str(TOPOLOGY))
    tables = build_protein_tables(u0)
    labels = tables["unique_labels"]
    n_lab = tables["n_labels"]
    ca0 = u0.select_atoms("protein and name CA")
    ca_by_resid = {int(r): i for i, r in enumerate(ca0.resids)}
    ca_match_idx = np.asarray([ca_by_resid[r] for r in matched_resids], dtype=np.int32)

    # CA contact label index (per-CA → residue label index in same unique_labels space)
    ca_labels = [res_label(rn, int(ri)) for rn, ri in zip(ca0.resnames, ca0.resids)]
    label_index = {lab: i for i, lab in enumerate(labels)}
    # Build CA-only label list for secondary
    ca_unique = []
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

    lm_order = STATE_ORDER
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
                "EXT_LANDMARK_BLOCKED_DATA",
                {
                    "ok": False,
                    "verdict": "EXT_LANDMARK_BLOCKED_DATA",
                    "reason": "walltime_during_analysis",
                    "processed_trajs": ti - 1,
                },
                git_sha,
            )
        print(f"[landmark] traj {ti}/{n_traj}: {nc.name}", flush=True)
        u = mda.Universe(str(TOPOLOGY), str(nc))
        if int(u.atoms.n_atoms) != EXPECT_N_ATOMS:
            return write_blocked(
                "EXT_LANDMARK_BLOCKED_ATOMCOUNT",
                {
                    "ok": False,
                    "verdict": "EXT_LANDMARK_BLOCKED_ATOMCOUNT",
                    "reason": f"{nc.name} n_atoms={u.atoms.n_atoms}",
                },
                git_sha,
            )
        # Rebind selections to this universe
        heavy = u.select_atoms("protein").select_atoms("not name H*")
        cas = u.select_atoms("protein and name CA")
        # Verify CA resid order matches gate0
        if list(map(int, cas.resids)) != list(map(int, ca0.resids)):
            return write_blocked(
                "EXT_LANDMARK_BLOCKED_NUMBERING",
                {
                    "ok": False,
                    "verdict": "EXT_LANDMARK_BLOCKED_NUMBERING",
                    "reason": "traj_ca_resid_order_mismatch",
                    "file": nc.name,
                    "needed": "All trajs must share the strip prmtop residue numbering.",
                },
                git_sha,
            )

        for _ts in u.trajectory:
            mobile = cas.positions[ca_match_idx].astype(np.float64)
            rmsds = np.asarray([kabsch_rmsd(mobile, tgt) for tgt in lm_targets], dtype=np.float64)
            hard_i = int(np.argmin(rmsds))
            hard_st = lm_order[hard_i]
            w = softmax_neg_rmsd(rmsds, tau)
            ent = float(-(w * np.log(np.clip(w, 1e-12, 1.0))).sum())
            soft_entropy_sum += ent

            # Contacts once per frame → hard counts + soft-weighted sensitivity
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

    # Occupancy
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

    # Primary edges
    edges: dict[str, set[tuple[str, str]]] = {}
    edges_ca: dict[str, set[tuple[str, str]]] = {}
    for st in lm_order:
        edges[st] = edges_from_counts(hard_counts[st], n_frames_lm[st], labels, P_IJ_THR)
        edges_ca[st] = edges_from_counts(ca_counts[st], n_frames_lm[st], ca_unique, P_IJ_THR)

    metrics = compute_metrics(edges, occupied)
    # secondary ca mean jaccard vs primary (occupied)
    ca_js = []
    for st in occupied:
        ca_js.append(jaccard(edges[st], edges_ca[st]))
    metrics["mean_jaccard_primary_vs_ca"] = float(np.mean(ca_js)) if ca_js else None

    verdicts = assign_verdicts(
        metrics["mean_jaccard"],
        metrics["frac_core"],
        metrics["frac_state_specific"],
        metrics["path_turnover_frac"],
        len(occupied),
        None,
    )

    # Soft sensitivity edges (p_ij = soft_counts / soft_mass)
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
    soft_metrics = compute_metrics(soft_edges, soft_occ)
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
        "soft_class_annotation": soft_verdicts["EXT_LANDMARK_CONTACTS"],
        "differs_from_hard": soft_verdicts["EXT_LANDMARK_CONTACTS"] != verdicts["EXT_LANDMARK_CONTACTS"],
        "soft_mass": {k: float(v) for k, v in soft_mass.items()},
    }
    if soft_sensitivity["differs_from_hard"]:
        verdicts["EXT_LANDMARK_SOFT_SENSITIVITY"] = "TRUE"

    # PI summary ES
    pi = (
        f"Landmark geométrico CB2 (6 PDBs Dutta): Gate0 OK (Cα emparejados={gate['n_matched_ca']}, "
        f"offset topo−UniProt≈{gate['topo_uniprot_align'].get('median_offset_resid_minus_uniprot')}). "
        f"N={n_per_state}+{n_per_state} trajs, frames={total_frames}. "
        f"Veredicto duro: **{verdicts['EXT_LANDMARK_CONTACTS']}** "
        f"(mean Jaccard={metrics['mean_jaccard']:.3f}, path turnover={metrics['path_turnover_frac']:.3f}, "
        f"frac_core={metrics['frac_core']:.3f}). "
        f"Compare PDB snapshot: {verdicts['EXT_LANDMARK_SOFT_COMPARE_PDB']}. "
        f"Importante: proximidad geométrica ≠ identidad MSM. P2 sin cambios. SHA `{git_sha}`."
    )

    # Serialize gate0 without coords
    gate_out = {k: v for k, v in gate.items() if k != "landmark_coords"}
    # matched_resids can be long — keep count + head/tail
    mrs = gate_out.get("matched_resids") or []
    gate_out["matched_resids"] = {
        "n": len(mrs),
        "head": mrs[:10],
        "tail": mrs[-10:],
    }

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
        "gate0": gate_out,
        "extract": {k: extract[k] for k in extract if k != "zip_members"},
        "n_trajs": n_traj,
        "total_frames": total_frames,
        "occupancy": occupancy,
        "assign_hist": {lm_order[i]: int(assign_hist[i]) for i in range(n_lm)},
        "metrics_primary": {
            **metrics,
            "pairwise_jaccard": metrics["pairwise_jaccard"],
            "path_steps": metrics["path_steps"],
        },
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
            "no_gi": True,
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(f"[landmark] done verdict={verdicts['EXT_LANDMARK_CONTACTS']} wall_s={payload['wall_s']:.1f}", flush=True)
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-per-state", type=int, default=N_PER_STATE_DEFAULT)
    ap.add_argument("--skip-extract", action="store_true")
    ap.add_argument("--tau", type=float, default=SOFT_TAU_A)
    args = ap.parse_args()

    import subprocess

    try:
        git_sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True)
            .strip()
        )
    except Exception:
        git_sha = "unknown"

    run(args.n_per_state, args.skip_extract, args.tau, git_sha)


if __name__ == "__main__":
    main()
