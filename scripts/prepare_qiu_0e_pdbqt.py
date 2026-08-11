#!/usr/bin/env python3
"""Qiu 0E — PDBQT preparation only (compounds 14/15/20/24). No docking.

Verifies MolFromSmiles connectivity against 0D (canonical SMILES + InChI),
embeds 3D (ETKDG + MMFF/UFF), writes Meeko PDBQT. Neutral as drawn (no
dimorphite — no COOH); morpholine/piperazine tertiary amines kept neutral
unless Meeko alters charge explicitly (documented).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import inchi

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chemistry.prepare_ligands import smiles_to_pdbqt

# Exact 0D SMILES / InChI / InChIKey (PASS 4/4) — do not alter connectivity.
COMPOUNDS: list[dict] = [
    {
        "id": 14,
        "name": "compound_14",
        "smiles": (
            "Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1"
        ),
        "inchi_0d": (
            "InChI=1S/C31H36N4O2/c1-21-28(30(36)32-31-18-22-15-23(19-31)17-24(16-22)"
            "20-31)33-35(29(21)25-7-3-2-4-8-25)27-10-6-5-9-26(27)34-11-13-37-14-12-34"
            "/h2-10,22-24H,11-20H2,1H3,(H,32,36)"
        ),
        "inchikey_0d": "QQXQVTJJXRACOB-UHFFFAOYSA-N",
        "note": "o-morpholine tertiary amine; neutral as drawn (pKa conj. acid ~8)",
    },
    {
        "id": 15,
        "name": "compound_15",
        "smiles": (
            "Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2cccc(N3CCOCC3)c2)c1-c1ccccc1"
        ),
        "inchi_0d": (
            "InChI=1S/C31H36N4O2/c1-21-28(30(36)32-31-18-22-14-23(19-31)16-24(15-22)"
            "20-31)33-35(29(21)25-6-3-2-4-7-25)27-9-5-8-26(17-27)34-10-12-37-13-11-34"
            "/h2-9,17,22-24H,10-16,18-20H2,1H3,(H,32,36)"
        ),
        "inchikey_0d": "ZVVBFOFPAAUAGH-UHFFFAOYSA-N",
        "note": "m-morpholine tertiary amine; neutral as drawn",
    },
    {
        "id": 20,
        "name": "compound_20",
        "smiles": (
            "Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCN(C)CC2)c1-c1ccccc1"
        ),
        "inchi_0d": (
            "InChI=1S/C32H39N5O/c1-22-29(31(38)33-32-19-23-16-24(20-32)18-25(17-23)"
            "21-32)34-37(30(22)26-8-4-3-5-9-26)28-11-7-6-10-27(28)36-14-12-35(2)"
            "13-15-36/h3-11,23-25H,12-21H2,1-2H3,(H,33,38)"
        ),
        "inchikey_0d": "ZWCGYXUFIUXGBQ-UHFFFAOYSA-N",
        "note": "o-(4-methylpiperazine); N-Me + aniline-N kept neutral as drawn",
    },
    {
        "id": 24,
        "name": "compound_24",
        "smiles": (
            "Cc1c(C(=O)NCC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1"
        ),
        "inchi_0d": (
            "InChI=1S/C32H38N4O2/c1-22-29(31(37)33-21-32-18-23-15-24(19-32)17-25"
            "(16-23)20-32)34-36(30(22)26-7-3-2-4-8-26)28-10-6-5-9-27(28)35-11-13"
            "-38-14-12-35/h2-10,23-25H,11-21H2,1H3,(H,33,37)"
        ),
        "inchikey_0d": "RAQAMHLYXWAFRF-UHFFFAOYSA-N",
        "note": "o-morpholine + adamantylmethyl amide; neutral as drawn",
    },
]


def verify_0d(cpd: dict) -> dict:
    """Match connectivity to 0D report (canonical SMILES + InChI + InChIKey)."""
    mol = Chem.MolFromSmiles(cpd["smiles"])
    if mol is None:
        raise ValueError(f"compound_{cpd['id']}: MolFromSmiles failed")
    can = Chem.MolToSmiles(mol, canonical=True)
    # Round-trip: parse canonical → same InChI (connectivity preserved)
    mol2 = Chem.MolFromSmiles(can)
    if mol2 is None:
        raise RuntimeError(f"compound_{cpd['id']}: canonical SMILES reparse failed")
    can2 = Chem.MolToSmiles(mol2, canonical=True)
    got_inchi = inchi.MolToInchi(mol)
    got_key = inchi.MolToInchiKey(mol)
    smiles_ok = can == can2
    inchi_ok = got_inchi == cpd["inchi_0d"]
    key_ok = got_key == cpd["inchikey_0d"]
    if not (smiles_ok and inchi_ok and key_ok):
        raise RuntimeError(
            f"compound_{cpd['id']}: 0D mismatch "
            f"smiles_ok={smiles_ok} inchi_ok={inchi_ok} key_ok={key_ok}\n"
            f"  got InChI: {got_inchi}\n"
            f"  exp InChI: {cpd['inchi_0d']}\n"
            f"  got Key: {got_key} exp Key: {cpd['inchikey_0d']}"
        )
    formal = sum(a.GetFormalCharge() for a in mol.GetAtoms())
    return {
        "canonical_smiles": can,
        "inchi": got_inchi,
        "inchikey": got_key,
        "formal_charge_2d": formal,
        "n_heavy_2d": mol.GetNumHeavyAtoms(),
        "verify_0d_ok": True,
    }


def _parse_pdbqt_qc(path: Path, expected_name: str) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    atom_lines = [
        ln
        for ln in text.splitlines()
        if ln.startswith(("ATOM", "HETATM"))
    ]
    n_atoms = len(atom_lines)
    # Residue / name hints from REMARK or root name
    remarks = [ln for ln in text.splitlines() if ln.startswith("REMARK")]
    name_hits = [
        ln
        for ln in text.splitlines()
        if expected_name in ln or expected_name.replace("_", "") in ln
    ]
    # Meeko often uses residue UNL; count unique residue names in cols 18-20
    resnames: set[str] = set()
    for ln in atom_lines:
        if len(ln) >= 20:
            resnames.add(ln[17:20].strip())
    # Sum partial charges (cols 71-76 typical PDBQT)
    charges = []
    for ln in atom_lines:
        parts = ln.split()
        if len(parts) >= 9:
            try:
                charges.append(float(parts[-2]))
            except ValueError:
                pass
    total_q = round(sum(charges), 3) if charges else None
    # File basename maps to compound ID
    stem_ok = path.stem.startswith(expected_name) or expected_name in path.name
    qc_ok = n_atoms > 0 and stem_ok and path.stat().st_size > 0
    return {
        "n_atoms_pdbqt": n_atoms,
        "resnames": sorted(resnames),
        "total_partial_charge": total_q,
        "remarks_n": len(remarks),
        "name_in_file": bool(name_hits) or stem_ok,
        "qc_ok": qc_ok,
    }


def prepare_one(cpd: dict, out_dir: Path, seed: int, ph: float) -> dict:
    v = verify_0d(cpd)
    name = cpd["name"]
    pdbqt_path = out_dir / f"{name}_lig.pdbqt"
    sdf_path = out_dir / f"{name}_lig.sdf"

    meta = smiles_to_pdbqt(
        cpd["smiles"],
        pdbqt_path,
        name=name,
        seed=seed,
        ph=ph,
        sdf_path=sdf_path,
    )
    # Formal charge after protonation path (should stay 0 — no COOH → no dimorphite)
    mol_used = Chem.MolFromSmiles(meta["smiles_docked"])
    total_charge = (
        sum(a.GetFormalCharge() for a in mol_used.GetAtoms()) if mol_used else None
    )
    qc = _parse_pdbqt_qc(pdbqt_path, name)

    # Protonation documentation
    protonation = (
        f"{meta['protonation']}; keep as drawn (neutral tertiary amines); "
        f"{cpd['note']}; dimorphite=N/A (no COOH)"
    )

    row = {
        "compound": cpd["id"],
        "name": name,
        "smiles_input": cpd["smiles"],
        "canonical_smiles": v["canonical_smiles"],
        "inchi": v["inchi"],
        "verify_0d_ok": v["verify_0d_ok"],
        "protonation": protonation,
        "protonation_tag": meta["protonation"],
        "total_charge": total_charge,
        "n_atoms": qc["n_atoms_pdbqt"],
        "n_heavy_2d": v["n_heavy_2d"],
        "pdbqt": str(pdbqt_path.relative_to(ROOT)).replace("\\", "/"),
        "sdf": str(sdf_path.relative_to(ROOT)).replace("\\", "/"),
        "resnames": qc["resnames"],
        "total_partial_charge": qc["total_partial_charge"],
        "qc_ok": qc["qc_ok"] and v["verify_0d_ok"] and total_charge == 0,
        "error": None,
    }
    return row


def write_report(rows: list[dict], report_path: Path) -> str:
    n_ok = sum(1 for r in rows if r.get("qc_ok") and not r.get("error"))
    n = len(rows)
    status = f"PASS {n_ok}/{n}" if n_ok == n else f"NEEDS REVIEW ({n_ok}/{n} OK)"
    lines = [
        "# Paso 0E — Preparación PDBQT Qiu 2023 (compuestos 14, 15, 20, 24)",
        "",
        "> Estricto: **solo** PDBQT / 3D prep. Sin Vina, sin receptor, sin grids, sin docking.",
        "> Conectividad = 0D PASS (`results/reports/qiu_0d_structure_verification.md`).",
        "> Fecha: 2026-08-11.",
        "",
        "## Estado global",
        "",
        f"**0E = {status}**",
        "",
        "## Método",
        "",
        "1. Import SMILES exactos 0D (RDKit `MolFromSmiles`).",
        "2. Verify: canonical SMILES self-consistent + InChI match to 0D table.",
        "3. Embed 3D: ETKDGv3 + MMFF (fallback UFF) — coordenadas only; sin cambiar "
        "conectividad/tautómero.",
        "4. Protonación: ruta janusforge `prepare_ligands.smiles_to_pdbqt` / Meeko "
        "`MoleculePreparation` + `PDBQTWriterLegacy`. Sin ácido carboxílico → "
        "**sin dimorphite**; aminas terciarias (morfolina / N-metilpiperazina) "
        "**neutras como dibujadas** a pH 7.4 (carga formal total 0).",
        "5. PDBQT independientes bajo `results/docking/qiu_0e/`.",
        "6. QC: reload PDBQT, contar ATOM/HETATM, residue names, basename → compound ID.",
        "",
        "Script: `scripts/prepare_qiu_0e_pdbqt.py`",
        "",
        "## Tabla 0E",
        "",
        "| Compound | input SMILES | protonation | total charge | n_atoms | pdbqt path | QC OK |",
        "|----------|--------------|-------------|--------------|---------|------------|-------|",
    ]
    for r in rows:
        if r.get("error"):
            lines.append(
                f"| {r['compound']} | `{r.get('smiles_input', '')}` | ERROR | — | — | "
                f"{r.get('pdbqt', '—')} | **NO** |"
            )
            continue
        prot_short = "neutral as drawn (no dimorphite; tertiary amines)"
        qc = "**YES**" if r["qc_ok"] else "**NO**"
        lines.append(
            f"| {r['compound']} | `{r['smiles_input']}` | {prot_short} | "
            f"{r['total_charge']} | {r['n_atoms']} | `{r['pdbqt']}` | {qc} |"
        )

    lines += [
        "",
        "## Detalle QC / protonación",
        "",
    ]
    for r in rows:
        lines.append(f"### Compound {r['compound']} (`{r.get('name', '')}`)")
        lines.append("")
        if r.get("error"):
            lines.append(f"- ERROR: {r['error']}")
            lines.append("")
            continue
        lines.extend(
            [
                f"- 0D InChI match: {'YES' if r['verify_0d_ok'] else 'NO'}",
                f"- Protonation tag: `{r['protonation_tag']}`",
                f"- Note: {r['protonation']}",
                f"- Formal charge (post-prep SMILES): {r['total_charge']}",
                f"- Meeko partial-charge sum: {r.get('total_partial_charge')}",
                f"- n_heavy (2D): {r['n_heavy_2d']}; n_atoms PDBQT (H included): {r['n_atoms']}",
                f"- Residue names in PDBQT: {', '.join(r.get('resnames') or [])}",
                f"- SDF intermediate: `{r['sdf']}`",
                f"- QC OK: {'YES' if r['qc_ok'] else 'NO'}",
                "",
            ]
        )

    lines += [
        "## Artefactos",
        "",
        "- PDBQT / SDF: `results/docking/qiu_0e/` (gitignored `*.pdbqt`; SDF local).",
        "- Meta JSON: `results/docking/qiu_0e/qiu_0e_meta.json` (local).",
        "- Report (público): este archivo.",
        "",
        "## Notas",
        "",
        "- SMILES públicos (publicados Qiu 2023 / verificados en 0D).",
        "- Piperazina/morfolina: a pH fisiológico una fracción puede estar "
        "protonada; aquí se conserva la forma **neutra dibujada** (consistente "
        "con 0D y con `prepare_ligands` sin COOH → sin dimorphite).",
        "- Sin docking en este paso.",
        "",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return status


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "results/docking/qiu_0e",
    )
    ap.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results/reports/qiu_0e_pdbqt_preparation.md",
    )
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--seed", type=int, default=0xF00D)
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for cpd in COMPOUNDS:
        print(f"  prepare compound_{cpd['id']} ...", flush=True)
        try:
            row = prepare_one(cpd, args.out_dir, seed=args.seed, ph=args.ph)
            print(
                f"    OK charge={row['total_charge']} n_atoms={row['n_atoms']} "
                f"qc={row['qc_ok']}",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            row = {
                "compound": cpd["id"],
                "name": cpd["name"],
                "smiles_input": cpd["smiles"],
                "pdbqt": str(
                    (args.out_dir / f"{cpd['name']}_lig.pdbqt").relative_to(ROOT)
                ).replace("\\", "/"),
                "error": str(exc)[:400],
                "qc_ok": False,
            }
            print(f"    FAIL: {exc}", flush=True)
        rows.append(row)

    meta_path = args.out_dir / "qiu_0e_meta.json"
    meta_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    status = write_report(rows, args.report)
    print(f"0E = {status}")
    print(f"Report: {args.report}")
    print(f"Meta: {meta_path}")
    n_ok = sum(1 for r in rows if r.get("qc_ok") and not r.get("error"))
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
