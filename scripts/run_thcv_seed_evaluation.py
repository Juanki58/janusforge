#!/usr/bin/env python3
"""Experimental seed THCV vs CB1 (5TGZ) / CB2 (6PT0) — Exam A protocol.

Docks delta9-THCV only; compares scores and microswitch distances against
HU-308 and CP-55,940 from benchmark_gold_exam_a (no re-dock of gold panel).

PubChem identity: tries directive CID 62310 first; if InChIKey does not match
canonical Δ9-THCV (6aR,10aR), falls back to chemome / CID 93147.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark_gold_exam_a import (  # noqa: E402
    RECEPTORS,
    _interaction_summary,
    _load_grid,
    compute_microswitch_distances,
)
from src.screening.docking import dock_ligand, resolve_vina

CHEMOME_CSV = ROOT / "data/libraries/quimioma_semillas.csv"
GOLD_JSON = ROOT / "results/docking/benchmark_gold_exam_a/benchmark_gold_exam_a.json"
GOLD_COMPARE_IDS = ("CP-55,940", "HU-308")

DIRECTIVE_PUBCHEM_CID = 62310
CANONICAL_THCV_CID = 93147
THCV_INCHIKEY = "ZROLHBHDLIHEMS-HUUCEWRRSA-N"


def _pubchem_props(cid: int) -> dict:
    props = "IsomericSMILES,InChIKey,IUPACName,MolecularFormula"
    url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}"
        f"/property/{props}/JSON"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "janusforge/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data["PropertyTable"]["Properties"][0]


def _inchikey_for_smiles(smiles: str) -> str | None:
    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/"
        f"{urllib.parse.quote(smiles)}/property/InChIKey/JSON"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "janusforge/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data["PropertyTable"]["Properties"][0].get("InChIKey")


def check_pubchem_identity() -> dict:
    """Compare directive CID 62310 vs canonical THCV CID 93147."""
    chemome_smiles = _load_chemome_smiles()
    out: dict = {
        "directive_cid": DIRECTIVE_PUBCHEM_CID,
        "canonical_thcv_cid": CANONICAL_THCV_CID,
        "thcv_inchikey": THCV_INCHIKEY,
        "chemome_smiles": chemome_smiles,
    }
    try:
        out["directive"] = _pubchem_props(DIRECTIVE_PUBCHEM_CID)
    except urllib.error.HTTPError as exc:
        out["directive"] = {"error": str(exc)}
    try:
        out["canonical"] = _pubchem_props(CANONICAL_THCV_CID)
    except urllib.error.HTTPError as exc:
        out["canonical"] = {"error": str(exc)}

    d_ik = out.get("directive", {}).get("InChIKey")
    c_ik = out.get("canonical", {}).get("InChIKey")
    try:
        chemome_ik = _inchikey_for_smiles(chemome_smiles)
    except urllib.error.HTTPError:
        chemome_ik = None
    out["chemome_inchikey"] = chemome_ik
    out["identical_inchikey"] = d_ik is not None and d_ik == c_ik
    out["chemome_matches_canonical"] = chemome_ik == THCV_INCHIKEY
    out["directive_is_thcv"] = d_ik == THCV_INCHIKEY
    return out


def _load_chemome_smiles() -> str:
    with CHEMOME_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["name"] == "delta9-THCV":
                return row["smiles"]
    raise RuntimeError(f"delta9-THCV not found in {CHEMOME_CSV}")


def _load_thcv_ligand(identity: dict) -> dict:
    chemome_smiles = identity["chemome_smiles"]
    role = None
    with CHEMOME_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["name"] == "delta9-THCV":
                role = row["role"]
                break
    if role is None:
        raise RuntimeError(f"delta9-THCV not found in {CHEMOME_CSV}")

    if identity["directive_is_thcv"]:
        pubchem_cid = DIRECTIVE_PUBCHEM_CID
        smiles = identity["directive"].get("IsomericSMILES") or chemome_smiles
        source = (
            f"PubChem CID {DIRECTIVE_PUBCHEM_CID} (directive); "
            f"InChIKey {identity['directive'].get('InChIKey')}"
        )
        redock_needed = False
    else:
        pubchem_cid = CANONICAL_THCV_CID
        smiles = chemome_smiles
        d = identity.get("directive", {})
        source = (
            f"PubChem CID {CANONICAL_THCV_CID} (Δ9-THCV 6aR,10aR); "
            f"chemome SMILES matches InChIKey {THCV_INCHIKEY}. "
            f"Directive CID {DIRECTIVE_PUBCHEM_CID} rejected: "
            f"{d.get('IUPACName', d.get('error', 'unknown'))} "
            f"(InChIKey {d.get('InChIKey', '—')}, formula {d.get('MolecularFormula', '—')}) "
            f"— not Δ9-THCV."
        )
        # Do not re-dock with 62310 SMILES (HCFC); retain / use canonical 93147.
        redock_needed = False

    return {
        "id": "delta9-THCV (THCV)",
        "aliases": ["THCV", "delta9-THCV"],
        "role": role,
        "pubchem_cid": pubchem_cid,
        "directive_pubchem_cid": DIRECTIVE_PUBCHEM_CID,
        "inchikey": THCV_INCHIKEY,
        "smiles": smiles,
        "source": source,
        "identity_check": identity,
        "redock_needed": redock_needed,
    }


def _load_gold_comparators() -> list[dict]:
    if not GOLD_JSON.exists():
        raise FileNotFoundError(f"Gold benchmark JSON missing: {GOLD_JSON}")
    payload = json.loads(GOLD_JSON.read_text(encoding="utf-8"))
    by_id = {lig["id"]: lig for lig in payload["ligands"]}
    missing = [i for i in GOLD_COMPARE_IDS if i not in by_id]
    if missing:
        raise RuntimeError(f"Gold JSON missing comparators: {missing}")
    return [by_id[i] for i in GOLD_COMPARE_IDS]


def _fmt(v: float | None, places: int = 2) -> str:
    return f"{v:.{places}f}" if v is not None else "—"


def _contacts_summary(row: dict, tk: str) -> str:
    dist = row.get(tk, {}).get("microswitch_distances", {})
    if not dist:
        return "—"
    return _interaction_summary(dist, tk)


def write_report(
    thcv: dict,
    gold_rows: list[dict],
    meta: dict,
    out_md: Path,
) -> None:
    cb1_a = thcv["cb1"]["affinity"]
    cb2_a = thcv["cb2"]["affinity"]
    delta = thcv.get("delta_cb2_minus_cb1")
    ident = thcv.get("identity_check", {})

    lines = [
        "# THCV Seed Evaluation — CB1/CB2 (Exam A protocol)",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Verificación de identidad PubChem (62310 vs 93147)",
        "",
        "| CID | Fórmula | InChIKey | IUPAC / identidad |",
        "|-----|---------|----------|-------------------|",
    ]

    for label, key in [("62310 (directive)", "directive"), ("93147 (THCV canon)", "canonical")]:
        rec = ident.get(key, {})
        lines.append(
            f"| {label} | {rec.get('MolecularFormula', '—')} | "
            f"{rec.get('InChIKey', '—')} | {rec.get('IUPACName', rec.get('error', '—'))} |"
        )

    lines.extend(
        [
            "",
            f"- **InChIKey idénticos:** {'sí' if ident.get('identical_inchikey') else '**no**'}",
            f"- **62310 es Δ9-THCV (6aR,10aR):** {'sí' if ident.get('directive_is_thcv') else '**no**'}",
            f"- **Chemome SMILES → InChIKey:** `{ident.get('chemome_inchikey', '—')}` "
            f"(match canon: {'sí' if ident.get('chemome_matches_canonical') else 'no'})",
            f"- **Re-dock requerido:** {'no — CID 62310 no es THCV; poses CID 93147 retenidas' if not thcv.get('redock_needed') else 'sí'}",
            "",
            "## Ligando",
            "",
            f"- **ID:** {thcv['id']}",
            f"- **PubChem CID usado:** {thcv['pubchem_cid']}",
            f"- **InChIKey:** `{thcv.get('inchikey', '—')}`",
            f"- **SMILES:** `{thcv['smiles']}`",
            f"- **Fuente:** {thcv['source']}",
            f"- **Rol quimioma:** `{thcv['role']}` (semilla Janus imperfecta)",
            "",
            "## Protocolo",
            "",
            "| Parámetro | Valor |",
            "|-----------|-------|",
            f"| Vina exhaustiveness | {meta['exhaustiveness']} |",
            f"| num_modes | {meta['num_modes']} |",
            f"| seed | {meta['seed']} |",
            f"| pH ligando | {meta['ph']} |",
            f"| Prep ligando | Meeko pH 7.4, Gasteiger, mínima energía (seed={meta['seed']}) |",
            f"| Receptor CB1 | `{meta['receptors']['cb1']}` |",
            f"| Receptor CB2 | `{meta['receptors']['cb2']}` |",
            f"| Grid CB1 | `{meta['grids']['cb1']}` |",
            f"| Grid CB2 | `{meta['grids']['cb2']}` |",
            "",
            "## Scores THCV",
            "",
            "| Receptor | Vina score (kcal/mol) |",
            "|----------|----------------------|",
            f"| CB1 (5TGZ) | {_fmt(cb1_a)} |",
            f"| CB2 (6PT0) | {_fmt(cb2_a)} |",
            f"| **Delta (CB2 − CB1)** | **{_fmt(delta, 2) if delta is not None else '—'}** |",
            "",
            "## Comparación vs Gold Exam A (HU-308, CP-55,940)",
            "",
            "Scores Gold reutilizados de "
            f"`{GOLD_JSON.relative_to(ROOT)}` — **sin re-dock**.",
            "",
            "| Ligando | Score CB1 (5TGZ) | Score CB2 (6PT0) | Delta (CB2 - CB1) | Contactos CB1 | Contactos CB2 |",
            "|---------|----------------|------------------|-------------------|---------------|---------------|",
        ]
    )

    all_rows = [thcv] + [
        {
            "id": g["id"],
            "cb1": g["cb1"],
            "cb2": g["cb2"],
            "delta_cb2_minus_cb1": g.get("delta_cb2_minus_cb1"),
            "interactions_summary": g.get("interactions_summary", ""),
        }
        for g in gold_rows
    ]
    for r in all_rows:
        cb1 = r["cb1"]["affinity"]
        cb2 = r["cb2"]["affinity"]
        d = r.get("delta_cb2_minus_cb1")
        if d is None and cb1 is not None and cb2 is not None:
            d = cb2 - cb1
        cb1_cont = _contacts_summary(r, "cb1")
        cb2_cont = _contacts_summary(r, "cb2")
        if r.get("interactions_summary") and r["id"] != thcv["id"]:
            parts = r["interactions_summary"].split(" | ")
            cb1_cont = parts[0].removeprefix("CB1: ") if parts else cb1_cont
            cb2_cont = parts[1].removeprefix("CB2: ") if len(parts) > 1 else cb2_cont
        lines.append(
            f"| {r['id']} | {_fmt(cb1)} | {_fmt(cb2)} | "
            f"{f'{d:+.2f}' if d is not None else '—'} | "
            f"{cb1_cont} | {cb2_cont} |"
        )

    lines.extend(
        [
            "",
            "### Microswitch distances (Å)",
            "",
            "| Ligando | CB1 Phe200 | CB1 Trp356 | CB2 Phe117 | CB2 Trp258 | CB2 Ser285 |",
            "|---------|------------|------------|------------|------------|------------|",
        ]
    )
    for r in all_rows:
        cb1d = r["cb1"].get("microswitch_distances", {})
        cb2d = r["cb2"].get("microswitch_distances", {})
        lines.append(
            f"| {r['id']} | "
            f"{_fmt(cb1d.get('Phe200(3.36)'))} | "
            f"{_fmt(cb1d.get('Trp356(6.48)'))} | "
            f"{_fmt(cb2d.get('Phe117(3.32)'))} | "
            f"{_fmt(cb2d.get('Trp258(6.48)'))} | "
            f"{_fmt(cb2d.get('Ser285(7.39)'))} |"
        )

    if cb1_a is not None and cb2_a is not None:
        hu = next(g for g in gold_rows if g["id"] == "HU-308")
        cp = next(g for g in gold_rows if g["id"] == "CP-55,940")
        lines.extend(
            [
                "",
                "## Interpretación breve",
                "",
                f"- THCV Δ(CB2−CB1) = **{delta:+.2f} kcal/mol** "
                f"(HU-308: {hu['delta_cb2_minus_cb1']:+.2f}; "
                f"CP-55,940: {cp['delta_cb2_minus_cb1']:+.2f}).",
            ]
        )
        if delta is not None:
            if delta < hu["delta_cb2_minus_cb1"]:
                lines.append(
                    "- THCV muestra mayor sesgo CB2 relativo que HU-308 por score Vina."
                )
            elif delta > hu["delta_cb2_minus_cb1"]:
                lines.append(
                    "- THCV muestra menor sesgo CB2 relativo que HU-308 por score Vina."
                )
            else:
                lines.append("- THCV y HU-308 comparten el mismo delta CB2−CB1 en este run.")

    if not ident.get("directive_is_thcv"):
        lines.extend(
            [
                "",
                f"- **Nota CID:** PubChem CID {DIRECTIVE_PUBCHEM_CID} "
                f"({ident.get('directive', {}).get('IUPACName', '?')}) "
                "no es Δ9-THCV; docking usa CID 93147 / chemome.",
            ]
        )

    lines.extend(
        [
            "",
            "- **5TGZ (CB1):** estructura antagonista-bound (AM6538); scores de agonistas/antagonistas pueden estar sesgados.",
            "- **6PT0 (CB2):** estructura agonista-bound (WIN 55,212-2).",
            "- Distancias ≤4 Å ≈ contacto directo con microswitch.",
            "",
            f"Poses: `{meta['out_dir']}/cb1/`, `{meta['out_dir']}/cb2/`",
            f"JSON: `{meta['json_path']}`",
            "",
        ]
    )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results/docking/thcv_seed",
    )
    ap.add_argument("--exhaustiveness", type=int, default=16)
    ap.add_argument("--num-modes", type=int, default=9)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--force", action="store_true", help="Re-dock even if poses exist")
    ap.add_argument(
        "--report-only",
        action="store_true",
        help="Skip docking; refresh report/JSON from existing poses",
    )
    args = ap.parse_args()

    identity = check_pubchem_identity()
    lig = _load_thcv_ligand(identity)
    gold_rows = _load_gold_comparators()

    print("=== PubChem identity check ===")
    print(f"  CID {DIRECTIVE_PUBCHEM_CID}: {identity.get('directive', {}).get('IUPACName')}")
    print(f"  CID {CANONICAL_THCV_CID}: {identity.get('canonical', {}).get('IUPACName')}")
    print(f"  Identical InChIKey: {identity['identical_inchikey']}")
    print(f"  Directive is THCV: {identity['directive_is_thcv']}")
    print(f"  Using CID: {lig['pubchem_cid']}")
    print(f"  Re-dock needed: {lig['redock_needed']}")

    if args.report_only:
        json_path = args.out_dir / "thcv_seed_evaluation.json"
        if not json_path.exists():
            print(f"BLOQUEO: --report-only pero falta {json_path}")
            return 2
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        row = payload["thcv"]
        row["identity_check"] = identity
        row["redock_needed"] = lig["redock_needed"]
        row["source"] = lig["source"]
        row["pubchem_cid"] = lig["pubchem_cid"]
        meta = payload["meta"]
        meta["identity_check"] = identity
        meta["generated_utc"] = datetime.now(timezone.utc).isoformat()
        json_path.write_text(
            json.dumps({"meta": meta, "thcv": row, "gold_comparators": payload["gold_comparators"]}, indent=2),
            encoding="utf-8",
        )
        md_path = ROOT / "results/docking/thcv_seed_evaluation.md"
        write_report(row, gold_rows, meta, md_path)
        print(f"Report: {md_path}")
        return 0

    try:
        vina = resolve_vina(root=ROOT)
    except FileNotFoundError as exc:
        print(f"BLOQUEO: {exc}")
        return 2

    for k, v in RECEPTORS.items():
        if not v["receptor_pdbqt"].exists():
            print(f"BLOQUEO: receptor ausente {v['receptor_pdbqt']}")
            return 2
        if not v["receptor_pdb"].exists():
            print(f"BLOQUEO: PDB limpio ausente {v['receptor_pdb']}")
            return 2

    boxes = {k: _load_grid(v["grid_config"]) for k, v in RECEPTORS.items()}

    args.out_dir.mkdir(parents=True, exist_ok=True)
    safe = "delta9-THCV"

    row: dict = {
        "id": lig["id"],
        "role": lig["role"],
        "pubchem_cid": lig["pubchem_cid"],
        "directive_pubchem_cid": lig["directive_pubchem_cid"],
        "inchikey": lig["inchikey"],
        "smiles": lig["smiles"],
        "source": lig["source"],
        "identity_check": identity,
        "redock_needed": lig["redock_needed"],
    }

    print(f"Vina: {vina}")
    print(f"THCV SMILES: {lig['smiles']}")
    print(
        f"exhaustiveness={args.exhaustiveness} num_modes={args.num_modes} "
        f"seed={args.seed} ph={args.ph}"
    )

    for tk, tmeta in RECEPTORS.items():
        work = args.out_dir / tk
        docked = work / f"{safe}_docked.pdbqt"
        alt = list(work.glob(f"{safe}*_docked.pdbqt"))
        if args.force:
            for p in [docked, *alt]:
                if p.exists():
                    p.unlink()

        print(f"[{tk}] {lig['id']} ...", flush=True)
        res = dock_ligand(
            smiles=lig["smiles"],
            name=lig["id"],
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
        dist: dict[str, float] = {}
        err = res.get("dock_error")
        if aff is not None and res.get("docked_pdbqt"):
            try:
                dist = compute_microswitch_distances(
                    Path(res["docked_pdbqt"]),
                    tmeta["receptor_pdb"],
                    tk,
                )
            except Exception as exc:  # noqa: BLE001
                err = f"distances: {exc}"[:200]

        row[tk] = {
            "affinity": aff,
            "error": err,
            "docked_pdbqt": res.get("docked_pdbqt"),
            "microswitch_distances": dist,
        }
        print(f"  {tk} affinity={aff} err={err}")

    cb1_a = row["cb1"]["affinity"]
    cb2_a = row["cb2"]["affinity"]
    inter_parts: list[str] = []
    if row["cb1"]["microswitch_distances"]:
        inter_parts.append(
            "CB1: " + _interaction_summary(row["cb1"]["microswitch_distances"], "cb1")
        )
    if row["cb2"]["microswitch_distances"]:
        inter_parts.append(
            "CB2: " + _interaction_summary(row["cb2"]["microswitch_distances"], "cb2")
        )
    row["interactions_summary"] = " | ".join(inter_parts) if inter_parts else "—"
    row["delta_cb2_minus_cb1"] = (
        cb2_a - cb1_a if cb1_a is not None and cb2_a is not None else None
    )

    json_path = args.out_dir / "thcv_seed_evaluation.json"
    md_path = ROOT / "results/docking/thcv_seed_evaluation.md"
    meta = {
        "exhaustiveness": args.exhaustiveness,
        "num_modes": args.num_modes,
        "seed": args.seed,
        "ph": args.ph,
        "vina": str(vina),
        "receptors": {k: str(v["receptor_pdbqt"]) for k, v in RECEPTORS.items()},
        "grids": {k: str(v["grid_config"]) for k, v in RECEPTORS.items()},
        "out_dir": str(args.out_dir.relative_to(ROOT)),
        "json_path": str(json_path.relative_to(ROOT)),
        "gold_benchmark_json": str(GOLD_JSON.relative_to(ROOT)),
        "identity_check": identity,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    payload = {
        "meta": meta,
        "thcv": row,
        "gold_comparators": {g["id"]: g for g in gold_rows},
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(row, gold_rows, meta, md_path)

    print(f"Report: {md_path}")
    print(f"JSON: {json_path}")
    ok = cb1_a is not None and cb2_a is not None
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
