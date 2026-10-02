"""Tests for P2 dry pipeline — synthetic matrices only (no real CB2 data)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SYS_SCRIPTS = ROOT / "scripts" / "network_core"
if str(SYS_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SYS_SCRIPTS))

import p2_dry_pipeline as p2  # noqa: E402


@pytest.fixture
def rng() -> np.random.Generator:
    return np.random.default_rng(42)


def test_mock_state_ingestion_10000_frames_6_states(rng: np.random.Generator) -> None:
    asg = p2.generate_mock_state_assignment(n_frames=10_000, n_states=6, rng=rng)
    assert asg.n_frames == 10_000
    assert asg.n_states == 6
    assert asg.labels.shape == (10_000,)
    assert set(np.unique(asg.labels).tolist()) == set(range(6))
    # Balanced: each state gets floor or ceil share
    counts = [int(np.sum(asg.labels == s)) for s in range(6)]
    assert min(counts) >= 10_000 // 6
    assert max(counts) <= 10_000 // 6 + 1


def test_load_state_assignment_mock_roundtrip(rng: np.random.Generator) -> None:
    labels = rng.integers(0, 4, size=200)
    asg = p2.load_state_assignment_mock(labels, n_states=4)
    assert asg.n_states == 4
    assert np.array_equal(asg.labels, labels)


def test_persistence_and_communication_shapes(rng: np.random.Generator) -> None:
    n_frames, n = 50, 8
    contacts = (rng.random((n_frames, n, n)) > 0.7).astype(float)
    for t in range(n_frames):
        contacts[t] = np.maximum(contacts[t], contacts[t].T)
        np.fill_diagonal(contacts[t], 0.0)
    features = rng.normal(size=(n_frames, n))
    dual = p2.extract_networks_for_state(contacts, features, state=0)
    assert dual.p_ij.shape == (n, n)
    assert dual.mi_ij.shape == (n, n)
    assert dual.W_contact.number_of_nodes() == n
    assert dual.W_info.number_of_nodes() == n
    # No metric mixing
    for _, _, d in dual.W_contact.edges(data=True):
        assert "p_ij" in d
        assert "mi" not in d
    for _, _, d in dual.W_info.edges(data=True):
        assert "mi" in d
        assert "p_ij" not in d


def test_degree_matched_null_runs(rng: np.random.Generator) -> None:
    import networkx as nx

    G = nx.Graph()
    nodes = [f"R{i}" for i in range(6)]
    G.add_nodes_from(nodes)
    for i in range(5):
        G.add_edge(nodes[i], nodes[i + 1], weight=0.9 - 0.1 * i)
    top = p2.top_k_edges(G, k=3)
    summary = p2.degree_matched_edge_null_overlap(G, top, n_null=50, rng=rng)
    assert summary["n_null"] == 50
    assert "null_jaccard_mean" in summary


def test_replica_intersection_filter() -> None:
    a = [("R0", "R1"), ("R1", "R2"), ("R2", "R3")]
    b = [("R0", "R1"), ("R1", "R2"), ("R4", "R5")]
    c = [("R0", "R1"), ("R8", "R9"), ("R1", "R2")]
    surv = p2.replica_edge_intersection([a, b, c])
    assert surv == [("R0", "R1"), ("R1", "R2")]


def test_full_pipeline_random_matrices_no_crash(rng: np.random.Generator) -> None:
    """Full pipeline on synthetic random-ish tensors — syntax/matrix logic must PASS."""
    asg = p2.generate_mock_state_assignment(n_frames=1200, n_states=6, rng=rng, balanced=True)
    n = 12
    contacts = (rng.random((asg.n_frames, n, n)) > 0.85).astype(float)
    for t in range(asg.n_frames):
        contacts[t] = np.maximum(contacts[t], contacts[t].T)
        np.fill_diagonal(contacts[t], 0.0)
    features = rng.normal(size=(asg.n_frames, n))
    graphs = {}
    for s in range(6):
        idx = asg.frames_for_state(s)
        dual = p2.extract_networks_for_state(contacts[idx], features[idx], state=s)
        graphs[s] = dual.W_info
    # Build 3 bootstrap replicas
    replicas = []
    for r in range(3):
        r_rng = np.random.default_rng(100 + r)
        rep = {}
        for s in range(6):
            idx = asg.frames_for_state(s)
            boot = r_rng.choice(idx, size=len(idx), replace=True)
            dual = p2.extract_networks_for_state(contacts[boot], features[boot], state=s)
            rep[s] = dual.W_info
        replicas.append(rep)
    clf = p2.classify_scenario(graphs, replica_graphs=replicas, n_null=40, rng=rng)
    assert clf.scenario in {
        p2.ESCENARIO_A,
        p2.ESCENARIO_B,
        p2.ESCENARIO_C,
        p2.INDETERMINATE,
    }
    assert 0.0 <= clf.mean_overlap <= 1.0
    assert 0.0 <= clf.mean_concentration <= 1.0


def test_planted_escenario_a_recovered() -> None:
    res = p2.run_p2_dry_pipeline(
        scenario=p2.ESCENARIO_A,
        n_frames=4000,
        n_states=6,
        n_nodes=16,
        n_replicas=3,
        seed=7,
        plant_msm_converged=True,
    )
    assert res.stage0.status == p2.MSM_INTERPRETABLE
    assert res.classification is not None
    assert res.classification.scenario == p2.ESCENARIO_A
    assert res.classification.mean_overlap >= p2.OVERLAP_STABLE_MIN


def test_planted_escenario_b_recovered() -> None:
    res = p2.run_p2_dry_pipeline(
        scenario=p2.ESCENARIO_B,
        n_frames=4000,
        n_states=6,
        n_nodes=16,
        n_replicas=3,
        seed=11,
        plant_msm_converged=True,
    )
    assert res.classification is not None
    assert res.classification.scenario == p2.ESCENARIO_B
    assert res.classification.mean_overlap < 0.40


def test_planted_escenario_c_recovered() -> None:
    res = p2.run_p2_dry_pipeline(
        scenario=p2.ESCENARIO_C,
        n_frames=4000,
        n_states=6,
        n_nodes=16,
        n_replicas=3,
        seed=13,
        plant_msm_converged=True,
    )
    assert res.classification is not None
    assert res.classification.scenario == p2.ESCENARIO_C
    assert res.classification.mean_concentration <= p2.CONC_MAX_DISTRIBUTED + 1e-9


def test_stage0_insufficient_sampling_stops_abc() -> None:
    res = p2.run_p2_dry_pipeline(
        scenario=p2.ESCENARIO_A,
        n_frames=2000,
        n_states=6,
        plant_msm_converged=False,
        seed=99,
    )
    assert res.stage0.status == p2.INSUFFICIENT_SAMPLING
    assert res.stage0.proceed_to_abc is False
    assert res.classification is None
    assert res.assignment is None
    assert res.meta.get("stopped") == p2.INSUFFICIENT_SAMPLING


def test_stage0_converged_proceeds(rng: np.random.Generator) -> None:
    report = p2.mock_msm_convergence_gate(
        n_trajs=5, plant_converged=True, n_metastable=4, rng=rng
    )
    assert report.status == p2.MSM_INTERPRETABLE
    assert report.proceed_to_abc is True
    assert report.n_metastable == 4  # K≠6 is allowed (Dutta not a template)


def test_no_real_data_flags_in_meta() -> None:
    res = p2.run_p2_dry_pipeline(
        scenario=p2.ESCENARIO_C,
        n_frames=600,
        n_states=6,
        n_nodes=10,
        n_replicas=3,
        seed=3,
        plant_msm_converged=True,
    )
    assert res.meta["NO_REAL_DATA"] is True
    assert res.meta["NO_INTERNET"] is True
    assert res.meta["NO_NEW_HUBS"] is True
    assert res.meta["real_p2_data_source_lock"]["dutta_shukla_role"] == (
        "EXTERNAL_COMPARISON_ONLY_NOT_TEMPLATE"
    )
