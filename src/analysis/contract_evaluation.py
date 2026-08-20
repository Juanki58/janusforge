"""THCV design contract v1.0 evaluation — geometric proxies only."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from rdkit import Chem
from rdkit.Chem import AllChem

from scripts.run_benchmark_gold_exam_a import _parse_receptor_sidechain_coords
from src.analysis.interaction_mapping import (
    CB1_TM3_RES,
    CB1_TM6_RES,
    _map_ref_to_docked,
    _min_dist_ligand_to_atoms,
    _parse_pdbqt_model,
    _parse_receptor_pdb,
    _receptor_atoms_for,
    _ref_coord,
    _vector_clearance,
)

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_YAML = ROOT / "configs/thcv_design_constraints.yaml"

ADAMANTYL_AMIDE_SMARTS = "C(=O)NC23CC4CC(CC(C4)C2)C3"
ADAMANTYL_METHYL_AMIDE_SMARTS = "C(=O)NCC23CC4CC(CC(C4)C2)C3"
MORPHOLINE_SMARTS = "N1CCOCC1"
PIPERAZINE_SMARTS = "N1CCN(C)CC1"
PYRAZOLE_C5_PHENYL_SMARTS = "c1ccccc1"


def load_contract(path: Path | None = None) -> dict[str, Any]:
    p = path or CONTRACT_YAML
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def _centroid(coords: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    arr = np.array(coords, dtype=float)
    c = arr.mean(axis=0)
    return float(c[0]), float(c[1]), float(c[2])


def _ligand_heavy_coords(docked: Path) -> list[tuple[float, float, float]]:
    return [a.coord for a in _parse_pdbqt_model(docked) if not a.is_h]


def _match_first(mol: Chem.Mol, smarts: str) -> tuple[int, ...] | None:
    q = Chem.MolFromSmarts(smarts)
    if q is None:
        return None
    hits = mol.GetSubstructMatches(q)
    return hits[0] if hits else None


def _walk_linear_alkyl_chain(mol: Chem.Mol, start_idx: int, prev_idx: int) -> list[int]:
    chain = [start_idx]
    current = start_idx
    prev = prev_idx
    while True:
        next_c = [
            nbr.GetIdx()
            for nbr in mol.GetAtomWithIdx(current).GetNeighbors()
            if nbr.GetIdx() != prev
            and nbr.GetSymbol() == "C"
            and not nbr.GetIsAromatic()
            and not nbr.IsInRing()
        ]
        if len(next_c) != 1:
            break
        nxt = next_c[0]
        if nxt in chain:
            break
        chain.append(nxt)
        prev, current = current, nxt
    return chain


def _resorcinol_ring_atoms(mol: Chem.Mol) -> list[int]:
    phenol_rings: list[list[int]] = []
    ri = mol.GetRingInfo()
    for ring in ri.AtomRings():
        ring_set = set(ring)
        oxy_on_ring = [
            a
            for a in ring
            if mol.GetAtomWithIdx(a).GetSymbol() == "O"
            and any(n.GetIdx() in ring_set for n in mol.GetAtomWithIdx(a).GetNeighbors())
        ]
        if oxy_on_ring:
            phenol_rings.append(list(ring))
    if not phenol_rings:
        return [a.GetIdx() for a in mol.GetAtoms() if a.GetIsAromatic()]
    best = max(phenol_rings, key=len)
    return [a for a in best if mol.GetAtomWithIdx(a).GetSymbol() == "C"]


def cannabinoid_feature_indices(smiles: str) -> dict[str, Any]:
    """Map phytocannabinoid atoms for contract v1.0 proxies (THCV cross-scaffold)."""
    mol = Chem.RemoveHs(Chem.MolFromSmiles(smiles))
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())

    best_anchor: int | None = None
    best_term: int | None = None
    best_len = -1
    for atom in mol.GetAtoms():
        if not atom.GetIsAromatic():
            continue
        for nbr in atom.GetNeighbors():
            if nbr.GetSymbol() != "C" or nbr.GetIsAromatic() or nbr.IsInRing():
                continue
            chain = _walk_linear_alkyl_chain(mol, nbr.GetIdx(), atom.GetIdx())
            if len(chain) > best_len:
                best_len = len(chain)
                best_anchor = atom.GetIdx()
                best_term = chain[-1]

    if best_anchor is None or best_term is None:
        raise ValueError("No C3 alkyl chain matched on phytocannabinoid scaffold")

    polar_idx: int | None = None
    for smarts in ("[CX3]=[CX3][CH3]", "OC(C)(C)", "[OX2H][c]"):
        match = _match_first(mol, smarts)
        if match:
            if smarts == "[CX3]=[CX3][CH3]":
                polar_idx = match[2]
            elif smarts == "OC(C)(C)":
                polar_idx = match[2]
            else:
                polar_idx = match[0]
            break

    ring_atoms = _resorcinol_ring_atoms(mol)
    return {
        "c3_anchor": best_anchor,
        "c3_term": best_term,
        "c9_polar": polar_idx,
        "c5_phenyl_atoms": ring_atoms,
        "amide_n": None,
    }


def qiu_feature_indices(smiles: str) -> dict[str, Any]:
    """Map Qiu scaffold atoms for contract proxies (0D-verified SMILES only)."""
    mol = Chem.RemoveHs(Chem.MolFromSmiles(smiles))
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())

    ad_match = _match_first(mol, ADAMANTYL_AMIDE_SMARTS)
    methyl_link = False
    if ad_match is None:
        ad_match = _match_first(mol, ADAMANTYL_METHYL_AMIDE_SMARTS)
        methyl_link = ad_match is not None
    if ad_match is None:
        raise ValueError("No adamantyl amide substructure matched")

    carbonyl_c = ad_match[0]
    amide_n = ad_match[2]
    ad_start = 4 if methyl_link else 3
    ad_atoms = [ad_match[i] for i in range(ad_start, len(ad_match))]

    ad_coords = [mol.GetConformer().GetAtomPosition(i) for i in ad_atoms]
    n_coord = mol.GetConformer().GetAtomPosition(amide_n)
    dists = [float(np.linalg.norm(np.array(c) - np.array(n_coord))) for c in ad_coords]
    c3_term = ad_atoms[int(np.argmax(dists))]

    morph = _match_first(mol, MORPHOLINE_SMARTS)
    pip = _match_first(mol, PIPERAZINE_SMARTS)
    polar_idx: int | None = None
    if morph:
        mol_q = Chem.MolFromSmarts(MORPHOLINE_SMARTS)
        o_local = [a.GetIdx() for a in mol_q.GetAtoms() if a.GetSymbol() == "O"][0]
        polar_idx = morph[o_local]
    elif pip:
        polar_idx = pip[0]

    phenyl_matches = mol.GetSubstructMatches(Chem.MolFromSmarts(PYRAZOLE_C5_PHENYL_SMARTS))
    c5_phenyl_atoms = list(phenyl_matches[-1]) if phenyl_matches else []

    return {
        "c3_anchor": carbonyl_c,
        "c3_term": c3_term,
        "c9_polar": polar_idx,
        "c5_phenyl_atoms": c5_phenyl_atoms,
        "amide_n": amide_n,
    }


def _tm_shell_atoms(pdb_atoms: list, tm3: bool = True, tm6: bool = True) -> list:
    atoms = []
    if tm3:
        for resseq, resname, ats in CB1_TM3_RES:
            atoms.extend(_receptor_atoms_for(pdb_atoms, resseq, resname, ats))
    if tm6:
        for resseq, resname, ats in CB1_TM6_RES:
            atoms.extend(_receptor_atoms_for(pdb_atoms, resseq, resname, ats))
    return atoms


def _cb2_tunnel_atoms(pdb_atoms: list, contract: dict) -> list:
    atoms = []
    for rec in contract.get("cb2_tunnel_residues", []):
        atoms.extend(
            _receptor_atoms_for(
                pdb_atoms,
                rec["resseq"],
                rec["resname"],
                tuple(rec["atoms"]),
            )
        )
    return atoms


def _feature_indices(smiles: str, scaffold: str) -> dict[str, Any]:
    if scaffold == "cannabinoid":
        return cannabinoid_feature_indices(smiles)
    return qiu_feature_indices(smiles)


def evaluate_cb1(
    smiles: str,
    docked_pdbqt: Path,
    receptor_pdb: Path,
    contract: dict | None = None,
    scaffold: str = "qiu",
) -> dict[str, Any]:
    contract = contract or load_contract()
    th = contract["cb1_filter"]
    ref, perm, coords, map_err = _map_ref_to_docked(smiles, docked_pdbqt)
    feats = _feature_indices(smiles, scaffold)
    pdb_atoms = _parse_receptor_pdb(receptor_pdb)
    lig_coords = _ligand_heavy_coords(docked_pdbqt)
    tm_shell = _tm_shell_atoms(pdb_atoms)

    c3_anchor = _ref_coord(coords, perm, feats["c3_anchor"])
    c3_term = _ref_coord(coords, perm, feats["c3_term"])
    c3_vec = np.array(c3_term) - np.array(c3_anchor)

    c3_clear = _vector_clearance(c3_term, c3_vec, lig_coords, pdb_atoms, extension_max_A=10.0)

    c9_clear: dict[str, float] | None = None
    volume_delta: float | None = None
    if feats["c9_polar"] is not None:
        polar = _ref_coord(coords, perm, feats["c9_polar"])
        ring_cent = np.mean(
            [_ref_coord(coords, perm, i) for i in feats["c5_phenyl_atoms"][:4]],
            axis=0,
        )
        c9_vec = np.array(polar) - ring_cent
        c9_clear = _vector_clearance(polar, c9_vec, lig_coords, pdb_atoms, extension_max_A=8.0)
        volume_delta = round(
            abs(
                c9_clear["free_extension_before_3.0A_clash_A"]
                - c3_clear["free_extension_before_3.0A_clash_A"]
            ),
            2,
        )
    elif feats["c5_phenyl_atoms"]:
        ring_cent = np.mean(
            [_ref_coord(coords, perm, i) for i in feats["c5_phenyl_atoms"]],
            axis=0,
        )
        c9_vec = np.array(c3_term) - ring_cent
        c9_clear = _vector_clearance(
            tuple(ring_cent), c9_vec, lig_coords, pdb_atoms, extension_max_A=8.0
        )
        volume_delta = round(
            abs(
                c9_clear["free_extension_before_3.0A_clash_A"]
                - c3_clear["free_extension_before_3.0A_clash_A"]
            ),
            2,
        )

    min_tm, _, _ = _min_dist_ligand_to_atoms(lig_coords, tm_shell)

    c3_pass = c3_clear["free_extension_before_3.0A_clash_A"] >= th["c3_clearance_min_A"]
    vol_pass = volume_delta is not None and volume_delta <= th["c9_c11_volume_delta_max_A"]
    clash_pass = min_tm >= th["clash_min_heavy_distance_A"]
    aggregate = c3_pass and vol_pass and clash_pass

    return {
        "atom_map_error_A": round(map_err, 3),
        "c3_clearance_A": c3_clear["free_extension_before_3.0A_clash_A"],
        "c3_clearance_pass": c3_pass,
        "c9_c11_volume_delta_A": volume_delta,
        "c9_c11_volume_delta_pass": vol_pass,
        "min_tm_shell_distance_A": round(min_tm, 2),
        "clash_pass": clash_pass,
        "aggregate_pass": aggregate,
        "details": {"c3_vector_clearance": c3_clear, "c9_vector_clearance": c9_clear},
        "proxy_note": (
            "C3 = alkyl terminus vector; C9/C11 = polar/methyl extension clearance delta "
            "(interaction_mapping _vector_clearance)."
            if scaffold == "cannabinoid"
            else (
                "Qiu C3 = adamantyl amide vector; C9/C11 = morpholine/piperazine or "
                "phenyl extension clearance delta (interaction_mapping _vector_clearance)."
            )
        ),
    }


def evaluate_cb2(
    smiles: str,
    docked_pdbqt: Path,
    receptor_pdb: Path,
    hu308_docked_pdbqt: Path | None,
    contract: dict | None = None,
    scaffold: str = "qiu",
) -> dict[str, Any]:
    contract = contract or load_contract()
    th = contract["cb2_filter"]
    _, perm, coords, map_err = _map_ref_to_docked(smiles, docked_pdbqt)
    feats = _feature_indices(smiles, scaffold)
    pdb_atoms = _parse_receptor_pdb(receptor_pdb)
    tunnel = _cb2_tunnel_atoms(pdb_atoms, contract)

    c3_term = _ref_coord(coords, perm, feats["c3_term"])
    min_tunnel, _, _ = _min_dist_ligand_to_atoms([c3_term], tunnel)
    c3_occ_pass = min_tunnel <= th["c3_occupancy_envelope_A"]

    ser285_sc = _parse_receptor_sidechain_coords(receptor_pdb, 285, "SER", ("OG", "CB"))
    lig_coords = _ligand_heavy_coords(docked_pdbqt)
    ser285_dist = min(
        math.sqrt(sum((a - b) ** 2 for a, b in zip(lc, sc)))
        for lc in lig_coords
        for sc in ser285_sc
    )
    ser285_pass = ser285_dist <= th["ser285_max_A"]

    centroid_sep: float | None = None
    persistence_pass = False
    if hu308_docked_pdbqt and hu308_docked_pdbqt.exists():
        hu_coords = _ligand_heavy_coords(hu308_docked_pdbqt)
        centroid_sep = round(
            float(np.linalg.norm(np.array(_centroid(lig_coords)) - np.array(_centroid(hu_coords)))),
            2,
        )
        persistence_pass = centroid_sep <= th["pose_persistence_centroid_max_A"]

    aggregate = c3_occ_pass and ser285_pass and persistence_pass

    return {
        "atom_map_error_A": round(map_err, 3),
        "c3_tunnel_min_distance_A": round(min_tunnel, 2),
        "c3_occupancy_pass": c3_occ_pass,
        "ser285_distance_A": round(ser285_dist, 2),
        "ser285_pass": ser285_pass,
        "hu308_centroid_separation_A": centroid_sep,
        "pose_persistence_pass": persistence_pass,
        "aggregate_pass": aggregate,
        "proxy_note": (
            "C3 occupancy = alkyl terminus distance to ILE110/ILE186/THR114 shell; "
            "persistence = ligand centroid vs HU-308 CB2 gold pose."
            if scaffold == "cannabinoid"
            else (
                "C3 occupancy = adamantyl terminus distance to ILE110/ILE186/THR114 shell; "
                "persistence = ligand centroid vs HU-308 CB2 gold pose."
            )
        ),
    }


def evaluate_admet(smiles: str, contract: dict | None = None) -> dict[str, Any]:
    from rdkit.Chem import Descriptors

    contract = contract or load_contract()
    th = contract["admet"]["tpsa_min_A2"]
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"tpsa_A2": None, "pass": False, "error": "invalid SMILES"}
    tpsa = round(float(Descriptors.TPSA(mol)), 2)
    return {"tpsa_A2": tpsa, "pass": tpsa >= th, "threshold_A2": th}


def decoupled_verdicts(result: dict[str, Any]) -> dict[str, str]:
    if result.get("blocker"):
        return {
            "structural_binding": "INDETERMINATE",
            "peripheral": "INDETERMINATE",
            "global_v1_0": "BLOCKED",
            "layer_diagnosis": result.get("blocker", "identity blocker"),
        }
    cb1_ok = bool(result.get("cb1_filter", {}).get("aggregate_pass"))
    cb2_ok = bool(result.get("cb2_filter", {}).get("aggregate_pass"))
    peripheral_ok = bool(result.get("admet", {}).get("pass"))
    structural_ok = cb1_ok and cb2_ok
    if structural_ok and peripheral_ok:
        layer_diag = "concomitant PASS (estructural + periférico)"
    elif structural_ok and not peripheral_ok:
        layer_diag = "desacoplamiento REAL: STRUCTURAL PASS / PERIPHERAL FAIL"
    elif not structural_ok and peripheral_ok:
        layer_diag = "desacoplamiento REAL: STRUCTURAL FAIL / PERIPHERAL PASS"
    else:
        layer_diag = "rechazo concomitante (estructural + periférico)"
    return {
        "structural_binding": "PASS" if structural_ok else "FAIL",
        "peripheral": "PASS" if peripheral_ok else "FAIL",
        "global_v1_0": "PASS" if structural_ok and peripheral_ok else "FAIL",
        "layer_diagnosis": layer_diag,
    }


def evaluate_compound(
    compound_id: str,
    smiles: str | None,
    cb1_docked: Path | None,
    cb2_docked: Path | None,
    cb1_receptor_pdb: Path,
    cb2_receptor_pdb: Path,
    hu308_cb2_docked: Path | None = None,
    contract: dict | None = None,
    scaffold: str = "qiu",
) -> dict[str, Any]:
    contract = contract or load_contract()
    out: dict[str, Any] = {"compound_id": compound_id, "smiles": smiles}

    if not smiles:
        out["blocker"] = "SMILES missing in quarantine/library — evaluation blocked"
        out["cb1_filter"] = {"aggregate_pass": False, "blocker": True}
        out["cb2_filter"] = {"aggregate_pass": False, "blocker": True}
        out["admet"] = {"pass": False, "blocker": True}
        out["contract_verdict"] = "FAIL"
        return out

    out["admet"] = evaluate_admet(smiles, contract)

    if cb1_docked and cb1_docked.exists():
        out["cb1_filter"] = evaluate_cb1(
            smiles, cb1_docked, cb1_receptor_pdb, contract, scaffold=scaffold
        )
    else:
        out["cb1_filter"] = {"aggregate_pass": False, "error": "missing CB1 pose"}

    if cb2_docked and cb2_docked.exists():
        out["cb2_filter"] = evaluate_cb2(
            smiles,
            cb2_docked,
            cb2_receptor_pdb,
            hu308_cb2_docked,
            contract,
            scaffold=scaffold,
        )
    else:
        out["cb2_filter"] = {"aggregate_pass": False, "error": "missing CB2 pose"}

    all_pass = (
        out["admet"].get("pass")
        and out["cb1_filter"].get("aggregate_pass")
        and out["cb2_filter"].get("aggregate_pass")
    )
    out["contract_verdict"] = "PASS" if all_pass else "FAIL"
    out.update(decoupled_verdicts(out))
    return out
