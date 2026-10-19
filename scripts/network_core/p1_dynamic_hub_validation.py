#!/usr/bin/env python3
"""P1 — dynamic hub validation on Morales/GPCRmd WT trajs only.

Governance (locked before results):
  - Scope: 5× GPCRmd/1540 WT replicas + psf/pdb; frozen six hubs.
  - Channels A (contact persistence) and B (Cα communication) are SEPARATE —
    never combined into one score.
  - Null / α / hub list from dynamic_pipeline.P1_NULL — no post-hoc retuning.
  - P2–P6 BLOCKED. No Dutta MSM. No docking / de novo / CB1 / Gαi2 reinterpretation.

Verdicts (exact labels):
  P1_DYNAMIC_SUPPORTED | P1_PARTIAL | P1_NOT_SUPPORTED | P1_INDETERMINATE

Outputs:
  results/network_core/p1_dynamic_hub_validation.json
  results/network_core/p1_dynamic_hub_validation.md
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from dynamic_pipeline import (  # noqa: E402
    HUB_LABELS,
    HUBS,
    P1_NULL,
    S_SET,
    T_SET,
    empirical_upper_p,
    pct_disconn,
    sample_degree_matched_sets,
)

try:
    import MDAnalysis as mda
    from MDAnalysis.analysis import align
    from MDAnalysis.lib.distances import capped_distance
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required for P1 real traj: {e}") from e

try:
    import networkx as nx
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"networkx required: {e}") from e

# ---------------------------------------------------------------------------
# Frozen a priori (DO NOT retune after inspecting results)
# ---------------------------------------------------------------------------

TRAJ_DIR = (
    ROOT
    / "data"
    / "external"
    / "morales_pastor_2025"
    / "trajectories"
    / "gpcrmd_dyn2126"
)
PSF = TRAJ_DIR / "24306_dyn_2126.psf"
PDB = TRAJ_DIR / "tmp_dyn_0_2417.pdb"
XTC_FILES = [
    TRAJ_DIR / "24307_trj_2126.xtc",
    TRAJ_DIR / "24308_trj_2126.xtc",
    TRAJ_DIR / "24309_trj_2126.xtc",
    TRAJ_DIR / "24310_trj_2126.xtc",
    TRAJ_DIR / "24311_trj_2126.xtc",
]

# A — Contact persistence (Morales-Pastor Methods + GetContacts VdW layer + AlloViz)
# Paper: GetContacts all chemotypes; AlloViz removes |i-j|==1 and keeps p_ij >= 0.1.
# Implementation: registered GetContacts van der Waals geometric criterion
#   |AB| < Rvdw(A)+Rvdw(B)+0.5 Å for non-hydrogen atoms
# (https://getcontacts.github.io/interactions.html). Chemotype-specific angle
# filters (hbond/pi) and water bridges are NOT re-run (no VMD GetContacts stack);
# VdW envelope is the registered distance layer and is documented as a limitation.
CONTACT_DEF = {
    "name": "getcontacts_vdw_envelope_plus_alloviz_filters",
    "geometry": "|AB| < Rvdw(A)+Rvdw(B)+0.5 Angstrom; A,B non-hydrogen",
    "vdw_radii_A": {
        "H": 1.20,
        "C": 1.70,
        "N": 1.55,
        "O": 1.52,
        "S": 1.80,
        "P": 1.80,
        "F": 1.47,
        "CL": 1.75,
        "BR": 1.85,
        "I": 1.98,
    },
    "slack_A": 0.5,
    "exclude_sequential_protein": True,
    "p_ij_edge_threshold": 0.1,
    "selection": "protein or resname 8D0",
    "references": [
        "Morales-Pastor et al. 2025 Methods (GetContacts + AlloViz p>=0.1, drop |i-j|==1)",
        "https://getcontacts.github.io/interactions.html (vdW criterion)",
    ],
    "limitation": (
        "Full GetContacts chemotypes (hbond angles, pi geometry, water bridges) "
        "not reimplemented; persistence uses registered VdW distance envelope only."
    ),
}

# B — Dynamic communication (Cα fluctuation correlations) — SEPARATE from A
COMM_DEF = {
    "name": "DCC_Ca_fluctuation_correlation",
    "formula": "DCC_ij = <Δr_i·Δr_j> / (sqrt(<Δr_i·Δr_i>) sqrt(<Δr_j·Δr_j>))",
    "alignment": "protein CA; mobile=reference=protein and name CA; ref=frame 0",
    "edge_threshold_abs": 0.3,
    "exclude_sequential_sep_lt": 2,
    "weight": "abs(DCC)",
    "caveat": "Correlation is not causality.",
    "note": "Matrix never mixed with contact persistence weights.",
}

# Real-run null size frozen before analysis (pipeline self-test used 200).
N_NULL_REAL = 1000
ALPHA = float(P1_NULL["alpha"])
SPEARMAN_MIN = float(P1_NULL["reproducibility"]["hub_rank_spearman_min"])
RNG_SEED = 20260821

OUT_JSON = ROOT / "results" / "network_core" / "p1_dynamic_hub_validation.json"
OUT_MD = ROOT / "results" / "network_core" / "p1_dynamic_hub_validation.md"
STATUS_PATH = ROOT / "results" / "network_core" / "dynamic_reanalysis_status.json"

# Soft atoms for VdW lookup
_VDW = {k.upper(): v for k, v in CONTACT_DEF["vdw_radii_A"].items()}
_SLACK = float(CONTACT_DEF["slack_A"])
_MAX_CUT = 2.0 * max(_VDW.values()) + _SLACK + 0.05


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def res_label(resname: str, resid: int) -> str:
    return f"{resname}:{int(resid)}"


def as_bidirected(G_u: nx.Graph) -> nx.DiGraph:
    """Undirected weighted contact/corr → DiGraph with both directions (for P1_NULL)."""
    D = nx.DiGraph()
    D.add_nodes_from(G_u.nodes())
    for u, v, d in G_u.edges(data=True):
        w = float(d.get("weight", 1.0))
        attrs = {k: val for k, val in d.items()}
        D.add_edge(u, v, **attrs)
        D.add_edge(v, u, **attrs)
        D[u][v]["weight"] = w
        D[v][u]["weight"] = w
    return D


def hub_strength(G: nx.Graph | nx.DiGraph, hubs: list[str]) -> float:
    s = 0.0
    for h in hubs:
        if h not in G:
            continue
        if G.is_directed():
            s += 0.5 * (
                float(sum(d.get("weight", 1.0) for _, _, d in G.out_edges(h, data=True)))
                + float(sum(d.get("weight", 1.0) for _, _, d in G.in_edges(h, data=True)))
            )
        else:
            s += float(sum(d.get("weight", 1.0) for _, _, d in G.edges(h, data=True)))
    return float(s)


def hub_betweenness_observed(G: nx.Graph | nx.DiGraph, hubs: list[str]) -> float:
    """Descriptive only (not used in null loop — too expensive at n_null=1000)."""
    if G.number_of_nodes() == 0:
        return 0.0

    def _dist(u, v, d):
        w = float(d.get("weight", 1.0))
        return 1.0 / max(w, 1e-12)

    bw = nx.betweenness_centrality(G, weight=_dist, normalized=True)
    return float(sum(bw.get(h, 0.0) for h in hubs))


def hub_rank_vector(G: nx.Graph | nx.DiGraph, hubs: list[str]) -> np.ndarray:
    """Per-hub strength ranks among all nodes (higher strength → rank 1)."""
    if G.is_directed():
        strength = {
            n: 0.5
            * (
                sum(d.get("weight", 1.0) for _, _, d in G.out_edges(n, data=True))
                + sum(d.get("weight", 1.0) for _, _, d in G.in_edges(n, data=True))
            )
            for n in G.nodes()
        }
    else:
        strength = {
            n: sum(d.get("weight", 1.0) for _, _, d in G.edges(n, data=True))
            for n in G.nodes()
        }
    nodes_sorted = sorted(strength, key=lambda n: (-strength[n], n))
    rank = {n: i + 1 for i, n in enumerate(nodes_sorted)}
    return np.asarray([rank.get(h, len(rank) + 1) for h in hubs], dtype=float)


def mean_pairwise_spearman(rank_rows: list[np.ndarray]) -> float:
    if len(rank_rows) < 2:
        return float("nan")
    from itertools import combinations

    vals = []
    for a, b in combinations(rank_rows, 2):
        if np.std(a) < 1e-12 or np.std(b) < 1e-12:
            vals.append(0.0)
            continue
        # Spearman = Pearson of ranks (already ranks)
        vals.append(float(np.corrcoef(a, b)[0, 1]))
    return float(np.mean(vals)) if vals else float("nan")


def effect_size(obs: float, null_vals: list[float]) -> dict[str, float]:
    arr = np.asarray(null_vals, dtype=float)
    mu = float(np.mean(arr))
    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else float("nan")
    z = (obs - mu) / sd if sd and sd > 0 else float("nan")
    return {
        "observed": float(obs),
        "null_mean": mu,
        "null_std": sd,
        "null_p05": float(np.percentile(arr, 5)),
        "null_p50": float(np.percentile(arr, 50)),
        "null_p95": float(np.percentile(arr, 95)),
        "effect_z": float(z),
    }


# ---------------------------------------------------------------------------
# Trajectory I/O + channel A/B builders
# ---------------------------------------------------------------------------


def load_universe(xtc: Path) -> mda.Universe:
    return mda.Universe(str(PSF), str(xtc))


def build_atom_tables(u: mda.Universe) -> dict[str, Any]:
    sel = u.select_atoms(CONTACT_DEF["selection"])
    heavy = sel.select_atoms("not name H*")
    elements = []
    for atom in heavy:
        el = (atom.element if hasattr(atom, "element") else "").upper()
        if not el or el == "DUMMY":
            # fallback from name
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
    res_ids = heavy.resids.astype(int)
    res_names = list(heavy.resnames)
    labels = [res_label(rn, ri) for rn, ri in zip(res_names, res_ids)]
    unique_labels = sorted(set(labels), key=lambda x: (x.split(":")[0], int(x.split(":")[1])))
    label_index = {lab: i for i, lab in enumerate(unique_labels)}
    atom_lab_idx = np.asarray([label_index[lab] for lab in labels], dtype=np.int32)
    radii = np.asarray([_VDW[e] for e in elements], dtype=np.float64)
    protein_mask = np.asarray(
        [("8D0" not in lab) for lab in unique_labels], dtype=bool
    )
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


def accumulate_contacts(
    u: mda.Universe,
    tables: dict[str, Any],
    frame_slice: slice | None = None,
) -> tuple[np.ndarray, int]:
    """Return symmetric count matrix (n_lab, n_lab) and n_frames used."""
    n = tables["n_labels"]
    counts = np.zeros((n, n), dtype=np.int32)
    heavy = tables["heavy"]
    atom_lab_idx = tables["atom_lab_idx"]
    radii = tables["radii"]
    protein_mask = tables["protein_mask"]
    resnums = tables["resnums"]
    exclude_seq = CONTACT_DEF["exclude_sequential_protein"]

    frames = range(u.trajectory.n_frames)
    if frame_slice is not None:
        frames = range(*frame_slice.indices(u.trajectory.n_frames))

    n_used = 0
    for ts_i in frames:
        u.trajectory[ts_i]
        pos = heavy.positions
        pairs = capped_distance(
            pos, pos, max_cutoff=_MAX_CUT, return_distances=True
        )
        if pairs[0].size == 0:
            n_used += 1
            continue
        idx, dist = pairs
        # unique unordered atom pairs i<j
        mask = idx[:, 0] < idx[:, 1]
        idx = idx[mask]
        dist = dist[mask]
        lim = radii[idx[:, 0]] + radii[idx[:, 1]] + _SLACK
        hit = dist < lim
        idx = idx[hit]
        if idx.size == 0:
            n_used += 1
            continue
        li = atom_lab_idx[idx[:, 0]]
        lj = atom_lab_idx[idx[:, 1]]
        same = li != lj
        li, lj = li[same], lj[same]
        # residue-pair contact present this frame
        # use set of pairs then mark
        seen = set()
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
        n_used += 1
    return counts, n_used


def pmat_to_graph(p_mat: np.ndarray, labels: list[str], thr: float, network: str) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(labels)
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            p = float(p_mat[i, j])
            if p >= thr:
                if network == "persistence":
                    G.add_edge(labels[i], labels[j], weight=p, p_ij=p, network="persistence")
                else:
                    G.add_edge(
                        labels[i],
                        labels[j],
                        weight=p,
                        corr=p,
                        network="communication",
                    )
    return G


def compute_dcc(u: mda.Universe, frame_slice: slice | None = None) -> tuple[np.ndarray, list[str]]:
    ca = u.select_atoms("protein and name CA")
    labels = [res_label(r.resname, int(r.resid)) for r in ca.residues]
    frames = list(range(u.trajectory.n_frames))
    if frame_slice is not None:
        frames = list(range(*frame_slice.indices(u.trajectory.n_frames)))
    # Reference = first frame in slice
    u.trajectory[frames[0]]
    ref = ca.positions.copy()
    ref_c = ref - ref.mean(axis=0)
    coords = []
    for i in frames:
        u.trajectory[i]
        mobile = ca.positions.copy()
        mobile_c = mobile - mobile.mean(axis=0)
        R, _rmsd = align.rotation_matrix(mobile_c, ref_c)
        aligned = mobile_c @ R.T
        coords.append(aligned)
    X = np.asarray(coords, dtype=np.float64)  # (F, N, 3)
    if X.shape[0] < 3:
        raise RuntimeError("Too few frames for DCC")
    mean = X.mean(axis=0)
    dX = X - mean
    dots = np.einsum("f i k, f j k -> i j", dX, dX) / dX.shape[0]
    norms = np.sqrt(np.diag(dots))
    denom = np.outer(norms, norms)
    with np.errstate(divide="ignore", invalid="ignore"):
        dcc = np.where(denom > 0, dots / denom, 0.0)
    np.fill_diagonal(dcc, 0.0)
    resids = np.asarray([int(r.resid) for r in ca.residues], dtype=int)
    min_sep = int(COMM_DEF["exclude_sequential_sep_lt"])
    for i in range(dcc.shape[0]):
        for j in range(i + 1, dcc.shape[0]):
            if abs(int(resids[i]) - int(resids[j])) < min_sep:
                dcc[i, j] = 0.0
                dcc[j, i] = 0.0
    return dcc, labels


def graph_from_dcc(dcc: np.ndarray, labels: list[str]) -> nx.Graph:
    thr = float(COMM_DEF["edge_threshold_abs"])
    G = nx.Graph()
    G.add_nodes_from(labels)
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            r = float(dcc[i, j])
            if abs(r) >= thr:
                G.add_edge(
                    labels[i],
                    labels[j],
                    weight=abs(r),
                    corr=r,
                    network="communication",
                )
    return G


def evaluate_channel(
    G_u: nx.Graph,
    hubs: list[str],
    sources: list[str],
    sinks: list[str],
    channel: str,
    rng: np.random.Generator,
    n_null: int | None = None,
    with_betweenness: bool = True,
) -> dict[str, Any]:
    n_null = N_NULL_REAL if n_null is None else int(n_null)
    missing = [h for h in hubs if h not in G_u]
    D = as_bidirected(G_u)
    present_hubs = [h for h in hubs if h in D]
    present_S = [s for s in sources if s in D]
    present_T = [t for t in sinks if t in D]

    out: dict[str, Any] = {
        "channel": channel,
        "n_nodes": G_u.number_of_nodes(),
        "n_edges": G_u.number_of_edges(),
        "hubs_missing_from_graph": missing,
        "hubs_present": present_hubs,
        "S_present": present_S,
        "T_present": present_T,
    }
    if len(present_hubs) < len(hubs):
        out["status"] = "INDETERMINATE_HUB_MAPPING"
        return out
    if channel == "persistence" and (len(present_S) == 0 or len(present_T) == 0):
        out["status"] = "INDETERMINATE_ST_MAPPING"
        return out

    exclude = set(present_hubs) | set(present_S) | set(present_T)
    try:
        null_sets, rule = sample_degree_matched_sets(
            D, present_hubs, exclude, n_null, rng
        )
    except RuntimeError as e:
        out["status"] = "INDETERMINATE_NULL_INFEASIBLE"
        out["null_error"] = str(e)
        return out

    obs_pct = (
        pct_disconn(D, present_hubs, present_S, present_T)
        if channel == "persistence"
        else None
    )
    obs_str = hub_strength(G_u, present_hubs)
    obs_bw = hub_betweenness_observed(G_u, present_hubs) if with_betweenness else float("nan")

    null_pct: list[float] = []
    null_str: list[float] = []
    for ns in null_sets:
        if channel == "persistence":
            null_pct.append(pct_disconn(D, ns, present_S, present_T))
        null_str.append(hub_strength(G_u, ns))

    primary_name = "pct_disconn" if channel == "persistence" else "hub_set_strength"
    if channel == "persistence":
        obs_primary = float(obs_pct)
        null_primary = null_pct
        p_primary = empirical_upper_p(obs_primary, null_primary)
    else:
        obs_primary = float(obs_str)
        null_primary = null_str
        p_primary = empirical_upper_p(obs_primary, null_primary)

    p_str = empirical_upper_p(obs_str, null_str)

    out.update(
        {
            "status": "OK",
            "null_rule": rule,
            "primary_metric": primary_name,
            "primary": {
                "observed": obs_primary,
                "p_upper": p_primary,
                "alpha": ALPHA,
                "significant": bool(p_primary < ALPHA),
                **{
                    k: v
                    for k, v in effect_size(obs_primary, null_primary).items()
                    if k != "observed"
                },
            },
            "strength": {
                "observed": obs_str,
                "p_upper": p_str,
                "significant": bool(p_str < ALPHA),
                **{
                    k: v
                    for k, v in effect_size(obs_str, null_str).items()
                    if k != "observed"
                },
            },
            "betweenness_observed_only": {
                "observed": obs_bw,
                "note": "Descriptive; not null-tested (cost).",
            },
            "per_hub_degree": {
                h: int(G_u.degree(h)) if h in G_u else 0 for h in hubs
            },
            "per_hub_strength": {
                h: float(
                    sum(d.get("weight", 1.0) for _, _, d in G_u.edges(h, data=True))
                )
                if h in G_u
                else 0.0
                for h in hubs
            },
        }
    )
    return out


def channel_passes(result: dict[str, Any], spearman: float) -> tuple[bool, str]:
    if result.get("status") != "OK":
        return False, result.get("status", "BAD")
    if not (isinstance(spearman, float) and spearman >= SPEARMAN_MIN):
        return False, "REPRO_FAIL"
    if not result["primary"]["significant"]:
        return False, "NULL_NOT_EXCEEDED"
    return True, "PASS"


def decide_verdict(
    a_pass: bool,
    b_pass: bool,
    a_reason: str,
    b_reason: str,
    a_repro_fail: bool,
    b_repro_fail: bool,
    indeterminate: bool,
) -> tuple[str, str]:
    if indeterminate:
        return "P1_INDETERMINATE", "data/topology/traj quality prevent valid evaluation"
    if a_pass and b_pass:
        return (
            "P1_DYNAMIC_SUPPORTED",
            "hubs above null in persistence AND communication with replica reproducibility",
        )
    if a_pass or b_pass:
        which = "persistence" if a_pass else "communication"
        if a_repro_fail or b_repro_fail:
            return (
                "P1_PARTIAL",
                f"{which} above null but replica heterogeneity (Spearman gate)",
            )
        return (
            "P1_PARTIAL",
            f"only {which} channel robust above null",
        )
    # Neither channel above null
    hard_ind = {
        "INDETERMINATE_HUB_MAPPING",
        "INDETERMINATE_ST_MAPPING",
        "INDETERMINATE_NULL_INFEASIBLE",
    }
    if a_reason in hard_ind and b_reason in hard_ind:
        return "P1_INDETERMINATE", f"A={a_reason}; B={b_reason}"
    note = "no signal above null in either channel"
    if a_repro_fail or b_repro_fail:
        note += "; communication hub-rank Spearman also below pre-registered gate"
    return "P1_NOT_SUPPORTED", note


def story_hint(verdict: str, a_pass: bool, b_pass: bool, a_repro: float, b_repro: float) -> str | None:
    """Suggest one of four stories only if data support; else leave open."""
    if verdict == "P1_DYNAMIC_SUPPORTED" and a_pass and b_pass:
        return "persistent"
    if verdict == "P1_PARTIAL" and (a_pass ^ b_pass):
        return "persistent+plastic"
    if verdict == "P1_NOT_SUPPORTED":
        return "distributed"
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RNG_SEED)

    # Provenance hashes (5 trajs)
    traj_meta = []
    for xtc in XTC_FILES:
        if not xtc.is_file():
            raise FileNotFoundError(xtc)
        traj_meta.append(
            {
                "path": str(xtc.relative_to(ROOT)).replace("\\", "/"),
                "bytes": xtc.stat().st_size,
                "sha256": sha256_file(xtc),
            }
        )
    top_meta = {
        "psf": {
            "path": str(PSF.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(PSF),
            "bytes": PSF.stat().st_size,
        },
        "pdb": {
            "path": str(PDB.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(PDB) if PDB.is_file() else None,
            "bytes": PDB.stat().st_size if PDB.is_file() else None,
        },
    }

    per_replica: list[dict[str, Any]] = []
    a_rank_rows: list[np.ndarray] = []
    b_rank_rows: list[np.ndarray] = []
    a_p_mats: list[np.ndarray] = []
    a_labels_ref: list[str] | None = None
    b_dccs: list[np.ndarray] = []
    b_labels_ref: list[str] | None = None
    frame_counts: list[int] = []

    for ri, xtc in enumerate(XTC_FILES, start=1):
        print(f"[P1] replica {ri}/5 {xtc.name} …", flush=True)
        u = load_universe(xtc)
        n_frames = int(u.trajectory.n_frames)
        frame_counts.append(n_frames)
        tables = build_atom_tables(u)
        counts, n_used = accumulate_contacts(u, tables)
        p_mat = counts.astype(np.float64) / max(n_used, 1)
        np.fill_diagonal(p_mat, 0.0)
        labels_a = tables["unique_labels"]
        if a_labels_ref is None:
            a_labels_ref = labels_a
        elif labels_a != a_labels_ref:
            raise RuntimeError(f"Replica {ri} contact label set differs from replica 1")
        a_p_mats.append(p_mat)
        G_a = pmat_to_graph(
            p_mat, labels_a, float(CONTACT_DEF["p_ij_edge_threshold"]), "persistence"
        )
        dcc, labels_b = compute_dcc(u)
        if b_labels_ref is None:
            b_labels_ref = labels_b
        elif labels_b != b_labels_ref:
            raise RuntimeError(f"Replica {ri} CA label set differs from replica 1")
        b_dccs.append(dcc)
        G_b = graph_from_dcc(dcc, labels_b)

        a_eval = evaluate_channel(G_a, HUB_LABELS, S_SET, T_SET, "persistence", rng)
        b_eval = evaluate_channel(G_b, HUB_LABELS, S_SET, T_SET, "communication", rng)
        a_ranks = hub_rank_vector(G_a, HUB_LABELS)
        b_ranks = hub_rank_vector(G_b, HUB_LABELS)
        a_rank_rows.append(a_ranks)
        b_rank_rows.append(b_ranks)

        per_replica.append(
            {
                "replica": ri,
                "xtc": traj_meta[ri - 1]["path"],
                "n_frames": n_frames,
                "n_frames_used_contacts": n_used,
                "dt_ps_header": float(u.trajectory.dt),
                "A_persistence": a_eval,
                "B_communication": b_eval,
                "A_hub_ranks": {h: float(r) for h, r in zip(HUB_LABELS, a_ranks)},
                "B_hub_ranks": {h: float(r) for h, r in zip(HUB_LABELS, b_ranks)},
            }
        )
        del u

    # Aggregate mean p_ij / mean DCC across replicas
    assert a_labels_ref is not None and b_labels_ref is not None
    p_agg = np.mean(np.stack(a_p_mats, axis=0), axis=0)
    dcc_agg = np.mean(np.stack(b_dccs, axis=0), axis=0)
    G_a_agg = pmat_to_graph(
        p_agg, a_labels_ref, float(CONTACT_DEF["p_ij_edge_threshold"]), "persistence"
    )
    G_b_agg = graph_from_dcc(dcc_agg, b_labels_ref)

    a_agg = evaluate_channel(G_a_agg, HUB_LABELS, S_SET, T_SET, "persistence", rng)
    b_agg = evaluate_channel(G_b_agg, HUB_LABELS, S_SET, T_SET, "communication", rng)

    spearman_a = mean_pairwise_spearman(a_rank_rows)
    spearman_b = mean_pairwise_spearman(b_rank_rows)

    a_pass, a_reason = channel_passes(a_agg, spearman_a)
    b_pass, b_reason = channel_passes(b_agg, spearman_b)
    a_repro_fail = not (isinstance(spearman_a, float) and spearman_a >= SPEARMAN_MIN)
    b_repro_fail = not (isinstance(spearman_b, float) and spearman_b >= SPEARMAN_MIN)

    # Leave-one-replica-out
    loo = []
    for leave in range(5):
        idx = [i for i in range(5) if i != leave]
        p_loo = np.mean(np.stack([a_p_mats[i] for i in idx], axis=0), axis=0)
        d_loo = np.mean(np.stack([b_dccs[i] for i in idx], axis=0), axis=0)
        Ga = pmat_to_graph(
            p_loo, a_labels_ref, float(CONTACT_DEF["p_ij_edge_threshold"]), "persistence"
        )
        Gb = graph_from_dcc(d_loo, b_labels_ref)
        ea = evaluate_channel(Ga, HUB_LABELS, S_SET, T_SET, "persistence", rng)
        eb = evaluate_channel(Gb, HUB_LABELS, S_SET, T_SET, "communication", rng)
        ranks_a = [a_rank_rows[i] for i in idx]
        ranks_b = [b_rank_rows[i] for i in idx]
        sa = mean_pairwise_spearman(ranks_a)
        sb = mean_pairwise_spearman(ranks_b)
        ap, ar = channel_passes(ea, sa)
        bp, br = channel_passes(eb, sb)
        v, _ = decide_verdict(ap, bp, ar, br, not (sa >= SPEARMAN_MIN), not (sb >= SPEARMAN_MIN), False)
        loo.append(
            {
                "left_out_replica": leave + 1,
                "A_pass": ap,
                "B_pass": bp,
                "A_p": ea.get("primary", {}).get("p_upper"),
                "B_p": eb.get("primary", {}).get("p_upper"),
                "spearman_A": sa,
                "spearman_B": sb,
                "verdict": v,
            }
        )

    # Traj-length sensitivity: first half of frames per replica → aggregate
    print("[P1] traj-length sensitivity (first half frames) …", flush=True)
    half_p = []
    half_dcc = []
    for xtc in XTC_FILES:
        u = load_universe(xtc)
        mid = u.trajectory.n_frames // 2
        tables = build_atom_tables(u)
        counts, n_used = accumulate_contacts(u, tables, frame_slice=slice(0, mid))
        p_mat = counts.astype(np.float64) / max(n_used, 1)
        np.fill_diagonal(p_mat, 0.0)
        half_p.append(p_mat)
        dcc, _ = compute_dcc(u, frame_slice=slice(0, mid))
        half_dcc.append(dcc)
        del u
    p_half = np.mean(np.stack(half_p, axis=0), axis=0)
    d_half = np.mean(np.stack(half_dcc, axis=0), axis=0)
    Ga_h = pmat_to_graph(
        p_half, a_labels_ref, float(CONTACT_DEF["p_ij_edge_threshold"]), "persistence"
    )
    Gb_h = graph_from_dcc(d_half, b_labels_ref)
    a_half = evaluate_channel(Ga_h, HUB_LABELS, S_SET, T_SET, "persistence", rng)
    b_half = evaluate_channel(Gb_h, HUB_LABELS, S_SET, T_SET, "communication", rng)

    # Frame/replica bootstrap: resample replica-level matrices (lighter null)
    boot = []
    for _b in range(100):
        draw = rng.integers(0, 5, size=5)
        p_b = np.mean(np.stack([a_p_mats[i] for i in draw], axis=0), axis=0)
        d_b = np.mean(np.stack([b_dccs[i] for i in draw], axis=0), axis=0)
        ea = evaluate_channel(
            pmat_to_graph(
                p_b, a_labels_ref, float(CONTACT_DEF["p_ij_edge_threshold"]), "persistence"
            ),
            HUB_LABELS,
            S_SET,
            T_SET,
            "persistence",
            rng,
            n_null=200,
            with_betweenness=False,
        )
        eb = evaluate_channel(
            graph_from_dcc(d_b, b_labels_ref),
            HUB_LABELS,
            S_SET,
            T_SET,
            "communication",
            rng,
            n_null=200,
            with_betweenness=False,
        )
        boot.append(
            {
                "A_significant": bool(ea.get("primary", {}).get("significant", False)),
                "B_significant": bool(eb.get("primary", {}).get("significant", False)),
                "A_p": ea.get("primary", {}).get("p_upper"),
                "B_p": eb.get("primary", {}).get("p_upper"),
            }
        )
    boot_a_frac = float(np.mean([1.0 if x["A_significant"] else 0.0 for x in boot]))
    boot_b_frac = float(np.mean([1.0 if x["B_significant"] else 0.0 for x in boot]))

    indeterminate = a_agg.get("status") != "OK" and b_agg.get("status") != "OK"
    verdict, verdict_note = decide_verdict(
        a_pass, b_pass, a_reason, b_reason, a_repro_fail, b_repro_fail, indeterminate
    )
    story = story_hint(verdict, a_pass, b_pass, spearman_a, spearman_b)

    report = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": {
            "system": "Morales-Pastor WT CB2 / GPCRmd publication_id 1540 / dyn2126",
            "replicas": 5,
            "hubs_fixed": HUBS,
            "S_set": S_SET,
            "T_set": T_SET,
            "excluded": ["Dutta_MSM", "CB1", "new_MD", "docking", "de_novo", "Gai2_reinterpretation"],
            "gates": {"P2_P6": "BLOCKED", "CONTRACT_v1.0": "ARCHIVED_HISTORICAL"},
        },
        "definitions_frozen_a_priori": {
            "A_contact_persistence": CONTACT_DEF,
            "B_communication": COMM_DEF,
            "P1_NULL": {**P1_NULL, "n_null_real_run": N_NULL_REAL},
            "channels_combined_score": False,
        },
        "inputs": {
            "trajectories": traj_meta,
            "topology": top_meta,
            "frames_per_replica": frame_counts,
            "note_dt": (
                "XTC header dt may be unreliable; report uses frame counts. "
                "GPCRmd/Morales deposit ≈ 400 ns / replica with ~1 frame/ns."
            ),
        },
        "per_replica": per_replica,
        "aggregate": {
            "A_persistence": a_agg,
            "B_communication": b_agg,
            "reproducibility": {
                "spearman_hub_ranks_A": spearman_a,
                "spearman_hub_ranks_B": spearman_b,
                "spearman_min_preregistered": SPEARMAN_MIN,
                "A_repro_pass": bool(spearman_a >= SPEARMAN_MIN),
                "B_repro_pass": bool(spearman_b >= SPEARMAN_MIN),
            },
            "channel_gates": {
                "A_pass": a_pass,
                "A_reason": a_reason,
                "B_pass": b_pass,
                "B_reason": b_reason,
            },
        },
        "robustness": {
            "leave_one_replica_out": loo,
            "traj_length_first_half": {
                "A_persistence": a_half,
                "B_communication": b_half,
            },
            "bootstrap_replicas_n100_null200": {
                "frac_A_significant": boot_a_frac,
                "frac_B_significant": boot_b_frac,
            },
        },
        "verdict": verdict,
        "verdict_note": verdict_note,
        "suggested_story": story,
        "suggested_story_note": (
            "One of persistent / persistent+plastic / distributed / state-specific "
            "only if supported; else null. state-specific requires MSM (P2 BLOCKED)."
        ),
        "does_not_answer": [
            "Gi control",
            "CB2-specificity",
            "MSM state changes",
            "membrane",
            "chemical switch",
        ],
        "artifacts": {
            "json": str(OUT_JSON.relative_to(ROOT)).replace("\\", "/"),
            "md": str(OUT_MD.relative_to(ROOT)).replace("\\", "/"),
        },
    }

    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(report), encoding="utf-8")
    update_status(report)
    print(f"[P1] verdict={verdict}", flush=True)
    print(f"[P1] wrote {OUT_JSON}", flush=True)
    print(f"[P1] wrote {OUT_MD}", flush=True)
    return 0


def render_md(r: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# P1 — Dynamic hub validation (GPCRmd/1540 WT only)")
    lines.append("")
    lines.append(f"**Generated (UTC):** `{r['generated_utc']}`")
    lines.append(f"**Verdict:** `{r['verdict']}`")
    lines.append(f"**Note:** {r['verdict_note']}")
    lines.append(
        f"**Suggested story (non-forced):** `{r['suggested_story']}` — {r['suggested_story_note']}"
    )
    lines.append("")
    lines.append("## Scope / governance")
    lines.append("")
    lines.append("- 5 WT GPCRmd/1540 replicas + psf/pdb; frozen six hubs.")
    lines.append("- Channels **A** (persistence) and **B** (communication) kept **separate**.")
    lines.append("- P2–P6 **BLOCKED**. No Dutta MSM, CB1, docking, de novo, Gαi2 reinterpretation.")
    lines.append("- Positive P1 = reproducible signal above background — **not** proof hubs are 100% permanent.")
    lines.append("")
    lines.append("## Inputs (SHA256 of 5 trajs)")
    lines.append("")
    lines.append("| File | bytes | sha256 |")
    lines.append("|------|------:|--------|")
    for t in r["inputs"]["trajectories"]:
        lines.append(f"| `{t['path']}` | {t['bytes']} | `{t['sha256']}` |")
    lines.append("")
    lines.append(
        f"**Frames/replica:** {r['inputs']['frames_per_replica']} — {r['inputs']['note_dt']}"
    )
    lines.append("")
    lines.append("## Exact definitions (frozen a priori)")
    lines.append("")
    lines.append("### A — Contact persistence")
    lines.append("")
    cd = r["definitions_frozen_a_priori"]["A_contact_persistence"]
    lines.append(f"- **Name:** `{cd['name']}`")
    lines.append(f"- **Geometry:** {cd['geometry']}")
    lines.append(f"- **p_ij edge threshold:** `{cd['p_ij_edge_threshold']}` (AlloViz/Morales)")
    lines.append(f"- **Exclude sequential protein contacts:** `{cd['exclude_sequential_protein']}`")
    lines.append(f"- **Limitation:** {cd['limitation']}")
    lines.append("")
    lines.append("### B — Dynamic communication")
    lines.append("")
    bd = r["definitions_frozen_a_priori"]["B_communication"]
    lines.append(f"- **Name:** `{bd['name']}`")
    lines.append(f"- **Formula:** `{bd['formula']}`")
    lines.append(f"- **|DCC| edge threshold:** `{bd['edge_threshold_abs']}`")
    lines.append(f"- **Caveat:** {bd['caveat']}")
    lines.append("")
    lines.append("### Null")
    lines.append("")
    pn = r["definitions_frozen_a_priori"]["P1_NULL"]
    lines.append(
        f"- `{pn['name']}`; n_null(real)={pn['n_null_real_run']}; α={pn['alpha']}; "
        f"primary(A)=`{pn['primary_metric']}`; Spearman≥{pn['reproducibility']['hub_rank_spearman_min']}"
    )
    lines.append("")
    lines.append("## Aggregate results")
    lines.append("")
    agg = r["aggregate"]
    for key, title in [
        ("A_persistence", "A — Persistence"),
        ("B_communication", "B — Communication"),
    ]:
        block = agg[key]
        lines.append(f"### {title}")
        lines.append("")
        if block.get("status") != "OK":
            lines.append(f"- Status: `{block.get('status')}`")
        else:
            p = block["primary"]
            lines.append(
                f"- Primary `{block['primary_metric']}`: obs={p['observed']:.4g}, "
                f"p={p['p_upper']:.4g}, z={p.get('effect_z')}, "
                f"null mean±sd={p.get('null_mean'):.4g}±{p.get('null_std'):.4g}, "
                f"sig={p['significant']}"
            )
            lines.append(
                f"- Strength: obs={block['strength']['observed']:.4g}, "
                f"p={block['strength']['p_upper']:.4g}, z={block['strength'].get('effect_z')}"
            )
            lines.append(
                f"- Betweenness (observed only): "
                f"{block.get('betweenness_observed_only', {}).get('observed')}"
            )
            lines.append(f"- Per-hub degree: `{block['per_hub_degree']}`")
            lines.append(f"- Per-hub strength: `{block['per_hub_strength']}`")
        lines.append("")
    repro = agg["reproducibility"]
    lines.append("### Reproducibility (hub-rank Spearman across replicas)")
    lines.append("")
    lines.append(
        f"- A: {repro['spearman_hub_ranks_A']:.4f} (pass={repro['A_repro_pass']})"
    )
    lines.append(
        f"- B: {repro['spearman_hub_ranks_B']:.4f} (pass={repro['B_repro_pass']})"
    )
    lines.append(
        f"- Gates: A_pass={agg['channel_gates']['A_pass']} ({agg['channel_gates']['A_reason']}); "
        f"B_pass={agg['channel_gates']['B_pass']} ({agg['channel_gates']['B_reason']})"
    )
    lines.append("")
    lines.append("## Per-replica summary")
    lines.append("")
    lines.append("| Rep | frames | A p(primary) | A sig | B p(primary) | B sig |")
    lines.append("|----:|-------:|-------------:|:-----:|-------------:|:-----:|")
    for pr in r["per_replica"]:
        ap = pr["A_persistence"].get("primary", {})
        bp = pr["B_communication"].get("primary", {})
        lines.append(
            f"| {pr['replica']} | {pr['n_frames']} | "
            f"{ap.get('p_upper', 'NA')} | {ap.get('significant', 'NA')} | "
            f"{bp.get('p_upper', 'NA')} | {bp.get('significant', 'NA')} |"
        )
    lines.append("")
    lines.append("## Robustness")
    lines.append("")
    lines.append("### Leave-one-replica-out")
    lines.append("")
    lines.append("| Left out | A_pass | B_pass | A_p | B_p | verdict |")
    lines.append("|--------:|:------:|:------:|----:|----:|---------|")
    for row in r["robustness"]["leave_one_replica_out"]:
        lines.append(
            f"| {row['left_out_replica']} | {row['A_pass']} | {row['B_pass']} | "
            f"{row['A_p']} | {row['B_p']} | `{row['verdict']}` |"
        )
    lines.append("")
    th = r["robustness"]["traj_length_first_half"]
    lines.append("### Traj-length sensitivity (first half frames)")
    lines.append("")
    for key, title in [("A_persistence", "A"), ("B_communication", "B")]:
        block = th[key]
        if block.get("status") == "OK":
            lines.append(
                f"- {title}: p={block['primary']['p_upper']:.4g}, "
                f"sig={block['primary']['significant']}"
            )
        else:
            lines.append(f"- {title}: `{block.get('status')}`")
    boot = r["robustness"]["bootstrap_replicas_n100_null200"]
    lines.append("")
    lines.append(
        f"### Bootstrap replicas (n=100, null=200): frac A sig={boot['frac_A_significant']:.3f}; "
        f"frac B sig={boot['frac_B_significant']:.3f}"
    )
    lines.append("")
    lines.append("## P1 does NOT answer")
    lines.append("")
    for x in r["does_not_answer"]:
        lines.append(f"- {x}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*End P1 report. STOP — no P2.*")
    lines.append("")
    return "\n".join(lines)


def update_status(report: dict[str, Any]) -> None:
    status = {
        "schema_version": 1,
        "generated_utc": report["generated_utc"],
        "status": "P1_COMPLETE_STOP",
        "verdict": report["verdict"],
        "blocked": False,
        "P1": {
            "complete": True,
            "verdict": report["verdict"],
            "artifacts": report["artifacts"],
            "channels_separate": True,
        },
        "P2_P6": "BLOCKED",
        "MSM_data_debt": "Dutta-Shukla MSM still missing — do NOT invent metastable states from Morales trajs",
        "governance": {
            "mode": "P1_EXECUTED_GPCRmd_ONLY",
            "DYNAMIC_REANALYSIS": "P1_DONE_AWAITING_JOINT_REVIEW",
            "NEW_MD": "STOP",
            "DOCKING": "STOP",
            "DE_NOVO": "STOP",
            "protocol": "docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md",
            "author_email_contingency": "REGISTERED_DO_NOT_EMAIL",
        },
        "hubs_fixed_a_priori": HUBS,
        "p1_null_preregistered": {**P1_NULL, "n_null_real_run": N_NULL_REAL},
        "networks_required": {
            "persistence": "W_contact = f(p_ij) — SEPARATE",
            "communication": "W_info = f(DCC_Ca) — SEPARATE",
            "do_not_use_universal": "W = -ln(p)",
            "combined_score": False,
        },
        "path_check": {
            "morales_gpcrmd_1540": True,
            "dutta_shukla_msm": False,
        },
        "artifacts": {
            "p1_json": report["artifacts"]["json"],
            "p1_md": report["artifacts"]["md"],
            "status_json": str(STATUS_PATH.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    STATUS_PATH.write_text(json.dumps(status, indent=2), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
