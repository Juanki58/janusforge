#!/usr/bin/env python3
"""EXTERNAL — Abrol IC fingerprint vs LigACN Sink Set T.

Pre-reg: docs/synthesis/EXPERIMENT_EXT_ABROL_LIGACN_SINKS.md
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
ABROL = OUT / "ext_abrol_ic_contacts.json"

SINK_T = [
    ("ARG:131", 131, "3x50"),
    ("ASP:240", 240, "6x30"),
    ("SER:303", 303, "8x47"),
    ("SER:69", 69, "2x39"),
]


def _parse_labels(labels: list[str]) -> set[int]:
    out: set[int] = set()
    for lab in labels:
        m = re.search(r":(\d+)$", str(lab))
        if m:
            out.add(int(m.group(1)))
        else:
            m2 = re.search(r"(\d+)", str(lab))
            if m2:
                out.add(int(m2.group(1)))
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not ABROL.exists():
        verdict = "EXT_ABROL_LIGACN_SINK_INDETERMINATE"
        payload = {"verdict": verdict, "error": "missing_abrol_json", "run_utc": run_utc}
        (OUT / "ext_abrol_ligacn_sinks.json").write_text(json.dumps(payload, indent=2) + "\n")
        (OUT / "ext_abrol_ligacn_sinks.md").write_text(f"**`{verdict}`**\n")
        print(verdict)
        return 1

    ab = json.loads(ABROL.read_text(encoding="utf-8"))
    # systems may be dict or list
    systems = ab.get("systems") or ab.get("metrics") or {}
    per_system: dict[str, set[int]] = {}

    if isinstance(systems, dict):
        for name, info in systems.items():
            if not isinstance(info, dict):
                continue
            if info.get("cb2_contact_residues"):
                per_system[name] = {int(x) for x in info["cb2_contact_residues"]}
            else:
                labels = (
                    info.get("cb2_contact_labels")
                    or info.get("contact_residues")
                    or info.get("residues")
                    or []
                )
                if labels:
                    per_system[name] = _parse_labels(labels)

    # Fallback: dig contact lists from known md-derived structure in prior JSON
    if not per_system:
        # Try top-level keys used in report
        for key in ("WT_Gi_Empty", "WT_Gi_GDP", "WT_BARR2_NoP", "WT_BARR2_P"):
            if key in ab:
                per_system[key] = _parse_labels(ab[key])
        # From markdown-equivalent embedded lists if present under metrics
        metrics = ab.get("metrics") or {}
        if isinstance(metrics, dict):
            for name, info in metrics.items():
                if isinstance(info, dict) and "contact_residues" in info:
                    per_system[name] = _parse_labels(info["contact_residues"])

    # Hardcoded fallback from published prior report if JSON schema differs
    if not per_system:
        prior = {
            "WT_Gi_Empty": [63, 131, 134, 135, 138, 142, 219, 223, 236, 238, 239, 240, 242, 302, 303, 307],
            "WT_Gi_GDP": [131, 134, 147, 216, 219, 220, 222, 229, 230, 231, 232, 239, 304],
            "WT_BARR2_NoP": [67, 131, 134, 136, 137, 138, 139, 140, 142, 143, 219, 222, 228, 229, 231, 239, 243, 246, 302, 304, 305],
            "WT_BARR2_P": [67, 69, 70, 131, 134, 135, 138, 139, 142, 219, 220, 223, 229, 232, 233, 236, 238, 243, 246, 302, 303],
        }
        per_system = {k: set(v) for k, v in prior.items()}
        source_note = "fallback_from_ext_abrol_ic_contacts.md_lists"
    else:
        source_note = "parsed_from_ext_abrol_ic_contacts.json"

    union = set().union(*per_system.values()) if per_system else set()
    sink_hits = []
    n_hit = 0
    for lab, resid, bw in SINK_T:
        systems_hit = sorted([s for s, res in per_system.items() if resid in res])
        hit = bool(systems_hit)
        if hit:
            n_hit += 1
        sink_hits.append(
            {
                "sink": lab,
                "resid": resid,
                "bw": bw,
                "in_any_abrol_IC": hit,
                "systems": systems_hit,
            }
        )

    if n_hit >= 3:
        verdict = "EXT_ABROL_LIGACN_SINK_OVERLAP"
    elif n_hit >= 1:
        verdict = "EXT_ABROL_LIGACN_SINK_PARTIAL"
    else:
        verdict = "EXT_ABROL_LIGACN_SINK_ABSENT"

    payload = {
        "experiment": "EXTERNAL_ABROL_LIGACN_SINKS",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_ABROL_LIGACN_SINKS.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "source_note": source_note,
        "sink_set_T": [{"label": a, "resid": b, "bw": c} for a, b, c in SINK_T],
        "sink_hits": sink_hits,
        "n_sinks_hit": n_hit,
        "per_system_n_contacts": {k: len(v) for k, v in per_system.items()},
        "union_size": len(union),
        "governance": {
            "P3_PROJECT_GATE": "BLOCKED",
            "Gi_FUNCTIONAL_CLAIM": False,
            "P2_REOPEN": False,
            "avg_frame_neq_MSM": True,
        },
        "prior_abrol_verdict": ab.get("verdict"),
    }
    (OUT / "ext_abrol_ligacn_sinks.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# EXTERNAL — Abrol IC fingerprint vs LigACN Sink Set T",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_ABROL_LIGACN_SINKS.md`  ",
        f"**Input:** `ext_abrol_ic_contacts.json` ({source_note})",
        "",
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        f"> {n_hit}/4 sinks de LigACN aparecen en ≥1 set de contactos IC Abrol (avg frames).  ",
        "> P3 sigue **BLOCKED**. Avg frame ≠ MSM. Sin claim Gi.",
        "",
        "## Sink membership",
        "",
        "| Sink | BW | In any Abrol IC | Systems |",
        "|------|----|-----------------|---------|",
    ]
    for h in sink_hits:
        sys = ", ".join(h["systems"]) if h["systems"] else "—"
        lines.append(
            f"| {h['sink']} | {h['bw']} | **{h['in_any_abrol_IC']}** | {sys} |"
        )
    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {verdict}",
        "P3_PROJECT_GATE: BLOCKED",
        "Gi_FUNCTIONAL_CLAIM: FALSE",
        "P2_REOPEN: FALSE",
        "```",
        "",
        "---",
        "",
        "*Fin Abrol × LigACN sinks.*",
        "",
    ]
    (OUT / "ext_abrol_ligacn_sinks.md").write_text("\n".join(lines), encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
