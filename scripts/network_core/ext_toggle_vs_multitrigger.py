#!/usr/bin/env python3
"""EXTERNAL — Toggle-continuo (Ganzoni) vs multi-trigger PrefCoup (Morales SI Note 1).

Pre-reg: docs/synthesis/EXPERIMENT_EXT_TOGGLE_VS_MULTITRIGGER.md
Lit discrimination table only. No Gi claim; no P2 reopen.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
SI_PDF = ROOT / "results" / "network_core" / "_raw_downloads" / "41467_2025_60003_MOESM1_ESM.pdf"

ROWS = [
    {
        "id": 1,
        "prediction": "PrefCoup_Gαi2 arises from mutations that need not hit W258",
        "toggle_continuum": "Neutral/underspecified — continuum is ligand–W258 efficacy, not PrefCoup mutant census",
        "multi_trigger": "SUPPORTED — clusters 1–3 mutate sites across TM3/5/7/ECL2; W258 not required as mutant site",
        "relation": "LEVEL_OK",
        "anchor": "Morales SI Table 1 / clusters; Ganzoni scaffold edits",
    },
    {
        "id": 2,
        "prediction": "W258 partner-contact stability changes in some PrefCoup clusters only",
        "toggle_continuum": "Would predict W258 contacts always central if toggle were unique PrefCoup gate",
        "multi_trigger": "SUPPORTED — SI Note 1: cluster1 W258–L195↑; cluster2 W258–C288/N291↓; cluster3 CWxP not highlighted",
        "relation": "CONFLICT",
        "anchor": "Morales SI Note 1 (MOESM1)",
    },
    {
        "id": 3,
        "prediction": "Single-position HU-308 edits retune efficacy continuum via W258 without unique PrefCoup path claim",
        "toggle_continuum": "SUPPORTED — Ganzoni / Kosar",
        "multi_trigger": "Compatible — does not assert single PrefCoup trigger",
        "relation": "LEVEL_OK",
        "anchor": "DOI 10.1039/D6SC00062B; 10.1021/acscentsci.3c01461",
    },
    {
        "id": 4,
        "prediction": "Na-site / NPxxY / DRY appear as PrefCoup features independent of CWxP in ≥1 cluster",
        "toggle_continuum": "False if toggle-only model of PrefCoup",
        "multi_trigger": "SUPPORTED — cluster3 NPxxY+Na+DRY; cluster2 Na+DRY+EC TM7/1/2; CWxP not universal",
        "relation": "CONFLICT",
        "anchor": "Morales SI Note 1 + Fig. 5E summary",
    },
    {
        "id": 5,
        "prediction": "Operational chain ligando → Trp258 → Gαi2 is sufficient",
        "toggle_continuum": "Tempting over-read of Ganzoni — NOT claimed as Gi-sufficient by authors as unique path",
        "multi_trigger": "REJECTED — multiple triggers → same PrefCoup; LigACN distributed",
        "relation": "CONFLICT",
        "anchor": "Morales title/abstract; project RESEARCH_STATE prohibition",
    },
]


def verdict(rows: list[dict]) -> str:
    if not SI_PDF.exists():
        return "EXT_TOGGLE_VS_MULTITRIGGER_INDETERMINATE"
    n_conflict = sum(1 for r in rows if r["relation"] == "CONFLICT")
    n_level = sum(1 for r in rows if r["relation"] == "LEVEL_OK")
    if n_conflict >= 3 and n_level >= 1:
        return "EXT_TOGGLE_VS_MULTITRIGGER_LEVEL_DISTINCT"
    if n_conflict >= 3:
        return "EXT_TOGGLE_VS_MULTITRIGGER_DISCRIMINABLE"
    return "EXT_TOGGLE_VS_MULTITRIGGER_INDETERMINATE"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    v = verdict(ROWS)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "experiment": "EXTERNAL_TOGGLE_VS_MULTITRIGGER",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_TOGGLE_VS_MULTITRIGGER.md",
        "run_utc": run_utc,
        "verdict": v,
        "si_pdf_present": SI_PDF.exists(),
        "rows": ROWS,
        "governance": {
            "P2_REOPEN": False,
            "Gi_FUNCTIONAL_CLAIM": False,
            "docking": "STOP",
            "note": "Level-distinct: pocket efficacy continuum vs PrefCoup multi-entry — both lit-true; chain→Gi forbidden",
        },
        "dois": [
            "10.1039/D6SC00062B",
            "10.1021/acscentsci.3c01461",
            "10.1038/s41467-025-60003-0",
        ],
    }
    (OUT / "ext_toggle_vs_multitrigger.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# EXTERNAL — Toggle-continuo vs PrefCoup multi-trigger",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_TOGGLE_VS_MULTITRIGGER.md`  ",
        "**Mode:** literature discrimination table — no MD.",
        "",
        "## Verdict",
        "",
        f"**`{v}`**",
        "",
        "> Ganzoni/Kosar: continuo de eficacia en el bolsillo vía Trp258^6.48.  ",
        "> Morales SI Note 1: PrefCoup_Gαi2 por **varios** triggers (CWxP no universal entre clusters).  ",
        "> Predicción `ligando → Trp258 → Gαi2` suficiente = **rechazada** como modelo operativo.  ",
        "> No reabre P2; no claim Gi del proyecto.",
        "",
        "## Discrimination table",
        "",
        "| # | Prediction | Toggle-continuum | Multi-trigger PrefCoup | Relation |",
        "|---|------------|------------------|------------------------|----------|",
    ]
    for r in ROWS:
        lines.append(
            f"| {r['id']} | {r['prediction']} | {r['toggle_continuum']} | {r['multi_trigger']} | **{r['relation']}** |"
        )
    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {v}",
        "P2_REOPEN: FALSE",
        "Gi_FUNCTIONAL_CLAIM: FALSE",
        "DOCKING: STOP",
        "```",
        "",
        "## References",
        "",
        "1. Ganzoni et al. — DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)",
        "2. Kosar et al. — DOI [10.1021/acscentsci.3c01461](https://doi.org/10.1021/acscentsci.3c01461)",
        "3. Morales-Pastor et al. + SI Note 1 — DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)",
        "",
        "---",
        "",
        "*Fin EXTERNAL toggle vs multi-trigger.*",
        "",
    ]
    (OUT / "ext_toggle_vs_multitrigger.md").write_text("\n".join(lines), encoding="utf-8")
    print(v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
