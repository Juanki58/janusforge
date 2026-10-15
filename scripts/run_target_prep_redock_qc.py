#!/usr/bin/env python3
"""PDB target prep + orthosteric grid boxes + redocking QC (CB1 5TGZ, CB2 6PT0/6KPC)."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.targets.prep import prepare_all_targets
from src.targets.redock_qc import run_redock_qc


def _write_report(prep: dict, redock: dict, report_path: Path) -> None:
    lines = [
        "# Target prep + redocking QC",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Receptores y ligandos de referencia",
        "",
    ]

    for key, meta in prep.get("targets", {}).items():
        if "error" in meta:
            lines.append(f"- **{key}**: ERROR — {meta['error']}")
            continue
        lines.append(f"### {key} ({meta['pdb_id']})")
        lines.append(f"- Receptor: `{meta['receptor_pdbqt']}`")
        if meta.get("chains_kept"):
            lines.append(f"- Cadenas: {meta['chains_kept']}")
        lines.append(
            f"- Ligando caja: {meta['ligand_resname']} ({meta['ligand_natoms']} át.)"
        )
        lines.append(f"- Grid: `{meta['grid_config']}`")
        lines.append(
            f"- Centro (Å): ({meta['center_x']}, {meta['center_y']}, {meta['center_z']})"
        )
        lines.append(
            f"- Tamaño (Å): {meta['size_x']} × {meta['size_y']} × {meta['size_z']}"
        )
        lines.append("")

    lines.extend(["## Ligandos de referencia (PDBQT)", ""])
    for key, meta in prep.get("ref_ligands", {}).items():
        if "error" in meta:
            lines.append(f"- **{key}**: ERROR — {meta['error']}")
        else:
            lines.append(f"- **{key}** ({meta['pdb_id']}): `{meta['ref_ligand_pdbqt']}`")
            if meta.get("note"):
                lines.append(f"  - Nota: {meta['note']}")
    lines.append("")

    notes = prep.get("notes", {})
    if notes:
        lines.extend(["## Notas estructurales", ""])
        for k, v in notes.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")

    lines.extend(["## Redocking QC (criterio RMSD < 2.0 Å)", ""])
    if redock.get("status") == "blocked":
        lines.append(f"**BLOQUEADO**: {redock.get('error')}")
        if redock.get("missing"):
            lines.append("")
            lines.append("Archivos ausentes:")
            for m in redock["missing"]:
                lines.append(f"- `{m}`")
        lines.extend(
            [
                "",
                "Comando para reintentar tras prep:",
                "```bash",
                "python scripts/run_target_prep_redock_qc.py --skip-prep",
                "```",
            ]
        )
    else:
        lines.append(f"- Vina: `{redock.get('vina_binary')}`")
        lines.append(f"- exhaustiveness={redock.get('exhaustiveness')} seed={redock.get('seed')}")
        lines.append("")
        lines.append("| Sistema | RMSD (Å) | Affinity (kcal/mol) | PASS (<2Å) |")
        lines.append("|---------|----------|---------------------|------------|")
        for job in redock.get("jobs", []):
            if job.get("status") != "ok":
                lines.append(
                    f"| {job['name']} | — | — | FAIL ({job.get('status')}) |"
                )
            else:
                passed = "PASS" if job.get("passed") else "FAIL"
                lines.append(
                    f"| {job['name']} | {job['rmsd_A']} | {job['vina_affinity_kcal_mol']} | {passed} |"
                )
        lines.append("")
        overall = "PASS" if redock.get("all_passed") else "FAIL"
        lines.append(f"**Resultado global**: {overall}")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skip-prep", action="store_true")
    ap.add_argument("--skip-redock", action="store_true")
    ap.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results/reports/TARGET_PREP_REDOCK_QC.md",
    )
    args = ap.parse_args()

    prep = {"targets": {}, "ref_ligands": {}, "notes": {}}
    if not args.skip_prep:
        print("=== Target prep ===", flush=True)
        prep = prepare_all_targets(root=ROOT)
        for key, meta in prep.get("targets", {}).items():
            if "error" in meta:
                print(f"  {key}: FAIL — {meta['error']}")
            else:
                print(f"  {key}: OK -> {meta['receptor_pdbqt']}")

    redock = {"status": "skipped"}
    if not args.skip_redock:
        print("=== Redock QC ===", flush=True)
        redock = run_redock_qc(root=ROOT)
        if redock.get("status") == "blocked":
            print(f"  BLOQUEADO: {redock.get('error')}")
        else:
            for job in redock.get("jobs", []):
                if job.get("status") == "ok":
                    tag = "PASS" if job.get("passed") else "FAIL"
                    print(
                        f"  {job['name']}: RMSD={job['rmsd_A']}Å "
                        f"aff={job['vina_affinity_kcal_mol']} [{tag}]"
                    )
                else:
                    print(f"  {job['name']}: {job.get('status')} — {job.get('error')}")

    _write_report(prep if not args.skip_prep else _load_prep_manifest(), redock, args.report)
    print(f"Reporte: {args.report}")

    if not args.skip_prep:
        failed = [k for k, v in prep.get("targets", {}).items() if "error" in v]
        if failed:
            return 1
    if redock.get("status") == "ok" and not redock.get("all_passed"):
        return 1
    return 0


def _load_prep_manifest() -> dict:
    path = ROOT / "data/targets/target_prep_redock_manifest.json"
    if path.exists():
        import json

        return json.loads(path.read_text(encoding="utf-8"))
    return {"targets": {}, "ref_ligands": {}, "notes": {}}


if __name__ == "__main__":
    raise SystemExit(main())
