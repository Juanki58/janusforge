#!/usr/bin/env python3
"""CLOSED dual validation: static LigACN hub knockout (A) × SD1 PrefCoup enrichment (B).

Governance: CLOSED_DUAL_VALIDATION | READ_ONLY_DATA
NO docking / de novo / new search / traj recovery.
Fixed hub set (a priori; do not retune):
  ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46)

Literature: Morales-Pastor et al. Nat Commun 2025, DOI 10.1038/s41467-025-60003-0
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import networkx as nx
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"networkx required: {e}") from e

try:
    from scipy.stats import fisher_exact
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"scipy required: {e}") from e

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "network_core" / "_raw_downloads"
OUT = ROOT / "results" / "network_core"
MOESM3 = RAW / "41467_2025_60003_MOESM3_ESM.xlsx"  # SD1
MOESM5 = RAW / "41467_2025_60003_MOESM5_ESM.xlsx"  # SD3 / WT_degeneracy

# Fixed a priori — do not add/remove
HUBS = [
    ("ALA:79", "ALA79", "2.49"),
    ("ALA:83", "ALA83", "2.53"),
    ("LEU:287", "LEU287", "7.41"),
    ("ASN:291", "ASN291", "7.45"),
    ("ASN:295", "ASN295", "7.49"),
    ("ARG:302", "ARG302", "8.46"),
]
HUB_LABELS = [h[0] for h in HUBS]

S_VERIFIED = ["8D0:1", "SER:285", "PHE:87"]
T_SINKS = ["ARG:131", "ASP:240", "SER:303", "SER:69"]
AUSENTE_NOT_FORCED = ["TRP:258", "PHE:183"]

N_NULL = 1000
RNG_SEED = 20260820
ALPHA = 0.05
EXPR_FLOOR = 25.0  # % WT surface expression

# SD1 category tokens (do not collapse neutral=false)
CAT_PREF = "PrefCoup_Gi"  # PrefCoup_Gαi2
CAT_COUP = "Coup_Gi_bArr"  # Coup_Gαi2_βarr1
CAT_NO = "NoCoup_Gi_bArr"  # Uncoupled / No_effect
CAT_PREF_BARR = "PrefCoup_barr"

GOVERNANCE = {
    "mode": "CLOSED_DUAL_VALIDATION",
    "MODO": "READ_ONLY_DATA",
    "DE_NOVO_GENERATION": "STOP",
    "DOCKING": "STOP",
    "NEW_DOCKING": "STOP",
    "NEW_CHEMISTRY": "STOP",
    "NEW_SEARCH": "STOP",
    "CONTRACT_v1.0": "ARCHIVED_HISTORICAL",
    "TECHNICAL_SEARCH_TRAJ": "STOP",
    "hub_list": "FIXED_A_PRIORI_NO_RETUNE",
    "literature_doi": "10.1038/s41467-025-60003-0",
}


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_wt_matrix() -> pd.DataFrame:
    df = pd.read_excel(MOESM5, sheet_name="WT_degeneracy", index_col=0)
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    return df


def build_digraph(mat: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for n in mat.index:
        G.add_node(str(n))
    arr = mat.to_numpy(dtype=float)
    for i, u in enumerate(mat.index):
        for j, v in enumerate(mat.columns):
            w = float(arr[i, j])
            if w > 0 and u != v:
                G.add_edge(str(u), str(v), weight=w, length=1.0 / w)
    return G


def io_degree(G: nx.DiGraph, n: str) -> tuple[int, int]:
    return (int(G.in_degree(n)), int(G.out_degree(n)))


def knockout(G: nx.DiGraph, nodes: list[str]) -> nx.DiGraph:
    H = G.copy()
    H.remove_nodes_from([n for n in nodes if n in H])
    return H


def st_pair_stats(G: nx.DiGraph, sources: list[str], sinks: list[str]) -> dict:
    """Metrics over Cartesian S×T pairs (hop distances)."""
    pairs = []
    n_conn = 0
    lengths = []
    for s in sources:
        for t in sinks:
            ok = s in G and t in G and nx.has_path(G, s, t)
            pairs.append((s, t, ok))
            if ok:
                n_conn += 1
                lengths.append(int(nx.shortest_path_length(G, s, t)))
    n_pairs = len(sources) * len(sinks)
    pct_disconn = 1.0 - (n_conn / n_pairs) if n_pairs else float("nan")
    # residual connectivity: fraction of T reachable from primary ligand source
    lig = sources[0] if sources else None
    n_t_reach = 0
    if lig and lig in G:
        for t in sinks:
            if t in G and nx.has_path(G, lig, t):
                n_t_reach += 1
    residual_conn = n_t_reach / len(sinks) if sinks else float("nan")
    mean_L = float(np.mean(lengths)) if lengths else float("nan")
    return {
        "n_pairs": n_pairs,
        "n_connected_pairs": n_conn,
        "pct_disconn": float(pct_disconn),
        "residual_connectivity_ligand_to_T": float(residual_conn),
        "n_T_reachable_from_ligand": n_t_reach,
        "mean_path_length_connected_ST": mean_L,
        "path_lengths_connected": lengths,
    }


def directed_global_efficiency(G: nx.DiGraph) -> float:
    n = G.number_of_nodes()
    if n < 2:
        return 0.0
    total = 0.0
    for u in G:
        lengths = nx.single_source_shortest_path_length(G, u)
        for v, d in lengths.items():
            if u != v and d > 0:
                total += 1.0 / d
    return float(total / (n * (n - 1)))


def knockout_metrics(G: nx.DiGraph, remove: list[str], sources: list[str], sinks: list[str]) -> dict:
    H = knockout(G, remove)
    st = st_pair_stats(H, sources, sinks)
    eff = directed_global_efficiency(H)
    return {
        "removed": list(remove),
        "n_nodes_remaining": H.number_of_nodes(),
        "n_edges_remaining": H.number_of_edges(),
        **st,
        "Eff_res": eff,
    }


def sample_degree_matched_sets(
    G: nx.DiGraph,
    hub_labels: list[str],
    exclude: set[str],
    n_null: int,
    rng: np.random.Generator,
) -> tuple[list[list[str]], dict]:
    """Pre-registered null: exact (in_degree, out_degree) multiset match to hubs.

    Matching rule (locked BEFORE computing p-values):
      1. Hub signature = multiset of (in_degree, out_degree) over the six hubs.
      2. Candidate pool = V \\ exclude (exclude = S ∪ T ∪ hubs).
      3. Each null set is six distinct pool nodes whose (in,out) multiset equals
         the hub signature exactly (sampled by filling each IO-bin without
         replacement from pool nodes of that exact IO pair).
      4. If a draw cannot fill all bins, reject and redraw (max attempts documented).
    """
    hub_ios = [io_degree(G, h) for h in hub_labels]
    hub_sig = Counter(hub_ios)
    pool = [n for n in G.nodes() if n not in exclude]
    by_io: dict[tuple[int, int], list[str]] = defaultdict(list)
    for n in pool:
        by_io[io_degree(G, n)].append(n)

    rule = {
        "name": "exact_in_out_degree_multiset_match",
        "hub_io_list": [{"node": h, "in": io[0], "out": io[1]} for h, io in zip(hub_labels, hub_ios)],
        "hub_io_multiset": {f"{k[0]},{k[1]}": int(v) for k, v in sorted(hub_sig.items())},
        "exclude_from_pool": sorted(exclude),
        "pool_size": len(pool),
        "pool_counts_per_hub_io": {
            f"{k[0]},{k[1]}": len(by_io[k]) for k in hub_sig
        },
        "n_null_requested": n_null,
    }

    # Feasibility
    for io, need in hub_sig.items():
        if len(by_io[io]) < need:
            raise RuntimeError(
                f"Cannot exact-match IO {io}: need {need}, pool has {len(by_io[io])}"
            )

    sets: list[list[str]] = []
    max_attempts = n_null * 200
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
            pick = rng.choice(avail, size=need, replace=False).tolist()
            chosen.extend(pick)
            used.update(pick)
        if not ok:
            continue
        # shuffle order within set for neutrality
        rng.shuffle(chosen)
        sets.append(chosen)

    rule["n_null_realized"] = len(sets)
    rule["sampling_attempts"] = attempts
    if len(sets) < n_null:
        raise RuntimeError(
            f"Only realized {len(sets)}/{n_null} exact degree-matched nulls "
            f"after {attempts} attempts"
        )
    return sets, rule


def empirical_upper_p(observed: float, null_vals: list[float]) -> float:
    """One-sided: P(null >= observed), with +1 pseudocount."""
    arr = np.asarray(null_vals, dtype=float)
    return float((1 + np.sum(arr >= observed)) / (1 + len(arr)))


def empirical_lower_p(observed: float, null_vals: list[float]) -> float:
    """One-sided: P(null <= observed), with +1 pseudocount."""
    arr = np.asarray(null_vals, dtype=float)
    return float((1 + np.sum(arr <= observed)) / (1 + len(arr)))


def map_category_label(raw: str) -> str:
    raw = str(raw)
    if raw == CAT_PREF:
        return "PrefCoup_Gαi2"
    if raw == CAT_COUP:
        return "Coup_Gαi2_βarr1"
    if raw == CAT_NO:
        return "Uncoupled_No_effect"
    if raw == CAT_PREF_BARR:
        return "PrefCoup_βarr"
    return f"OTHER:{raw}"


def load_sd1() -> pd.DataFrame:
    return pd.read_excel(MOESM3, header=1)


def _f(x):
    try:
        if pd.isna(x):
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def test_a(G: nx.DiGraph) -> dict:
    """Topology knockout vs 1000 exact degree-matched nulls."""
    # --- Pre-register significance BEFORE looking at p ---
    primary_metric = "pct_disconn"
    primary_rule = (
        "TOPOLOGICAL_BOTTLENECK_SUPPORTED iff empirical one-sided p < 0.05 for "
        "pct_disconn after hub knockout vs exact (in,out)-degree-matched null "
        "knockouts of equal size (upper-tail: larger %Disconn = stronger impact). "
        "Equivalently: observed impact in upper ≥95th percentile of nulls. "
        "Secondary metrics (residual connectivity, ΔL, Eff_res) reported but do "
        "not override the primary call unless primary is undefined."
    )

    sources = list(S_VERIFIED)
    sinks = list(T_SINKS)
    baseline = knockout_metrics(G, [], sources, sinks)
    obs = knockout_metrics(G, HUB_LABELS, sources, sinks)

    delta_L = (
        obs["mean_path_length_connected_ST"] - baseline["mean_path_length_connected_ST"]
        if (
            not math.isnan(obs["mean_path_length_connected_ST"])
            and not math.isnan(baseline["mean_path_length_connected_ST"])
        )
        else float("nan")
    )
    delta_eff = obs["Eff_res"] - baseline["Eff_res"]
    # Impact scores used for null comparison (higher = stronger bottleneck)
    obs_impact = {
        "pct_disconn": obs["pct_disconn"],
        "delta_L": delta_L if not math.isnan(delta_L) else float("inf"),
        "neg_residual_connectivity": 1.0 - obs["residual_connectivity_ligand_to_T"],
        "neg_Eff_res": -obs["Eff_res"],
    }

    exclude = set(HUB_LABELS) | set(S_VERIFIED) | set(T_SINKS)
    rng = np.random.default_rng(RNG_SEED)
    null_sets, match_rule = sample_degree_matched_sets(
        G, HUB_LABELS, exclude, N_NULL, rng
    )

    null_metrics = []
    for ns in null_sets:
        m = knockout_metrics(G, ns, sources, sinks)
        dL = (
            m["mean_path_length_connected_ST"] - baseline["mean_path_length_connected_ST"]
            if (
                not math.isnan(m["mean_path_length_connected_ST"])
                and not math.isnan(baseline["mean_path_length_connected_ST"])
            )
            else float("nan")
        )
        null_metrics.append(
            {
                "pct_disconn": m["pct_disconn"],
                "residual_connectivity_ligand_to_T": m[
                    "residual_connectivity_ligand_to_T"
                ],
                "mean_path_length_connected_ST": m["mean_path_length_connected_ST"],
                "delta_L": dL,
                "Eff_res": m["Eff_res"],
            }
        )

    null_pct = [m["pct_disconn"] for m in null_metrics]
    null_dL = [
        m["delta_L"] if not (isinstance(m["delta_L"], float) and math.isnan(m["delta_L"])) else np.nan
        for m in null_metrics
    ]
    null_eff = [m["Eff_res"] for m in null_metrics]
    null_res = [m["residual_connectivity_ligand_to_T"] for m in null_metrics]

    p_pct = empirical_upper_p(obs["pct_disconn"], null_pct)
    # ΔL: larger increase = more impact (ignore nulls with nan ΔL)
    dL_obs = delta_L
    dL_null_finite = [x for x in null_dL if not (isinstance(x, float) and math.isnan(x))]
    if math.isnan(dL_obs) or not dL_null_finite:
        p_dL = float("nan")
    else:
        p_dL = empirical_upper_p(dL_obs, dL_null_finite)
    # Eff_res: smaller residual efficiency = more impact
    p_eff = empirical_lower_p(obs["Eff_res"], null_eff)
    # residual connectivity: smaller = more impact
    p_res = empirical_lower_p(
        obs["residual_connectivity_ligand_to_T"], null_res
    )

    supported = bool(p_pct < ALPHA)
    outcome = (
        "TOPOLOGICAL_BOTTLENECK_SUPPORTED"
        if supported
        else "TOPOLOGICAL_BOTTLENECK_NOT_SUPPORTED"
    )

    return {
        "test": "A_topology",
        "primary_metric": primary_metric,
        "primary_significance_rule": primary_rule,
        "alpha": ALPHA,
        "n_null": N_NULL,
        "rng_seed": RNG_SEED,
        "degree_matching": match_rule,
        "graph": {
            "n_nodes": G.number_of_nodes(),
            "n_edges": G.number_of_edges(),
            "note_on_117_edges": (
                "PI text mentioned 117 edges; recovered WT_degeneracy DiGraph has "
                f"{G.number_of_edges()} directed weight>0 off-diagonal edges "
                "(same construction as static_ligacn_topology). Documented actual count."
            ),
        },
        "S": S_VERIFIED,
        "T": T_SINKS,
        "ausente_not_forced": AUSENTE_NOT_FORCED,
        "hubs": HUB_LABELS,
        "baseline_WT": {
            "pct_disconn": baseline["pct_disconn"],
            "residual_connectivity_ligand_to_T": baseline[
                "residual_connectivity_ligand_to_T"
            ],
            "mean_path_length_connected_ST": baseline["mean_path_length_connected_ST"],
            "Eff_res": baseline["Eff_res"],
            "n_connected_pairs": baseline["n_connected_pairs"],
        },
        "hub_knockout": {
            "pct_disconn": obs["pct_disconn"],
            "residual_connectivity_ligand_to_T": obs[
                "residual_connectivity_ligand_to_T"
            ],
            "mean_path_length_connected_ST": obs["mean_path_length_connected_ST"],
            "delta_L_vs_WT": dL_obs,
            "Eff_res": obs["Eff_res"],
            "delta_Eff_vs_WT": delta_eff,
            "n_connected_pairs": obs["n_connected_pairs"],
            "n_nodes_remaining": obs["n_nodes_remaining"],
            "n_edges_remaining": obs["n_edges_remaining"],
        },
        "null_summary": {
            "pct_disconn_mean": float(np.mean(null_pct)),
            "pct_disconn_std": float(np.std(null_pct)),
            "pct_disconn_p95": float(np.percentile(null_pct, 95)),
            "delta_L_mean": float(np.nanmean(null_dL)),
            "Eff_res_mean": float(np.mean(null_eff)),
            "Eff_res_p05": float(np.percentile(null_eff, 5)),
            "residual_connectivity_mean": float(np.mean(null_res)),
        },
        "p_values": {
            "pct_disconn_upper": p_pct,
            "delta_L_upper": p_dL,
            "Eff_res_lower": p_eff,
            "residual_connectivity_lower": p_res,
        },
        "outcome": outcome,
        "supported": supported,
        "epistemic_tag": "[INTERNAL_REANALYSIS]",
    }


def test_b(sd1: pd.DataFrame) -> dict:
    """Functional enrichment with membership vs statistical bias distinguished."""
    rows = []
    for _, r in sd1.iterrows():
        try:
            pos = int(r["position"])
        except (TypeError, ValueError):
            continue
        expr = _f(r.get("%wt expression"))
        raw_cat = str(r.get("coupling profile"))
        rows.append(
            {
                "mutant": str(r.get("mutant")),
                "position": pos,
                "pct_wt_expression": expr,
                "Gi2_Emax_raw": _f(r.get("Gi2 Emax")),
                "bArr1_Emax_raw": _f(r.get("bArr1 Emax")),
                "Gi2_Emax_norm": _f(r.get("Gi2 Emax.1")),
                "bArr1_Emax_norm": _f(r.get("bArr1 Emax.1")),
                "coupling_profile_raw": raw_cat,
                "coupling_profile_mapped": map_category_label(raw_cat),
                "simulated": str(r.get("simulated")),
            }
        )
    all_df = pd.DataFrame(rows)

    # Background after expression filter
    bg = all_df[
        all_df["pct_wt_expression"].notna()
        & (all_df["pct_wt_expression"] >= EXPR_FLOOR)
    ].copy()

    hub_positions = {int(lab.split(":")[1]): lab for lab in HUB_LABELS}

    # Per-hub: list EVERY mutation separately (no premature collapse)
    per_hub_mutations = []
    missing = []
    for lab, short, bw in HUBS:
        pos = int(lab.split(":")[1])
        muts = all_df[all_df["position"] == pos]
        if muts.empty:
            missing.append(
                {
                    "node": lab,
                    "ballesteros": bw,
                    "status": "MISSING",
                    "note": "No SD1 mutant row at this position",
                }
            )
            per_hub_mutations.append(
                {
                    "node": lab,
                    "short": short,
                    "ballesteros": bw,
                    "position": pos,
                    "mutations": [],
                    "status": "MISSING",
                }
            )
            continue
        mut_records = []
        for _, m in muts.iterrows():
            expr = m["pct_wt_expression"]
            excl = expr is None or expr < EXPR_FLOOR
            mut_records.append(
                {
                    "mutant": m["mutant"],
                    "position": pos,
                    "pct_wt_expression": expr,
                    "expression_filter_excluded": bool(excl),
                    "expression_floor_pct_WT": EXPR_FLOOR,
                    "coupling_profile_raw": m["coupling_profile_raw"],
                    "coupling_profile_mapped": m["coupling_profile_mapped"],
                    "Gi2_Emax_raw": m["Gi2_Emax_raw"],
                    "bArr1_Emax_raw": m["bArr1_Emax_raw"],
                    "Gi2_Emax_norm": m["Gi2_Emax_norm"],
                    "bArr1_Emax_norm": m["bArr1_Emax_norm"],
                    "simulated": m["simulated"],
                    # membership flags (not statistical attribution)
                    "position_membership_PrefCoup_Gai2": m["coupling_profile_raw"]
                    == CAT_PREF,
                    "position_membership_Coup_Gai2_barr1": m["coupling_profile_raw"]
                    == CAT_COUP,
                    "position_membership_Uncoupled_No_effect": m["coupling_profile_raw"]
                    == CAT_NO,
                }
            )
        per_hub_mutations.append(
            {
                "node": lab,
                "short": short,
                "ballesteros": bw,
                "position": pos,
                "n_mutations_in_SD1": len(mut_records),
                "mutations": mut_records,
                "status": "PRESENT",
                "note": (
                    "Multiple mutations listed separately; categories not collapsed."
                    if len(mut_records) > 1
                    else "Single SD1 mutant at this position."
                ),
            }
        )

    # Hub mutants entering enrichment (expression-filtered)
    hub_pos_set = set(hub_positions.keys())
    hub_bg = bg[bg["position"].isin(hub_pos_set)]
    nonhub_bg = bg[~bg["position"].isin(hub_pos_set)]

    a = int((hub_bg["coupling_profile_raw"] == CAT_PREF).sum())
    b = int((hub_bg["coupling_profile_raw"] != CAT_PREF).sum())
    c = int((nonhub_bg["coupling_profile_raw"] == CAT_PREF).sum())
    d = int((nonhub_bg["coupling_profile_raw"] != CAT_PREF).sum())

    table = [[a, b], [c, d]]
    odds, p_fisher = fisher_exact(table, alternative="greater")

    # Category tallies (expression-filtered hub mutants) — keep all classes
    hub_cat_counts = hub_bg["coupling_profile_raw"].value_counts().to_dict()
    bg_cat_counts = bg["coupling_profile_raw"].value_counts().to_dict()

    # Position membership summary (any SD1 row, before expr filter for transparency)
    membership = {
        "PrefCoup_Gαi2_positions": [],
        "Coup_Gαi2_βarr1_positions": [],
        "Uncoupled_No_effect_positions": [],
        "PrefCoup_βarr_positions": [],
        "excluded_low_expression": [],
        "missing": [m["node"] for m in missing],
    }
    for rec in per_hub_mutations:
        for m in rec["mutations"]:
            if m["expression_filter_excluded"]:
                membership["excluded_low_expression"].append(
                    {
                        "node": rec["node"],
                        "mutant": m["mutant"],
                        "pct_wt_expression": m["pct_wt_expression"],
                        "coupling_profile_mapped": m["coupling_profile_mapped"],
                    }
                )
                continue
            mapped = m["coupling_profile_mapped"]
            if mapped == "PrefCoup_Gαi2":
                membership["PrefCoup_Gαi2_positions"].append(
                    {"node": rec["node"], "mutant": m["mutant"]}
                )
            elif mapped == "Coup_Gαi2_βarr1":
                membership["Coup_Gαi2_βarr1_positions"].append(
                    {"node": rec["node"], "mutant": m["mutant"]}
                )
            elif mapped == "Uncoupled_No_effect":
                membership["Uncoupled_No_effect_positions"].append(
                    {"node": rec["node"], "mutant": m["mutant"]}
                )
            elif mapped == "PrefCoup_βarr":
                membership["PrefCoup_βarr_positions"].append(
                    {"node": rec["node"], "mutant": m["mutant"]}
                )

    # Decisive missing? If zero hub mutants pass filter → INDETERMINATE pressure
    n_hub_in_test = len(hub_bg)
    indeterminate_pressure = n_hub_in_test == 0 or len(missing) == len(HUBS)

    supported = bool(p_fisher < ALPHA) and not indeterminate_pressure
    if indeterminate_pressure:
        outcome = "FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED"
        # Caller may elevate combined to INDETERMINATE
        functional_data_status = "INSUFFICIENT_HUB_MUTANTS_AFTER_FILTER"
    else:
        outcome = (
            "FUNCTIONAL_ENRICHMENT_SUPPORTED"
            if supported
            else "FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED"
        )
        functional_data_status = "OK"

    # Verify paper-like PrefCoup/Coup counts on full unfiltered table
    full_pref = int((all_df["coupling_profile_raw"] == CAT_PREF).sum())
    full_coup = int((all_df["coupling_profile_raw"] == CAT_COUP).sum())
    filt_pref = int((bg["coupling_profile_raw"] == CAT_PREF).sum())
    filt_coup = int((bg["coupling_profile_raw"] == CAT_COUP).sum())

    return {
        "test": "B_function",
        "expression_floor_pct_WT": EXPR_FLOOR,
        "category_policy": (
            "Respect SD1 experimental categories exactly; do not collapse "
            "neutral/NoCoup into false. PrefCoup_barr kept distinct from PrefCoup_Gi."
        ),
        "safeguard": {
            "distinction": (
                "position_membership = which hubs appear in PrefCoup/Coup/Uncoupled "
                "lists; statistical_attribution = Fisher enrichment of PrefCoup_Gi "
                "among expression-filtered hub-position mutants vs non-hub background."
            ),
            "multiple_mutations_policy": (
                "Each mutation/category reported separately under per_hub_mutations; "
                "no premature single-label collapse."
            ),
        },
        "background_counts": {
            "n_SD1_rows_parsed": int(len(all_df)),
            "n_after_expression_filter": int(len(bg)),
            "category_counts_filtered": {str(k): int(v) for k, v in bg_cat_counts.items()},
            "PrefCoup_Gi_filtered": filt_pref,
            "Coup_Gi_bArr_filtered": filt_coup,
            "PrefCoup_Gi_unfiltered": full_pref,
            "Coup_Gi_bArr_unfiltered": full_coup,
            "note_14_of_20": (
                "Prior narrative 14 PrefCoup / 20 Coup does not match full SD1 "
                f"({full_pref} PrefCoup_Gi / {full_coup} Coup_Gi_bArr unfiltered; "
                f"{filt_pref}/{filt_coup} after ≥{EXPR_FLOOR}% WT expression). "
                "Enrichment uses expression-filtered full mutagenic background."
            ),
        },
        "per_hub_mutations": per_hub_mutations,
        "position_membership": membership,
        "statistical_attribution": {
            "test": "Fisher exact (one-sided greater) PrefCoup_Gi enrichment",
            "contingency_table": {
                "rows": ["hub_positions", "nonhub_positions"],
                "cols": ["PrefCoup_Gi", "not_PrefCoup_Gi"],
                "table": table,
            },
            "n_hub_mutants_in_test": n_hub_in_test,
            "hub_category_counts_filtered": {
                str(k): int(v) for k, v in hub_cat_counts.items()
            },
            "odds_ratio": float(odds),
            "p_value": float(p_fisher),
            "alpha": ALPHA,
            "interpretation_limit": (
                "Significant enrichment attributes PrefCoup bias to the *set* vs "
                "background; it does not prove each hub position is causally PrefCoup."
            ),
        },
        "missing": missing,
        "functional_data_status": functional_data_status,
        "outcome": outcome,
        "supported": supported,
        "epistemic_tag": "[INTERNAL_REANALYSIS] + [LITERATURA_PRIMARIA] categories from Morales-Pastor SD1",
    }


def verdict_tree(a: dict, b: dict) -> dict:
    a_ok = bool(a.get("supported"))
    b_ok = bool(b.get("supported"))
    b_indeterminate = b.get("functional_data_status") == "INSUFFICIENT_HUB_MUTANTS_AFTER_FILTER"

    if b_indeterminate and not a_ok:
        combined = "INDETERMINATE"
        interpretation = "INDETERMINATE → insufficient or incompatible data"
    elif a_ok and b_ok:
        combined = "CORE_CANDIDATE_SUPPORTED"
        interpretation = (
            "CORE_CANDIDATE_SUPPORTED → name entity CB2_Gi_NETWORK_CANDIDATE, not “switch”"
        )
    elif a_ok and not b_ok:
        combined = "CORE_TOPOLOGICAL_ONLY"
        interpretation = (
            "CORE_TOPOLOGICAL_ONLY → network architecture without sufficient functional evidence"
        )
    elif (not a_ok) and b_ok:
        combined = "CORE_FUNCTIONAL_ONLY"
        interpretation = (
            "CORE_FUNCTIONAL_ONLY → functional signal that static LigACN does not capture"
        )
    else:
        combined = "NETWORK_DISTRIBUTED"
        interpretation = "NETWORK_DISTRIBUTED → no support for a joint bottleneck"

    formal_name = (
        "CB2_Gi_NETWORK_CANDIDATE" if combined == "CORE_CANDIDATE_SUPPORTED" else None
    )
    forbidden = ["switch", "núcleo universal probado", "CORE_FOUND"]

    # Test C: convergence only meaningful when both supported
    if a_ok and b_ok:
        pref_nodes = [
            x["node"] for x in b["position_membership"]["PrefCoup_Gαi2_positions"]
        ]
        c = {
            "executed": True,
            "question": (
                "Do the same residues appear simultaneously as topological hubs "
                "AND PrefCoup_Gαi2 membership (expression-filtered)?"
            ),
            "hubs_fixed": HUB_LABELS,
            "PrefCoup_membership_subset": pref_nodes,
            "overlap_yes": len(pref_nodes) > 0,
            "overlap_residues": pref_nodes,
            "note": (
                "Convergence here is set-level A∧B plus PrefCoup membership list; "
                "not a claim of universal Gi core."
            ),
        }
    else:
        c = {
            "executed": False,
            "reason": "Skipped: requires A and B both SUPPORTED",
            "A_supported": a_ok,
            "B_supported": b_ok,
        }

    return {
        "combined_verdict": combined,
        "interpretation_exact": interpretation,
        "formal_name_if_supported": formal_name,
        "forbidden_language": forbidden,
        "A_outcome": a["outcome"],
        "B_outcome": b["outcome"],
        "A_p_primary_pct_disconn": a["p_values"]["pct_disconn_upper"],
        "B_p_fisher_PrefCoup": b["statistical_attribution"]["p_value"],
        "test_C_convergence": c,
        "epistemic_tag": "[INTERNAL_REANALYSIS]",
        "limit": (
            "Topology ≠ causal Gi necessity unless B supports; even CORE_CANDIDATE_"
            "SUPPORTED is a network candidate pending human review — not a switch."
        ),
    }


def write_markdown(report: dict, path: Path) -> None:
    a = report["test_A"]
    b = report["test_B"]
    v = report["verdict"]
    lines = []
    lines.append("# Dual validation — static hubs × functional enrichment")
    lines.append("")
    lines.append(f"**Run UTC:** `{report['run_utc']}`")
    lines.append(f"**Branch:** `{report.get('branch', 'feat/cb2-hubs-functional-topology-test')}`")
    lines.append(f"**Mode:** `{report['governance']['mode']}` / READ_ONLY_DATA")
    lines.append(
        "**Literature (PRIMARY):** Morales-Pastor et al., *Nat Commun* (2025), "
        "DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)"
    )
    lines.append("")
    lines.append("## Governance locks")
    lines.append("")
    lines.append("```yaml")
    for k, val in report["governance"].items():
        lines.append(f"{k}: {val}")
    lines.append("```")
    lines.append("")
    lines.append("## Fixed hub set (a priori)")
    lines.append("")
    lines.append("| LigACN | Short | Ballesteros |")
    lines.append("|--------|-------|-------------|")
    for lab, short, bw in HUBS:
        lines.append(f"| `{lab}` | {short} | {bw} |")
    lines.append("")
    lines.append(f"**S (verified only):** {S_VERIFIED}")
    lines.append(f"**T:** {T_SINKS}")
    lines.append(f"**Not forced:** {AUSENTE_NOT_FORCED}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Test A — Topology")
    lines.append("")
    lines.append(f"**Tag:** {a['epistemic_tag']}")
    lines.append("")
    lines.append(f"- Graph: {a['graph']['n_nodes']} nodes × **{a['graph']['n_edges']}** directed edges (WT_degeneracy).")
    lines.append(f"- {a['graph']['note_on_117_edges']}")
    lines.append(f"- Nulls: **{a['n_null']}** exact (in,out)-degree-matched knockouts.")
    lines.append(f"- Matching rule: `{a['degree_matching']['name']}`")
    lines.append(f"- Hub IO multiset: `{a['degree_matching']['hub_io_multiset']}`")
    lines.append(f"- **Primary metric:** `{a['primary_metric']}`")
    lines.append(f"- Rule: {a['primary_significance_rule']}")
    lines.append("")
    lines.append("| Metric | WT | Hub KO | Null mean | p |")
    lines.append("|--------|----|--------|-----------|---|")
    lines.append(
        f"| %Disconn (S×T) | {a['baseline_WT']['pct_disconn']:.4f} | "
        f"{a['hub_knockout']['pct_disconn']:.4f} | "
        f"{a['null_summary']['pct_disconn_mean']:.4f} | "
        f"**{a['p_values']['pct_disconn_upper']:.4g}** |"
    )
    lines.append(
        f"| Residual connectivity (ligand→T) | "
        f"{a['baseline_WT']['residual_connectivity_ligand_to_T']:.4f} | "
        f"{a['hub_knockout']['residual_connectivity_ligand_to_T']:.4f} | "
        f"{a['null_summary']['residual_connectivity_mean']:.4f} | "
        f"{a['p_values']['residual_connectivity_lower']:.4g} |"
    )
    dL = a["hub_knockout"]["delta_L_vs_WT"]
    dL_s = "nan" if (isinstance(dL, float) and math.isnan(dL)) else f"{dL:.4f}"
    p_dL = a["p_values"]["delta_L_upper"]
    p_dL_s = "nan" if (isinstance(p_dL, float) and math.isnan(p_dL)) else f"{p_dL:.4g}"
    lines.append(
        f"| ΔL mean path length S→T | 0 (ref) | {dL_s} | "
        f"{a['null_summary']['delta_L_mean']:.4f} | {p_dL_s} |"
    )
    lines.append(
        f"| Eff_res (directed global efficiency) | "
        f"{a['baseline_WT']['Eff_res']:.6f} | "
        f"{a['hub_knockout']['Eff_res']:.6f} | "
        f"{a['null_summary']['Eff_res_mean']:.6f} | "
        f"{a['p_values']['Eff_res_lower']:.4g} |"
    )
    lines.append("")
    lines.append(f"**Outcome A:** `{a['outcome']}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Test B — Function")
    lines.append("")
    lines.append(f"**Tag:** {b['epistemic_tag']}")
    lines.append("")
    lines.append("### Safeguard: membership ≠ statistical attribution")
    lines.append("")
    lines.append(f"1. **Position membership:** {b['safeguard']['distinction'].split(';')[0].strip()}")
    lines.append(
        "2. **Statistically attributable bias:** Fisher one-sided PrefCoup_Gi enrichment "
        "of the hub-position mutant *set* vs non-hub background (expression-filtered)."
    )
    lines.append(f"3. Multiple mutations: {b['safeguard']['multiple_mutations_policy']}")
    lines.append("")
    lines.append(f"Expression filter: exclude surface expression **<{EXPR_FLOOR}% WT**.")
    lines.append("")
    lines.append("### Per-hub mutations (not collapsed)")
    lines.append("")
    for rec in b["per_hub_mutations"]:
        lines.append(
            f"#### `{rec['node']}` ({rec['short']}, {rec['ballesteros']}) — {rec['status']}"
        )
        if not rec["mutations"]:
            lines.append("- MISSING in SD1")
            continue
        for m in rec["mutations"]:
            excl = "EXCLUDED_LOW_EXPR" if m["expression_filter_excluded"] else "IN_TEST"
            lines.append(
                f"- **{m['mutant']}** [{excl}]: raw=`{m['coupling_profile_raw']}` → "
                f"mapped=`{m['coupling_profile_mapped']}`; "
                f"%wt_expr={m['pct_wt_expression']}; "
                f"Gi2_Emax_raw={m['Gi2_Emax_raw']}; bArr1_Emax_raw={m['bArr1_Emax_raw']}"
            )
        lines.append("")
    lines.append("### Position membership (expression-filtered)")
    lines.append("")
    pm = b["position_membership"]
    lines.append(f"- PrefCoup_Gαi2: {pm['PrefCoup_Gαi2_positions']}")
    lines.append(f"- Coup_Gαi2_βarr1: {pm['Coup_Gαi2_βarr1_positions']}")
    lines.append(f"- Uncoupled/No_effect: {pm['Uncoupled_No_effect_positions']}")
    lines.append(f"- Excluded low expression: {pm['excluded_low_expression']}")
    lines.append("")
    sa = b["statistical_attribution"]
    lines.append("### Statistical attribution (Fisher)")
    lines.append("")
    lines.append(f"- Contingency: `{sa['contingency_table']['table']}`")
    lines.append(f"- Odds ratio: **{sa['odds_ratio']:.4g}**")
    lines.append(f"- p (greater): **{sa['p_value']:.4g}**")
    lines.append(f"- Hub mutants in test: {sa['n_hub_mutants_in_test']}")
    lines.append(f"- Hub category counts: `{sa['hub_category_counts_filtered']}`")
    lines.append(f"- Background note: {b['background_counts']['note_14_of_20']}")
    lines.append("")
    lines.append(f"**Outcome B:** `{b['outcome']}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Test C — Convergence")
    lines.append("")
    c = v["test_C_convergence"]
    if c.get("executed"):
        lines.append(f"- Overlap yes: **{c['overlap_yes']}**")
        lines.append(f"- Residues: `{c['overlap_residues']}`")
    else:
        lines.append(f"- Skipped: {c.get('reason')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Combined verdict")
    lines.append("")
    lines.append(f"**`{v['combined_verdict']}`**")
    lines.append("")
    lines.append(f"Interpretation (exact): {v['interpretation_exact']}")
    if v.get("formal_name_if_supported"):
        lines.append(f"**Formal name:** `{v['formal_name_if_supported']}`")
    lines.append("")
    lines.append(f"Limit: {v['limit']}")
    lines.append("")
    lines.append("Forbidden language in this deliverable: switch / núcleo universal probado / CORE_FOUND.")
    lines.append("")
    lines.append("**TOTAL STOP** — joint human review. No next phase.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not MOESM5.exists() or not MOESM3.exists():
        print("Missing MOESM3/MOESM5 under results/network_core/_raw_downloads", file=sys.stderr)
        return 1

    mat = load_wt_matrix()
    G = build_digraph(mat)
    sd1 = load_sd1()

    print(f"[A] graph nodes={G.number_of_nodes()} edges={G.number_of_edges()}")
    print("[A] running hub knockout + 1000 degree-matched nulls …")
    a = test_a(G)
    print(f"[A] outcome={a['outcome']} p_pct={a['p_values']['pct_disconn_upper']:.4g}")

    print("[B] SD1 PrefCoup enrichment …")
    b = test_b(sd1)
    print(
        f"[B] outcome={b['outcome']} p_fisher={b['statistical_attribution']['p_value']:.4g}"
    )

    v = verdict_tree(a, b)
    print(f"[V] {v['combined_verdict']}")

    report = {
        "run_utc": run_utc,
        "branch": "feat/cb2-hubs-functional-topology-test",
        "governance": GOVERNANCE,
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "networkx": nx.__version__,
            "numpy": np.__version__,
        },
        "inputs": {
            "moesm5": str(MOESM5.relative_to(ROOT)).replace("\\", "/"),
            "moesm5_sha256": sha256(MOESM5),
            "moesm3": str(MOESM3.relative_to(ROOT)).replace("\\", "/"),
            "moesm3_sha256": sha256(MOESM3),
            "sheet": "WT_degeneracy",
            "doi": "10.1038/s41467-025-60003-0",
        },
        "hubs_fixed": [
            {"ligacn": lab, "short": short, "ballesteros": bw}
            for lab, short, bw in HUBS
        ],
        "test_A": a,
        "test_B": b,
        "verdict": v,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "hubs_dual_validation_report.json"
    md_path = OUT / "hubs_dual_validation_report.md"
    json_path.write_text(json.dumps(report, indent=2, allow_nan=True), encoding="utf-8")
    write_markdown(report, md_path)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
