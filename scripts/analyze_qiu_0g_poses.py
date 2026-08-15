#!/usr/bin/env python3
"""Qiu 0G — pose analysis of CB2 docking outputs (compounds 14/15/20/24).

Read-only: parses poses written in *_out.pdbqt only (no Vina re-run,
no PDBQT modification). Writes JSON summary for report authoring.
"""

from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

ROOT = Path(__file__).resolve().parents[1]
RECEPTOR = ROOT / "data" / "targets" / "cb2" / "6PT0_rec.pdbqt"
OUT_DIR = ROOT / "results" / "docking" / "qiu_0f"
REPORT_JSON = ROOT / "results" / "reports" / "qiu_0g_pose_analysis_data.json"

# Box from 0F protocol (reference only; not used to filter poses).
BOX_CENTER = np.array([98.379, 109.559, 123.801], dtype=float)

HEAVY_CUTOFF = 4.0  # Å — contact definition
HBOND_DA_CUTOFF = 3.5  # Å donor–acceptor heavy
HBOND_HA_CUTOFF = 2.5  # Å H–acceptor
HBOND_ANGLE_MIN = 120.0  # degrees D–H···A

COMPOUNDS = {
    14: {
        "smiles": "Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1",
        "n1_sub": "o-morpholine",
        "r3": "CONH-Ad",
    },
    15: {
        "smiles": "Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2cccc(N3CCOCC3)c2)c1-c1ccccc1",
        "n1_sub": "m-morpholine",
        "r3": "CONH-Ad",
    },
    20: {
        "smiles": "Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCN(C)CC2)c1-c1ccccc1",
        "n1_sub": "o-Me-piperazine",
        "r3": "CONH-Ad",
    },
    24: {
        "smiles": "Cc1c(C(=O)NCC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1",
        "n1_sub": "o-morpholine",
        "r3": "CONH-CH2-Ad",
    },
}

# SMARTS for moiety centroids (matched on RDKit mol from REMARK SMILES).
SMARTS = {
    "pyrazole": Chem.MolFromSmarts("n1nccc1"),  # 1H-pyrazole core (aromatic)
    "amide_c": Chem.MolFromSmarts("[CX3](=O)[NX3]"),
    "morpholine": Chem.MolFromSmarts("N1CCOCC1"),
    "piperazine": Chem.MolFromSmarts("N1CCN(C)CC1"),
    "adamantyl": Chem.MolFromSmarts("C12CC3CC(CC(C3)C1)C2"),
    "phenyl": Chem.MolFromSmarts("c1ccccc1"),
}


def is_hydrogen_name(name: str, atype: str) -> bool:
    n = name.strip().upper()
    t = atype.strip().upper()
    if n.startswith("H"):
        return True
    if t in {"H", "HD", "HS"}:
        return True
    return False


def parse_pdbqt_atoms(text: str, chain_filter: str | None = None):
    """Parse ATOM/HETATM lines → list of dicts."""
    atoms = []
    for line in text.splitlines():
        if not (line.startswith("ATOM") or line.startswith("HETATM")):
            continue
        # PDBQT columns (AutoDock-style)
        name = line[12:16].strip()
        resn = line[17:20].strip()
        chain = line[21].strip() or " "
        try:
            resi = int(line[22:26])
        except ValueError:
            continue
        try:
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
        except ValueError:
            continue
        atype = line[77:79].strip() if len(line) >= 79 else ""
        if chain_filter is not None and chain != chain_filter:
            continue
        atoms.append(
            {
                "name": name,
                "resn": resn,
                "chain": chain,
                "resi": resi,
                "xyz": np.array([x, y, z], dtype=float),
                "atype": atype,
                "heavy": not is_hydrogen_name(name, atype),
                "serial": len(atoms) + 1,
            }
        )
    return atoms


def parse_smiles_idx(block: str) -> dict[int, int]:
    """Map RDKit/SMILES 1-based atom index → PDBQT atom serial (1-based)."""
    pairs = []
    for line in block.splitlines():
        if not line.startswith("REMARK SMILES IDX"):
            continue
        nums = [int(x) for x in line.split()[3:]]
        for i in range(0, len(nums), 2):
            if i + 1 < len(nums):
                pairs.append((nums[i], nums[i + 1]))
    return {smi: pdb for smi, pdb in pairs}


def parse_poses(pdbqt_path: Path) -> list[dict]:
    text = pdbqt_path.read_text(encoding="utf-8", errors="replace")
    # Split on MODEL … ENDMDL; only written models.
    models = []
    parts = re.split(r"(?=^MODEL\s+\d+)", text, flags=re.M)
    for part in parts:
        part = part.strip()
        if not part.startswith("MODEL"):
            continue
        m_model = re.search(r"^MODEL\s+(\d+)", part, re.M)
        m_vina = re.search(
            r"REMARK VINA RESULT:\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)",
            part,
        )
        if not m_model or not m_vina:
            continue
        smiles_m = re.search(r"REMARK SMILES\s+(\S+)", part)
        atoms = parse_pdbqt_atoms(part)
        # renumber serials 1..n in order of appearance
        for i, a in enumerate(atoms, start=1):
            a["serial"] = i
        models.append(
            {
                "model": int(m_model.group(1)),
                "vina_score": float(m_vina.group(1)),
                "rmsd_lb": float(m_vina.group(2)),
                "rmsd_ub": float(m_vina.group(3)),
                "smiles": smiles_m.group(1) if smiles_m else None,
                "smiles_idx": parse_smiles_idx(part),
                "atoms": atoms,
            }
        )
    return models


def load_receptor_chain_r() -> list[dict]:
    text = RECEPTOR.read_text(encoding="utf-8", errors="replace")
    atoms = parse_pdbqt_atoms(text, chain_filter="R")
    return atoms


def residue_key(a: dict) -> str:
    return f"{a['resn']}{a['resi']}"


def classify_hbond_partners(atype: str, name: str) -> tuple[bool, bool]:
    """Return (is_donor_heavy, is_acceptor) from PDBQT atom type."""
    t = atype.strip().upper()
    n = name.strip().upper()
    # Acceptors: OA, NA, N (some), SA, OS — conservative PDBQT set
    acceptor = t in {"OA", "NA", "N", "SA", "OS", "O"}
    # Donor heavy: N, NA, OA (OH), SA (SH) — H attached separately
    donor_heavy = t in {"N", "NA", "OA", "SA", "O"} or n in {"N", "O", "S", "OG", "OG1", "ND1", "ND2", "NE", "NE1", "NE2", "NH1", "NH2", "NZ", "OH", "SG"}
    return donor_heavy, acceptor


def find_attached_h(atoms: list[dict], heavy_idx: int, max_bond: float = 1.3) -> list[int]:
    h_idxs = []
    hv = atoms[heavy_idx]["xyz"]
    for j, a in enumerate(atoms):
        if a["heavy"]:
            continue
        if np.linalg.norm(a["xyz"] - hv) <= max_bond:
            h_idxs.append(j)
    return h_idxs


def analyze_contacts(lig_atoms: list[dict], rec_atoms: list[dict]) -> dict:
    lig_heavy = [(i, a) for i, a in enumerate(lig_atoms) if a["heavy"]]
    rec_heavy = [(i, a) for i, a in enumerate(rec_atoms) if a["heavy"]]

    lig_xyz = np.array([a["xyz"] for _, a in lig_heavy])
    rec_xyz = np.array([a["xyz"] for _, a in rec_heavy])

    # Pairwise distances (could be large but receptor+ligand is fine)
    # Restrict receptor to nearby box for speed
    near_mask = np.linalg.norm(rec_xyz - BOX_CENTER, axis=1) <= 20.0
    rec_heavy_near = [rec_heavy[k] for k in np.where(near_mask)[0]]
    rec_xyz_near = rec_xyz[near_mask]

    dmat = np.linalg.norm(lig_xyz[:, None, :] - rec_xyz_near[None, :, :], axis=2)
    contact_pairs = np.argwhere(dmat <= HEAVY_CUTOFF)

    residue_min: dict[str, float] = {}
    residue_atoms: dict[str, list] = defaultdict(list)
    for li, ri in contact_pairs:
        la = lig_heavy[li][1]
        ra = rec_heavy_near[ri][1]
        key = residue_key(ra)
        dist = float(dmat[li, ri])
        if key not in residue_min or dist < residue_min[key]:
            residue_min[key] = dist
        residue_atoms[key].append(
            {
                "lig_atom": la["name"],
                "lig_atype": la["atype"],
                "rec_atom": ra["name"],
                "rec_atype": ra["atype"],
                "dist": round(dist, 3),
            }
        )

    # H-bonds with geometry when H present
    hbonds = []
    # Build ligand donor/acceptor lists with H
    for li, la in lig_heavy:
        is_don, is_acc = classify_hbond_partners(la["atype"], la["name"])
        if is_don:
            h_idxs = find_attached_h(lig_atoms, li)
            for ri, ra in rec_heavy_near:
                _, r_acc = classify_hbond_partners(ra["atype"], ra["name"])
                if not r_acc:
                    continue
                da = float(np.linalg.norm(la["xyz"] - ra["xyz"]))
                if da > HBOND_DA_CUTOFF:
                    continue
                best = None
                for hi in h_idxs:
                    ha = float(np.linalg.norm(lig_atoms[hi]["xyz"] - ra["xyz"]))
                    if ha > HBOND_HA_CUTOFF:
                        continue
                    v1 = la["xyz"] - lig_atoms[hi]["xyz"]
                    v2 = ra["xyz"] - lig_atoms[hi]["xyz"]
                    n1 = np.linalg.norm(v1)
                    n2 = np.linalg.norm(v2)
                    if n1 < 1e-6 or n2 < 1e-6:
                        continue
                    ang = math.degrees(
                        math.acos(np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0))
                    )
                    if ang < HBOND_ANGLE_MIN:
                        continue
                    cand = (ha, da, ang)
                    if best is None or ha < best[0]:
                        best = cand
                if best is not None:
                    hbonds.append(
                        {
                            "direction": "lig_donor→rec_acceptor",
                            "lig": f"{la['name']}({la['atype']})",
                            "rec": f"{residue_key(ra)} {ra['name']}({ra['atype']})",
                            "d_HA": round(best[0], 3),
                            "d_DA": round(best[1], 3),
                            "angle_DHA": round(best[2], 1),
                        }
                    )
                elif da <= 3.2 and not h_idxs:
                    # no H on ligand donor — note proximity only
                    pass

        if is_acc:
            for ri, ra in rec_heavy_near:
                r_don, _ = classify_hbond_partners(ra["atype"], ra["name"])
                if not r_don:
                    continue
                da = float(np.linalg.norm(la["xyz"] - ra["xyz"]))
                if da > HBOND_DA_CUTOFF:
                    continue
                # find H on receptor donor
                # receptor atom list index
                # search among all rec atoms near this heavy
                rec_h = []
                for a in rec_atoms:
                    if a["heavy"]:
                        continue
                    if a["resi"] != ra["resi"] or a["chain"] != ra["chain"]:
                        continue
                    if np.linalg.norm(a["xyz"] - ra["xyz"]) <= 1.3:
                        rec_h.append(a)
                best = None
                for h in rec_h:
                    ha = float(np.linalg.norm(h["xyz"] - la["xyz"]))
                    if ha > HBOND_HA_CUTOFF:
                        continue
                    v1 = ra["xyz"] - h["xyz"]
                    v2 = la["xyz"] - h["xyz"]
                    n1 = np.linalg.norm(v1)
                    n2 = np.linalg.norm(v2)
                    if n1 < 1e-6 or n2 < 1e-6:
                        continue
                    ang = math.degrees(
                        math.acos(np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0))
                    )
                    if ang < HBOND_ANGLE_MIN:
                        continue
                    cand = (ha, da, ang)
                    if best is None or ha < best[0]:
                        best = cand
                if best is not None:
                    hbonds.append(
                        {
                            "direction": "rec_donor→lig_acceptor",
                            "lig": f"{la['name']}({la['atype']})",
                            "rec": f"{residue_key(ra)} {ra['name']}({ra['atype']})",
                            "d_HA": round(best[0], 3),
                            "d_DA": round(best[1], 3),
                            "angle_DHA": round(best[2], 1),
                        }
                    )

    # Deduplicate hbonds by (lig, rec)
    seen = set()
    uniq = []
    for h in sorted(hbonds, key=lambda x: x["d_HA"]):
        k = (h["direction"], h["lig"], h["rec"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(h)

    # Hydrophobic proximity: C/A-type lig near C/A-type rec within cutoff
    hydrophobic = []
    for key, pairs in residue_atoms.items():
        hydro_pairs = [
            p
            for p in pairs
            if p["lig_atype"] in {"C", "A"} and p["rec_atype"] in {"C", "A"}
        ]
        if hydro_pairs:
            hydrophobic.append(
                {
                    "residue": key,
                    "n_pairs": len(hydro_pairs),
                    "min_dist": min(p["dist"] for p in hydro_pairs),
                }
            )
    hydrophobic.sort(key=lambda x: x["min_dist"])

    contacts_sorted = sorted(residue_min.items(), key=lambda x: x[1])
    return {
        "n_contact_residues": len(contacts_sorted),
        "contact_residues": [
            {"residue": k, "min_heavy_dist": round(v, 3)} for k, v in contacts_sorted
        ],
        "principal_residues": [k for k, _ in contacts_sorted[:12]],
        "hbonds_geometry_ok": uniq,
        "hydrophobic_proximity": hydrophobic[:15],
        "cutoff_heavy_A": HEAVY_CUTOFF,
    }


def moiety_atom_serials(smiles: str, smiles_idx: dict[int, int], compound_id: int) -> dict:
    """Map moiety names → list of PDBQT serials via SMARTS + SMILES IDX."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {}
    out = {}

    # pyrazole
    hits = mol.GetSubstructMatches(SMARTS["pyrazole"])
    if hits:
        out["pyrazole"] = [smiles_idx[i + 1] for i in hits[0] if (i + 1) in smiles_idx]

    # amide carbonyl C + O + N
    amide = Chem.MolFromSmarts("[CX3](=O)[NX3]")
    hits = mol.GetSubstructMatches(amide)
    if hits:
        out["amide"] = [smiles_idx[i + 1] for i in hits[0] if (i + 1) in smiles_idx]

    # N1 substituent heterocycle
    if compound_id == 20:
        hits = mol.GetSubstructMatches(SMARTS["piperazine"])
        key = "n1_heterocycle"
    else:
        hits = mol.GetSubstructMatches(SMARTS["morpholine"])
        key = "n1_heterocycle"
    if hits:
        out[key] = [smiles_idx[i + 1] for i in hits[0] if (i + 1) in smiles_idx]

    # adamantyl
    hits = mol.GetSubstructMatches(SMARTS["adamantyl"])
    if hits:
        # pick largest / first adamantyl (R3)
        out["adamantyl"] = [
            smiles_idx[i + 1] for i in hits[0] if (i + 1) in smiles_idx
        ]

    # phenyls: C5-Ph and N1-Ph — distinguish by attachment
    # N1 attachment: phenyl bonded to pyrazole N
    # Use atom indices from pyrazole match
    phenyls = mol.GetSubstructMatches(SMARTS["phenyl"])
    if "pyrazole" in out and hits is not None:
        # map pyrazole N atoms in SMILES indexing
        pyr_match = mol.GetSubstructMatches(SMARTS["pyrazole"])[0]
        # In 1H-pyrazole SMARTS n1nccc1: indices 0,1 are N atoms; N1 is typically the substituted N
        # Find which N has a phenyl substituent
        n1_ph = None
        c5_ph = None
        for ph in phenyls:
            ph_set = set(ph)
            # check neighbors of phenyl carbons outside ring
            for aidx in ph:
                atom = mol.GetAtomWithIdx(aidx)
                for nbr in atom.GetNeighbors():
                    if nbr.GetIdx() in ph_set:
                        continue
                    # bonded to pyrazole?
                    if nbr.GetIdx() in pyr_match:
                        # which pyrazole atom?
                        pos = pyr_match.index(nbr.GetIdx())
                        serials = [
                            smiles_idx[i + 1] for i in ph if (i + 1) in smiles_idx
                        ]
                        if pos <= 1:  # N
                            n1_ph = serials
                        else:
                            c5_ph = serials
        if n1_ph:
            out["n1_phenyl"] = n1_ph
        if c5_ph:
            out["c5_phenyl"] = c5_ph

    # C4-methyl: aliphatic methyl on pyrazole
    # SMARTS: [CH3] attached to pyrazole C
    me = Chem.MolFromSmarts("[CH3][#6]")
    for hit in mol.GetSubstructMatches(me):
        # methyl carbon
        if (hit[0] + 1) in smiles_idx:
            # check attachment to pyrazole
            if hit[1] in mol.GetSubstructMatches(SMARTS["pyrazole"])[0]:
                out["c4_methyl"] = [smiles_idx[hit[0] + 1]]
                break

    # linker CH2 for compound 24: amide N–CH2–Ad
    if compound_id == 24:
        linker = Chem.MolFromSmarts("[NX3][CH2][C]")
        for hit in mol.GetSubstructMatches(linker):
            if (hit[1] + 1) in smiles_idx:
                out["amide_ch2"] = [smiles_idx[hit[1] + 1]]
                break

    return out


def centroid_from_serials(atoms: list[dict], serials: list[int]) -> np.ndarray | None:
    by_s = {a["serial"]: a for a in atoms}
    pts = [by_s[s]["xyz"] for s in serials if s in by_s and by_s[s]["heavy"]]
    if not pts:
        return None
    return np.mean(pts, axis=0)


def orientation_summary(pose: dict, compound_id: int) -> dict:
    smiles = pose["smiles"] or COMPOUNDS[compound_id]["smiles"]
    moieties = moiety_atom_serials(smiles, pose["smiles_idx"], compound_id)
    atoms = pose["atoms"]
    cents = {}
    for name, serials in moieties.items():
        c = centroid_from_serials(atoms, serials)
        if c is not None:
            cents[name] = c

    lig_heavy_xyz = np.array([a["xyz"] for a in atoms if a["heavy"]])
    lig_cent = lig_heavy_xyz.mean(axis=0)

    def vec(name: str):
        if "pyrazole" not in cents or name not in cents:
            return None
        v = cents[name] - cents["pyrazole"]
        return {
            "dx": round(float(v[0]), 3),
            "dy": round(float(v[1]), 3),
            "dz": round(float(v[2]), 3),
            "length": round(float(np.linalg.norm(v)), 3),
            "centroid": [round(float(x), 3) for x in cents[name]],
        }

    # Direction labels relative to box axes (observed geometry, not biology)
    def axis_label(vinfo):
        if vinfo is None:
            return None
        comps = [("+x", vinfo["dx"]), ("+y", vinfo["dy"]), ("+z", vinfo["dz"])]
        # dominant absolute component
        best = max(
            [
                ("+x" if vinfo["dx"] >= 0 else "-x", abs(vinfo["dx"])),
                ("+y" if vinfo["dy"] >= 0 else "-y", abs(vinfo["dy"])),
                ("+z" if vinfo["dz"] >= 0 else "-z", abs(vinfo["dz"])),
            ],
            key=lambda t: t[1],
        )
        return best[0]

    orient = {
        "ligand_centroid": [round(float(x), 3) for x in lig_cent],
        "dist_to_box_center": round(float(np.linalg.norm(lig_cent - BOX_CENTER)), 3),
        "pyrazole_centroid": (
            [round(float(x), 3) for x in cents["pyrazole"]]
            if "pyrazole" in cents
            else None
        ),
        "vectors_from_pyrazole": {
            "n1_heterocycle": vec("n1_heterocycle"),
            "adamantyl": vec("adamantyl"),
            "c5_phenyl": vec("c5_phenyl"),
            "n1_phenyl": vec("n1_phenyl"),
            "amide": vec("amide"),
        },
        "dominant_axis_from_pyrazole": {
            k: axis_label(vec(k))
            for k in ("n1_heterocycle", "adamantyl", "c5_phenyl", "n1_phenyl")
        },
        "moiety_serials": moieties,
        "n1_sub_label": COMPOUNDS[compound_id]["n1_sub"],
        "r3_label": COMPOUNDS[compound_id]["r3"],
    }
    # Heterocycle vs amide/Ad relative placement (observed)
    if "n1_heterocycle" in cents and "adamantyl" in cents and "pyrazole" in cents:
        d_het_ad = float(np.linalg.norm(cents["n1_heterocycle"] - cents["adamantyl"]))
        orient["dist_n1het_to_adamantyl"] = round(d_het_ad, 3)
    if "amide_ch2" in cents:
        orient["amide_ch2_centroid"] = [round(float(x), 3) for x in cents["amide_ch2"]]

    # Nearest contact residues to n1 heterocycle and adamantyl (structural proximity)
    return orient


def nearest_residues_to_moiety(
    pose: dict, serials: list[int], rec_atoms: list[dict], top_n: int = 5
) -> list[dict]:
    by_s = {a["serial"]: a for a in pose["atoms"]}
    lig_pts = [by_s[s]["xyz"] for s in serials if s in by_s and by_s[s]["heavy"]]
    if not lig_pts:
        return []
    lig_xyz = np.array(lig_pts)
    rec_heavy = [a for a in rec_atoms if a["heavy"]]
    rec_xyz = np.array([a["xyz"] for a in rec_heavy])
    near = np.linalg.norm(rec_xyz - BOX_CENTER, axis=1) <= 20.0
    rec_heavy = [a for a, m in zip(rec_heavy, near) if m]
    rec_xyz = rec_xyz[near]
    dmat = np.linalg.norm(lig_xyz[:, None, :] - rec_xyz[None, :, :], axis=2)
    res_min: dict[str, float] = {}
    for ri, ra in enumerate(rec_heavy):
        md = float(dmat[:, ri].min())
        if md > HEAVY_CUTOFF:
            continue
        key = residue_key(ra)
        if key not in res_min or md < res_min[key]:
            res_min[key] = md
    return [
        {"residue": k, "min_dist": round(v, 3)}
        for k, v in sorted(res_min.items(), key=lambda x: x[1])[:top_n]
    ]


def heavy_rmsd(a_atoms: list[dict], b_atoms: list[dict]) -> float | None:
    ah = [a["xyz"] for a in a_atoms if a["heavy"]]
    bh = [a["xyz"] for a in b_atoms if a["heavy"]]
    if len(ah) != len(bh) or not ah:
        return None
    a = np.array(ah)
    b = np.array(bh)
    return float(np.sqrt(((a - b) ** 2).sum(axis=1).mean()))


def main() -> None:
    rec = load_receptor_chain_r()
    results = {
        "methods": {
            "poses_source": "MODEL blocks in results/docking/qiu_0f/compound_*_cb2_out.pdbqt only",
            "receptor": str(RECEPTOR.relative_to(ROOT)).replace("\\", "/"),
            "receptor_chain": "R (CB2 in 6PT0)",
            "heavy_contact_cutoff_A": HEAVY_CUTOFF,
            "hbond_criteria": {
                "d_DA_max_A": HBOND_DA_CUTOFF,
                "d_HA_max_A": HBOND_HA_CUTOFF,
                "angle_DHA_min_deg": HBOND_ANGLE_MIN,
                "note": "H-bond reported only when D–H···A geometry criteria met; else hydrophobic proximity or unlabeled contact",
            },
            "box_center_ref": BOX_CENTER.tolist(),
        },
        "compounds": {},
    }

    best_poses = {}
    for cid in (14, 15, 20, 24):
        path = OUT_DIR / f"compound_{cid}_cb2_out.pdbqt"
        poses = parse_poses(path)
        # best = lowest (most negative) vina score among written poses
        best = min(poses, key=lambda p: p["vina_score"])
        contacts = analyze_contacts(best["atoms"], rec)
        orient = orientation_summary(best, cid)
        # moiety-local contacts
        mo = orient["moiety_serials"]
        orient["n1_heterocycle_nearby_residues"] = nearest_residues_to_moiety(
            best, mo.get("n1_heterocycle", []), rec
        )
        orient["adamantyl_nearby_residues"] = nearest_residues_to_moiety(
            best, mo.get("adamantyl", []), rec
        )

        entry = {
            "out_pdbqt": str(path.relative_to(ROOT)).replace("\\", "/"),
            "n_poses_pdbqt": len(poses),
            "poses": [
                {
                    "model": p["model"],
                    "vina_score": p["vina_score"],
                    "rmsd_lb": p["rmsd_lb"],
                    "rmsd_ub": p["rmsd_ub"],
                    "n_atoms": len(p["atoms"]),
                    "n_heavy": sum(1 for a in p["atoms"] if a["heavy"]),
                }
                for p in poses
            ],
            "best_pose_model": best["model"],
            "best_vina_score": best["vina_score"],
            "contacts_best": contacts,
            "orientation_best": orient,
            "n1_sub": COMPOUNDS[cid]["n1_sub"],
            "r3": COMPOUNDS[cid]["r3"],
        }
        results["compounds"][str(cid)] = entry
        best_poses[cid] = best

    # Pairwise comparisons of best poses (geometry)
    comparisons = {}
    ids = [14, 15, 20, 24]
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            ca = np.array(
                results["compounds"][str(a)]["orientation_best"]["ligand_centroid"]
            )
            cb = np.array(
                results["compounds"][str(b)]["orientation_best"]["ligand_centroid"]
            )
            pyr_a = results["compounds"][str(a)]["orientation_best"]["pyrazole_centroid"]
            pyr_b = results["compounds"][str(b)]["orientation_best"]["pyrazole_centroid"]
            d_cent = float(np.linalg.norm(ca - cb))
            d_pyr = (
                float(np.linalg.norm(np.array(pyr_a) - np.array(pyr_b)))
                if pyr_a and pyr_b
                else None
            )
            # heavy RMSD only if same atom count
            rmsd = heavy_rmsd(best_poses[a]["atoms"], best_poses[b]["atoms"])
            set_a = set(
                r["residue"]
                for r in results["compounds"][str(a)]["contacts_best"]["contact_residues"]
            )
            set_b = set(
                r["residue"]
                for r in results["compounds"][str(b)]["contacts_best"]["contact_residues"]
            )
            comparisons[f"{a}_vs_{b}"] = {
                "centroid_distance_A": round(d_cent, 3),
                "pyrazole_centroid_distance_A": round(d_pyr, 3) if d_pyr is not None else None,
                "heavy_rmsd_A_same_atom_count_only": (
                    round(rmsd, 3) if rmsd is not None else None
                ),
                "contact_residue_jaccard": round(
                    len(set_a & set_b) / len(set_a | set_b), 3
                )
                if (set_a | set_b)
                else None,
                "shared_contact_residues": sorted(set_a & set_b),
                "unique_a": sorted(set_a - set_b),
                "unique_b": sorted(set_b - set_a),
            }
    results["pairwise_best_pose_geometry"] = comparisons

    # Binding-region flag: all within ~same region if centroids within 3 Å of mutual mean
    cents = np.array(
        [
            results["compounds"][str(c)]["orientation_best"]["ligand_centroid"]
            for c in ids
        ]
    )
    mean_c = cents.mean(axis=0)
    dists = np.linalg.norm(cents - mean_c, axis=1)
    results["binding_region_check"] = {
        "mean_ligand_centroid": [round(float(x), 3) for x in mean_c],
        "dist_from_mean_centroid_A": {
            str(c): round(float(d), 3) for c, d in zip(ids, dists)
        },
        "max_dist_from_mean_A": round(float(dists.max()), 3),
        "comparable_region_criterion": "all best-pose ligand centroids within 3.0 Å of mutual mean AND Jaccard(contact residues) mean >= 0.40",
    }
    jacs = [
        comparisons[k]["contact_residue_jaccard"]
        for k in comparisons
        if comparisons[k]["contact_residue_jaccard"] is not None
    ]
    results["binding_region_check"]["mean_pairwise_contact_jaccard"] = round(
        float(np.mean(jacs)), 3
    )
    results["binding_region_check"]["comparable_yes_no"] = bool(
        float(dists.max()) <= 3.0 and float(np.mean(jacs)) >= 0.40
    )

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {REPORT_JSON}")
    print("poses:", {c: results["compounds"][str(c)]["n_poses_pdbqt"] for c in ids})
    print(
        "best scores:",
        {c: results["compounds"][str(c)]["best_vina_score"] for c in ids},
    )
    print("comparable:", results["binding_region_check"]["comparable_yes_no"])
    print("max centroid drift:", results["binding_region_check"]["max_dist_from_mean_A"])


if __name__ == "__main__":
    main()
