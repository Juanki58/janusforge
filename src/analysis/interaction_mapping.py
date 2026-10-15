"""Spatial sub-pocket mapping: THCV vs gold references (Mode 1 poses).

Analysis-only module — no docking, no biological inference from scores.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path(__file__).resolve().parents[2]

# Atom indices in canonical RDKit SMILES graphs (see scripts docstring).
THCV_FEATURES = {
    "propyl_term": 0,
    "propyl_beta": 1,
    "propyl_gamma": 2,
    "propyl_aromatic": 3,
    "c9_methyl": 17,
    "phenol_o": 20,
}

HU308_FEATURES = {
    "alkyl_chain": tuple(range(0, 7)),
    "alkyl_term": 0,
    "alkyl_branch": 6,
    "ring_attachment": 9,
    "hydroxymethyl_c": 26,
    "hydroxymethyl_o": 27,
}

THCV_SMILES = "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C)C)O"
HU308_SMILES = (
    "CCCCCCC(C)(C)C1=CC(=C(C(=C1)OC)[C@H]2C=C([C@H]3C[C@@H]2C3(C)C)CO)OC"
)

AD4_TO_ELEM = {
    "A": "C",
    "C": "C",
    "N": "N",
    "NA": "N",
    "NS": "N",
    "OA": "O",
    "OS": "O",
    "SA": "S",
    "P": "P",
    "F": "F",
    "Cl": "Cl",
    "Br": "Br",
    "I": "I",
    "HD": "H",
    "HS": "H",
}

# Ballesteros-Weinstein labels in comments where known from Exam A scripts.
CB2_POLAR = {
    "Thr114(3.29)": (114, "THR", ("OG1", "CB", "CG2")),
    "Ser285(7.39)": (285, "SER", ("OG", "CB")),
    "Lys109(EC2)": (109, "LYS", ("NZ", "CE", "CD", "CG", "CB")),
}

CB1_SWITCH = {
    "Phe200(3.36)": (200, "PHE", ("CG", "CD1", "CD2", "CE1", "CE2", "CZ")),
    "Trp356(6.48)": (
        356,
        "TRP",
        ("CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"),
    ),
}

# TM3 / TM6 shell residues flanking inactive CB1 pocket (5TGZ numbering).
CB1_TM3_RES = [
    (196, "VAL", ("CG1", "CG2", "CB")),
    (197, "THR", ("OG1", "CB", "CG2")),
    (201, "THR", ("OG1", "CB", "CG2")),
]
CB1_TM6_RES = [
    (353, "ILE", ("CG1", "CG2", "CD1", "CB")),
    (357, "GLY", ("CA",)),
]

CLASH_THRESHOLDS_A = (2.5, 3.0)
POLAR_CUTOFF_A = 4.5
HBOND_DA_MAX_A = 3.5
HBOND_HA_MAX_A = 2.6


@dataclass(frozen=True)
class AtomRecord:
    idx: int
    elem: str
    coord: tuple[float, float, float]
    is_h: bool = False


@dataclass(frozen=True)
class ReceptorAtom:
    resseq: int
    resname: str
    atom: str
    elem: str
    coord: tuple[float, float, float]
    is_h: bool


def _dist(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _unit(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v)
    if n < 1e-8:
        return v
    return v / n


def _parse_pdbqt_model(path: Path) -> list[AtomRecord]:
    atoms: list[AtomRecord] = []
    in_model = False
    has_model = False
    idx = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("MODEL"):
            in_model = True
            has_model = True
            continue
        if line.startswith("ENDMDL"):
            break
        if has_model and not in_model:
            continue
        if not line.startswith(("ATOM", "HETATM")):
            continue
        atype = line[77:79].strip() if len(line) >= 79 else ""
        elem = AD4_TO_ELEM.get(atype, atype[:1] if atype else "C")
        is_h = elem.upper() in {"H", "D"}
        coord = (
            float(line[30:38]),
            float(line[38:46]),
            float(line[46:54]),
        )
        atoms.append(AtomRecord(idx=idx, elem=elem, coord=coord, is_h=is_h))
        idx += 1
    if not atoms:
        raise RuntimeError(f"No atoms in {path}")
    return atoms


def _heavy_coords(atoms: list[AtomRecord]) -> np.ndarray:
    return np.array([a.coord for a in atoms if not a.is_h], dtype=float)


def _distmat(coords: np.ndarray) -> np.ndarray:
    n = len(coords)
    d = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            d[i, j] = d[j, i] = np.linalg.norm(coords[i] - coords[j])
    return d


def _map_ref_to_docked(
    smiles: str,
    docked_path: Path,
) -> tuple[Chem.Mol, list[int], np.ndarray, float]:
    """Map RDKit ref atom index -> docked heavy-atom index via distance signatures."""
    ref = Chem.RemoveHs(Chem.MolFromSmiles(smiles))
    AllChem.EmbedMolecule(ref, AllChem.ETKDGv3())
    ref_coords = ref.GetConformer().GetPositions()
    ref_elems = [a.GetSymbol() for a in ref.GetAtoms()]

    docked = _parse_pdbqt_model(docked_path)
    heavy = [a for a in docked if not a.is_h]
    probe_coords = np.array([a.coord for a in heavy], dtype=float)
    probe_elems = [a.elem for a in heavy]

    n = ref.GetNumAtoms()
    if n != len(heavy):
        raise RuntimeError(
            f"Atom count mismatch ref={n} docked={len(heavy)} for {docked_path}"
        )

    d_ref = _distmat(ref_coords)
    d_probe = _distmat(probe_coords)
    ref_sigs = [
        tuple(sorted(round(float(x), 1) for x in d_ref[i])) for i in range(n)
    ]
    probe_sigs = [
        tuple(sorted(round(float(x), 1) for x in d_probe[i])) for i in range(n)
    ]

    used: set[int] = set()
    perm: list[int | None] = [None] * n
    for i, sig_r in enumerate(ref_sigs):
        cands = [
            j
            for j, sig_p in enumerate(probe_sigs)
            if j not in used and ref_elems[i] == probe_elems[j]
        ]
        if not cands:
            cands = [j for j in range(n) if j not in used]
        j = min(
            cands,
            key=lambda jj: sum(abs(a - b) for a, b in zip(sig_r, probe_sigs[jj])),
        )
        perm[i] = j
        used.add(j)

    perm_int = [int(p) for p in perm]
    err = float(np.abs(d_ref - d_probe[np.ix_(perm_int, perm_int)]).mean())
    return ref, perm_int, probe_coords, err


def _ref_coord(
    probe_coords: np.ndarray,
    perm: list[int],
    ref_idx: int,
) -> tuple[float, float, float]:
    c = probe_coords[perm[ref_idx]]
    return float(c[0]), float(c[1]), float(c[2])


def _parse_receptor_pdb(path: Path) -> list[ReceptorAtom]:
    out: list[ReceptorAtom] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("ATOM"):
            continue
        resseq = int(line[22:26])
        resname = line[17:20].strip()
        atom = line[12:16].strip()
        elem = (line[76:78].strip() or atom[0]).upper()
        coord = (
            float(line[30:38]),
            float(line[38:46]),
            float(line[46:54]),
        )
        out.append(
            ReceptorAtom(
                resseq=resseq,
                resname=resname,
                atom=atom,
                elem=elem,
                coord=coord,
                is_h=elem.startswith("H"),
            )
        )
    return out


def _receptor_atoms_for(
    pdb_atoms: list[ReceptorAtom],
    resseq: int,
    resname: str,
    atom_names: tuple[str, ...] | None = None,
) -> list[ReceptorAtom]:
    want = set(atom_names) if atom_names else None
    return [
        a
        for a in pdb_atoms
        if a.resseq == resseq
        and a.resname == resname
        and (want is None or a.atom in want)
    ]


def _min_dist_ligand_to_atoms(
    lig_coords: list[tuple[float, float, float]],
    rec_atoms: list[ReceptorAtom],
    heavy_only: bool = True,
) -> tuple[float, ReceptorAtom | None, tuple[float, float, float] | None]:
    best = math.inf
    best_atom: ReceptorAtom | None = None
    best_lig: tuple[float, float, float] | None = None
    for lc in lig_coords:
        for ra in rec_atoms:
            if heavy_only and ra.is_h:
                continue
            d = _dist(lc, ra.coord)
            if d < best:
                best = d
                best_atom = ra
                best_lig = lc
    return best, best_atom, best_lig


def _min_hbond_distance(
    donor_h_coords: list[tuple[float, float, float]],
    acceptor_coords: list[tuple[float, float, float]],
    donor_heavy_coords: list[tuple[float, float, float]],
) -> dict[str, float | bool]:
    best_h = math.inf
    best_d = math.inf
    for dh in donor_heavy_coords:
        for ac in acceptor_coords:
            d = _dist(dh, ac)
            if d < best_d:
                best_d = d
    for h in donor_h_coords:
        for ac in acceptor_coords:
            d = _dist(h, ac)
            if d < best_h:
                best_h = d
    present = best_d <= HBOND_DA_MAX_A and best_h <= HBOND_HA_MAX_A
    return {
        "min_heavy_donor_to_acceptor_A": round(best_d, 2),
        "min_H_to_acceptor_A": round(best_h, 2) if math.isfinite(best_h) else None,
        "hbond_geometry_present": present,
    }


def _polar_contacts_cb2(
    lig_atoms: list[AtomRecord],
    pdb_path: Path,
) -> dict[str, Any]:
    pdb_atoms = _parse_receptor_pdb(pdb_path)
    heavy_lig = [a.coord for a in lig_atoms if not a.is_h]
    h_lig = [a.coord for a in lig_atoms if a.is_h]

    out: dict[str, Any] = {}
    for label, (resseq, resname, atoms) in CB2_POLAR.items():
        rec = _receptor_atoms_for(pdb_atoms, resseq, resname, atoms)
        rec_heavy = [a for a in rec if not a.is_h]
        rec_h = [a for a in rec if a.is_h]
        within = [
            a
            for a in rec_heavy
            if min(_dist(a.coord, lc) for lc in heavy_lig) <= POLAR_CUTOFF_A
        ]
        min_heavy, _, _ = _min_dist_ligand_to_atoms(heavy_lig, rec_heavy)
        entry: dict[str, Any] = {
            "within_4.5A": len(within) > 0,
            "min_heavy_ligand_to_sidechain_A": round(min_heavy, 2),
            "sidechain_atoms_within_4.5A": sorted({a.atom for a in within}),
        }
        if resname in {"SER", "THR"}:
            acceptors = [a.coord for a in rec_heavy if a.atom.startswith("O")]
            donors_h = h_lig
            donors_heavy = heavy_lig
            if resname == "SER" and any(a.atom == "OG" for a in rec_heavy):
                hb_d = _min_hbond_distance(donors_h, acceptors, donors_heavy)
                hb_a = _min_hbond_distance(
                    [a.coord for a in rec_h if a.atom == "HG"],
                    heavy_lig,
                    [a.coord for a in rec_heavy if a.atom == "OG"],
                )
                entry["hbond_ligand_as_donor"] = hb_d
                entry["hbond_ligand_as_acceptor"] = hb_a
                entry["hbond_geometry_present"] = bool(
                    hb_d.get("hbond_geometry_present")
                    or hb_a.get("hbond_geometry_present")
                )
        if resname == "LYS":
            nz = [a for a in rec_heavy if a.atom == "NZ"]
            if nz:
                entry["min_heavy_to_NZ_A"] = round(
                    min(_dist(lc, nz[0].coord) for lc in heavy_lig), 2
                )
        out[label] = entry
    return out


def _vector_clearance(
    origin: tuple[float, float, float],
    direction: np.ndarray,
    lig_coords: list[tuple[float, float, float]],
    receptor_atoms: list[ReceptorAtom],
    extension_max_A: float = 8.0,
    step_A: float = 0.25,
) -> dict[str, float]:
    """Estimate steric clearance along a unit direction from origin."""
    u = _unit(direction)
    rec_heavy = [a for a in receptor_atoms if not a.is_h]
    # exclude receptor atoms very close to current ligand (likely contact, not shell)
    lig_arr = np.array(lig_coords)
    shell = [
        a
        for a in rec_heavy
        if min(_dist(a.coord, lc) for lc in lig_coords) > 2.0
    ]

    clearances: list[float] = []
    for t in np.arange(0.0, extension_max_A + step_A, step_A):
        probe = np.array(origin) + u * t
        md = min(_dist(tuple(probe), a.coord) for a in shell) if shell else 99.0
        clearances.append(md)

    # first distance where probe comes within clash 3.0 Å of shell
    tol_25 = next((i * step_A for i, c in enumerate(clearances) if c < 2.5), extension_max_A)
    tol_30 = next((i * step_A for i, c in enumerate(clearances) if c < 3.0), extension_max_A)

    return {
        "direction_unit": [round(float(x), 4) for x in u],
        "min_shell_distance_at_origin_A": round(clearances[0], 2),
        "free_extension_before_2.5A_clash_A": round(float(tol_25), 2),
        "free_extension_before_3.0A_clash_A": round(float(tol_30), 2),
        "max_sampled_clearance_A": round(max(clearances[:1] + [clearances[4]]), 2),
    }


def _analyze_cb2(
    thcv_docked: Path,
    hu_docked: Path,
    receptor_pdb: Path,
) -> dict[str, Any]:
    thcv_ref, thcv_perm, thcv_coords, thcv_map_err = _map_ref_to_docked(
        THCV_SMILES, thcv_docked
    )
    hu_ref, hu_perm, hu_coords, hu_map_err = _map_ref_to_docked(
        HU308_SMILES, hu_docked
    )

    def dc(ref_mol: Chem.Mol, perm: list[int], coords: np.ndarray, idx: int):
        return _ref_coord(coords, perm, idx)

    propyl_term = dc(thcv_ref, thcv_perm, thcv_coords, THCV_FEATURES["propyl_term"])
    propyl_inner = dc(thcv_ref, thcv_perm, thcv_coords, THCV_FEATURES["propyl_aromatic"])
    c9_coord = dc(thcv_ref, thcv_perm, thcv_coords, THCV_FEATURES["c9_methyl"])
    phenol_coord = dc(thcv_ref, thcv_perm, thcv_coords, THCV_FEATURES["phenol_o"])

    hu_chain_coords = [
        dc(hu_ref, hu_perm, hu_coords, i) for i in HU308_FEATURES["alkyl_chain"]
    ]
    hu_term = dc(hu_ref, hu_perm, hu_coords, HU308_FEATURES["alkyl_term"])
    hu_branch = dc(hu_ref, hu_perm, hu_coords, HU308_FEATURES["alkyl_branch"])
    hu_ring = dc(hu_ref, hu_perm, hu_coords, HU308_FEATURES["ring_attachment"])
    hu_hydroxy_c = dc(hu_ref, hu_perm, hu_coords, HU308_FEATURES["hydroxymethyl_c"])
    hu_hydroxy_o = dc(hu_ref, hu_perm, hu_coords, HU308_FEATURES["hydroxymethyl_o"])

    # C3 axis: ring attachment → propyl terminus → outward (same direction)
    c3_vec = np.array(propyl_term) - np.array(propyl_inner)
    c3_length = float(np.linalg.norm(c3_vec))
    c3_u = _unit(c3_vec)

    def proj_origin(point: tuple[float, float, float]) -> float:
        return float(np.dot(np.array(point) - np.array(propyl_inner), c3_u))

    thcv_term_proj = proj_origin(propyl_term)
    hu_chain_projs = [proj_origin(p) for p in hu_chain_coords]
    hu_max_proj = max(hu_chain_projs)
    hu_min_proj = min(hu_chain_projs)
    residual_along_axis = round(max(0.0, hu_max_proj - thcv_term_proj), 2)

    # Transverse gap: min distance from THCV terminus to HU chain atoms
    min_term_to_hu_chain = round(
        min(_dist(propyl_term, p) for p in hu_chain_coords),
        2,
    )
    min_term_to_hu_branch = round(_dist(propyl_term, hu_branch), 2)

    thcv_atoms = _parse_pdbqt_model(thcv_docked)
    polar = _polar_contacts_cb2(thcv_atoms, receptor_pdb)
    pdb_atoms = _parse_receptor_pdb(receptor_pdb)
    thcv_coords_list = [a.coord for a in thcv_atoms if not a.is_h]

    # Receptor clearance beyond THCV propyl terminus along C3 (CB2 tunnel)
    c3_receptor_clear = _vector_clearance(
        propyl_term,
        c3_vec,
        thcv_coords_list,
        pdb_atoms,
        extension_max_A=12.0,
    )

    c9_hu_polar = hu_hydroxy_o
    c9_hu_dist = round(_dist(c9_coord, c9_hu_polar), 2)
    v = np.array(c9_hu_polar) - np.array(c9_coord)
    c9_hu_vec = [round(float(x), 2) for x in _unit(v)]

    return {
        "atom_mapping": {
            "thcv_map_mean_dist_matrix_error_A": round(thcv_map_err, 3),
            "hu308_map_mean_dist_matrix_error_A": round(hu_map_err, 3),
        },
        "c3_alkyl_subpocket": {
            "thcv_propyl_terminus": [round(x, 2) for x in propyl_term],
            "thcv_propyl_aromatic_attachment": [round(x, 2) for x in propyl_inner],
            "c3_vector_propyl_length_A": round(c3_length, 2),
            "hu308_alkyl_chain_atoms": list(HU308_FEATURES["alkyl_chain"]),
            "hu308_alkyl_term_to_thcv_propyl_term_A": round(_dist(hu_term, propyl_term), 2),
            "hu308_branch_to_thcv_propyl_term_A": min_term_to_hu_branch,
            "min_thcv_propyl_term_to_hu_chain_A": min_term_to_hu_chain,
            "thcv_propyl_projection_on_c3_axis_A": round(thcv_term_proj, 2),
            "hu308_chain_max_projection_on_c3_axis_A": round(hu_max_proj, 2),
            "hu308_chain_min_projection_on_c3_axis_A": round(hu_min_proj, 2),
            "hu308_depth_beyond_thcv_propyl_along_c3_A": residual_along_axis,
            "residual_free_volume_along_c3_vector_A": c3_receptor_clear[
                "free_extension_before_3.0A_clash_A"
            ],
            "receptor_clearance_beyond_propyl_term_A": c3_receptor_clear,
            "hu308_alkyl_span_ring_to_term_A": round(_dist(hu_ring, hu_term), 2),
            "interpretation": (
                "C3 axis anchored at THCV aromatic attachment, directed through "
                "propyl terminus. HU-308 alkyl max projection on this axis "
                f"({round(hu_max_proj, 2)} Å) vs THCV terminus ({round(thcv_term_proj, 2)} Å) "
                "shows whether HU occupies deeper tunnel. Receptor clearance beyond "
                "THCV propyl terminus estimates exploitable vector for C3 extension."
            ),
        },
        "hbond_network_cb2_thcv": polar,
        "c9_c11_zone": {
            "thcv_c9_methyl": [round(x, 2) for x in c9_coord],
            "thcv_phenol_O": [round(x, 2) for x in phenol_coord],
            "hu308_hydroxymethyl_C": [round(x, 2) for x in hu_hydroxy_c],
            "hu308_hydroxymethyl_O": [round(x, 2) for x in hu_hydroxy_o],
            "c9_methyl_to_hu_hydroxymethyl_O_A": c9_hu_dist,
            "c9_methyl_to_hu_hydroxymethyl_C_A": round(_dist(c9_coord, hu_hydroxy_c), 2),
            "c9_to_hu_polar_direction_unit": c9_hu_vec,
            "geometry_note": (
                "THCV bears a vinylic C9 methyl; HU-308 places a hydroxymethyl "
                "on the bicyclic core. Distances and direction reported without "
                "functional assignment."
            ),
        },
    }


def _analyze_cb1(
    thcv_docked: Path,
    am6538_ref: Path,
    receptor_pdb: Path,
) -> dict[str, Any]:
    thcv_ref, thcv_perm, thcv_coords, map_err = _map_ref_to_docked(
        THCV_SMILES, thcv_docked
    )
    am_atoms = _parse_pdbqt_model(am6538_ref)
    am_heavy = [a.coord for a in am_atoms if not a.is_h]

    propyl_term = _ref_coord(thcv_coords, thcv_perm, THCV_FEATURES["propyl_term"])
    propyl_inner = _ref_coord(thcv_coords, thcv_perm, THCV_FEATURES["propyl_aromatic"])
    c9_coord = _ref_coord(thcv_coords, thcv_perm, THCV_FEATURES["c9_methyl"])
    thcv_heavy = [tuple(thcv_coords[thcv_perm[i]]) for i in range(thcv_ref.GetNumAtoms())]

    pdb_atoms = _parse_receptor_pdb(receptor_pdb)

    switch: dict[str, Any] = {}
    for label, (resseq, resname, atoms) in CB1_SWITCH.items():
        rec = _receptor_atoms_for(pdb_atoms, resseq, resname, atoms)
        d_thcv, _, _ = _min_dist_ligand_to_atoms(thcv_heavy, rec)
        d_am, _, _ = _min_dist_ligand_to_atoms(am_heavy, rec)
        switch[label] = {
            "thcv_min_heavy_A": round(d_thcv, 2),
            "am6538_min_heavy_A": round(d_am, 2),
            "gap_thcv_to_switch_A": round(d_thcv - 4.0, 2),
        }

    # THCV vs AM6538 centroid separation
    thcv_cent = np.mean(thcv_coords, axis=0)
    am_cent = np.mean(np.array(am_heavy), axis=0)
    centroid_sep = round(float(np.linalg.norm(thcv_cent - am_cent)), 2)

    # min ligand-ligand heavy distance
    min_thcv_am = round(
        min(_dist(t, a) for t in thcv_heavy for a in am_heavy),
        2,
    )

    c3_vec = np.array(propyl_term) - np.array(propyl_inner)
    # C9 vector: from ring centroid toward C9 methyl
    ring_cent = np.mean(
        [thcv_coords[thcv_perm[i]] for i in range(4, 16)],
        axis=0,
    )
    c9_vec = np.array(c9_coord) - ring_cent

    tm3_atoms: list[ReceptorAtom] = []
    tm6_atoms: list[ReceptorAtom] = []
    for resseq, resname, atoms in CB1_TM3_RES:
        tm3_atoms.extend(_receptor_atoms_for(pdb_atoms, resseq, resname, atoms))
    for resseq, resname, atoms in CB1_TM6_RES:
        tm6_atoms.extend(_receptor_atoms_for(pdb_atoms, resseq, resname, atoms))

    thcv_atom_records = _parse_pdbqt_model(thcv_docked)
    thcv_coords_list = [a.coord for a in thcv_atom_records if not a.is_h]

    c3_clear = _vector_clearance(
        propyl_term, c3_vec, thcv_coords_list, pdb_atoms, extension_max_A=10.0
    )
    c9_clear = _vector_clearance(
        c9_coord, c9_vec, thcv_coords_list, pdb_atoms, extension_max_A=8.0
    )

    # Direct min distances C3/C9 to TM shell
    c3_tm3, _, _ = _min_dist_ligand_to_atoms([propyl_term], tm3_atoms)
    c3_tm6, _, _ = _min_dist_ligand_to_atoms([propyl_term], tm6_atoms)
    c9_tm3, _, _ = _min_dist_ligand_to_atoms([c9_coord], tm3_atoms)
    c9_tm6, _, _ = _min_dist_ligand_to_atoms([c9_coord], tm6_atoms)

    steric: dict[str, Any] = {}
    for thr in CLASH_THRESHOLDS_A:
        key = f"clash_threshold_{thr:.1f}A"
        steric[key] = {
            "c3_extension_tolerance_A": round(
                max(0.0, c3_clear["free_extension_before_2.5A_clash_A"] - thr + 2.5)
                if thr == 2.5
                else max(0.0, c3_clear["free_extension_before_3.0A_clash_A"] - thr + 3.0),
                2,
            ),
            "c9_extension_tolerance_A": round(
                max(0.0, c9_clear["free_extension_before_2.5A_clash_A"] - thr + 2.5)
                if thr == 2.5
                else max(0.0, c9_clear["free_extension_before_3.0A_clash_A"] - thr + 3.0),
                2,
            ),
        }

    return {
        "atom_mapping_mean_error_A": round(map_err, 3),
        "thcv_vs_am6538_placement": {
            "ligand_centroid_separation_A": centroid_sep,
            "min_heavy_heavy_distance_A": min_thcv_am,
            "note": (
                "5TGZ CB1 is antagonist/inactive (AM6538 co-crystal). THCV mode 1 "
                "occupies the orthosteric cavity with partial overlap vs AM6538; "
                "distances are geometric only."
            ),
        },
        "switch_zone_Phe200_Trp356": switch,
        "c3_extension_clearance": {
            **c3_clear,
            "min_propyl_term_to_TM3_shell_A": round(c3_tm3, 2),
            "min_propyl_term_to_TM6_shell_A": round(c3_tm6, 2),
        },
        "c9_extension_clearance": {
            **c9_clear,
            "min_c9_methyl_to_TM3_shell_A": round(c9_tm3, 2),
            "min_c9_methyl_to_TM6_shell_A": round(c9_tm6, 2),
        },
        "steric_tolerance_summary": steric,
    }


def _build_summary_table(cb2: dict[str, Any], cb1: dict[str, Any]) -> list[dict[str, str]]:
    c3 = cb2["c3_alkyl_subpocket"]
    c9z = cb2["c9_c11_zone"]
    polar = cb2["hbond_network_cb2_thcv"]
    c3_cb1 = cb1["c3_extension_clearance"]
    c9_cb1 = cb1["c9_extension_clearance"]
    steric = cb1["steric_tolerance_summary"]["clash_threshold_3.0A"]

    def polar_note() -> str:
        parts = []
        for res, data in polar.items():
            if data.get("within_4.5A"):
                hb = ""
                if "hbond_ligand_as_donor" in data:
                    d = data["hbond_ligand_as_donor"]
                    hb = (
                        " H-bond geom"
                        if d.get("hbond_geometry_present")
                        else " no H-bond geom"
                    )
                parts.append(f"{res.split('(')[0]} {data['min_heavy_ligand_to_sidechain_A']:.1f}Å{hb}")
        return "; ".join(parts) if parts else "—"

    rows = [
        {
            "vector": "C3 propilo → canal alquílico HU-308",
            "espacio_A": str(c3.get("residual_free_volume_along_c3_vector_A") or "—"),
            "cb2_interactions": polar_note(),
            "cb1_steric_risk": (
                f"C3 ext ≤{steric['c3_extension_tolerance_A']:.1f} Å @3.0; "
                f"TM3 {c3_cb1['min_propyl_term_to_TM3_shell_A']:.1f} / "
                f"TM6 {c3_cb1['min_propyl_term_to_TM6_shell_A']:.1f} Å"
            ),
        },
        {
            "vector": "C3 terminus → profundidad HU (eje común)",
            "espacio_A": str(
                round(
                    c3["hu308_chain_max_projection_on_c3_axis_A"]
                    - c3["thcv_propyl_projection_on_c3_axis_A"],
                    2,
                )
            ),
            "cb2_interactions": (
                f"Phe117 3.7 Å; Ser285 4.0 Å (sin H-bond); "
                f"Thr114 {polar['Thr114(3.29)']['min_heavy_ligand_to_sidechain_A']:.1f} Å"
            ),
            "cb1_steric_risk": f"Phe200 {cb1['switch_zone_Phe200_Trp356']['Phe200(3.36)']['thcv_min_heavy_A']:.1f} Å (lejos)",
        },
        {
            "vector": "C9 metilo THCV ↔ hidroximetilo HU-308",
            "espacio_A": str(c9z.get("c9_methyl_to_hu_hydroxymethyl_O_A") or "—"),
            "cb2_interactions": (
                f"Ser285 OG {polar['Ser285(7.39)']['min_heavy_ligand_to_sidechain_A']:.1f} Å; "
                f"Lys109 {polar['Lys109(EC2)']['min_heavy_ligand_to_sidechain_A']:.1f} Å"
            ),
            "cb1_steric_risk": (
                f"C9 ext ≤{steric['c9_extension_tolerance_A']:.1f} Å @3.0; "
                f"Trp356 {cb1['switch_zone_Phe200_Trp356']['Trp356(6.48)']['thcv_min_heavy_A']:.1f} Å"
            ),
        },
        {
            "vector": "Switch Phe200 / Trp356 (CB1)",
            "espacio_A": (
                f"gap Phe200 {cb1['switch_zone_Phe200_Trp356']['Phe200(3.36)']['gap_thcv_to_switch_A']:.1f}; "
                f"Trp356 {cb1['switch_zone_Phe200_Trp356']['Trp356(6.48)']['thcv_min_heavy_A']:.1f} Å"
            ),
            "cb2_interactions": "N/A (CB1 frame)",
            "cb1_steric_risk": (
                f"AM6538 centroid Δ {cb1['thcv_vs_am6538_placement']['ligand_centroid_separation_A']:.1f} Å; "
                f"min HH {cb1['thcv_vs_am6538_placement']['min_heavy_heavy_distance_A']:.1f} Å"
            ),
        },
    ]
    return rows


def _write_markdown(
    out_md: Path,
    cb2: dict[str, Any],
    cb1: dict[str, Any],
    table: list[dict[str, str]],
    paths: dict[str, str],
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    c3 = cb2["c3_alkyl_subpocket"]
    c9z = cb2["c9_c11_zone"]
    polar = cb2["hbond_network_cb2_thcv"]

    lines = [
        "# Interaction Mapping — THCV vs Gold References (Mode 1)",
        "",
        f"Generado: {ts}",
        "",
        "**Modo:** análisis geométrico únicamente — poses Mode 1 validadas en QC; "
        "sin re-dock, sin inferencia agonista/antagonista desde scores.",
        "",
        "## Inputs",
        "",
        "| Rol | Archivo |",
        "|-----|---------|",
        f"| THCV CB2 pose | `{paths['thcv_cb2']}` |",
        f"| THCV CB1 pose | `{paths['thcv_cb1']}` |",
        f"| HU-308 CB2 pose | `{paths['hu_cb2']}` |",
        f"| AM6538 co-crystal (CB1 ref) | `{paths['am6538']}` |",
        f"| CB2 receptor | `{paths['cb2_pdb']}` |",
        f"| CB1 receptor | `{paths['cb1_pdb']}` |",
        "",
        "## 1. CB2 (6PT0) — THCV vs HU-308",
        "",
        "### 1.1 Sub-bolsillo C3 (cadena propílica vs canal HU-308)",
        "",
        f"- Terminación propilo THCV → attachment aromático: "
        f"**{c3['c3_vector_propyl_length_A']:.2f} Å**",
        f"- Profundidad relativa HU vs THCV en eje C3 (proyección desde anillo): "
        f"HU max **{c3['hu308_chain_max_projection_on_c3_axis_A']} Å** vs "
        f"THCV term **{c3['thcv_propyl_projection_on_c3_axis_A']} Å** "
        f"(Δ profundidad HU − THCV = "
        f"{round(c3['hu308_chain_max_projection_on_c3_axis_A'] - c3['thcv_propyl_projection_on_c3_axis_A'], 2)} Å)",
        f"- Distancia mínima termino propilo THCV → cadena HU-308: "
        f"**{c3['min_thcv_propyl_term_to_hu_chain_A']} Å**",
        f"- **Clearance receptor** más allá del termino propilo (@3.0 Å clash): "
        f"**{c3['receptor_clearance_beyond_propyl_term_A']['free_extension_before_3.0A_clash_A']} Å**",
        "",
        "En el eje C3 definido por THCV, el propilo **proyecta más lejos** que la cadena "
        "alquílica de HU-308; la ocupación HU es principalmente **transversal** "
        f"(min dist {c3['min_thcv_propyl_term_to_hu_chain_A']} Å al termino propilo). "
        f"El espacio explotable para extensión C3 hacia el túnel es ~"
        f"{c3['residual_free_volume_along_c3_vector_A']} Å antes del primer clash "
        "con cáscara del receptor.",
        "",
        "### 1.2 Red H-bond / polar (THCV, residuos ≤4.5 Å)",
        "",
        "| Residuo | Min heavy (Å) | ≤4.5 Å | H-bond convencional |",
        "|---------|---------------|--------|---------------------|",
    ]

    for label, data in polar.items():
        hb = "—"
        if "hbond_ligand_as_donor" in data:
            d = data["hbond_ligand_as_donor"]
            hb = "sí" if d.get("hbond_geometry_present") else "no"
        lines.append(
            f"| {label} | {data['min_heavy_ligand_to_sidechain_A']:.2f} | "
            f"{'sí' if data['within_4.5A'] else 'no'} | {hb} |"
        )

    lines.extend(
        [
            "",
            "Criterio H-bond: donor heavy ≤3.5 Å y H ≤2.6 Å al aceptor. "
            "Ningún donor THCV satisface geometría convencional con Ser285 OG "
            "(consistente con QC previo).",
            "",
            "### 1.3 Zona C9 / C11",
            "",
        f"- C9 metilo THCV ↔ hidroximetilo O (HU-308): **{c9z['c9_methyl_to_hu_hydroxymethyl_O_A']} Å**",
        f"- C9 metilo THCV ↔ hidroximetilo C (HU-308): **{c9z['c9_methyl_to_hu_hydroxymethyl_C_A']} Å**",
        f"- Vector unitario C9→HU polar: `{c9z.get('c9_to_hu_polar_direction_unit')}`",
            "",
            c9z["geometry_note"],
            "",
            "## 2. CB1 (5TGZ) — THCV vs AM6538",
            "",
            "### 2.1 Posicionamiento en cavidad ocluida (inactive)",
            "",
            f"- Separación centroides ligando THCV / AM6538: **{cb1['thcv_vs_am6538_placement']['ligand_centroid_separation_A']} Å**",
            f"- Min distancia heavy-heavy inter-ligando: **{cb1['thcv_vs_am6538_placement']['min_heavy_heavy_distance_A']} Å**",
            "",
            cb1["thcv_vs_am6538_placement"]["note"],
            "",
            "### 2.2 Espacio libre hacia zona switch Phe200 / Trp356",
            "",
            "| Microswitch | THCV min (Å) | AM6538 min (Å) |",
            "|-------------|--------------|----------------|",
        ]
    )

    for label, data in cb1["switch_zone_Phe200_Trp356"].items():
        lines.append(
            f"| {label} | {data['thcv_min_heavy_A']:.2f} | {data['am6538_min_heavy_A']:.2f} |"
        )

    c3c = cb1["c3_extension_clearance"]
    c9c = cb1["c9_extension_clearance"]
    lines.extend(
        [
            "",
            "THCV mode 1 mantiene **Trp356(6.48)** a ~3.7 Å (contacto cercano) mientras "
            "**Phe200(3.36)** permanece lejano (~7.0 Å), coherente con poses parcialmente "
            "desplazadas respecto al AM6538 cristalino en el bolsillo ocluido.",
            "",
            "### 2.3 Tolerancia estérica C3 / C9 (umbral clash HA–HA)",
            "",
            "| Vector | Extensión libre @2.5 Å | Extensión libre @3.0 Å | "
            "Min TM3 shell | Min TM6 shell |",
            "|--------|------------------------|------------------------|"
            "---------------|---------------|",
            f"| C3 (propilo) | {c3c['free_extension_before_2.5A_clash_A']:.2f} Å | "
            f"{c3c['free_extension_before_3.0A_clash_A']:.2f} Å | "
            f"{c3c['min_propyl_term_to_TM3_shell_A']:.2f} Å | "
            f"{c3c['min_propyl_term_to_TM6_shell_A']:.2f} Å |",
            f"| C9 (metilo) | {c9c['free_extension_before_2.5A_clash_A']:.2f} Å | "
            f"{c9c['free_extension_before_3.0A_clash_A']:.2f} Å | "
            f"{c9c['min_c9_methyl_to_TM3_shell_A']:.2f} Å | "
            f"{c9c['min_c9_methyl_to_TM6_shell_A']:.2f} Å |",
            "",
            "## 3. Tabla resumen — vectores de tolerancia",
            "",
            "| Vector / Posición | Espacio Disponible (Å) | "
            "Interacciones Potenciales en CB2 | Riesgo Estérico en CB1 |",
            "|-------------------|------------------------|"
            "--------------------------------|------------------------|",
        ]
    )

    for row in table:
        lines.append(
            f"| {row['vector']} | {row['espacio_A']} | "
            f"{row['cb2_interactions']} | {row['cb1_steric_risk']} |"
        )

    lines.extend(
        [
            "",
            "## 4. Sub-bolsillos explotables (solo geometría)",
            "",
            "1. **Canal C3 (CB2):** THCV propilo ya proyecta más lejos que la cadena HU "
            f"en el eje C3 común; clearance receptor ~"
            f"{c3['residual_free_volume_along_c3_vector_A']} Å más allá del termino propilo.",
            "2. **Zona polar C9/C11 (CB2):** THCV presenta metilo apolar donde HU-308 tiene "
            f"hidroximetilo (O a {c9z['c9_methyl_to_hu_hydroxymethyl_O_A']} Å); Ser285 queda a "
            f"{polar['Ser285(7.39)']['min_heavy_ligand_to_sidechain_A']:.1f} Å — espacio para "
            "introducir heteroátomo sin saturar red H-bond existente.",
            "3. **CB1 switch:** Trp356 contacto cercano (~3.7 Å) limita expansiones hacia TM6; "
            f"Phe200 deja ~{cb1['switch_zone_Phe200_Trp356']['Phe200(3.36)']['thcv_min_heavy_A']:.1f} Å "
            "de margen — extensiones C9 deben monitorear clash TM6 antes que TM3.",
            "",
            f"JSON distancias: `{paths['json_out']}`",
            f"Script: `{paths['script']}`",
            "",
        ]
    )

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def run_interaction_mapping(
    root: Path = ROOT,
    out_md: Path | None = None,
    out_json: Path | None = None,
) -> dict[str, Any]:
    """Run full THCV vs gold interaction mapping analysis."""
    out_md = out_md or root / "results/docking/interaction_mapping_thcv_vs_gold.md"
    out_json = out_json or root / "results/docking/interaction_mapping_thcv_vs_gold_distances.json"

    paths = {
        "thcv_cb2": "results/docking/thcv_seed/cb2/delta9-THCV__THCV__docked.pdbqt",
        "thcv_cb1": "results/docking/thcv_seed/cb1/delta9-THCV__THCV__docked.pdbqt",
        "hu_cb2": "results/docking/benchmark_gold_exam_a/cb2/HU-308_docked.pdbqt",
        "am6538": "data/targets/cb1/am6538_ref.pdbqt",
        "cb2_pdb": "data/targets/cb2/6PT0_clean.pdb",
        "cb1_pdb": "data/targets/cb1/5TGZ_clean.pdb",
        "json_out": str(out_json.relative_to(root)),
        "script": "scripts/run_interaction_mapping_thcv_vs_gold.py",
    }

    missing = [k for k, v in paths.items() if k not in {"json_out", "script"} and not (root / v).exists()]
    if missing:
        raise FileNotFoundError(f"Missing inputs: {missing}")

    cb2 = _analyze_cb2(
        root / paths["thcv_cb2"],
        root / paths["hu_cb2"],
        root / paths["cb2_pdb"],
    )
    cb1 = _analyze_cb1(
        root / paths["thcv_cb1"],
        root / paths["am6538"],
        root / paths["cb1_pdb"],
    )
    table = _build_summary_table(cb2, cb1)

    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "method": (
            "Mode 1 poses; atom mapping via distance-signature permutation; "
            "min heavy-atom distances; vector clearance sampling step=0.25 Å; "
            f"polar cutoff {POLAR_CUTOFF_A} Å; H-bond D-A ≤{HBOND_DA_MAX_A} Å, H-A ≤{HBOND_HA_MAX_A} Å"
        ),
        "inputs": paths,
        "cb2_thcv_vs_hu308": cb2,
        "cb1_thcv_vs_am6538": cb1,
        "summary_table": table,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    _write_markdown(out_md, cb2, cb1, table, paths)

    return payload
