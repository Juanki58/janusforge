#!/usr/bin/env python3
"""EXTERNAL — Ec21a PAM structural vs pharmacological assay checklist.

Pre-reg: docs/synthesis/EXPERIMENT_EXT_EC21A_PAM_CHECKLIST.md
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
CIF = ROOT / "data" / "external" / "cb2_landmark_expanded" / "9U7L.cif"

ROWS = [
    {
        "residue": "S268^6.58",
        "struct_role": "Portion II contact with Ec21a (Wang/9U7L)",
        "mutant_effect": "CP55 retained; PAM almost abolished (S268A)",
        "call": "AGREE",
        "source": "Wang Nat Commun 2026",
    },
    {
        "residue": "K278^7.32",
        "struct_role": "Portion II contact",
        "mutant_effect": "CP55 retained; PAM almost abolished (K278A)",
        "call": "AGREE",
        "source": "Wang 2026",
    },
    {
        "residue": "F183 ECL2",
        "struct_role": "Portion I/II hydrophobic enclosure",
        "mutant_effect": "F183A PAM loss; F183L partial rescue",
        "call": "AGREE",
        "source": "Wang 2026",
    },
    {
        "residue": "I186 ECL2",
        "struct_role": "Portion I enclosure",
        "mutant_effect": "I186A PAM loss",
        "call": "AGREE",
        "source": "Wang 2026",
    },
    {
        "residue": "P176 / P178 ECL2",
        "struct_role": "ECL2 flexibility / CB2 motif",
        "mutant_effect": "PAM abolished / strongly attenuated",
        "call": "AGREE",
        "source": "Wang 2026 / atlas",
    },
    {
        "residue": "E181 ECL2",
        "struct_role": "Map poorly resolved near portion II",
        "mutant_effect": "Slight PAM attenuation",
        "call": "PARTIAL",
        "source": "Wang 2026",
    },
    {
        "residue": "F106 / P184 / M22 / Y25",
        "struct_role": "Portion III pocket",
        "mutant_effect": "Mixed; some abolish cellular response (not PAM-selective)",
        "call": "PARTIAL",
        "source": "Wang 2026",
    },
    {
        "residue": "EC21a scaffold (cross-lab)",
        "struct_role": "Same chemotype discussed as PAM in Wang",
        "mutant_effect": "Qi/Niswender 2024: inverse agonist / assay-dependent at CB2 (PI hydrolysis / GIRK)",
        "call": "TENSION_ASSAY",
        "source": "DOI via PMID 39575892 / PMC11636628",
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    n_agree = sum(1 for r in ROWS if r["call"] == "AGREE")
    n_tension = sum(1 for r in ROWS if r["call"] == "TENSION_ASSAY")
    struct_ok = CIF.exists()
    if not struct_ok:
        verdict = "EXT_EC21A_PAM_INDETERMINATE"
    elif n_agree >= 4 and n_tension >= 1:
        verdict = "EXT_EC21A_PAM_STRUCT_ASSAY_PARTIAL"
    elif n_agree >= 4 and n_tension == 0:
        verdict = "EXT_EC21A_PAM_STRUCT_ASSAY_ALIGNED"
    else:
        verdict = "EXT_EC21A_PAM_STRUCT_ASSAY_TENSION"

    payload = {
        "experiment": "EXTERNAL_EC21A_PAM_CHECKLIST",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_EC21A_PAM_CHECKLIST.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "structure_9U7L_present": struct_ok,
        "rows": ROWS,
        "counts": {"n_AGREE": n_agree, "n_TENSION_ASSAY": n_tension},
        "governance": {
            "docking": "STOP",
            "P2_REOPEN": False,
            "Gi_FUNCTIONAL_CLAIM": False,
            "harmonize_Wang_vs_Qi": False,
        },
        "dois": [
            "10.1038/s41467-026-72923-6",
            "PMID:39575892",
        ],
    }
    (OUT / "ext_ec21a_pam_checklist.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# EXTERNAL — Ec21a PAM structural vs assay checklist",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_EC21A_PAM_CHECKLIST.md`",
        "",
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        "> Panel mutagénico Wang alinea plug estructural (S268/K278/F183/I186/P176–P178) con pérdida selectiva de PAM.  ",
        "> Qi/Niswender 2024 reporta farmacología **assay-dependent** (inverse agonist / mixed) — tensión entre labs/ensayos, **no** armonizada aquí.",
        "",
        "## Checklist",
        "",
        "| Residue | Struct role | Mutant / assay | Call |",
        "|---------|-------------|----------------|------|",
    ]
    for r in ROWS:
        lines.append(
            f"| {r['residue']} | {r['struct_role']} | {r['mutant_effect']} | **{r['call']}** |"
        )
    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {verdict}",
        "HARMONIZE_WANG_VS_QI: FALSE",
        "DOCKING: STOP",
        "P2_REOPEN: FALSE",
        "```",
        "",
        "---",
        "",
        "*Fin Ec21a PAM checklist.*",
        "",
    ]
    (OUT / "ext_ec21a_pam_checklist.md").write_text("\n".join(lines), encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
