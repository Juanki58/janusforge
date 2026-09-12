#!/usr/bin/env python3
"""EXTERNAL — CB2_APO inactive vs active trajectory pilot contact maps.

Governance: docs/synthesis/EXPERIMENT_CB2_APO_PILOT_CONTACTS.md (pre-registered).
  - Pilot-only EXTERNAL; does NOT reopen P2 as CONVERGENT.
  - 1 traj / state ≠ ensemble; soft compare to prior PDB STATE_DEPENDENT / snapshot B.

Outputs:
  results/network_core/cb2_apo_pilot_contacts.{md,json}
"""
from __future__ import annotations

import argparse
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

from dynamic_pipeline import HUBS, HUB_LABELS  # noqa: E402
from p1_dynamic_hub_validation import (  # noqa: E402
    CONTACT_DEF,
    _MAX_CUT,
    _SLACK,
    _VDW,
    accumulate_contacts,
    res_label,
)

try:
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import capped_distance
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required: {e}") from e

# ---------------------------------------------------------------------------
# Locked a priori (see EXPERIMENT_CB2_APO_PILOT_CONTACTS.md)
# ---------------------------------------------------------------------------

TRAJ_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO"
ZIP_PATH = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO.zip"
TOPOLOGY = TRAJ_DIR / "CB2-APO_inactive_pr_1-strip.prmtop"
STATE_FILES = {
    "inactive": "CB2-APO_inactive_pr_9_frame_99-strip.nc",
    "active": "CB2-APO_active_pr_10_frame_28-strip.nc",
}
STATE_ORDER = ["inactive", "active"]

UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

THR_J_STABLE = 0.80
THR_FRAC_PRIVATE_B = 0.15
THR_J_DIFFUSE = 0.55
P_IJ_THR = float(CONTACT_DEF["p_ij_edge_threshold"])
CA_CUTOFF_A = 8.0
CA_MIN_SEP = 2
EXPECT_N_ATOMS = 4566

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
OUT_JSON = OUT_DIR / "cb2_apo_pilot_contacts.json"
OUT_MD = OUT_DIR / "cb2_apo_pilot_contacts.md"
SAMPLE_DIR = TRAJ_DIR / "_pilot_sample"


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
        }
    return {
        "alignment_identity": identity,
        "n_protein_residues": len(pdb_resids),
        "hubs": mapped,
        "note": "Project hub labels use UniProt P34972 indices; topo resid may differ (N-term truncation).",
    }


def build_protein_tables(u: mda.Universe) -> dict[str, Any]:
    """Same tables as P1 accumulate_contacts, but selection='protein' (apo)."""
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


def edges_from_pmat(p_mat: np.ndarray, labels: list[str], thr: float) -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            if float(p_mat[i, j]) >= thr:
                edges.add(edge_key(labels[i], labels[j]))
    return edges


def accumulate_ca_contacts(u: mda.Universe) -> tuple[set[tuple[str, str]], int]:
    """Cα–Cα persistence ≥ p_ij thr; sensitivity only."""
    cas = u.select_atoms("protein and name CA")
    if len(cas) < 2:
        return set(), 0
    labels = [res_label(rn, int(ri)) for rn, ri in zip(cas.resnames, cas.resids)]
    resnums = cas.resids.astype(int)
    n = len(labels)
    counts = np.zeros((n, n), dtype=np.int32)
    n_used = 0
    for ts_i in range(u.trajectory.n_frames):
        u.trajectory[ts_i]
        pos = cas.positions
        pairs = capped_distance(pos, pos, max_cutoff=CA_CUTOFF_A, return_distances=False)
        if pairs.size:
            mask = pairs[:, 0] < pairs[:, 1]
            for i, j in pairs[mask]:
                if abs(int(resnums[i]) - int(resnums[j])) < CA_MIN_SEP:
                    continue
                counts[i, j] += 1
                counts[j, i] += 1
        n_used += 1
    thr_count = int(np.ceil(P_IJ_THR * n_used)) if n_used else 1
    edges: set[tuple[str, str]] = set()
    for i in range(n):
        for j in range(i + 1, n):
            if counts[i, j] >= thr_count:
                edges.add(edge_key(labels[i], labels[j]))
    return edges, n_used


def hub_participation(
    edges: set[tuple[str, str]],
    hub_map: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for hub_lab, info in hub_map["hubs"].items():
        if info.get("status") != "OK":
            out[hub_lab] = {"status": info.get("status"), "degree": None, "neighbors": []}
            continue
        node = info["topo_label"]
        nbrs = sorted({v if u == node else u for u, v in edges if u == node or v == node})
        out[hub_lab] = {
            "status": "OK",
            "topo_label": node,
            "degree": len(nbrs),
            "neighbors": nbrs,
        }
    return out


def assign_verdicts(jacc: float, mean_frac_private: float) -> dict[str, str]:
    if jacc >= THR_J_STABLE and mean_frac_private < THR_FRAC_PRIVATE_B:
        primary = "EXT_APO_PILOT_CONTACTS_STABLE"
    elif mean_frac_private >= THR_FRAC_PRIVATE_B:
        primary = "EXT_APO_PILOT_CONTACTS_STATE_DEPENDENT"
    elif jacc < THR_J_DIFFUSE and mean_frac_private < THR_FRAC_PRIVATE_B:
        primary = "EXT_APO_PILOT_CONTACTS_DIFFUSE"
    else:
        primary = "EXT_APO_PILOT_CONTACTS_INDETERMINATE"

    q2 = "DIFFERS_SUBSTANTIALLY" if jacc < THR_J_STABLE else "SIMILAR_OVERALL"
    soft = (
        "EXT_APO_PILOT_SOFT_AGREE_PDB_B"
        if primary == "EXT_APO_PILOT_CONTACTS_STATE_DEPENDENT"
        else "EXT_APO_PILOT_SOFT_DISAGREE_PDB_B"
    )
    return {
        "EXT_APO_PILOT_CONTACTS": primary,
        "Q2_MAPS": q2,
        "EXT_APO_PILOT_SOFT_COMPARE_PDB": soft,
        "EXT_APO_PILOT_SINGLE_TRAJ_LIMIT": "TRUE",
        "EXT_APO_PILOT_NEEDS_MORE_TRAJS": "YES",
        "P2_STATUS_UNCHANGED": "CLOSED_ABORTED_NOT_CONVERGENT",
    }


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


def extract_stratified_sample(n_per_state: int = 5) -> dict[str, Any]:
    """Extract n+n .nc from zip without unpacking the archive."""
    if not ZIP_PATH.is_file():
        return {"ok": False, "reason": "zip_missing"}
    by_state = list_zip_nc_by_state(ZIP_PATH)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20260912)
    extracted: dict[str, list[str]] = {"inactive": [], "active": []}
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        for st in STATE_ORDER:
            pool = by_state[st]
            if len(pool) < n_per_state:
                return {
                    "ok": False,
                    "reason": f"insufficient_{st}",
                    "available": {k: len(v) for k, v in by_state.items()},
                }
            # Stratify by sorting then take evenly spaced + small jitter via seed pick
            idx = np.linspace(0, len(pool) - 1, n_per_state, dtype=int)
            # de-dup if linspace collapses
            chosen_idx = sorted(set(int(i) for i in idx))
            while len(chosen_idx) < n_per_state:
                extra = int(rng.integers(0, len(pool)))
                if extra not in chosen_idx:
                    chosen_idx.append(extra)
            chosen_idx = sorted(chosen_idx)[:n_per_state]
            for i in chosen_idx:
                member = pool[i]
                dest = SAMPLE_DIR / Path(member).name
                if not dest.is_file():
                    with zf.open(member) as src, dest.open("wb") as dst:
                        while True:
                            chunk = src.read(1 << 20)
                            if not chunk:
                                break
                            dst.write(chunk)
                extracted[st].append(dest.name)
    return {
        "ok": True,
        "n_per_state": n_per_state,
        "dir": str(SAMPLE_DIR.relative_to(ROOT)),
        "files": extracted,
        "pool_sizes": {k: len(v) for k, v in by_state.items()},
    }


def smoke_open(top: Path, nc: Path) -> dict[str, Any]:
    u = mda.Universe(str(top), str(nc))
    return {
        "file": nc.name,
        "n_atoms": int(u.atoms.n_atoms),
        "n_frames": int(u.trajectory.n_frames),
        "n_residues": int(u.residues.n_residues),
        "atoms_ok": int(u.atoms.n_atoms) == EXPECT_N_ATOMS,
        "first_res": [
            f"{r.resname}:{int(r.resid)}" for r in list(u.residues)[:3]
        ],
        "last_res": [
            f"{r.resname}:{int(r.resid)}" for r in list(u.residues)[-3:]
        ],
        "universe": u,
    }


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    m = payload["metrics_primary"]
    lines = [
        "# EXTERNAL — CB2_APO pilot contact maps (inactive vs active)",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_APO_PILOT_CONTACTS.md`",
        "",
        "## Epistemology",
        "",
        "- EXTERNAL **trajectory pilot** (1 inactive + 1 active `.nc` + shared prmtop).",
        "- **Few trajs ≠ ensemble.** Not P2 CONVERGENT; not Gi mechanism; not P1 hub hunt.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_APO_PILOT_CONTACTS']}`**",
        f"- Q2 maps: `{v['Q2_MAPS']}`",
        f"- Soft compare vs prior PDB snapshot B: `{v['EXT_APO_PILOT_SOFT_COMPARE_PDB']}`",
        f"- Single-traj limit: `{v['EXT_APO_PILOT_SINGLE_TRAJ_LIMIT']}`",
        f"- Needs more trajs (stratified zip sample): `{v['EXT_APO_PILOT_NEEDS_MORE_TRAJS']}`",
        f"- P2 status: `{v['P2_STATUS_UNCHANGED']}`",
        "",
        "## Smoke-open",
        "",
        f"- Topology: `{payload['topology']['file']}` sha256=`{payload['topology']['sha256'][:12]}…`",
        f"- Expect n_atoms={EXPECT_N_ATOMS}; both pilots atoms_ok=`{payload['smoke_all_ok']}`",
        "",
    ]
    for st in STATE_ORDER:
        sm = payload["states"][st]["smoke"]
        lines.append(
            f"- `{st}`: `{sm['file']}` n_atoms={sm['n_atoms']} n_frames={sm['n_frames']} "
            f"n_edges_vdw={payload['states'][st]['n_edges_vdw']} "
            f"sha256=`{payload['states'][st]['sha256'][:12]}…`"
        )

    lines += [
        "",
        "## Contact definition",
        "",
        f"- Primary: `{payload['contact_def']['name']}` — {payload['contact_def']['geometry']}",
        f"- `p_ij` threshold: `{P_IJ_THR}` (P1)",
        f"- Exclude sequential `|Δresid|==1`: `{payload['contact_def']['exclude_sequential_protein']}`",
        f"- Selection: `protein` (apo)",
        "",
        "## Metrics (primary VdW persistence)",
        "",
        f"- jaccard(inactive, active) = **{m['jaccard_inactive_active']:.4f}**",
        f"- n_edges inactive={m['n_edges']['inactive']} active={m['n_edges']['active']}",
        f"- n_shared={m['n_shared']} n_union={m['n_union']}",
        f"- frac_private inactive={m['frac_private']['inactive']:.4f} "
        f"active={m['frac_private']['active']:.4f} mean={m['mean_frac_private']:.4f}",
        "",
        "## Soft compare to prior PDB experiment",
        "",
        "- Prior: `EXT_PDB_CONTACTS_STATE_DEPENDENT` / `EXT_STRUCTURAL_ABC_SNAPSHOT_B` "
        "(6 state PDBs; mean Jaccard≈0.64; path turnover≈0.35).",
        f"- This pilot soft tag: `{v['EXT_APO_PILOT_SOFT_COMPARE_PDB']}` "
        "(contact-map class only; not ensemble promotion).",
        "",
        "## LigACN hubs (descriptive)",
        "",
        f"- Alignment identity: `{payload['hub_mapping']['alignment_identity']:.4f}`",
        f"- Note: {payload['hub_mapping']['note']}",
        "",
    ]
    for hub in HUB_LABELS:
        info = payload["hub_mapping"]["hubs"][hub]
        lines.append(
            f"- `{hub}`: status=`{info['status']}` "
            f"topo=`{info.get('topo_label')}` resid=`{info.get('topo_resid')}` "
            f"aa=`{info.get('topo_resname')}`"
            + (f" ({info.get('reason')})" if info.get("reason") else "")
        )
    lines += [
        "",
        "### Hub degrees (inactive | active)",
        "",
        "| hub | inactive | active |",
        "|---|---|---|",
    ]
    for hub in HUB_LABELS:
        di = payload["states"]["inactive"]["hub_participation"].get(hub, {}).get("degree")
        da = payload["states"]["active"]["hub_participation"].get(hub, {}).get("degree")
        lines.append(
            f"| `{hub}` | {'—' if di is None else di} | {'—' if da is None else da} |"
        )

    hij = payload.get("hub_incident_jaccard", {})
    if hij:
        lines += ["", "### Hub-incident edge Jaccard (inactive vs active)", ""]
        for hub in HUB_LABELS:
            val = hij.get(hub)
            if val is None or (isinstance(val, float) and np.isnan(val)):
                lines.append(f"- `{hub}`: —")
            else:
                lines.append(f"- `{hub}`: {float(val):.4f}")

    ca = payload["metrics_secondary_ca"]
    lines += [
        "",
        "## Secondary Cα 8Å (sensitivity)",
        "",
        f"- jaccard_ca={ca['jaccard_inactive_active']:.4f} (not used for verdicts)",
        "",
        "## Robustness note",
        "",
        "- Primary N=1 traj/state → always `EXT_APO_PILOT_NEEDS_MORE_TRAJS=YES`.",
        "- Optional: extract 5+5 from local `CB2_APO.zip` without full unpack "
        "(`--extract-sample 5`) and re-aggregate.",
        "",
    ]
    if payload.get("sample_extract"):
        se = payload["sample_extract"]
        lines += [
            "### Sample extract",
            "",
            f"- ok=`{se.get('ok')}` dir=`{se.get('dir')}` pool=`{se.get('pool_sizes')}`",
            "",
        ]

    lines += [
        "## Forbidden claims (reminder)",
        "",
        "- No Gi mechanism; no docking/de novo; no P2 CONVERGENT; pilot ≠ ensemble.",
        "",
    ]
    return "\n".join(lines)


def analyze_nc_list(
    top: Path,
    files_by_state: dict[str, list[Path]],
) -> tuple[dict[str, set[tuple[str, str]]], dict[str, set[tuple[str, str]]], dict[str, Any], dict[str, Any]]:
    """Aggregate persistence across one or more nc per state (mean p_ij then threshold)."""
    state_edges: dict[str, set[tuple[str, str]]] = {}
    state_edges_ca: dict[str, set[tuple[str, str]]] = {}
    state_payload: dict[str, Any] = {}
    hub_mapping: dict[str, Any] | None = None

    for st in STATE_ORDER:
        paths = files_by_state[st]
        p_sum: np.ndarray | None = None
        labels_ref: list[str] | None = None
        n_frames_total = 0
        traj_meta: list[dict[str, Any]] = []
        hub_map_st: dict[str, Any] | None = None
        ca_union_counts: dict[tuple[str, str], int] = {}
        ca_frames = 0

        for path in paths:
            smoke = smoke_open(top, path)
            u = smoke.pop("universe")
            if hub_mapping is None:
                hub_mapping = map_hubs(u)
            hub_map_st = map_hubs(u)
            tables = build_protein_tables(u)
            counts, n_used = accumulate_contacts(u, tables)
            p_mat = counts.astype(np.float64) / max(n_used, 1)
            if p_sum is None:
                p_sum = p_mat
                labels_ref = tables["unique_labels"]
            else:
                if tables["unique_labels"] != labels_ref:
                    raise SystemExit(f"Label mismatch across trajs for {st}")
                p_sum = p_sum + p_mat
            n_frames_total += n_used
            traj_meta.append(
                {
                    "file": path.name,
                    "sha256": sha256_file(path),
                    "n_atoms": smoke["n_atoms"],
                    "n_frames": smoke["n_frames"],
                    "n_frames_used": n_used,
                    "atoms_ok": smoke["atoms_ok"],
                }
            )
            ca_edges, ca_n = accumulate_ca_contacts(u)
            ca_frames += ca_n
            for e in ca_edges:
                ca_union_counts[e] = ca_union_counts.get(e, 0) + 1

        assert p_sum is not None and labels_ref is not None and hub_map_st is not None
        p_mean = p_sum / len(paths)
        edges = edges_from_pmat(p_mean, labels_ref, P_IJ_THR)
        # CA: edge if present in ≥1 traj after per-traj thr (pilot: usually 1)
        ca_edges_agg = set(ca_union_counts.keys())
        hp = hub_participation(edges, hub_map_st)
        first = traj_meta[0]
        u0 = mda.Universe(str(top), str(paths[0]))
        state_edges[st] = edges
        state_edges_ca[st] = ca_edges_agg
        state_payload[st] = {
            "smoke": {
                "file": first["file"] if len(traj_meta) == 1 else f"{len(traj_meta)}_trajs",
                "n_atoms": first["n_atoms"],
                "n_frames": n_frames_total if len(traj_meta) > 1 else first["n_frames"],
                "n_residues": int(u0.residues.n_residues),
                "atoms_ok": all(t["atoms_ok"] for t in traj_meta),
                "first_res": [f"{r.resname}:{int(r.resid)}" for r in list(u0.residues)[:3]],
                "last_res": [f"{r.resname}:{int(r.resid)}" for r in list(u0.residues)[-3:]],
            },
            "sha256": first["sha256"] if len(traj_meta) == 1 else "multi",
            "n_edges_vdw": len(edges),
            "n_edges_ca": len(ca_edges_agg),
            "hub_participation": hp,
            "trajs": traj_meta,
            "n_trajs": len(traj_meta),
        }

    assert hub_mapping is not None
    return state_edges, state_edges_ca, state_payload, hub_mapping


def build_payload(
    state_edges: dict[str, set[tuple[str, str]]],
    state_edges_ca: dict[str, set[tuple[str, str]]],
    state_payload: dict[str, Any],
    hub_mapping: dict[str, Any],
    sample_extract: dict[str, Any] | None,
) -> dict[str, Any]:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ei, ea = state_edges["inactive"], state_edges["active"]
    jacc = jaccard(ei, ea)
    shared = ei & ea
    union = ei | ea
    priv_i = ei - ea
    priv_a = ea - ei
    frac_i = len(priv_i) / max(len(ei), 1)
    frac_a = len(priv_a) / max(len(ea), 1)
    mean_priv = float(np.mean([frac_i, frac_a]))
    jacc_ca = jaccard(state_edges_ca["inactive"], state_edges_ca["active"])

    hub_edge_j: dict[str, float] = {}
    for hub in HUB_LABELS:
        sets: list[set[tuple[str, str]]] = []
        for st in STATE_ORDER:
            hp = state_payload[st]["hub_participation"].get(hub, {})
            node = hp.get("topo_label")
            if not node or hp.get("degree") is None:
                sets = []
                break
            he = {edge_key(u, v) for u, v in state_edges[st] if u == node or v == node}
            sets.append(he)
        hub_edge_j[hub] = float(jaccard(sets[0], sets[1])) if len(sets) == 2 else float("nan")

    verdicts = assign_verdicts(jacc, mean_priv)
    smoke_all_ok = all(
        state_payload[st]["smoke"]["atoms_ok"] for st in STATE_ORDER
    ) and all(
        t["atoms_ok"]
        for st in STATE_ORDER
        for t in state_payload[st]["trajs"]
    )

    return {
        "generated_utc": generated,
        "branch": "feat/cb2-hubs-functional-topology-test",
        "experiment": "EXPERIMENT_CB2_APO_PILOT_CONTACTS",
        "epistemology": {
            "scope": "EXTERNAL_APO_TRAJ_PILOT",
            "few_trajs_neq_ensemble": True,
            "p2_unchanged": True,
            "no_gi_claim": True,
            "no_docking": True,
            "no_p1_hub_hunt": True,
            "soft_compare_prior": "EXT_PDB_CONTACTS_STATE_DEPENDENT / EXT_STRUCTURAL_ABC_SNAPSHOT_B",
        },
        "contact_def": {
            "name": CONTACT_DEF["name"],
            "geometry": CONTACT_DEF["geometry"],
            "slack_A": CONTACT_DEF["slack_A"],
            "exclude_sequential_protein": CONTACT_DEF["exclude_sequential_protein"],
            "p_ij_edge_threshold": P_IJ_THR,
            "selection": "protein",
            "limitation": CONTACT_DEF["limitation"],
        },
        "secondary_ca_def": {
            "cutoff_A": CA_CUTOFF_A,
            "min_sep": CA_MIN_SEP,
            "p_ij_edge_threshold": P_IJ_THR,
            "drives_verdict": False,
        },
        "thresholds": {
            "jaccard_stable": THR_J_STABLE,
            "mean_frac_private_B": THR_FRAC_PRIVATE_B,
            "jaccard_diffuse": THR_J_DIFFUSE,
        },
        "topology": {
            "file": TOPOLOGY.name,
            "sha256": sha256_file(TOPOLOGY),
            "path": str(TOPOLOGY.relative_to(ROOT)),
        },
        "smoke_all_ok": smoke_all_ok,
        "hub_mapping": hub_mapping,
        "hub_incident_jaccard": hub_edge_j,
        "states": state_payload,
        "metrics_primary": {
            "jaccard_inactive_active": jacc,
            "n_edges": {"inactive": len(ei), "active": len(ea)},
            "n_shared": len(shared),
            "n_union": len(union),
            "frac_private": {"inactive": frac_i, "active": frac_a},
            "mean_frac_private": mean_priv,
            "n_private": {"inactive": len(priv_i), "active": len(priv_a)},
        },
        "metrics_secondary_ca": {
            "jaccard_inactive_active": jacc_ca,
            "n_edges": {
                "inactive": len(state_edges_ca["inactive"]),
                "active": len(state_edges_ca["active"]),
            },
        },
        "sample_extract": sample_extract,
        "verdicts": verdicts,
        "outputs": {
            "json": str(OUT_JSON.relative_to(ROOT)),
            "md": str(OUT_MD.relative_to(ROOT)),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extract-sample",
        type=int,
        default=0,
        metavar="N",
        help="Optionally extract N inactive + N active .nc from zip (no full unpack).",
    )
    parser.add_argument(
        "--use-sample",
        action="store_true",
        help="Analyze SAMPLE_DIR trajs instead of the two primary pilots.",
    )
    parser.add_argument(
        "--out-tag",
        type=str,
        default="",
        help="Optional output filename tag, e.g. sample5 → cb2_apo_pilot_contacts_sample5.{md,json}",
    )
    args = parser.parse_args(argv)

    global OUT_JSON, OUT_MD
    if args.out_tag:
        tag = args.out_tag.strip().lstrip("_")
        OUT_JSON = OUT_DIR / f"cb2_apo_pilot_contacts_{tag}.json"
        OUT_MD = OUT_DIR / f"cb2_apo_pilot_contacts_{tag}.md"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if not TOPOLOGY.is_file():
        raise SystemExit(f"Missing topology: {TOPOLOGY}")

    sample_extract: dict[str, Any] | None = None
    if args.extract_sample and args.extract_sample > 0:
        print(f"[cb2_apo_pilot] extracting {args.extract_sample}+{args.extract_sample} from zip…")
        sample_extract = extract_stratified_sample(args.extract_sample)
        print(f"[cb2_apo_pilot] extract ok={sample_extract.get('ok')}")

    if args.use_sample:
        if not SAMPLE_DIR.is_dir():
            raise SystemExit(f"Missing sample dir: {SAMPLE_DIR}")
        files_by_state = {
            "inactive": sorted(
                p for p in SAMPLE_DIR.glob("*-strip.nc") if "_inactive_" in p.name
            ),
            "active": sorted(
                p for p in SAMPLE_DIR.glob("*-strip.nc") if "_active_" in p.name
            ),
        }
        if not files_by_state["inactive"] or not files_by_state["active"]:
            raise SystemExit("Sample dir missing inactive or active .nc")
        print(
            f"[cb2_apo_pilot] using sample "
            f"{len(files_by_state['inactive'])}+{len(files_by_state['active'])}"
        )
    else:
        files_by_state = {
            st: [TRAJ_DIR / STATE_FILES[st]] for st in STATE_ORDER
        }
        for st, paths in files_by_state.items():
            if not paths[0].is_file():
                raise SystemExit(f"Missing {st} traj: {paths[0]}")

    print("[cb2_apo_pilot] computing VdW persistence contacts…")
    state_edges, state_edges_ca, state_payload, hub_mapping = analyze_nc_list(
        TOPOLOGY, files_by_state
    )
    payload = build_payload(
        state_edges, state_edges_ca, state_payload, hub_mapping, sample_extract
    )
    # If using sample, single-traj limit may be relaxed in note but keep NEEDS_MORE if <5
    if args.use_sample:
        n_i = state_payload["inactive"]["n_trajs"]
        n_a = state_payload["active"]["n_trajs"]
        if n_i >= 5 and n_a >= 5:
            payload["verdicts"]["EXT_APO_PILOT_SINGLE_TRAJ_LIMIT"] = "FALSE_SAMPLE"
            payload["verdicts"]["EXT_APO_PILOT_NEEDS_MORE_TRAJS"] = "OPTIONAL"
        payload["run_mode"] = "stratified_sample"
    else:
        payload["run_mode"] = "primary_pilots"

    OUT_JSON.write_text(json.dumps(payload, indent=2, allow_nan=True), encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")

    v = payload["verdicts"]
    m = payload["metrics_primary"]
    print(f"[cb2_apo_pilot] {v['EXT_APO_PILOT_CONTACTS']}")
    print(f"[cb2_apo_pilot] soft={v['EXT_APO_PILOT_SOFT_COMPARE_PDB']}")
    print(
        f"[cb2_apo_pilot] jaccard={m['jaccard_inactive_active']:.4f} "
        f"mean_frac_private={m['mean_frac_private']:.4f}"
    )
    print(f"[cb2_apo_pilot] wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
