#!/usr/bin/env python3
"""OpenMM membrane MD: CB1 inactive 5TGZ in explicit POPC + water + NaCl.

Triplet panel (default --ligand all):
  JANUS_H1_02c  vs  delta9-THCV  vs  delta9-THC (agonist control)

Builds an all-atom POPC bilayer around the docked complex (AmberTools
packmol_memgen preferred; Packmol+lipid17 fallback documented), then runs
NPT production with a semi-isotropic membrane barostat.

IP
----
- Reads docked poses from gitignored paths (default: results/docking/h1_h5_batch3/).
- Never embeds SMILES/coordinates in this script or in public reports.
- Trajectories / metrics CSV land under results/md/membrane/ (gitignored).

Force field
-----------
- Protein: amber14-all.xml
- Lipids:  amber14/lipid17.xml (POPC)
- Water:   tip3p.xml
- Ligand:  GAFF2 via openmmforcefields.GAFFTemplateGenerator + OpenFF Toolkit
- Ions:    neutralize + NaCl 0.15 M (via packmol_memgen / solvent stage)

Metrics
-------
- Cα RMSD of TM6 vs minimized frame
- COM distance of Cα atoms TM3 vs TM6
- Helix-axis angle TM3–TM6 (degrees; THC expected to open relative to inactive)
- Phenolic H-bond persistence (% frames; ligand OH → protein acceptor)

CLI aliases for --ligand: h1_02c, thcv, thc, all (or full ids).

Usage
-----
  python scripts/run_md_openmm_membrane_lead.py --dry-run
  python scripts/run_md_openmm_membrane_lead.py --ns 20 --ligand all
  python scripts/run_md_openmm_membrane_lead.py --ligand thc --ns 0.01 --build-only
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = Path(__file__).resolve().parent
for _p in (str(ROOT), str(_SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# Reuse soluble-MD helpers (pose I/O, receptor filter/protonate, TM analysis bits)
from run_md_openmm_lead import (  # noqa: E402
    DEFAULT_KEEP_RESIDUE_RANGES,
    DEFAULT_RECEPTOR,
    DEFAULT_TM3,
    DEFAULT_TM6,
    HBOND_DIST_CUTOFF_A,
    extract_model1_pdbqt,
    filter_receptor_pdb,
    pdbqt_model_to_sdf,
    pose_pdbqt_path,
    probe_deps as probe_soluble_deps,
    protonate_receptor_pdb,
    _select_platform,
    _uniprot_ca_resseqs_from_pdb,
    _map_uniprot_range_to_serial,
)

DEFAULT_DOCK_DIR = ROOT / "results/docking/h1_h5_batch3/cb1"
DEFAULT_OUT_DIR = ROOT / "results/md/membrane"
DEFAULT_METRICS_CSV = DEFAULT_OUT_DIR / "h1_02c_vs_thcv_vs_thc_5tgz_popc.csv"

# Canonical ligand ids used in docking filenames
LIGAND_CANONICAL = {
    "h1_02c": "JANUS_H1_02c",
    "janus_h1_02c": "JANUS_H1_02c",
    "JANUS_H1_02c": "JANUS_H1_02c",
    "thcv": "delta9-THCV",
    "delta9-thcv": "delta9-THCV",
    "delta9-THCV": "delta9-THCV",
    "thc": "delta9-THC",
    "delta9-thc": "delta9-THC",
    "delta9-THC": "delta9-THC",
}
DEFAULT_TRIPLET = ("JANUS_H1_02c", "delta9-THCV", "delta9-THC")


@dataclass
class MembraneMDConfig:
    receptor_pdb: Path = DEFAULT_RECEPTOR
    dock_dir: Path = DEFAULT_DOCK_DIR
    out_dir: Path = DEFAULT_OUT_DIR
    metrics_csv: Path = DEFAULT_METRICS_CSV
    tm3: tuple[int, int] = DEFAULT_TM3
    tm6: tuple[int, int] = DEFAULT_TM6
    keep_residue_ranges: list[tuple[int, int]] = field(
        default_factory=lambda: list(DEFAULT_KEEP_RESIDUE_RANGES)
    )
    salt_molar: float = 0.15
    temperature_k: float = 300.0
    pressure_atm: float = 1.0
    minimize_max_iter: int = 5000
    equil_ps: float = 1000.0  # membrane needs longer equilibration
    production_ns: float = 20.0
    report_interval_ps: float = 10.0
    seed: int = 42
    platform: Optional[str] = None
    strip_fusion: bool = True
    # packmol_memgen: water slab thickness (Å) above/below leaflet
    water_dist_a: float = 15.0
    # xy padding around protein for bilayer extent (Å)
    lipid_dist_a: float = 15.0


def resolve_ligand_ids(raw: Optional[list[str]]) -> list[str]:
    if not raw or any(str(x).lower() == "all" for x in raw):
        return list(DEFAULT_TRIPLET)
    out: list[str] = []
    for item in raw:
        key = item.strip()
        canon = LIGAND_CANONICAL.get(key) or LIGAND_CANONICAL.get(key.lower())
        if canon is None:
            raise SystemExit(
                f"Unknown --ligand {item!r}. "
                f"Use: h1_02c, thcv, thc, all, or full ids {DEFAULT_TRIPLET}"
            )
        if canon not in out:
            out.append(canon)
    return out


def _load_yaml_config(path: Optional[Path]) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.is_file():
        raise FileNotFoundError(f"Config not found: {path}")
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("pyyaml required for --config") from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("Config must be a mapping")
    return data


def config_from_args(args: argparse.Namespace) -> MembraneMDConfig:
    y = _load_yaml_config(args.config)
    cfg = MembraneMDConfig()
    for key, caster in (
        ("receptor_pdb", Path),
        ("dock_dir", Path),
        ("out_dir", Path),
        ("metrics_csv", Path),
    ):
        if key in y:
            setattr(cfg, key, caster(y[key]))
    if "tm3" in y:
        cfg.tm3 = (int(y["tm3"][0]), int(y["tm3"][1]))
    if "tm6" in y:
        cfg.tm6 = (int(y["tm6"][0]), int(y["tm6"][1]))
    if "keep_residue_ranges" in y:
        cfg.keep_residue_ranges = [(int(a), int(b)) for a, b in y["keep_residue_ranges"]]
    for key in (
        "salt_molar",
        "temperature_k",
        "pressure_atm",
        "equil_ps",
        "report_interval_ps",
        "water_dist_a",
        "lipid_dist_a",
    ):
        if key in y:
            setattr(cfg, key, float(y[key]))
    if "minimize_max_iter" in y:
        cfg.minimize_max_iter = int(y["minimize_max_iter"])
    if "seed" in y:
        cfg.seed = int(y["seed"])
    if "platform" in y:
        cfg.platform = y["platform"]
    if "strip_fusion" in y:
        cfg.strip_fusion = bool(y["strip_fusion"])

    if args.receptor is not None:
        cfg.receptor_pdb = Path(args.receptor)
    if args.dock_dir is not None:
        cfg.dock_dir = Path(args.dock_dir)
    if args.out_dir is not None:
        cfg.out_dir = Path(args.out_dir)
    if args.metrics_csv is not None:
        cfg.metrics_csv = Path(args.metrics_csv)
    if args.ns is not None:
        cfg.production_ns = float(args.ns)
    if args.seed is not None:
        cfg.seed = int(args.seed)
    if args.platform is not None:
        cfg.platform = args.platform

    for pattr in ("receptor_pdb", "dock_dir", "out_dir", "metrics_csv"):
        p = getattr(cfg, pattr)
        if not p.is_absolute():
            setattr(cfg, pattr, ROOT / p)
    return cfg


def probe_membrane_deps() -> dict[str, Any]:
    info = probe_soluble_deps()
    info["packmol"] = bool(shutil.which("packmol"))
    info["packmol_memgen"] = False
    info["lipid17"] = False
    # AmberTools packmol_memgen may be installed as packmol-memgen or packmol_memgen
    for name in ("packmol-memgen", "packmol_memgen"):
        if shutil.which(name):
            info["packmol_memgen"] = True
            info["packmol_memgen_bin"] = name
            break
    # Also try python -m / ambertools path via which conda env
    if not info["packmol_memgen"]:
        amberhome = os.environ.get("AMBERHOME")
        if amberhome:
            for name in ("packmol-memgen", "packmol_memgen"):
                cand = Path(amberhome) / "bin" / name
                if cand.is_file():
                    info["packmol_memgen"] = True
                    info["packmol_memgen_bin"] = str(cand)
                    break
    try:
        from openmm import app

        # Presence of lipid17 XML in OpenMM data files
        ff = app.ForceField("amber14-all.xml", "amber14/lipid17.xml", "amber14/tip3p.xml")
        info["lipid17"] = True
        del ff
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"lipid17: {exc}")
    info["membrane_ready"] = bool(
        info.get("gaff_ready") and info.get("lipid17") and info.get("packmol_memgen")
    )
    return info


def membrane_install_message() -> str:
    return (
        "Membrane MD requires Linux/macOS conda-forge stack (AmberTools not on win-64):\n"
        "  conda env create -f environments/environment-md-membrane.yml\n"
        "  conda activate janus_md_membrane\n"
        "Or Docker (Windows host):\n"
        "  docker run --rm --gpus all -v janus_md_mamba:/opt/conda \\\n"
        "    -v \"$PWD:/work\" -w /work mambaorg/micromamba:2 bash -lc \\\n"
        "    'micromamba run -n janus_md python scripts/run_md_openmm_membrane_lead.py --dry-run'\n"
        "Needs: OpenMM + openmmforcefields + OpenFF + ambertools (packmol_memgen) + lipid17.\n"
        "See results/reports/md_membrane_20ns_plan.md."
    )


def validate_inputs(cfg: MembraneMDConfig, ligand_ids: list[str]) -> list[str]:
    problems: list[str] = []
    if not cfg.receptor_pdb.is_file():
        problems.append(f"missing receptor: {cfg.receptor_pdb}")
    for lid in ligand_ids:
        p = pose_pdbqt_path(cfg.dock_dir, lid)
        if not p.is_file():
            problems.append(f"missing pose: {p}")
    return problems


def write_complex_pdb(protein_pdb: Path, ligand_pdb: Path, out_pdb: Path) -> Path:
    """Concatenate protein ATOMs + ligand HETATM/ATOM into one PDB (no SMILES)."""
    lines: list[str] = []
    for line in protein_pdb.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(("ATOM", "TER")):
            lines.append(line)
    for line in ligand_pdb.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(("ATOM", "HETATM")):
            # Force HETATM + resname LIG for clarity in topology merge
            atom = "HETATM" + line[6:]
            if len(atom) >= 20:
                atom = atom[:17] + "LIG" + atom[20:]
            lines.append(atom)
    lines.append("END")
    out_pdb.parent.mkdir(parents=True, exist_ok=True)
    out_pdb.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_pdb


def find_packmol_memgen(deps: dict[str, Any]) -> Optional[str]:
    if deps.get("packmol_memgen_bin"):
        return str(deps["packmol_memgen_bin"])
    for name in ("packmol-memgen", "packmol_memgen"):
        p = shutil.which(name)
        if p:
            return p
    return None


def orient_complex_for_membrane(
    complex_pdb: Path,
    out_pdb: Path,
    tm3: tuple[int, int],
    tm6: tuple[int, int],
) -> Path:
    """Rotate complex so TM3/TM6 Cα PCA axis ≈ Z, then center XY/Z at origin.

    Avoids packmol-memgen MEMEMBED+keepligs path (broken on ligand complexes in
    AmberTools 2025.1). Output is suitable for ``--preoriented``.
    """
    import numpy as np

    rows: list[tuple[str, Optional[np.ndarray]]] = []
    ca_xyz: list[np.ndarray] = []
    for line in complex_pdb.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(("ATOM", "HETATM")) and len(line) >= 54:
            try:
                xyz = np.array(
                    [float(line[30:38]), float(line[38:46]), float(line[46:54])],
                    dtype=float,
                )
            except ValueError:
                rows.append((line, None))
                continue
            rows.append((line, xyz))
            name = line[12:16].strip()
            try:
                resseq = int(line[22:26])
            except ValueError:
                continue
            if name == "CA" and (
                tm3[0] <= resseq <= tm3[1] or tm6[0] <= resseq <= tm6[1]
            ):
                ca_xyz.append(xyz)
        else:
            rows.append((line, None))
    if len(ca_xyz) < 6:
        # Fallback: all protein CA
        ca_xyz = []
        for line, xyz in rows:
            if xyz is None or not line.startswith("ATOM"):
                continue
            if line[12:16].strip() == "CA":
                ca_xyz.append(xyz)
    if len(ca_xyz) < 3:
        raise RuntimeError("Cannot orient membrane complex: too few CA atoms")

    pts = np.vstack(ca_xyz)
    com = pts.mean(axis=0)
    centered = pts - com
    cov = centered.T @ centered / max(len(centered) - 1, 1)
    vals, vecs = np.linalg.eigh(cov)
    axis = vecs[:, int(np.argmax(vals))]
    axis = axis / (np.linalg.norm(axis) + 1e-12)
    # Rotation that maps axis → +Z
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(axis, z)
    c = float(np.dot(axis, z))
    if np.linalg.norm(v) < 1e-8:
        R = np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        vx = np.array(
            [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]], dtype=float
        )
        R = np.eye(3) + vx + vx @ vx * ((1.0 - c) / (np.linalg.norm(v) ** 2))

    out_lines: list[str] = []
    for line, xyz in rows:
        if xyz is None:
            if line.startswith("END"):
                continue
            out_lines.append(line)
            continue
        new = R @ (xyz - com)
        out_lines.append(
            f"{line[:30]}{new[0]:8.3f}{new[1]:8.3f}{new[2]:8.3f}{line[54:]}"
        )
    out_lines.append("END")
    out_pdb.parent.mkdir(parents=True, exist_ok=True)
    out_pdb.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return out_pdb


def run_packmol_memgen(
    complex_pdb: Path,
    out_dir: Path,
    cfg: MembraneMDConfig,
    deps: dict[str, Any],
) -> Path:
    """Embed complex in POPC + TIP3P + NaCl via AmberTools packmol-memgen."""
    bin_path = find_packmol_memgen(deps)
    if not bin_path:
        raise RuntimeError(
            "packmol_memgen not found. Install ambertools (Linux/macOS conda-forge) "
            "or provide a pre-built membrane PDB via --prebuilt-pdb."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    # Short local name: MEMEMBED/keepligs path mangles long filenames.
    oriented = out_dir / "complex.pdb"
    orient_complex_for_membrane(complex_pdb, oriented, cfg.tm3, cfg.tm6)
    out_pdb = out_dir / "packed_membrane.pdb"
    # AmberTools packmol-memgen 2025.x:
    #   -l POPC -r 1 builds bilayer + water by default.
    #   Do NOT pass --solvate: that flag means "water only, no lipids".
    #   --preoriented + --keepligs: skip broken MEMEMBED+ligand path; we oriented.
    cmd = [
        bin_path,
        "-p",
        str(oriented.resolve()),
        "-l",
        "POPC",
        "-r",
        "1",
        "--salt",
        "--saltcon",
        str(cfg.salt_molar),
        "--dist",
        str(cfg.lipid_dist_a),
        "--dist_wat",
        str(cfg.water_dist_a),
        "--preoriented",
        "--keepligs",
        "--overwrite",
        "-o",
        str(out_pdb.resolve()),
        "--log",
        str((out_dir / "memgen_run.log").resolve()),
    ]
    log_path = out_dir / "packmol_memgen.log"
    print(f"  packmol_memgen: {' '.join(cmd)}", flush=True)
    proc = subprocess.run(
        cmd,
        cwd=str(out_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    log_path.write_text(
        f"CMD: {' '.join(cmd)}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n",
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"packmol_memgen failed (rc={proc.returncode}). See {log_path}"
        )

    # Discover output PDB (CLI -o or default names in CWD)
    candidates: list[Path] = []
    if out_pdb.is_file():
        candidates.append(out_pdb)
    candidates.extend(
        sorted(
            list(out_dir.glob("*.pdb"))
            + list(out_dir.glob("**/*solvated*.pdb"))
            + list(out_dir.glob("**/*packed*.pdb")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
    )
    # Accept POPC or common Amber lipid residue names after charmmlipid2amber
    lipid_tokens = ("POPC", "PA", "OL", "PC", "PLPC")
    chosen: Optional[Path] = None
    for cand in candidates:
        if not cand.is_file():
            continue
        if cand.name in {"complex.pdb", "complex_pre_membrane.pdb"}:
            continue
        if cand.name.startswith("receptor") or cand.name.endswith("_lig.pdb"):
            continue
        if cand.resolve() == complex_pdb.resolve():
            continue
        text_head = cand.read_text(encoding="utf-8", errors="replace")[:500_000]
        if any(tok in text_head for tok in lipid_tokens):
            chosen = cand
            if "POPC" in text_head or text_head.count("ATOM") > 5000:
                break
    if chosen is None:
        raise RuntimeError(
            f"packmol_memgen finished but no lipid-containing PDB found in {out_dir}. "
            f"See {log_path}"
        )
    final = out_dir / "membrane_system.pdb"
    if chosen.resolve() != final.resolve():
        shutil.copy2(chosen, final)
    return final


def build_and_run_membrane_complex(
    cfg: MembraneMDConfig,
    ligand_id: str,
    deps: dict[str, Any],
    ligand_sdf: Optional[Path] = None,
    prebuilt_pdb: Optional[Path] = None,
    build_only: bool = False,
) -> dict[str, Any]:
    from openmm import (
        LangevinMiddleIntegrator,
        MonteCarloMembraneBarostat,
        unit,
    )
    from openmm import app
    from openmm.app import HBonds, Modeller, PDBFile, PME, Simulation, StateDataReporter
    from openff.toolkit import Molecule
    from openmmforcefields.generators import GAFFTemplateGenerator

    work = cfg.out_dir / ligand_id
    work.mkdir(parents=True, exist_ok=True)

    rec_filt = work / "receptor_cb1_nofusion.pdb"
    filter_receptor_pdb(
        cfg.receptor_pdb, rec_filt, cfg.keep_residue_ranges, cfg.strip_fusion
    )
    rec_prot = work / "receptor_cb1_protonated.pdb"
    protonate_receptor_pdb(rec_filt, rec_prot)

    pose_path = pose_pdbqt_path(cfg.dock_dir, ligand_id)
    if ligand_sdf is None:
        ligand_sdf = work / f"{ligand_id}_pose.sdf"
        pdbqt_model_to_sdf(pose_path, ligand_sdf)

    off_mol = Molecule.from_file(
        str(ligand_sdf), file_format="sdf", allow_undefined_stereo=True
    )
    if off_mol.n_conformers == 0:
        off_mol.generate_conformers(n_conformers=1)
    gaff = GAFFTemplateGenerator(molecules=off_mol, forcefield="gaff-2.11")

    lig_pdb = work / f"{ligand_id}_lig.pdb"
    off_mol.to_file(str(lig_pdb), file_format="pdb")

    complex_pdb = work / "complex_pre_membrane.pdb"
    write_complex_pdb(rec_prot, lig_pdb, complex_pdb)

    if prebuilt_pdb is not None:
        memb_pdb = work / "membrane_system.pdb"
        shutil.copy2(prebuilt_pdb, memb_pdb)
    else:
        pack_dir = work / "packmol_memgen"
        memb_pdb = run_packmol_memgen(complex_pdb, pack_dir, cfg, deps)
        # copy to work root for convenience
        shutil.copy2(memb_pdb, work / "membrane_system.pdb")
        memb_pdb = work / "membrane_system.pdb"

    forcefield = app.ForceField(
        "amber14-all.xml",
        "amber14/lipid17.xml",
        "amber14/tip3p.xml",
    )
    forcefield.registerTemplateGenerator(gaff.generator)

    pdb = PDBFile(str(memb_pdb))
    modeller = Modeller(pdb.topology, pdb.positions)

    # If packmol_memgen stripped ligand naming, try to ensure LIG is present;
    # otherwise system may still include it as UNL/MOL from merged PDB.
    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=PME,
        nonbondedCutoff=1.0 * unit.nanometers,
        constraints=HBonds,
        rigidWater=True,
        ewaldErrorTolerance=0.0005,
    )
    # Semi-isotropic membrane barostat (XY isotropic, Z free)
    system.addForce(
        MonteCarloMembraneBarostat(
            cfg.pressure_atm * unit.atmospheres,
            0.0 * unit.bar * unit.nanometer,  # zero surface tension
            cfg.temperature_k * unit.kelvin,
            MonteCarloMembraneBarostat.XYIsotropic,
            MonteCarloMembraneBarostat.ZFree,
            25,
        )
    )

    integrator = LangevinMiddleIntegrator(
        cfg.temperature_k * unit.kelvin,
        1.0 / unit.picosecond,
        0.002 * unit.picoseconds,
    )
    integrator.setRandomNumberSeed(cfg.seed)

    platform = _select_platform(cfg.platform)
    simulation = Simulation(modeller.topology, system, integrator, platform)
    simulation.context.setPositions(modeller.positions)

    print(f"[{ligand_id}] platform={platform.getName()} minimize...", flush=True)
    simulation.minimizeEnergy(maxIterations=cfg.minimize_max_iter)

    state0 = simulation.context.getState(getPositions=True)
    min_pdb = work / "minimized.pdb"
    with open(min_pdb, "w", encoding="utf-8") as fh:
        PDBFile.writeFile(simulation.topology, state0.getPositions(), fh)

    meta = {
        "ligand_id": ligand_id,
        "receptor": "5TGZ",
        "membrane": "POPC bilayer (lipid17)",
        "solvent": f"TIP3P + NaCl {cfg.salt_molar} M",
        "forcefield_protein": "amber14-all",
        "forcefield_lipid": "amber14/lipid17",
        "forcefield_ligand": "GAFF2 (gaff-2.11 via OpenFF)",
        "barostat": "MonteCarloMembraneBarostat XYIsotropic/ZFree",
        "production_ns": cfg.production_ns,
        "seed": cfg.seed,
        "platform": platform.getName(),
        "membrane_pdb": str(memb_pdb.relative_to(ROOT))
        if memb_pdb.is_relative_to(ROOT)
        else str(memb_pdb),
        "minimized_pdb": str(min_pdb.relative_to(ROOT))
        if min_pdb.is_relative_to(ROOT)
        else str(min_pdb),
        "tm3_range": f"{cfg.tm3[0]}-{cfg.tm3[1]}",
        "tm6_range": f"{cfg.tm6[0]}-{cfg.tm6[1]}",
    }

    if build_only or (cfg.production_ns <= 0 and cfg.equil_ps <= 0):
        meta["status"] = "built"
        meta["note"] = "build-only / no production"
        (work / "metrics_summary.json").write_text(
            json.dumps(meta, indent=2), encoding="utf-8"
        )
        return meta

    # Equilibration: short NVT (barostat off) then NPT membrane
    equil_steps = int((cfg.equil_ps * unit.picoseconds) / (0.002 * unit.picoseconds))
    nvt_steps = max(equil_steps // 4, 1)
    npt_steps = max(equil_steps - nvt_steps, 1)

    barostat_force_index = None
    for i, f in enumerate(system.getForces()):
        if f.__class__.__name__ == "MonteCarloMembraneBarostat":
            barostat_force_index = i
            break
    if barostat_force_index is not None:
        system.getForce(barostat_force_index).setFrequency(0)

    print(f"[{ligand_id}] NVT equil ~{cfg.equil_ps/4:.1f} ps...", flush=True)
    simulation.context.setVelocitiesToTemperature(
        cfg.temperature_k * unit.kelvin, cfg.seed
    )
    simulation.step(nvt_steps)

    if barostat_force_index is not None:
        system.getForce(barostat_force_index).setFrequency(25)
    print(f"[{ligand_id}] NPT membrane equil ~{3*cfg.equil_ps/4:.1f} ps...", flush=True)
    simulation.step(npt_steps)

    traj_dcd = work / "production.dcd"
    log_path = work / "production.log"
    prod_steps = int(
        (cfg.production_ns * unit.nanoseconds) / (0.002 * unit.picoseconds)
    )
    report_steps = max(
        int((cfg.report_interval_ps * unit.picoseconds) / (0.002 * unit.picoseconds)),
        1,
    )
    simulation.reporters.append(app.DCDReporter(str(traj_dcd), report_steps))
    simulation.reporters.append(
        StateDataReporter(
            str(log_path),
            report_steps,
            step=True,
            time=True,
            potentialEnergy=True,
            temperature=True,
            volume=True,
            speed=True,
        )
    )
    print(
        f"[{ligand_id}] production {cfg.production_ns} ns "
        f"({prod_steps} steps, report every {report_steps})...",
        flush=True,
    )
    simulation.step(prod_steps)

    metrics = analyze_membrane_trajectory(
        topology_pdb=min_pdb,
        trajectory_dcd=traj_dcd,
        tm3=cfg.tm3,
        tm6=cfg.tm6,
    )
    metrics.update(meta)
    metrics["status"] = "ok"
    metrics["traj_dcd"] = (
        str(traj_dcd.relative_to(ROOT)) if traj_dcd.is_relative_to(ROOT) else str(traj_dcd)
    )
    (work / "metrics_summary.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    return metrics


def _pca_axis(coords) -> Any:
    """Principal axis of a set of 3D points (mdtraj nm array Nx3)."""
    import numpy as np

    c = coords - coords.mean(axis=0)
    # covariance eigen
    cov = c.T @ c / max(len(c) - 1, 1)
    vals, vecs = np.linalg.eigh(cov)
    axis = vecs[:, int(np.argmax(vals))]
    return axis / (np.linalg.norm(axis) + 1e-12)


def analyze_membrane_trajectory(
    topology_pdb: Path,
    trajectory_dcd: Path,
    tm3: tuple[int, int],
    tm6: tuple[int, int],
) -> dict[str, Any]:
    """TM6 RMSD, TM3–TM6 COM distance, helix-axis angle, phenolic H-bond %."""
    try:
        import mdtraj as md
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("mdtraj+numpy required for trajectory analysis") from exc

    traj = md.load(str(trajectory_dcd), top=str(topology_pdb))
    top = traj.topology

    def ca_atoms_by_resseq(targets: set[int]) -> list[int]:
        idxs: list[int] = []
        for a in top.atoms:
            if a.name != "CA":
                continue
            try:
                r = int(a.residue.resSeq)
            except Exception:  # noqa: BLE001
                r = a.residue.index + 1
            if r in targets:
                idxs.append(a.index)
        return idxs

    def resolve_tm_ca(lo: int, hi: int) -> list[int]:
        direct = ca_atoms_by_resseq(set(range(lo, hi + 1)))
        if len(direct) >= 3:
            return direct
        nofusion = topology_pdb.parent / "receptor_cb1_nofusion.pdb"
        if nofusion.is_file():
            order = _uniprot_ca_resseqs_from_pdb(nofusion)
            serial = _map_uniprot_range_to_serial(order, lo, hi)
            mapped = ca_atoms_by_resseq(set(serial))
            if len(mapped) >= 3:
                return mapped
        return direct

    tm3_idx = resolve_tm_ca(tm3[0], tm3[1])
    tm6_idx = resolve_tm_ca(tm6[0], tm6[1])
    if len(tm6_idx) < 3:
        raise RuntimeError(f"Too few TM6 CA atoms ({len(tm6_idx)}) for range {tm6}.")
    if len(tm3_idx) < 3:
        raise RuntimeError(f"Too few TM3 CA atoms ({len(tm3_idx)}) for range {tm3}.")

    rmsd_a = md.rmsd(traj, traj, 0, atom_indices=tm6_idx) * 10.0
    xyz = traj.xyz
    com3 = xyz[:, tm3_idx, :].mean(axis=1)
    com6 = xyz[:, tm6_idx, :].mean(axis=1)
    dist_a = np.linalg.norm(com3 - com6, axis=1) * 10.0

    angles = np.zeros(traj.n_frames, dtype=float)
    for fi in range(traj.n_frames):
        a3 = _pca_axis(xyz[fi, tm3_idx, :])
        a6 = _pca_axis(xyz[fi, tm6_idx, :])
        cos = float(np.clip(abs(np.dot(a3, a6)), 0.0, 1.0))
        angles[fi] = math.degrees(math.acos(cos))

    # Phenolic H-bond (same flexible criterion as soluble MD)
    protein_res = {
        "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
        "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
        "HID", "HIE", "HIP",
    }
    lipid_res = {"POPC", "POPE", "POPS", "CHL", "CHL1", "TIP3", "WAT", "HOH", "NA", "CL", "NA+", "CL-"}
    bonds: dict[int, list[int]] = {}
    for a, b in top.bonds:
        bonds.setdefault(a.index, []).append(b.index)
        bonds.setdefault(b.index, []).append(a.index)

    donors: list[int] = []
    for a in top.atoms:
        rname = a.residue.name.strip().upper()
        if rname in protein_res or rname in lipid_res:
            continue
        if a.element.symbol != "O":
            continue
        neigh = bonds.get(a.index, [])
        heavy = [j for j in neigh if top.atom(j).element.symbol != "H"]
        if len(heavy) == 1 and top.atom(heavy[0]).element.symbol == "C":
            donors.append(a.index)

    acceptors: list[int] = []
    for a in top.atoms:
        if a.residue.name.strip().upper() not in protein_res:
            continue
        if a.element.symbol in {"O", "N"}:
            acceptors.append(a.index)

    hbond_on = []
    if donors and acceptors:
        d_xyz = xyz[:, donors, :]
        a_xyz = xyz[:, acceptors, :]
        for fi in range(xyz.shape[0]):
            d = d_xyz[fi][:, None, :] - a_xyz[fi][None, :, :]
            dist = np.linalg.norm(d, axis=-1) * 10.0
            hbond_on.append(bool(dist.min() <= HBOND_DIST_CUTOFF_A))
    else:
        hbond_on = [False] * traj.n_frames
    hbond_pct = 100.0 * (sum(hbond_on) / max(len(hbond_on), 1))

    frame_csv = topology_pdb.parent / "frame_metrics.csv"
    with frame_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(
            [
                "frame",
                "time_ps_est",
                "tm6_ca_rmsd_A",
                "tm3_tm6_com_A",
                "tm3_tm6_angle_deg",
                "phenol_hbond",
            ]
        )
        dt = 10.0
        for i in range(traj.n_frames):
            w.writerow(
                [
                    i,
                    i * dt,
                    f"{rmsd_a[i]:.4f}",
                    f"{dist_a[i]:.4f}",
                    f"{angles[i]:.4f}",
                    int(hbond_on[i]),
                ]
            )

    return {
        "n_frames": int(traj.n_frames),
        "tm6_ca_rmsd_mean_A": float(np.mean(rmsd_a)),
        "tm6_ca_rmsd_std_A": float(np.std(rmsd_a)),
        "tm6_ca_rmsd_final_A": float(rmsd_a[-1]),
        "tm3_tm6_com_mean_A": float(np.mean(dist_a)),
        "tm3_tm6_com_std_A": float(np.std(dist_a)),
        "tm3_tm6_com_final_A": float(dist_a[-1]),
        "tm3_tm6_angle_mean_deg": float(np.mean(angles)),
        "tm3_tm6_angle_std_deg": float(np.std(angles)),
        "tm3_tm6_angle_final_deg": float(angles[-1]),
        "phenol_hbond_pct": float(hbond_pct),
        "n_tm3_ca": len(tm3_idx),
        "n_tm6_ca": len(tm6_idx),
        "n_phenol_donors": len(donors),
        "n_acceptors_scanned": len(acceptors),
        "frame_metrics_csv": str(frame_csv),
    }


def write_aggregate_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "ligand_id",
        "receptor",
        "status",
        "production_ns",
        "seed",
        "platform",
        "tm3_range",
        "tm6_range",
        "tm6_ca_rmsd_mean_A",
        "tm6_ca_rmsd_std_A",
        "tm3_tm6_com_mean_A",
        "tm3_tm6_com_std_A",
        "tm3_tm6_angle_mean_deg",
        "tm3_tm6_angle_std_deg",
        "phenol_hbond_pct",
        "n_frames",
        "forcefield_ligand",
        "membrane",
        "solvent",
        "note",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_stub_metrics(
    path: Path, ligand_ids: list[str], cfg: MembraneMDConfig, note: str
) -> None:
    rows = []
    for lid in ligand_ids:
        rows.append(
            {
                "ligand_id": lid,
                "receptor": "5TGZ",
                "status": "stub",
                "production_ns": cfg.production_ns,
                "seed": cfg.seed,
                "platform": "",
                "tm3_range": f"{cfg.tm3[0]}-{cfg.tm3[1]}",
                "tm6_range": f"{cfg.tm6[0]}-{cfg.tm6[1]}",
                "tm6_ca_rmsd_mean_A": "",
                "tm6_ca_rmsd_std_A": "",
                "tm3_tm6_com_mean_A": "",
                "tm3_tm6_com_std_A": "",
                "tm3_tm6_angle_mean_deg": "",
                "tm3_tm6_angle_std_deg": "",
                "phenol_hbond_pct": "",
                "n_frames": "",
                "forcefield_ligand": "GAFF2 (pending)",
                "membrane": "POPC bilayer (lipid17)",
                "solvent": f"TIP3P + NaCl {cfg.salt_molar} M",
                "note": note,
            }
        )
    write_aggregate_csv(path, rows)


def dry_run(cfg: MembraneMDConfig, ligand_ids: list[str]) -> int:
    print("=== dry-run: membrane MD inputs + deps (no MD) ===", flush=True)
    print(f"receptor: {cfg.receptor_pdb} exists={cfg.receptor_pdb.is_file()}")
    print(f"dock_dir: {cfg.dock_dir}")
    print(f"out_dir:  {cfg.out_dir}")
    print(
        f"TM3 CA: {cfg.tm3[0]}-{cfg.tm3[1]} | TM6 CA: {cfg.tm6[0]}-{cfg.tm6[1]} "
        f"| strip_fusion={cfg.strip_fusion}"
    )
    print(
        f"protocol: POPC + TIP3P + NaCl {cfg.salt_molar} M | "
        f"min {cfg.minimize_max_iter} | equil {cfg.equil_ps} ps | "
        f"prod {cfg.production_ns} ns | seed={cfg.seed}"
    )
    print(f"panel: {ligand_ids}")
    problems = validate_inputs(cfg, ligand_ids)
    for lid in ligand_ids:
        p = pose_pdbqt_path(cfg.dock_dir, lid)
        print(f"  pose {lid}: {p} exists={p.is_file()}")
        if p.is_file():
            try:
                block = extract_model1_pdbqt(p)
                nat = sum(1 for ln in block.splitlines() if ln.startswith("ATOM"))
                print(f"    MODEL1 atoms: {nat}")
            except Exception as exc:  # noqa: BLE001
                problems.append(f"{lid}: {exc}")
    deps = probe_membrane_deps()
    print(
        "deps:",
        json.dumps(
            {
                k: v
                for k, v in deps.items()
                if k not in {"errors"}
            },
            indent=2,
            default=str,
        ),
    )
    if deps.get("errors"):
        print("dep notes:")
        for e in deps["errors"]:
            print(f"  - {e}")
    cfg.out_dir.mkdir(parents=True, exist_ok=True)
    if problems:
        print("INPUT PROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        write_stub_metrics(
            cfg.metrics_csv, ligand_ids, cfg, note="dry-run failed input validation"
        )
        return 2
    if not deps.get("gaff_ready"):
        print("\n" + membrane_install_message())
        write_stub_metrics(
            cfg.metrics_csv,
            ligand_ids,
            cfg,
            note="dry-run OK inputs; GAFF2/OpenFF not available",
        )
        print(f"stub metrics: {cfg.metrics_csv}")
        return 0
    if not deps.get("lipid17"):
        print("WARNING: amber14/lipid17.xml not loadable")
    if not deps.get("packmol_memgen"):
        print(
            "WARNING: packmol_memgen missing — production needs AmberTools "
            "or --prebuilt-pdb. Dry-run of poses still OK."
        )
        write_stub_metrics(
            cfg.metrics_csv,
            ligand_ids,
            cfg,
            note="dry-run OK poses; packmol_memgen missing for membrane build",
        )
        print(f"stub: {cfg.metrics_csv}")
        return 0
    write_stub_metrics(
        cfg.metrics_csv,
        ligand_ids,
        cfg,
        note="dry-run OK; membrane deps ready — re-run without --dry-run",
    )
    print(f"membrane deps ready. stub: {cfg.metrics_csv}")
    return 0


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs/deps only")
    ap.add_argument(
        "--ns",
        type=float,
        default=None,
        help="Production length in ns (default 20)",
    )
    ap.add_argument(
        "--ligand",
        action="append",
        dest="ligands",
        help="h1_02c|thcv|thc|all or full id (repeatable). Default: all",
    )
    ap.add_argument("--receptor", type=Path, default=None)
    ap.add_argument("--dock-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--metrics-csv", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=None)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--platform", type=str, default=None, help="CUDA|OpenCL|CPU")
    ap.add_argument(
        "--ligand-sdf",
        type=Path,
        default=None,
        help="Optional pre-built SDF for a single --ligand (gitignored local)",
    )
    ap.add_argument(
        "--prebuilt-pdb",
        type=Path,
        default=None,
        help="Skip packmol_memgen; use this membrane+complex PDB (local)",
    )
    ap.add_argument(
        "--build-only",
        action="store_true",
        help="Build+minimize membrane system; skip equilibration/production",
    )
    return ap.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    cfg = config_from_args(args)
    try:
        ligand_ids = resolve_ligand_ids(args.ligands)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.dry_run:
        return dry_run(cfg, ligand_ids)

    problems = validate_inputs(cfg, ligand_ids)
    if problems:
        print("INPUT PROBLEMS:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 2

    deps = probe_membrane_deps()
    if not deps.get("gaff_ready"):
        print(membrane_install_message(), file=sys.stderr)
        write_stub_metrics(
            cfg.metrics_csv,
            ligand_ids,
            cfg,
            note="MD blocked: OpenFF/GAFF2 unavailable",
        )
        return 3
    if not deps.get("lipid17"):
        print("amber14/lipid17.xml required for POPC", file=sys.stderr)
        return 3
    if args.prebuilt_pdb is None and not deps.get("packmol_memgen"):
        print(membrane_install_message(), file=sys.stderr)
        print("Missing packmol_memgen and no --prebuilt-pdb.", file=sys.stderr)
        return 3

    rows: list[dict[str, Any]] = []
    for lid in ligand_ids:
        try:
            lig_sdf = (
                args.ligand_sdf if (args.ligand_sdf and len(ligand_ids) == 1) else None
            )
            prebuilt = (
                Path(args.prebuilt_pdb)
                if (args.prebuilt_pdb and len(ligand_ids) == 1)
                else None
            )
            m = build_and_run_membrane_complex(
                cfg,
                lid,
                deps,
                ligand_sdf=lig_sdf,
                prebuilt_pdb=prebuilt,
                build_only=args.build_only,
            )
            rows.append(m)
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            rows.append(
                {
                    "ligand_id": lid,
                    "receptor": "5TGZ",
                    "status": f"error: {exc}",
                    "production_ns": cfg.production_ns,
                    "seed": cfg.seed,
                    "tm3_range": f"{cfg.tm3[0]}-{cfg.tm3[1]}",
                    "tm6_range": f"{cfg.tm6[0]}-{cfg.tm6[1]}",
                    "forcefield_ligand": "GAFF2",
                    "membrane": "POPC bilayer (lipid17)",
                    "solvent": f"TIP3P + NaCl {cfg.salt_molar} M",
                    "note": str(exc),
                }
            )

    write_aggregate_csv(cfg.metrics_csv, rows)
    print(f"Wrote {cfg.metrics_csv}")
    ok = all(r.get("status") in {"ok", "built"} for r in rows)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
