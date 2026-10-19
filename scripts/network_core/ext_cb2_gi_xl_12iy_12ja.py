#!/usr/bin/env python3
"""EXTERNAL extension — Mnpotra 2014 XL pairs on 12IY / 12JA (same protocol).

Pre-reg: docs/synthesis/EXPERIMENT_EXT_CB2_GI_XL_12IY_12JA.md
Reuses locked XL pairs + Cα windows from EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

# Import locked protocol from 2014 runner
_spec = importlib.util.spec_from_file_location(
    "ext_cb2_gi_crosslink_2014",
    ROOT / "scripts" / "network_core" / "ext_cb2_gi_crosslink_2014.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

XL_PAIRS = _mod.XL_PAIRS
PRO139_POCKET_GAI = _mod.PRO139_POCKET_GAI
classify = _mod.classify
measure_pair = _mod.measure_pair
measure_pro139 = _mod.measure_pro139
pick_receptor_chain = _mod.pick_receptor_chain
pick_gai_chain = _mod.pick_gai_chain
chain_stats = _mod.chain_stats
NAME_ALIASES = _mod.NAME_ALIASES

PDB_DIR = ROOT / "data" / "external" / "cb2_landmark_expanded"
OUT_MD = ROOT / "results" / "network_core" / "ext_cb2_gi_xl_12iy_12ja.md"
OUT_JSON = ROOT / "results" / "network_core" / "ext_cb2_gi_xl_12iy_12ja.json"

# PI panel: 12IY + 12JA. 12IZ appendix = Gi complex for same agonist series as 12IY.
STRUCTURES = [
    (
        "12IY",
        PDB_DIR / "12IY.cif",
        False,  # locally refined CB2+ligand; no Gi in deposit
        "Locally refined CB2 + agonist '5249 (Rachman 2026); receptor-only deposit",
    ),
    (
        "12JA",
        PDB_DIR / "12JA.cif",
        True,
        "CB2–Gi + agonist '1029 (Rachman 2026)",
    ),
    (
        "12IZ",
        PDB_DIR / "12IZ.cif",
        True,
        "APPENDIX: CB2–Gi + agonist '5249 (full complex; Gi counterpart of 12IY series)",
    ),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ca_cif(path: Path) -> dict[tuple[str, int, str], np.ndarray]:
    from Bio.PDB import MMCIFParser

    parser = MMCIFParser(QUIET=True)
    struct = parser.get_structure(path.stem, str(path))
    atoms: dict[tuple[str, int, str], np.ndarray] = {}
    for model in struct:
        for chain in model:
            for res in chain:
                if res.id[0] != " ":
                    continue
                if "CA" not in res:
                    continue
                ca = res["CA"]
                atoms[(chain.id, res.id[1], res.get_resname())] = np.array(
                    ca.coord, dtype=float
                )
    return atoms


def analyze_structure(
    label: str, path: Path, has_gi_expected: bool, note: str
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "label": label,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "exists": path.exists(),
        "has_gi_expected": has_gi_expected,
        "note": note,
        "format": path.suffix.lstrip("."),
    }
    if not path.exists():
        rec["status"] = "FILE_MISSING"
        return rec
    rec["sha256"] = sha256_file(path)
    atoms = parse_ca_cif(path) if path.suffix.lower() == ".cif" else _mod.parse_ca(path)
    rec["chains"] = chain_stats(atoms)
    r_chain = pick_receptor_chain(atoms)
    g_chain = pick_gai_chain(atoms, r_chain) if has_gi_expected else None
    # If Gi expected but absent in file, detect honestly
    if has_gi_expected and g_chain is None:
        # also try: if only receptor markers exist
        rec["receptor_chain"] = r_chain
        rec["gai_chain"] = None
        rec["status"] = "NO_GAI_MAP"
        rec["pairs"] = {}
        rec["pro139"] = {"status": "NO_GAI"}
        return rec
    if not has_gi_expected:
        # Confirm no Gαi C-term markers that would contradict receptor-only claim
        g_probe = pick_gai_chain(atoms, r_chain)
        rec["receptor_chain"] = r_chain
        rec["gai_chain"] = g_probe
        rec["status"] = "NO_GI_COMPLEX"
        rec["pairs"] = {p["id"]: {"call": "N/A_NO_GI", "status": "N/A"} for p in XL_PAIRS}
        rec["pro139"] = {"status": "N/A_NO_GI"}
        if g_probe is not None:
            rec["status"] = "UNEXPECTED_GAI_PRESENT"
            # still measure if present (fail-open for honesty)
            pairs_out = {
                p["id"]: measure_pair(atoms, r_chain, g_probe, p) for p in XL_PAIRS
            }
            rec["pairs"] = pairs_out
            rec["pro139"] = measure_pro139(atoms, r_chain, g_probe)
        return rec

    if r_chain is None:
        rec["status"] = "NO_RECEPTOR_MAP"
        return rec

    pairs_out = {p["id"]: measure_pair(atoms, r_chain, g_chain, p) for p in XL_PAIRS}
    rec["pairs"] = pairs_out
    rec["pro139"] = measure_pro139(atoms, r_chain, g_chain)
    calls = [v["call"] for v in pairs_out.values()]
    if all(c == "WITHIN" for c in calls):
        rec["structure_call"] = "ALL_WITHIN"
    elif any(c == "MISSING" for c in calls):
        rec["structure_call"] = "PARTIAL_MISSING"
    elif all(c in ("WITHIN", "BORDERLINE") for c in calls):
        rec["structure_call"] = "WITHIN_OR_BORDERLINE"
    elif any(c == "OUT" for c in calls) and any(c == "WITHIN" for c in calls):
        rec["structure_call"] = "MIXED"
    elif all(c == "OUT" for c in calls):
        rec["structure_call"] = "ALL_OUT"
    else:
        rec["structure_call"] = "MIXED"
    rec["status"] = "OK"
    rec["receptor_chain"] = r_chain
    rec["gai_chain"] = g_chain
    return rec


def aggregate_verdict(records: list[dict[str, Any]]) -> dict[str, Any]:
    by = {r["label"]: r for r in records}
    r_iy = by["12IY"]
    r_ja = by["12JA"]
    r_iz = by.get("12IZ")

    ja_ok = r_ja.get("status") == "OK"
    ja_calls = (
        [r_ja["pairs"][p["id"]]["call"] for p in XL_PAIRS] if ja_ok else []
    )
    ja_all_within = ja_ok and all(c == "WITHIN" for c in ja_calls)
    ja_any_out = ja_ok and any(c == "OUT" for c in ja_calls)
    iy_no_gi = r_iy.get("status") == "NO_GI_COMPLEX"

    if not ja_ok:
        verdict = "EXT_CB2_GI_XL_12IY_12JA_INDETERMINATE"
        reason = "12JA not mappable (missing file / chains / residues); prefer INDETERMINATE"
    elif ja_any_out and not all(c == "WITHIN" for c in ja_calls):
        if any(c == "WITHIN" for c in ja_calls):
            verdict = "EXT_CB2_GI_XL_12IY_12JA_PARTIAL"
            reason = "12JA mixed WITHIN/OUT; 12IY receptor-only (N/A_NO_GI)"
        else:
            verdict = "EXT_CB2_GI_XL_12IY_12JA_TENSION"
            reason = "12JA XL pairs OUT under Mnpotra Cα windows"
    elif ja_all_within and iy_no_gi:
        verdict = "EXT_CB2_GI_XL_12IY_12JA_PARTIAL"
        reason = (
            "12JA (Gi complex): all three XL pairs WITHIN Mnpotra windows; "
            "12IY is locally refined receptor-only (no Gi) — XL intermolecular map N/A for 12IY"
        )
    elif ja_all_within and r_iy.get("status") == "OK":
        iy_calls = [r_iy["pairs"][p["id"]]["call"] for p in XL_PAIRS]
        if all(c == "WITHIN" for c in iy_calls):
            verdict = "EXT_CB2_GI_XL_12IY_12JA_SUPPORTED"
            reason = "Both 12IY and 12JA have Gi and all XL pairs WITHIN"
        else:
            verdict = "EXT_CB2_GI_XL_12IY_12JA_PARTIAL"
            reason = "12JA ALL_WITHIN; 12IY not fully WITHIN/mappable"
    else:
        verdict = "EXT_CB2_GI_XL_12IY_12JA_PARTIAL"
        reason = "Partial geometric compatibility under locked protocol"

    iz_note = None
    if r_iz and r_iz.get("status") == "OK":
        iz_calls = [r_iz["pairs"][p["id"]]["call"] for p in XL_PAIRS]
        iz_note = {
            "structure_call": r_iz.get("structure_call"),
            "all_within": all(c == "WITHIN" for c in iz_calls),
            "role": "APPENDIX only — Gi counterpart for '5249 series; not in PI primary pair",
        }

    return {
        "verdict": verdict,
        "reason": reason,
        "protocol_source": "EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014 (identical XL pairs + Cα windows)",
        "12IY_status": r_iy.get("status"),
        "12JA_status": r_ja.get("status"),
        "12JA_structure_call": r_ja.get("structure_call"),
        "12IZ_appendix": iz_note,
        "non_claims": [
            "XL = intermolecular CB2↔Gi proximity, not intramolecular CB2 distances",
            "Geometric compatibility ≠ Gi functional proof; ≠ Janusforge hubs; ≠ P3",
            "12IY receptor-only deposit does not support XL mapping (honest N/A_NO_GI)",
            "P2 not reopened; P5 not advanced; no docking; no Tier B MD",
        ],
    }


def cell(rec: dict[str, Any], pid: str) -> str:
    if rec.get("status") == "NO_GI_COMPLEX":
        return "— / `N/A_NO_GI`"
    if rec.get("status") != "OK":
        return f"— / `{rec.get('status')}`"
    p = rec["pairs"][pid]
    if p.get("ca_ca_A") is None:
        return f"— / `{p['call']}`"
    return f"{p['ca_ca_A']:.2f} / `{p['call']}`"


def render_md(payload: dict[str, Any]) -> str:
    v = payload["aggregate"]
    by = {r["label"]: r for r in payload["structures"]}
    lines = [
        "# EXTERNAL — Mnpotra 2014 XL pairs on 12IY / 12JA (protocol extension)",
        "",
        f"**Run UTC:** `{payload['run_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_CB2_GI_XL_12IY_12JA.md`",
        "**Protocol:** identical to `EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014` (Cα–Cα windows locked).",
        "",
        "## Verdict",
        "",
        f"**Primary:** `{v['verdict']}`",
        "",
        f"> {v['reason']}",
        "",
        "## Plain-language answer",
        "",
        "**12JA** (CB2–Gi + '1029) se evalúa con las tres parejas XL de Mnpotra 2014. "
        "**12IY** es un depósito de refinamiento local **solo receptor** (sin Gi) → el mapa "
        "intermolecular CB2↔Gi **no aplica** (`N/A_NO_GI`). Apéndice **12IZ** = complejo Gi "
        "de la misma serie '5249. Compatibilidad geométrica ≠ claim funcional Gi ni hubs.",
        "",
        "## Locked XL windows (unchanged)",
        "",
        "| Pair | Chemistry | Cα–Cα window |",
        "|------|-----------|--------------|",
        "| C134–C351 | HgCl2 | 7–10 Å |",
        "| K245–K349 | DSS | ≤24.2 Å |",
        "| K215–K317 | DSS | ≤24.2 Å |",
        "",
        "## PI panel (12IY, 12JA)",
        "",
        "| Structure | Role | C134–C351 | K245–K349 | K215–K317 | Call |",
        "|-----------|------|-----------|-----------|-----------|------|",
    ]
    for lab in ("12IY", "12JA"):
        r = by[lab]
        sc = r.get("structure_call") or r.get("status")
        lines.append(
            f"| {lab} | {r['note'][:48]}… | {cell(r,'C134_C351')} | {cell(r,'K245_K349')} | "
            f"{cell(r,'K215_K317')} | `{sc}` |"
        )

    lines += [
        "",
        "## Appendix — 12IZ (Gi counterpart of '5249 series)",
        "",
        "| Structure | C134–C351 | K245–K349 | K215–K317 | Call |",
        "|-----------|-----------|-----------|-----------|------|",
    ]
    r = by["12IZ"]
    sc = r.get("structure_call") or r.get("status")
    lines.append(
        f"| 12IZ | {cell(r,'C134_C351')} | {cell(r,'K245_K349')} | {cell(r,'K215_K317')} | `{sc}` |"
    )
    if r.get("status") == "OK" and r.get("pro139", {}).get("status") == "OK":
        lines += [
            "",
            f"Pro139 pocket min (12JA): "
            f"{by['12JA'].get('pro139', {}).get('min_ca_ca_A', '—')} Å → "
            f"{by['12JA'].get('pro139', {}).get('nearest', '—')} (MD registering; not XL).",
            f"Pro139 pocket min (12IZ): {r['pro139']['min_ca_ca_A']:.2f} Å → {r['pro139']['nearest']}.",
        ]

    lines += [
        "",
        "## Epistemic limits",
        "",
    ]
    for nc in v["non_claims"]:
        lines.append(f"- {nc}")

    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {v['verdict']}",
        "PROTOCOL: SAME_AS_EXT_CB2_GI_CROSSLINK_2014",
        "XL_MEASURES: INTERMOLECULAR_CB2_Gi_PROXIMITY",
        "HUB_CLAIM: FALSE",
        "P3_CLAIM: FALSE",
        "P2_REOPEN: FALSE",
        "P5_ADVANCE: FALSE",
        "DOCKING: FALSE",
        "TIER_B_MD: FALSE",
        "```",
        "",
        "## References",
        "",
        "1. Mnpotra et al. *JBC* 2014 — [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916)",
        "2. Rachman et al. *J. Med. Chem.* 2026 — [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PDB **12IY**, **12JA**, **12IZ**",
        "3. Parent compare — [`ext_cb2_gi_crosslink_2014.md`](ext_cb2_gi_crosslink_2014.md)",
        "",
        "---",
        "",
        "*Fin. EXTERNAL discrimination-only.*",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    records = [
        analyze_structure(label, path, has_gi, note)
        for label, path, has_gi, note in STRUCTURES
    ]
    aggregate = aggregate_verdict(records)
    payload = {
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "branch": "feat/cb2-hubs-functional-topology-test",
        "experiment": "EXT_CB2_GI_XL_12IY_12JA",
        "parent_protocol": "EXT_CB2_GI_CROSSLINK_2014",
        "xl_pairs_definition": XL_PAIRS,
        "structures": records,
        "aggregate": aggregate,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"VERDICT: {aggregate['verdict']}")
    for r in records:
        print(f"  {r['label']}: {r.get('status')} {r.get('structure_call','')}")


if __name__ == "__main__":
    main()
