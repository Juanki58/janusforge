#!/usr/bin/env python3
"""EXTERNAL comparison — Dutta & Shukla 2023 Final_MSM kinetics (CB1 vs CB2).

Pre-registration: docs/synthesis/EXPERIMENT_EXTERNAL_DUTTA_MSM.md

Epistemology: EXTERNAL_COMPARISON only. Does NOT reopen P2 Gate-1 / structural A/B/C.
Without trajectories: EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES.

CLI::

    micromamba run -n janus_p1 python scripts/network_core/external_dutta_msm_compare.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MSM_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "msm"
MANIFEST_PATH = MSM_DIR / "MANIFEST.json"
PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_EXTERNAL_DUTTA_MSM.md"
OUT_DIR = ROOT / "results" / "network_core"
OUT_STEM = "external_dutta_msm_compare"

K = 6
LAG = 1
TAU_EDGE = 0.05
N_BOOT = 200
SEED = 20260910
# Similarity / distinctness thresholds (pre-registered)
L1_SIM_MAX = 0.20
ROW_TV_SIM_MAX = 0.15
P_BOOT_SIM_MIN = 0.10
# Kinetic pattern thresholds
ROW_ENT_A_MAX = 0.45
SPARSITY_A_MAX = 0.35
N_STRONG_A_MAX = 2.0
TOP_PATH_B_MAX = 0.50
ROW_TV_B_MIN = 0.25
ROW_ENT_C_MIN = 0.75
SPARSITY_C_MIN = 0.60


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def verify_manifest() -> dict[str, Any]:
    man = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    checks = []
    for entry in man["files"]:
        path = MSM_DIR / entry["name"]
        if not path.exists():
            raise FileNotFoundError(path)
        got = sha256_file(path)
        ok = got == entry["sha256"].upper()
        checks.append(
            {
                "name": entry["name"],
                "bytes": path.stat().st_size,
                "sha256_ok": ok,
                "sha256": got,
            }
        )
        if not ok:
            raise ValueError(f"SHA mismatch for {entry['name']}: {got} != {entry['sha256']}")
        if path.stat().st_size != entry["bytes"]:
            raise ValueError(f"Size mismatch for {entry['name']}")
    return {"manifest": man, "checks": checks}


def load_receptor(prefix: str) -> dict[str, Any]:
    cl_path = MSM_DIR / f"{prefix}_msm_feature_final_clustering.pkl"
    pr_path = MSM_DIR / f"{prefix}_state_prob.pkl"
    with cl_path.open("rb") as f:
        clustering = pickle.load(f)
    with pr_path.open("rb") as f:
        state_prob = pickle.load(f)
    if len(clustering) != len(state_prob):
        raise ValueError(f"{prefix}: traj count mismatch {len(clustering)} vs {len(state_prob)}")

    hard_seqs: list[np.ndarray] = []
    soft_seqs: list[np.ndarray] = []
    n_trunc = 0
    lengths: list[int] = []
    for cl, pr in zip(clustering, state_prob):
        cl_a = np.asarray(cl).reshape(-1)
        pr_a = np.asarray(pr, dtype=np.float64)
        if pr_a.ndim != 2 or pr_a.shape[1] != K:
            raise ValueError(f"{prefix}: unexpected state_prob shape {pr_a.shape}")
        t = min(cl_a.shape[0], pr_a.shape[0])
        if t == 0:
            continue
        if cl_a.shape[0] != pr_a.shape[0]:
            n_trunc += 1
        pr_a = pr_a[:t]
        hard = np.argmax(pr_a, axis=1).astype(np.int32)
        hard_seqs.append(hard)
        soft_seqs.append(pr_a)
        lengths.append(t)

    return {
        "prefix": prefix,
        "n_traj": len(hard_seqs),
        "n_truncations": n_trunc,
        "lengths": lengths,
        "n_frames": int(sum(lengths)),
        "hard_seqs": hard_seqs,
        "soft_seqs": soft_seqs,
        "n_microstate_labels_global": int(
            len({int(x) for traj in clustering for x in np.unique(np.asarray(traj))})
        ),
    }


def count_transitions(seqs: list[np.ndarray], n_states: int = K, lag: int = LAG) -> np.ndarray:
    C = np.zeros((n_states, n_states), dtype=np.float64)
    for s in seqs:
        C += traj_transition_counts(s, n_states=n_states, lag=lag)
    return C


def traj_transition_counts(s: np.ndarray, n_states: int = K, lag: int = LAG) -> np.ndarray:
    if s.shape[0] <= lag:
        return np.zeros((n_states, n_states), dtype=np.float64)
    src = s[:-lag].astype(np.int64, copy=False)
    dst = s[lag:].astype(np.int64, copy=False)
    flat = src * n_states + dst
    return np.bincount(flat, minlength=n_states * n_states).astype(np.float64).reshape(
        n_states, n_states
    )


def traj_occ_counts(s: np.ndarray, n_states: int = K) -> np.ndarray:
    return np.bincount(s.astype(np.int64, copy=False), minlength=n_states)[:n_states].astype(
        np.float64
    )


def traj_dwell_stats(s: np.ndarray, n_states: int = K) -> tuple[np.ndarray, np.ndarray]:
    sums = np.zeros(n_states, dtype=np.float64)
    counts = np.zeros(n_states, dtype=np.float64)
    if s.size == 0:
        return sums, counts
    # vectorized run-length via change points
    change = np.flatnonzero(s[1:] != s[:-1]) + 1
    starts = np.r_[0, change]
    ends = np.r_[change, s.size]
    for a, b in zip(starts, ends):
        st = int(s[a])
        sums[st] += b - a
        counts[st] += 1
    return sums, counts


def precompute_traj_tables(hard_seqs: list[np.ndarray]) -> dict[str, np.ndarray]:
    n = len(hard_seqs)
    C = np.zeros((n, K, K), dtype=np.float64)
    occ = np.zeros((n, K), dtype=np.float64)
    dwell_sum = np.zeros((n, K), dtype=np.float64)
    dwell_n = np.zeros((n, K), dtype=np.float64)
    for i, s in enumerate(hard_seqs):
        C[i] = traj_transition_counts(s)
        occ[i] = traj_occ_counts(s)
        ds, dn = traj_dwell_stats(s)
        dwell_sum[i] = ds
        dwell_n[i] = dn
    return {"C": C, "occ": occ, "dwell_sum": dwell_sum, "dwell_n": dwell_n}


def row_normalize(C: np.ndarray, eps_flag: dict[str, Any] | None = None) -> np.ndarray:
    P = np.zeros_like(C, dtype=np.float64)
    used_add_one = False
    for i in range(C.shape[0]):
        row = C[i].copy()
        s = row.sum()
        if s <= 0:
            row += 1.0
            s = row.sum()
            used_add_one = True
        P[i] = row / s
    if eps_flag is not None:
        eps_flag["add_one_smoothing_used"] = used_add_one
    return P


def entropy(p: np.ndarray, axis: int | None = None) -> np.ndarray | float:
    p = np.asarray(p, dtype=np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        logp = np.where(p > 0, np.log(p), 0.0)
    h = -np.sum(p * logp, axis=axis)
    return h


def hard_populations(seqs: list[np.ndarray], n_states: int = K) -> np.ndarray:
    counts = np.zeros(n_states, dtype=np.float64)
    for s in seqs:
        counts += traj_occ_counts(s, n_states=n_states)
    total = counts.sum()
    if total <= 0:
        return np.full(n_states, 1.0 / n_states)
    return counts / total


def soft_populations(soft_seqs: list[np.ndarray]) -> np.ndarray:
    acc = np.zeros(K, dtype=np.float64)
    n = 0
    for pr in soft_seqs:
        acc += pr.sum(axis=0)
        n += pr.shape[0]
    return acc / max(n, 1)


def dwell_means(seqs: list[np.ndarray], n_states: int = K) -> np.ndarray:
    sums = np.zeros(n_states, dtype=np.float64)
    counts = np.zeros(n_states, dtype=np.float64)
    for s in seqs:
        ds, dn = traj_dwell_stats(s, n_states=n_states)
        sums += ds
        counts += dn
    out = np.full(n_states, np.nan)
    mask = counts > 0
    out[mask] = sums[mask] / counts[mask]
    return out


def metrics_from_tables(C: np.ndarray, occ: np.ndarray, dwell_sum: np.ndarray, dwell_n: np.ndarray) -> dict[str, Any]:
    """Aggregate stacked per-traj tables (already selected/summed over traj axis)."""
    if C.ndim == 3:
        C = C.sum(axis=0)
        occ = occ.sum(axis=0)
        dwell_sum = dwell_sum.sum(axis=0)
        dwell_n = dwell_n.sum(axis=0)
    P = row_normalize(C)
    pi = occ / max(occ.sum(), 1.0)
    dwell = np.full(K, np.nan)
    mask = dwell_n > 0
    dwell[mask] = dwell_sum[mask] / dwell_n[mask]
    kg = kinetic_graph_metrics(P)
    return {"C": C, "P": P, "pi": pi, "dwell": dwell, "kg": kg}

def kinetic_graph_metrics(P: np.ndarray, tau: float = TAU_EDGE) -> dict[str, Any]:
    row_h = np.array([float(entropy(P[i])) for i in range(P.shape[0])])
    logk = float(np.log(K))
    row_h_norm = row_h / logk
    off = ~np.eye(K, dtype=bool)
    strong = (P >= tau) & off
    edge_sparsity = float(strong.sum() / off.sum())
    n_strong_out = strong.sum(axis=1).astype(float)
    top_edges = []
    for i in range(K):
        row = P[i].copy()
        row[i] = -1.0
        j = int(np.argmax(row))
        top_edges.append((i, j))
    return {
        "row_entropy": row_h.tolist(),
        "row_entropy_norm": row_h_norm.tolist(),
        "mean_row_entropy_norm": float(row_h_norm.mean()),
        "max_row_entropy_norm": float(row_h_norm.max()),
        "edge_sparsity": edge_sparsity,
        "n_strong_out": n_strong_out.tolist(),
        "mean_n_strong_out": float(n_strong_out.mean()),
        "top_exit_edges": top_edges,
        "P_ii": np.diag(P).tolist(),
        "escape_rate": (1.0 - np.diag(P)).tolist(),
    }


def top_path_jaccard(edges_a: list[tuple[int, int]], edges_b: list[tuple[int, int]]) -> float:
    sa = set(edges_a)
    sb = set(edges_b)
    if not sa and not sb:
        return 1.0
    return float(len(sa & sb) / len(sa | sb))


def mean_row_tv(P1: np.ndarray, P2: np.ndarray) -> float:
    return float(np.mean(0.5 * np.sum(np.abs(P1 - P2), axis=1)))


def frobenius(A: np.ndarray, B: np.ndarray) -> float:
    return float(np.linalg.norm(A - B, ord="fro"))


def spearman_rho(a: np.ndarray, b: np.ndarray) -> float:
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    ra = ra.astype(float)
    rb = rb.astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    denom = np.sqrt((ra**2).sum() * (rb**2).sum())
    if denom <= 0:
        return float("nan")
    return float((ra * rb).sum() / denom)


def analyze_receptor(data: dict[str, Any]) -> dict[str, Any]:
    flag: dict[str, Any] = {}
    C = count_transitions(data["hard_seqs"])
    P = row_normalize(C, flag)
    pi_hard = hard_populations(data["hard_seqs"])
    pi_soft = soft_populations(data["soft_seqs"])
    dwell = dwell_means(data["hard_seqs"])
    kg = kinetic_graph_metrics(P)
    return {
        "n_traj": data["n_traj"],
        "n_frames": data["n_frames"],
        "n_truncations": data["n_truncations"],
        "length_min": int(min(data["lengths"])),
        "length_max": int(max(data["lengths"])),
        "length_median": float(np.median(data["lengths"])),
        "n_microstate_labels_global": data["n_microstate_labels_global"],
        "pi_hard": pi_hard.tolist(),
        "pi_soft": pi_soft.tolist(),
        "pi_hard_entropy": float(entropy(pi_hard)),
        "pi_hard_entropy_norm": float(entropy(pi_hard) / np.log(K)),
        "pi_soft_entropy_norm": float(entropy(pi_soft) / np.log(K)),
        "dwell_mean_frames": dwell.tolist(),
        "C": C.tolist(),
        "P": P.tolist(),
        "add_one_smoothing_used": flag.get("add_one_smoothing_used", False),
        "kinetic_graph": kg,
    }


def pattern_tag(kg: dict[str, Any]) -> str:
    """Per-receptor soft tag (A/B/C incomplete alone — B needs cross-receptor)."""
    a_like = (
        kg["mean_row_entropy_norm"] <= ROW_ENT_A_MAX
        and kg["edge_sparsity"] <= SPARSITY_A_MAX
        and kg["mean_n_strong_out"] <= N_STRONG_A_MAX
    )
    c_like = (
        kg["mean_row_entropy_norm"] >= ROW_ENT_C_MIN
        and kg["edge_sparsity"] >= SPARSITY_C_MIN
    )
    if a_like and not c_like:
        return "A"
    if c_like and not a_like:
        return "C"
    return "NEITHER_A_NOR_C"


def assign_kinetic_pattern(
    cb1: dict[str, Any], cb2: dict[str, Any], top_overlap: float, mean_tv: float
) -> str:
    kg1 = cb1["kinetic_graph"]
    kg2 = cb2["kinetic_graph"]
    both_a = (
        kg1["mean_row_entropy_norm"] <= ROW_ENT_A_MAX
        and kg2["mean_row_entropy_norm"] <= ROW_ENT_A_MAX
        and kg1["edge_sparsity"] <= SPARSITY_A_MAX
        and kg2["edge_sparsity"] <= SPARSITY_A_MAX
        and kg1["mean_n_strong_out"] <= N_STRONG_A_MAX
        and kg2["mean_n_strong_out"] <= N_STRONG_A_MAX
    )
    both_c = (
        kg1["mean_row_entropy_norm"] >= ROW_ENT_C_MIN
        and kg2["mean_row_entropy_norm"] >= ROW_ENT_C_MIN
        and kg1["edge_sparsity"] >= SPARSITY_C_MIN
        and kg2["edge_sparsity"] >= SPARSITY_C_MIN
    )
    if both_a and not both_c:
        return "EXT_KINETIC_PATTERN_A"
    # B: not A, and pathway distinctness
    if (not both_a) and (top_overlap <= TOP_PATH_B_MAX or mean_tv >= ROW_TV_B_MIN):
        # Avoid claiming B if both clearly C
        if both_c:
            return "EXT_KINETIC_PATTERN_C"
        return "EXT_KINETIC_PATTERN_B"
    if both_c:
        return "EXT_KINETIC_PATTERN_C"
    return "EXT_KINETIC_PATTERN_INDETERMINATE"


def bootstrap_receptor_metrics(
    tables: dict[str, np.ndarray], rng: np.random.Generator
) -> dict[str, Any]:
    n = tables["C"].shape[0]
    store: dict[str, Any] = {
        "mean_row_entropy_norm": [],
        "edge_sparsity": [],
        "mean_dwell": [],
        "pi": [],
    }
    for _ in range(N_BOOT):
        idx = rng.integers(0, n, size=n)
        m = metrics_from_tables(
            tables["C"][idx],
            tables["occ"][idx],
            tables["dwell_sum"][idx],
            tables["dwell_n"][idx],
        )
        store["mean_row_entropy_norm"].append(m["kg"]["mean_row_entropy_norm"])
        store["edge_sparsity"].append(m["kg"]["edge_sparsity"])
        store["mean_dwell"].append(float(np.nanmean(m["dwell"])))
        store["pi"].append(m["pi"])
    return store


def percentile_ci(xs: list[float], lo: float = 2.5, hi: float = 97.5) -> dict[str, float]:
    arr = np.asarray(xs, dtype=np.float64)
    return {
        "mean": float(arr.mean()),
        "ci95_lo": float(np.percentile(arr, lo)),
        "ci95_hi": float(np.percentile(arr, hi)),
    }


def bootstrap_compare(
    t1: dict[str, np.ndarray],
    t2: dict[str, np.ndarray],
    rng: np.random.Generator,
) -> dict[str, Any]:
    n1 = t1["C"].shape[0]
    n2 = t2["C"].shape[0]
    m1 = metrics_from_tables(t1["C"], t1["occ"], t1["dwell_sum"], t1["dwell_n"])
    m2 = metrics_from_tables(t2["C"], t2["occ"], t2["dwell_sum"], t2["dwell_n"])
    obs_l1 = float(np.sum(np.abs(m1["pi"] - m2["pi"])))
    obs_frob = frobenius(m1["P"], m2["P"])
    obs_tv = mean_row_tv(m1["P"], m2["P"])

    pool_C = np.concatenate([t1["C"], t2["C"]], axis=0)
    pool_occ = np.concatenate([t1["occ"], t2["occ"]], axis=0)
    pool_ds = np.concatenate([t1["dwell_sum"], t2["dwell_sum"]], axis=0)
    pool_dn = np.concatenate([t1["dwell_n"], t2["dwell_n"]], axis=0)
    n_pool = pool_C.shape[0]

    null_l1 = []
    null_frob = []
    for _ in range(N_BOOT):
        perm = rng.permutation(n_pool)
        a_idx = perm[:n1]
        b_idx = perm[n1 : n1 + n2]
        ma = metrics_from_tables(pool_C[a_idx], pool_occ[a_idx], pool_ds[a_idx], pool_dn[a_idx])
        mb = metrics_from_tables(pool_C[b_idx], pool_occ[b_idx], pool_ds[b_idx], pool_dn[b_idx])
        null_l1.append(float(np.sum(np.abs(ma["pi"] - mb["pi"]))))
        null_frob.append(frobenius(ma["P"], mb["P"]))

    p_l1 = float(np.mean(np.asarray(null_l1) >= obs_l1))
    p_frob = float(np.mean(np.asarray(null_frob) >= obs_frob))
    return {
        "obs_L1_pi": obs_l1,
        "obs_frobenius_P": obs_frob,
        "obs_mean_row_TV": obs_tv,
        "null_L1_pi": percentile_ci(null_l1),
        "null_frobenius_P": percentile_ci(null_frob),
        "p_boot_L1_pi": p_l1,
        "p_boot_frobenius_P": p_frob,
        "spearman_pi_hard": spearman_rho(m1["pi"], m2["pi"]),
    }


def kinetics_verdict(cmp: dict[str, Any]) -> str:
    distinct = (cmp["p_boot_L1_pi"] <= 0.025 and cmp["p_boot_frobenius_P"] <= 0.025) or (
        cmp["p_boot_L1_pi"] <= 0.025 or cmp["p_boot_frobenius_P"] <= 0.025
    )
    # Pre-reg: Distinct if BOTH exceed 97.5th of null OR CIs exclude equality —
    # operationalized as both p_boot <= 0.025
    distinct_strict = cmp["p_boot_L1_pi"] <= 0.025 and cmp["p_boot_frobenius_P"] <= 0.025
    similar = (
        cmp["p_boot_L1_pi"] > P_BOOT_SIM_MIN
        and cmp["p_boot_frobenius_P"] > P_BOOT_SIM_MIN
        and cmp["obs_L1_pi"] < L1_SIM_MAX
        and cmp["obs_mean_row_TV"] < ROW_TV_SIM_MAX
    )
    if distinct_strict:
        return "EXT_KINETICS_CB1_CB2_DISTINCT"
    if similar:
        return "EXT_KINETICS_CB1_CB2_SIMILAR"
    # one-sided strong signal still Distinct if both metrics large vs null median
    if distinct and cmp["obs_L1_pi"] > cmp["null_L1_pi"]["ci95_hi"] and cmp[
        "obs_frobenius_P"
    ] > cmp["null_frobenius_P"]["ci95_hi"]:
        return "EXT_KINETICS_CB1_CB2_DISTINCT"
    return "EXT_KINETICS_CB1_CB2_INDETERMINATE"


def maybe_plot(cb1: dict[str, Any], cb2: dict[str, Any], out_dir: Path) -> list[str]:
    """Optional plots in a child process (parent survives Windows matplotlib fatals)."""
    import subprocess
    import tempfile

    payload = {
        "out_dir": str(out_dir),
        "stem": OUT_STEM,
        "root": str(ROOT),
        "K": K,
        "pi1": cb1["pi_hard"],
        "pi2": cb2["pi_hard"],
        "P1": cb1["P"],
        "P2": cb2["P"],
    }
    helper = r'''
import json, sys
from pathlib import Path
import numpy as np
payload = json.loads(sys.argv[1])
out_dir = Path(payload["out_dir"])
ROOT = Path(payload["root"])
stem = payload["stem"]
K = payload["K"]
paths = []
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7, 4))
x = np.arange(K)
ax.plot(x, payload["pi1"], "o-", label="CB1 hard", color="#2c6e49")
ax.plot(x, payload["pi2"], "s-", label="CB2 hard", color="#bc4749")
ax.set_xlabel("Metastable state"); ax.set_ylabel("Occupancy")
ax.set_title("Dutta Final_MSM — empirical hard populations")
ax.legend(); ax.set_xticks(x); ax.set_ylim(0, None)
p1 = out_dir / f"{stem}_populations.png"
fig.savefig(p1, dpi=120, bbox_inches="tight"); plt.close(fig)
paths.append(str(p1.relative_to(ROOT)).replace("\\", "/"))
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
for ax, lab, P in ((axes[0], "CB1 P (lag=1)", np.asarray(payload["P1"])),
                   (axes[1], "CB2 P (lag=1)", np.asarray(payload["P2"]))):
    im = ax.imshow(P, vmin=0, vmax=1, cmap="viridis")
    ax.set_title(lab); ax.set_xlabel("to"); ax.set_ylabel("from")
    fig.colorbar(im, ax=ax, fraction=0.046)
p2 = out_dir / f"{stem}_P.png"
fig.savefig(p2, dpi=120, bbox_inches="tight"); plt.close(fig)
paths.append(str(p2.relative_to(ROOT)).replace("\\", "/"))
print(json.dumps(paths))
'''
    try:
        proc = subprocess.run(
            [sys.executable, "-c", helper, json.dumps(payload)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if proc.returncode != 0:
            print(f"Plot skipped (child rc={proc.returncode}): {proc.stderr[-500:]}")
            return []
        line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else "[]"
        return json.loads(line)
    except Exception as exc:
        print(f"Plot skipped: {exc}")
        return []


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    c1 = payload["CB1"]
    c2 = payload["CB2"]
    cmp = payload["comparison"]
    lines = [
        "# EXTERNAL — Dutta & Shukla 2023 Final_MSM kinetic comparison (CB1 vs CB2)",
        "",
        f"**Generated:** {payload['generated_at']}",
        f"**Pre-registration:** `{payload['preregistration']}`",
        f"**Mode:** `EXTERNAL_COMPARISON` — does **not** reopen P2 Gate-1 / structural A/B/C.",
        "",
        "## Verdicts",
        "",
        f"- `{v['kinetics_cb1_cb2']}`",
        f"- `{v['structural_abc']}`",
        f"- `{v['kinetic_pattern']}`",
        "",
        "## Inventory",
        "",
        f"| Receptor | Trajs | Frames | T median | Microstate labels | Truncations |",
        f"|----------|------:|-------:|---------:|------------------:|------------:|",
        f"| CB1 | {c1['n_traj']} | {c1['n_frames']} | {c1['length_median']:.0f} | {c1['n_microstate_labels_global']} | {c1['n_truncations']} |",
        f"| CB2 | {c2['n_traj']} | {c2['n_frames']} | {c2['length_median']:.0f} | {c2['n_microstate_labels_global']} | {c2['n_truncations']} |",
        "",
        f"Lag = **{LAG} frame** (physical Δt **unknown** from pickles → all dwells in frames).",
        "Hard metastable label = `argmax(state_prob)`; clustering.pkl = microstates (alignment only).",
        "",
        "## Populations (hard occupancy)",
        "",
        "| State | CB1 π̂ | CB2 π̂ |",
        "|------:|-------:|-------:|",
    ]
    for k in range(K):
        lines.append(f"| {k} | {c1['pi_hard'][k]:.4f} | {c2['pi_hard'][k]:.4f} |")
    lines += [
        "",
        f"- H_norm(π̂) CB1={c1['pi_hard_entropy_norm']:.3f}, CB2={c2['pi_hard_entropy_norm']:.3f}",
        f"- Spearman ρ(π̂_CB1, π̂_CB2)={cmp['spearman_pi_hard']:.3f}",
        f"- L1 ‖π̂_CB1−π̂_CB2‖₁={cmp['obs_L1_pi']:.4f} (bootstrap p={cmp['p_boot_L1_pi']:.4f})",
        "",
        "## Kinetics (lag=1)",
        "",
        f"- Frobenius ‖P_CB1−P_CB2‖_F={cmp['obs_frobenius_P']:.4f} (bootstrap p={cmp['p_boot_frobenius_P']:.4f})",
        f"- Mean row TV={cmp['obs_mean_row_TV']:.4f}",
        f"- Top-exit path Jaccard overlap={cmp['top_path_overlap']:.3f}",
        "",
        "### Mean dwell (frames)",
        "",
        "| State | CB1 | CB2 |",
        "|------:|----:|----:|",
    ]
    for k in range(K):
        lines.append(
            f"| {k} | {c1['dwell_mean_frames'][k]:.2f} | {c2['dwell_mean_frames'][k]:.2f} |"
        )
    kg1, kg2 = c1["kinetic_graph"], c2["kinetic_graph"]
    lines += [
        "",
        "### Soft kinetic graph metrics",
        "",
        "| Metric | CB1 | CB2 |",
        "|--------|----:|----:|",
        f"| mean row_entropy_norm | {kg1['mean_row_entropy_norm']:.3f} | {kg2['mean_row_entropy_norm']:.3f} |",
        f"| edge_sparsity (τ={TAU_EDGE}) | {kg1['edge_sparsity']:.3f} | {kg2['edge_sparsity']:.3f} |",
        f"| mean n_strong_out | {kg1['mean_n_strong_out']:.2f} | {kg2['mean_n_strong_out']:.2f} |",
        "",
        "**Caveat (lag=1):** metastable hard labels are highly self-persistent at one frame "
        "(near-diagonal P; row entropy ≈0; no off-diagonal edges ≥τ). "
        "`EXT_KINETIC_PATTERN_A` therefore mainly reflects lag-1 stickiness of published metastable "
        "states, not a structural LigACN architecture. Population differences remain the primary "
        "CB1≠CB2 kinetic discriminator here.",
        "",
        "### Bootstrap CI (traj resample, B=200)",
        "",
        f"- CB1 mean_row_entropy_norm: {payload['bootstrap']['CB1']['mean_row_entropy_norm']}",
        f"- CB2 mean_row_entropy_norm: {payload['bootstrap']['CB2']['mean_row_entropy_norm']}",
        f"- CB1 edge_sparsity: {payload['bootstrap']['CB1']['edge_sparsity']}",
        f"- CB2 edge_sparsity: {payload['bootstrap']['CB2']['edge_sparsity']}",
        "",
        "## Epistemic locks",
        "",
        "- `EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES` (no coords → no LigACN/networks per state).",
        "- `P2_MSM_TRANSITIONS` remains **CLOSED (INSUFFICIENT_SAMPLING)** on our GPCRmd data.",
        "- Dutta K=6 is **not** a template for refitting our MSM.",
        "",
        "## Plots",
        "",
    ]
    for p in payload.get("plots", []):
        lines.append(f"- `{p}`")
    if not payload.get("plots"):
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()

    if not PREREG.exists():
        print(f"ERROR: pre-registration missing: {PREREG}", file=sys.stderr)
        return 2

    print("Verifying MANIFEST SHA256…")
    man_info = verify_manifest()
    print("Loading CB1 / CB2 pickles…")
    raw1 = load_receptor("CB1")
    raw2 = load_receptor("CB2")
    print(f"  CB1: {raw1['n_traj']} trajs, {raw1['n_frames']} frames")
    print(f"  CB2: {raw2['n_traj']} trajs, {raw2['n_frames']} frames")

    print("Analyzing populations / transitions…")
    a1 = analyze_receptor(raw1)
    a2 = analyze_receptor(raw2)

    print("Precomputing per-traj tables for bootstrap…")
    t1 = precompute_traj_tables(raw1["hard_seqs"])
    t2 = precompute_traj_tables(raw2["hard_seqs"])
    # free large soft/hard lists from RAM where possible after tables built
    del raw1["soft_seqs"]
    del raw2["soft_seqs"]

    rng = np.random.default_rng(SEED)
    print(f"Bootstrap B={N_BOOT}…")
    cmp = bootstrap_compare(t1, t2, rng)
    top_overlap = top_path_jaccard(
        a1["kinetic_graph"]["top_exit_edges"], a2["kinetic_graph"]["top_exit_edges"]
    )
    cmp["top_path_overlap"] = top_overlap

    b1 = bootstrap_receptor_metrics(t1, rng)
    b2 = bootstrap_receptor_metrics(t2, rng)
    boot_summary = {
        "CB1": {
            "mean_row_entropy_norm": percentile_ci(b1["mean_row_entropy_norm"]),
            "edge_sparsity": percentile_ci(b1["edge_sparsity"]),
            "mean_dwell": percentile_ci(b1["mean_dwell"]),
            "pi_ci": [
                percentile_ci([float(p[k]) for p in b1["pi"]]) for k in range(K)
            ],
        },
        "CB2": {
            "mean_row_entropy_norm": percentile_ci(b2["mean_row_entropy_norm"]),
            "edge_sparsity": percentile_ci(b2["edge_sparsity"]),
            "mean_dwell": percentile_ci(b2["mean_dwell"]),
            "pi_ci": [
                percentile_ci([float(p[k]) for p in b2["pi"]]) for k in range(K)
            ],
        },
    }

    kin_v = kinetics_verdict(cmp)
    pat_v = assign_kinetic_pattern(a1, a2, top_overlap, cmp["obs_mean_row_TV"])

    # Strip non-serializable if any
    def public_receptor(a: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in a.items() if k not in ("hard_seqs", "soft_seqs")}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    plots: list[str] = []
    if not args.no_plot:
        plots = maybe_plot(a1, a2, OUT_DIR)

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "experiment": "EXTERNAL_DUTTA_MSM_COMPARE",
        "preregistration": "docs/synthesis/EXPERIMENT_EXTERNAL_DUTTA_MSM.md",
        "doi": "10.1038/s42003-023-04868-1",
        "data_dir": "data/external/dutta_shukla_2023/msm",
        "lag_frames": LAG,
        "frame_dt": "UNKNOWN_REPORT_IN_FRAMES",
        "n_boot": N_BOOT,
        "seed": SEED,
        "manifest_ok": True,
        "manifest_checks": man_info["checks"],
        "CB1": public_receptor(a1),
        "CB2": public_receptor(a2),
        "comparison": cmp,
        "bootstrap": boot_summary,
        "per_receptor_soft_tags": {
            "CB1": pattern_tag(a1["kinetic_graph"]),
            "CB2": pattern_tag(a2["kinetic_graph"]),
        },
        "verdicts": {
            "kinetics_cb1_cb2": kin_v,
            "structural_abc": "EXT_STRUCTURAL_ABC = INDETERMINATE_NO_TRAJECTORIES",
            "kinetic_pattern": pat_v,
        },
        "epistemic_locks": {
            "P2_MSM_TRANSITIONS": "CLOSED (INSUFFICIENT_SAMPLING)",
            "P2_NETWORK_A_B_C": "ABORTED",
            "DUTTA_AS_TEMPLATE": "FORBIDDEN",
        },
        "plots": plots,
    }

    md_path = OUT_DIR / f"{OUT_STEM}.md"
    json_path = OUT_DIR / f"{OUT_STEM}.json"
    md_path.write_text(render_md(payload), encoding="utf-8")
    # JSON: convert numpy-unfriendly
    json_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print("Verdicts:", payload["verdicts"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
