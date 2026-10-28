#!/usr/bin/env python3
"""X1 — Mean contact persistence vs temporal variance vs LigACN / hub neighborhood.

Pre-registration: docs/synthesis/EXPERIMENT_X1_MEAN_VS_VARIANCE.md
Contact definition: exact P1 CONTACT_DEF (no post-hoc cutoff).

CLI::

    micromamba run -n janus_p1 python scripts/network_core/x1_mean_vs_variance_contacts.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from dynamic_pipeline import HUB_LABELS, S_SET, T_SET  # noqa: E402
from p1_dynamic_hub_validation import (  # noqa: E402
    CONTACT_DEF,
    PSF,
    TRAJ_DIR,
    XTC_FILES,
    accumulate_contacts,
    build_atom_tables,
    load_universe,
    sha256_file,
)

try:
    import networkx as nx
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"networkx required: {e}") from e

try:
    import pandas as pd
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"pandas required: {e}") from e

PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_X1_MEAN_VS_VARIANCE.md"
OUT_DIR = ROOT / "results" / "network_core"
MOESM5 = OUT_DIR / "_raw_downloads" / "41467_2025_60003_MOESM5_ESM.xlsx"

# Locked a priori (EXPERIMENT_X1_MEAN_VS_VARIANCE.md)
K = 200
N_NULL = 1000
ALPHA = 0.05
RNG_SEED = 20260821
P_POOL_MIN = float(CONTACT_DEF["p_ij_edge_threshold"])  # 0.1
K_EFF_MIN = 50


def edge_key(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def load_ligacn_refs() -> dict[str, Any]:
    df = pd.read_excel(MOESM5, sheet_name="WT_degeneracy", index_col=0)
    df.index = df.index.astype(str)
    df.columns = df.columns.astype(str)
    G = nx.DiGraph()
    arr = df.to_numpy(dtype=float)
    for i, u in enumerate(df.index):
        for j, v in enumerate(df.columns):
            w = float(arr[i, j])
            if w > 0 and u != v:
                G.add_edge(str(u), str(v), weight=w)

    ref_ligacn: set[tuple[str, str]] = set()
    for u, v in G.edges():
        ref_ligacn.add(edge_key(str(u), str(v)))

    hubs = set(HUB_LABELS)
    neighbors: set[str] = set()
    for h in hubs:
        if h not in G:
            continue
        neighbors.update(str(x) for x in G.predecessors(h))
        neighbors.update(str(x) for x in G.successors(h))
    closed = hubs | neighbors

    ref_hub: set[tuple[str, str]] = set()
    for u, v in ref_ligacn:
        if u in closed or v in closed:
            ref_hub.add((u, v))

    return {
        "n_directed_edges": int(G.number_of_edges()),
        "n_nodes": int(G.number_of_nodes()),
        "ref_ligacn": ref_ligacn,
        "ref_hub_nbhd": ref_hub,
        "hub_closed_neighborhood_nodes": sorted(closed),
        "n_hub_nodes_present": sum(1 for h in hubs if h in G),
    }


def compute_pooled_occupancy() -> dict[str, Any]:
    """Accumulate contact counts across all replicas → mean and Bernoulli variance."""
    labels: list[str] | None = None
    counts_sum: np.ndarray | None = None
    n_frames = 0
    per_rep: list[dict[str, Any]] = []

    for xtc in XTC_FILES:
        u = load_universe(xtc)
        tables = build_atom_tables(u)
        if labels is None:
            labels = tables["unique_labels"]
            counts_sum = np.zeros((len(labels), len(labels)), dtype=np.int64)
        elif tables["unique_labels"] != labels:
            # Align by label intersection map if residue naming drifts (should not)
            raise RuntimeError(f"label set mismatch in {xtc.name}")
        counts, n_used = accumulate_contacts(u, tables)
        assert counts_sum is not None
        counts_sum += counts.astype(np.int64)
        n_frames += int(n_used)
        per_rep.append({"xtc": xtc.name, "n_frames": int(n_used)})

    assert labels is not None and counts_sum is not None and n_frames > 0
    # counts_sum is symmetric; use upper triangle
    mean = counts_sum.astype(np.float64) / float(n_frames)
    # Because we double-count both [i,j] and [j,i] identically, mean[i,j] is correct
    return {
        "labels": labels,
        "n_frames": n_frames,
        "mean_mat": mean,
        "per_replica": per_rep,
    }


def build_edge_table(labels: list[str], mean_mat: np.ndarray) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            m = float(mean_mat[i, j])
            if m < P_POOL_MIN:
                continue
            var = m * (1.0 - m)
            cv = float(np.sqrt(var) / m) if m > 0 else float("nan")
            a, b = edge_key(labels[i], labels[j])
            edges.append(
                {
                    "u": a,
                    "v": b,
                    "mean": m,
                    "var": var,
                    "cv": cv,
                }
            )
    return edges


def top_k(edges: list[dict[str, Any]], key: str, k: int) -> list[dict[str, Any]]:
    ranked = sorted(edges, key=lambda e: (-float(e[key]), e["u"], e["v"]))
    return ranked[:k]


def overlap_count(top: list[dict[str, Any]], ref: set[tuple[str, str]]) -> int:
    s = {edge_key(e["u"], e["v"]) for e in top}
    return int(len(s & ref))


def jaccard(top: list[dict[str, Any]], ref: set[tuple[str, str]]) -> float:
    s = {edge_key(e["u"], e["v"]) for e in top}
    if not s and not ref:
        return float("nan")
    return float(len(s & ref) / len(s | ref))


def empirical_upper_p(observed: int, null: np.ndarray) -> float:
    return float((1 + int(np.sum(null >= observed))) / (1 + null.size))


def assign_verdict(
    mean_beats: bool,
    var_beats: bool,
    overlap_mean: int,
    overlap_var: int,
    var_more_than_mean: bool,
    indeterminate: str | None,
) -> str:
    if indeterminate:
        return "X1_INDETERMINATE"
    if var_beats and var_more_than_mean:
        return "X1_VARIANCE_ALIGNS_STATIC"
    if mean_beats and not (var_beats and var_more_than_mean):
        # MEAN aligns; VAR does not uniquely win
        if not var_beats or overlap_mean >= overlap_var:
            return "X1_MEAN_ALIGNS_STATIC"
        # both beat null but paired rule says VAR does not dominate → NEITHER unique
        return "X1_NEITHER"
    if not mean_beats and not var_beats:
        return "X1_NEITHER"
    # only VAR beats null but var_more_than_mean false (e.g. overlap_var <= overlap_mean)
    if var_beats and not mean_beats:
        # Still VARIANCE if overlap_var > overlap_mean; else NEITHER
        if overlap_var > overlap_mean:
            return "X1_VARIANCE_ALIGNS_STATIC"
        return "X1_NEITHER"
    return "X1_NEITHER"


def run() -> dict[str, Any]:
    indeterminate: str | None = None
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not PSF.is_file():
        indeterminate = f"missing PSF: {PSF}"
    for xtc in XTC_FILES:
        if not xtc.is_file():
            indeterminate = f"missing XTC: {xtc}"
    if not MOESM5.is_file():
        indeterminate = f"missing LigACN matrix: {MOESM5}"

    traj_sha = {}
    for p in [PSF, *XTC_FILES]:
        if p.is_file():
            traj_sha[p.name] = sha256_file(p)

    refs: dict[str, Any] = {}
    edges: list[dict[str, Any]] = []
    top_mean: list[dict[str, Any]] = []
    top_var: list[dict[str, Any]] = []
    k_eff = K
    n_frames = 0
    per_rep: list[dict[str, Any]] = []

    stats: dict[str, Any] = {}

    if indeterminate is None:
        try:
            refs = load_ligacn_refs()
            if not refs["ref_hub_nbhd"]:
                indeterminate = "empty REF_HUB_NBHD"
            else:
                occ = compute_pooled_occupancy()
                n_frames = int(occ["n_frames"])
                per_rep = occ["per_replica"]
                edges = build_edge_table(occ["labels"], occ["mean_mat"])
                k_eff = min(K, len(edges))
                if k_eff < K_EFF_MIN:
                    indeterminate = f"k_eff={k_eff} < {K_EFF_MIN}"
                else:
                    top_mean = top_k(edges, "mean", k_eff)
                    top_var = top_k(edges, "var", k_eff)

                    pool = [edge_key(e["u"], e["v"]) for e in edges]
                    ref_hub: set[tuple[str, str]] = refs["ref_hub_nbhd"]
                    ref_lig: set[tuple[str, str]] = refs["ref_ligacn"]
                    rng = np.random.default_rng(RNG_SEED)

                    # Shared null subsets for paired difference
                    n_pool = len(pool)
                    idx = np.arange(n_pool)
                    null_idx = np.empty((N_NULL, k_eff), dtype=np.int32)
                    for t in range(N_NULL):
                        null_idx[t] = rng.choice(idx, size=k_eff, replace=False)

                    def overlaps_from_idx(rows: np.ndarray, ref: set[tuple[str, str]]) -> np.ndarray:
                        out = np.empty(rows.shape[0], dtype=np.int32)
                        for t in range(rows.shape[0]):
                            ov = 0
                            for i in rows[t]:
                                if pool[int(i)] in ref:
                                    ov += 1
                            out[t] = ov
                        return out

                    null_hub = overlaps_from_idx(null_idx, ref_hub)
                    null_lig = overlaps_from_idx(null_idx, ref_lig)

                    ov_mean_hub = overlap_count(top_mean, ref_hub)
                    ov_var_hub = overlap_count(top_var, ref_hub)
                    ov_mean_lig = overlap_count(top_mean, ref_lig)
                    ov_var_lig = overlap_count(top_var, ref_lig)

                    p_mean_hub = empirical_upper_p(ov_mean_hub, null_hub)
                    p_var_hub = empirical_upper_p(ov_var_hub, null_hub)
                    p_mean_lig = empirical_upper_p(ov_mean_lig, null_lig)
                    p_var_lig = empirical_upper_p(ov_var_lig, null_lig)

                    mean_beats = p_mean_hub <= ALPHA
                    var_beats = p_var_hub <= ALPHA

                    # Paired difference: for shared nulls, null_VAR - null_MEAN is 0
                    # (same random subsets). Channel comparison uses observed overlaps
                    # plus: VAR more than MEAN if overlap_var > overlap_mean AND
                    # (VAR beats & MEAN does not) OR (both beat & diff > 95th pct of
                    # null differences). With shared subsets null diff is identically 0,
                    # so 95th pct is 0 → require overlap_var - overlap_mean > 0 when both beat.
                    diff_obs = ov_var_hub - ov_mean_hub
                    null_diff_p95 = 0  # shared subset null → diff always 0
                    if var_beats and not mean_beats and ov_var_hub > ov_mean_hub:
                        var_more = True
                    elif (
                        var_beats
                        and mean_beats
                        and diff_obs > null_diff_p95
                    ):
                        var_more = True
                    else:
                        var_more = False

                    verdict = assign_verdict(
                        mean_beats,
                        var_beats,
                        ov_mean_hub,
                        ov_var_hub,
                        var_more,
                        None,
                    )

                    stats = {
                        "k": K,
                        "k_eff": k_eff,
                        "n_eligible_edges": len(edges),
                        "n_frames_pooled": n_frames,
                        "ref_hub_nbhd_size": len(ref_hub),
                        "ref_ligacn_size": len(ref_lig),
                        "overlap_mean_hub": ov_mean_hub,
                        "overlap_var_hub": ov_var_hub,
                        "overlap_mean_ligacn": ov_mean_lig,
                        "overlap_var_ligacn": ov_var_lig,
                        "jaccard_mean_hub": jaccard(top_mean, ref_hub),
                        "jaccard_var_hub": jaccard(top_var, ref_hub),
                        "jaccard_mean_ligacn": jaccard(top_mean, ref_lig),
                        "jaccard_var_ligacn": jaccard(top_var, ref_lig),
                        "p_mean_hub": p_mean_hub,
                        "p_var_hub": p_var_hub,
                        "p_mean_ligacn": p_mean_lig,
                        "p_var_ligacn": p_var_lig,
                        "mean_beats_null_hub": mean_beats,
                        "var_beats_null_hub": var_beats,
                        "var_more_than_mean": var_more,
                        "diff_var_minus_mean_hub": diff_obs,
                        "null_hub_mean": float(np.mean(null_hub)),
                        "null_hub_p95": float(np.percentile(null_hub, 95)),
                        "alpha": ALPHA,
                        "n_null": N_NULL,
                        "rng_seed": RNG_SEED,
                    }
        except Exception as exc:  # noqa: BLE001
            indeterminate = f"{type(exc).__name__}: {exc}"
            verdict = "X1_INDETERMINATE"
    else:
        verdict = "X1_INDETERMINATE"

    if indeterminate:
        verdict = "X1_INDETERMINATE"

    # Serialize refs sizes only in main payload; full rank lists separately
    def edge_public(e: dict[str, Any]) -> dict[str, Any]:
        return {
            "u": e["u"],
            "v": e["v"],
            "mean": e["mean"],
            "var": e["var"],
            "cv": e["cv"],
        }

    rank_payload = {
        "top_mean": [edge_public(e) for e in top_mean],
        "top_var": [edge_public(e) for e in top_var],
        "stats": stats,
    }
    rank_path = OUT_DIR / "x1_rank_lists.json"
    rank_path.write_text(json.dumps(rank_payload, indent=2), encoding="utf-8")

    payload: dict[str, Any] = {
        "experiment": "X1_MEAN_VS_VARIANCE",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "preregistration": str(PREREG.relative_to(ROOT)),
        "contact_def": CONTACT_DEF,
        "traj_dir": str(TRAJ_DIR.relative_to(ROOT)),
        "traj_sha256": traj_sha,
        "hubs": HUB_LABELS,
        "S_set": S_SET,
        "T_set": T_SET,
        "ligacn": {
            "moesm5": str(MOESM5.relative_to(ROOT)),
            "n_directed_edges": refs.get("n_directed_edges"),
            "n_nodes": refs.get("n_nodes"),
            "n_hub_nodes_present": refs.get("n_hub_nodes_present"),
            "ref_ligacn_size": len(refs["ref_ligacn"]) if refs else None,
            "ref_hub_nbhd_size": len(refs["ref_hub_nbhd"]) if refs else None,
            "hub_closed_neighborhood_n_nodes": (
                len(refs["hub_closed_neighborhood_nodes"]) if refs else None
            ),
        },
        "per_replica": per_rep,
        "n_frames_pooled": n_frames,
        "metrics": stats,
        "x1_verdict": verdict,
        "indeterminate_reason": indeterminate,
        "governance": {
            "reuses_p1_contact_def": True,
            "no_new_cutoff": True,
            "no_new_hub_hunt": True,
            "no_gi_mechanism_claim": True,
            "no_cholesterol_rescue_of_p1": True,
        },
        "artifacts": {
            "report_json": "results/network_core/x1_mean_vs_variance_report.json",
            "report_md": "results/network_core/x1_mean_vs_variance_report.md",
            "rank_lists": "results/network_core/x1_rank_lists.json",
        },
    }

    lines = [
        "# X1 — Mean contact vs temporal variance",
        "",
        f"**Generated (UTC):** {payload['generated_utc']}",
        f"**Pre-registration:** `{payload['preregistration']}`",
        f"**X1 verdict:** `{verdict}`",
        "",
        "## Contact definition (P1 reuse)",
        "",
        f"- `{CONTACT_DEF['name']}`",
        f"- Geometry: {CONTACT_DEF['geometry']}",
        f"- Eligible pool: `mean ≥ {P_POOL_MIN}` (AlloViz / P1 threshold)",
        f"- Top-k: **{K}** (k_eff={stats.get('k_eff', 'n/a')})",
        "",
        "## Static references",
        "",
        f"- LigACN directed edges: {payload['ligacn']['n_directed_edges']}",
        f"- REF_LIGACN undirected: {payload['ligacn']['ref_ligacn_size']}",
        f"- REF_HUB_NBHD: {payload['ligacn']['ref_hub_nbhd_size']}",
        "",
        "## Results (primary = REF_HUB_NBHD)",
        "",
    ]
    if stats:
        lines += [
            f"- Eligible edges: **{stats['n_eligible_edges']}**",
            f"- Frames pooled: **{stats['n_frames_pooled']}**",
            f"- Overlap top-mean ∩ hub-nbhd: **{stats['overlap_mean_hub']}** "
            f"(p={stats['p_mean_hub']:.4f}; beats_null={stats['mean_beats_null_hub']})",
            f"- Overlap top-var ∩ hub-nbhd: **{stats['overlap_var_hub']}** "
            f"(p={stats['p_var_hub']:.4f}; beats_null={stats['var_beats_null_hub']})",
            f"- Null hub overlap mean / p95: {stats['null_hub_mean']:.2f} / {stats['null_hub_p95']:.2f}",
            f"- Secondary LigACN overlaps mean/var: "
            f"{stats['overlap_mean_ligacn']} / {stats['overlap_var_ligacn']}",
            f"- var_more_than_mean: **{stats['var_more_than_mean']}**",
            "",
        ]
    if indeterminate:
        lines += [f"**Indeterminate reason:** {indeterminate}", ""]
    lines += [
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        "## Governance",
        "",
        "- Descriptive overlap only; not a new switch claim.",
        "- Does not reopen P1 hub hypothesis or rescue via cholesterol.",
        "",
        "## Artifacts",
        "",
        f"- `{payload['artifacts']['rank_lists']}`",
        f"- `{payload['artifacts']['report_json']}`",
        "",
    ]
    md_path = OUT_DIR / "x1_mean_vs_variance_report.md"
    json_path = OUT_DIR / "x1_mean_vs_variance_report.json"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    payload = run()
    print(f"X1_VERDICT={payload['x1_verdict']}")
    m = payload.get("metrics") or {}
    if m:
        print(
            f"overlap_mean_hub={m.get('overlap_mean_hub')} "
            f"overlap_var_hub={m.get('overlap_var_hub')} "
            f"p_mean={m.get('p_mean_hub')} p_var={m.get('p_var_hub')}"
        )
    if payload.get("indeterminate_reason"):
        print(f"INDETERMINATE: {payload['indeterminate_reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
