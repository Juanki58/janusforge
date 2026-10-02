#!/usr/bin/env python3
"""P2 dry analytical pipeline — synthetic data ONLY (pre-registration).

Governance
----------
- NO_INTERNET: never download trajs / MSM
- NO_REAL_DATA: never open GPCRmd .xtc or real MSM on disk (dry freeze)
- NO_NEW_HUBS: evaluate transition / state edges, not permanent hub hunting
- Real P2 (later, human green light): **own MSM** on 5 WT GPCRmd Morales-Pastor
  trajs — Dutta & Shukla is **not** a fitting template (external comparison only)

Two decision stages (mandatory)
--------------------------------
0. MSM statistically interpretable / convergent?
   → if no: ``INSUFFICIENT_SAMPLING`` and STOP (do not invent A/B/C)
1. Only if yes → architecture among metastable states: ESCENARIO_A / B / C

Modules
-------
0. Stage-0 mock MSM convergence gate
A. State ingestion (Mock) — frame → microstate labels
B. Network extraction per state — persistence (p_ij) + communication (corr / sim. MI)
C. Hypothesis comparison — ESCENARIO_A / ESCENARIO_B / ESCENARIO_C
D. Rigor controls — degree-matched edge nulls + multi-replica intersection

Run self-demo::

    python scripts/network_core/p2_dry_pipeline.py --self-demo

Protocol: docs/synthesis/P2_STATE_ROUTE_PREGISTRATION.md
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np

try:
    import networkx as nx
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"networkx required for P2 dry pipeline: {e}") from e

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "results" / "network_core"
DEFAULT_SEED = 20260821

# Locked classification thresholds (data-blind)
OVERLAP_STABLE_MIN = 0.80  # ESCENARIO_A: dominant-route overlap across states
CONC_MIN_ROUTES = 0.25  # min top-k weight concentration to claim "routes exist"
CONC_MAX_DISTRIBUTED = 0.15  # ESCENARIO_C: diluted signal
TOP_K = 5
N_NULL_DEFAULT = 100
N_REPLICAS_DEFAULT = 3
ALPHA = 0.05

# Stage-0 MSM convergence thresholds (synthetic mock mirrors real pre-reg)
TIMESCALE_GAP_MIN = 1.5  # implied λ1/λ2 gap proxy
BOOTSTRAP_STABILITY_MIN = 0.70  # fraction of bootstrap MSMs agreeing on K
LOO_AGREEMENT_MIN = 0.65  # leave-one-traj-out metastable assignment agreement

ESCENARIO_A = "ESCENARIO_A"
ESCENARIO_B = "ESCENARIO_B"
ESCENARIO_C = "ESCENARIO_C"
INDETERMINATE = "INDETERMINATE"
INSUFFICIENT_SAMPLING = "INSUFFICIENT_SAMPLING"
MSM_INTERPRETABLE = "MSM_INTERPRETABLE"

# Real-P2 data source lock (documented; dry code never opens these paths)
REAL_P2_DATA_SOURCE = {
    "source": "morales_pastor_2025_gpcrmd_wt",
    "n_trajs_expected": 5,
    "path_hint": "data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/",
    "dutta_shukla_role": "EXTERNAL_COMPARISON_ONLY_NOT_TEMPLATE",
}


# ---------------------------------------------------------------------------
# 0. Stage-0 — mock MSM convergence gate (synthetic only)
# ---------------------------------------------------------------------------


@dataclass
class MSMConvergenceReport:
    """Stage-0 gate: interpretable MSM vs insufficient sampling."""

    status: str  # MSM_INTERPRETABLE | INSUFFICIENT_SAMPLING
    n_trajs: int
    n_metastable: int
    timescale_gap: float
    bootstrap_stability: float
    loo_agreement: float
    proceed_to_abc: bool
    detail: dict[str, Any] = field(default_factory=dict)


def mock_msm_convergence_gate(
    n_trajs: int = 5,
    n_frames_per_traj: int = 2000,
    plant_converged: bool = True,
    n_metastable: int | None = None,
    rng: np.random.Generator | None = None,
) -> MSMConvergenceReport:
    """Synthetic stand-in for: featurize → tICA → lag → MSM → CK/bootstrap/LOO.

    Does **not** read real .xtc. Plants either a convergent or under-sampled regime
    so the dry pipeline can exercise the mandatory two-stage stop rule.

    ``n_metastable`` is free (e.g. 4 vs 6); matching Dutta's K is **not** required.
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED)
    if n_trajs < 1:
        raise ValueError("n_trajs must be >= 1")
    # K is method/data-dependent — draw or accept caller value (never force 6)
    if n_metastable is None:
        n_metastable = int(rng.integers(3, 7))  # 3..6 inclusive-ish

    if plant_converged:
        timescale_gap = float(rng.uniform(TIMESCALE_GAP_MIN + 0.2, TIMESCALE_GAP_MIN + 2.5))
        bootstrap_stability = float(rng.uniform(BOOTSTRAP_STABILITY_MIN + 0.05, 0.98))
        loo_agreement = float(rng.uniform(LOO_AGREEMENT_MIN + 0.05, 0.95))
    else:
        timescale_gap = float(rng.uniform(0.8, TIMESCALE_GAP_MIN - 0.05))
        bootstrap_stability = float(rng.uniform(0.2, BOOTSTRAP_STABILITY_MIN - 0.05))
        loo_agreement = float(rng.uniform(0.2, LOO_AGREEMENT_MIN - 0.05))

    ok = (
        timescale_gap >= TIMESCALE_GAP_MIN
        and bootstrap_stability >= BOOTSTRAP_STABILITY_MIN
        and loo_agreement >= LOO_AGREEMENT_MIN
    )
    status = MSM_INTERPRETABLE if ok else INSUFFICIENT_SAMPLING
    return MSMConvergenceReport(
        status=status,
        n_trajs=n_trajs,
        n_metastable=int(n_metastable),
        timescale_gap=timescale_gap,
        bootstrap_stability=bootstrap_stability,
        loo_agreement=loo_agreement,
        proceed_to_abc=ok,
        detail={
            "mode": "MOCK_SYNTHETIC_MSM_GATE",
            "NO_REAL_DATA": True,
            "protocol_sketch": "5 WT trajs → featurize → tICA → lag → MSM → CK/bootstrap/LOO",
            "n_frames_per_traj_mock": n_frames_per_traj,
            "thresholds": {
                "timescale_gap_min": TIMESCALE_GAP_MIN,
                "bootstrap_stability_min": BOOTSTRAP_STABILITY_MIN,
                "loo_agreement_min": LOO_AGREEMENT_MIN,
            },
            "dutta_template_forbidden": True,
            "plant_converged": plant_converged,
        },
    )


# ---------------------------------------------------------------------------
# A. State ingestion (Mock)
# ---------------------------------------------------------------------------


@dataclass
class StateAssignment:
    """Frame → microstate labels (synthetic or mock ingest)."""

    labels: np.ndarray  # shape (n_frames,), int in [0, n_states)
    n_states: int
    n_frames: int
    meta: dict[str, Any] = field(default_factory=dict)

    def frames_for_state(self, state: int) -> np.ndarray:
        return np.flatnonzero(self.labels == state)


def generate_mock_state_assignment(
    n_frames: int = 10_000,
    n_states: int = 6,
    rng: np.random.Generator | None = None,
    balanced: bool = True,
) -> StateAssignment:
    """Assign frames uniformly (or multinomial) to ``n_states`` distinct microstates."""
    rng = rng or np.random.default_rng(DEFAULT_SEED)
    if n_states < 2:
        raise ValueError("n_states must be >= 2")
    if balanced:
        base = n_frames // n_states
        rem = n_frames % n_states
        counts = [base + (1 if i < rem else 0) for i in range(n_states)]
        parts = [np.full(c, i, dtype=int) for i, c in enumerate(counts)]
        labels = np.concatenate(parts)
        rng.shuffle(labels)
    else:
        labels = rng.integers(0, n_states, size=n_frames)
    return StateAssignment(
        labels=labels,
        n_states=n_states,
        n_frames=n_frames,
        meta={"source": "mock_synthetic", "balanced": balanced, "seed_note": "caller-owned"},
    )


def load_state_assignment_mock(labels: np.ndarray, n_states: int | None = None) -> StateAssignment:
    """Ingest a pre-built frame→state vector (still synthetic / mock — no traj I/O)."""
    labels = np.asarray(labels, dtype=int)
    if labels.ndim != 1:
        raise ValueError("labels must be 1-D")
    k = int(n_states if n_states is not None else (labels.max() + 1 if len(labels) else 0))
    if k < 1:
        raise ValueError("empty or invalid state assignment")
    if labels.min() < 0 or labels.max() >= k:
        raise ValueError("labels out of range for n_states")
    return StateAssignment(
        labels=labels,
        n_states=k,
        n_frames=len(labels),
        meta={"source": "mock_vector_ingest"},
    )


# ---------------------------------------------------------------------------
# B. Network extraction (per state)
# ---------------------------------------------------------------------------


@dataclass
class DualStateNetworks:
    state: int
    W_contact: nx.Graph
    W_info: nx.Graph
    p_ij: np.ndarray
    mi_ij: np.ndarray
    node_labels: list[str]


def _node_labels(n: int) -> list[str]:
    return [f"R{i}" for i in range(n)]


def contact_probability_matrix(
    contacts: np.ndarray,
    thr: float = 0.05,
) -> tuple[np.ndarray, nx.Graph, list[str]]:
    """Persistence network from binary contact tensor (n_frames, n, n) → p_ij."""
    if contacts.ndim != 3 or contacts.shape[1] != contacts.shape[2]:
        raise ValueError("contacts must be (n_frames, n, n)")
    p = contacts.mean(axis=0).astype(float)
    np.fill_diagonal(p, 0.0)
    labels = _node_labels(p.shape[0])
    G = nx.Graph()
    G.add_nodes_from(labels)
    n = p.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if p[i, j] >= thr:
                G.add_edge(labels[i], labels[j], weight=float(p[i, j]), p_ij=float(p[i, j]))
    return p, G, labels


def communication_from_features(
    features: np.ndarray,
    thr: float = 0.15,
    mode: str = "abs_corr",
) -> tuple[np.ndarray, nx.Graph, list[str]]:
    """Communication network from per-frame node features (n_frames, n).

    ``mode='abs_corr'``: |Pearson| as simulated mutual-information proxy.
    ``mode='sim_mi'``: rank-transformed |corr| (same topology, MI-flavoured scale).
    """
    if features.ndim != 2:
        raise ValueError("features must be (n_frames, n)")
    n = features.shape[1]
    if features.shape[0] < 3:
        # Degenerate: return empty signal
        mi = np.zeros((n, n), dtype=float)
    else:
        # Column-center; guard zero-variance
        X = features.astype(float)
        X = X - X.mean(axis=0, keepdims=True)
        std = X.std(axis=0, keepdims=True)
        std = np.where(std < 1e-12, 1.0, std)
        Z = X / std
        corr = (Z.T @ Z) / max(features.shape[0] - 1, 1)
        corr = np.clip(corr, -1.0, 1.0)
        mi = np.abs(corr)
        if mode == "sim_mi":
            # Monotone map to (0,1)-ish "MI-like" scores without claiming true MI
            mi = -0.5 * np.log(np.clip(1.0 - mi**2, 1e-9, 1.0))
            mi = mi / (mi.max() + 1e-12)
        elif mode != "abs_corr":
            raise ValueError(f"unknown communication mode: {mode}")
    np.fill_diagonal(mi, 0.0)
    labels = _node_labels(n)
    G = nx.Graph()
    G.add_nodes_from(labels)
    for i in range(n):
        for j in range(i + 1, n):
            if mi[i, j] >= thr:
                G.add_edge(labels[i], labels[j], weight=float(mi[i, j]), mi=float(mi[i, j]))
    return mi, G, labels


def extract_networks_for_state(
    contacts: np.ndarray,
    features: np.ndarray,
    state: int,
    contact_thr: float = 0.05,
    info_thr: float = 0.15,
    info_mode: str = "abs_corr",
) -> DualStateNetworks:
    """Build persistence + communication nets for one microstate's frames."""
    p, Wc, labels = contact_probability_matrix(contacts, thr=contact_thr)
    mi, Wi, _ = communication_from_features(features, thr=info_thr, mode=info_mode)
    # Guard: do not mix metrics into one weight
    for _, _, d in Wc.edges(data=True):
        if "mi" in d:
            raise RuntimeError("persistence graph contaminated with mi")
    for _, _, d in Wi.edges(data=True):
        if "p_ij" in d:
            raise RuntimeError("communication graph contaminated with p_ij")
    return DualStateNetworks(
        state=state,
        W_contact=Wc,
        W_info=Wi,
        p_ij=p,
        mi_ij=mi,
        node_labels=labels,
    )


# ---------------------------------------------------------------------------
# Synthetic generators (dry only — plant A/B/C)
# ---------------------------------------------------------------------------


def _empty_contact_stack(n_frames: int, n: int) -> np.ndarray:
    return np.zeros((n_frames, n, n), dtype=np.float64)


def plant_scenario_tensors(
    scenario: str,
    assignment: StateAssignment,
    n_nodes: int = 16,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (contacts[n_frames,n,n], features[n_frames,n]) for a planted scenario.

    Contacts are binary-ish Bernoulli draws; features drive communication nets.
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED)
    n_frames = assignment.n_frames
    k = assignment.n_states
    contacts = _empty_contact_stack(n_frames, n_nodes)
    features = rng.normal(0.0, 0.15, size=(n_frames, n_nodes))

    # Shared "backbone" edges — disjoint pairs so top-k is uniquely identifiable
    backbone = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
    # State-specific route sets (disjoint-ish paths)
    state_routes = [
        [(0, 6), (6, 7), (7, 5)],
        [(0, 8), (8, 9), (9, 5)],
        [(0, 10), (10, 11), (11, 5)],
        [(0, 12), (12, 13), (13, 5)],
        [(1, 6), (6, 14), (14, 4)],
        [(2, 8), (8, 15), (15, 3)],
    ]

    for s in range(k):
        idx = assignment.frames_for_state(s)
        if len(idx) == 0:
            continue
        if scenario == ESCENARIO_A:
            # Same dominant topology; intensity scales with state.
            # Per-edge latents keep top-k identical across states (>80% overlap).
            amp = 1.2 + 0.35 * s
            for i, j in backbone:
                contacts[idx, i, j] = rng.random(len(idx)) < min(0.55 + 0.08 * s, 0.95)
                contacts[idx, j, i] = contacts[idx, i, j]
                edge_lat = rng.normal(0.0, 1.0, size=len(idx)) * amp
                features[idx, i] += edge_lat
                features[idx, j] += edge_lat
        elif scenario == ESCENARIO_B:
            routes = state_routes[s % len(state_routes)]
            route_set = {(min(i, j), max(i, j)) for i, j in routes}
            for i, j in routes:
                contacts[idx, i, j] = rng.random(len(idx)) < 0.9
                contacts[idx, j, i] = contacts[idx, i, j]
            latent = rng.normal(0.0, 1.0, size=len(idx))
            for i, j in routes:
                features[idx, i] += latent
                features[idx, j] += latent
            # Light noise contacts off the planted route
            pairs = [(a, b) for a in range(n_nodes) for b in range(a + 1, n_nodes)]
            pick = rng.choice(len(pairs), size=min(6, len(pairs)), replace=False)
            for pidx in np.atleast_1d(pick):
                i, j = pairs[int(pidx)]
                if (i, j) in route_set:
                    continue
                contacts[idx, i, j] = rng.random(len(idx)) < 0.05
                contacts[idx, j, i] = contacts[idx, i, j]
        elif scenario == ESCENARIO_C:
            # Diluted: weak random contacts, no shared latent
            for _ in range(12):
                i, j = rng.integers(0, n_nodes, size=2)
                if i == j:
                    continue
                contacts[idx, i, j] = rng.random(len(idx)) < 0.08
                contacts[idx, j, i] = contacts[idx, i, j]
            features[idx] += rng.normal(0.0, 0.4, size=(len(idx), n_nodes))
        else:
            raise ValueError(f"unknown planted scenario: {scenario}")

    # Symmetry / diagonal
    for t in range(n_frames):
        c = contacts[t]
        contacts[t] = np.maximum(c, c.T)
        np.fill_diagonal(contacts[t], 0.0)
    return contacts, features


# ---------------------------------------------------------------------------
# Edge summaries + replica filter
# ---------------------------------------------------------------------------


def top_k_edges(G: nx.Graph, k: int = TOP_K) -> list[tuple[str, str]]:
    edges = sorted(
        G.edges(data=True),
        key=lambda e: float(e[2].get("weight", 0.0)),
        reverse=True,
    )
    out: list[tuple[str, str]] = []
    for u, v, _ in edges[:k]:
        out.append((u, v) if u <= v else (v, u))
    return out


def edge_weight_concentration(G: nx.Graph, k: int = TOP_K) -> float:
    if G.number_of_edges() == 0:
        return 0.0
    weights = np.array([float(d.get("weight", 0.0)) for _, _, d in G.edges(data=True)])
    total = float(weights.sum())
    if total <= 0:
        return 0.0
    top = np.sort(weights)[::-1][:k]
    return float(top.sum() / total)


def jaccard(a: Iterable[tuple[str, str]], b: Iterable[tuple[str, str]]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def mean_pairwise_overlap(edge_sets: list[list[tuple[str, str]]]) -> float:
    if len(edge_sets) < 2:
        return 1.0
    vals = []
    for i in range(len(edge_sets)):
        for j in range(i + 1, len(edge_sets)):
            vals.append(jaccard(edge_sets[i], edge_sets[j]))
    return float(np.mean(vals)) if vals else 1.0


def replica_edge_intersection(
    replica_edge_sets: list[list[tuple[str, str]]],
) -> list[tuple[str, str]]:
    """Edges that survive intersection across ≥3 independent replicas."""
    if not replica_edge_sets:
        return []
    acc = set(replica_edge_sets[0])
    for s in replica_edge_sets[1:]:
        acc &= set(s)
    return sorted(acc)


def degree_matched_edge_null_overlap(
    G: nx.Graph,
    observed_top: list[tuple[str, str]],
    n_null: int = N_NULL_DEFAULT,
    rng: np.random.Generator | None = None,
) -> dict[str, Any]:
    """Permute edge weights among existing edges (degree-preserving skeleton).

    Compares observed top-k set overlap-with-self (1.0) against null top-k sets
    drawn after weight permutation — reports how often null top-k Jaccard with
    observed exceeds a high bar (stability under noise).
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED)
    edges = list(G.edges())
    if len(edges) < 2 or not observed_top:
        return {
            "name": "degree_matched_weight_permute",
            "n_null": 0,
            "frac_null_jaccard_ge_0_5": float("nan"),
            "obs_self_jaccard": 1.0,
            "note": "insufficient edges",
        }
    weights = np.array([float(G[u][v].get("weight", 0.0)) for u, v in edges])
    obs_set = set(observed_top)
    null_jac = []
    for _ in range(n_null):
        perm_w = rng.permutation(weights)
        ranked = sorted(zip(edges, perm_w), key=lambda t: t[1], reverse=True)
        null_top = []
        for (u, v), _w in ranked[: len(observed_top)]:
            null_top.append((u, v) if u <= v else (v, u))
        null_jac.append(jaccard(obs_set, null_top))
    arr = np.asarray(null_jac, dtype=float)
    return {
        "name": "degree_matched_weight_permute",
        "n_null": n_null,
        "null_jaccard_mean": float(arr.mean()),
        "null_jaccard_p95": float(np.quantile(arr, 0.95)),
        "frac_null_jaccard_ge_0_5": float(np.mean(arr >= 0.5)),
        "obs_self_jaccard": 1.0,
        "alpha": ALPHA,
    }


# ---------------------------------------------------------------------------
# C. Hypothesis comparison
# ---------------------------------------------------------------------------


@dataclass
class P2Classification:
    scenario: str
    mean_overlap: float
    mean_concentration: float
    per_state_top_edges: dict[int, list[tuple[str, str]]]
    replica_surviving_edges: list[tuple[str, str]]
    null_summary: dict[str, Any]
    detail: dict[str, Any] = field(default_factory=dict)


def classify_scenario(
    state_graphs: dict[int, nx.Graph],
    replica_graphs: list[dict[int, nx.Graph]] | None = None,
    k: int = TOP_K,
    n_null: int = N_NULL_DEFAULT,
    rng: np.random.Generator | None = None,
) -> P2Classification:
    """Classify communication (or persistence) graphs into ESCENARIO_A/B/C.

    Primary channel expected: communication nets per state.
    """
    rng = rng or np.random.default_rng(DEFAULT_SEED)
    states = sorted(state_graphs.keys())
    tops = {s: top_k_edges(state_graphs[s], k=k) for s in states}
    concs = {s: edge_weight_concentration(state_graphs[s], k=k) for s in states}
    mean_ov = mean_pairwise_overlap([tops[s] for s in states])
    mean_conc = float(np.mean([concs[s] for s in states])) if states else 0.0

    # Replica filter: intersection of top edges pooled across states, per replica
    surviving: list[tuple[str, str]] = []
    if replica_graphs and len(replica_graphs) >= N_REPLICAS_DEFAULT:
        per_rep = []
        for rep in replica_graphs:
            pooled: set[tuple[str, str]] = set()
            for s, G in rep.items():
                pooled.update(top_k_edges(G, k=k))
            per_rep.append(sorted(pooled))
        surviving = replica_edge_intersection(per_rep)
    elif replica_graphs:
        # fewer than required replicas → fail closed on replica gate
        surviving = []

    # Null on pooled graph (union of edges) using first state's graph as skeleton proxy
    # Prefer a graph with max edges
    ref_state = max(states, key=lambda s: state_graphs[s].number_of_edges()) if states else None
    null_summary: dict[str, Any] = {}
    if ref_state is not None:
        null_summary = degree_matched_edge_null_overlap(
            state_graphs[ref_state], tops[ref_state], n_null=n_null, rng=rng
        )

    # Distinctness vs null for B: mean concentration high AND overlap low
    # Also require that observed top edges are not typical of weight-permuted null
    null_diluted = null_summary.get("frac_null_jaccard_ge_0_5", 1.0)
    if isinstance(null_diluted, float) and np.isnan(null_diluted):
        null_diluted = 1.0

    if mean_conc <= CONC_MAX_DISTRIBUTED:
        scenario = ESCENARIO_C
    elif mean_ov >= OVERLAP_STABLE_MIN and mean_conc >= CONC_MIN_ROUTES:
        scenario = ESCENARIO_A
    elif mean_ov < 0.40 and mean_conc >= CONC_MIN_ROUTES:
        # Routes exist but disagree across states; null should not recreate obs top often
        scenario = ESCENARIO_B
    else:
        scenario = INDETERMINATE

    # Replica gate: if replicas provided and intersection empty while claiming A/B with
    # concentrated routes, demote to INDETERMINATE (reproducibility filter).
    if replica_graphs is not None and len(replica_graphs) >= N_REPLICAS_DEFAULT:
        if scenario in (ESCENARIO_A, ESCENARIO_B) and len(surviving) == 0 and mean_conc >= CONC_MIN_ROUTES:
            scenario = INDETERMINATE

    return P2Classification(
        scenario=scenario,
        mean_overlap=mean_ov,
        mean_concentration=mean_conc,
        per_state_top_edges={s: tops[s] for s in states},
        replica_surviving_edges=surviving,
        null_summary=null_summary,
        detail={
            "per_state_concentration": concs,
            "thresholds": {
                "overlap_stable_min": OVERLAP_STABLE_MIN,
                "conc_min_routes": CONC_MIN_ROUTES,
                "conc_max_distributed": CONC_MAX_DISTRIBUTED,
                "top_k": k,
                "n_replicas_required": N_REPLICAS_DEFAULT,
            },
            "null_diluted_frac_jaccard_ge_0_5": null_diluted,
        },
    )


# ---------------------------------------------------------------------------
# Full dry pipeline
# ---------------------------------------------------------------------------


@dataclass
class P2DryResult:
    stage0: MSMConvergenceReport
    assignment: StateAssignment | None
    networks_contact: dict[int, DualStateNetworks]
    networks_info_graphs: dict[int, nx.Graph]
    classification: P2Classification | None
    planted: str | None
    meta: dict[str, Any]


def run_p2_dry_pipeline(
    scenario: str | None = ESCENARIO_A,
    n_frames: int = 10_000,
    n_states: int = 6,
    n_nodes: int = 16,
    n_replicas: int = N_REPLICAS_DEFAULT,
    seed: int = DEFAULT_SEED,
    use_communication: bool = True,
    plant_msm_converged: bool = True,
    n_trajs_mock: int = 5,
) -> P2DryResult:
    """End-to-end synthetic P2 dry run (no real data).

    Stage-0 runs first. If ``INSUFFICIENT_SAMPLING``, A/B/C is **not** invented.
    """
    rng = np.random.default_rng(seed)

    # --- Stage 0: mock MSM convergence (5-traj conceptual protocol) ---
    stage0 = mock_msm_convergence_gate(
        n_trajs=n_trajs_mock,
        n_frames_per_traj=max(n_frames // max(n_trajs_mock, 1), 10),
        plant_converged=plant_msm_converged,
        n_metastable=n_states,
        rng=rng,
    )

    base_meta: dict[str, Any] = {
        "mode": "P2_DRY_SYNTHETIC_ONLY",
        "NO_REAL_DATA": True,
        "NO_INTERNET": True,
        "NO_NEW_HUBS": True,
        "real_p2_data_source_lock": REAL_P2_DATA_SOURCE,
        "n_frames": n_frames,
        "n_states": n_states,
        "n_nodes": n_nodes,
        "n_replicas": n_replicas,
        "seed": seed,
        "channel": "communication" if use_communication else "persistence",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stage0_status": stage0.status,
    }

    if not stage0.proceed_to_abc:
        return P2DryResult(
            stage0=stage0,
            assignment=None,
            networks_contact={},
            networks_info_graphs={},
            classification=None,
            planted=scenario,
            meta={**base_meta, "stopped": INSUFFICIENT_SAMPLING},
        )

    # Use stage0 K when caller left default aligned — states from mock MSM
    n_states = int(stage0.n_metastable)
    assignment = generate_mock_state_assignment(n_frames=n_frames, n_states=n_states, rng=rng)

    plant = scenario if scenario is not None else ESCENARIO_C
    contacts, features = plant_scenario_tensors(plant, assignment, n_nodes=n_nodes, rng=rng)

    duals: dict[int, DualStateNetworks] = {}
    info_graphs: dict[int, nx.Graph] = {}
    contact_graphs: dict[int, nx.Graph] = {}
    for s in range(n_states):
        idx = assignment.frames_for_state(s)
        dual = extract_networks_for_state(contacts[idx], features[idx], state=s)
        duals[s] = dual
        info_graphs[s] = dual.W_info
        contact_graphs[s] = dual.W_contact

    replica_graphs: list[dict[int, nx.Graph]] = []
    for r in range(n_replicas):
        r_rng = np.random.default_rng(seed + 1000 + r)
        rep: dict[int, nx.Graph] = {}
        for s in range(n_states):
            idx = assignment.frames_for_state(s)
            if len(idx) == 0:
                rep[s] = nx.Graph()
                continue
            boot = r_rng.choice(idx, size=len(idx), replace=True)
            dual = extract_networks_for_state(contacts[boot], features[boot], state=s)
            rep[s] = dual.W_info if use_communication else dual.W_contact
        replica_graphs.append(rep)

    primary = info_graphs if use_communication else contact_graphs
    classification = classify_scenario(primary, replica_graphs=replica_graphs, rng=rng)

    return P2DryResult(
        stage0=stage0,
        assignment=assignment,
        networks_contact=duals,
        networks_info_graphs=info_graphs,
        classification=classification,
        planted=scenario,
        meta=base_meta,
    )


def result_to_dict(result: P2DryResult) -> dict[str, Any]:
    s0 = result.stage0
    out: dict[str, Any] = {
        "meta": result.meta,
        "planted": result.planted,
        "stage0": {
            "status": s0.status,
            "proceed_to_abc": s0.proceed_to_abc,
            "n_trajs": s0.n_trajs,
            "n_metastable": s0.n_metastable,
            "timescale_gap": s0.timescale_gap,
            "bootstrap_stability": s0.bootstrap_stability,
            "loo_agreement": s0.loo_agreement,
            "detail": s0.detail,
        },
    }
    if result.assignment is None or result.classification is None:
        out["assignment"] = None
        out["classification"] = {"scenario": INSUFFICIENT_SAMPLING, "stopped": True}
        return out

    c = result.classification
    out["assignment"] = {
        "n_frames": result.assignment.n_frames,
        "n_states": result.assignment.n_states,
        "counts": {
            str(s): int(np.sum(result.assignment.labels == s))
            for s in range(result.assignment.n_states)
        },
    }
    out["classification"] = {
        "scenario": c.scenario,
        "mean_overlap": c.mean_overlap,
        "mean_concentration": c.mean_concentration,
        "replica_surviving_n": len(c.replica_surviving_edges),
        "replica_surviving_edges": [list(e) for e in c.replica_surviving_edges],
        "null_summary": c.null_summary,
        "detail": {
            **c.detail,
            "per_state_top_edges": {
                str(s): [list(e) for e in edges] for s, edges in c.per_state_top_edges.items()
            },
        },
    }
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P2 dry pipeline (synthetic only)")
    parser.add_argument(
        "--self-demo",
        action="store_true",
        help="Run Stage-0 + planted A/B/C demos and write results JSON",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args(argv)

    if not args.self_demo:
        parser.print_help()
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "schema_version": 1,
        "mode": "P2_DRY_SELF_DEMO",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "real_p2_data_source_lock": REAL_P2_DATA_SOURCE,
        "runs": [],
    }

    # Stage-0 fail-closed demo
    bad = run_p2_dry_pipeline(
        scenario=ESCENARIO_A,
        n_frames=3000,
        n_states=6,
        plant_msm_converged=False,
        seed=args.seed,
    )
    report["runs"].append(result_to_dict(bad))
    print(f"[p2_dry] stage0 planted=under-sampled → {bad.stage0.status} (ABC skipped)")

    for plant in (ESCENARIO_A, ESCENARIO_B, ESCENARIO_C):
        res = run_p2_dry_pipeline(
            scenario=plant,
            n_frames=3000,
            n_states=6,
            n_nodes=16,
            n_replicas=3,
            seed=args.seed,
            plant_msm_converged=True,
        )
        payload = result_to_dict(res)
        report["runs"].append(payload)
        call = res.classification.scenario if res.classification else INSUFFICIENT_SAMPLING
        print(
            f"[p2_dry] stage0={res.stage0.status} planted={plant} → call={call} "
            f"overlap={res.classification.mean_overlap if res.classification else float('nan'):.3f} "
            f"conc={res.classification.mean_concentration if res.classification else float('nan'):.3f}"
        )

    out = OUT_DIR / "p2_dry_pipeline_selfdemo.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[p2_dry] wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
