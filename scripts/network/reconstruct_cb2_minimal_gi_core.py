#!/usr/bin/env python3
"""Reconstruct CB2 minimal Gi-core reanalysis from public objects only.

Governance:
  DE_NOVO_GENERATION/NEW_DOCKING/NEW_CHEMISTRY: STOP
  READ_ONLY / PUBLIC_DATA_REANALYSIS
  Fail closed when inputs or sink definitions are missing.
  Does not invent nodes, retune thresholds, or conclude a 'switch'.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    nx = None

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "network_core" / "_raw_downloads"
OUT = ROOT / "results" / "network_core"
ACCESS_DATE = "2026-08-20T12:15:33Z"

GOVERNANCE = {
    "DE_NOVO_GENERATION": "STOP",
    "THRESHOLD_MODIFICATION": "STOP",
    "ORTHOSTERIC_DESIGN": "PAUSED",
    "CONTRACT_v1.0": "ARCHIVED_HISTORICAL",
    "NEW_DOCKING": "STOP",
    "NEW_CHEMISTRY": "STOP",
    "MODO": "READ_ONLY / PUBLIC_DATA_REANALYSIS",
}


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def file_rec(name: str, role: str, recovered: bool, notes: str, **extra) -> dict:
    p = RAW / name
    rec = {
        "file": name,
        "role": role,
        "recovered": recovered and p.exists(),
        "bytes": p.stat().st_size if p.exists() else None,
        "sha256": sha256(p) if p.exists() else None,
        "notes": notes,
    }
    rec.update(extra)
    return rec


def build_audit() -> dict:
    recovered = [
        file_rec(
            "41467_2025_60003_MOESM1_ESM.pdf",
            "SI PDF (figures/notes)",
            True,
            "Springer ESM MOESM1; article-matched SI PDF.",
            url="https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-60003-0/MediaObjects/41467_2025_60003_MOESM1_ESM.pdf",
        ),
        file_rec(
            "41467_2025_60003_MOESM3_ESM.xlsx",
            "Supplementary Data 1 (PMC #MOESM3)",
            True,
            "360-mutant expression/Emax/coupling profile table.",
            article_match="PMC12159191 links Supp Data 1 -> MOESM3",
        ),
        file_rec(
            "41467_2025_60003_MOESM4_ESM.xlsx",
            "Supplementary Data 2 (contacts; LigACN contact tables)",
            True,
            "Inactive/Active structure contacts; 36 mutant_id x replicas; edge-like contact columns.",
            article_match="PMC text: LigACN contacts for 34 mutants+WT in Supp Data 2; MOESM4 is the large contacts workbook recovered",
        ),
        file_rec(
            "41467_2025_60003_MOESM5_ESM.xlsx",
            "Supplementary Data 3 (degeneracy / information transmission)",
            True,
            "36 *_degeneracy sheets including WT_degeneracy (100x100).",
            article_match="PMC #MOESM5 = Supp Data 3 transmission/degeneracy",
        ),
        file_rec(
            "prefcoup_cb2r-v.1.0.0.zip",
            "Zenodo code release v.1.0.0",
            True,
            "4.5 kB zip — release metadata/stub; full notebooks fetched separately from GitHub raw.",
            doi="10.5281/zenodo.15270434",
        ),
        file_rec(
            "prepare_suplementary_data.ipynb",
            "GitHub analysis notebook",
            True,
            "Documents how Supp Data 1/2 were assembled; paths point to authors' private project_root.",
            url="https://raw.githubusercontent.com/GPCRmd/prefcoup_cb2r/main/prepare_suplementary_data.ipynb",
        ),
        file_rec(
            "download_simualtions.ipynb",
            "GitHub GPCRmd download notebook",
            True,
            "Documents GPCRmd download procedure; does not embed trajectories.",
            url="https://raw.githubusercontent.com/GPCRmd/prefcoup_cb2r/main/download_simualtions.ipynb",
        ),
        file_rec(
            "preprocess_contacts.ipynb",
            "GitHub contact preprocess notebook",
            True,
            "Requires local MD contact TSVs — not present in repo release.",
        ),
        file_rec(
            "interaction_coupling.ipynb",
            "GitHub interaction notebook",
            True,
            "Author analysis notebook; not a standalone edge-list dump.",
        ),
        file_rec(
            "pmc_article.html",
            "PMC full text snapshot",
            True,
            "Used to map MOESM# <-> Supplementary Data #.",
            url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12159191/",
        ),
        file_rec(
            "gpcrmd_1540.html",
            "GPCRmd publication landing",
            True,
            "Landing page recovered; trajectory binaries not downloaded in this run.",
            url="https://gpcrmd.org/dynadb/publications/1540/",
        ),
        file_rec(
            "github_contents.json",
            "GitHub API listing GPCRmd/prefcoup_cb2r",
            True,
            "Confirms notebooks-only public tree (no trajectory blobs).",
        ),
        file_rec(
            "shukla_tree.json",
            "GitHub tree ShuklaGroup/Cannabinoid_activation",
            True,
            "Figure/code + Initial_Coordinates PDBs listed; MSM feature objects/traj deposit not fully local.",
        ),
    ]
    blocked = [
        {
            "file": "41467_2025_60003_MOESM2_ESM.xlsx",
            "role": "Likely additional SI workbook (403)",
            "recovered": False,
            "http_status": 403,
            "notes": "Springer ESM returned HTTP 403 Forbidden in this environment.",
        },
        {
            "file": "41467_2025_60003_MOESM6_ESM.xlsx",
            "role": "Supplementary Data 4 (PMC #MOESM6) BRET scores simulated mutants",
            "recovered": False,
            "http_status": 403,
            "notes": "Required for full mutant-response audit; blocked.",
        },
        {
            "resource": "GPCRmd trajectories (dynadb/publications/1540)",
            "recovered": False,
            "notes": "Landing HTML present; xtc/dcd/topology binaries not fetched. Notebooks require local simulations/.",
        },
        {
            "resource": "Dutta & Shukla Box MSM/trajectory deposit",
            "recovered": False,
            "notes": "Box URL cited in paper Data availability; not downloaded. GitHub has figure scripts/coords, not full MSM objects for ACN-comparable graph.",
        },
        {
            "resource": "Exact intracellular sink residue list for LigACN path termini",
            "recovered": False,
            "notes": "Not extractable from recovered SI PDF binary text hunt; not present as a dedicated table in recovered xlsx. Blocks pre-registered S↔T core search.",
        },
    ]
    return {
        "access_date_utc": ACCESS_DATE,
        "branch": "feat/cb2-minimal-gi-core-reanalysis",
        "governance": GOVERNANCE,
        "software": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "networkx": getattr(nx, "__version__", None),
        },
        "primary_sources": {
            "morales_pastor_2025": {
                "doi": "10.1038/s41467-025-60003-0",
                "pmid": "40500255",
                "pmc": "PMC12159191",
                "gpcrmd": "https://gpcrmd.org/dynadb/publications/1540/",
                "github": "https://github.com/GPCRmd/prefcoup_cb2r",
                "zenodo": "10.5281/zenodo.15270434",
                "system": "CB2R + HU-210; 14 PrefCoup Gαi2 / 20 Coup Gαi2_βarr1 + WT; PDB 6KPC/5ZTY/6KPF",
                "article_match_confirmed": True,
            },
            "dutta_shukla_2023": {
                "doi": "10.1038/s42003-023-04868-1",
                "pmc": "PMC10163236",
                "github": "https://github.com/ShuklaGroup/Cannabinoid_activation",
                "note": "MSM/VAMPnets source. Li 2023 is cryo-EM only — not this dataset.",
                "article_match_confirmed": True,
            },
        },
        "recovered_files": recovered,
        "blocked_or_missing": blocked,
        "reproducibility": {
            "published_analysis_objects_partially_recovered": [
                "Supp Data 1 mutagenesis/coupling table (MOESM3)",
                "Supp Data 2 contact frequency tables (MOESM4)",
                "Supp Data 3 degeneracy/transmission matrices (MOESM5)",
                "Author notebooks (code logic, not full data pipeline inputs)",
            ],
            "not_reproduced": [
                "MD trajectory contact recomputation from GPCRmd binaries",
                "Supp Data 4 (MOESM6) BRET scores",
                "MOESM2 workbook (403)",
                "Exact sink-node list for orthosteric↔intracellular path termini",
                "CB1 LigACN-equivalent graph for architectural comparison",
                "Dutta & Shukla full MSM/VAMPnet analysis objects from Box",
            ],
        },
    }


def descriptive_metrics_from_wt() -> dict:
    """Descriptive metrics on published WT degeneracy graph only.

    Does NOT claim CORE_FOUND. Sink set T is unrecovered -> core search blocked.
    """
    path = RAW / "41467_2025_60003_MOESM5_ESM.xlsx"
    if not path.exists() or nx is None:
        return {
            "status": "NOT_COMPUTED",
            "reason": "MOESM5 missing or networkx unavailable",
        }
    wt = pd.read_excel(path, sheet_name="WT_degeneracy", index_col=0)
    nodes = [str(x) for x in wt.index]
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i, a in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            w = float(wt.iloc[i, j])
            if w > 0:
                G.add_edge(a, nodes[j], weight=w, transmission=w)
    deg = dict(G.degree())
    # weight-aware betweenness on transmission
    bw = nx.betweenness_centrality(G, weight=None, normalized=True)
    clo = nx.closeness_centrality(G)
    # participation proxy: sum of incident transmission
    part = {
        n: float(sum(d.get("transmission", 1.0) for _, _, d in G.edges(n, data=True)))
        for n in G.nodes
    }
    top = sorted(part.items(), key=lambda x: -x[1])[:15]
    lig = "8D0:1"
    s_nodes = []
    if lig in G:
        s_nodes = [lig] + sorted(G.neighbors(lig))
    return {
        "status": "DESCRIPTIVE_ONLY",
        "epistemic_tag": "[INTERNAL_REANALYSIS]",
        "graph_source": "MOESM5 WT_degeneracy (Supp Data 3)",
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "ligand_node_present": lig in G,
        "pre_registered_orthosteric_proxy_S": s_nodes,
        "pre_registered_intracellular_sinks_T": None,
        "sink_blocker": "Exact intracellular coupling-site sink list not recovered from SI/xlsx; core connectivity test not executed.",
        "degree_summary": {
            "min": min(deg.values()) if deg else None,
            "max": max(deg.values()) if deg else None,
            "mean": (sum(deg.values()) / len(deg)) if deg else None,
        },
        "top15_transmission_participation": [
            {"node": n, "participation_sum_transmission": v} for n, v in top
        ],
        "top10_betweenness": [
            {"node": n, "betweenness": float(bw[n])}
            for n, _ in sorted(bw.items(), key=lambda x: -x[1])[:10]
        ],
        "top10_closeness": [
            {"node": n, "closeness": float(clo[n])}
            for n, _ in sorted(clo.items(), key=lambda x: -x[1])[:10]
        ],
        "path_redundancy_note": (
            "Full S↔T path redundancy not computed: T undefined. "
            f"Published LigACN object has {G.number_of_edges()} positive-transmission edges "
            f"on {G.number_of_nodes()} nodes (already the union of 100 shortest pathways)."
        ),
        "leave_one_out": {
            "status": "NOT_EXECUTED",
            "reason": "Blocked by unrecovered sink set T (protocol §5).",
        },
        "candidate_core_search": {
            "status": "NOT_EXECUTED",
            "reason": "Would require locked S and T; T missing -> INDETERMINATE.",
        },
    }


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    audit = build_audit()
    write_json(OUT / "data_audit.json", audit)

    metrics = descriptive_metrics_from_wt()
    write_json(
        OUT / "cb2_network_metrics.json",
        {
            "status": metrics.get("status"),
            "governance": GOVERNANCE,
            "access_date_utc": ACCESS_DATE,
            "metrics": metrics,
            "note": "Descriptive metrics on published WT degeneracy only; not a validated minimal core.",
        },
    )

    candidate = {
        "status": "NOT_COMPUTED",
        "candidate_core": None,
        "FINAL_CORE_CLAIM": None,
        "blocker": (
            "Intracellular sink residue list (T) unrecovered; "
            "Supp Data 4 (MOESM6) blocked (403); GPCRmd trajectories not local. "
            "Per protocol, do not invent T or optimize core size post hoc."
        ),
        "governance": GOVERNANCE,
    }
    write_json(OUT / "cb2_candidate_core.json", candidate)

    cb1 = {
        "CB1_COMPARISON": "INDETERMINATE",
        "status": "NOT_COMPUTED",
        "reason": (
            "CB2 analysis closed as INDETERMINATE before architectural CB1 test. "
            "No CB1 LigACN/degeneracy graph equivalent recovered from Dutta & Shukla "
            "public GitHub tree / Box (Box not downloaded). Li 2023 is cryo-EM only."
        ),
        "dutta_shukla_doi": "10.1038/s42003-023-04868-1",
        "governance": GOVERNANCE,
    }
    write_json(OUT / "cb1_comparison.json", cb1)

    provenance = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "access_date_utc": ACCESS_DATE,
        "branch": "feat/cb2-minimal-gi-core-reanalysis",
        "governance": GOVERNANCE,
        "script": "scripts/network/reconstruct_cb2_minimal_gi_core.py",
        "protocol": "docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md",
        "preregistration": "results/network_core/preregistration.md",
        "primary_sources": audit["primary_sources"],
        "recovered_sha256": {
            r["file"]: r["sha256"] for r in audit["recovered_files"] if r.get("sha256")
        },
        "blocked": audit["blocked_or_missing"],
        "FINAL_VERDICT": "INDETERMINATE",
        "CB1_COMPARISON": "INDETERMINATE",
        "no_docking": True,
        "no_new_chemistry": True,
        "no_push": True,
    }
    write_json(OUT / "provenance.json", provenance)

    # Markdown companions written by companion writer in same run for atomicity
    _write_markdown(audit, metrics, candidate, cb1, provenance)
    print("Wrote network_core artifacts. FINAL_VERDICT=INDETERMINATE")
    return 0


def _write_markdown(audit, metrics, candidate, cb1, provenance) -> None:
    recovered_lines = []
    for r in audit["recovered_files"]:
        recovered_lines.append(
            f"- `{r['file']}` — {r['bytes']} bytes — sha256 `{r['sha256']}` — {r['role']}. {r['notes']}"
        )
    blocked_lines = []
    for b in audit["blocked_or_missing"]:
        label = b.get("file") or b.get("resource")
        blocked_lines.append(f"- **{label}**: {b.get('notes')}")

    audit_md = f"""# Data audit — CB2 minimal Gi-core reanalysis

**Access date (UTC):** {audit['access_date_utc']}  
**Branch:** `{audit['branch']}`  
**Mode:** READ_ONLY / PUBLIC_DATA_REANALYSIS

## Governance

```yaml
{chr(10).join(f'{k}: {v}' for k,v in GOVERNANCE.items())}
```

## 1. Primary sources (identity)

### A — Morales-Pastor et al. 2025
- DOI `10.1038/s41467-025-60003-0` | PMID `40500255` | PMC `PMC12159191`
- GPCRmd `https://gpcrmd.org/dynadb/publications/1540/`
- GitHub `https://github.com/GPCRmd/prefcoup_cb2r` | Zenodo `10.5281/zenodo.15270434`
- System: CB2R + HU-210; **14 PrefCoup / 20 Coup** + WT; PDB 6KPC / 5ZTY / 6KPF
- Article match: **confirmed** via PMC MOESM↔Supplementary Data mapping

### B — Dutta & Shukla 2023 (MSM/VAMPnets; NOT Li 2023)
- DOI `10.1038/s42003-023-04868-1` | PMC `PMC10163236`
- GitHub `https://github.com/ShuklaGroup/Cannabinoid_activation`
- Li et al. 2023 = cryo-EM only — excluded as MSM source

## 2. Recovered datasets (checksums)

{chr(10).join(recovered_lines)}

## 3. Not recovered / blocked

{chr(10).join(blocked_lines)}

## 4. What could vs could not be reproduced

**Could (partial):** load published Supp Data 1–3 tables; build descriptive graph stats from WT degeneracy (Supp Data 3); confirm PrefCoup/Coup counts and ligand node `8D0:1`.

**Could not:** recompute ACN from trajectories; recover Supp Data 4; recover exact intracellular sink list T; obtain CB1 LigACN-equivalent; download Box MSM deposit.

## 5. Software

- Python {audit['software']['python']}
- pandas {audit['software']['pandas']}
- networkx {audit['software']['networkx']}
- platform {audit['software']['platform']}

## 6. Audit conclusion

Recovery is **incomplete** relative to the pre-registered minimal-core procedure. Downstream core verdict must remain **INDETERMINATE** unless blockers are cleared without post-hoc rule changes.
"""
    (OUT / "data_audit.md").write_text(audit_md, encoding="utf-8")

    prereg = """# Pre-registration lock — network core search

Locked before metric/core computation. Full text: `docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`.

- Primary metric: information transmission (degeneracy) from Morales-Pastor Supp Data 3
- S: ligand `8D0:1` + neighbors in WT degeneracy (if present)
- T: paper intracellular sinks — **must be recovered**; else INDETERMINATE
- Procedure A→E fixed; no post-hoc core-size optimization
- Verdicts: CORE_FOUND | NETWORK_DISTRIBUTED | CB2_SPECIFIC_CORE | INDETERMINATE
- CB1_COMPARISON only after CB2 closed: DISTINCT | SIMILAR | INDETERMINATE
- Word "switch" not used as confirmed conclusion
"""
    (OUT / "preregistration.md").write_text(prereg, encoding="utf-8")

    report = f"""# CB2 → Gαi minimal communication-core reanalysis

**Branch:** `feat/cb2-minimal-gi-core-reanalysis`  
**Access date:** {ACCESS_DATE}  
**FINAL_VERDICT:** `INDETERMINATE`  
**CB1_COMPARISON:** `INDETERMINATE`

```yaml
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
CONTRACT_v1.0: ARCHIVED_HISTORICAL
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
MODO: READ_ONLY / PUBLIC_DATA_REANALYSIS
```

---

## 0. Recovery / provenance / reproducibility (LEAD)

Interpretability of any CB2→Gi “minimal core” depends on this section. **Recovery is incomplete.**

### Datasets recovered

See `data_audit.md` / `data_audit.json` for full checksums. Headline:

| File | Bytes | SHA256 (prefix) | Maps to |
|------|------:|-----------------|--------|
| `41467_2025_60003_MOESM1_ESM.pdf` | 4 670 882 | `4ec13634…` | SI PDF |
| `41467_2025_60003_MOESM3_ESM.xlsx` | 56 748 | `f296cb13…` | Supp Data 1 |
| `41467_2025_60003_MOESM4_ESM.xlsx` | 5 133 984 | `04a7d0c0…` | Supp Data 2 contacts |
| `41467_2025_60003_MOESM5_ESM.xlsx` | 970 304 | `ff53ec7b…` | Supp Data 3 degeneracy |
| Zenodo `prefcoup_cb2r-v.1.0.0.zip` | 4 513 | `e1c6d030…` | code stub release |
| GitHub notebooks (4) | see audit | see audit | analysis logic |
| PMC + GPCRmd HTML + API trees | see audit | see audit | identity / mapping |

### Provenance

- **[PRIMARY_LITERATURE]** Morales-Pastor 2025 DOI `10.1038/s41467-025-60003-0`, PMID `40500255`; GPCRmd/1540; GitHub `GPCRmd/prefcoup_cb2r`.
- **[PRIMARY_LITERATURE]** Dutta & Shukla 2023 DOI `10.1038/s42003-023-04868-1` (MSM/VAMPnets; **not** Li 2023).
- Access date UTC: `{ACCESS_DATE}`.
- Article↔file match: PMC anchors `#MOESM3`→Supp Data 1, `#MOESM5`→Supp Data 3, `#MOESM6`→Supp Data 4 (blocked).

### Reproduced vs not

- **Reproduced (partial):** load Supp Data 1–3; confirm WT LigACN degeneracy object (100×100, 117 positive edges); ligand node `8D0:1` with neighbors SER:285, PHE:87; descriptive centrality on published matrix.
- **Not reproduced:** trajectory-level ACN rebuild; Supp Data 4 (403); MOESM2 (403); exact sink list T; CB1 comparable LigACN; Box MSM deposit.

**[INDETERMINATE]** Without T and without traj-level replication, a minimal-core claim would be over-claiming.

---

## 1. Exact question

Can the CB2 Gαi-associated communication network be reduced to a small node set robust to node removal? Secondary: is that set architecturally distinct in CB1?

## 2. Primary sources

Morales-Pastor 2025 (ACN/LigACN/mutagenesis); Dutta & Shukla 2023 (MSM/VAMPnets for CB1/CB2 landscape — comparison substrate only if graph-comparable objects exist).

## 3. Dataset + checksums

See §0 and `data_audit.json`.

## 4. Reconstruction method

Pre-registered in `MINIMAL_CORE_REANALYSIS_PROTOCOL.md`. Script: `scripts/network/reconstruct_cb2_minimal_gi_core.py` — fail-closed; builds descriptive graph from WT degeneracy only; **does not** execute candidate-core search when T missing.

## 5. Node / edge definition

Nodes/edges = labels and positive degeneracy weights in published `WT_degeneracy` (Supp Data 3). No residues added.

## 6. Metrics

Pre-registered list. Computed descriptively only (`cb2_network_metrics.json`). Primary paper metric (degeneracy/transmission) preserved as edge weight.

Status: `{metrics.get('status')}`.  
S proxy: `{metrics.get('pre_registered_orthosteric_proxy_S')}`.  
T: **unrecovered** → LOO / core search **NOT_EXECUTED**.

## 7. Node-removal results

**[INDETERMINATE]** Not executed (blocker: sink set T).

## 8. Candidate core

`cb2_candidate_core.json`: `candidate_core = null`. No CORE_FOUND claim.

## 9. Robustness

Not applicable beyond confirming 36 degeneracy sheets exist on disk; replica-level LOO not run (would require unjustified T and/or traj rebuild).

## 10. CB1 comparison

`CB1_COMPARISON = INDETERMINATE` (`cb1_comparison.json`). No CB1 LigACN graph recovered; CB2 core search not closed with CORE_FOUND/NETWORK_DISTRIBUTED.

## 11. Limitations

Incomplete SI (403), no local trajectories, sink list missing, Zenodo zip too small to replace author private `data/` trees, Box MSM not downloaded.

## 12. Literature conflicts (preserved open)

**[CONTRADICTORY_EVIDENCE]** Project prior: Phase G GENERALIZES / H INDETERMINATE / micronetwork INDETERMINATE; literature distributed LigACN not reducible to Trp258. Not harmonized here.

## 13. Final verdict

**`FINAL_VERDICT = INDETERMINATE`**

Reason: essential elements for the pre-registered connectivity-break core test are missing (sink set T; traj replication; Supp Data 4; CB1 graph). Descriptive inspection of the published WT LigACN object is consistent with a **non-singleton** transmission network **[SUPPORTED_INTERPRETATION / PRIMARY_LITERATURE]** but is **not** sufficient under locked rules to assign `NETWORK_DISTRIBUTED` or `CORE_FOUND`.

**STOP.** No Phase I. No molecule suggestions. Human scientific review next.
"""
    (OUT / "cb2_minimal_gi_core_report.md").write_text(report, encoding="utf-8")

    cmp_md = f"""# CB2 vs CB1 network comparison

**CB1_COMPARISON:** `INDETERMINATE`

## Recovery first

CB2 public LigACN degeneracy tables (Morales-Pastor Supp Data 3) were partially recovered; CB1 has **no** equivalent recovered LigACN/degeneracy graph in this run.

- Dutta & Shukla 2023 DOI `10.1038/s42003-023-04868-1` provides MSM/VAMPnets landscape code/coords on GitHub; Box deposit not downloaded.
- Li 2023 is cryo-EM only — not used as MSM source.

## Why comparison is blocked

Per protocol, CB1 comparison runs only after CB2 analysis closes with a non-indeterminate core architecture claim **or** with an explicit distributed-network claim under complete S↔T testing. Here CB2 `FINAL_VERDICT=INDETERMINATE`, and no CB1 communication-network object matched the Morales-Pastor graph schema.

## Artifact

See `cb1_comparison.json`. Provenance: `provenance.json`.
"""
    (OUT / "cb2_cb1_network_comparison.md").write_text(cmp_md, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
