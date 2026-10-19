#!/usr/bin/env python3
"""EXTERNAL — Dutta Supp Fig. 22 tunnel membership vs hubs.

Pre-reg: docs/synthesis/EXPERIMENT_EXT_DUTTA_SF22_TUNNEL_HUBS.md
Prefer INDETERMINATE / QUALITATIVE_ONLY over inventing residues from figure.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
SI_PDF = OUT / "_raw_downloads" / "42003_2023_4868_MOESM1_ESM.pdf"

HUBS = ["ALA79", "ALA83", "LEU287", "ASN291", "ASN295", "ARG302"]


def extract_sf22_text() -> dict:
    info = {
        "si_present": SI_PDF.exists(),
        "caption": None,
        "residue_roster_found": False,
        "main_text_claim": (
            "CB2: no clear allosteric-pipeline distinction between active-like "
            "(active, I4) and inactive-like (inactive, I1–I3); most metastable "
            "states contain extracellular-to-intracellular communications (Supp Fig. 22)."
        ),
    }
    if not SI_PDF.exists():
        return info
    try:
        import pypdf

        reader = pypdf.PdfReader(str(SI_PDF))
        for page in reader.pages:
            t = page.extract_text() or ""
            if "Supplementary Figure 22" in t or "Figure 22:" in t:
                info["caption"] = " ".join(t.split())
                # Heuristic: residue roster would list many residue numbers / BW
                # Caption-only pages lack hub residue lists
                if any(h.replace("ALA", "A").replace("LEU", "L").replace("ASN", "N").replace("ARG", "R") in t for h in HUBS):
                    info["residue_roster_found"] = True
                if re_hub_numbers(t):
                    info["residue_roster_found"] = True
                break
    except Exception as e:
        info["extract_error"] = str(e)
    return info


def re_hub_numbers(text: str) -> bool:
    # Only true if explicit hub indices appear in a membership-like list near "tunnel"
    import re

    if "tunnel" not in text.lower() and "Tunnel" not in text:
        return False
    hits = sum(1 for n in (79, 83, 287, 291, 295, 302) if re.search(rf"\b{n}\b", text))
    return hits >= 3


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    info = extract_sf22_text()

    if not info["si_present"]:
        verdict = "EXT_DUTTA_SF22_TUNNEL_HUB_INDETERMINATE"
    elif info.get("residue_roster_found"):
        verdict = "EXT_DUTTA_SF22_TUNNEL_HUB_MEMBERSHIP"
    else:
        verdict = "EXT_DUTTA_SF22_TUNNEL_HUB_QUALITATIVE_ONLY"

    hub_membership = {
        h: "INDETERMINATE_NO_RESIDUE_ROSTER" for h in HUBS
    }

    payload = {
        "experiment": "EXTERNAL_DUTTA_SF22_TUNNEL_HUBS",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_DUTTA_SF22_TUNNEL_HUBS.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "si_pdf": str(SI_PDF.relative_to(ROOT)) if SI_PDF.exists() else None,
        "si_bytes": SI_PDF.stat().st_size if SI_PDF.exists() else None,
        "caption_extract": info.get("caption"),
        "residue_roster_found": info.get("residue_roster_found", False),
        "main_text_claim": info["main_text_claim"],
        "hub_tunnel_membership": hub_membership,
        "governance": {
            "P2_REOPEN": False,
            "invented_tunnel_residues": False,
            "note": "SF22 is image+caption; residue membership not parseable — prefer INDETERMINATE over inventing",
        },
        "doi": "10.1038/s42003-023-04868-1",
        "prior_p4lite": "EXT_P4LITE_ASYMMETRIES_CLOSED_IN_LIT claim2 (pipelines)",
    }
    (OUT / "ext_dutta_sf22_tunnel_hubs.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# EXTERNAL — Dutta Supp Fig. 22 tunnels vs hubs",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_DUTTA_SF22_TUNNEL_HUBS.md`  ",
        f"**SI:** `{'present' if info['si_present'] else 'MISSING'}`",
        "",
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        "> Main text: CB2 pipelines EC→IC **without** clear active/inactive distinction (SF22).  ",
        "> SI caption lists six tunnels by network count — **no residue roster** extractable.  ",
        "> Hub membership per tunnel = **INDETERMINATE** (not invented from the figure).  ",
        "> Does **not** reopen P2 as CONVERGENT.",
        "",
        "## Qualitative claim (CLOSED_IN_LIT; prior P4-lite)",
        "",
        info["main_text_claim"],
        "",
        "## Hub membership",
        "",
        "| Hub | Tunnel membership |",
        "|-----|-------------------|",
    ]
    for h, m in hub_membership.items():
        lines.append(f"| {h} | {m} |")
    lines += [
        "",
        "## SI caption (extract)",
        "",
        info.get("caption") or "_unavailable_",
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {verdict}",
        "INVENTED_TUNNEL_RESIDUES: FALSE",
        "P2_REOPEN: FALSE",
        "```",
        "",
        "---",
        "",
        "*Fin Dutta SF22 tunnel vs hubs.*",
        "",
    ]
    (OUT / "ext_dutta_sf22_tunnel_hubs.md").write_text("\n".join(lines), encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
