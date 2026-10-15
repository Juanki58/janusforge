#!/usr/bin/env python3
"""Static LigACN topology: orthosteric Source S → Sink Set T.

Governance:
  STATIC_TOPOLOGICAL_BOTTLENECKS only (exploratory / aggregated graph).
  CB2_MINIMAL_GI_CORE = BLOCKED_PENDING_DYNAMIC_VALIDATION
  No CORE_FOUND / no causal Gi necessity / no 'switch'.
  Source Set S: only residues present in WT LigACN matrix AND verified
  against recovered Supp Data contact/source definitions; AUSENTE logged.
"""
from __future__ import annotations

import hashlib
import json
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

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "network_core" / "_raw_downloads"
OUT = ROOT / "results" / "network_core"
MOESM3 = RAW / "41467_2025_60003_MOESM3_ESM.xlsx"  # SD1
MOESM4 = RAW / "41467_2025_60003_MOESM4_ESM.xlsx"  # SD2 contacts
MOESM5 = RAW / "41467_2025_60003_MOESM5_ESM.xlsx"  # SD3 degeneracy

# Sink Set T — Methods Morales-Pastor 2025 (pre-extracted)
SINK_T_SPEC = [
    ("ARG:131", "Arg131", "3x50"),
    ("ASP:240", "Asp240", "6x30"),
    ("SER:303", "Ser303", "8x47"),
    ("SER:69", "Ser69", "2x39"),
]

# Literature / informal pocket candidates — VERIFY only; never auto-add if AUSENTE
CANDIDATE_PROBE = [
    "PHE:87",
    "SER:285",
    "TRP:258",
    "PHE:183",
]

GOVERNANCE = {
    "STATIC_GRAPH_ANALYSIS": "CLOSED",
    "CB2_MINIMAL_GI_CORE": "BLOCKED_PENDING_DYNAMIC_VALIDATION",
    "CB1_COMPARISON": "BLOCKED",
    "DOCKING": "STOP",
    "DE_NOVO_GENERATION": "STOP",
    "NEW_CHEMISTRY": "STOP",
    "TECHNICAL_SEARCH_TRAJ": "NOT_STARTED_THIS_RUN; prior ENLACE_REGISTRADO only",
    "MODO": "READ_ONLY / PUBLIC_DATA_REANALYSIS",
    "report_field": "STATIC_TOPOLOGICAL_BOTTLENECKS",
}

N_NULL = 200
RNG_SEED = 20260820
# Pre-registered topological criteria (before inspecting enrichment p-values for verdict)
# SIGNAL_WEAK: fraction of sinks reachable from ligand source < 0.5 OR mean path-participation
#   enrichment vs degree-preserving null not significant at alpha=0.05 for any non-S/T node.
# HUBS_IDENTIFIED: >=1 non-S/T node with path-participation OR betweenness on S→T paths
#   significantly above degree-preserving null (empirical p < 0.05, two-sided via rank).
# NETWORK_DISTRIBUTED: all T reachable, path redundancy high (median simple-path count
#   upper-bounded enumeration >=3 per reachable sink) AND no node passes hub enrichment.
ALPHA = 0.05
PATH_ENUM_CUTOFF = 8  # max simple-path length for redundancy count


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


def parse_contact_pair(col: str) -> tuple[str, str] | None:
    s = str(col)
    if s in {"mutant_id", "replica"}:
        return None
    parts = s.split("-")
    if len(parts) != 2:
        return None
    return parts[0].strip(), parts[1].strip()


def residue_num(label: str) -> str | None:
    if label == "8D0:1":
        return "LIG"
    if ":" in label:
        return label.split(":")[1]
    return None


def _sheet_contact_evidence(df: pd.DataFrame, label: str, sheet_name: str) -> dict:
    """Per-sheet SD2 contact evidence for a residue / ligand token."""
    num = residue_num(label)
    lig_cols: list[str] = []
    any_cols: list[str] = []
    if num is None:
        return {
            "sheet": sheet_name,
            "residue_number_token": None,
            "n_contact_columns_involving_residue": 0,
            "ligand_contact_columns": [],
            "ligand_contact_wt_or_global_mean": {},
            "wt_rows_found": 0,
        }
    for c in df.columns:
        pair = parse_contact_pair(str(c))
        if pair is None:
            continue
        a, b = pair
        if a == num or b == num:
            any_cols.append(str(c))
            if "LIG" in (a.upper(), b.upper()):
                lig_cols.append(str(c))
    wt = df[df["mutant_id"].astype(str).str.upper() == "WT"]
    lig_wt_means = {}
    for c in lig_cols:
        series = wt[c] if len(wt) else df[c]
        lig_wt_means[c] = float(pd.to_numeric(series, errors="coerce").mean())
    return {
        "sheet": sheet_name,
        "residue_number_token": num,
        "n_contact_columns_involving_residue": len(any_cols),
        "ligand_contact_columns": lig_cols,
        "ligand_contact_wt_or_global_mean": lig_wt_means,
        "wt_rows_found": int(len(wt)),
    }


def contact_evidence_for_residue(
    inactive: pd.DataFrame, active: pd.DataFrame, label: str
) -> dict:
    """Check SD2 Inactive+Active contact tables (network substrate).

    Note: ligand–residue columns (`*-LIG`) are present in Inactive structure
    contacts; Active structure contacts in this deposit has zero LIG columns.
    """
    by_sheet = [
        _sheet_contact_evidence(inactive, label, "Inactive structure contacts"),
        _sheet_contact_evidence(active, label, "Active structure contacts"),
    ]
    lig_cols = []
    n_any = 0
    for s in by_sheet:
        lig_cols.extend([f"{s['sheet']}:{c}" for c in s["ligand_contact_columns"]])
        n_any += s["n_contact_columns_involving_residue"]
    return {
        "residue_number_token": residue_num(label),
        "n_contact_columns_involving_residue": n_any,
        "ligand_contact_columns": lig_cols,
        "by_sheet": by_sheet,
        "note": (
            "SD2 Inactive carries residue–LIG columns; Active sheet in recovered "
            "MOESM4 has no LIG columns."
        ),
    }


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


def define_source_set(
    mat: pd.DataFrame, inactive: pd.DataFrame, active: pd.DataFrame
) -> dict:
    """S = ligand source explicit in matrix + direct out-neighbors verified in graph+contacts.

    Never auto-expand literature pocket lists. Log AUSENTE for missing candidates.
    Contact verification uses SD2 Inactive + Active sheets (LIG columns are in Inactive).
    """
    nodes = set(map(str, mat.index))
    ausente: list[dict] = []
    verified: list[dict] = []

    ligand = "8D0:1"
    if ligand not in nodes:
        ausente.append(
            {
                "label": ligand,
                "status": "AUSENTE",
                "reason": "ligand node not in WT_degeneracy index",
            }
        )
        return {
            "S_final": [],
            "S_definition_rule": "FAILED — ligand absent",
            "verified_members": verified,
            "ausente": ausente,
            "ligand_node": None,
        }

    lig_contact = contact_evidence_for_residue(inactive, active, ligand)
    verified.append(
        {
            "label": ligand,
            "status": "IN_GRAPH",
            "role": "explicit_ligand_source_node_in_WT_degeneracy",
            "in_WT_degeneracy": True,
            "contact_evidence": lig_contact,
            "inclusion_basis": (
                "Present as node 8D0:1 in Supp Data 3 WT_degeneracy; "
                "Morales-Pastor Methods: Dijkstra source = ligand CHEMBL5085420."
            ),
        }
    )

    row = mat.loc[ligand]
    direct = [
        (str(c), float(row[c]))
        for c in mat.columns
        if float(row[c]) > 0 and str(c) != ligand
    ]

    for lab, w in sorted(direct, key=lambda x: -x[1]):
        in_graph = lab in nodes
        ce = contact_evidence_for_residue(inactive, active, lab)
        if not in_graph:
            ausente.append(
                {
                    "label": lab,
                    "status": "AUSENTE",
                    "reason": "listed as neighbor weight but missing from index (should not happen)",
                }
            )
            continue
        if ce["n_contact_columns_involving_residue"] == 0:
            ausente.append(
                {
                    "label": lab,
                    "status": "AUSENTE_FROM_CONTACT_SET",
                    "reason": (
                        "In WT_degeneracy as ligand out-neighbor, but residue number "
                        "not found in any SD2 Inactive/Active contact column."
                    ),
                    "degeneracy_edge_weight_from_ligand": w,
                    "contact_evidence": ce,
                }
            )
            continue
        has_lig = len(ce.get("ligand_contact_columns") or []) > 0
        verified.append(
            {
                "label": lab,
                "status": "IN_GRAPH_AND_CONTACT_SET",
                "role": "direct_LigACN_out_neighbor_of_ligand",
                "in_WT_degeneracy": True,
                "has_residue_LIG_contact_column": has_lig,
                "degeneracy_edge_weight_from_ligand": w,
                "contact_evidence": ce,
                "inclusion_basis": (
                    "Out-neighbor of 8D0:1 with weight>0 in WT_degeneracy AND "
                    "residue number appears in SD2 contact columns "
                    "(Inactive and/or Active); "
                    + (
                        f"explicit LIG contact column(s): {ce['ligand_contact_columns']}."
                        if has_lig
                        else "no explicit *-LIG column (still present in contact set)."
                    )
                ),
            }
        )

    for lab in CANDIDATE_PROBE:
        if any(v["label"] == lab for v in verified):
            continue
        ce = contact_evidence_for_residue(inactive, active, lab)
        if lab not in nodes:
            ausente.append(
                {
                    "label": lab,
                    "status": "AUSENTE",
                    "reason": (
                        "Not present in WT_degeneracy node set; not substituted. "
                        f"SD2 LIG-contact columns (if any): {ce.get('ligand_contact_columns')}."
                    ),
                    "contact_evidence": ce,
                    "probe": "literature_or_informal_pocket_candidate",
                }
            )
        else:
            ausente.append(
                {
                    "label": lab,
                    "status": "PRESENT_IN_GRAPH_BUT_EXCLUDED_FROM_S",
                    "reason": (
                        "In WT_degeneracy but not a direct out-neighbor of 8D0:1 "
                        "under locked S rule (no auto-expansion of pocket lists)."
                    ),
                    "contact_evidence": ce,
                    "probe": "literature_or_informal_pocket_candidate",
                }
            )

    S_final = [v["label"] for v in verified]
    return {
        "S_final": S_final,
        "S_definition_rule": (
            "S = {8D0:1} ∪ {nodes u | w(8D0:1→u)>0 in WT_degeneracy AND "
            "residue number of u appears in SD2 Inactive and/or Active contact columns}. "
            "Literature pocket names probed only for AUSENTE / exclusion log; "
            "no substitution of AUSENTE residues."
        ),
        "verified_members": verified,
        "ausente_or_excluded": ausente,
        "ligand_node": ligand,
        "primary_source_for_paths": ligand,
    }


def path_stats(G: nx.DiGraph, source: str, sinks: list[str]) -> dict:
    out: dict = {
        "source": source,
        "per_sink": {},
        "nodes_on_shortest_paths": Counter(),
        "edges_on_shortest_paths": Counter(),
    }
    for t in sinks:
        rec: dict = {"sink": t, "in_graph": t in G, "reachable": False}
        if t not in G:
            rec["status"] = "AUSENTE_FROM_GRAPH"
            out["per_sink"][t] = rec
            continue
        if not nx.has_path(G, source, t):
            rec["status"] = "NO_PATH"
            out["per_sink"][t] = rec
            continue
        rec["reachable"] = True
        rec["status"] = "PATH_EXISTS"
        # hop-shortest (unweighted) and transmission-weighted shortest
        paths_hop = list(nx.all_shortest_paths(G, source, t))
        paths_w = list(nx.all_shortest_paths(G, source, t, weight="length"))
        rec["n_hop_shortest_paths"] = len(paths_hop)
        rec["hop_length"] = len(paths_hop[0]) - 1
        rec["n_weighted_shortest_paths"] = len(paths_w)
        rec["weighted_length_sum_inv_w"] = float(
            nx.shortest_path_length(G, source, t, weight="length")
        )
        # redundancy: count simple paths up to cutoff
        n_simple = 0
        try:
            for _ in nx.all_simple_paths(G, source, t, cutoff=PATH_ENUM_CUTOFF):
                n_simple += 1
                if n_simple >= 500:
                    break
        except nx.NetworkXError:
            n_simple = 0
        rec["n_simple_paths_cutoff"] = n_simple
        rec["simple_path_cutoff"] = PATH_ENUM_CUTOFF
        for p in paths_hop:
            for n in p[1:-1]:
                out["nodes_on_shortest_paths"][n] += 1
            for a, b in zip(p[:-1], p[1:]):
                out["edges_on_shortest_paths"][(a, b)] += 1
        out["per_sink"][t] = rec
    return out


def betweenness_on_st(G: nx.DiGraph, source: str, sinks: list[str]) -> dict[str, float]:
    """Node betweenness restricted to pairs (source, t) for reachable sinks."""
    bb: dict[str, float] = defaultdict(float)
    reachable = [t for t in sinks if t in G and nx.has_path(G, source, t)]
    if not reachable:
        return {}
    for t in reachable:
        paths = list(nx.all_shortest_paths(G, source, t))
        npaths = len(paths)
        for p in paths:
            for n in p[1:-1]:
                bb[n] += 1.0 / npaths
    # normalize by number of sink targets
    return {k: v / len(reachable) for k, v in bb.items()}


def degree_preserving_null_digraph(G: nx.DiGraph, rng: np.random.Generator) -> nx.DiGraph:
    """Configuration-model style null preserving in/out degree sequences."""
    nodes = list(G.nodes())
    out_deg = [G.out_degree(n) for n in nodes]
    in_deg = [G.in_degree(n) for n in nodes]
    # stub matching
    out_stubs: list[str] = []
    in_stubs: list[str] = []
    for n, od, id_ in zip(nodes, out_deg, in_deg):
        out_stubs.extend([n] * od)
        in_stubs.extend([n] * id_)
    rng.shuffle(out_stubs)
    rng.shuffle(in_stubs)
    H = nx.DiGraph()
    H.add_nodes_from(nodes)
    # pair stubs; skip self-loops by reshuffling limited times
    edges = list(zip(out_stubs, in_stubs))
    for _ in range(10):
        cleaned = []
        leftovers_out = []
        leftovers_in = []
        for u, v in edges:
            if u != v and not H.has_edge(u, v):
                H.add_edge(u, v, weight=1.0, length=1.0)
            else:
                leftovers_out.append(u)
                leftovers_in.append(v)
        if not leftovers_out:
            break
        rng.shuffle(leftovers_out)
        rng.shuffle(leftovers_in)
        edges = list(zip(leftovers_out, leftovers_in))
    return H


def participation_vector(G: nx.DiGraph, source: str, sinks: list[str]) -> dict[str, float]:
    stats = path_stats(G, source, sinks)
    total = sum(stats["nodes_on_shortest_paths"].values()) or 1
    return {n: c / total for n, c in stats["nodes_on_shortest_paths"].items()}


def enrichment_vs_null(
    G: nx.DiGraph, source: str, sinks: list[str], n_null: int, seed: int
) -> dict:
    obs_part = participation_vector(G, source, sinks)
    obs_bb = betweenness_on_st(G, source, sinks)
    rng = np.random.default_rng(seed)
    null_parts: list[dict[str, float]] = []
    null_bbs: list[dict[str, float]] = []
    null_reach: list[int] = []
    for _ in range(n_null):
        H = degree_preserving_null_digraph(G, rng)
        # ensure source exists
        if source not in H:
            continue
        ps = path_stats(H, source, sinks)
        null_reach.append(sum(1 for t, r in ps["per_sink"].items() if r.get("reachable")))
        null_parts.append(participation_vector(H, source, sinks))
        null_bbs.append(betweenness_on_st(H, source, sinks))

    def empir_p(obs: float, null_vals: list[float]) -> float:
        if not null_vals:
            return 1.0
        # two-sided via extremity vs null mean
        arr = np.asarray(null_vals, dtype=float)
        return float((np.sum(np.abs(arr - arr.mean()) >= abs(obs - arr.mean())) + 1) / (len(arr) + 1))

    nodes_of_interest = sorted(set(obs_part) | set(obs_bb))
    rows = []
    for n in nodes_of_interest:
        pv = [d.get(n, 0.0) for d in null_parts]
        bv = [d.get(n, 0.0) for d in null_bbs]
        rows.append(
            {
                "node": n,
                "obs_path_participation": obs_part.get(n, 0.0),
                "null_mean_participation": float(np.mean(pv)) if pv else None,
                "p_participation": empir_p(obs_part.get(n, 0.0), pv),
                "obs_st_betweenness": obs_bb.get(n, 0.0),
                "null_mean_st_betweenness": float(np.mean(bv)) if bv else None,
                "p_st_betweenness": empir_p(obs_bb.get(n, 0.0), bv),
            }
        )
    rows.sort(key=lambda r: (-r["obs_path_participation"], -r["obs_st_betweenness"]))
    return {
        "null_model": (
            "Directed configuration-model style rewiring preserving in- and out-degree "
            f"sequences of WT LigACN DiGraph; n_null={n_null}; seed={seed}. "
            "Self-loops/multiedges avoided when possible."
        ),
        "n_null_realized": len(null_parts),
        "obs_n_sinks_reachable": sum(
            1 for t in sinks if t in G and nx.has_path(G, source, t)
        ),
        "null_mean_n_sinks_reachable": float(np.mean(null_reach)) if null_reach else None,
        "node_enrichment": rows,
    }


def load_sd1() -> pd.DataFrame:
    df = pd.read_excel(MOESM3, header=1)
    return df


def mutagenesis_overlap(
    path_nodes: list[str], hubs: list[str], sd1: pd.DataFrame, sd3_sheets: list[str]
) -> list[dict]:
    """Exact residue ↔ SD1 functional effect; SD3 sheet presence if simulated."""
    pos_to_rows: dict[int, list[dict]] = defaultdict(list)
    for _, row in sd1.iterrows():
        try:
            pos = int(row["position"])
        except (TypeError, ValueError):
            continue
        pos_to_rows[pos].append(
            {
                "mutant": str(row.get("mutant")),
                "position": pos,
                "pct_wt_expression": _f(row.get("%wt expression")),
                "Gi2_Emax_raw": _f(row.get("Gi2 Emax")),
                "bArr1_Emax_raw": _f(row.get("bArr1 Emax")),
                "Gi2_Emax_norm": _f(row.get("Gi2 Emax.1")),
                "bArr1_Emax_norm": _f(row.get("bArr1 Emax.1")),
                "simulated": str(row.get("simulated")),
                "coupling_profile": str(row.get("coupling profile")),
            }
        )

    interest = []
    for lab in path_nodes + hubs:
        if lab not in interest:
            interest.append(lab)

    out = []
    for lab in interest:
        num = residue_num(lab)
        if num is None or not str(num).isdigit():
            out.append(
                {
                    "node": lab,
                    "sd1_rows": [],
                    "sd3_degeneracy_sheet": None,
                    "note": "non-residue or ligand node",
                }
            )
            continue
        pos = int(num)
        sheet = f"{pos}_degeneracy"
        out.append(
            {
                "node": lab,
                "position": pos,
                "sd1_rows": pos_to_rows.get(pos, []),
                "sd3_degeneracy_sheet_present": sheet in sd3_sheets,
                "sd3_sheet_name": sheet if sheet in sd3_sheets else None,
            }
        )
    return out


def _f(x):
    try:
        if pd.isna(x):
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def assign_verdict(
    n_reachable: int,
    n_sinks: int,
    enrichment: dict,
    S: set[str],
    T: set[str],
    path_redundancy_medians: list[int],
) -> dict:
    excl = S | T
    sig_hubs = [
        r
        for r in enrichment["node_enrichment"]
        if r["node"] not in excl
        and (
            (r["p_participation"] is not None and r["p_participation"] < ALPHA)
            or (r["p_st_betweenness"] is not None and r["p_st_betweenness"] < ALPHA)
        )
        and r["obs_path_participation"] > 0
    ]
    frac = n_reachable / n_sinks if n_sinks else 0.0
    med_red = float(np.median(path_redundancy_medians)) if path_redundancy_medians else 0.0

    if frac < 0.5:
        code = "TOPOLOGICAL_SIGNAL_WEAK"
        rationale = (
            f"Only {n_reachable}/{n_sinks} sinks reachable from ligand source in WT LigACN "
            f"(fraction={frac:.2f} < 0.5). Degree-preserving null documented in metrics."
        )
    elif sig_hubs:
        code = "TOPOLOGICAL_HUBS_IDENTIFIED"
        rationale = (
            f"{len(sig_hubs)} non-S/T node(s) enriched vs degree-preserving null "
            f"(alpha={ALPHA}) on S→T shortest-path participation and/or betweenness."
        )
    elif n_reachable == n_sinks and med_red >= 3 and not sig_hubs:
        code = "TOPOLOGICAL_NETWORK_DISTRIBUTED"
        rationale = (
            f"All {n_sinks} sinks reachable; median simple-path count (cutoff={PATH_ENUM_CUTOFF}) "
            f"= {med_red}; no non-S/T node passes enrichment vs degree-preserving null."
        )
    else:
        code = "INDETERMINATE"
        rationale = (
            "Reachability/enrichment/redundancy pattern does not uniquely match "
            "HUBS / DISTRIBUTED / SIGNAL_WEAK pre-registered criteria."
        )

    return {
        "STATIC_TOPOLOGICAL_BOTTLENECKS": code,
        "rationale": rationale,
        "significant_hub_nodes": [r["node"] for r in sig_hubs],
        "significant_hub_detail": sig_hubs,
        "fraction_sinks_reachable": frac,
        "median_simple_path_redundancy": med_red,
        "alpha": ALPHA,
        "epistemic_tag": "[INTERNAL_REANALYSIS]",
        "interpretation_limit": (
            "Describes topological properties of the aggregated published LigACN only. "
            "Does NOT establish residues as causally necessary for Gi. "
            "Dynamic causal core remains BLOCKED_PENDING_DYNAMIC_VALIDATION."
        ),
    }


def write_report(payload: dict) -> str:
    gdef = payload["graph_definition"]
    Sinfo = payload["source_set_S"]
    Tinfo = payload["sink_set_T"]
    conn = payload["connectivity"]
    verd = payload["verdict"]
    mut = payload["mutagenesis_overlap"]
    enr = payload["enrichment"]

    lines = []
    lines.append("# STATIC_TOPOLOGICAL_BOTTLENECKS — LigACN WT (exploratory)")
    lines.append("")
    lines.append(f"**Branch:** `task/static-ligacn-topology`  ")
    lines.append(f"**Access / run UTC:** `{payload['run_utc']}`  ")
    lines.append(f"**Verdict field:** `STATIC_TOPOLOGICAL_BOTTLENECKS` = **`{verd['STATIC_TOPOLOGICAL_BOTTLENECKS']}`**  ")
    lines.append("")
    lines.append("```yaml")
    for k, v in GOVERNANCE.items():
        lines.append(f"{k}: {v}")
    lines.append("```")
    lines.append("")
    lines.append(
        "**Interpretation limit:** ONLY topological properties of the aggregated published "
        "network — **not** causal necessity for Gi, **not** dynamic minimal core, **not** a switch."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Exact graph definition")
    lines.append("")
    lines.append(f"- **Source object:** `{gdef['matrix_file']}` sheet `{gdef['sheet']}` (Supp Data 3).")
    lines.append(f"- **SHA256:** `{gdef['sha256']}`")
    lines.append(f"- **Nodes:** {gdef['n_nodes']} labels from matrix index/columns (residue tokens `AA:pos` or ligand `8D0:1`).")
    lines.append(
        f"- **Edges:** directed; edge `u→v` iff cell `(u,v) > 0`. "
        f"**Weight** = published **degeneracy / information-transmission** value in that cell "
        f"(fractional participation of contact in shortest ligand→intracellular pathways; paper metric)."
    )
    lines.append(
        f"- **Edge count (weight>0, excluding diagonal):** {gdef['n_edges']}."
    )
    lines.append(
        "- **Path length for weighted shortest paths:** `length = 1/weight` (higher transmission → shorter)."
    )
    lines.append(
        "- **Unweighted / hop shortest paths:** each positive edge length 1 (used for path participation counts)."
    )
    lines.append(
        f"- **Contact substrate (SD2):** `{gdef['contacts_file']}` sheets "
        f"`Inactive structure contacts` + `Active structure contacts` — columns are "
        f"residue–residue (or residue–LIG) contact IDs; used only to **verify** Source Set S "
        f"membership, not to rebuild edges. "
        f"(Recovered MOESM4: residue–LIG columns are in **Inactive** only.)"
    )
    lines.append("")
    lines.append("## 2. Real composition of S and T")
    lines.append("")
    lines.append("### Source Set S (locked rule)")
    lines.append("")
    lines.append(f"**Rule:** {Sinfo['S_definition_rule']}")
    lines.append("")
    lines.append(f"**Final S:** `{Sinfo['S_final']}`")
    lines.append("")
    lines.append("| Member | Status | Basis |")
    lines.append("|--------|--------|-------|")
    for v in Sinfo["verified_members"]:
        lines.append(
            f"| `{v['label']}` | {v['status']} | {v['inclusion_basis']} |"
        )
    lines.append("")
    lines.append("**AUSENTE / excluded probes (no silent drop, no substitution):**")
    lines.append("")
    if not Sinfo.get("ausente_or_excluded"):
        lines.append("- (none)")
    else:
        for a in Sinfo["ausente_or_excluded"]:
            lines.append(
                f"- `{a['label']}` — **{a['status']}** — {a.get('reason','')}"
            )
    lines.append("")
    lines.append("### Sink Set T")
    lines.append("")
    lines.append("| Matrix node | Paper residue | BW | In graph |")
    lines.append("|-------------|---------------|----|----------|")
    for t in Tinfo["members"]:
        lines.append(
            f"| `{t['matrix_label']}` | {t['paper_name']} | {t['bw']} | {t['in_graph']} |"
        )
    lines.append("")
    lines.append("### Connectivity S (ligand source) → T")
    lines.append("")
    lines.append(
        f"Primary path source used: `{Sinfo['primary_source_for_paths']}` "
        "(paper Dijkstra source). Other S members are documented orthosteric contacts, "
        "not alternate Dijkstra sources unless noted."
    )
    lines.append("")
    lines.append("| Sink | Status | Hop length | # hop-shortest paths | # simple paths (cutoff) |")
    lines.append("|------|--------|------------|----------------------|-------------------------|")
    for t, rec in conn["per_sink"].items():
        lines.append(
            f"| `{t}` | {rec.get('status')} | {rec.get('hop_length','')} | "
            f"{rec.get('n_hop_shortest_paths','')} | {rec.get('n_simple_paths_cutoff','')} |"
        )
    lines.append("")
    lines.append(
        f"**Sinks with a path from ligand:** "
        f"{conn['n_reachable']}/{conn['n_sinks']}."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Nulls and enrichment")
    lines.append("")
    lines.append(f"**Null model:** {enr['null_model']}")
    lines.append("")
    lines.append(
        f"- Observed sinks reachable: **{enr['obs_n_sinks_reachable']}**; "
        f"null mean reachable: **{enr['null_mean_n_sinks_reachable']}** "
        f"(n_null realized={enr['n_null_realized']})."
    )
    lines.append(f"- Alpha (pre-registered): **{ALPHA}**.")
    lines.append("")
    lines.append("Top nodes by observed path participation (intermediates on hop-shortest paths):")
    lines.append("")
    lines.append("| Node | obs participation | null mean | p_part | obs ST-betweenness | p_bb |")
    lines.append("|------|-------------------|-----------|--------|--------------------|------|")
    for r in enr["node_enrichment"][:20]:
        lines.append(
            f"| `{r['node']}` | {r['obs_path_participation']:.4f} | "
            f"{r['null_mean_participation']} | {r['p_participation']:.4f} | "
            f"{r['obs_st_betweenness']:.4f} | {r['p_st_betweenness']:.4f} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Mutagenesis overlap (exact)")
    lines.append("")
    lines.append(
        "Overlap is **not** asserted qualitatively. Below: each high-interest topology node "
        "with SD1 (MOESM3) rows at that position and whether an SD3 degeneracy sheet exists."
    )
    lines.append("")
    for m in mut:
        lines.append(f"### `{m['node']}`")
        rows = m.get("sd1_rows") or []
        if not rows:
            lines.append(f"- SD1: no mutant row at this position ({m.get('note','')}).")
        else:
            for r in rows:
                lines.append(
                    f"- **{r['mutant']}** (pos {r['position']}): coupling_profile=`{r['coupling_profile']}`; "
                    f"simulated=`{r['simulated']}`; "
                    f"%wt_expr={r['pct_wt_expression']}; "
                    f"Gi2_Emax_raw={r['Gi2_Emax_raw']}; bArr1_Emax_raw={r['bArr1_Emax_raw']}; "
                    f"Gi2_Emax_norm={r['Gi2_Emax_norm']}; bArr1_Emax_norm={r['bArr1_Emax_norm']}"
                )
        lines.append(
            f"- SD3 sheet `{m.get('sd3_sheet_name')}` present: "
            f"**{m.get('sd3_degeneracy_sheet_present')}**"
        )
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Topological summary (non-causal)")
    lines.append("")
    lines.append(f"- **Hubs (enriched):** {verd.get('significant_hub_nodes')}")
    lines.append(
        f"- **High path-participation intermediates (descriptive top):** "
        f"{payload['descriptive_top_intermediates']}"
    )
    lines.append(f"- **Verdict rationale:** {verd['rationale']}")
    lines.append(f"- **Tag:** {verd['epistemic_tag']}")
    lines.append(f"- **Limit:** {verd['interpretation_limit']}")
    lines.append("")
    lines.append("## 6. Trajectories / MSM (one-liner status)")
    lines.append("")
    lines.append(payload["traj_status_oneliner"])
    lines.append("")
    lines.append("## 7. Future work (not now)")
    lines.append("")
    lines.append(
        "When trajectories exist: compare dynamic communication network vs this static map "
        "(do static bottlenecks survive dynamically?). Dynamic causal core remains "
        "`BLOCKED_PENDING_DYNAMIC_VALIDATION`."
    )
    lines.append("")
    lines.append("**STOP.** No docking. No de novo. Human review next.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mat = load_wt_matrix()
    inactive = pd.read_excel(MOESM4, sheet_name="Inactive structure contacts")
    active = pd.read_excel(MOESM4, sheet_name="Active structure contacts")
    G = build_digraph(mat)
    Sinfo = define_source_set(mat, inactive, active)
    source = Sinfo["primary_source_for_paths"]
    if source is None or source not in G:
        raise SystemExit("Ligand source absent — abort fail-closed")

    T_members = []
    sinks = []
    for lab, paper, bw in SINK_T_SPEC:
        present = lab in G
        T_members.append(
            {
                "matrix_label": lab,
                "paper_name": paper,
                "bw": bw,
                "in_graph": present,
                "status": "IN_GRAPH" if present else "AUSENTE",
            }
        )
        if present:
            sinks.append(lab)
        # if AUSENTE — do not substitute

    ps = path_stats(G, source, sinks)
    n_reachable = sum(1 for r in ps["per_sink"].values() if r.get("reachable"))
    enr = enrichment_vs_null(G, source, sinks, N_NULL, RNG_SEED)

    red = [
        r.get("n_simple_paths_cutoff", 0)
        for r in ps["per_sink"].values()
        if r.get("reachable")
    ]
    verd = assign_verdict(
        n_reachable,
        len(sinks),
        enr,
        set(Sinfo["S_final"]),
        set(sinks),
        red,
    )

    # descriptive tops
    top_inter = [
        n
        for n, _ in ps["nodes_on_shortest_paths"].most_common(15)
        if n not in set(Sinfo["S_final"]) | set(sinks)
    ]

    xl5 = pd.ExcelFile(MOESM5)
    sd1 = load_sd1()
    interest_nodes = list(
        dict.fromkeys(
            top_inter[:12]
            + verd.get("significant_hub_nodes", [])
            + [n for n, _ in ps["nodes_on_shortest_paths"].most_common(20)]
        )
    )
    mut = mutagenesis_overlap(interest_nodes, verd.get("significant_hub_nodes", []), sd1, xl5.sheet_names)

    # bottlenecks: edges on many shortest paths
    top_edges = [
        {"edge": [a, b], "count_on_hop_shortest": c}
        for (a, b), c in ps["edges_on_shortest_paths"].most_common(15)
    ]

    graph_definition = {
        "matrix_file": str(MOESM5.relative_to(ROOT)).replace("\\", "/"),
        "sheet": "WT_degeneracy",
        "sha256": sha256(MOESM5),
        "bytes": MOESM5.stat().st_size,
        "contacts_file": str(MOESM4.relative_to(ROOT)).replace("\\", "/"),
        "contacts_sheets": [
            "Inactive structure contacts",
            "Active structure contacts",
        ],
        "contacts_sha256": sha256(MOESM4),
        "sd1_file": str(MOESM3.relative_to(ROOT)).replace("\\", "/"),
        "sd1_sha256": sha256(MOESM3),
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "weight_meaning": (
            "Supp Data 3 degeneracy / information transmission "
            "(pathway participation frequency)"
        ),
        "software": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "networkx": nx.__version__,
            "numpy": np.__version__,
        },
    }

    traj_status = (
        "Trajectories/MSM: **not recovered this run** — GPCRmd/1540 and Box "
        "`jzooa0o27z1w9ha0h6va3i51ir7l38j4` remain ENLACE_REGISTRADO only "
        "(no new multi-cycle hunt)."
    )

    metrics = {
        "run_utc": run_utc,
        "governance": GOVERNANCE,
        "graph_definition": graph_definition,
        "source_set_S": Sinfo,
        "sink_set_T": {"members": T_members, "used_for_paths": sinks},
        "connectivity": {
            "primary_source": source,
            "n_sinks": len(sinks),
            "n_reachable": n_reachable,
            "per_sink": ps["per_sink"],
            "nodes_on_shortest_paths": dict(ps["nodes_on_shortest_paths"]),
            "top_bottleneck_edges": top_edges,
        },
        "enrichment": enr,
        "descriptive_top_intermediates": top_inter,
        "mutagenesis_overlap": mut,
        "verdict": verd,
        "traj_status_oneliner": traj_status,
    }

    verdict_json = {
        "report_field": "STATIC_TOPOLOGICAL_BOTTLENECKS",
        "STATIC_TOPOLOGICAL_BOTTLENECKS": verd["STATIC_TOPOLOGICAL_BOTTLENECKS"],
        "rationale": verd["rationale"],
        "significant_hub_nodes": verd["significant_hub_nodes"],
        "S_final": Sinfo["S_final"],
        "T": sinks,
        "governance": GOVERNANCE,
        "interpretation_limit": verd["interpretation_limit"],
        "run_utc": run_utc,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    metrics_path = OUT / "static_ligacn_topology_metrics.json"
    verdict_path = OUT / "static_topological_verdict.json"
    report_path = OUT / "static_ligacn_topology_report.md"

    metrics_path.write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    verdict_path.write_text(json.dumps(verdict_json, indent=2), encoding="utf-8")
    report_path.write_text(write_report(metrics), encoding="utf-8")

    print("WROTE", report_path)
    print("WROTE", metrics_path)
    print("WROTE", verdict_path)
    print("VERDICT", verd["STATIC_TOPOLOGICAL_BOTTLENECKS"])
    print("S_final", Sinfo["S_final"])
    print("hubs", verd["significant_hub_nodes"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
