"""Redocking QC: dock co-crystallized ligands and compute RMSD vs crystal pose."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml
from rdkit import Chem
from rdkit.Chem import AllChem

from src.screening.docking import parse_best_affinity, resolve_vina


ROOT = Path(__file__).resolve().parents[2]
_AFFINITY_RE = re.compile(
    r"REMARK VINA RESULT:\s+(-?\d+\.\d+)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RedockJob:
    name: str
    receptor_pdbqt: Path
    ref_ligand_pdbqt: Path
    ref_ligand_pdb: Path
    grid_config: Path
    success_rmsd_A: float = 2.0


def _load_grid(path: Path) -> dict[str, float]:
    box: dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        box[key.strip()] = float(val.strip())
    required = {
        "center_x",
        "center_y",
        "center_z",
        "size_x",
        "size_y",
        "size_z",
    }
    missing = required - set(box)
    if missing:
        raise ValueError(f"Grid incompleto {path}: faltan {sorted(missing)}")
    return box


def _pdbqt_first_model_to_mol(path: Path) -> Chem.Mol:
    """Parse first MODEL from PDBQT into RDKit mol (heavy atoms only)."""
    lines: list[str] = []
    in_model = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("MODEL"):
            in_model = True
            continue
        if line.startswith("ENDMDL"):
            break
        if in_model and line.startswith(("ATOM", "HETATM")):
            pdb_line = (
                line.replace("HETATM", "ATOM  ", 1)[:66]
                + " 1.00  0.00           C  "
            )
            lines.append(pdb_line)
    if not lines:
        raise RuntimeError(f"Sin MODEL/ATOM en {path}")
    block = "\n".join(lines) + "\nEND\n"
    mol = Chem.MolFromPDBBlock(block, sanitize=False, removeHs=True)
    if mol is None:
        raise RuntimeError(f"RDKit no leyó pose de {path}")
    Chem.SanitizeMol(mol)
    return mol


def _crystal_ligand_mol(path: Path) -> Chem.Mol:
    mol = Chem.MolFromPDBFile(str(path), removeHs=True, sanitize=False)
    if mol is None:
        raise RuntimeError(f"No se leyó ligando cristal {path}")
    Chem.SanitizeMol(mol)
    return mol


def compute_ligand_rmsd(
    crystal_pdb: Path,
    docked_pdbqt: Path,
) -> float:
    """Symmetry-correct heavy-atom RMSD (Å) after optimal alignment."""
    ref = _crystal_ligand_mol(crystal_pdb)
    mob = _pdbqt_first_model_to_mol(docked_pdbqt)
    rmsd = AllChem.GetBestRMS(ref, mob)
    return float(rmsd)


def run_vina_redock(
    job: RedockJob,
    vina_path: Path,
    out_dir: Path,
    exhaustiveness: int = 16,
    num_modes: int = 9,
    seed: int = 42,
) -> dict:
    """Redock reference ligand; return scores and paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    box = _load_grid(job.grid_config)
    out_pdbqt = out_dir / f"{job.name}_redocked.pdbqt"
    log_path = out_dir / f"{job.name}_vina.log"

    lig_copy = out_dir / f"{job.name}_lig.pdbqt"
    if not lig_copy.exists():
        lig_copy.write_text(
            job.ref_ligand_pdbqt.read_text(encoding="utf-8"), encoding="utf-8"
        )

    if not out_pdbqt.exists():
        cmd = [
            str(vina_path),
            "--receptor",
            str(job.receptor_pdbqt),
            "--ligand",
            str(lig_copy),
            "--out",
            str(out_pdbqt),
            "--center_x",
            str(box["center_x"]),
            "--center_y",
            str(box["center_y"]),
            "--center_z",
            str(box["center_z"]),
            "--size_x",
            str(box["size_x"]),
            "--size_y",
            str(box["size_y"]),
            "--size_z",
            str(box["size_z"]),
            "--exhaustiveness",
            str(exhaustiveness),
            "--num_modes",
            str(num_modes),
            "--seed",
            str(seed),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        log_path.write_text(
            (proc.stdout or "") + "\n" + (proc.stderr or ""),
            encoding="utf-8",
        )
        if proc.returncode != 0 or not out_pdbqt.exists():
            return {
                "name": job.name,
                "status": "vina_failed",
                "error": (proc.stderr or proc.stdout or "vina failed")[:500],
                "log": str(log_path),
            }

    affinity = parse_best_affinity(out_pdbqt.read_text(encoding="utf-8"))
    try:
        rmsd = compute_ligand_rmsd(job.ref_ligand_pdb, out_pdbqt)
    except Exception as exc:  # noqa: BLE001
        return {
            "name": job.name,
            "status": "rmsd_failed",
            "vina_affinity_kcal_mol": affinity,
            "error": str(exc),
            "docked_pdbqt": str(out_pdbqt),
            "log": str(log_path),
        }

    passed = rmsd < job.success_rmsd_A
    return {
        "name": job.name,
        "status": "ok",
        "vina_affinity_kcal_mol": affinity,
        "rmsd_A": round(rmsd, 3),
        "success_threshold_A": job.success_rmsd_A,
        "passed": passed,
        "receptor": str(job.receptor_pdbqt),
        "ref_ligand_pdbqt": str(job.ref_ligand_pdbqt),
        "ref_ligand_pdb": str(job.ref_ligand_pdb),
        "docked_pdbqt": str(out_pdbqt),
        "grid_config": str(job.grid_config),
        "log": str(log_path),
    }


def run_redock_qc(
    root: Path = ROOT,
    config_path: Path | None = None,
    out_dir: Path | None = None,
) -> dict:
    """Run AM6538→5TGZ and WIN→6PT0 redocking QC."""
    config_path = config_path or root / "configs" / "cb1_cb2.yaml"
    out_dir = out_dir or root / "results" / "docking" / "redock_qc"
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    dock_cfg = cfg.get("docking", {})

    try:
        vina = resolve_vina(dock_cfg.get("vina_binary"), root=root)
    except FileNotFoundError as exc:
        return {"status": "blocked", "error": str(exc)}

    jobs = [
        RedockJob(
            name="AM6538_5TGZ",
            receptor_pdbqt=root / "data/targets/cb1/cb1_5tgz_clean.pdbqt",
            ref_ligand_pdbqt=root / "data/targets/cb1/am6538_ref.pdbqt",
            ref_ligand_pdb=root / "data/targets/cb1/5TGZ_ligand.pdb",
            grid_config=root / "configs/grid_cb1_5tgz.txt",
        ),
        RedockJob(
            name="WIN55212_6PT0",
            receptor_pdbqt=root / "data/targets/cb2/cb2_6pt0_clean.pdbqt",
            ref_ligand_pdbqt=root / "data/targets/cb2/win55212_ref.pdbqt",
            ref_ligand_pdb=root / "data/targets/cb2/6PT0_ligand.pdb",
            grid_config=root / "configs/grid_cb2_6pt0.txt",
        ),
    ]

    missing = [
        str(p)
        for job in jobs
        for p in (
            job.receptor_pdbqt,
            job.ref_ligand_pdbqt,
            job.ref_ligand_pdb,
            job.grid_config,
        )
        if not p.exists()
    ]
    if missing:
        return {"status": "blocked", "error": "Archivos ausentes", "missing": missing}

    exhaustiveness = int(dock_cfg.get("exhaustiveness", 16))
    num_modes = int(dock_cfg.get("num_modes", 9))
    seed = int(dock_cfg.get("seed", 42))

    results = []
    for job in jobs:
        results.append(
            run_vina_redock(
                job,
                vina_path=vina,
                out_dir=out_dir,
                exhaustiveness=exhaustiveness,
                num_modes=num_modes,
                seed=seed,
            )
        )

    summary = {
        "status": "ok",
        "vina_binary": str(vina),
        "exhaustiveness": exhaustiveness,
        "seed": seed,
        "jobs": results,
        "all_passed": all(r.get("passed") for r in results if r.get("status") == "ok"),
    }
    out_json = out_dir / "redock_qc_results.json"
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
