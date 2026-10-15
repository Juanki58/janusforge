#!/usr/bin/env python3
"""EXTERNAL — CB2 MSM metastable-state contact probabilities.

Governance: docs/synthesis/EXPERIMENT_CB2_MSM_STATE_CONTACTS.md (pre-registered).
  - Gate 0: traj index ↔ zip .nc alignment required; else INDETERMINATE_NO_ALIGNMENT.
  - Filename inactive/active ≠ MSM macrostate.
  - Does NOT reopen P2 as CONVERGENT; no Gi claims.

Outputs:
  results/network_core/cb2_msm_state_contacts.{md,json}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from dynamic_pipeline import HUBS, HUB_LABELS  # noqa: E402
from p1_dynamic_hub_validation import (  # noqa: E402
    CONTACT_DEF,
    _VDW,
    accumulate_contacts,
    res_label,
)

try:
    import MDAnalysis as mda
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required: {e}") from e

# ---------------------------------------------------------------------------
# Locked a priori (see EXPERIMENT_CB2_MSM_STATE_CONTACTS.md)
# ---------------------------------------------------------------------------

TRAJ_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO"
ZIP_PATH = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO.zip"
TOPOLOGY = TRAJ_DIR / "CB2-APO_inactive_pr_1-strip.prmtop"
CACHE_DIR = TRAJ_DIR / "_cache_msm_states"
MSM_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "msm"
STATE_PROB_PKL = MSM_DIR / "CB2_state_prob.pkl"
CLUSTERING_PKL = MSM_DIR / "CB2_msm_feature_final_clustering.pkl"
MANIFEST = MSM_DIR / "MANIFEST.json"

# Authors' column order (CB2-APO_vampnet_states_TPT.py)
IDX_TO_LABEL = {
    0: "I1",
    1: "I2",
    2: "I3",
    3: "inactive",
    4: "I4",
    5: "active",
}
LABEL_TO_IDX = {v: k for k, v in IDX_TO_LABEL.items()}
# Path / report order (paper Fig. 6 narrative)
STATE_ORDER = ["inactive", "I1", "I2", "I3", "I4", "active"]

UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

THR_J_STABLE = 0.80
THR_FRAC_PRIVATE_B = 0.15
THR_J_DIFFUSE = 0.55
P_IJ_THR = float(CONTACT_DEF["p_ij_edge_threshold"])
P_IJ_THR_HIGH = 0.5
EXPECT_N_ATOMS = 4566
PILOT_N_PER_STATE = 5
FRAME_CAP = 200
SEED = 20260912
DOM_FRAC_MIN = 0.9

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
OUT_JSON = OUT_DIR / "cb2_msm_state_contacts.json"
OUT_MD = OUT_DIR / "cb2_msm_state_contacts.md"


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


def map_hubs(u: mda.Universe) -> dict[str, Any]:
    residues = [r for r in u.residues if r.resname not in ("ACE", "NME")]
    pdb_resids: list[int] = []
    pdb_aas: list[str] = []
    for r in residues:
        aa = AA3_TO_1.get(r.resname)
        if aa is None:
            continue
        pdb_resids.append(int(r.resid))
        pdb_aas.append(aa)
    pdb_seq = "".join(pdb_aas)
    up_aln, pdb_aln = nw_align(UNIPROT_P34972, pdb_seq)
    up_i = 0
    pdb_i = 0
    up_to_pdb: dict[int, tuple[int, str]] = {}
    n_match = 0
    n_aligned = 0
    for ua, pa in zip(up_aln, pdb_aln):
        if ua != "-":
            up_i += 1
        if pa != "-":
            resid = pdb_resids[pdb_i]
            pdb_i += 1
            if ua != "-":
                up_to_pdb[up_i] = (resid, pa)
                n_aligned += 1
                if ua == pa:
                    n_match += 1
    identity = float(n_match) / float(n_aligned) if n_aligned else 0.0
    mapped: dict[str, Any] = {}
    for hub in HUBS:
        up_num = int(hub["label"].split(":")[1])
        expect_aa = hub["label"].split(":")[0]
        expect_1 = AA3_TO_1[expect_aa]
        hit = up_to_pdb.get(up_num)
        if hit is None:
            mapped[hub["label"]] = {
                "status": "HUB_MAP_FAIL",
                "reason": "uniprot_index_not_in_alignment",
                "uniprot": up_num,
                "expected_aa": expect_aa,
            }
            continue
        resid, aa1 = hit
        sel = u.select_atoms(f"resid {resid}")
        resname = str(sel.residues.resnames[0]) if len(sel) else "?"
        label = res_label(resname, resid)
        ok = aa1 == expect_1
        mapped[hub["label"]] = {
            "status": "OK" if ok else "HUB_MAP_FAIL",
            "reason": None if ok else f"aa_mismatch_expected_{expect_aa}_got_{resname}",
            "uniprot": up_num,
            "expected_aa": expect_aa,
            "topo_resid": resid,
            "topo_resname": resname,
            "topo_label": label,
            "aligned_aa1": aa1,
            "uniprot_minus_topo": up_num - resid,
        }
    return {
        "alignment_identity": identity,
        "n_protein_residues": len(pdb_resids),
        "hubs": mapped,
        "note": "Project hub labels = UniProt P34972; topo resid typically UniProt−20 on this construct.",
    }


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
    return {
        "heavy": heavy,
        "unique_labels": unique_labels,
        "atom_lab_idx": atom_lab_idx,
        "radii": radii,
        "protein_mask": np.ones(len(unique_labels), dtype=bool),
        "resnums": np.asarray([int(lab.split(":")[1]) for lab in unique_labels], dtype=np.int32),
        "n_labels": len(unique_labels),
    }


def edges_from_pmat(p_mat: np.ndarray, labels: list[str], thr: float) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            if float(p_mat[i, j]) >= thr:
                edges.add(edge_key(labels[i], labels[j]))
    return edges


def load_msm() -> tuple[list[np.ndarray], list[np.ndarray], dict[str, Any]]:
    sp = pickle.load(open(STATE_PROB_PKL, "rb"))
    cl = pickle.load(open(CLUSTERING_PKL, "rb"))
    if len(sp) != len(cl):
        raise SystemExit(f"MSM length mismatch state_prob={len(sp)} clustering={len(cl)}")
    meta = {
        "n_traj": len(sp),
        "state_prob_sha256": sha256_file(STATE_PROB_PKL),
        "clustering_sha256": sha256_file(CLUSTERING_PKL),
        "idx_to_label": {str(k): v for k, v in IDX_TO_LABEL.items()},
        "label_source": (
            "ShuklaGroup/Cannabinoid_activation "
            "Main_Figure_6/CB2-APO_vampnet_states_TPT.py "
            "labels=['I1','I2','I3','Inactive','I4','Active']"
        ),
    }
    return sp, cl, meta


def compute_pi(sp: list[np.ndarray]) -> dict[str, Any]:
    occ = Counter()
    soft = np.zeros(6, dtype=np.float64)
    nf = 0
    traj_dom = []
    for arr in sp:
        hard = np.argmax(arr, axis=1).astype(int)
        for k in hard:
            occ[int(k)] += 1
        soft += arr.sum(axis=0)
        nf += arr.shape[0]
        counts = Counter(int(x) for x in hard)
        dom, n = counts.most_common(1)[0]
        traj_dom.append({"dom_idx": dom, "dom_label": IDX_TO_LABEL[dom], "frac": n / len(hard), "T": len(hard)})
    tot = sum(occ.values())
    pi_hard = {IDX_TO_LABEL[k]: occ[k] / tot for k in range(6)}
    pi_soft = {IDX_TO_LABEL[k]: float(soft[k] / nf) for k in range(6)}
    pi_hard_by_idx = {str(k): occ[k] / tot for k in range(6)}
    return {
        "n_frames": nf,
        "pi_hard_by_label": pi_hard,
        "pi_soft_by_label": pi_soft,
        "pi_hard_by_idx": pi_hard_by_idx,
        "traj_dom_counts_by_label": dict(Counter(t["dom_label"] for t in traj_dom)),
        "n_traj_dom_frac_ge_0.9": sum(1 for t in traj_dom if t["frac"] >= 0.9),
        "path_order": STATE_ORDER,
    }


def find_sidecar_filelists() -> list[dict[str, Any]]:
    """Search for an explicit traj filelist next to MSM or in traj dir."""
    candidates: list[Path] = []
    patterns = [
        "*traj*list*",
        "*file*list*",
        "*dtraj*name*",
        "*traj*names*",
        "*nc*order*",
        "*msm*index*",
        "*.txt",
        "*.csv",
        "*.json",
        "*.npy",
        "*.pkl",
    ]
    for base in (MSM_DIR, TRAJ_DIR):
        for pat in patterns:
            candidates.extend(base.glob(pat))
    # Dedup; exclude known non-filelist pickles / manifests we already use
    skip = {
        "CB2_state_prob.pkl",
        "CB2_msm_feature_final_clustering.pkl",
        "CB1_state_prob.pkl",
        "CB1_msm_feature_final_clustering.pkl",
        "MANIFEST.json",
        "BLOCKED_README.md",
        "INGEST_README.md",
    }
    out = []
    seen: set[str] = set()
    for p in candidates:
        if p.name in skip or p.name.startswith("_inspect"):
            continue
        key = str(p.resolve())
        if key in seen:
            continue
        seen.add(key)
        info: dict[str, Any] = {
            "path": str(p.relative_to(ROOT)),
            "bytes": p.stat().st_size,
            "role": "candidate_sidecar",
        }
        # Heuristic: text file with many .nc lines
        if p.suffix.lower() in {".txt", ".csv", ".list", ""} or p.name == "list":
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
                n_nc = len(re.findall(r"\.nc\b", text))
                info["n_nc_mentions"] = n_nc
                info["preview"] = text[:500]
            except Exception as e:
                info["read_err"] = str(e)
        out.append(info)
    return out


def inspect_zip_helpers() -> dict[str, Any]:
    if not ZIP_PATH.is_file():
        return {"exists": False}
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        names = zf.namelist()
        nc = [n for n in names if n.endswith("-strip.nc")]
        helpers = [n for n in names if not n.endswith("-strip.nc")]
        helper_preview = {}
        for h in helpers:
            info = zf.getinfo(h)
            entry: dict[str, Any] = {"bytes": info.file_size}
            if info.file_size < 1_000_000 and not h.endswith(".prmtop"):
                raw = zf.read(h)
                try:
                    text = raw.decode("utf-8", errors="replace")
                    entry["text"] = text
                    entry["n_nc_lines"] = len(
                        [ln for ln in text.splitlines() if ln.strip().endswith(".nc")]
                    )
                except Exception as e:
                    entry["err"] = str(e)
            helper_preview[h] = entry
        return {
            "exists": True,
            "n_entries": len(names),
            "n_nc": len(nc),
            "n_inactive_filename": sum(1 for n in nc if "_inactive_" in Path(n).name),
            "n_active_filename": sum(1 for n in nc if "_active_" in Path(n).name),
            "helpers": helper_preview,
            "note": (
                "Filename inactive/active = simulation start label, NOT MSM macrostate. "
                "Zip member order is not validated as MSM list order."
            ),
        }


def gate0_alignment(
    sp: list[np.ndarray],
    cl: list[np.ndarray],
) -> dict[str, Any]:
    """Determine whether traj index ↔ zip .nc mapping is available.

    Per pre-registration: do NOT invent lex/zip order. Require an explicit key.
    """
    lens = [int(a.shape[0]) for a in sp]
    n_mismatch = sum(1 for a, b in zip(sp, cl) if a.shape[0] != b.shape[0])
    sidecars = find_sidecar_filelists()
    zip_info = inspect_zip_helpers()

    # Accepted: sidecar with n_nc_mentions == n_traj (or n_traj-delta with documented drop)
    usable_lists = [
        s for s in sidecars if isinstance(s.get("n_nc_mentions"), int) and s["n_nc_mentions"] >= len(sp) - 1
    ]
    # Zip helper `list` is only short-traj mover scrap — not a full order
    zip_list_n = 0
    if zip_info.get("helpers"):
        for h, meta in zip_info["helpers"].items():
            if Path(h).name == "list":
                zip_list_n = int(meta.get("n_nc_lines") or 0)

    missing_key = (
        "No co-deposited traj filename/path list of length n_traj aligned to "
        "CB2_state_prob.pkl list indices. Pickles are anonymous list[ndarray] only. "
        f"Zip has {zip_info.get('n_nc')} .nc vs MSM n_traj={len(sp)} (delta={len(sp) - int(zip_info.get('n_nc') or 0)}). "
        f"Zip helper CB2_APO/list has only {zip_list_n} short-traj names (not MSM order). "
        "Authors' load order (glob / box pagination) is not reconstructible from available artifacts. "
        "Lexicographic / zip-member / natural sort are NOT accepted without independent validation."
    )

    ok = False
    method = None
    if usable_lists:
        # Would need further validation against per-traj T; none expected today
        ok = False
        method = "sidecar_candidate_present_but_unvalidated"
        missing_key = (
            "Sidecar candidate(s) found but not validated against per-traj T sequence; "
            "refusing to guess. Candidates: "
            + ", ".join(s["path"] for s in usable_lists)
        )

    return {
        "ok": ok,
        "method": method,
        "n_traj_msm": len(sp),
        "n_len_mismatch_sp_cl": n_mismatch,
        "T_min_median_max": [min(lens), int(np.median(lens)), max(lens)],
        "sidecars_scanned": sidecars,
        "zip": zip_info,
        "missing_mapping_key": missing_key,
        "rejected_heuristics": [
            "lexicographic_sort_of_nc_names",
            "zip_member_order",
            "natural_sort",
            "filename_inactive_active_as_msm_label",
            "majority_hard_state_without_index_map",
        ],
        "verdict_if_fail": "EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT",
    }


def assign_verdicts_from_metrics(mean_j: float, mean_priv: float) -> str:
    if mean_j >= THR_J_STABLE and mean_priv < THR_FRAC_PRIVATE_B:
        return "EXT_MSM_STATE_CONTACTS_STABLE"
    if mean_priv >= THR_FRAC_PRIVATE_B:
        return "EXT_MSM_STATE_CONTACTS_STATE_DEPENDENT"
    if mean_j < THR_J_DIFFUSE and mean_priv < THR_FRAC_PRIVATE_B:
        return "EXT_MSM_STATE_CONTACTS_DIFFUSE"
    return "EXT_MSM_STATE_CONTACTS_INDETERMINATE"


def mean_pairwise_metrics(
    edges_by_state: dict[str, set[tuple[str, str]]],
) -> dict[str, Any]:
    labels = [s for s in STATE_ORDER if s in edges_by_state]
    jaccs = []
    privs = []
    pair_j: dict[str, float] = {}
    for i, a in enumerate(labels):
        for b in labels[i + 1 :]:
            j = jaccard(edges_by_state[a], edges_by_state[b])
            jaccs.append(j)
            pair_j[f"{a}__{b}"] = j
            ea, eb = edges_by_state[a], edges_by_state[b]
            fa = len(ea - eb) / max(len(ea), 1)
            fb = len(eb - ea) / max(len(eb), 1)
            privs.append(0.5 * (fa + fb))
    return {
        "mean_jaccard": float(np.mean(jaccs)) if jaccs else float("nan"),
        "mean_frac_private": float(np.mean(privs)) if privs else float("nan"),
        "pairwise_jaccard": pair_j,
        "n_edges": {s: len(edges_by_state[s]) for s in labels},
    }


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    pi = payload["stationary_populations"]
    g0 = payload["gate0_alignment"]
    lines = [
        "# EXTERNAL — CB2 MSM metastable-state contact probabilities",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_MSM_STATE_CONTACTS.md`",
        "",
        "## Epistemology",
        "",
        "- EXTERNAL MSM-state contacts (Dutta & Shukla 2023 Final_MSM + CB2_APO.zip).",
        "- Filename `inactive`/`active` ≠ MSM macrostate.",
        "- Does **not** reopen P2 as CONVERGENT; no Gi claims.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_MSM_STATE_CONTACTS']}`**",
        f"- Soft compare vs PDB snapshot B: `{v['EXT_MSM_SOFT_COMPARE_PDB']}`",
        f"- Filename ≠ MSM state: `{v['EXT_MSM_FILENAME_NEQ_MSM_STATE']}`",
        f"- P2 status: `{v['P2_STATUS_UNCHANGED']}`",
        "",
        "## Gate 0 — traj ↔ MSM alignment",
        "",
        f"- ok=`{g0['ok']}` method=`{g0.get('method')}`",
        f"- n_traj_msm=`{g0['n_traj_msm']}` zip_n_nc=`{g0.get('zip', {}).get('n_nc')}`",
        f"- **Missing mapping key:** {g0['missing_mapping_key']}",
        "",
        "Rejected heuristics (not used):",
        "",
    ]
    for h in g0.get("rejected_heuristics", []):
        lines.append(f"- `{h}`")

    lines += [
        "",
        "## Macrostate label map (authors’ code)",
        "",
        f"- Source: `{payload['msm']['label_source']}`",
        "",
        "| argmax idx | label |",
        "|----------:|-------|",
    ]
    for i in range(6):
        lines.append(f"| {i} | `{IDX_TO_LABEL[i]}` |")

    lines += [
        "",
        "## Stationary / empirical populations π (bonus; no traj alignment needed)",
        "",
        f"- n_frames pooled = `{pi['n_frames']}`",
        "",
        "| state | π̂ hard | π̃ soft |",
        "|-------|--------:|--------:|",
    ]
    for s in STATE_ORDER:
        lines.append(
            f"| `{s}` | {pi['pi_hard_by_label'][s]:.4f} | {pi['pi_soft_by_label'][s]:.4f} |"
        )
    lines += [
        "",
        f"- Trajs with dominant hard frac ≥0.9: `{pi['n_traj_dom_frac_ge_0.9']}` / `{g0['n_traj_msm']}`",
        "",
        "## Contact analysis",
        "",
    ]
    if not g0["ok"]:
        lines += [
            "- **Skipped.** Gate 0 failed — no per-state contact matrices / Jaccard / hub degrees.",
            "- Would have used VdW+0.5 Å, `p_ij≥0.1` (primary) / `0.5` (secondary), "
            f"pilot N={PILOT_N_PER_STATE} trajs/macrostate, frame_cap={FRAME_CAP}.",
            "",
        ]
    else:
        m = payload["metrics_primary"]
        lines += [
            f"- mean_jaccard(τ=0.1)=**{m['mean_jaccard']:.4f}**",
            f"- mean_frac_private=**{m['mean_frac_private']:.4f}**",
            f"- n_edges: `{m['n_edges']}`",
            f"- subsample N_per_state=`{payload.get('sampling', {}).get('n_per_state')}`",
            "",
        ]

    lines += [
        "## Soft compare (annotation)",
        "",
        "- Prior PDB: `EXT_PDB_CONTACTS_STATE_DEPENDENT` / `EXT_STRUCTURAL_ABC_SNAPSHOT_B`.",
        "- Prior filename pilot: `EXT_APO_PILOT_CONTACTS_INDETERMINATE` (Jaccard≈0.78).",
        f"- This run soft tag: `{v['EXT_MSM_SOFT_COMPARE_PDB']}`.",
        "",
        "## Forbidden claims (reminder)",
        "",
        "- No Gi; no docking; no P2 CONVERGENT; no fake traj↔MSM map.",
        "",
    ]
    return "\n".join(lines)


def build_no_alignment_payload(
    msm_meta: dict[str, Any],
    pi: dict[str, Any],
    gate0: dict[str, Any],
) -> dict[str, Any]:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "generated_utc": generated,
        "branch": "feat/cb2-hubs-functional-topology-test",
        "experiment": "EXPERIMENT_CB2_MSM_STATE_CONTACTS",
        "epistemology": {
            "scope": "EXTERNAL_MSM_STATE_CONTACTS",
            "filename_neq_msm_state": True,
            "p2_unchanged": True,
            "no_gi_claim": True,
            "no_docking": True,
            "no_p1_hub_hunt": True,
            "soft_compare_prior": "EXT_PDB_CONTACTS_STATE_DEPENDENT / EXT_STRUCTURAL_ABC_SNAPSHOT_B",
            "prior_filename_pilot": "EXT_APO_PILOT_CONTACTS_INDETERMINATE",
        },
        "contact_def": {
            "name": CONTACT_DEF["name"],
            "geometry": CONTACT_DEF["geometry"],
            "slack_A": CONTACT_DEF["slack_A"],
            "exclude_sequential_protein": CONTACT_DEF["exclude_sequential_protein"],
            "p_ij_edge_threshold": P_IJ_THR,
            "p_ij_report_threshold_high": P_IJ_THR_HIGH,
            "selection": "protein",
            "applied": False,
            "reason": "gate0_failed",
        },
        "thresholds": {
            "jaccard_stable": THR_J_STABLE,
            "mean_frac_private_B": THR_FRAC_PRIVATE_B,
            "jaccard_diffuse": THR_J_DIFFUSE,
        },
        "sampling_plan_registered": {
            "n_per_state_pilot": PILOT_N_PER_STATE,
            "frame_cap": FRAME_CAP,
            "dom_frac_min": DOM_FRAC_MIN,
            "seed": SEED,
            "cache_dir": str(CACHE_DIR.relative_to(ROOT)),
            "executed": False,
        },
        "msm": msm_meta,
        "gate0_alignment": gate0,
        "stationary_populations": pi,
        "metrics_primary": None,
        "hub_mapping": None,
        "verdicts": {
            "EXT_MSM_STATE_CONTACTS": "EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT",
            "EXT_MSM_SOFT_COMPARE_PDB": "EXT_MSM_SOFT_COMPARE_NA",
            "EXT_MSM_FILENAME_NEQ_MSM_STATE": "TRUE",
            "EXT_MSM_UPGRADES_FILENAME_PILOT": "FALSE_NO_ALIGNMENT",
            "P2_STATUS_UNCHANGED": "CLOSED_ABORTED_NOT_CONVERGENT",
            "MISSING_KEY": "traj_index_to_nc_filename_filelist",
        },
        "outputs": {
            "json": str(OUT_JSON.relative_to(ROOT)),
            "md": str(OUT_MD.relative_to(ROOT)),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-per-state", type=int, default=PILOT_N_PER_STATE)
    parser.add_argument("--frame-cap", type=int, default=FRAME_CAP)
    parser.add_argument(
        "--cleanup-cache",
        action="store_true",
        help="Delete extracted .nc under CACHE after processing (only if Gate 0 passes).",
    )
    args = parser.parse_args(argv)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_PROB_PKL.is_file() or not CLUSTERING_PKL.is_file():
        raise SystemExit("Missing CB2 MSM pickles under data/external/dutta_shukla_2023/msm/")

    print("[cb2_msm_state_contacts] loading Final_MSM pickles…")
    sp, cl, msm_meta = load_msm()
    pi = compute_pi(sp)
    print("[cb2_msm_state_contacts] Gate 0 alignment check…")
    gate0 = gate0_alignment(sp, cl)

    if not gate0["ok"]:
        payload = build_no_alignment_payload(msm_meta, pi, gate0)
        OUT_JSON.write_text(json.dumps(payload, indent=2, allow_nan=True), encoding="utf-8")
        OUT_MD.write_text(render_md(payload), encoding="utf-8")
        print("[cb2_msm_state_contacts] EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT")
        print(f"[cb2_msm_state_contacts] missing: {gate0['missing_mapping_key'][:160]}…")
        print(f"[cb2_msm_state_contacts] wrote {OUT_MD}")
        return 0

    # Gate 0 passed — stratified contacts would run here.
    # Kept as explicit stub so a future filelist enables the registered pilot without redesign.
    raise SystemExit(
        "Gate 0 reported ok but stratified contact runner is not wired for a validated "
        f"filelist yet (n_per_state={args.n_per_state}, frame_cap={args.frame_cap}, "
        f"cleanup={args.cleanup_cache}). Provide mapping and extend this branch."
    )


if __name__ == "__main__":
    raise SystemExit(main())
