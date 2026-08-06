"""3D ligand preparation for the quimioma panel (RDKit + optional dimorphite-dl)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from meeko import MoleculePreparation, PDBQTWriterLegacy

PROTONATION_NOTE = (
    "Protonación pH 7.4: dimorphite-dl solo si hay ácido carboxílico "
    "(p. ej. THCVA → carboxilato); fenoles se mantienen neutros (pKa ~10, "
    "dimorphite a veces genera fenolato espurio). Si falla dimorphite, SMILES curado + AddHs."
)

_CARBOXYLIC = Chem.MolFromSmarts("C(=O)[OH]")


def _has_carboxylic_acid(smiles: str) -> bool:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None or _CARBOXYLIC is None:
        return False
    return mol.HasSubstructMatch(_CARBOXYLIC)


def protonate_smiles_ph(smiles: str, ph: float = 7.4) -> tuple[str, str]:
    """Return (protonated_smiles, method_tag).

    Fenoles/resorcinales del quimioma se dejan neutros a pH 7.4.
    Solo se enumera dimorphite cuando hay COOH (estados aniónicos relevantes).
    """
    if not _has_carboxylic_acid(smiles):
        return smiles, "rdkit_neutral_phenol_ok_ph7.4"

    try:
        from dimorphite_dl import protonate_smiles
    except ImportError:
        return smiles, "rdkit_default_no_dimorphite"

    try:
        variants = protonate_smiles(smiles, ph_min=ph, ph_max=ph, max_variants=8)
        if not variants:
            return smiles, "rdkit_default_dimorphite_empty"
        # Prefer charged carboxylate if present among variants
        for v in variants:
            m = Chem.MolFromSmiles(v)
            if m is not None and any(a.GetFormalCharge() < 0 for a in m.GetAtoms()):
                return v, "dimorphite_dl_ph7.4_carboxylate"
        return variants[0], "dimorphite_dl_ph7.4"
    except Exception as exc:  # noqa: BLE001 — keep panel runnable
        return smiles, f"rdkit_default_dimorphite_error:{type(exc).__name__}"


def load_panel_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"name", "smiles", "role"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Panel CSV missing columns: {sorted(missing)}")
    return df


def _largest_fragment(mol: Chem.Mol) -> Chem.Mol:
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    if not frags:
        return mol
    return max(frags, key=lambda m: m.GetNumHeavyAtoms())


def prepare_ligand_3d(
    smiles: str,
    name: str,
    out_sdf: Path | None = None,
    seed: int = 0xF00D,
    ph: float = 7.4,
) -> tuple[Chem.Mol, str, str]:
    """Embed + MMFF optimize. Returns (mol_with_hs, smiles_used, protonation_method)."""
    smiles_used, method = protonate_smiles_ph(smiles, ph=ph)
    mol = Chem.MolFromSmiles(smiles_used)
    if mol is None:
        mol = Chem.MolFromSmiles(smiles)
        smiles_used, method = smiles, "rdkit_default_parse_fallback"
    if mol is None:
        raise ValueError(f"Invalid SMILES for {name}: {smiles}")

    mol = _largest_fragment(mol)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    if AllChem.EmbedMolecule(mol, params) != 0:
        if AllChem.EmbedMolecule(mol, randomSeed=seed) != 0:
            raise RuntimeError(f"Could not embed 3D coords for {name}")
    try:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
    except Exception:  # noqa: BLE001
        AllChem.UFFOptimizeMolecule(mol, maxIters=200)

    mol.SetProp("_Name", name)
    mol.SetProp("smiles_input", smiles)
    mol.SetProp("smiles_docked", smiles_used)
    mol.SetProp("protonation", method)

    if out_sdf is not None:
        out_sdf.parent.mkdir(parents=True, exist_ok=True)
        with SDWriter(str(out_sdf)) as w:
            w.write(mol)
    return mol, smiles_used, method


def smiles_to_pdbqt(
    smiles: str,
    out_path: Path,
    name: str = "ligand",
    seed: int = 0xF00D,
    ph: float = 7.4,
    sdf_path: Path | None = None,
) -> dict:
    """Prepare ligand PDBQT via RDKit 3D + Meeko. Returns metadata dict."""
    mol, smiles_used, method = prepare_ligand_3d(
        smiles, name=name, out_sdf=sdf_path, seed=seed, ph=ph
    )
    preparator = MoleculePreparation()
    setups = preparator.prepare(mol)
    if not setups:
        raise RuntimeError(f"Meeko failed to prepare ligand: {name}")
    pdbqt, ok, err = PDBQTWriterLegacy.write_string(setups[0])
    if not ok and not pdbqt:
        raise RuntimeError(f"Meeko PDBQT write failed for {name}: {err}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(pdbqt, encoding="utf-8")
    return {
        "name": name,
        "smiles_input": smiles,
        "smiles_docked": smiles_used,
        "protonation": method,
        "pdbqt": str(out_path),
        "sdf": str(sdf_path) if sdf_path else None,
    }
