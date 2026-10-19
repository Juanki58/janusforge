#!/usr/bin/env python3
"""EXTERNAL — DEER candidate design DOC ONLY (no invented distances).

Pre-reg: docs/synthesis/EXPERIMENT_EXT_DEER_CANDIDATES.md
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
EPR_JSON = OUT / "ext_epr_nmr_anchors.json"

PAIRS = [
    {
        "id": "D1",
        "site_a": "ICL3 center (~G225C class; Yeliseev)",
        "site_b": "ICL3 edge / TM6 IC",
        "discriminates": "Local ICL3 mobility vs broader IC opening",
        "distance_A": None,
        "status": "DESIGN_ONLY",
    },
    {
        "id": "D2",
        "site_a": "TM3 IC near R131 DRY",
        "site_b": "TM6 IC near T246",
        "discriminates": "Activation opening axis (Phase F/G TM3–TM6 IC)",
        "distance_A": None,
        "status": "DESIGN_ONLY",
    },
    {
        "id": "D3",
        "site_a": "M293 / TM7 hub corridor (N291–N295)",
        "site_b": "TM2 A79–A83 neighborhood",
        "discriminates": "Static hub corridor persistence vs state-route",
        "distance_A": None,
        "status": "DESIGN_ONLY",
    },
    {
        "id": "D4",
        "site_a": "A270C TM6 EC tip (Yeliseev)",
        "site_b": "ECL2 / vestibule",
        "discriminates": "EC tip mobility; Phase F/G had NO_PRIOR_PRED for A270",
        "distance_A": None,
        "status": "DESIGN_ONLY",
    },
    {
        "id": "D5",
        "site_a": "N291 or N295",
        "site_b": "R302 H8",
        "discriminates": "TM7–H8 bottleneck neighborhood (static topology)",
        "distance_A": None,
        "status": "DESIGN_ONLY",
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    epr_ok = EPR_JSON.exists()
    if len(PAIRS) >= 4 and epr_ok:
        verdict = "EXT_DEER_CANDIDATES_DESIGNED_NO_DISTANCES"
    elif len(PAIRS) >= 4:
        verdict = "EXT_DEER_CANDIDATES_DESIGNED_NO_DISTANCES"
    else:
        verdict = "EXT_DEER_CANDIDATES_INDETERMINATE"

    # Hard assert: no distances
    assert all(p["distance_A"] is None for p in PAIRS)

    payload = {
        "experiment": "EXTERNAL_DEER_CANDIDATES",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_DEER_CANDIDATES.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "DEER_CB2_DISTANCE_MAP": "ABSENT",
        "restraints_added": False,
        "pairs": PAIRS,
        "governance": {
            "invented_distances": False,
            "P2_REOPEN": False,
            "MD_run": False,
            "note": "Design doc only; conditional on future own sampling",
        },
        "refs": [
            "10.1016/j.bbamem.2021.183603",
            "10.1021/acsomega.3c04681",
            "results/network_core/ext_epr_nmr_anchors.md",
        ],
    }
    (OUT / "ext_deer_candidates.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# EXTERNAL — DEER candidate design (DOC ONLY)",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_DEER_CANDIDATES.md`",
        "",
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        "> **DEER_CB2 = ABSENT.** No distances invented. No restraints added.  ",
        "> Pairs are discrimination *designs* for a future experiment — not measurements.",
        "",
        "## Candidate pairs",
        "",
        "| ID | Site A | Site B | Discriminates | Distance |",
        "|----|--------|--------|---------------|----------|",
    ]
    for p in PAIRS:
        lines.append(
            f"| {p['id']} | {p['site_a']} | {p['site_b']} | {p['discriminates']} | **NOT_INVENTED** |"
        )
    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {verdict}",
        "DEER_CB2_DISTANCE_MAP: ABSENT",
        "RESTRAINTS_ADDED: FALSE",
        "P2_REOPEN: FALSE",
        "```",
        "",
        "---",
        "",
        "*Fin DEER design doc.*",
        "",
    ]
    (OUT / "ext_deer_candidates.md").write_text("\n".join(lines), encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
