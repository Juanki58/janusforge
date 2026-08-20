#!/usr/bin/env python3
"""Phase A — Blind Qiu challenge set vs THCV_DESIGN_CONSTRAINTS v1.0.

Docks Qiu-14/15/16/20/24 from verified library SMILES only (no de novo).
Contract evaluation is blind in the primary table; literature labels used
only in the concordance section after scores are locked.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark_gold_exam_a import (  # noqa: E402
    RECEPTORS,
    _load_grid,
    compute_microswitch_distances,
)
from src.analysis.contract_evaluation import evaluate_compound, load_contract  # noqa: E402
from src.screening.docking import dock_ligand, resolve_vina  # noqa: E402

STRUCTURES_CSV = ROOT / "data/libraries/qiu_0d_structures.csv"
GOLD_JSON = ROOT / "results/docking/benchmark_gold_exam_a/benchmark_gold_exam_a.json"
CONTRACT_MD = ROOT / "docs/thcv_design_constraints.md"

CHALLENGE_IDS = ("Qiu-14", "Qiu-15", "Qiu-16", "Qiu-20", "Qiu-24")
COMPOUND_TO_NUM = {"Qiu-14": "14", "Qiu-15": "15", "Qiu-16": "16", "Qiu-20": "20", "Qiu-24": "24"}

# Literature / Round1 labels — concordance ONLY (do not alter contract verdicts).
EXPERIMENTAL_LABELS: dict[str, dict[str, str]] = {
    "Qiu-14": {
        "cb2_cAMP": "agonist (Fig. S5A)",
        "cb1_cAMP": "antagonist (Fig. S5B)",
        "yin_yang": "claimed (paper)",
        "evidence_tag": "D qualitative / HOLD",
        "source": "Qiu2023 SI Fig. S5; Round1 CB2 Master Dataset",
    },
    "Qiu-15": {
        "cb2_cAMP": "NOT DETERMINABLE (S13 no Cpd15 OCR)",
        "cb1_cAMP": "panel present (S11); potency NF",
        "yin_yang": "NOT DETERMINABLE",
        "evidence_tag": "N / HOLD",
        "source": "qiu_0q2f_regioisomer audit; QUARANTINE Q-02",
    },
    "Qiu-16": {
        "cb2_cAMP": "panel present (S13); potency NF",
        "cb1_cAMP": "panel present (S11); potency NF",
        "yin_yang": "NOT DETERMINABLE",
        "evidence_tag": "N / HOLD; SMILES pending 0D",
        "source": "Scheme S1 OCR para-morpholine; 0D 4/4 excludes 16",
    },
    "Qiu-20": {
        "cb2_cAMP": "NOT DETERMINABLE",
        "cb1_cAMP": "NOT DETERMINABLE",
        "yin_yang": "NOT DETERMINABLE",
        "evidence_tag": "N / HOLD",
        "source": "QUARANTINE Q-03; identity 0D OK",
    },
    "Qiu-24": {
        "cb2_cAMP": "NOT DETERMINABLE",
        "cb1_cAMP": "NOT DETERMINABLE",
        "yin_yang": "NOT DETERMINABLE",
        "evidence_tag": "N / HOLD",
        "source": "QUARANTINE Q-03; identity 0D OK",
    },
}


def _load_verified_structures() -> dict[str, dict]:
    by_compound: dict[str, dict] = {}
    if not STRUCTURES_CSV.exists():
        return by_compound
    with STRUCTURES_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            by_compound[row["compound"]] = {
                "smiles": row["smiles"],
                "inchikey": row.get("inchikey", ""),
                "verified": row.get("verified", ""),
                "source": row.get("source", ""),
            }
    return by_compound


def _safe_name(compound_id: str) -> str:
    return compound_id.replace(" ", "_").replace("/", "-")


def _fmt(v: float | None, places: int = 2) -> str:
    return f"{v:.{places}f}" if v is not None else "—"


def _filter_label(result: dict, key: str) -> str:
    block = result.get(key, {})
    if block.get("blocker"):
        return "FAIL (blocker)"
    if block.get("error"):
        return f"FAIL ({block['error']})"
    return "PASS" if block.get("aggregate_pass") else "FAIL"


def _ensure_hu308_pose(out_dir: Path, vina: Path, boxes: dict, args) -> Path | None:
    """Return HU-308 CB2 docked pose path (from gold JSON or fresh dock)."""
    hu_work = out_dir / "reference" / "cb2"
    hu_docked = hu_work / "HU-308_docked.pdbqt"

    if GOLD_JSON.exists():
        payload = json.loads(GOLD_JSON.read_text(encoding="utf-8"))
        hu = next((l for l in payload["ligands"] if l["id"] == "HU-308"), None)
        if hu and hu.get("cb2", {}).get("docked_pdbqt"):
            ref = ROOT / hu["cb2"]["docked_pdbqt"]
            if ref.exists():
                return ref

    if hu_docked.exists() and not args.force:
        return hu_docked

    from scripts.run_benchmark_gold_exam_a import GOLD_LIGANDS

    hu_lig = next(l for l in GOLD_LIGANDS if l["id"] == "HU-308")
    print("[reference] Docking HU-308 CB2 for persistence proxy ...", flush=True)
    res = dock_ligand(
        smiles=hu_lig["smiles"],
        name="HU-308",
        receptor=RECEPTORS["cb2"]["receptor_pdbqt"],
        box=boxes["cb2"],
        work_dir=hu_work,
        vina_path=vina,
        exhaustiveness=args.exhaustiveness,
        num_modes=args.num_modes,
        seed=args.seed,
        ph=args.ph,
    )
    p = Path(res["docked_pdbqt"]) if res.get("docked_pdbqt") else None
    return p if p and p.exists() else None


def write_report(payload: dict, out_md: Path) -> None:
    meta = payload["meta"]
    rows = payload["compounds"]
    lines = [
        "# Blind Qiu Challenge — THCV Design Contract v1.0",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Protocol",
        "",
        "| Parámetro | Valor |",
        "|-----------|-------|",
        f"| Receptor CB1 | `{Path(meta['receptors']['cb1']).as_posix()}` |",
        f"| Receptor CB2 | `{Path(meta['receptors']['cb2']).as_posix()}` |",
        f"| Grid CB1 | `{Path(meta['grids']['cb1']).as_posix()}` |",
        f"| Grid CB2 | `{Path(meta['grids']['cb2']).as_posix()}` |",
        f"| Vina exhaustiveness | {meta['exhaustiveness']} |",
        f"| num_modes | {meta['num_modes']} |",
        f"| seed | {meta['seed']} |",
        f"| pH (Meeko) | {meta['ph']} |",
        f"| Contrato | `{meta['contract_yaml']}` |",
        "",
        "## Fuentes estructurales",
        "",
        "| Compuesto | SMILES | Fuente |",
        "|-----------|--------|--------|",
    ]
    for r in rows:
        src = r.get("structure_source") or "—"
        smi = f"`{r['smiles']}`" if r.get("smiles") else "**MISSING — blocker**"
        lines.append(f"| {r['compound_id']} | {smi} | {src} |")

    lines.extend(
        [
            "",
            "## Tabla principal (ciega — sin etiquetas biológicas)",
            "",
            "| Compuesto | Score CB1 | Score CB2 | Delta | Filtro CB1 | Filtro CB2 | TPSA (Å²) | Veredicto Contrato |",
            "|-----------|-----------|-----------|-------|------------|------------|-----------|-------------------|",
        ]
    )
    for r in rows:
        cb1 = r.get("cb1_score")
        cb2 = r.get("cb2_score")
        delta = r.get("delta_cb2_minus_cb1")
        tpsa = r.get("admet", {}).get("tpsa_A2")
        lines.append(
            f"| {r['compound_id']} | {_fmt(cb1)} | {_fmt(cb2)} | "
            f"{f'{delta:+.2f}' if delta is not None else '—'} | "
            f"{_filter_label(r, 'cb1_filter')} | {_filter_label(r, 'cb2_filter')} | "
            f"{_fmt(tpsa, 1) if tpsa is not None else '—'} | **{r.get('contract_verdict', '—')}** |"
        )

    lines.extend(
        [
            "",
            "## Proxies y limitaciones",
            "",
            "- **CB1 C3 clearance:** extensión libre antes de clash 3.0 Å a lo largo del vector "
            "adamantilo-amida (`interaction_mapping._vector_clearance`).",
            "- **CB1 C9/C11 volume delta:** |clearance C9 − clearance C3| en el mismo probe.",
            "- **CB2 C3 occupancy:** distancia mínima del término adamantilo al shell "
            "ILE110/ILE186/THR114 (envelope 2.5 Å).",
            "- **CB2 Ser285:** distancia mínima heavy ligando → OG/CB Ser285.",
            "- **Pose persistence:** separación de centroides vs HU-308 CB2 (gold / referencia).",
            "- Vina scores y proxies geométricos **no** equivalen a agonismo/antagonismo funcional.",
            "",
            "## Concordancia vs etiquetas experimentales (Round1 / HOLD — post-hoc)",
            "",
            "Las etiquetas **no** modifican el veredicto del contrato.",
            "",
            "| Compuesto | Veredicto Contrato | CB2 label (lit.) | CB1 label (lit.) | Concordancia |",
            "|-----------|-------------------|------------------|------------------|--------------|",
        ]
    )
    for r in rows:
        cid = r["compound_id"]
        lab = EXPERIMENTAL_LABELS.get(cid, {})
        conc = _concordance_note(r, lab)
        lines.append(
            f"| {cid} | {r.get('contract_verdict', '—')} | "
            f"{lab.get('cb2_cAMP', '—')} | {lab.get('cb1_cAMP', '—')} | {conc} |"
        )

    lines.extend(
        [
            "",
            "## Detalle por compuesto",
            "",
        ]
    )
    for r in rows:
        lines.append(f"### {r['compound_id']}")
        if r.get("blocker"):
            lines.append(f"- **Blocker:** {r['blocker']}")
        cb1f = r.get("cb1_filter", {})
        cb2f = r.get("cb2_filter", {})
        ad = r.get("admet", {})
        lines.extend(
            [
                f"- CB1 score: {_fmt(r.get('cb1_score'))} kcal/mol",
                f"- CB2 score: {_fmt(r.get('cb2_score'))} kcal/mol",
                f"- C3 clearance: {cb1f.get('c3_clearance_A', '—')} Å (pass={cb1f.get('c3_clearance_pass')})",
                f"- C9/C11 Δvol: {cb1f.get('c9_c11_volume_delta_A', '—')} Å",
                f"- CB2 Ser285: {cb2f.get('ser285_distance_A', '—')} Å",
                f"- HU-308 centroid Δ: {cb2f.get('hu308_centroid_separation_A', '—')} Å",
                f"- TPSA: {ad.get('tpsa_A2', '—')} Å²",
                "",
            ]
        )

    lines.extend(
        [
            f"JSON: `{meta['json_path']}`",
            f"Poses: `{meta['out_dir']}/`",
            "",
        ]
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def _concordance_note(result: dict, labels: dict) -> str:
    verdict = result.get("contract_verdict")
    if result.get("blocker"):
        return "N/A (structure blocker)"
    delta = result.get("delta_cb2_minus_cb1")
    cb2f = result.get("cb2_filter", {}).get("aggregate_pass")
    cb1f = result.get("cb1_filter", {}).get("aggregate_pass")

    if labels.get("yin_yang") == "claimed (paper)":
        # Yin-Yang expects CB2-favorable docking delta + dual filter feasibility
        if verdict == "PASS" and delta is not None and delta < 0:
            return "aligned (contract PASS + Δ(CB2−CB1)<0)"
        if delta is not None and delta < 0 and cb2f:
            return "partial (CB2 score/filter; contract global FAIL)"
        return "misaligned or indeterminate"

    if labels.get("evidence_tag", "").startswith("N"):
        return "indeterminate (literature HOLD/NF)"
    return "not scored"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results/docking/challenge_qiu_blind",
    )
    ap.add_argument("--exhaustiveness", type=int, default=16)
    ap.add_argument("--num-modes", type=int, default=9)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--force", action="store_true")
    ap.add_argument(
        "--report-only",
        action="store_true",
        help="Rebuild report/JSON from existing poses",
    )
    args = ap.parse_args()

    verified = _load_verified_structures()
    contract = load_contract()
    out_md = ROOT / "results/docking/challenge_qiu_blind_evaluation.md"
    json_path = args.out_dir / "challenge_qiu_blind_evaluation.json"

    if args.report_only:
        if not json_path.exists():
            print(f"BLOQUEO: --report-only pero falta {json_path}")
            return 2
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        write_report(payload, out_md)
        print(f"Report: {out_md}")
        return 0

    for tk, v in RECEPTORS.items():
        if not v["receptor_pdbqt"].exists():
            print(f"BLOQUEO: receptor ausente {v['receptor_pdbqt']}")
            return 2

    try:
        vina = resolve_vina(root=ROOT)
    except FileNotFoundError as exc:
        print(f"BLOQUEO: {exc}")
        return 2

    boxes = {k: _load_grid(v["grid_config"]) for k, v in RECEPTORS.items()}
    args.out_dir.mkdir(parents=True, exist_ok=True)

    hu308_cb2 = _ensure_hu308_pose(args.out_dir, vina, boxes, args)
    print(f"Vina: {vina}")
    print(f"HU-308 CB2 reference: {hu308_cb2}")

    compounds: list[dict] = []

    for cid in CHALLENGE_IDS:
        num = COMPOUND_TO_NUM[cid]
        rec = verified.get(num)
        smiles = rec["smiles"] if rec else None
        entry: dict = {
            "compound_id": cid,
            "compound_num": num,
            "smiles": smiles,
            "structure_source": (
                f"`data/libraries/qiu_0d_structures.csv` ({rec['source']})"
                if rec
                else "NOT IN 0D CSV — Scheme S1 names para-16 only"
            ),
        }

        if not smiles:
            entry["blocker"] = (
                "SMILES not in verified quarantine library "
                f"({STRUCTURES_CSV.relative_to(ROOT)}). "
                "Compound 16 identity (para-morpholine) documented in SI OCR only — do not fabricate."
            )
            evaluated = evaluate_compound(
                cid,
                None,
                None,
                None,
                RECEPTORS["cb1"]["receptor_pdb"],
                RECEPTORS["cb2"]["receptor_pdb"],
                hu308_cb2,
                contract,
            )
            entry.update(evaluated)
            compounds.append(entry)
            print(f"[{cid}] BLOCKED — no verified SMILES")
            continue

        safe = _safe_name(cid)
        row_scores: dict = {}

        for tk, tmeta in RECEPTORS.items():
            work = args.out_dir / tk
            docked = work / f"{safe}_docked.pdbqt"
            if args.force and docked.exists():
                docked.unlink()

            print(f"[{cid}] docking {tk} ...", flush=True)
            res = dock_ligand(
                smiles=smiles,
                name=cid,
                receptor=tmeta["receptor_pdbqt"],
                box=boxes[tk],
                work_dir=work,
                vina_path=vina,
                exhaustiveness=args.exhaustiveness,
                num_modes=args.num_modes,
                seed=args.seed,
                ph=args.ph,
            )
            aff = res.get("vina_affinity")
            row_scores[tk] = {
                "affinity": aff,
                "docked_pdbqt": res.get("docked_pdbqt"),
                "error": res.get("dock_error"),
            }
            if aff is not None:
                dist = {}
                if res.get("docked_pdbqt"):
                    try:
                        dist = compute_microswitch_distances(
                            Path(res["docked_pdbqt"]),
                            tmeta["receptor_pdb"],
                            tk,
                        )
                    except Exception as exc:  # noqa: BLE001
                        row_scores[tk]["error"] = str(exc)[:200]
                row_scores[tk]["microswitch_distances"] = dist
            print(f"  {tk} affinity={aff}")

        cb1_a = row_scores["cb1"]["affinity"]
        cb2_a = row_scores["cb2"]["affinity"]
        entry["cb1_score"] = cb1_a
        entry["cb2_score"] = cb2_a
        entry["delta_cb2_minus_cb1"] = (
            cb2_a - cb1_a if cb1_a is not None and cb2_a is not None else None
        )
        entry["docking"] = row_scores

        cb1_pose = Path(row_scores["cb1"]["docked_pdbqt"]) if row_scores["cb1"].get("docked_pdbqt") else None
        cb2_pose = Path(row_scores["cb2"]["docked_pdbqt"]) if row_scores["cb2"].get("docked_pdbqt") else None

        evaluated = evaluate_compound(
            cid,
            smiles,
            cb1_pose,
            cb2_pose,
            RECEPTORS["cb1"]["receptor_pdb"],
            RECEPTORS["cb2"]["receptor_pdb"],
            hu308_cb2,
            contract,
        )
        entry.update(evaluated)
        compounds.append(entry)

    meta = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "exhaustiveness": args.exhaustiveness,
        "num_modes": args.num_modes,
        "seed": args.seed,
        "ph": args.ph,
        "vina": str(vina),
        "receptors": {k: str(v["receptor_pdbqt"]) for k, v in RECEPTORS.items()},
        "grids": {k: str(v["grid_config"]) for k, v in RECEPTORS.items()},
        "structures_csv": str(STRUCTURES_CSV.relative_to(ROOT)),
        "contract_yaml": str((ROOT / "configs/thcv_design_constraints.yaml").relative_to(ROOT)),
        "contract_md": str(CONTRACT_MD.relative_to(ROOT)),
        "out_dir": str(args.out_dir.relative_to(ROOT)),
        "json_path": str(json_path.relative_to(ROOT)),
        "hu308_cb2_reference": str(hu308_cb2.relative_to(ROOT)) if hu308_cb2 else None,
        "de_novo_generation": "STOP",
    }
    payload = {"meta": meta, "compounds": compounds, "experimental_labels": EXPERIMENTAL_LABELS}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(payload, out_md)

    print(f"Report: {out_md}")
    print(f"JSON: {json_path}")
    for c in compounds:
        print(f"  {c['compound_id']}: {c.get('contract_verdict')} (blocker={bool(c.get('blocker'))})")

    docked_ok = sum(1 for c in compounds if c.get("cb1_score") is not None and c.get("cb2_score") is not None)
    return 0 if docked_ok >= 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
