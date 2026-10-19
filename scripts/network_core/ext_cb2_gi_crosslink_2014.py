#!/usr/bin/env python3
"""EXTERNAL — Map Mnpotra 2014 CB2–Gi crosslinking pairs onto modern complex PDBs.

Pre-reg: docs/synthesis/EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md
Governance: intermolecular proximity only; NOT Gi functional proof; NOT hub/P3 claim.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PDB_DIR = ROOT / "data" / "external" / "cb2_landmark_expanded"
ABROL_DIR = ROOT / "data" / "external" / "abrol_heo_2024" / "avg_pdbs"
OUT_MD = ROOT / "results" / "network_core" / "ext_cb2_gi_crosslink_2014.md"
OUT_JSON = ROOT / "results" / "network_core" / "ext_cb2_gi_crosslink_2014.json"

# Mnpotra et al. JBC 2014 — DOI 10.1074/jbc.M113.539916
XL_PAIRS = [
    {
        "id": "C134_C351",
        "cb2_resid": 134,
        "cb2_resname": "CYS",
        "cb2_bw": "C3.53/C3.54(134)",
        "gai_resid": 351,
        "gai_resname": "CYS",
        "gai_site": "a5 i-3",
        "chemistry": "HgCl2 Cys-Cys",
        "ca_lo": 7.0,
        "ca_hi": 10.0,
        "source": "experimental_XL",
    },
    {
        "id": "K245_K349",
        "cb2_resid": 245,
        "cb2_resname": "LYS",
        "cb2_bw": "K6.35(245)",
        "gai_resid": 349,
        "gai_resname": "LYS",
        "gai_site": "a5 i-5",
        "chemistry": "DSS Lys-Lys",
        "ca_lo": 0.0,
        "ca_hi": 24.2,
        "source": "experimental_XL",
    },
    {
        "id": "K215_K317",
        "cb2_resid": 215,
        "cb2_resname": "LYS",
        "cb2_bw": "K5.64(215)",
        "gai_resid": 317,
        "gai_resname": "LYS",
        "gai_site": "a4b6 loop",
        "chemistry": "DSS Lys-Lys",
        "ca_lo": 0.0,
        "ca_hi": 24.2,
        "source": "experimental_XL",
    },
]

PRO139_POCKET_GAI = [34, 194, 196, 336, 340, 343, 344]

STRUCTURES = [
    ("6PT0", PDB_DIR / "6PT0.pdb", True, "WIN-CB2-Gi complex"),
    ("6KPF", PDB_DIR / "6KPF.pdb", True, "agonist-CB2-Gi cryo-EM"),
    ("8GUR", PDB_DIR / "8GUR.pdb", True, "CP55,940-CB2-Gi"),
    ("8GUS", PDB_DIR / "8GUS.pdb", True, "HU-308-CB2-Gi"),
    ("8GUQ", PDB_DIR / "8GUQ.pdb", True, "Olorinab-CB2-Gi"),
    ("8GUT", PDB_DIR / "8GUT.pdb", True, "LEI-102-CB2-Gi"),
    ("8X3L", PDB_DIR / "8X3L.pdb", True, "CB2-G complex (Shen 2024)"),
    ("9U7L", PDB_DIR / "9U7L.pdb", False, "PAM complex; Gi absent in local file"),
    ("5ZTY", PDB_DIR / "5ZTY.pdb", False, "inactive crystal — no Gi"),
    ("6KPC", PDB_DIR / "6KPC.pdb", False, "active crystal — no Gi"),
    (
        "Abrol_Gi_Empty",
        ABROL_DIR / "CB2R-WT-NoPhosphoC_Gi-Empty_avgframe569.pdb",
        True,
        "Abrol/Heo avg frame Gi-Empty (MD model, not cryo)",
    ),
    (
        "Abrol_Gi_GDP",
        ABROL_DIR / "CB2R-WT-NoPhosphoC_Gi-GDP_avgframe1262.pdb",
        True,
        "Abrol/Heo avg frame Gi-GDP (MD model, not cryo)",
    ),
]

NAME_ALIASES = {
    "CYS": {"CYS", "CYX"},
    "LYS": {"LYS"},
    "PRO": {"PRO"},
}


def parse_ca(path: Path) -> dict[tuple[str, int, str], np.ndarray]:
    atoms: dict[tuple[str, int, str], np.ndarray] = {}
    with path.open() as f:
        for line in f:
            if not line.startswith("ATOM"):
                continue
            if line[12:16].strip() != "CA":
                continue
            ch = line[21]
            resn = line[17:20].strip()
            try:
                resid = int(line[22:26])
            except ValueError:
                continue
            xyz = np.array(
                [float(line[30:38]), float(line[38:46]), float(line[46:54])],
                dtype=float,
            )
            atoms[(ch, resid, resn)] = xyz
    return atoms


def chain_stats(atoms: dict[tuple[str, int, str], np.ndarray]) -> dict[str, Any]:
    by: dict[str, list[int]] = {}
    for ch, resid, _ in atoms:
        by.setdefault(ch, []).append(resid)
    return {
        ch: {"n_ca": len(resids), "resid_min": min(resids), "resid_max": max(resids)}
        for ch, resids in sorted(by.items())
    }


def pick_receptor_chain(atoms: dict[tuple[str, int, str], np.ndarray]) -> str | None:
    markers = {134, 215, 245, 139}
    scores: dict[str, int] = {}
    for ch, resid, _ in atoms:
        if resid in markers:
            scores[ch] = scores.get(ch, 0) + 1
    if "R" in scores:
        return "R"
    if not scores:
        return None
    return max(scores, key=scores.get)


def pick_gai_chain(
    atoms: dict[tuple[str, int, str], np.ndarray], receptor: str | None
) -> str | None:
    markers = {317, 349, 351, 354}
    scores: dict[str, int] = {}
    for ch, resid, _resn in atoms:
        if receptor is not None and ch == receptor:
            continue
        if resid in markers:
            scores[ch] = scores.get(ch, 0) + 1
    if "A" in scores and scores["A"] >= 2:
        return "A"
    if not scores:
        return None
    return max(scores, key=scores.get)


def residues_on_chain(
    atoms: dict[tuple[str, int, str], np.ndarray],
    chain: str,
    resid: int,
    expect: str,
) -> list[tuple[tuple[str, int, str], np.ndarray]]:
    allowed = NAME_ALIASES.get(expect, {expect})
    hits = [
        (k, v)
        for k, v in atoms.items()
        if k[0] == chain and k[1] == resid and k[2] in allowed
    ]
    if hits:
        return hits
    return [(k, v) for k, v in atoms.items() if k[0] == chain and k[1] == resid]


def classify(d: float, lo: float, hi: float, kind: str) -> str:
    if lo <= d <= hi:
        return "WITHIN"
    if kind == "cys":
        if d < lo and d >= lo - 2.0:
            return "BORDERLINE"
        if d > hi and d <= hi + 3.0:
            return "BORDERLINE"
        return "OUT"
    if d > hi and d <= hi + 3.0:
        return "BORDERLINE"
    return "OUT"


def measure_pair(
    atoms: dict[tuple[str, int, str], np.ndarray],
    r_chain: str,
    g_chain: str,
    pair: dict[str, Any],
) -> dict[str, Any]:
    rh = residues_on_chain(atoms, r_chain, pair["cb2_resid"], pair["cb2_resname"])
    gh = residues_on_chain(atoms, g_chain, pair["gai_resid"], pair["gai_resname"])
    if not rh:
        return {
            "status": "MISSING_CB2",
            "ca_ca_A": None,
            "call": "MISSING",
            "cb2": None,
            "gai": None,
        }
    if not gh:
        return {
            "status": "MISSING_GAI",
            "ca_ca_A": None,
            "call": "MISSING",
            "cb2": f"{rh[0][0][2]}{rh[0][0][1]}:{rh[0][0][0]}",
            "gai": None,
        }
    best_d = None
    best = None
    for rk, rv in rh:
        for gk, gv in gh:
            d = float(np.linalg.norm(rv - gv))
            if best_d is None or d < best_d:
                best_d = d
                best = (rk, gk)
    assert best is not None and best_d is not None
    kind = "cys" if pair["chemistry"].startswith("HgCl2") else "lys"
    call = classify(best_d, pair["ca_lo"], pair["ca_hi"], kind)
    return {
        "status": "OK",
        "ca_ca_A": round(best_d, 3),
        "call": call,
        "cb2": f"{best[0][2]}{best[0][1]}:{best[0][0]}",
        "gai": f"{best[1][2]}{best[1][1]}:{best[1][0]}",
        "window_A": [pair["ca_lo"], pair["ca_hi"]],
    }


def measure_pro139(
    atoms: dict[tuple[str, int, str], np.ndarray],
    r_chain: str,
    g_chain: str,
) -> dict[str, Any]:
    rh = residues_on_chain(atoms, r_chain, 139, "PRO")
    if not rh:
        return {"status": "MISSING_CB2", "min_ca_ca_A": None, "nearest": None}
    _pk, pv = rh[0]
    dists = []
    for resid in PRO139_POCKET_GAI:
        hits = [(k, v) for k, v in atoms.items() if k[0] == g_chain and k[1] == resid]
        if not hits:
            continue
        d = float(np.linalg.norm(pv - hits[0][1]))
        dists.append(
            {
                "gai": f"{hits[0][0][2]}{resid}:{g_chain}",
                "ca_ca_A": round(d, 3),
            }
        )
    if not dists:
        return {
            "status": "MISSING_POCKET",
            "min_ca_ca_A": None,
            "nearest": None,
            "n_pocket": 0,
        }
    nearest = min(dists, key=lambda x: x["ca_ca_A"])
    return {
        "status": "OK",
        "min_ca_ca_A": nearest["ca_ca_A"],
        "nearest": nearest["gai"],
        "n_pocket": len(dists),
        "pocket_distances": dists,
        "note": "MD registering contact (Mnpotra), NOT an experimental cross-link",
    }


def analyze_structure(
    label: str, path: Path, has_gi_expected: bool, note: str
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "label": label,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "exists": path.exists(),
        "has_gi_expected": has_gi_expected,
        "note": note,
    }
    if not path.exists():
        rec["status"] = "FILE_MISSING"
        return rec
    atoms = parse_ca(path)
    rec["chains"] = chain_stats(atoms)
    r_chain = pick_receptor_chain(atoms)
    g_chain = pick_gai_chain(atoms, r_chain) if has_gi_expected else None
    rec["receptor_chain"] = r_chain
    rec["gai_chain"] = g_chain
    if r_chain is None:
        rec["status"] = "NO_RECEPTOR_MAP"
        return rec
    if has_gi_expected and g_chain is None:
        rec["status"] = "NO_GAI_MAP"
        rec["pairs"] = {}
        rec["pro139"] = {"status": "NO_GAI"}
        return rec
    if not has_gi_expected:
        rec["status"] = "NO_GI_COMPLEX"
        rec["pairs"] = {
            p["id"]: {"call": "N/A_NO_GI", "status": "N/A"} for p in XL_PAIRS
        }
        rec["pro139"] = {"status": "N/A_NO_GI"}
        return rec

    pairs_out = {}
    for p in XL_PAIRS:
        pairs_out[p["id"]] = measure_pair(atoms, r_chain, g_chain, p)
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
    return rec


def aggregate_verdict(records: list[dict[str, Any]]) -> dict[str, Any]:
    primary_labels = {"6PT0", "6KPF", "8GUR", "8GUS", "8GUQ", "8GUT", "8X3L"}
    primary = [
        r for r in records if r["label"] in primary_labels and r.get("status") == "OK"
    ]
    pair_ids = [p["id"] for p in XL_PAIRS]
    tallies: dict[str, dict[str, int]] = {
        pid: {"WITHIN": 0, "BORDERLINE": 0, "OUT": 0, "MISSING": 0, "n": 0}
        for pid in pair_ids
    }
    for r in primary:
        for pid in pair_ids:
            call = r["pairs"][pid]["call"]
            tallies[pid][call] = tallies[pid].get(call, 0) + 1
            tallies[pid]["n"] += 1

    within_frac = {}
    for pid, t in tallies.items():
        n = t["n"]
        within_frac[pid] = (t["WITHIN"] / n) if n else None

    n_primary = len(primary)
    if n_primary < 3:
        verdict = "EXT_CB2_GI_XL_STRUCTURAL_INDETERMINATE"
        reason = "Fewer than 3 mappable modern CB2-Gi complexes"
    else:
        lys_ok = all(
            (within_frac[pid] or 0) >= 0.7 for pid in ("K245_K349", "K215_K317")
        )
        cys_within = within_frac["C134_C351"] or 0
        cys_border = (
            tallies["C134_C351"]["BORDERLINE"] / tallies["C134_C351"]["n"]
        )
        cys_ok = cys_within >= 0.5 or (cys_within + cys_border) >= 0.7
        any_out_majority = any(
            (tallies[pid]["OUT"] / tallies[pid]["n"]) > 0.5 for pid in pair_ids
        )

        if lys_ok and cys_within >= 0.7:
            verdict = "EXT_CB2_GI_XL_STRUCTURAL_SUPPORTED"
            reason = (
                "All three XL pairs WITHIN in >=70% of primary cryo/X-ray CB2-Gi panel"
            )
        elif lys_ok and cys_ok:
            verdict = "EXT_CB2_GI_XL_STRUCTURAL_PARTIAL"
            reason = (
                "Lys-Lys XL pairs geometrically compatible; Cys-Cys often "
                "WITHIN/BORDERLINE (HgCl2 window tight; paper start pose also borderline)"
            )
        elif any_out_majority:
            verdict = "EXT_CB2_GI_XL_STRUCTURAL_TENSION"
            reason = ">=1 XL pair OUT in majority of primary panel"
        else:
            verdict = "EXT_CB2_GI_XL_STRUCTURAL_PARTIAL"
            reason = "Mixed WITHIN/BORDERLINE/OUT across primary panel"

    return {
        "verdict": verdict,
        "reason": reason,
        "n_primary_structures": n_primary,
        "pair_tallies_primary": tallies,
        "within_fraction_primary": within_frac,
        "non_claims": [
            "XL = intermolecular CB2<->Gi proximity under crosslinking chemistry, not intramolecular CB2 distances",
            "Geometric compatibility != proof of Janusforge hubs or P3 effector mechanism",
            "Pro139 pocket proximity is MD registering contact from Mnpotra, not an experimental XL",
            "Abrol avg frames are secondary (MD models), not primary cryo evidence",
            "P2 not reopened; P5 not advanced; no docking/de novo; no Tier B MD",
        ],
    }


def render_md(payload: dict[str, Any]) -> str:
    v = payload["aggregate"]
    lines = [
        "# EXTERNAL — Mnpotra 2014 CB2-Gi crosslinking vs modern complex structures",
        "",
        f"**Run UTC:** `{payload['run_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_CB2_GI_CROSSLINK_2014.md`",
        "**Scope:** EXTERNAL structural comparison only — **intermolecular proximity**, not intramolecular CB2 map.",
        "",
        "## Verdict",
        "",
        f"**Primary:** `{v['verdict']}`",
        "",
        f"> {v['reason']}",
        "",
        "## Plain-language answer",
        "",
        "Las tres parejas de entrecruzamiento CB2<->Gai1 de Mnpotra 2014 se contrastan con "
        "estructuras modernas CB2-Gi (panel cryo/X-ray local). Lo que se mide es distancia Ca-Ca "
        "**entre receptor y Gi**, bajo ventanas quimicas del paper (HgCl2 Cys-Cys ~7-10 A; "
        "DSS Lys-Lys <=24.2 A). Esto **no** demuestra hubs Janusforge ni cierra P3.",
        "",
        "## Bibliographic note (locked)",
        "",
        "| Field | Value |",
        "|-------|-------|",
        "| Paper | Mnpotra et al., *J. Biol. Chem.* 2014 |",
        "| DOI | [10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916) |",
        "| PMID | 24855641 |",
        "| PMC | [PMC4106340](https://pmc.ncbi.nlm.nih.gov/articles/PMC4106340/) |",
        "| What XL measures | Intermolecular CB2<->Gai1 proximity compatible with crosslinker geometry |",
        "| What XL does **not** measure | Intramolecular CB2 distances; allosteric path; hub identity |",
        "",
        "### Experimental pairs (sequence numbers authoritative)",
        "",
        "| Pair | CB2 | Gai1 | Chemistry | Ca-Ca window (paper) |",
        "|------|-----|------|-----------|----------------------|",
        "| C134-C351 | C3.53/C3.54(134) | Cys351 a5 i-3 | HgCl2 | 7-10 A |",
        "| K245-K349 | K6.35(245) | Lys349 a5 i-5 | DSS | <=24.2 A |",
        "| K215-K317 | K5.64(215) | Lys317 a4b6 | DSS | <=24.2 A |",
        "",
        "Ballesteros label for Cys134 is **C3.53 in the abstract** and **C3.54 in the Results body** — "
        "sequence number **134** is used for mapping. Pro139-Gai hydrophobic pocket is an **MD "
        "registering contact**, reported separately, not as XL.",
        "",
        "## Primary panel (cryo/X-ray CB2-Gi)",
        "",
        "| Structure | C134-C351 (A / call) | K245-K349 (A / call) | K215-K317 (A / call) | Structure call |",
        "|-----------|----------------------|----------------------|----------------------|----------------|",
    ]
    primary_order = ["6PT0", "6KPF", "8GUR", "8GUS", "8GUQ", "8GUT", "8X3L"]
    by_label = {r["label"]: r for r in payload["structures"]}
    for lab in primary_order:
        r = by_label[lab]
        if r.get("status") != "OK":
            lines.append(f"| {lab} | — | — | — | `{r.get('status')}` |")
            continue

        def cell(pid: str) -> str:
            p = r["pairs"][pid]
            if p.get("ca_ca_A") is None:
                return f"— / `{p['call']}`"
            return f"{p['ca_ca_A']:.2f} / `{p['call']}`"

        lines.append(
            f"| {lab} | {cell('C134_C351')} | {cell('K245_K349')} | {cell('K215_K317')} | "
            f"`{r.get('structure_call')}` |"
        )

    lines += [
        "",
        "### Pair tallies (primary panel)",
        "",
        "| Pair | WITHIN | BORDERLINE | OUT | MISSING | WITHIN frac |",
        "|------|--------|------------|-----|---------|-------------|",
    ]
    for pid, t in v["pair_tallies_primary"].items():
        frac = v["within_fraction_primary"][pid]
        frac_s = f"{frac:.2f}" if frac is not None else "—"
        lines.append(
            f"| {pid} | {t['WITHIN']} | {t['BORDERLINE']} | {t['OUT']} | {t['MISSING']} | {frac_s} |"
        )

    lines += [
        "",
        "## Pro139 pocket (MD registering; not XL)",
        "",
        "| Structure | min Ca-Ca to pocket (A) | nearest Gai residue |",
        "|-----------|-------------------------|---------------------|",
    ]
    for lab in primary_order:
        r = by_label[lab]
        p139 = r.get("pro139") or {}
        if p139.get("status") != "OK":
            lines.append(f"| {lab} | — | `{p139.get('status')}` |")
        else:
            lines.append(
                f"| {lab} | {p139['min_ca_ca_A']:.2f} | {p139['nearest']} |"
            )

    lines += [
        "",
        "## Secondary / negative controls",
        "",
        "| Structure | Role | Result |",
        "|-----------|------|--------|",
    ]
    for lab in ["9U7L", "5ZTY", "6KPC", "Abrol_Gi_Empty", "Abrol_Gi_GDP"]:
        r = by_label[lab]
        if r.get("status") == "NO_GI_COMPLEX":
            lines.append(f"| {lab} | {r['note']} | `N/A_NO_GI` (expected) |")
        elif r.get("status") == "OK":
            cells = []
            for pid in ("C134_C351", "K245_K349", "K215_K317"):
                p = r["pairs"][pid]
                if p.get("ca_ca_A") is None:
                    cells.append(p["call"])
                else:
                    cells.append(f"{p['ca_ca_A']:.1f}:{p['call']}")
            lines.append(
                f"| {lab} | {r['note']} | {' · '.join(cells)} (`{r.get('structure_call')}`) |"
            )
        else:
            lines.append(f"| {lab} | {r.get('note', '')} | `{r.get('status')}` |")

    lines += [
        "",
        "## Epistemic limits (locked)",
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
        "2. Local structures — [`CB2_STRUCTURE_ATLAS.md`](../../docs/synthesis/CB2_STRUCTURE_ATLAS.md)",
        "3. Abrol avg frames — Heo & Abrol [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100) "
        "(secondary only)",
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
        "experiment": "EXT_CB2_GI_CROSSLINK_2014",
        "paper": {
            "citation": "Mnpotra et al. J Biol Chem 2014",
            "doi": "10.1074/jbc.M113.539916",
            "pmid": "24855641",
            "pmc": "PMC4106340",
        },
        "xl_pairs_definition": XL_PAIRS,
        "pro139_pocket_gai_resids": PRO139_POCKET_GAI,
        "structures": records,
        "aggregate": aggregate,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"VERDICT: {aggregate['verdict']}")


if __name__ == "__main__":
    main()
