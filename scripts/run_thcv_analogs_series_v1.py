#!/usr/bin/env python3
"""THCV analog series V1.0 — generate, dock CB1/CB2, ADMET, report.

Base scaffold: delta9-THCV (6aR,10aR) PubChem CID 93147 / chemome SMILES.
Does NOT touch Round 1.1/1.2 certified datasets or Qiu blind set.
Excludes AM1710 / GW405833 by design (not in panel).

Serie V1 (C3-Mod), V2 (C1-SoftDrug), V3 (C9/C11-Polar) — 12 analogs + parent ref.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, rdMolDescriptors

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark_gold_exam_a import RECEPTORS, _load_grid  # noqa: E402
from src.chemistry.prepare_ligands import smiles_to_pdbqt  # noqa: E402
from src.screening.docking import dock_ligand, resolve_vina  # noqa: E402

CHEMOME_CSV = ROOT / "data/libraries/quimioma_semillas.csv"
THCV_INCHIKEY = "ZROLHBHDLIHEMS-HUUCEWRRSA-N"
CANONICAL_THCV_CID = 93147

# Atom-mapping notes (cannabinoid numbering on delta9-THCV 6aR,10aR):
# - C3 alkyl: n-propyl on resorcinol ring A (SMILES prefix CCCc… / CCCC legacy).
# - C1 phenol: free OH on ring A (position ortho to C3 chain in quimioma SMILES).
# - C9/C11: methyl on bridgehead terpenoid ring → 11-hydroxymethyl / 11-carboxylate
#   (THC metabolite pattern mapped to gem-dimethyl bridgehead carbon in SMILES core).
THCV_CORE_PHENOL = (
    "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)O"
)
THCV_CORE_11OH = (
    "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)CO)C)O"
)

ANALOGS: tuple[dict, ...] = (
    # --- Serie V1: C3-Mod ---
    {
        "id": "THCV-01",
        "series": "V1-C3",
        "modification": "C3 = 1',1'-dimethylpropyl (neopentyl)",
        "smiles": (
            "CC(C)(C)CC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)O"
        ),
    },
    {
        "id": "THCV-02",
        "series": "V1-C3",
        "modification": "C3 = cyclopropylmethyl",
        "smiles": (
            "C1CC1CC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)O"
        ),
    },
    {
        "id": "THCV-03",
        "series": "V1-C3",
        "modification": "C3 = 3-fluoropropyl (-CH2-CH2-CH2-F)",
        "smiles": (
            "CCC(F)c1cc(O)c2c(c1)OC(C)(C)[C@@H]1CCC(C)=C[C@@H]21"
        ),
    },
    {
        "id": "THCV-04",
        "series": "V1-C3",
        "modification": "C3 = methylpropyl ether (-CH2-O-Et)",
        "smiles": (
            "CCOCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)O"
        ),
    },
    # --- Serie V2: C1-SoftDrug ---
    {
        "id": "THCV-05",
        "series": "V2-C1",
        "modification": "C1 = O-isobutyrate (soft-drug ester)",
        "smiles": (
            "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)OC(=O)C(C)C"
        ),
    },
    {
        "id": "THCV-06",
        "series": "V2-C1",
        "modification": "C1 = O-cyclopentanecarboxylate (soft-drug ester)",
        "smiles": (
            "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)OC(=O)C2CCCC2"
        ),
    },
    {
        "id": "THCV-07",
        "series": "V2-C1",
        "modification": "C1 = O-acetate (soft-drug ester)",
        "smiles": (
            "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)OC(=O)C"
        ),
    },
    {
        "id": "THCV-08",
        "series": "V2-C1",
        "modification": (
            "Cleaved C1 metabolite control — free phenol (= parent THCV; "
            "expected plasma esterase product of THCV-05/06/07)"
        ),
        "smiles": THCV_CORE_PHENOL,
    },
    # --- Serie V3: C9/C11-Polar ---
    {
        "id": "THCV-09",
        "series": "V3-C11",
        "modification": "C11 = 11-hydroxymethyl (-CH2OH)",
        "smiles": THCV_CORE_11OH,
    },
    {
        "id": "THCV-10",
        "series": "V3-C11",
        "modification": "C11 = 11-carboxylate (-COOH)",
        "smiles": (
            "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C(=O)O)C)O"
        ),
    },
    {
        "id": "THCV-11",
        "series": "V3-C11",
        "modification": "Hybrid: 11-CH2OH + C3 = 1',1'-dimethylpropyl",
        "smiles": (
            "CC(C)(C)CC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)CO)C)O"
        ),
    },
    {
        "id": "THCV-12",
        "series": "V3-C11",
        "modification": "Hybrid: 11-CH2OH + C1 = O-isobutyrate",
        "smiles": (
            "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)CO)C)OC(=O)C(C)C"
        ),
    },
)

PARENT_REF = {
    "id": "delta9-THCV (parent)",
    "series": "ref",
    "modification": "Parent scaffold (CID 93147 / chemome); C3=n-propyl, C1=OH, C9-methyl",
    "smiles": THCV_CORE_PHENOL,
    "pubchem_cid": CANONICAL_THCV_CID,
    "inchikey": THCV_INCHIKEY,
}

# Peripheral filter (documented rule-of-thumb for CNS liability / periphery hypothesis):
# PASS if TPSA > 70 Å² OR (TPSA > 55 AND cLogP < 4.0 AND MW > 300).
# Primary gate per directive: TPSA > 70 Å².
PERIPHERAL_TPSA_THRESHOLD = 70.0


def _load_chemome_thcv_smiles() -> str:
    with CHEMOME_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["name"] == "delta9-THCV":
                return row["smiles"]
    raise RuntimeError(f"delta9-THCV not found in {CHEMOME_CSV}")


def validate_smiles(smiles: str) -> tuple[Chem.Mol, str]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"RDKit parse failed: {smiles}")
    canonical = Chem.MolToSmiles(mol, isomericSmiles=True)
    try:
        Chem.SanitizeMol(mol)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Sanitize failed: {exc}") from exc
    return mol, canonical


def compute_descriptors(mol: Chem.Mol) -> dict:
    tpsa = Descriptors.TPSA(mol)
    clogp = Crippen.MolLogP(mol)
    mw = Descriptors.ExactMolWt(mol)
    rot = Descriptors.NumRotatableBonds(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    return {
        "tpsa": round(tpsa, 2),
        "clogp": round(clogp, 2),
        "mw": round(mw, 2),
        "rotatable_bonds": rot,
        "hbd": hbd,
        "hba": hba,
    }


def peripheral_filter(desc: dict) -> tuple[bool, str]:
    tpsa = desc["tpsa"]
    clogp = desc["clogp"]
    mw = desc["mw"]
    if tpsa > PERIPHERAL_TPSA_THRESHOLD:
        return True, f"PASS (TPSA {tpsa:.1f} > {PERIPHERAL_TPSA_THRESHOLD:.0f})"
    if tpsa > 55 and clogp < 4.0 and mw > 300:
        return True, f"PASS* (TPSA {tpsa:.1f}, cLogP {clogp:.1f}, MW {mw:.0f}; secondary rule)"
    return False, f"FAIL (TPSA {tpsa:.1f} ≤ {PERIPHERAL_TPSA_THRESHOLD:.0f})"


def build_library(parent_smiles: str) -> list[dict]:
    """Validate all analogs; parent SMILES must match chemome."""
    if Chem.MolToSmiles(Chem.MolFromSmiles(parent_smiles), isomericSmiles=True) != Chem.MolToSmiles(
        Chem.MolFromSmiles(PARENT_REF["smiles"]), isomericSmiles=True
    ):
        # Allow equivalent tautomers — compare InChI keys
        ik_a = Chem.MolToInchiKey(Chem.MolFromSmiles(parent_smiles))
        ik_b = Chem.MolToInchiKey(Chem.MolFromSmiles(PARENT_REF["smiles"]))
        if ik_a != ik_b:
            raise RuntimeError(
                f"Parent SMILES mismatch vs chemome.\n  chemome: {parent_smiles}\n  built: {PARENT_REF['smiles']}"
            )

    library: list[dict] = []
    for spec in ANALOGS:
        mol, canonical = validate_smiles(spec["smiles"])
        desc = compute_descriptors(mol)
        periph_pass, periph_note = peripheral_filter(desc)
        library.append(
            {
                **spec,
                "canonical_smiles": canonical,
                "inchikey": Chem.MolToInchiKey(mol),
                "descriptors": desc,
                "peripheral_pass": periph_pass,
                "peripheral_note": periph_note,
                "smiles_valid": True,
            }
        )
    # Parent reference row (not counted in the 12 analogs)
    pmol, pcanon = validate_smiles(parent_smiles)
    pdesc = compute_descriptors(pmol)
    pp, pn = peripheral_filter(pdesc)
    library.insert(
        0,
        {
            **PARENT_REF,
            "canonical_smiles": pcanon,
            "inchikey": Chem.MolToInchiKey(pmol),
            "descriptors": pdesc,
            "peripheral_pass": pp,
            "peripheral_note": pn,
            "smiles_valid": True,
        },
    )
    return library


def write_smiles_csv(library: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "id",
        "series",
        "modification",
        "smiles",
        "canonical_smiles",
        "inchikey",
        "mw",
        "tpsa",
        "clogp",
        "rotatable_bonds",
        "peripheral_pass",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for row in library:
            d = row["descriptors"]
            w.writerow(
                {
                    "id": row["id"],
                    "series": row["series"],
                    "modification": row["modification"],
                    "smiles": row["smiles"],
                    "canonical_smiles": row["canonical_smiles"],
                    "inchikey": row["inchikey"],
                    "mw": d["mw"],
                    "tpsa": d["tpsa"],
                    "clogp": d["clogp"],
                    "rotatable_bonds": d["rotatable_bonds"],
                    "peripheral_pass": row["peripheral_pass"],
                }
            )


def prep_ligand_pdbs(
    library: list[dict],
    out_dir: Path,
    seed: int,
    ph: float,
) -> None:
    lig_dir = out_dir / "ligands"
    lig_dir.mkdir(parents=True, exist_ok=True)
    for row in library:
        safe = row["id"].replace(" ", "_").replace("/", "-")
        pdbqt = lig_dir / f"{safe}_lig.pdbqt"
        if pdbqt.exists():
            continue
        smiles_to_pdbqt(
            row["canonical_smiles"],
            pdbqt,
            name=row["id"],
            seed=seed,
            ph=ph,
            sdf_path=lig_dir / f"{safe}_lig.sdf",
        )


def dock_library(
    library: list[dict],
    out_dir: Path,
    vina: Path,
    boxes: dict,
    exhaustiveness: int,
    num_modes: int,
    seed: int,
    ph: float,
    force: bool,
) -> list[dict]:
    results: list[dict] = []
    for row in library:
        entry = dict(row)
        for tk, tmeta in RECEPTORS.items():
            work = out_dir / tk
            safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in row["id"])[:80]
            docked = work / f"{safe}_docked.pdbqt"
            if force and docked.exists():
                docked.unlink()

            res = dock_ligand(
                smiles=row["canonical_smiles"],
                name=row["id"],
                receptor=tmeta["receptor_pdbqt"],
                box=boxes[tk],
                work_dir=work,
                vina_path=vina,
                exhaustiveness=exhaustiveness,
                num_modes=num_modes,
                seed=seed,
                ph=ph,
            )
            entry[tk] = {
                "affinity": res.get("vina_affinity"),
                "error": res.get("dock_error"),
                "docked_pdbqt": res.get("docked_pdbqt"),
            }
        cb1 = entry["cb1"]["affinity"]
        cb2 = entry["cb2"]["affinity"]
        entry["delta_cb2_minus_cb1"] = (
            cb2 - cb1 if cb1 is not None and cb2 is not None else None
        )
        results.append(entry)
    return results


def rank_top_candidates(results: list[dict]) -> dict:
    """Top 2: maximize negative delta AND TPSA > 70."""
    analog_rows = [r for r in results if r["id"] != "delta9-THCV (parent)"]
    dual_pass = [
        r
        for r in analog_rows
        if r.get("delta_cb2_minus_cb1") is not None
        and r["descriptors"]["tpsa"] > PERIPHERAL_TPSA_THRESHOLD
    ]
    dual_pass.sort(key=lambda r: r["delta_cb2_minus_cb1"])

    tpsa_only = [
        r for r in analog_rows if r["descriptors"]["tpsa"] > PERIPHERAL_TPSA_THRESHOLD
    ]
    delta_only = sorted(
        [r for r in analog_rows if r.get("delta_cb2_minus_cb1") is not None],
        key=lambda r: r["delta_cb2_minus_cb1"],
    )

    return {
        "dual_criteria": dual_pass[:2],
        "tpsa_pass": tpsa_only,
        "best_delta": delta_only[:5],
        "compromise": _compromise_rank(analog_rows),
    }


def _compromise_rank(rows: list[dict]) -> list[dict]:
    """Score = normalized(-delta) + normalized(TPSA) for rows with valid delta."""
    valid = [r for r in rows if r.get("delta_cb2_minus_cb1") is not None]
    if not valid:
        return []
    deltas = [r["delta_cb2_minus_cb1"] for r in valid]
    tpsas = [r["descriptors"]["tpsa"] for r in valid]
    d_min, d_max = min(deltas), max(deltas)
    t_min, t_max = min(tpsas), max(tpsas)

    def norm(x: float, lo: float, hi: float) -> float:
        if hi == lo:
            return 0.5
        return (x - lo) / (hi - lo)

    scored: list[tuple[float, dict]] = []
    for r in valid:
        d = r["delta_cb2_minus_cb1"]
        t = r["descriptors"]["tpsa"]
        # More negative delta is better → invert normalized delta
        delta_score = 1.0 - norm(d, d_min, d_max)
        tpsa_score = norm(t, t_min, t_max)
        composite = delta_score + tpsa_score
        scored.append((composite, r))
    scored.sort(key=lambda x: -x[0])
    return [r for _, r in scored[:3]]


def _fmt(v: float | None, places: int = 2) -> str:
    return f"{v:.{places}f}" if v is not None else "—"


def write_report(
    results: list[dict],
    ranking: dict,
    meta: dict,
    out_md: Path,
) -> None:
    lines = [
        "# THCV Analog Series V1.0 — Docking & ADMET",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Scaffold base",
        "",
        f"- **Parent:** Δ9-THCV (6aR,10aR), PubChem CID {CANONICAL_THCV_CID}",
        f"- **InChIKey:** `{THCV_INCHIKEY}`",
        f"- **Fuente SMILES:** `{CHEMOME_CSV.relative_to(ROOT)}` (NOT CID 62310)",
        "",
        "## Atom-mapping (assumptions)",
        "",
        "| Sitio | Quimioma / SMILES | Notas |",
        "|-------|-------------------|-------|",
        "| C3 alkyl | Prefijo `CCC`/`CCCC` en anillo resorcinol | n-propyl nativo; Serie V1 sustituye cadena |",
        "| C1 fenol | `…)O` terminal en anillo A | Serie V2: ésteres soft-drug; THCV-08 = fenol libre (metabolito esperado) |",
        "| C9/C11 | Metilo en puente `C)(C)C` → `C)(C)CO` o `C)(C)C(=O)O` | Patrón metabolito 11-OH / 11-COOH tipo THC mapeado al puente gem-dimetilo |",
        "",
        "## Filtro periférico",
        "",
        f"**Regla primaria:** TPSA > {PERIPHERAL_TPSA_THRESHOLD:.0f} Å² (menor penetración SNC hipotética).",
        "",
        "**Regla secundaria (*):** TPSA > 55 Å² AND cLogP < 4.0 AND MW > 300.",
        "",
        "Ésteres C1 elevan TPSA moderadamente pero no garantizan periferia sin hidrólisis; "
        "THCV-08 documenta el control fenólico post-cleavage.",
        "",
        "## Protocolo docking",
        "",
        "| Parámetro | Valor |",
        "|-----------|-------|",
        f"| Vina exhaustiveness | {meta['exhaustiveness']} |",
        f"| num_modes | {meta['num_modes']} |",
        f"| seed | {meta['seed']} |",
        f"| pH ligando | {meta['ph']} (Meeko + dimorphite COOH) |",
        f"| Receptor CB1 | `{meta['receptors']['cb1']}` |",
        f"| Receptor CB2 | `{meta['receptors']['cb2']}` |",
        f"| Grid CB1 | `{meta['grids']['cb1']}` |",
        f"| Grid CB2 | `{meta['grids']['cb2']}` |",
        "",
        "## Tabla de resultados",
        "",
        "| ID | Modificación | Score CB1 | Score CB2 | Delta (CB2 − CB1) | TPSA (Å²) | cLogP | Filtro Periférico |",
        "|----|--------------|-----------|-----------|-------------------|-----------|-------|-------------------|",
    ]

    for r in results:
        cb1 = r["cb1"]["affinity"]
        cb2 = r["cb2"]["affinity"]
        delta = r.get("delta_cb2_minus_cb1")
        d = r["descriptors"]
        delta_s = f"{delta:+.2f}" if delta is not None else "—"
        periph = "Sí" if r["peripheral_pass"] else "No"
        mod = r["modification"][:60] + ("…" if len(r["modification"]) > 60 else "")
        lines.append(
            f"| {r['id']} | {mod} | {_fmt(cb1)} | {_fmt(cb2)} | {delta_s} | "
            f"{d['tpsa']:.1f} | {d['clogp']:.2f} | {periph} |"
        )

    lines.extend(["", "## SMILES (canónicos RDKit)", ""])
    for r in results:
        lines.append(f"- **{r['id']}:** `{r['canonical_smiles']}`")

    lines.extend(["", "## Top 2 candidatos (Δ negativo + TPSA > 70)", ""])
    dual = ranking["dual_criteria"]
    if len(dual) >= 2:
        for i, r in enumerate(dual[:2], 1):
            lines.append(
                f"{i}. **{r['id']}** — Δ={r['delta_cb2_minus_cb1']:+.2f} kcal/mol, "
                f"TPSA={r['descriptors']['tpsa']:.1f} Å², cLogP={r['descriptors']['clogp']:.2f}. "
                f"{r['modification']}"
            )
    else:
        lines.append(
            f"**Menos de 2 compuestos pasan ambos criterios** (TPSA > {PERIPHERAL_TPSA_THRESHOLD:.0f} "
            f"AND delta CB2−CB1 negativo)."
        )
        lines.append("")
        lines.append("### Criterio TPSA > 70")
        if ranking["tpsa_pass"]:
            for r in ranking["tpsa_pass"]:
                d = r.get("delta_cb2_minus_cb1")
                lines.append(
                    f"- **{r['id']}** TPSA={r['descriptors']['tpsa']:.1f}, "
                    f"Δ={f'{d:+.2f}' if d is not None else '—'}"
                )
        else:
            lines.append("- Ningún análogo supera TPSA 70 Å².")
        lines.append("")
        lines.append("### Mejor delta (sesgo CB2 por score Vina)")
        for r in ranking["best_delta"][:3]:
            lines.append(
                f"- **{r['id']}** Δ={r['delta_cb2_minus_cb1']:+.2f}, "
                f"TPSA={r['descriptors']['tpsa']:.1f}"
            )
        lines.append("")
        lines.append("### Compromiso (ranking compuesto Δ + TPSA)")
        for r in ranking["compromise"]:
            lines.append(
                f"- **{r['id']}** Δ={r['delta_cb2_minus_cb1']:+.2f}, "
                f"TPSA={r['descriptors']['tpsa']:.1f}"
            )

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- CB1 receptor 5TGZ = estado antagonista-bound; scores de semillas neutras pueden diferir de CB2 agonista-bound 6PT0.",
            "- THCV-08 ≡ parent fenólico; no aporta novedad química pero ancla el control soft-drug.",
            "- THCV-10 carboxilato: dimorphite → carboxilato a pH 7.4; fenol neutro.",
            "- Scores Vina ≠ afinidad experimental; delta es proxy de selectividad de pose.",
            "",
            f"Poses: `{meta['out_dir']}/cb1/`, `{meta['out_dir']}/cb2/`",
            f"SMILES CSV: `{meta['smiles_csv']}`",
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
        default=ROOT / "results/docking/thcv_analogs_v1",
    )
    ap.add_argument(
        "--smiles-csv",
        type=Path,
        default=ROOT / "results/docking/thcv_analogs_v1/thcv_analogs_series_v1_smiles.csv",
    )
    ap.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results/docking/thcv_analogs_series_v1.md",
    )
    ap.add_argument("--exhaustiveness", type=int, default=16)
    ap.add_argument("--num-modes", type=int, default=9)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--prep-only", action="store_true", help="SMILES + PDBQT only, no docking")
    ap.add_argument("--report-only", action="store_true", help="Rebuild report from JSON")
    args = ap.parse_args()

    parent_smiles = _load_chemome_thcv_smiles()
    library = build_library(parent_smiles)
    write_smiles_csv(library, args.smiles_csv)
    print(f"Library: {len(library)} entries ({len(ANALOGS)} analogs + parent)")
    print(f"SMILES CSV: {args.smiles_csv}")

    json_path = args.out_dir / "thcv_analogs_series_v1.json"

    if args.report_only:
        if not json_path.exists():
            print(f"BLOQUEO: --report-only but missing {json_path}")
            return 2
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        write_report(payload["results"], payload["ranking"], payload["meta"], args.report)
        print(f"Report: {args.report}")
        return 0

    prep_ligand_pdbs(library, args.out_dir, seed=args.seed, ph=args.ph)

    if args.prep_only:
        print("Prep-only mode; skipping docking.")
        return 0

    try:
        vina = resolve_vina(root=ROOT)
    except FileNotFoundError as exc:
        print(f"BLOQUEO: {exc}")
        return 2

    for k, v in RECEPTORS.items():
        if not v["receptor_pdbqt"].exists():
            print(f"BLOQUEO: receptor missing {v['receptor_pdbqt']}")
            return 2

    boxes = {k: _load_grid(v["grid_config"]) for k, v in RECEPTORS.items()}
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Vina: {vina}")
    results = dock_library(
        library,
        args.out_dir,
        vina,
        boxes,
        args.exhaustiveness,
        args.num_modes,
        args.seed,
        args.ph,
        args.force,
    )

    ranking = rank_top_candidates(results)
    meta = {
        "exhaustiveness": args.exhaustiveness,
        "num_modes": args.num_modes,
        "seed": args.seed,
        "ph": args.ph,
        "vina": str(vina),
        "receptors": {k: str(v["receptor_pdbqt"]) for k, v in RECEPTORS.items()},
        "grids": {k: str(v["grid_config"]) for k, v in RECEPTORS.items()},
        "out_dir": str(args.out_dir.relative_to(ROOT)),
        "smiles_csv": str(args.smiles_csv.relative_to(ROOT)),
        "json_path": str(json_path.relative_to(ROOT)),
        "peripheral_tpsa_threshold": PERIPHERAL_TPSA_THRESHOLD,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    payload = {"meta": meta, "results": results, "ranking": ranking}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(results, ranking, meta, args.report)

    print(f"Report: {args.report}")
    print(f"JSON: {json_path}")
    n_ok = sum(
        1
        for r in results
        if r["cb1"]["affinity"] is not None and r["cb2"]["affinity"] is not None
    )
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
