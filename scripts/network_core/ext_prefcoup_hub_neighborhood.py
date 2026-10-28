#!/usr/bin/env python3
"""EXTERNAL — PrefCoup cluster-2/3 SI contacts → hub neighborhood inventory.

Pre-reg: docs/synthesis/EXPERIMENT_EXT_PREFCOUP_HUB_NEIGHBORHOOD.md
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
SI_PDF = OUT / "_raw_downloads" / "41467_2025_60003_MOESM1_ESM.pdf"

# SI Note 1 — curated contact pairs (residue UniProt ints) with cluster + direction note
# direction: more_stable / less_stable in PrefCoup vs Coup (as stated in SI Note 1)
SI_NOTE1_CONTACTS = [
    # Cluster 2
    {"cluster": 2, "a": 258, "b": 288, "label": "W258–C288", "stability": "less_stable", "motifs": ["CWxP", "Na_site_adj"]},
    {"cluster": 2, "a": 258, "b": 291, "label": "W258–N291", "stability": "less_stable", "motifs": ["CWxP", "Na_site"]},
    {"cluster": 2, "a": 292, "b": 47, "label": "S292–S47", "stability": "more_stable", "motifs": ["Na_site"]},
    {"cluster": 2, "a": 131, "b": 127, "label": "R131–T127", "stability": "more_stable", "motifs": ["DRY"]},
    {"cluster": 2, "a": 40, "b": 87, "label": "C40–F87", "stability": "more_stable", "motifs": ["EC_TM7_1_2"]},
    {"cluster": 2, "a": 40, "b": 91, "label": "C40–F91", "stability": "less_stable", "motifs": ["EC_TM7_1_2"]},
    {"cluster": 2, "a": 285, "b": 44, "label": "S285–G44", "stability": "less_stable", "motifs": ["EC_TM7_1_2"]},
    # Cluster 3
    {"cluster": 3, "a": 295, "b": 51, "label": "N295–N51 (NPxxY)", "stability": "more_stable", "motifs": ["NPxxY"]},
    {"cluster": 3, "a": 295, "b": 80, "label": "NPxxY–D80", "stability": "more_stable", "motifs": ["NPxxY", "Na_site"]},
    {"cluster": 3, "a": 131, "b": 127, "label": "R131–T127", "stability": "more_stable", "motifs": ["DRY"]},
    {"cluster": 3, "a": 131, "b": 246, "label": "R131–T246", "stability": "more_stable", "motifs": ["DRY"]},
]

HUBS = {
    79: "ALA79",
    83: "ALA83",
    287: "LEU287",
    291: "ASN291",
    295: "ASN295",
    302: "ARG302",
}
PROXIES = {
    288: {"hub": 287, "hub_name": "LEU287", "note": "C288≈L287 adjacent Δseq=1; SI uses C288 7x41"},
    80: {"hub": 79, "hub_name": "ALA79", "note": "D80≈A79 adjacent Δseq=1; Na-site 2x50"},
}


def classify_res(resid: int) -> tuple[str, str | None]:
    if resid in HUBS:
        return "EXACT_HUB", HUBS[resid]
    if resid in PROXIES:
        return "PROXY_NEIGHBOR", PROXIES[resid]["hub_name"]
    return "NON_HUB", None


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not SI_PDF.exists():
        verdict = "EXT_PREFCOUP_HUB_NEIGHBORHOOD_INDETERMINATE"
        rows = []
    else:
        rows = []
        exact = proxy = 0
        for c in SI_NOTE1_CONTACTS:
            ca, na = classify_res(c["a"])
            cb, nb = classify_res(c["b"])
            if ca == "EXACT_HUB" or cb == "EXACT_HUB":
                exact += 1
                best = "EXACT_HUB"
            elif ca == "PROXY_NEIGHBOR" or cb == "PROXY_NEIGHBOR":
                proxy += 1
                best = "PROXY_NEIGHBOR"
            else:
                best = "NON_HUB"
            rows.append(
                {
                    **c,
                    "class_a": ca,
                    "hub_a": na,
                    "class_b": cb,
                    "hub_b": nb,
                    "best_class": best,
                }
            )
        if exact >= 1 and proxy >= 1:
            verdict = "EXT_PREFCOUP_HUB_NEIGHBORHOOD_OVERLAP"
        elif exact >= 1 or proxy >= 1:
            verdict = "EXT_PREFCOUP_HUB_NEIGHBORHOOD_PARTIAL"
        else:
            verdict = "EXT_PREFCOUP_HUB_NEIGHBORHOOD_ABSENT"

    # Also note cluster membership of hubs as mutants (prior inventory)
    mutant_overlay = {
        "cluster_2_mutants": [77, 117, 217],
        "cluster_3_mutants": [199, 205, 291, 302],
        "hubs_as_prefcoup_mutants": {"ASN291": 3, "ARG302": 3},
    }

    payload = {
        "experiment": "EXTERNAL_PREFCOUP_HUB_NEIGHBORHOOD",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_PREFCOUP_HUB_NEIGHBORHOOD.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "si_pdf_present": SI_PDF.exists(),
        "proxies": PROXIES,
        "hubs": HUBS,
        "contacts": rows,
        "counts": {
            "n_contacts": len(rows),
            "n_exact_hub_touching": sum(1 for r in rows if r.get("best_class") == "EXACT_HUB"),
            "n_proxy_touching": sum(1 for r in rows if r.get("best_class") == "PROXY_NEIGHBOR"),
        },
        "mutant_overlay": mutant_overlay,
        "governance": {
            "P1_REOPEN": False,
            "P2_REOPEN": False,
            "Gi_ENRICHMENT_REOPEN": False,
            "proxy_neq_identity": True,
        },
        "doi": "10.1038/s41467-025-60003-0",
    }
    (OUT / "ext_prefcoup_hub_neighborhood.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# EXTERNAL — PrefCoup cluster-2/3 → hub neighborhood",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_PREFCOUP_HUB_NEIGHBORHOOD.md`  ",
        "**Source:** Morales-Pastor SI Note 1 (MOESM1)",
        "",
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        "> N291 es hub exacto en contactos cluster-2 (W258–N291) y mutante PrefCoup cluster-3.  ",
        "> C288≈L287 y D80≈A79 son **proxies adyacentes** (no identidad).  ",
        "> N295 (hub) aparece en contactos NPxxY de cluster-3.  ",
        "> No reabre Fisher PrefCoup / P1 / P2.",
        "",
        "## Proxy map",
        "",
        "| SI residue | Hub proxy | Relation |",
        "|------------|-----------|----------|",
        "| N291 | ASN291 | exact |",
        "| C288 | LEU287 | adjacent Δseq=1 |",
        "| D80 | ALA79 | adjacent Δseq=1 (Na-site) |",
        "",
        "## Contact inventory (SI Note 1)",
        "",
        "| Cluster | Contact | Stability (PrefCoup) | Class | Hub link |",
        "|---------|---------|----------------------|-------|----------|",
    ]
    for r in rows:
        link = r.get("hub_a") or r.get("hub_b") or "—"
        lines.append(
            f"| {r['cluster']} | {r['label']} | {r['stability']} | **{r['best_class']}** | {link} |"
        )
    lines += [
        "",
        "## PrefCoup mutant overlay (prior)",
        "",
        "- Cluster 2 mutants: 77, 117, 217",
        "- Cluster 3 mutants: 199, 205, **291**, **302** (hubs N291, R302)",
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {verdict}",
        "PROXY_NEQ_IDENTITY: TRUE",
        "Gi_ENRICHMENT_REOPEN: FALSE",
        "P2_REOPEN: FALSE",
        "```",
        "",
        "---",
        "",
        "*Fin EXTERNAL PrefCoup hub neighborhood.*",
        "",
    ]
    (OUT / "ext_prefcoup_hub_neighborhood.md").write_text("\n".join(lines), encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
