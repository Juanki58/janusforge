#!/usr/bin/env python3
"""Phase H1 — Ordinal functional separation vs CB2 conformational coordinate.

Sequence (strict): H0 pharmacology audit → conformational projection → verdict.
Static docking / receptor fingerprints do NOT equate to Gi Emax.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

H0_JSON = ROOT / "data/benchmarks/cb2_functional_audit_level0.json"
PHASE_F_MATRIX = ROOT / "results/conformational/cb2_state_distance_matrix.json"
PHASE_G_JSON = ROOT / "results/conformational/fase_g_generalization_report.json"
CALIBRATION_JSON = ROOT / "results/docking/cb2_multistate_calibration.json"
THCV_JSON = ROOT / "results/docking/thcv_seed/thcv_seed_evaluation.json"

OUT_DIR = ROOT / "results/conformational"
JSON_OUT = OUT_DIR / "fase_h_ordinal_functional_report.json"
MD_OUT = OUT_DIR / "fase_h_ordinal_functional_report.md"

CB2_ACTIVE_REFS = ("6PT0", "6KPF")
CB2_STATES = ("6PT0", "6KPF", "5ZTY", "8GUR")

GOVERNANCE = {
    "PHASE_H": "ORDINAL_FUNCTIONAL_SEPARATION",
    "CONTRACT_v1.0": "FROZEN",
    "DE_NOVO_GENERATION": "STOP",
    "THRESHOLD_MODIFICATION": "STOP",
    "ALLOSTERIC_FRAMEWORK": "HYPOTHESIS_PENDING_CALIBRATION",
    "H0_BEFORE_H1": "mandatory",
    "FORBIDDEN_PATHWAYS": "beta_arrestin, ERK_phosphorylation",
}

VERDICT_LABELS = {
    "ORDINAL_FUNCTIONAL_SEPARATION": "Verde",
    "BINARY_FUNCTIONAL_SEPARATION": "Amarillo",
    "NO_FUNCTIONAL_CORRELATION": "Rojo",
    "INDETERMINATE": "Blanco",
}

# Documented multistate contact table (docs/cb2_multistate_calibration_synthesis.md §5.1)
HU_PAIR_POSE_CONTACTS = {
    "HU-308": {"6PT0": {"score": -9.47, "Ser285_A": 3.33, "Trp258_A": 5.15}},
    "HU-433": {"6PT0": {"score": -9.87, "Ser285_A": 3.06, "Trp258_A": 6.47}},
}


def _sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _load_h0() -> dict[str, Any]:
    if not H0_JSON.exists():
        raise FileNotFoundError(f"H0 audit missing: {H0_JSON}")
    return json.loads(H0_JSON.read_text(encoding="utf-8"))


def _ordinal_class_for_assay(h0: dict[str, Any], assay_type: str) -> dict[str, dict[str, Any]]:
    """Map compound_id → best row for ordinal tier assignment in one assay."""
    eligible = set(h0.get("h0_gate_summary", {}).get("ordinal_eligible_compound_ids", []))
    by_compound: dict[str, list[dict[str, Any]]] = {}
    for row in h0.get("entries", []):
        cid = row["compound_id"]
        if cid not in eligible:
            continue
        if row["assay_type"] != assay_type:
            continue
        by_compound.setdefault(cid, []).append(row)

    out: dict[str, dict[str, Any]] = {}
    for cid, rows in by_compound.items():
        # Prefer LEVEL_0_HIGH over MODERATE
        rank = {"LEVEL_0_HIGH": 0, "LEVEL_0_MODERATE": 1, "INDETERMINATE": 9}
        rows.sort(key=lambda r: rank.get(r.get("comparability_level", "INDETERMINATE"), 9))
        out[cid] = rows[0]
    return out


def _tier_from_class(functional_class: str) -> str | None:
    mapping = {
        "TOTAL": "TOTAL",
        "PARTIAL": "PARTIAL",
        "INVERSE": "INVERSE",
    }
    return mapping.get(functional_class)


def _load_coordinate() -> dict[str, Any]:
    phase_f = _load_json(PHASE_F_MATRIX) or {}
    phase_g = _load_json(PHASE_G_JSON) or {}
    norm_dist_f = {
        pid: row.get("cb2_state_distance_normalized")
        for pid, row in phase_f.get("cb2_state_distance_matrix", {}).items()
        if row.get("receptor") == "cb2"
    }
    norm_dist_g = phase_g.get("cb2_state_distance", {}).get("normalized", {})
    return {
        "active_centroid_from": phase_f.get("cb2_active_centroid_from", list(CB2_ACTIVE_REFS)),
        "phase_f_normalized": norm_dist_f,
        "phase_g_normalized": norm_dist_g,
        "phase_f_sha256": _sha256(PHASE_F_MATRIX),
        "phase_g_sha256": _sha256(PHASE_G_JSON),
        "interpretation": (
            "Receptor-state fingerprint distance to active centroid (6PT0+6KPF). "
            "Ligand projection = distance of multistate-docking preferred receptor state "
            "to that centroid — NOT ligand pose fingerprint, NOT Vina score as Gi Emax."
        ),
    }


def _calibration_rows() -> dict[str, list[dict[str, Any]]]:
    data = _load_json(CALIBRATION_JSON)
    if not data:
        return {}
    rows = data.get("rows", data.get("results", []))
    by_lig: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        lid = row.get("ligand_id") or row.get("id")
        if lid:
            by_lig.setdefault(lid, []).append(row)
    return by_lig


def _best_docked_state(ligand_id: str, cal: dict[str, list[dict[str, Any]]], probe_f: dict) -> dict[str, Any]:
    probe = probe_f.get("probe_secondary", {}).get("entries", {}).get(ligand_id, {})
    if probe.get("best_docked_state") and probe["best_docked_state"] != "not_computed_locally":
        return {
            "preferred_state": probe["best_docked_state"],
            "source": "phase_f_probe_secondary",
            "best_score_kcal_mol": probe.get("best_score_kcal_mol"),
        }
    rows = cal.get(ligand_id, [])
    if rows:
        best = min(rows, key=lambda r: float(r.get("best_score", r.get("score", 999))))
        return {
            "preferred_state": best.get("state_pdb") or best.get("pdb_id", "6PT0"),
            "source": str(CALIBRATION_JSON),
            "best_score_kcal_mol": best.get("best_score", best.get("score")),
        }
    if ligand_id == "Delta9-THCV" and THCV_JSON.exists():
        return {"preferred_state": "6PT0", "source": str(THCV_JSON), "best_score_kcal_mol": None}
    return {"preferred_state": None, "source": None, "best_score_kcal_mol": None}


def _project_ligand(
    ligand_id: str,
    coord: dict[str, Any],
    cal: dict[str, list[dict[str, Any]]],
    phase_f: dict[str, Any],
) -> dict[str, Any]:
    dock = _best_docked_state(ligand_id, cal, phase_f)
    state = dock.get("preferred_state")
    dist_f = coord["phase_f_normalized"].get(state) if state else None
    dist_g = coord["phase_g_normalized"].get(state) if state else None
    return {
        "ligand_id": ligand_id,
        "preferred_receptor_state": state,
        "cb2_state_distance_normalized_phase_f": dist_f,
        "cb2_state_distance_normalized_phase_g": dist_g,
        "projection_defined": state is not None and dist_f is not None,
        "docking_meta": dock,
        "limitation": (
            "Distance is receptor-state coordinate of preferred docked state; "
            "static structure ≠ Gi efficacy."
        ),
    }


def _hu308_hu433_case_study(coord: dict[str, Any]) -> dict[str, Any]:
    hu308 = HU_PAIR_POSE_CONTACTS["HU-308"]["6PT0"]
    hu433 = HU_PAIR_POSE_CONTACTS["HU-433"]["6PT0"]
    active_dist = coord["phase_f_normalized"].get("6PT0")
    return {
        "priority": "primary_mechanistic_case_study",
        "pair": ["HU-308", "HU-433"],
        "relationship": "C3/C1 stereoisomers (enantiomeric pair)",
        "functional_dissociation_literature": {
            "HU-308_cb2_ki_nM": "22.7±3.9 (Hanus 1999)",
            "HU-433_cb2_ki_nM": "12.2 (patent US20110269842A1; higher affinity)",
            "note": (
                "Authors (Hanus 2015) report HU-433 higher biological potency despite "
                "lower CP55940 displacement and GTPgammaS differences — distinct binding "
                "conformations proposed. Do not collapse into one functional class."
            ),
        },
        "multistate_docking_6PT0": {
            "HU-308": hu308,
            "HU-433": hu433,
            "score_delta_kcal_mol": round(hu433["score"] - hu308["score"], 2),
            "Trp258_delta_A": round(hu433["Trp258_A"] - hu308["Trp258_A"], 2),
        },
        "receptor_state_projection": {
            "both_preferred_state": "6PT0",
            "distance_to_active_centroid_phase_f": active_dist,
            "interpretation": (
                "Identical receptor-state centroid distance for both ligands (pose selects same "
                "PDB state), yet pose-conditioned microswitch contacts differ (Trp258 5.15 vs "
                "6.47 Å) and literature reports affinity vs Gi efficacy dissociation. "
                "Supports orientation/conformation mechanism over simple 'distance = Emax' ordinal."
            ),
        },
        "hu433_gi_class": "INDETERMINATE (no comparable CP55940-normalized hCB2 Gi row in H0)",
    }


def _evaluate_ordinal(
    tier_rows: dict[str, dict[str, Any]],
    projections: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Test monotonic order dist(TOTAL) < dist(PARTIAL) < dist(INVERSE) on defined projections."""
    by_tier: dict[str, list[tuple[str, float]]] = {"TOTAL": [], "PARTIAL": [], "INVERSE": []}
    for cid, row in tier_rows.items():
        tier = _tier_from_class(row["functional_class_assigned"])
        if tier is None:
            continue
        proj = projections.get(cid, {})
        dist = proj.get("cb2_state_distance_normalized_phase_f")
        if proj.get("projection_defined") and dist is not None:
            by_tier[tier].append((cid, float(dist)))

    n_tiers_with_data = sum(1 for t in by_tier if by_tier[t])
    total_n = sum(len(v) for v in by_tier.values())

    result: dict[str, Any] = {
        "by_tier": {t: [{"compound_id": c, "distance": d} for c, d in v] for t, v in by_tier.items()},
        "n_projections": total_n,
        "n_tiers_with_data": n_tiers_with_data,
    }

    if n_tiers_with_data < 3 or total_n < 3:
        result["verdict"] = "INDETERMINATE"
        result["rationale"] = (
            f"Insufficient ligands with both comparable Gi tier and defined conformational "
            f"projection ({total_n} projections across {n_tiers_with_data} tiers; need ≥3 "
            f"projections spanning TOTAL/PARTIAL/INVERSE)."
        )
        return result

    tier_means = {t: float(np.mean([d for _, d in v])) if v else None for t, v in by_tier.items()}
    result["tier_mean_distance"] = tier_means

    total_mean = tier_means.get("TOTAL")
    partial_mean = tier_means.get("PARTIAL")
    inverse_mean = tier_means.get("INVERSE")

    if None in (total_mean, partial_mean, inverse_mean):
        result["verdict"] = "INDETERMINATE"
        result["rationale"] = "One or more ordinal tiers lacks projected distance after H0 filtering."
        return result

    eps = 1e-6
    ordinal_ok = total_mean + eps < partial_mean < inverse_mean - eps
    binary_ok = total_mean + eps < inverse_mean - eps

    # Collapse check: TOTAL ≈ INVERSE
    if abs(total_mean - inverse_mean) < 0.05:
        result["verdict"] = "NO_FUNCTIONAL_CORRELATION"
        result["rationale"] = (
            f"TOTAL mean distance ({total_mean:.4f}) ≈ INVERSE ({inverse_mean:.4f}) — "
            "no functional correlation (H1 falsified)."
        )
    elif ordinal_ok:
        result["verdict"] = "ORDINAL_FUNCTIONAL_SEPARATION"
        result["rationale"] = (
            f"Monotonic order holds: TOTAL ({total_mean:.4f}) < PARTIAL ({partial_mean:.4f}) "
            f"< INVERSE ({inverse_mean:.4f}) on receptor-state projection."
        )
    elif binary_ok:
        result["verdict"] = "BINARY_FUNCTIONAL_SEPARATION"
        result["rationale"] = (
            f"Agonist vs inverse separated (TOTAL {total_mean:.4f} < INVERSE {inverse_mean:.4f}) "
            f"but PARTIAL tier mean ({partial_mean:.4f}) overlaps extremes — not full ordinal."
        )
    else:
        result["verdict"] = "NO_FUNCTIONAL_CORRELATION"
        result["rationale"] = (
            f"Order not preserved: TOTAL={total_mean:.4f}, PARTIAL={partial_mean:.4f}, "
            f"INVERSE={inverse_mean:.4f}."
        )
    return result


def _write_md(payload: dict[str, Any]) -> None:
    h0 = payload["h0_summary"]
    h1 = payload["h1_evaluation"]
    verdict = h1["verdict"]
    emoji = {"ORDINAL_FUNCTIONAL_SEPARATION": "🟢", "BINARY_FUNCTIONAL_SEPARATION": "🟡",
             "NO_FUNCTIONAL_CORRELATION": "🔴", "INDETERMINATE": "⚪"}.get(verdict, "⚪")

    lines = [
        "# Phase H — Auditoría funcional (H0) y separación ordinal (H1)",
        "",
        f"**Generado:** {payload['generated_utc']}  ",
        f"**Rama:** `{payload['branch']}`",
        "",
        "## Gobernanza",
        "",
        "```yaml",
        *[f"{k}: {v}" for k, v in GOVERNANCE.items()],
        "```",
        "",
        "## H0 — ¿Tenemos datos Gi comparables?",
        "",
        f"**Respuesta:** {'**Sí** (parcial)' if h0['comparable_gi_data_exists'] else '**No**'}",
        "",
        h0.get("rationale", ""),
        "",
        f"- Mejor ensayo para ordinal: **{h0.get('best_comparable_assay_for_ordinal', '—')}**",
        f"- Compuestos elegibles ordinal: {', '.join(h0.get('ordinal_eligible_compound_ids', []))}",
        "",
        "### Tabla H0 (filas auditadas)",
        "",
        "| Compuesto | Ensayo | Ref. | Emax % | Clase | Comparabilidad | DOI/PMID |",
        "|-----------|--------|------|--------|-------|----------------|----------|",
    ]
    for row in payload["h0_entries_table"]:
        emax = row.get("relative_emax_percent")
        emax_s = "null" if emax is None else str(emax)
        lines.append(
            f"| {row['compound_id']} | {row['assay_type']} | {row['reference_agonist']} | "
            f"{emax_s} | {row['functional_class_assigned']} | {row['comparability_level']} | "
            f"{row['primary_doi_or_pmid']} |"
        )

    lines.extend([
        "",
        "**Cautelas PI:** AM630 → PROTEAN (no INVERSE automático). THCV → INDETERMINATE "
        "(no intermediario ordinal forzado). HU-308/HU-433 → caso pareado, no misma clase.",
        "",
        "## H1 — Proyección conformacional",
        "",
        payload["coordinate"]["interpretation"],
        "",
        f"- Centroide activo: **{' + '.join(payload['coordinate']['active_centroid_from'])}**",
        f"- SHA256 Phase F matrix: `{payload['coordinate'].get('phase_f_sha256', '—')}`",
        f"- SHA256 Phase G report: `{payload['coordinate'].get('phase_g_sha256', '—')}`",
        "",
        "### Distancias por compuesto (Phase F normalizado)",
        "",
        "| Compuesto | Estado preferido | Distancia | Proyección definida |",
        "|-----------|------------------|-----------|---------------------|",
    ])
    for lid, proj in sorted(payload["projections"].items()):
        lines.append(
            f"| {lid} | {proj.get('preferred_receptor_state') or '—'} | "
            f"{proj.get('cb2_state_distance_normalized_phase_f') or '—'} | "
            f"{'sí' if proj.get('projection_defined') else 'no'} |"
        )

    pair = payload["hu308_hu433_case_study"]
    lines.extend([
        "",
        "## Caso prioritario — par HU-308 ↔ HU-433",
        "",
        f"- Relación: {pair['relationship']}",
        f"- Ki literatura: HU-308 {pair['functional_dissociation_literature']['HU-308_cb2_ki_nM']}; "
        f"HU-433 {pair['functional_dissociation_literature']['HU-433_cb2_ki_nM']}",
        f"- Docking 6PT0 Δscore: {pair['multistate_docking_6PT0']['score_delta_kcal_mol']} kcal/mol; "
        f"ΔTrp258: {pair['multistate_docking_6PT0']['Trp258_delta_A']} Å",
        f"- {pair['receptor_state_projection']['interpretation']}",
        "",
        "## Veredicto H1",
        "",
        f"### {emoji} {verdict} ({VERDICT_LABELS.get(verdict, verdict)})",
        "",
        h1.get("rationale", ""),
        "",
        "### Limitaciones explícitas",
        "",
        "- Proyección = estado receptor preferido por docking multistate; **no** equivalencia Vina ↔ Gi Emax.",
        "- Ensayo funcional y expresión celular no entran en la coordenada estructural.",
        "- β-arrestin / ERK **prohibidos** como proxy de clase Gi.",
        "",
        "## Integridad (SHA256)",
        "",
        f"| Artefacto | SHA256 |",
        f"|-----------|--------|",
        f"| H0 JSON | `{payload['input_hashes'].get('h0_json')}` |",
        f"| Phase F matrix | `{payload['input_hashes'].get('phase_f_matrix')}` |",
        f"| Phase G report | `{payload['input_hashes'].get('phase_g_report')}` |",
        f"| Este reporte JSON | `{payload.get('report_sha256', 'pending')}` |",
        "",
    ])
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def run_evaluation(assay_type: str = "GTPgammaS") -> dict[str, Any]:
    h0 = _load_h0()
    phase_f = _load_json(PHASE_F_MATRIX) or {}
    coord = _load_coordinate()
    cal = _calibration_rows()

    tier_rows = _ordinal_class_for_assay(h0, assay_type)
    all_ligands = sorted(
        set(tier_rows.keys())
        | {"HU-433", "Delta9-THCV", "AM630"}
    )
    projections = {lid: _project_ligand(lid, coord, cal, phase_f) for lid in all_ligands}

    h1_eval = _evaluate_ordinal(tier_rows, projections)
    if not h0.get("h0_gate_summary", {}).get("comparable_gi_data_exists"):
        h1_eval = {
            "verdict": "INDETERMINATE",
            "rationale": "H0 gate: no comparable Gi data — H1 not executed.",
            "by_tier": {},
            "n_projections": 0,
            "n_tiers_with_data": 0,
        }

    payload: dict[str, Any] = {
        "governance": GOVERNANCE,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "branch": "feat/fase-h-conformational-functional-correlation",
        "sequence": ["H0_pharmacology_audit", "H1_conformational_projection", "verdict"],
        "h0_summary": h0.get("h0_gate_summary", {}),
        "h0_entries_table": h0.get("entries", []),
        "coordinate": coord,
        "projection_method": {
            "name": "multistate_preferred_state_to_active_centroid",
            "active_centroid": list(CB2_ACTIVE_REFS),
            "states_available": list(CB2_STATES),
            "metric": "cb2_state_distance_normalized (Phase F fingerprint space)",
            "honest_limitations": [
                "Static receptor snapshot ≠ Gi efficacy",
                "Vina score is NOT used as functional Emax proxy",
                "Ligands without multistate docking lack defined projection",
                "Identical receptor-state distance can mask pose/orientation differences (HU-308/HU-433)",
            ],
        },
        "assay_used_for_ordinal": assay_type,
        "tier_rows": tier_rows,
        "projections": projections,
        "hu308_hu433_case_study": _hu308_hu433_case_study(coord),
        "h1_evaluation": h1_eval,
        "verdict": h1_eval["verdict"],
        "verdict_label": VERDICT_LABELS.get(h1_eval["verdict"], h1_eval["verdict"]),
        "input_hashes": {
            "h0_json": _sha256(H0_JSON),
            "phase_f_matrix": _sha256(PHASE_F_MATRIX),
            "phase_g_report": _sha256(PHASE_G_JSON),
            "calibration_json": _sha256(CALIBRATION_JSON),
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    payload["report_sha256"] = _sha256(JSON_OUT)
    JSON_OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _write_md(payload)
    return payload


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--assay",
        default="GTPgammaS",
        choices=("GTPgammaS", "cAMP_inhibition"),
        help="Gi assay for ordinal tier assignment from H0 rows",
    )
    args = ap.parse_args()
    payload = run_evaluation(assay_type=args.assay)
    print(f"H0 comparable Gi: {payload['h0_summary'].get('comparable_gi_data_exists')}")
    print(f"H1 verdict: {payload['verdict']} ({payload['verdict_label']})")
    print(f"JSON: {JSON_OUT}")
    print(f"MD:   {MD_OUT}")
    print(f"SHA256: {payload.get('report_sha256')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
