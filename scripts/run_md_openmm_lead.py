#!/usr/bin/env python3
"""Short OpenMM MD: CB1 inactive 5TGZ + JANUS_H1_02c vs delta9-THCV.

Compares local Vina poses in explicit TIP3P (no membrane). Metrics probe whether
the 1′-methyl lead behaves as a geometric “ratchet” vs THCV in the inactive
receptor — not functional agonism / Janus α.

IP
----
- Reads docked poses from gitignored paths (default: results/docking/h1_h5_batch3/).
- Never embeds SMILES/coordinates in this script or in public reports.
- Trajectories / metrics CSV land under results/md/ (gitignored).

Force field / setup (production path)
------------------------------------
- Protein: amber14-all.xml + tip3p.xml (OpenMM)
- Ligand: GAFF2 via openmmforcefields.GAFFTemplateGenerator + OpenFF Toolkit
  (fallback message if OpenFF/antechamber unavailable)
- Solvent: cubic TIP3P box, neutralize, NaCl 0.15 M

Stages
------
1. Minimization 5000 steps
2. Short NVT then NPT equilibration (~100 ps), 300 K, 1 atm
3. NPT production (CLI --ns; default 2)

Metrics
-------
- Cα RMSD of TM6 vs minimized frame
- COM distance of Cα atoms TM3 vs TM6
- Phenolic H-bond persistence (% frames; flexible ligand OH → protein acceptor)

Residue indices (5TGZ / UniProt P21554 numbering; GPCRdb CNR1_HUMAN):
  TM3: 185–220 (S3.21–R3.56); TM6: 332–369 (P6.24–G6.61).
  Override via --config YAML. 5TGZ flavodoxin insert (≈1002–1148) is stripped
  by default so ICL3 is a peptide gap — document in md_lead_plan.md.

Usage
-----
  python scripts/run_md_openmm_lead.py --dry-run
  python scripts/run_md_openmm_lead.py --ns 2
  python scripts/run_md_openmm_lead.py --ligand JANUS_H1_02c --ns 0.01  # smoke
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import traceback
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Defaults (paths point at gitignored local artifacts)
# ---------------------------------------------------------------------------

DEFAULT_RECEPTOR = ROOT / "data/targets/cb1/5TGZ_clean.pdb"
DEFAULT_DOCK_DIR = ROOT / "results/docking/h1_h5_batch3/cb1"
DEFAULT_OUT_DIR = ROOT / "results/md"
DEFAULT_METRICS_CSV = DEFAULT_OUT_DIR / "janus_h1_02c_vs_thcv_5tgz.csv"

# GPCRdb CNR1_HUMAN / 5TGZ UniProt residue numbers
DEFAULT_TM3 = (185, 220)
DEFAULT_TM6 = (332, 369)
# Strip flavodoxin fusion insert in 5TGZ chimera
DEFAULT_KEEP_RESIDUE_RANGES = ((99, 306), (332, 414))

LIGAND_IDS = ("JANUS_H1_02c", "delta9-THCV")

HBOND_DIST_CUTOFF_A = 3.5
HBOND_ANGLE_CUTOFF_DEG = 120.0  # D–H···A if H present; else donor–acceptor only


@dataclass
class MDConfig:
    receptor_pdb: Path = DEFAULT_RECEPTOR
    dock_dir: Path = DEFAULT_DOCK_DIR
    out_dir: Path = DEFAULT_OUT_DIR
    metrics_csv: Path = DEFAULT_METRICS_CSV
    tm3: tuple[int, int] = DEFAULT_TM3
    tm6: tuple[int, int] = DEFAULT_TM6
    keep_residue_ranges: list[tuple[int, int]] = field(
        default_factory=lambda: list(DEFAULT_KEEP_RESIDUE_RANGES)
    )
    padding_nm: float = 1.0
    salt_molar: float = 0.15
    temperature_k: float = 300.0
    pressure_atm: float = 1.0
    minimize_max_iter: int = 5000
    equil_ps: float = 100.0
    production_ns: float = 2.0
    report_interval_ps: float = 10.0
    seed: int = 42
    platform: Optional[str] = None  # CUDA / OpenCL / CPU
    strip_fusion: bool = True


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


def config_from_args(args: argparse.Namespace) -> MDConfig:
    y = _load_yaml_config(args.config)
    cfg = MDConfig()
    if "receptor_pdb" in y:
        cfg.receptor_pdb = Path(y["receptor_pdb"])
    if "dock_dir" in y:
        cfg.dock_dir = Path(y["dock_dir"])
    if "out_dir" in y:
        cfg.out_dir = Path(y["out_dir"])
    if "metrics_csv" in y:
        cfg.metrics_csv = Path(y["metrics_csv"])
    if "tm3" in y:
        cfg.tm3 = (int(y["tm3"][0]), int(y["tm3"][1]))
    if "tm6" in y:
        cfg.tm6 = (int(y["tm6"][0]), int(y["tm6"][1]))
    if "keep_residue_ranges" in y:
        cfg.keep_residue_ranges = [
            (int(a), int(b)) for a, b in y["keep_residue_ranges"]
        ]
    for key in (
        "padding_nm",
        "salt_molar",
        "temperature_k",
        "pressure_atm",
        "equil_ps",
        "report_interval_ps",
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
    if not cfg.receptor_pdb.is_absolute():
        cfg.receptor_pdb = ROOT / cfg.receptor_pdb
    if not cfg.dock_dir.is_absolute():
        cfg.dock_dir = ROOT / cfg.dock_dir
    if not cfg.out_dir.is_absolute():
        cfg.out_dir = ROOT / cfg.out_dir
    if not cfg.metrics_csv.is_absolute():
        cfg.metrics_csv = ROOT / cfg.metrics_csv
    return cfg


# ---------------------------------------------------------------------------
# Dependency probes
# ---------------------------------------------------------------------------

def probe_deps() -> dict[str, Any]:
    info: dict[str, Any] = {
        "openmm": False,
        "openmm_version": None,
        "openff": False,
        "openmmforcefields": False,
        "rdkit": False,
        "mdtraj": False,
        "pdbfixer": False,
        "gaff_ready": False,
        "errors": [],
    }
    try:
        import openmm

        info["openmm"] = True
        info["openmm_version"] = openmm.__version__
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"openmm: {exc}")
    try:
        import openff.toolkit  # noqa: F401
        from openff.toolkit import Molecule  # noqa: F401

        info["openff"] = True
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"openff-toolkit: {exc}")
    try:
        from openmmforcefields.generators import GAFFTemplateGenerator  # noqa: F401

        info["openmmforcefields"] = True
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"openmmforcefields: {exc}")
    try:
        from rdkit import Chem  # noqa: F401

        info["rdkit"] = True
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"rdkit: {exc}")
    try:
        import mdtraj  # noqa: F401

        info["mdtraj"] = True
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"mdtraj: {exc}")
    try:
        import pdbfixer  # noqa: F401

        info["pdbfixer"] = True
    except Exception as exc:  # noqa: BLE001
        info["errors"].append(f"pdbfixer: {exc}")

    info["gaff_ready"] = bool(
        info["openmm"] and info["openff"] and info["openmmforcefields"] and info["rdkit"]
    )
    return info


def gaff_install_message() -> str:
    return (
        "GAFF2 ligand parametrization requires a working OpenFF Toolkit + "
        "openmmforcefields (GAFFTemplateGenerator).\n"
        "PyPI openff-toolkit==0.18.0 is yanked / incomplete - use conda-forge:\n"
        "  conda create -n janus-md -c conda-forge python=3.12 \\\n"
        "    openmm openmmforcefields openff-toolkit ambertools mdtraj pdbfixer rdkit\n"
        "  conda activate janus-md\n"
        "See requirements-md.txt and results/reports/md_lead_plan.md."
    )


# ---------------------------------------------------------------------------
# Pose / receptor I/O (no SMILES written to public outputs)
# ---------------------------------------------------------------------------

def pose_pdbqt_path(dock_dir: Path, ligand_id: str) -> Path:
    return dock_dir / f"{ligand_id}_docked.pdbqt"


def extract_model1_pdbqt(pdbqt_path: Path) -> str:
    """Return MODEL 1 block as PDB-like ATOM/HETATM lines (no REMARK/SMILES)."""
    text = pdbqt_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    in_model = False
    model_idx = 0
    keep: list[str] = []
    for line in lines:
        if line.startswith("MODEL"):
            model_idx += 1
            in_model = model_idx == 1
            continue
        if line.startswith("ENDMDL"):
            if in_model:
                break
            in_model = False
            continue
        if model_idx == 0:
            # some writers omit MODEL for single pose
            in_model = True
            model_idx = 1
        if not in_model:
            continue
        if line.startswith(("ATOM", "HETATM")):
            # PDBQT has charge/type in cols 67+; trim to PDB-ish 66 chars
            keep.append(line[:66].rstrip())
        elif line.startswith("TER"):
            keep.append("TER")
    if not keep:
        raise ValueError(f"No ATOM/HETATM in MODEL 1 of {pdbqt_path}")
    keep.append("END")
    return "\n".join(keep) + "\n"


def pdbqt_model_to_sdf(pdbqt_path: Path, sdf_path: Path) -> Path:
    """Convert docked PDBQT MODEL 1 → SDF via RDKit (coordinates only; local file)."""
    from rdkit import Chem
    from rdkit.Chem import AllChem

    pdb_block = extract_model1_pdbqt(pdbqt_path)
    # Rewrite HETATM→ATOM and residue name UNL for RDKit PDB parser
    pdb_block = re.sub(r"^HETATM", "ATOM  ", pdb_block, flags=re.M)
    mol = Chem.MolFromPDBBlock(pdb_block, removeHs=False, sanitize=False)
    if mol is None or mol.GetNumAtoms() == 0:
        raise RuntimeError(
            f"RDKit failed to parse pose PDB from {pdbqt_path}. "
            "Provide a local SDF via --ligand-sdf or fix the PDBQT."
        )
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        # Docked PDBQT often lacks bond orders; keep geometry, infer later via OpenFF
        pass
    mol = Chem.AddHs(mol, addCoords=True)
    sdf_path.parent.mkdir(parents=True, exist_ok=True)
    w = Chem.SDWriter(str(sdf_path))
    w.write(mol)
    w.close()
    # Strip any property that might carry SMILES if present
    return sdf_path


def filter_receptor_pdb(
    src: Path,
    dst: Path,
    keep_ranges: Iterable[tuple[int, int]],
    strip_fusion: bool,
) -> Path:
    """Keep ATOM records in UniProt CB1 ranges; drop flavodoxin insert / HETATM."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    ranges = list(keep_ranges) if strip_fusion else [(None, None)]  # type: ignore[list-item]
    out_lines: list[str] = []
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("ATOM"):
            try:
                resseq = int(line[22:26])
            except ValueError:
                continue
            if strip_fusion:
                if any(a <= resseq <= b for a, b in ranges):  # type: ignore[operator]
                    out_lines.append(line)
            else:
                out_lines.append(line)
        elif line.startswith("TER"):
            out_lines.append("TER")
        elif line.startswith("END"):
            break
        # drop HETATM (crystallographic ligand / lipids) — docked ligand added separately
    out_lines.append("END")
    dst.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return dst


def protonate_receptor_pdb(src: Path, dst: Path, pH: float = 7.0) -> Path:
    """Rebuild incomplete sidechains + add hydrogens; keep UniProt resSeq.

    5TGZ often has truncated sidechains (e.g. MET with only CB). Modeller
    addHydrogens alone fails template matching on those residues. PDBFixer
    adds missing heavy atoms; keepIds=True preserves UniProt numbering so
    TM3/TM6 selections stay valid. Intentionally does NOT rebuild missing
    loops (ICL3 gap after flavodoxin strip).
    """
    from openmm.app import PDBFile
    from pdbfixer import PDBFixer

    fixer = PDBFixer(filename=str(src))
    fixer.findMissingResidues()
    # Do not insert the deleted ICL3 / fusion gap as a modelled loop
    fixer.missingResidues = {}
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(pH)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        PDBFile.writeFile(fixer.topology, fixer.positions, fh, keepIds=True)

    # Sanity: UniProt TM6 must still be addressable after protonation
    resseqs = []
    for line in dst.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            try:
                resseqs.append(int(line[22:26]))
            except ValueError:
                continue
    if resseqs and max(resseqs) < 332:
        raise RuntimeError(
            f"Protonated receptor lost UniProt numbering (CA resSeq max={max(resseqs)}). "
            "TM6 selection would fail."
        )
    return dst


def _uniprot_ca_resseqs_from_pdb(pdb_path: Path) -> list[int]:
    """Ordered Cα UniProt/resSeq list from a filtered receptor PDB."""
    out: list[int] = []
    for line in pdb_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            try:
                out.append(int(line[22:26]))
            except ValueError:
                continue
    return out


def _map_uniprot_range_to_serial(
    uniprot_order: list[int], lo: int, hi: int
) -> list[int]:
    """Map UniProt inclusive range → 1-based serial resSeq after renumbering."""
    return [i + 1 for i, u in enumerate(uniprot_order) if lo <= u <= hi]


def validate_inputs(cfg: MDConfig, ligand_ids: list[str]) -> list[str]:
    problems: list[str] = []
    if not cfg.receptor_pdb.is_file():
        problems.append(f"missing receptor: {cfg.receptor_pdb}")
    for lid in ligand_ids:
        p = pose_pdbqt_path(cfg.dock_dir, lid)
        if not p.is_file():
            problems.append(f"missing pose: {p}")
    return problems


# ---------------------------------------------------------------------------
# System build + MD
# ---------------------------------------------------------------------------

def _select_platform(name: Optional[str]):
    from openmm import Platform

    if name:
        return Platform.getPlatformByName(name)
    for candidate in ("CUDA", "OpenCL", "CPU"):
        try:
            return Platform.getPlatformByName(candidate)
        except Exception:  # noqa: BLE001
            continue
    return Platform.getPlatformByName("Reference")


def build_and_run_complex(
    cfg: MDConfig,
    ligand_id: str,
    ligand_sdf: Optional[Path] = None,
) -> dict[str, Any]:
    """Full MD for one complex; returns paths + summary stats."""
    from openmm import LangevinMiddleIntegrator, MonteCarloBarostat, unit
    from openmm import app
    from openmm.app import HBonds, Modeller, PME, PDBFile, Simulation, StateDataReporter
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

    off_mol = Molecule.from_file(str(ligand_sdf), file_format="sdf", allow_undefined_stereo=True)
    # Ensure conformer exists
    if off_mol.n_conformers == 0:
        off_mol.generate_conformers(n_conformers=1)
    gaff = GAFFTemplateGenerator(molecules=off_mol, forcefield="gaff-2.11")

    forcefield = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    forcefield.registerTemplateGenerator(gaff.generator)

    protein = PDBFile(str(rec_prot))
    # Write ligand PDB from OpenFF for Modeller
    lig_pdb = work / f"{ligand_id}_lig.pdb"
    off_mol.to_file(str(lig_pdb), file_format="pdb")
    ligand_pdb = PDBFile(str(lig_pdb))

    modeller = Modeller(protein.topology, protein.positions)
    modeller.add(ligand_pdb.topology, ligand_pdb.positions)
    modeller.addSolvent(
        forcefield,
        model="tip3p",
        padding=cfg.padding_nm * unit.nanometers,
        ionicStrength=cfg.salt_molar * unit.molar,
        neutralize=True,
        boxShape="cube",
    )

    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=PME,
        nonbondedCutoff=1.0 * unit.nanometers,
        constraints=HBonds,
        rigidWater=True,
        ewaldErrorTolerance=0.0005,
    )
    system.addForce(
        MonteCarloBarostat(
            cfg.pressure_atm * unit.atmospheres,
            cfg.temperature_k * unit.kelvin,
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

    # NVT: temporarily disable barostat by setting frequency huge via context? 
    # Simpler: short heat with barostat on is fine for ~100 ps total equilibration.
    equil_steps = int((cfg.equil_ps * unit.picoseconds) / (0.002 * unit.picoseconds))
    nvt_steps = max(equil_steps // 2, 1)
    npt_steps = max(equil_steps - nvt_steps, 1)

    # NVT phase: remove barostat force for half equilibration
    barostat_force_index = None
    for i, f in enumerate(system.getForces()):
        if f.__class__.__name__ == "MonteCarloBarostat":
            barostat_force_index = i
            break
    if barostat_force_index is not None:
        system.getForce(barostat_force_index).setFrequency(0)

    print(f"[{ligand_id}] NVT equil ~{cfg.equil_ps/2:.1f} ps...", flush=True)
    simulation.context.setVelocitiesToTemperature(cfg.temperature_k * unit.kelvin, cfg.seed)
    simulation.step(nvt_steps)

    if barostat_force_index is not None:
        system.getForce(barostat_force_index).setFrequency(25)
    print(f"[{ligand_id}] NPT equil ~{cfg.equil_ps/2:.1f} ps...", flush=True)
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

    metrics = analyze_trajectory(
        topology_pdb=min_pdb,
        trajectory_dcd=traj_dcd,
        tm3=cfg.tm3,
        tm6=cfg.tm6,
        ligand_resname_guess=("UNL", "LIG", "MOL"),
    )
    metrics.update(
        {
            "ligand_id": ligand_id,
            "receptor": "5TGZ",
            "production_ns": cfg.production_ns,
            "seed": cfg.seed,
            "platform": platform.getName(),
            "traj_dcd": str(traj_dcd.relative_to(ROOT)) if traj_dcd.is_relative_to(ROOT) else str(traj_dcd),
            "minimized_pdb": str(min_pdb.relative_to(ROOT)) if min_pdb.is_relative_to(ROOT) else str(min_pdb),
            "forcefield_protein": "amber14-all",
            "forcefield_ligand": "GAFF2 (gaff-2.11 via OpenFF)",
            "solvent": "TIP3P cubic + NaCl 0.15 M (no membrane)",
            "tm3_range": f"{cfg.tm3[0]}-{cfg.tm3[1]}",
            "tm6_range": f"{cfg.tm6[0]}-{cfg.tm6[1]}",
            "status": "ok",
        }
    )
    summary_json = work / "metrics_summary.json"
    # Do not dump structures; numeric metrics only
    summary_json.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def analyze_trajectory(
    topology_pdb: Path,
    trajectory_dcd: Path,
    tm3: tuple[int, int],
    tm6: tuple[int, int],
    ligand_resname_guess: tuple[str, ...] = ("UNL", "LIG", "MOL"),  # noqa: ARG001
) -> dict[str, Any]:
    """Compute TM6 Cα RMSD, TM3–TM6 COM distance, phenolic H-bond % (mdtraj)."""
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
        """Select TM Cα by UniProt resSeq; remap if topology was renumbered 1..N."""
        direct = ca_atoms_by_resseq(set(range(lo, hi + 1)))
        if len(direct) >= 3:
            return direct
        # Legacy PDBFixer outputs: serial 1..N. Map via receptor_cb1_nofusion.pdb.
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
        raise RuntimeError(
            f"Too few TM6 CA atoms ({len(tm6_idx)}) for range {tm6}. "
            "Check residue numbering / fusion strip."
        )
    if len(tm3_idx) < 3:
        raise RuntimeError(
            f"Too few TM3 CA atoms ({len(tm3_idx)}) for range {tm3}."
        )

    # RMSD TM6 Cα vs frame 0 (mdtraj.rmsd is in nm → Å)
    rmsd_a = md.rmsd(traj, traj, 0, atom_indices=tm6_idx) * 10.0

    xyz = traj.xyz  # nm
    com3 = xyz[:, tm3_idx, :].mean(axis=1)
    com6 = xyz[:, tm6_idx, :].mean(axis=1)
    dist_nm = np.linalg.norm(com3 - com6, axis=1)
    dist_a = dist_nm * 10.0

    # Phenolic H-bond persistence
    # Rebuild donor/acceptor from mdtraj topology
    protein_res = {
        "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
        "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
        "HID", "HIE", "HIP",
    }
    bonds: dict[int, list[int]] = {}
    for a, b in top.bonds:
        bonds.setdefault(a.index, []).append(b.index)
        bonds.setdefault(b.index, []).append(a.index)

    donors: list[int] = []
    for a in top.atoms:
        rname = a.residue.name.strip().upper()
        if rname in protein_res or rname in {"HOH", "WAT", "NA", "CL", "NA+", "CL-"}:
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
        d_xyz = xyz[:, donors, :]  # (F, D, 3)
        a_xyz = xyz[:, acceptors, :]
        # pairwise min distance per frame
        for fi in range(xyz.shape[0]):
            d = d_xyz[fi][:, None, :] - a_xyz[fi][None, :, :]
            dist = np.linalg.norm(d, axis=-1) * 10.0  # Å
            hbond_on.append(bool(dist.min() <= HBOND_DIST_CUTOFF_A))
    else:
        hbond_on = [False] * traj.n_frames

    hbond_pct = 100.0 * (sum(hbond_on) / max(len(hbond_on), 1))

    # Per-frame table (local)
    frame_csv = topology_pdb.parent / "frame_metrics.csv"
    with frame_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["frame", "time_ps_est", "tm6_ca_rmsd_A", "tm3_tm6_com_A", "phenol_hbond"])
        dt = 10.0  # matches default report_interval_ps if unchanged
        for i in range(traj.n_frames):
            w.writerow(
                [
                    i,
                    i * dt,
                    f"{rmsd_a[i]:.4f}",
                    f"{dist_a[i]:.4f}",
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
        "phenol_hbond_pct",
        "n_frames",
        "forcefield_ligand",
        "solvent",
        "note",
    ]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_stub_metrics(path: Path, ligand_ids: list[str], cfg: MDConfig, note: str) -> None:
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
                "phenol_hbond_pct": "",
                "n_frames": "",
                "forcefield_ligand": "GAFF2 (pending OpenFF)",
                "solvent": "TIP3P cubic + NaCl 0.15 M (no membrane)",
                "note": note,
            }
        )
    write_aggregate_csv(path, rows)


def dry_run(cfg: MDConfig, ligand_ids: list[str]) -> int:
    print("=== dry-run: validate inputs + deps (no MD) ===", flush=True)
    print(f"receptor: {cfg.receptor_pdb} exists={cfg.receptor_pdb.is_file()}")
    print(f"dock_dir: {cfg.dock_dir}")
    print(
        f"TM3 CA range (UniProt/5TGZ): {cfg.tm3[0]}-{cfg.tm3[1]} "
        "(GPCRdb S3.21-R3.56)"
    )
    print(
        f"TM6 CA range (UniProt/5TGZ): {cfg.tm6[0]}-{cfg.tm6[1]} "
        "(GPCRdb P6.24-G6.61)"
    )
    print(f"strip flavodoxin fusion: {cfg.strip_fusion} keep={cfg.keep_residue_ranges}")
    print(
        f"protocol: min {cfg.minimize_max_iter} | equil {cfg.equil_ps} ps NVT/NPT | "
        f"prod {cfg.production_ns} ns | TIP3P + {cfg.salt_molar} M NaCl | seed={cfg.seed}"
    )
    problems = validate_inputs(cfg, ligand_ids)
    for lid in ligand_ids:
        p = pose_pdbqt_path(cfg.dock_dir, lid)
        print(f"  pose {lid}: {p} exists={p.is_file()}")
        if p.is_file():
            try:
                block = extract_model1_pdbqt(p)
                nat = sum(1 for ln in block.splitlines() if ln.startswith("ATOM"))
                print(f"    MODEL1 atoms (no REMARKs kept): {nat}")
            except Exception as exc:  # noqa: BLE001
                problems.append(f"{lid}: {exc}")
    deps = probe_deps()
    print("deps:", json.dumps({k: v for k, v in deps.items() if k != "errors"}, indent=2))
    if deps["errors"]:
        print("dep notes:")
        for e in deps["errors"]:
            print(f"  - {e}")
    cfg.out_dir.mkdir(parents=True, exist_ok=True)
    if problems:
        print("INPUT PROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        write_stub_metrics(
            cfg.metrics_csv,
            ligand_ids,
            cfg,
            note="dry-run failed input validation",
        )
        return 2
    if not deps["gaff_ready"]:
        print("\n" + gaff_install_message())
        write_stub_metrics(
            cfg.metrics_csv,
            ligand_ids,
            cfg,
            note="dry-run OK inputs; GAFF2/OpenFF not available - MD blocked",
        )
        print(f"stub metrics: {cfg.metrics_csv}")
        return 0
    write_stub_metrics(
        cfg.metrics_csv,
        ligand_ids,
        cfg,
        note="dry-run OK; deps ready - re-run without --dry-run",
    )
    print(f"deps ready for GAFF2 MD. stub: {cfg.metrics_csv}")
    return 0


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="Validate inputs/deps only")
    ap.add_argument("--ns", type=float, default=None, help="Production length in ns (default 2)")
    ap.add_argument(
        "--ligand",
        action="append",
        dest="ligands",
        help="Ligand id (repeatable). Default: JANUS_H1_02c and delta9-THCV",
    )
    ap.add_argument("--receptor", type=Path, default=None)
    ap.add_argument("--dock-dir", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--metrics-csv", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=None, help="Optional YAML overrides (local)")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--platform", type=str, default=None, help="CUDA|OpenCL|CPU")
    ap.add_argument(
        "--ligand-sdf",
        type=Path,
        default=None,
        help="Optional pre-built SDF for a single --ligand (gitignored local)",
    )
    ap.add_argument(
        "--minimize-only",
        action="store_true",
        help="Stop after minimization (sets production/equil ~0 via ns=0 and equil skip)",
    )
    return ap.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    cfg = config_from_args(args)
    ligand_ids = args.ligands or list(LIGAND_IDS)

    if args.dry_run:
        return dry_run(cfg, ligand_ids)

    problems = validate_inputs(cfg, ligand_ids)
    if problems:
        print("INPUT PROBLEMS:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 2

    deps = probe_deps()
    if not deps["gaff_ready"]:
        print(gaff_install_message(), file=sys.stderr)
        write_stub_metrics(
            cfg.metrics_csv,
            ligand_ids,
            cfg,
            note="MD blocked: OpenFF/GAFF2 unavailable",
        )
        return 3

    if args.minimize_only:
        cfg.equil_ps = 0.0
        cfg.production_ns = 0.0

    rows: list[dict[str, Any]] = []
    for lid in ligand_ids:
        try:
            lig_sdf = args.ligand_sdf if (args.ligand_sdf and len(ligand_ids) == 1) else None
            if cfg.production_ns <= 0 and cfg.equil_ps <= 0:
                # minimize-only path: tiny equil/prod so reporters still flush
                cfg_min = replace(cfg, equil_ps=0.002, production_ns=0.002)
                m = build_and_run_complex(cfg_min, lid, ligand_sdf=lig_sdf)
            else:
                m = build_and_run_complex(cfg, lid, ligand_sdf=lig_sdf)
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
                    "solvent": "TIP3P cubic + NaCl 0.15 M (no membrane)",
                    "note": str(exc),
                }
            )

    write_aggregate_csv(cfg.metrics_csv, rows)
    print(f"Wrote {cfg.metrics_csv}")
    return 0 if all(r.get("status") == "ok" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
