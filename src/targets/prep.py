"""Prepare CB1/CB2 receptors, reference ligands, and Vina grid boxes."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from rdkit import Chem
from meeko import MoleculePreparation, PDBQTWriterLegacy

from src.screening.receptors import (
    clean_protein_pdb,
    download_pdb,
    find_ligand_group,
    centroid,
    prepare_receptor_pdbqt,
    write_ligand_pdb,
)


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class TargetSpec:
    key: str
    pdb_id: str
    out_subdir: str
    receptor_filename: str
    ligand_resname: str | None
    ref_ligand_filename: str | None
    chains: list[str] | None
    grid_config: str
    box_size: float = 20.0


@dataclass(frozen=True)
class RefLigandSpec:
    key: str
    pdb_id: str
    out_subdir: str
    ligand_resname: str
    ref_ligand_filename: str
    chains: list[str] | None = None


TARGET_SPECS: tuple[TargetSpec, ...] = (
    TargetSpec(
        key="cb1_5tgz",
        pdb_id="5TGZ",
        out_subdir="cb1",
        receptor_filename="cb1_5tgz_clean.pdbqt",
        ligand_resname="ZDG",
        ref_ligand_filename="am6538_ref.pdbqt",
        chains=["A"],
        grid_config="grid_cb1_5tgz.txt",
    ),
    TargetSpec(
        key="cb2_6pt0",
        pdb_id="6PT0",
        out_subdir="cb2",
        receptor_filename="cb2_6pt0_clean.pdbqt",
        ligand_resname="WI5",
        ref_ligand_filename="win55212_ref.pdbqt",
        chains=["R"],
        grid_config="grid_cb2_6pt0.txt",
    ),
    TargetSpec(
        key="cb2_6kpc",
        pdb_id="6KPC",
        out_subdir="cb2",
        receptor_filename="cb2_6kpc_clean.pdbqt",
        ligand_resname="E3R",
        ref_ligand_filename=None,
        chains=["A"],
        grid_config="grid_cb2_6kpc.txt",
    ),
)

REF_LIGAND_SPECS: tuple[RefLigandSpec, ...] = (
    RefLigandSpec(
        key="apd371",
        pdb_id="8GUQ",
        out_subdir="cb2",
        ligand_resname="KNF",
        ref_ligand_filename="apd371_ref.pdbqt",
        chains=["R"],
    ),
)


def pdb_ligand_to_pdbqt(ligand_pdb: Path, out_pdbqt: Path) -> Path:
    """Convert crystal ligand PDB → PDBQT (explicit H, pH 7.4 via Meeko)."""
    mol = Chem.MolFromPDBFile(str(ligand_pdb), removeHs=False, sanitize=False)
    if mol is None:
        raise RuntimeError(f"No se pudo leer ligando PDB: {ligand_pdb}")
    Chem.SanitizeMol(mol)
    mol = Chem.AddHs(mol, addCoords=True)
    preparator = MoleculePreparation()
    setups = preparator.prepare(mol)
    if not setups:
        raise RuntimeError(f"Meeko no preparó ligando: {ligand_pdb}")
    pdbqt, ok, err = PDBQTWriterLegacy.write_string(setups[0])
    if not ok and not pdbqt:
        raise RuntimeError(f"Meeko PDBQT falló para {ligand_pdb}: {err}")
    out_pdbqt.parent.mkdir(parents=True, exist_ok=True)
    out_pdbqt.write_text(pdbqt, encoding="utf-8")
    return out_pdbqt


def write_vina_grid_txt(box: dict, path: Path) -> Path:
    """Write AutoDock Vina grid parameter file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f"center_x = {box['center_x']:.3f}\n"
        f"center_y = {box['center_y']:.3f}\n"
        f"center_z = {box['center_z']:.3f}\n"
        f"size_x = {box['size_x']:.3f}\n"
        f"size_y = {box['size_y']:.3f}\n"
        f"size_z = {box['size_z']:.3f}\n"
    )
    path.write_text(text, encoding="utf-8")
    return path


def prepare_target_spec(spec: TargetSpec, root: Path = ROOT) -> dict:
    """Download, clean, parametrize receptor; extract co-ligand; write aliases."""
    out_dir = root / "data" / "targets" / spec.out_subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    box_size = (spec.box_size, spec.box_size, spec.box_size)

    raw = download_pdb(spec.pdb_id, out_dir / f"{spec.pdb_id.upper()}.pdb")
    text = raw.read_text(encoding="utf-8", errors="replace")

    resname, chain, resseq, coords = find_ligand_group(text, spec.ligand_resname)
    cx, cy, cz = centroid(coords)
    lig_pdb = write_ligand_pdb(
        text,
        resname,
        chain,
        resseq,
        out_dir / f"{spec.pdb_id.upper()}_ligand.pdb",
    )
    clean_pdb = clean_protein_pdb(
        text,
        out_dir / f"{spec.pdb_id.upper()}_clean.pdb",
        chains=spec.chains,
    )

    rec_basename = out_dir / f"{spec.pdb_id.upper()}_rec"
    rec_pdbqt = prepare_receptor_pdbqt(
        clean_pdb,
        rec_basename,
        box_center=(cx, cy, cz),
        box_size=box_size,
    )

    canonical_rec = out_dir / spec.receptor_filename
    shutil.copy2(rec_pdbqt, canonical_rec)

    ref_lig_pdbqt = None
    if spec.ref_ligand_filename:
        ref_lig_pdbqt = pdb_ligand_to_pdbqt(
            lig_pdb, out_dir / spec.ref_ligand_filename
        )

    box = {
        "center_x": round(cx, 3),
        "center_y": round(cy, 3),
        "center_z": round(cz, 3),
        "size_x": float(box_size[0]),
        "size_y": float(box_size[1]),
        "size_z": float(box_size[2]),
        "source": "co-crystallized_ligand_centroid",
        "ligand_resname": resname,
        "ligand_chain": chain,
        "ligand_resseq": resseq,
        "ligand_natoms": len(coords),
        "ligand_pdb": str(lig_pdb),
        "receptor_pdbqt": str(canonical_rec),
        "receptor_pdbqt_legacy": str(rec_pdbqt),
        "clean_pdb": str(clean_pdb),
        "pdb_id": spec.pdb_id.upper(),
        "chains_kept": spec.chains,
        "grid_config": f"configs/{spec.grid_config}",
    }
    (out_dir / f"{spec.key}_box.json").write_text(
        json.dumps(box, indent=2), encoding="utf-8"
    )
    return box


def prepare_ref_ligand_spec(spec: RefLigandSpec, root: Path = ROOT) -> dict:
    """Extract reference ligand from a separate PDB (e.g. APD371 from 8GUQ)."""
    out_dir = root / "data" / "targets" / spec.out_subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = download_pdb(spec.pdb_id, out_dir / f"{spec.pdb_id.upper()}.pdb")
    text = raw.read_text(encoding="utf-8", errors="replace")
    resname, chain, resseq, coords = find_ligand_group(text, spec.ligand_resname)
    lig_pdb = write_ligand_pdb(
        text,
        resname,
        chain,
        resseq,
        out_dir / f"{spec.pdb_id.upper()}_{spec.key}_ligand.pdb",
    )
    ref_pdbqt = pdb_ligand_to_pdbqt(
        lig_pdb, out_dir / spec.ref_ligand_filename
    )
    return {
        "pdb_id": spec.pdb_id.upper(),
        "ligand_resname": resname,
        "ligand_chain": chain,
        "ligand_resseq": resseq,
        "ligand_natoms": len(coords),
        "ligand_pdb": str(lig_pdb),
        "ref_ligand_pdbqt": str(ref_pdbqt),
        "note": "APD371/Olorinab extraído de 8GUQ (6KPC contiene agonista E3R, no APD371)",
    }


def write_grid_configs(results: dict, root: Path = ROOT) -> list[Path]:
    """Write configs/grid_*.txt from prep results."""
    written: list[Path] = []
    configs_dir = root / "configs"
    for _key, meta in results.items():
        if "grid_config" not in meta or "error" in meta:
            continue
        cfg_path = root / meta["grid_config"]
        box = {
            k: meta[k]
            for k in (
                "center_x",
                "center_y",
                "center_z",
                "size_x",
                "size_y",
                "size_z",
            )
        }
        write_vina_grid_txt(box, cfg_path)
        written.append(cfg_path)
    return written


def prepare_all_targets(root: Path = ROOT) -> dict:
    """Run full target prep pipeline; return summary dict."""
    results: dict = {}
    for spec in TARGET_SPECS:
        try:
            results[spec.key] = prepare_target_spec(spec, root=root)
        except Exception as exc:  # noqa: BLE001
            results[spec.key] = {"error": str(exc), "pdb_id": spec.pdb_id}

    ref_ligands: dict = {}
    for spec in REF_LIGAND_SPECS:
        try:
            ref_ligands[spec.key] = prepare_ref_ligand_spec(spec, root=root)
        except Exception as exc:  # noqa: BLE001
            ref_ligands[spec.key] = {"error": str(exc), "pdb_id": spec.pdb_id}

    summary = {
        "targets": results,
        "ref_ligands": ref_ligands,
        "box_size_A": TARGET_SPECS[0].box_size,
        "notes": {
            "6KPC_ligand": "E3R (agonista cristal); APD371 proviene de 8GUQ (KNF)",
            "6PT0_chains": "Solo cadena R (CNR2); Gi/Nb35 excluidos",
            "5TGZ_chains": "Cadena A (CNR1 chimera)",
        },
    }
    summary_path = root / "data" / "targets" / "target_prep_redock_manifest.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_grid_configs(results, root=root)
    return summary
