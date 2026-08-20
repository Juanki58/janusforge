#!/usr/bin/env python3
"""Calibration Benchmark Exam A — Gold ligands vs CB1 (5TGZ) / CB2 (6PT0).

Docks CP-55,940, HU-308, and RG7774/Vicasinabin only; writes markdown + JSON report.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.screening.docking import dock_ligand, resolve_vina

# Gold Exam A panel — SMILES from PubChem (2026-08-18); InChIKeys cross-checked Round1.
GOLD_LIGANDS: tuple[dict, ...] = (
    {
        "id": "CP-55,940",
        "aliases": ["CP55940", "CP55,940"],
        "role": "universal_agonist",
        "pubchem_cid": 10494,
        "inchikey": "MIJYXULNPSFWEK-GTOFXWBISA-N",
        "smiles": (
            "C[C@]12CC[C@@H](C([C@@H]1CC[C@@]3([C@@H]2CC=C4[C@]3("
            "CC[C@@]5([C@H]4CC(CC5)(C)C)C(=O)O)C)C)(C)C)O"
        ),
        "source": "PubChem CID 10494 (IsomericSMILES)",
    },
    {
        "id": "HU-308",
        "aliases": ["HU308"],
        "role": "cb2_agonist",
        "pubchem_cid": 11553430,
        "inchikey": "CFMRIVODIXTERW-BDTNDASRSA-N",
        "smiles": (
            "CCCCCCC(C)(C)C1=CC(=C(C(=C1)OC)[C@H]2C=C([C@H]3C[C@@H]2C3(C)C)CO)OC"
        ),
        "source": "PubChem CID 11553430; Round1 InChIKey CFMRIVODIXTERW-BDTNDASRSA-N",
    },
    {
        "id": "RG7774 / Vicasinabin",
        "aliases": ["RG7774", "Vicasinabin"],
        "role": "cb2_agonist",
        "pubchem_cid": 86296048,
        "inchikey": "MAYZWDRUFKUGGP-VIFPVBQESA-N",
        "smiles": "CC(C)(C)C1=NC2=C(C(=N1)N3CC[C@@H](C3)O)N=NN2CC4=NN=NN4C",
        "source": (
            "PubChem CID 86296048; Round1 GOLD VICASINABIN_func_cAMP_hCB2 "
            "(Grether 2024 DOI 10.3389/fphar.2024.1426446)"
        ),
    },
)

MICROSWITCHS: dict[str, dict[str, tuple[int, str, tuple[str, ...]]]] = {
    "cb1": {
        "Phe200(3.36)": (200, "PHE", ("CG", "CD1", "CD2", "CE1", "CE2", "CZ")),
        "Trp356(6.48)": (
            356,
            "TRP",
            ("CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"),
        ),
    },
    "cb2": {
        "Phe117(3.32)": (117, "PHE", ("CG", "CD1", "CD2", "CE1", "CE2", "CZ")),
        "Trp258(6.48)": (
            258,
            "TRP",
            ("CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"),
        ),
        "Ser285(7.39)": (285, "SER", ("CB", "OG")),
    },
}

RECEPTORS = {
    "cb1": {
        "label": "CB1 (5TGZ)",
        "pdb_id": "5TGZ",
        "receptor_pdbqt": ROOT / "data/targets/cb1/cb1_5tgz_clean.pdbqt",
        "receptor_pdb": ROOT / "data/targets/cb1/5TGZ_clean.pdb",
        "grid_config": ROOT / "configs/grid_cb1_5tgz.txt",
    },
    "cb2": {
        "label": "CB2 (6PT0)",
        "pdb_id": "6PT0",
        "receptor_pdbqt": ROOT / "data/targets/cb2/cb2_6pt0_clean.pdbqt",
        "receptor_pdb": ROOT / "data/targets/cb2/6PT0_clean.pdb",
        "grid_config": ROOT / "configs/grid_cb2_6pt0.txt",
    },
}


def _load_grid(path: Path) -> dict[str, float]:
    box: dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, val = line.split("=", 1)
        box[key.strip()] = float(val.strip())
    return box


def _parse_receptor_sidechain_coords(
    pdb_path: Path,
    resseq: int,
    resname: str,
    atoms: tuple[str, ...],
) -> list[tuple[float, float, float]]:
    want = set(atoms)
    coords: list[tuple[float, float, float]] = []
    for line in pdb_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("ATOM"):
            continue
        if line[17:20].strip() != resname:
            continue
        if int(line[22:26]) != resseq:
            continue
        atom = line[12:16].strip()
        if atom in want:
            coords.append(
                (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            )
    if not coords:
        raise RuntimeError(
            f"Sin átomos sidechain {resname}{resseq} {atoms} en {pdb_path}"
        )
    return coords


def _parse_ligand_heavy_coords(pdbqt_path: Path) -> list[tuple[float, float, float]]:
    coords: list[tuple[float, float, float]] = []
    in_model = False
    for line in pdbqt_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("MODEL"):
            in_model = True
            continue
        if line.startswith("ENDMDL"):
            break
        if not in_model or not line.startswith(("ATOM", "HETATM")):
            continue
        elem = line[77:79].strip() if len(line) >= 79 else line[12:14].strip()[0]
        if elem.upper() == "H":
            continue
        coords.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    if not coords:
        raise RuntimeError(f"Sin coords ligando en {pdbqt_path}")
    return coords


def _min_distance(
    a: list[tuple[float, float, float]],
    b: list[tuple[float, float, float]],
) -> float:
    best = math.inf
    for x1, y1, z1 in a:
        for x2, y2, z2 in b:
            d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            if d < best:
                best = d
    return best


def compute_microswitch_distances(
    docked_pdbqt: Path,
    receptor_pdb: Path,
    target_key: str,
) -> dict[str, float]:
    lig = _parse_ligand_heavy_coords(docked_pdbqt)
    out: dict[str, float] = {}
    for label, (resseq, resname, atoms) in MICROSWITCHS[target_key].items():
        sc = _parse_receptor_sidechain_coords(receptor_pdb, resseq, resname, atoms)
        out[label] = round(_min_distance(lig, sc), 2)
    return out


def _interaction_summary(dist: dict[str, float], target_key: str) -> str:
    parts: list[str] = []
    for label, d in dist.items():
        tag = "cerca" if d <= 4.0 else ("medio" if d <= 6.0 else "lejos")
        parts.append(f"{label.split('(')[0].strip()} {d:.1f}Å ({tag})")
    return "; ".join(parts)


def _pass_notes(lig: dict, cb1_score: float | None, cb2_score: float | None) -> str:
    if cb1_score is None or cb2_score is None:
        return "FAIL — docking incompleto"
    delta = cb2_score - cb1_score
    role = lig["role"]
    notes: list[str] = []
    if role == "universal_agonist":
        if abs(cb1_score) > 2 and abs(cb2_score) > 2:
            notes.append("PASS parcial — afinidades en rango útil en ambos")
        else:
            notes.append("REVISAR — scores débiles en uno o ambos receptores")
        notes.append(
            "CAVEAT: CB1=5TGZ es estado antagonista/inactivo (AM6538); "
            "agonistas pueden subestimarse vs CB2 agonista-bound 6PT0"
        )
    elif role == "cb2_agonist":
        if delta < -0.5:
            notes.append("PASS — delta CB2 favorecido (Δ<−0.5 kcal/mol)")
        elif delta <= 0.5:
            notes.append("MIXED — selectividad CB2 no clara por score Vina")
        else:
            notes.append("FAIL calibración — CB1 score mejor que CB2")
    return " | ".join(notes)


def write_report(results: list[dict], out_md: Path, meta: dict) -> None:
    lines = [
        "# Calibration Benchmark Exam A — Gold ligands vs CB1/CB2",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Protocolo",
        "",
        "| Parámetro | Valor |",
        "|-----------|-------|",
        f"| Vina exhaustiveness | {meta['exhaustiveness']} |",
        f"| num_modes | {meta['num_modes']} |",
        f"| seed | {meta['seed']} (convención `configs/cb1_cb2.yaml`) |",
        f"| pH ligando | {meta['ph']} |",
        f"| Receptor CB1 | `{meta['receptors']['cb1']}` |",
        f"| Receptor CB2 | `{meta['receptors']['cb2']}` |",
        f"| Grid CB1 | `{meta['grids']['cb1']}` |",
        f"| Grid CB2 | `{meta['grids']['cb2']}` |",
        "",
        "## Tabla de afinidades (mode 1 / best)",
        "",
        "| Ligando | Score CB1 (5TGZ) | Score CB2 (6PT0) | Delta (CB2 − CB1) | Interacciones Clave |",
        "|---------|------------------|------------------|-------------------|---------------------|",
    ]
    for r in results:
        cb1 = r["cb1"]["affinity"]
        cb2 = r["cb2"]["affinity"]
        cb1_s = f"{cb1:.2f}" if cb1 is not None else "—"
        cb2_s = f"{cb2:.2f}" if cb2 is not None else "—"
        if cb1 is not None and cb2 is not None:
            delta_s = f"{cb2 - cb1:+.2f}"
        else:
            delta_s = "—"
        inter = r.get("interactions_summary", "—")
        lines.append(
            f"| {r['id']} | {cb1_s} | {cb2_s} | {delta_s} | {inter} |"
        )

    lines.extend(
        [
            "",
            "## Fuentes estructurales (ligandos)",
            "",
        ]
    )
    for lig in GOLD_LIGANDS:
        lines.append(
            f"- **{lig['id']}**: PubChem CID {lig['pubchem_cid']}, "
            f"InChIKey `{lig['inchikey']}` — {lig['source']}"
        )

    lines.extend(
        [
            "",
            "## Notas PASS / caveats",
            "",
        ]
    )
    for r in results:
        lines.append(f"- **{r['id']}**: {r['pass_notes']}")

    lines.extend(
        [
            "",
            "## Microswitch distances (Å, min ligando heavy → sidechain)",
            "",
            "Residuos verificados en PDBs limpios (`5TGZ_clean.pdb`, `6PT0_clean.pdb`).",
            "",
        ]
    )
    for r in results:
        lines.append(f"### {r['id']}")
        for tk in ("cb1", "cb2"):
            dist = r[tk].get("microswitch_distances", {})
            if dist:
                parts = ", ".join(f"{k}: {v:.2f}" for k, v in dist.items())
                lines.append(f"- **{RECEPTORS[tk]['label']}**: {parts}")
        lines.append("")

    lines.extend(
        [
            "## Interpretación",
            "",
            "- **Delta (CB2 − CB1) < 0**: pose CB2 más favorable (score Vina más negativo en CB2).",
            "- **5TGZ (CB1)**: estructura con antagonista AM6538 — cautela al interpretar agonistas universales.",
            "- **6PT0 (CB2)**: estructura agonista-bound (WIN 55,212-2) — más apropiada para agonistas CB2.",
            "- Distancias ≤4 Å sugieren contacto directo con microswitch; >6 Å contacto débil o ausente.",
            "",
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
        default=ROOT / "results/docking/benchmark_gold_exam_a",
    )
    ap.add_argument("--exhaustiveness", type=int, default=16)
    ap.add_argument("--num-modes", type=int, default=9)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--force", action="store_true", help="Re-dock even if poses exist")
    args = ap.parse_args()

    try:
        vina = resolve_vina(root=ROOT)
    except FileNotFoundError as exc:
        print(f"BLOQUEO: {exc}")
        return 2

    boxes = {k: _load_grid(v["grid_config"]) for k, v in RECEPTORS.items()}
    for k, v in RECEPTORS.items():
        if not v["receptor_pdbqt"].exists():
            print(f"BLOQUEO: receptor ausente {v['receptor_pdbqt']}")
            return 2
        if not v["receptor_pdb"].exists():
            print(f"BLOQUEO: PDB limpio ausente {v['receptor_pdb']}")
            return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []

    print(f"Vina: {vina}")
    print(
        f"exhaustiveness={args.exhaustiveness} num_modes={args.num_modes} "
        f"seed={args.seed}"
    )

    for lig in GOLD_LIGANDS:
        row: dict = {
            "id": lig["id"],
            "role": lig["role"],
            "pubchem_cid": lig["pubchem_cid"],
            "inchikey": lig["inchikey"],
            "smiles": lig["smiles"],
            "source": lig["source"],
        }
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in lig["id"])[:80]

        for tk, tmeta in RECEPTORS.items():
            work = args.out_dir / tk
            docked = work / f"{safe}_docked.pdbqt"
            if args.force and docked.exists():
                docked.unlink()

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
        row["pass_notes"] = _pass_notes(lig, cb1_a, cb2_a)
        results.append(row)

    json_path = args.out_dir / "benchmark_gold_exam_a.json"
    md_path = ROOT / "results/docking/benchmark_gold_exam_a.md"
    meta = {
        "exhaustiveness": args.exhaustiveness,
        "num_modes": args.num_modes,
        "seed": args.seed,
        "ph": args.ph,
        "vina": str(vina),
        "receptors": {k: str(v["receptor_pdbqt"]) for k, v in RECEPTORS.items()},
        "grids": {k: str(v["grid_config"]) for k, v in RECEPTORS.items()},
        "json_path": str(json_path.relative_to(ROOT)),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    payload = {"meta": meta, "ligands": results}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(results, md_path, meta)

    print(f"Report: {md_path}")
    print(f"JSON: {json_path}")
    n_ok = sum(
        1
        for r in results
        if r["cb1"]["affinity"] is not None and r["cb2"]["affinity"] is not None
    )
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
