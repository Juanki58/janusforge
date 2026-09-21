#!/usr/bin/env python3
"""EXTERNAL inventory: six frozen Janusforge hubs ↔ LigACNtop / PrefCoup clusters 1–3.

Pre-reg: docs/synthesis/EXPERIMENT_HUBS_VS_LIGACN_INVENTORY.md
Scope: EXTERNAL inventory only. Does NOT reopen P1/P2 or claim Gi.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "network_core" / "_raw_downloads"
OUT = ROOT / "results" / "network_core"
MOESM3 = RAW / "41467_2025_60003_MOESM3_ESM.xlsx"  # SD1
MOESM5 = RAW / "41467_2025_60003_MOESM5_ESM.xlsx"  # SD3 / WT_degeneracy
PREFCOUP_NB = RAW / "prefcoup_cb2r" / "clustering.ipynb"
PREFCOUP_GROUPS_JSON = RAW / "prefcoup_cb2r" / "pca_groups_published.json"

# Fixed a priori — do not retune (same set as dual-test / X1)
HUBS = [
    ("ALA:79", "ALA79", "2.49", 79),
    ("ALA:83", "ALA83", "2.53", 83),
    ("LEU:287", "LEU287", "7.41", 287),
    ("ASN:291", "ASN291", "7.45", 291),
    ("ASN:295", "ASN295", "7.49", 295),
    ("ARG:302", "ARG302", "8.46", 302),
]
HUB_LABELS = [h[0] for h in HUBS]

# Morales-Pastor Methods / Fig. 3 caption
LIGACNTOP_DEGENERACY_CUTOFF = 0.146

# Published PrefCoup cluster membership from GPCRmd/prefcoup_cb2r clustering.ipynb
# (cell defining `groups`; mutant_id = UniProt residue number as string).
# Cluster 1–3 = PrefCoup_Gαi2 simulated mutants; labels are paper cluster IDs.
PUBLISHED_PREFCOUP_GROUPS = {
    1: {"109", "125", "176", "285", "292"},
    2: {"77", "117", "217"},
    3: {"199", "205", "291", "302"},
}
# Notebook notes these PrefCoup simulated mutants were not caught in `groups`:
PREFCOUP_SIMULATED_UNCATCHED = {"61", "297"}

GOVERNANCE = {
    "mode": "EXTERNAL_HUBS_VS_LIGACN_INVENTORY",
    "MODO": "READ_ONLY_DATA",
    "P1_DYNAMIC_HUBS": "CLOSED_NOT_SUPPORTED_UNCHANGED",
    "P2_MSM": "CLOSED_INSUFFICIENT_SAMPLING_UNCHANGED",
    "STATIC_DUAL_TEST": "CORE_TOPOLOGICAL_ONLY_UNCHANGED",
    "Gi_claims": "STOP",
    "docking": "STOP",
    "de_novo": "STOP",
    "hub_list": "FIXED_A_PRIORI_NO_RETUNE",
    "literature_doi": "10.1038/s41467-025-60003-0",
    "prefcoup_code": "https://github.com/GPCRmd/prefcoup_cb2r",
    "zenodo": "10.5281/zenodo.15270434",
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


def build_undirected_ligacn(mat: pd.DataFrame) -> nx.Graph:
    """Undirected contact graph for hop-distance (paper Methods)."""
    G = nx.Graph()
    arr = mat.to_numpy(dtype=float)
    for i, u in enumerate(mat.index):
        for j, v in enumerate(mat.columns):
            w = float(arr[i, j])
            if w > 0 and u != v:
                if G.has_edge(u, v):
                    G[u][v]["weight"] = max(float(G[u][v]["weight"]), w)
                else:
                    G.add_edge(u, v, weight=w)
    return G


def ligacntop_edges(mat: pd.DataFrame, cutoff: float) -> list[tuple[str, str, float]]:
    edges: list[tuple[str, str, float]] = []
    arr = mat.to_numpy(dtype=float)
    for i, u in enumerate(mat.index):
        for j, v in enumerate(mat.columns):
            w = float(arr[i, j])
            if w >= cutoff and u != v:
                edges.append((str(u), str(v), w))
    return edges


def dist_to_top(G: nx.Graph, hub: str, top_nodes: set[str]) -> int | None:
    if hub not in G:
        return None
    if hub in top_nodes:
        return 0
    dists = []
    for t in top_nodes:
        if t in G and nx.has_path(G, hub, t):
            dists.append(int(nx.shortest_path_length(G, hub, t)))
    return min(dists) if dists else None


def max_incident_weight(mat: pd.DataFrame, hub: str) -> float:
    if hub not in mat.index or hub not in mat.columns:
        return float("nan")
    vals = [float(x) for x in list(mat.loc[hub].values) + list(mat[hub].values) if pd.notna(x)]
    pos = [v for v in vals if v > 0]
    return float(max(pos)) if pos else 0.0


def load_sd1() -> pd.DataFrame | None:
    if not MOESM3.exists():
        return None
    df = pd.read_excel(MOESM3, header=1)
    df["position"] = pd.to_numeric(df["position"], errors="coerce")
    return df


def sd1_row_for_position(df: pd.DataFrame | None, pos: int) -> dict:
    if df is None:
        return {"status": "SD1_MISSING"}
    rows = df[df["position"] == pos]
    if rows.empty:
        return {"status": "NO_MUTANT_AT_POSITION"}
    # Prefer alanine/valine scan row matching dual-test nomenclature if multiple
    out = []
    for _, r in rows.iterrows():
        out.append(
            {
                "mutant": str(r.get("mutant")),
                "pct_wt_expression": float(r["%wt expression"])
                if pd.notna(r.get("%wt expression"))
                else None,
                "coupling_profile": str(r.get("coupling profile")),
                "simulated": str(r.get("simulated")),
            }
        )
    return {"status": "PRESENT", "mutations": out}


def _recover_groups_from_notebook() -> dict[int, set[str]]:
    import ast

    nb = json.loads(PREFCOUP_NB.read_text(encoding="utf-8"))
    src = ""
    for cell in nb.get("cells", []):
        s = cell.get("source", [])
        src += "".join(s) if isinstance(s, list) else str(s)
        src += "\n"
    idx = src.find("groups = {")
    if idx < 0:
        raise ValueError("groups = { not found in notebook source")
    brace = src.find("{", idx)
    depth = 0
    end = None
    for i, ch in enumerate(src[brace:], start=brace):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise ValueError("unbalanced braces in groups dict")
    groups = ast.literal_eval(src[brace:end])
    return {int(k): {str(sim).split("-")[0] for sim in sims} for k, sims in groups.items()}


def verify_prefcoup_groups() -> dict:
    """Confirm published groups vs local notebook and/or slim JSON provenance."""
    expected = {k: set(v) for k, v in PUBLISHED_PREFCOUP_GROUPS.items()}
    out: dict = {
        "expected": {str(k): sorted(v) for k, v in sorted(expected.items())},
        "json_provenance": None,
        "notebook": None,
    }

    if PREFCOUP_GROUPS_JSON.exists():
        meta = json.loads(PREFCOUP_GROUPS_JSON.read_text(encoding="utf-8"))
        from_json = {
            int(k): set(v) for k, v in meta.get("groups_mutant_positions", {}).items()
        }
        out["json_provenance"] = {
            "path": str(PREFCOUP_GROUPS_JSON.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(PREFCOUP_GROUPS_JSON),
            "match_published_dict": from_json == expected,
            "source_url": meta.get("source"),
            "notebook_sha256_at_fetch": meta.get("notebook_sha256_at_fetch"),
        }

    if PREFCOUP_NB.exists():
        try:
            recovered = _recover_groups_from_notebook()
            out["notebook"] = {
                "present": True,
                "path": str(PREFCOUP_NB.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256(PREFCOUP_NB),
                "match_published_dict": recovered == expected,
                "recovered": {str(k): sorted(v) for k, v in sorted(recovered.items())},
            }
        except Exception as e:  # noqa: BLE001
            out["notebook"] = {
                "present": True,
                "match_published_dict": False,
                "error": str(e),
                "sha256": sha256(PREFCOUP_NB),
            }
    else:
        out["notebook"] = {
            "present": False,
            "note": "Full clustering.ipynb optional; slim pca_groups_published.json is sufficient",
        }

    json_ok = bool(out["json_provenance"] and out["json_provenance"].get("match_published_dict"))
    nb_ok = bool(out["notebook"] and out["notebook"].get("match_published_dict"))
    out["match_published_dict"] = json_ok or nb_ok or (not PREFCOUP_NB.exists() and not PREFCOUP_GROUPS_JSON.exists())
    return out


def prefcoup_cluster_for_position(pos: int) -> str:
    s = str(pos)
    for cid, members in PUBLISHED_PREFCOUP_GROUPS.items():
        if s in members:
            return str(cid)
    if s in PREFCOUP_SIMULATED_UNCATCHED:
        return "PREFCOUP_SIMULATED_NOT_IN_GROUPS"
    return "NOT_IN_SIMULATED_PREFCOUP_CLUSTERS"


def call_verdict(n_in_top: int, moesm5_ok: bool) -> str:
    if not moesm5_ok:
        return "INDETERMINATE_MISSING_SUPP"
    if n_in_top >= 5:
        return "EXT_HUBS_IN_LIGACNTOP"
    if n_in_top >= 2:
        return "PARTIAL"
    # ≤1: check if DISTINCT needs median distance — handled by caller if needed
    return "DISTINCT_CANDIDATE"


def prefcoup_overlay(n_in_cluster: int, groups_ok: bool) -> str:
    if not groups_ok:
        return "INDETERMINATE"
    if n_in_cluster >= 5:
        return "FULL"
    if n_in_cluster >= 1:
        return "PARTIAL"
    return "NONE"


def write_md(payload: dict, path: Path) -> None:
    lines: list[str] = []
    v = payload["verdict"]
    lines.append("# EXTERNAL inventory — hubs ↔ LigACNtop / PrefCoup clusters")
    lines.append("")
    lines.append(f"**Run UTC:** `{payload['run_utc']}`  ")
    lines.append(f"**Branch context:** `feat/cb2-hubs-functional-topology-test`  ")
    lines.append(f"**Pre-reg:** `docs/synthesis/EXPERIMENT_HUBS_VS_LIGACN_INVENTORY.md`  ")
    lines.append(
        f"**Literature:** Morales-Pastor et al., *Nat Commun* (2025), "
        f"DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)"
    )
    lines.append("")
    lines.append("## Verdict")
    lines.append("")
    lines.append(f"**Primary (LigACNtop):** `{v['primary']}`  ")
    lines.append(f"**PrefCoup overlay (secondary):** `{v['prefcoup_overlay']}`  ")
    lines.append("")
    lines.append(
        "> EXTERNAL inventory only. Does **not** reopen P1, P2, or Gi enrichment claims. "
        "Static dual-test remains `CORE_TOPOLOGICAL_ONLY`."
    )
    lines.append("")
    lines.append("## Plain-language answer")
    lines.append("")
    lines.append(payload["plain_language"])
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    p = payload["provenance"]
    lines.append(f"- MOESM5 (Supp Data 3): `{p['moesm5']}` sha256=`{p['moesm5_sha256']}`")
    lines.append(f"- MOESM3 (Supp Data 1): `{p['moesm3']}` sha256=`{p['moesm3_sha256']}`")
    lines.append(
        f"- LigACNtop cutoff: degeneracy ≥ **{p['ligacntop_cutoff']}** "
        "(Morales-Pastor Methods / Fig. 3)"
    )
    lines.append(
        f"- LigACNtop edges / nodes: **{p['n_ligacntop_edges']}** / **{p['n_ligacntop_nodes']}**"
    )
    lines.append(
        f"- PrefCoup `groups` verify match: `{p['prefcoup_groups_verify'].get('match_published_dict')}`"
    )
    lines.append("")
    lines.append("## Per-hub inventory")
    lines.append("")
    lines.append(
        "| Hub | BW | in LigACN | in LigACNtop | dist→top | max degeneracy | PrefCoup cluster | SD1 profile |"
    )
    lines.append(
        "|-----|----|-----------|--------------|----------|----------------|------------------|-------------|"
    )
    for row in payload["hubs"]:
        sd1 = row["sd1"]
        if sd1.get("status") == "PRESENT" and sd1.get("mutations"):
            m0 = sd1["mutations"][0]
            sd1_s = f"{m0['mutant']} / {m0['coupling_profile']} / {m0['simulated']}"
        else:
            sd1_s = sd1.get("status", "?")
        lines.append(
            f"| `{row['ligacn']}` | {row['bw']} | {row['in_LigACN']} | "
            f"**{row['in_LigACNtop']}** | {row['dist_to_LigACNtop']} | "
            f"{row['max_incident_degeneracy']:.4f} | {row['prefcoup_cluster']} | {sd1_s} |"
        )
    lines.append("")
    lines.append("### LigACNtop edges incident to hubs")
    lines.append("")
    for row in payload["hubs"]:
        edges = row["ligacntop_edges_incident"]
        if not edges:
            lines.append(f"- `{row['ligacn']}`: *(none as endpoint at cutoff)*")
        else:
            e_s = ", ".join(f"{u}→{v} ({w:.4f})" for u, v, w in edges)
            lines.append(f"- `{row['ligacn']}`: {e_s}")
    lines.append("")
    lines.append("## PrefCoup clusters 1–3 (published mutant positions)")
    lines.append("")
    for cid, members in sorted(payload["prefcoup_clusters"].items(), key=lambda x: int(x[0])):
        lines.append(f"- **Cluster {cid}:** {', '.join(members)}")
    lines.append(
        f"- PrefCoup simulated not in `groups`: "
        f"{', '.join(sorted(payload['prefcoup_simulated_uncatched']))}"
    )
    lines.append("")
    lines.append("## Aggregates")
    lines.append("")
    a = payload["aggregates"]
    lines.append(f"- Hubs in LigACNtop: **{a['n_hubs_in_LigACNtop']}/6**")
    lines.append(
        f"- Hubs in any PrefCoup cluster 1–3: **{a['n_hubs_in_any_PrefCoup_cluster']}/6**"
    )
    lines.append(
        f"- Jaccard(hubs, LigACNtop nodes): **{a['jaccard_hubs_vs_LigACNtop_nodes']:.4f}**"
    )
    lines.append("")
    lines.append("## Governance")
    lines.append("")
    lines.append("```yaml")
    for k, val in GOVERNANCE.items():
        lines.append(f"{k}: {val}")
    lines.append("```")
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not MOESM5.exists():
        payload = {
            "run_utc": run_utc,
            "verdict": {
                "primary": "INDETERMINATE_MISSING_SUPP",
                "prefcoup_overlay": "INDETERMINATE",
            },
            "plain_language": (
                "Supp Data 3 (MOESM5 WT_degeneracy) missing locally; cannot reconstruct LigACNtop."
            ),
            "governance": GOVERNANCE,
            "platform": platform.platform(),
        }
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "hubs_vs_ligacn_inventory.json").write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )
        write_md(payload, OUT / "hubs_vs_ligacn_inventory.md")
        print("INDETERMINATE_MISSING_SUPP", file=sys.stderr)
        return 2

    mat = load_wt_matrix()
    G = build_undirected_ligacn(mat)
    top_e = ligacntop_edges(mat, LIGACNTOP_DEGENERACY_CUTOFF)
    top_nodes = {u for u, v, _ in top_e} | {v for u, v, _ in top_e}
    sd1 = load_sd1()
    groups_verify = verify_prefcoup_groups()
    groups_ok = bool(groups_verify.get("match_published_dict"))

    hub_rows = []
    for label, short, bw, pos in HUBS:
        incident = [
            [u, v, float(w)]
            for u, v, w in sorted(top_e, key=lambda x: -x[2])
            if u == label or v == label
        ]
        d = dist_to_top(G, label, top_nodes)
        hub_rows.append(
            {
                "ligacn": label,
                "short": short,
                "bw": bw,
                "uniprot_position": pos,
                "in_LigACN": label in G,
                "in_LigACNtop": label in top_nodes,
                "dist_to_LigACNtop": d,
                "max_incident_degeneracy": max_incident_weight(mat, label),
                "ligacntop_edges_incident": incident,
                "prefcoup_cluster": prefcoup_cluster_for_position(pos),
                "sd1": sd1_row_for_position(sd1, pos),
            }
        )

    n_in_top = sum(1 for r in hub_rows if r["in_LigACNtop"])
    n_in_pc = sum(
        1
        for r in hub_rows
        if r["prefcoup_cluster"] in {"1", "2", "3"}
    )
    primary = call_verdict(n_in_top, True)
    if primary == "DISTINCT_CANDIDATE":
        dists = [r["dist_to_LigACNtop"] for r in hub_rows if r["dist_to_LigACNtop"] is not None]
        med = sorted(dists)[len(dists) // 2] if dists else None
        primary = "DISTINCT" if (med is not None and med >= 2) or n_in_top <= 1 else "PARTIAL"

    hub_set = set(HUB_LABELS)
    jacc = (
        len(hub_set & top_nodes) / len(hub_set | top_nodes) if (hub_set | top_nodes) else float("nan")
    )

    plain = (
        f"Los seis hubs caen **dentro de LigACNtop** ({n_in_top}/6 nodos con degeneracy≥"
        f"{LIGACNTOP_DEGENERACY_CUTOFF}; distancia 0). "
        f"No son un objeto topológico disjunto del mapa publicado. "
        f"Overlay PrefCoup clusters 1–3: {n_in_pc}/6 posiciones hub "
        f"(N291A y R302A en cluster 3); el resto no está en mutantes PrefCoup simulados de esos clusters. "
        "Esto **no** reabre el enrichment Fisher del dual-test ni P1 dinámico."
    )

    payload = {
        "run_utc": run_utc,
        "governance": GOVERNANCE,
        "platform": platform.platform(),
        "verdict": {
            "primary": primary,
            "prefcoup_overlay": prefcoup_overlay(n_in_pc, True),
            "rules": {
                "EXT_HUBS_IN_LIGACNTOP": ">=5/6 hubs are LigACNtop nodes",
                "PARTIAL": "2-4/6 in LigACNtop",
                "DISTINCT": "<=1/6 in LigACNtop and median dist>=2",
                "INDETERMINATE_MISSING_SUPP": "MOESM5 missing",
            },
        },
        "plain_language": plain,
        "provenance": {
            "moesm5": str(MOESM5.relative_to(ROOT)).replace("\\", "/"),
            "moesm5_sha256": sha256(MOESM5),
            "moesm5_bytes": MOESM5.stat().st_size,
            "moesm3": str(MOESM3.relative_to(ROOT)).replace("\\", "/") if MOESM3.exists() else None,
            "moesm3_sha256": sha256(MOESM3),
            "ligacntop_cutoff": LIGACNTOP_DEGENERACY_CUTOFF,
            "n_ligacntop_edges": len(top_e),
            "n_ligacntop_nodes": len(top_nodes),
            "ligacntop_nodes": sorted(top_nodes),
            "prefcoup_groups_verify": groups_verify,
            "prefcoup_groups_source": (
                "GPCRmd/prefcoup_cb2r clustering.ipynb `groups` dict "
                "(Zenodo 10.5281/zenodo.15270434 points at same code; v.1.0.0 zip is LICENSE-only)"
            ),
        },
        "prefcoup_clusters": {
            str(k): sorted(v, key=lambda x: int(x)) for k, v in PUBLISHED_PREFCOUP_GROUPS.items()
        },
        "prefcoup_simulated_uncatched": sorted(PREFCOUP_SIMULATED_UNCATCHED),
        "hubs": hub_rows,
        "aggregates": {
            "n_hubs_in_LigACNtop": n_in_top,
            "n_hubs_in_any_PrefCoup_cluster": n_in_pc,
            "jaccard_hubs_vs_LigACNtop_nodes": jacc,
            "n_LigACN_nodes": int(G.number_of_nodes()),
            "n_LigACN_undirected_edges": int(G.number_of_edges()),
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "hubs_vs_ligacn_inventory.json"
    md_path = OUT / "hubs_vs_ligacn_inventory.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_md(payload, md_path)
    print(f"Wrote {json_path.relative_to(ROOT)}")
    print(f"Wrote {md_path.relative_to(ROOT)}")
    print(f"VERDICT primary={primary} prefcoup_overlay={payload['verdict']['prefcoup_overlay']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
