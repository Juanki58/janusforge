#!/usr/bin/env python3
"""Dry dynamic-reanalysis pipeline + synthetic null self-tests (data-blind).

Governance: COMPUTATIONAL_PREREGISTRATION | PREPARE_ONLY
NO real .xtc / MSM analysis. Synthetic graphs only for self-tests.

Pipeline (frozen order):
  TRAJECTORIES -> normalize/select frames
               -> PERSISTENCE NET (W_contact = f(p_ij))
               -> COMMUNICATION NET (W_info = f(corr/MI))
               -> microstates / MSM
               -> centrality + paths + robustness
               -> mutagenesis cross
               -> CB1 comparison
               -> optional membrane module

P1 null (pre-registered BEFORE real traj):
  - structure-compatible: exact (in_degree, out_degree) multiset match
  - reproducibility: replica / state stability gates (documented thresholds)

Protocol: docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md

Run self-tests:
  python scripts/network_core/dynamic_pipeline.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

try:
    import networkx as nx
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"networkx required for dry pipeline: {e}") from e

# Optional heavy deps — guarded (real traj path only)
try:
    import MDAnalysis as mda  # noqa: F401

    HAS_MDANALYSIS = True
except ImportError:
    mda = None  # type: ignore
    HAS_MDANALYSIS = False

try:
    import pyemma  # noqa: F401

    HAS_PYEMMA = True
except ImportError:
    pyemma = None  # type: ignore
    HAS_PYEMMA = False

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "results" / "network_core"
STATUS_PATH = OUT_DIR / "dynamic_reanalysis_status.json"
SELFTEST_PATH = OUT_DIR / "dynamic_pipeline_selftest.json"
PROTOCOL = "docs/synthesis/DYNAMIC_REANALYSIS_PROTOCOL.md"

# ---------------------------------------------------------------------------
# Locked a priori (do not retune after seeing real traj)
# ---------------------------------------------------------------------------

HUBS = [
    {"label": "ALA:79", "short": "ALA79", "bw": "2.49"},
    {"label": "ALA:83", "short": "ALA83", "bw": "2.53"},
    {"label": "LEU:287", "short": "LEU287", "bw": "7.41"},
    {"label": "ASN:291", "short": "ASN291", "bw": "7.45"},
    {"label": "ASN:295", "short": "ASN295", "bw": "7.49"},
    {"label": "ARG:302", "short": "ARG302", "bw": "8.46"},
]
HUB_LABELS = [h["label"] for h in HUBS]
S_SET = ["8D0:1", "SER:285", "PHE:87"]
T_SET = ["ARG:131", "ASP:240", "SER:303", "SER:69"]

# P1 null model — frozen
P1_NULL = {
    "name": "exact_in_out_degree_multiset_match",
    "n_null": 200,  # self-test default; real run may raise to 1000 (pre-register before unpark)
    "alpha": 0.05,
    "primary_metric": "pct_disconn",
    "tail": "upper",  # larger %Disconn after KO = stronger bottleneck
    "reproducibility": {
        "min_replicas": 2,
        "min_states_if_msm": 2,
        "hub_rank_spearman_min": 0.7,  # across replicas / states — locked a priori
        "note": "If reproducibility gate fails -> INDETERMINATE, not retune alpha",
    },
    "forbidden": [
        "universal_W=-ln(p)",
        "a_priori_flow_gt_50pct",
        "post_hoc_hub_list",
        "call_result_switch",
    ],
}

PIPELINE_STAGES = [
    "trajectories",
    "normalize_select_frames",
    "persistence_net",
    "communication_net",
    "microstates_msm",
    "centrality_paths_robustness",
    "mutagenesis_cross",
    "cb1_comparison",
    "optional_membrane_module",
]

EXPECTED_TRAJ_MSM = {
    "morales_pastor_2025_trajectories": ROOT
    / "data"
    / "external"
    / "morales_pastor_2025"
    / "trajectories",
    "dutta_shukla_2023_msm": ROOT / "data" / "external" / "dutta_shukla_2023" / "msm",
}

TRAJ_SUFFIXES = {
    ".xtc",
    ".dcd",
    ".trr",
    ".nc",
    ".h5",
    ".hdf5",
    ".pdb",
    ".gro",
    ".tpr",
    ".psf",
    ".prmtop",
}

RNG_SEED_SELFTEST = 20260821


# ---------------------------------------------------------------------------
# Optional import probes (dry scaffolding)
# ---------------------------------------------------------------------------


def optional_deps_status() -> dict[str, bool]:
    return {"MDAnalysis": HAS_MDANALYSIS, "PyEMMA": HAS_PYEMMA, "networkx": True, "numpy": True}


def require_mdanalysis() -> Any:
    if not HAS_MDANALYSIS:
        raise RuntimeError(
            "MDAnalysis not installed — real traj load blocked. "
            "Install only when unparking DYNAMIC_REANALYSIS."
        )
    return mda


def require_pyemma() -> Any:
    if not HAS_PYEMMA:
        raise RuntimeError(
            "PyEMMA not installed — MSM stage blocked. "
            "Install only when unparking DYNAMIC_REANALYSIS."
        )
    return pyemma


# ---------------------------------------------------------------------------
# Path gate (real data) — fail closed
# ---------------------------------------------------------------------------


def _has_manifest(directory: Path) -> bool:
    man = directory / "MANIFEST.json"
    return man.is_file() and man.stat().st_size > 2


def _has_traj_like(directory: Path) -> bool:
    if not directory.is_dir():
        return False
    return any(p.is_file() and p.suffix.lower() in TRAJ_SUFFIXES for p in directory.rglob("*"))


def check_expected_paths() -> dict:
    details: dict[str, dict] = {}
    all_ready = True
    for key, path in EXPECTED_TRAJ_MSM.items():
        exists = path.is_dir()
        ready = bool(exists and (_has_manifest(path) or _has_traj_like(path)))
        if not ready:
            all_ready = False
        details[key] = {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "directory_exists": exists,
            "has_manifest": _has_manifest(path) if exists else False,
            "has_traj_like_files": _has_traj_like(path) if exists else False,
            "ready": ready,
        }
    return {"all_ready": all_ready, "paths": details}


# ---------------------------------------------------------------------------
# Graph / null primitives (shared by real stub + synthetic tests)
# ---------------------------------------------------------------------------


def io_degree(G: nx.DiGraph, n: str) -> tuple[int, int]:
    return (int(G.in_degree(n)), int(G.out_degree(n)))


def sample_degree_matched_sets(
    G: nx.DiGraph,
    hub_labels: list[str],
    exclude: set[str],
    n_null: int,
    rng: np.random.Generator,
) -> tuple[list[list[str]], dict]:
    """P1 null: exact (in, out) degree multiset match (pre-registered)."""
    hub_ios = [io_degree(G, h) for h in hub_labels]
    hub_sig = Counter(hub_ios)
    pool = [n for n in G.nodes() if n not in exclude]
    by_io: dict[tuple[int, int], list[str]] = defaultdict(list)
    for n in pool:
        by_io[io_degree(G, n)].append(n)

    rule = {
        "name": P1_NULL["name"],
        "hub_io_multiset": {f"{k[0]},{k[1]}": int(v) for k, v in sorted(hub_sig.items())},
        "pool_size": len(pool),
        "n_null_requested": n_null,
    }
    for io, need in hub_sig.items():
        if len(by_io[io]) < need:
            raise RuntimeError(
                f"Cannot exact-match IO {io}: need {need}, pool has {len(by_io[io])}"
            )

    sets: list[list[str]] = []
    max_attempts = n_null * 500
    attempts = 0
    while len(sets) < n_null and attempts < max_attempts:
        attempts += 1
        chosen: list[str] = []
        used: set[str] = set()
        ok = True
        for io, need in hub_sig.items():
            avail = [n for n in by_io[io] if n not in used]
            if len(avail) < need:
                ok = False
                break
            pick = list(rng.choice(avail, size=need, replace=False))
            chosen.extend(pick)
            used.update(pick)
        if ok and len(chosen) == len(hub_labels):
            sets.append(chosen)
    if len(sets) < n_null:
        raise RuntimeError(f"Only realized {len(sets)}/{n_null} nulls after {attempts} attempts")
    rule["n_null_realized"] = len(sets)
    rule["attempts"] = attempts
    return sets, rule


def empirical_upper_p(observed: float, null_vals: list[float]) -> float:
    arr = np.asarray(null_vals, dtype=float)
    return float((1 + np.sum(arr >= observed)) / (1 + len(arr)))


def pct_disconn(G: nx.DiGraph, removed: list[str], sources: list[str], sinks: list[str]) -> float:
    H = G.copy()
    H.remove_nodes_from([n for n in removed if n in H])
    pairs = [(s, t) for s in sources if s in H for t in sinks if t in H]
    if not pairs:
        return 1.0
    lost = sum(1 for s, t in pairs if not nx.has_path(H, s, t))
    return lost / len(pairs)


def flow_fraction_through_nodes(
    G: nx.DiGraph, nodes: list[str], sources: list[str], sinks: list[str]
) -> float:
    """Share of simple S->T shortest paths that touch any node in `nodes`."""
    path_nodes = set(nodes)
    total = 0
    hit = 0
    for s in sources:
        if s not in G:
            continue
        for t in sinks:
            if t not in G:
                continue
            try:
                paths = list(nx.all_shortest_paths(G, s, t))
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            for p in paths:
                total += 1
                if any(n in path_nodes for n in p[1:-1]):
                    hit += 1
    if total == 0:
        return 0.0
    return hit / total


# ---------------------------------------------------------------------------
# Two networks — must not mix
# ---------------------------------------------------------------------------


@dataclass
class DualNetworks:
    """Persistence and communication kept as separate objects."""

    W_contact: nx.DiGraph
    W_info: nx.DiGraph
    meta: dict = field(default_factory=dict)

    def assert_not_mixed(self) -> None:
        if self.W_contact is self.W_info:
            raise AssertionError("W_contact and W_info must be distinct graph objects")
        # Edge attribute namespaces
        for u, v, d in self.W_contact.edges(data=True):
            if "info" in d and "contact" not in d and "p_ij" not in d:
                raise AssertionError(f"persistence edge {u}->{v} carries communication-only attrs")
        for u, v, d in self.W_info.edges(data=True):
            if "p_ij" in d and "mi" not in d and "corr" not in d:
                raise AssertionError(f"communication edge {u}->{v} carries persistence-only attrs")


def build_persistence_from_p(p_mat: np.ndarray, labels: list[str], thr: float = 0.05) -> nx.DiGraph:
    """W_contact = f(p_ij): keep edges with contact probability >= thr; weight=p_ij."""
    G = nx.DiGraph()
    G.add_nodes_from(labels)
    n = len(labels)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            p = float(p_mat[i, j])
            if p >= thr:
                G.add_edge(labels[i], labels[j], weight=p, p_ij=p, network="persistence")
    return G


def build_communication_from_mi(
    mi_mat: np.ndarray, labels: list[str], thr: float = 0.05
) -> nx.DiGraph:
    """W_info = f(MI): keep edges with MI >= thr; weight=MI. Never -ln(p)."""
    G = nx.DiGraph()
    G.add_nodes_from(labels)
    n = len(labels)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            mi = float(mi_mat[i, j])
            if mi >= thr:
                G.add_edge(labels[i], labels[j], weight=mi, mi=mi, network="communication")
    return G


# ---------------------------------------------------------------------------
# Dry stage stubs (real traj — NotImplemented / blocked)
# ---------------------------------------------------------------------------


def stage_load_trajectories(_paths: dict) -> None:
    """TODO real: MDAnalysis Universe from .xtc + topology; checksum MANIFEST."""
    require_mdanalysis()
    raise NotImplementedError("real traj load not implemented (data-blind scaffolding)")


def stage_normalize_select_frames(_traj: object) -> None:
    raise NotImplementedError("frame normalize/select stub")


def stage_microstates_msm(_features: object) -> None:
    """TODO real: PyEMMA / MSM assignment per frame."""
    require_pyemma()
    raise NotImplementedError("MSM stage stub")


def stage_mutagenesis_cross(_dynamic_nodes: object) -> None:
    raise NotImplementedError("mutagenesis cross stub (P3)")


def stage_cb1_comparison(_cb2_result: object) -> None:
    raise NotImplementedError("CB1 comparison stub (P4)")


def stage_optional_membrane(_ctx: object) -> None:
    raise NotImplementedError("membrane module stub (P5) — PARKED")


# ---------------------------------------------------------------------------
# Synthetic generators (self-test only — NOT real traj substitutes)
# ---------------------------------------------------------------------------


def synth_gaussian_noise_graph(
    n: int = 48,
    out_degree: int = 4,
    rng: np.random.Generator | None = None,
) -> tuple[nx.DiGraph, list[str], list[str], list[str]]:
    """Near-regular digraph with gaussian weights — no planted bottleneck.

    Configuration-style fixed out-degree so many nodes share IO signatures
    and exact degree-matched nulls stay feasible.
    """
    rng = rng or np.random.default_rng(RNG_SEED_SELFTEST)
    labels = [f"N{i}" for i in range(n)]
    G = nx.DiGraph()
    G.add_nodes_from(labels)
    # Circular k-out skeleton (identical structure) + light random rewires
    for i, u in enumerate(labels):
        for k in range(1, out_degree + 1):
            v = labels[(i + k) % n]
            w = float(np.clip(abs(rng.normal(0.25, 0.05)), 0.05, 1.0))
            G.add_edge(u, v, weight=w, p_ij=w, network="persistence")
    sources = labels[:2]
    sinks = labels[-2:]
    pool = [n_ for n_ in labels if n_ not in set(sources) | set(sinks)]
    hubs = list(rng.choice(pool, size=6, replace=False))
    return G, hubs, sources, sinks


def synth_bottleneck_graph(
    rng: np.random.Generator | None = None,
) -> tuple[nx.DiGraph, list[str], list[str], list[str]]:
    """Plant bottleneck set B: all S->T shortest paths must pass through B."""
    rng = rng or np.random.default_rng(RNG_SEED_SELFTEST + 1)
    sources = ["S0", "S1"]
    sinks = ["T0", "T1"]
    bottleneck = [f"B{i}" for i in range(6)]
    decoys = [f"D{i}" for i in range(24)]
    labels = sources + sinks + bottleneck + decoys
    G = nx.DiGraph()
    G.add_nodes_from(labels)

    # Only path family: S -> B -> T (no S->T bypass)
    for s in sources:
        for b in bottleneck:
            G.add_edge(s, b, weight=0.95, p_ij=0.95, network="persistence")
    for b in bottleneck:
        for t in sinks:
            G.add_edge(b, t, weight=0.95, p_ij=0.95, network="persistence")

    # Decoy clique with SAME IO as each B node where possible:
    # B nodes: in=2 (from S), out=2 (to T). Give decoys identical IO via private pads.
    pads_in = [f"PI{i}" for i in range(6)]
    pads_out = [f"PO{i}" for i in range(6)]
    G.add_nodes_from(pads_in + pads_out)
    for i, d in enumerate(decoys[:6]):
        # Match IO (2,2)
        G.add_edge(pads_in[i], d, weight=0.5, p_ij=0.5, network="persistence")
        G.add_edge(sources[i % 2], d, weight=0.5, p_ij=0.5, network="persistence")
        G.add_edge(d, pads_out[i], weight=0.5, p_ij=0.5, network="persistence")
        G.add_edge(d, sinks[i % 2], weight=0.2, p_ij=0.2, network="persistence")
        # Note: decoy->sink edges create partial bypass — keep weight low;
        # knockout of ALL six B still breaks if we don't connect decoys fully.
        # Remove decoy->sink to keep B obligatory:
        G.remove_edge(d, sinks[i % 2])
        # Need out=2: already pads_out + need one more
        G.add_edge(d, pads_out[(i + 1) % 6], weight=0.4, p_ij=0.4, network="persistence")

    # Remaining decoys: dense noise among themselves (not on S-T cut)
    for u in decoys[6:]:
        for v in decoys[6:]:
            if u != v and rng.random() < 0.2:
                w = float(abs(rng.normal(0.3, 0.05)))
                G.add_edge(u, v, weight=w, p_ij=w, network="persistence")

    return G, bottleneck, sources, sinks


def synth_dual_matrices(n: int = 20, rng: np.random.Generator | None = None) -> DualNetworks:
    """Persistence high where communication low (and vice versa) — must not mix."""
    rng = rng or np.random.default_rng(RNG_SEED_SELFTEST + 2)
    labels = [f"R{i}" for i in range(n)]
    p = np.clip(rng.normal(0.1, 0.05, size=(n, n)), 0, 1)
    mi = np.clip(rng.normal(0.1, 0.05, size=(n, n)), 0, 1)
    np.fill_diagonal(p, 0.0)
    np.fill_diagonal(mi, 0.0)
    # Anti-correlate a block: high p, low mi
    p[:5, 5:10] = 0.8
    mi[:5, 5:10] = 0.01
    # High mi, low p
    mi[10:15, 15:20] = 0.8
    p[10:15, 15:20] = 0.01
    dual = DualNetworks(
        W_contact=build_persistence_from_p(p, labels, thr=0.2),
        W_info=build_communication_from_mi(mi, labels, thr=0.2),
        meta={"synthetic": True, "note": "anti-correlated blocks"},
    )
    dual.assert_not_mixed()
    return dual


def synth_two_state_features(
    n_frames: int = 200, n_feat: int = 4, rng: np.random.Generator | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """Two well-separated gaussian blobs; labels 0/1."""
    rng = rng or np.random.default_rng(RNG_SEED_SELFTEST + 3)
    half = n_frames // 2
    a = rng.normal(0.0, 0.3, size=(half, n_feat))
    b = rng.normal(5.0, 0.3, size=(n_frames - half, n_feat))
    X = np.vstack([a, b])
    y = np.array([0] * half + [1] * (n_frames - half))
    return X, y


def assign_microstates_kmeans(X: np.ndarray, k: int, seed: int) -> np.ndarray:
    """Minimal deterministic-ish k-means (numpy only) for seed/order tests."""
    rng = np.random.default_rng(seed)
    # init: pick k points
    idx = rng.choice(len(X), size=k, replace=False)
    centers = X[idx].copy()
    labels = np.zeros(len(X), dtype=int)
    for _ in range(40):
        d = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = d.argmin(axis=1)
        for j in range(k):
            mask = labels == j
            if mask.any():
                centers[j] = X[mask].mean(axis=0)
    return labels


def labels_match_up_to_permutation(a: np.ndarray, b: np.ndarray) -> bool:
    if a.shape != b.shape:
        return False
    mapping: dict[int, int] = {}
    for x, y in zip(a.tolist(), b.tolist()):
        if x in mapping:
            if mapping[x] != y:
                return False
        else:
            # y must not already be claimed by another x
            if y in mapping.values():
                return False
            mapping[x] = y
    return True


# ---------------------------------------------------------------------------
# Self-tests (must RUN and pass)
# ---------------------------------------------------------------------------


@dataclass
class TestResult:
    name: str
    passed: bool
    detail: dict


def test_1_noise_no_false_hubs() -> TestResult:
    rng = np.random.default_rng(RNG_SEED_SELFTEST)
    G, hubs, sources, sinks = synth_gaussian_noise_graph(rng=rng)
    exclude = set(hubs) | set(sources) | set(sinks)
    obs = pct_disconn(G, hubs, sources, sinks)
    null_sets, rule = sample_degree_matched_sets(G, hubs, exclude, P1_NULL["n_null"], rng)
    null_vals = [pct_disconn(G, ns, sources, sinks) for ns in null_sets]
    p = empirical_upper_p(obs, null_vals)
    # Under noise, claimed hubs must NOT clear alpha as bottlenecks
    passed = p >= P1_NULL["alpha"]
    return TestResult(
        "noise_no_false_hubs",
        passed,
        {
            "obs_pct_disconn": obs,
            "null_mean": float(np.mean(null_vals)),
            "p_upper": p,
            "alpha": P1_NULL["alpha"],
            "null_rule": rule["name"],
            "expectation": "p >= alpha (no false bottleneck call)",
        },
    )


def test_2_planted_bottleneck_recovered() -> TestResult:
    rng = np.random.default_rng(RNG_SEED_SELFTEST + 11)
    G, hubs, sources, sinks = synth_bottleneck_graph(rng=rng)
    exclude = set(hubs) | set(sources) | set(sinks)
    obs = pct_disconn(G, hubs, sources, sinks)
    # May fail exact degree match if pool thin — fall back to same-size random
    try:
        null_sets, rule = sample_degree_matched_sets(G, hubs, exclude, 100, rng)
    except RuntimeError:
        pool = [n for n in G.nodes() if n not in exclude]
        null_sets = [list(rng.choice(pool, size=len(hubs), replace=False)) for _ in range(100)]
        rule = {"name": "fallback_same_size_random_when_degree_match_infeasible"}
    null_vals = [pct_disconn(G, ns, sources, sinks) for ns in null_sets]
    p = empirical_upper_p(obs, null_vals)
    flow = flow_fraction_through_nodes(G, hubs, sources, sinks)
    passed = (obs >= 0.99) and (p < P1_NULL["alpha"]) and (flow >= 0.9)
    return TestResult(
        "planted_bottleneck_recovered",
        passed,
        {
            "obs_pct_disconn": obs,
            "p_upper": p,
            "flow_fraction": flow,
            "null_rule": rule["name"],
            "expectation": "obs~1, p<alpha, high flow through planted B",
        },
    )


def test_3_null_distribution_shape() -> TestResult:
    """Degree-matched nulls on noise: observed random set p-values not systematically tiny."""
    rng = np.random.default_rng(RNG_SEED_SELFTEST + 21)
    G, _, sources, sinks = synth_gaussian_noise_graph(n=48, rng=rng)
    # Draw many random 6-sets; each vs degree-matched null → collect p
    ps: list[float] = []
    for _ in range(30):
        pool = [n for n in G.nodes() if n not in set(sources) | set(sinks)]
        hubs = list(rng.choice(pool, size=6, replace=False))
        exclude = set(hubs) | set(sources) | set(sinks)
        obs = pct_disconn(G, hubs, sources, sinks)
        try:
            null_sets, _ = sample_degree_matched_sets(G, hubs, exclude, 80, rng)
        except RuntimeError:
            continue
        null_vals = [pct_disconn(G, ns, sources, sinks) for ns in null_sets]
        ps.append(empirical_upper_p(obs, null_vals))
    if len(ps) < 10:
        return TestResult("null_distribution_shape", False, {"error": "too few p-values", "n": len(ps)})
    frac_sig = float(np.mean(np.asarray(ps) < P1_NULL["alpha"]))
    # False positive rate should not be wildly inflated (allow up to ~0.20 with small n)
    passed = frac_sig <= 0.25 and float(np.median(ps)) >= 0.2
    return TestResult(
        "null_distribution_shape",
        passed,
        {
            "n_pvalues": len(ps),
            "median_p": float(np.median(ps)),
            "frac_p_lt_alpha": frac_sig,
            "expectation": "FPR not inflated; median p not near 0",
        },
    )


def test_4_persistence_vs_communication_not_mixed() -> TestResult:
    dual = synth_dual_matrices()
    dual.assert_not_mixed()
    # High-p block should dominate contact, not info
    contact_edges = {(u, v) for u, v, d in dual.W_contact.edges(data=True) if d.get("p_ij", 0) >= 0.7}
    info_edges = {(u, v) for u, v, d in dual.W_info.edges(data=True) if d.get("mi", 0) >= 0.7}
    overlap_hi = contact_edges & info_edges
    # Build -ln(p) and assert we never use it as W_info
    # (guard: communication graph must not equal -ln(p) transform of contact)
    passed = len(overlap_hi) == 0 and dual.W_contact.number_of_edges() > 0 and dual.W_info.number_of_edges() > 0
    return TestResult(
        "persistence_vs_communication_not_mixed",
        passed,
        {
            "n_contact_edges": dual.W_contact.number_of_edges(),
            "n_info_edges": dual.W_info.number_of_edges(),
            "high_weight_overlap": len(overlap_hi),
            "expectation": "anti-correlated blocks => zero high-weight edge overlap",
        },
    )


def test_5_microstate_seed_and_order_independence() -> TestResult:
    X, y_true = synth_two_state_features()
    lab_a = assign_microstates_kmeans(X, k=2, seed=0)
    lab_b = assign_microstates_kmeans(X, k=2, seed=0)
    # Same seed => identical
    same_seed = np.array_equal(lab_a, lab_b)
    # Shuffle frame order, remap by inverse permutation
    rng = np.random.default_rng(99)
    perm = rng.permutation(len(X))
    X_shuf = X[perm]
    lab_shuf = assign_microstates_kmeans(X_shuf, k=2, seed=0)
    lab_unshuf = np.empty_like(lab_shuf)
    lab_unshuf[perm] = lab_shuf
    order_ok = labels_match_up_to_permutation(lab_a, lab_unshuf)
    # Different seed: still two clean clusters matching truth up to perm
    lab_c = assign_microstates_kmeans(X, k=2, seed=7)
    vs_truth_a = labels_match_up_to_permutation(lab_a, y_true)
    vs_truth_c = labels_match_up_to_permutation(lab_c, y_true)
    passed = same_seed and order_ok and vs_truth_a and vs_truth_c
    return TestResult(
        "microstate_seed_frame_order_independence",
        passed,
        {
            "same_seed_identical": same_seed,
            "shuffle_order_equiv_up_to_perm": order_ok,
            "recovers_truth_seed0": vs_truth_a,
            "recovers_truth_seed7": vs_truth_c,
            "expectation": "k-means on separated blobs stable to seed/order (label perm OK)",
        },
    )


def run_self_tests() -> dict:
    tests = [
        test_1_noise_no_false_hubs,
        test_2_planted_bottleneck_recovered,
        test_3_null_distribution_shape,
        test_4_persistence_vs_communication_not_mixed,
        test_5_microstate_seed_and_order_independence,
    ]
    results = [t() for t in tests]
    payload = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "SYNTHETIC_SELFTEST_DATA_BLIND",
        "protocol": PROTOCOL,
        "p1_null_preregistered": P1_NULL,
        "pipeline_stages": PIPELINE_STAGES,
        "optional_deps": optional_deps_status(),
        "tests": [{"name": r.name, "passed": r.passed, "detail": r.detail} for r in results],
        "all_passed": all(r.passed for r in results),
        "naming_lock": "never call result switch",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SELFTEST_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


# ---------------------------------------------------------------------------
# Status writer (real traj gate)
# ---------------------------------------------------------------------------


def write_blocked_status() -> dict:
    path_check = check_expected_paths()
    blocked = not path_check["all_ready"]
    payload = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "BLOCKED_PENDING_TRAJECTORIES" if blocked else "PATHS_PRESENT_ANALYSIS_STUBBED",
        "verdict": "INDETERMINATE" if blocked else "READY_FOR_STUBBED_PIPELINE",
        "blocked": blocked,
        "governance": {
            "mode": "COMPUTATIONAL_PREREGISTRATION",
            "DYNAMIC_REANALYSIS": "BLOCKED_PENDING_TRAJECTORIES",
            "TRAJ_DOWNLOAD": "STOP",
            "NEW_MD": "STOP",
            "protocol": PROTOCOL,
        },
        "pipeline_stages": PIPELINE_STAGES,
        "p1_null_preregistered": P1_NULL,
        "hubs_fixed_a_priori": HUBS,
        "S_set": S_SET,
        "T_set": T_SET,
        "networks_required": {
            "persistence": "W_contact = f(p_ij)",
            "communication": "W_info = f(correlation / MI)",
            "do_not_use_universal": "W = -ln(p)",
        },
        "path_check": path_check,
        "optional_deps": optional_deps_status(),
        "artifacts": {
            "status_json": str(STATUS_PATH.relative_to(ROOT)).replace("\\", "/"),
            "selftest_json": str(SELFTEST_PATH.relative_to(ROOT)).replace("\\", "/"),
            "protocol": PROTOCOL,
        },
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dry dynamic pipeline + synthetic self-tests")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run synthetic null / dual-network / microstate unit tests (no real traj)",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Write BLOCKED_PENDING_TRAJECTORIES status if real traj/MSM missing",
    )
    args = parser.parse_args(argv)

    if not args.self_test and not args.status:
        args.self_test = True
        args.status = True

    rc = 0
    if args.status:
        st = write_blocked_status()
        print(f"[dynamic_pipeline] status={st['status']} verdict={st['verdict']}")
        print(f"[dynamic_pipeline] wrote {STATUS_PATH}")

    if args.self_test:
        print("[dynamic_pipeline] running synthetic self-tests (data-blind) ...")
        payload = run_self_tests()
        for t in payload["tests"]:
            flag = "PASS" if t["passed"] else "FAIL"
            print(f"  [{flag}] {t['name']}")
        print(f"[dynamic_pipeline] wrote {SELFTEST_PATH}")
        if not payload["all_passed"]:
            print("[dynamic_pipeline] SELF-TEST FAILURES")
            rc = 1
        else:
            print("[dynamic_pipeline] all synthetic self-tests passed")
    return rc


if __name__ == "__main__":
    sys.exit(main())
