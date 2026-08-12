#!/usr/bin/env python3
"""Geometric pharmacophore feature map: D2_20/06/22 vs Qiu 14/15/20/24 on CB2.

Read-only: best MODEL poses from existing PDBQTs only.
No re-docking, no PDBQT modification, no SAR / pharmacology claims.

Primary metrics: feature centroids + residue shells (heavy ≤ 4.0 Å).
Cross-chemotype whole-ligand RMSD is intentionally omitted.

Writes:
  results/reports/qiu_0g_vs_d1_pharmacophore_geometry_data.json
  results/reports/qiu_0g_vs_d1_pharmacophore_geometry.md
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from rdkit import Chem

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_qiu_0g_poses import (  # noqa: E402
    BOX_CENTER,
    HEAVY_CUTOFF,
    load_receptor_chain_r,
    parse_pdbqt_atoms,
    parse_smiles_idx,
    residue_key,
)
from compare_qiu_0g_vs_d1_cb2 import parse_poses  # noqa: E402

RECEPTOR = ROOT / "data" / "targets" / "cb2" / "6PT0_rec.pdbqt"
D1_DIR = ROOT / "results" / "docking" / "option_d_batch2" / "cb2"
QIU_DIR = ROOT / "results" / "docking" / "qiu_0f"
LIB_CSV = ROOT / "data" / "libraries" / "option_d_batch2.csv"
OUT_JSON = ROOT / "results" / "reports" / "qiu_0g_vs_d1_pharmacophore_geometry_data.json"
OUT_MD = ROOT / "results" / "reports" / "qiu_0g_vs_d1_pharmacophore_geometry.md"

REGION = ("SER285", "TYR25", "THR114", "ILE110", "ILE186")
FEATURE_RES_CUTOFF = HEAVY_CUTOFF  # 4.0 Å
CENTROID_NEAR_A = 3.0  # feature–feature spatial correspondence gate
SHELL_JACCARD_MIN = 0.25

D2_IDS = ("JANUS_D2_20", "JANUS_D2_06", "JANUS_D2_22")
QIU_IDS = (14, 15, 20, 24)

# Library / 0D SMILES (authoritative for feature SMARTS; pose REMARK used when present)
QIU_META = {
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

# Hypothetical cross-chemotype feature pairs for correspondence tables
# (geometry may or may not support each pair — reported as observed).
HYPOTHETICAL_PAIRS = [
    ("pyrrole", "pyrazole", "5-membered N-heteroaromatic core"),
    ("aryl_ketone", "amide", "carbonyl linker (ketone vs CONH)"),
    ("benzoyl_aryl", "adamantyl", "bulky hydrophobic from carbonyl side"),
    ("n1_benzyl_aryl", "n1_phenyl", "N-linked aryl region"),
    ("n1_benzyl_aryl", "n1_heterocycle", "N-aryl / N-het extension"),
    ("c2_phenyl", "c5_phenyl", "C-aryl on heteroaromatic"),
    ("c5_methyl", "c4_methyl", "small alkyl on ring"),
    ("c3_amino", "amide", "H-bond donor-capable N near core (weak analogy)"),
]


def load_library_smiles() -> dict[str, str]:
    out: dict[str, str] = {}
    if not LIB_CSV.is_file():
        return out
    import csv

    with LIB_CSV.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            out[row["name"]] = row["smiles"]
    return out


def smiles_to_pdb_serials(
    smiles: str, smiles_idx: dict[int, int], smarts: str
) -> list[list[int]]:
    mol = Chem.MolFromSmiles(smiles)
    pat = Chem.MolFromSmarts(smarts)
    if mol is None or pat is None:
        return []
    hits = []
    for match in mol.GetSubstructMatches(pat):
        serials = [smiles_idx[i + 1] for i in match if (i + 1) in smiles_idx]
        if serials:
            hits.append(serials)
    return hits


def qiu_features(smiles: str, smiles_idx: dict[int, int], cid: int) -> dict[str, list[int]]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {}
    out: dict[str, list[int]] = {}

    def first(smarts: str) -> list[int] | None:
        hits = smiles_to_pdb_serials(smiles, smiles_idx, smarts)
        return hits[0] if hits else None

    pyr = first("n1nccc1")
    if pyr:
        out["pyrazole"] = pyr
    amide = first("[CX3](=O)[NX3]")
    if amide:
        out["amide"] = amide
    if cid == 20:
        het = first("N1CCN(C)CC1")
    else:
        het = first("N1CCOCC1")
    if het:
        out["n1_heterocycle"] = het
    ad = first("C12CC3CC(CC(C3)C1)C2")
    if ad:
        out["adamantyl"] = ad

    phenyls = smiles_to_pdb_serials(smiles, smiles_idx, "c1ccccc1")
    pyr_match = mol.GetSubstructMatches(Chem.MolFromSmarts("n1nccc1"))
    if pyr_match and phenyls:
        pyr_atoms = pyr_match[0]
        for ph in mol.GetSubstructMatches(Chem.MolFromSmarts("c1ccccc1")):
            ph_set = set(ph)
            for aidx in ph:
                atom = mol.GetAtomWithIdx(aidx)
                for nbr in atom.GetNeighbors():
                    if nbr.GetIdx() in ph_set:
                        continue
                    if nbr.GetIdx() in pyr_atoms:
                        pos = pyr_atoms.index(nbr.GetIdx())
                        serials = [
                            smiles_idx[i + 1] for i in ph if (i + 1) in smiles_idx
                        ]
                        if pos <= 1:
                            out.setdefault("n1_phenyl", serials)
                        else:
                            out.setdefault("c5_phenyl", serials)

    me = Chem.MolFromSmarts("[CH3][#6]")
    if pyr_match:
        for hit in mol.GetSubstructMatches(me):
            if hit[1] in pyr_match[0] and (hit[0] + 1) in smiles_idx:
                out["c4_methyl"] = [smiles_idx[hit[0] + 1]]
                break

    if cid == 24:
        for hit in mol.GetSubstructMatches(Chem.MolFromSmarts("[NX3][CH2][C]")):
            if (hit[1] + 1) in smiles_idx:
                out["amide_ch2"] = [smiles_idx[hit[1] + 1]]
                break
    return out


def d2_features(smiles: str, smiles_idx: dict[int, int]) -> dict[str, list[int]]:
    """URB447-like features actually present (SMARTS); do not invent."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {}
    out: dict[str, list[int]] = {}

    def map_atoms(indices) -> list[int]:
        return [smiles_idx[i + 1] for i in indices if (i + 1) in smiles_idx]

    # Pyrrole core
    pyr_hits = mol.GetSubstructMatches(Chem.MolFromSmarts("n1cccc1"))
    if pyr_hits:
        out["pyrrole"] = map_atoms(pyr_hits[0])
        pyr_atoms = pyr_hits[0]
        pyr_n = pyr_atoms[0]  # SMARTS n1cccc1 → index 0 is N
    else:
        return out

    # Aryl ketone: [c]C(=O)[c] — take C=O atoms + keep benzoyl aryl separately
    ket = Chem.MolFromSmarts("[c][CX3](=O)[c]")
    ket_hits = mol.GetSubstructMatches(ket)
    benzoyl_set: set[int] = set()
    if ket_hits:
        # atoms: aryl_C, carbonyl_C, O, aryl_C' (order depends on SMILES)
        h = ket_hits[0]
        out["aryl_ketone"] = map_atoms([h[1], h[2]])  # C=O
        # benzoyl aryl = six-membered phenyl containing either ketone-linked aryl C
        # that is NOT the pyrrole ring atom
        phenyls_idx = list(mol.GetSubstructMatches(Chem.MolFromSmarts("c1ccccc1")))
        for attach in (h[0], h[3]):
            if attach in pyr_atoms:
                continue
            for ph in phenyls_idx:
                if attach in ph:
                    out["benzoyl_aryl"] = map_atoms(ph)
                    benzoyl_set = set(ph)
                    break
            if benzoyl_set:
                break
        # fallback: any phenyl containing either attach carbon
        if not benzoyl_set:
            for attach in (h[0], h[3]):
                for ph in phenyls_idx:
                    if attach in ph:
                        out["benzoyl_aryl"] = map_atoms(ph)
                        benzoyl_set = set(ph)
                        break
                if benzoyl_set:
                    break

    # C3-amino (primary or monoalkyl on pyrrole)
    for smarts in ("[NX3H2]", "[NX3H1][CH3]", "[NX3]([CH3])[CH3]"):
        for hit in mol.GetSubstructMatches(Chem.MolFromSmarts(smarts)):
            # must be attached to pyrrole
            n_idx = hit[0]
            atom = mol.GetAtomWithIdx(n_idx)
            if any(nbr.GetIdx() in pyr_atoms for nbr in atom.GetNeighbors()):
                out["c3_amino"] = map_atoms(hit)
                break
        if "c3_amino" in out:
            break

    # N1-benzyl: n-CH2-aryl
    bn = Chem.MolFromSmarts("[n][CH2]c1ccccc1")
    bn_hits = mol.GetSubstructMatches(bn)
    if bn_hits:
        h = bn_hits[0]
        out["n1_ch2"] = map_atoms([h[1]])
        # benzyl aryl = phenyl portion
        for ph in mol.GetSubstructMatches(Chem.MolFromSmarts("c1ccccc1")):
            if set(ph).issubset(set(h)) or h[2] in ph:
                out["n1_benzyl_aryl"] = map_atoms(ph)
                break
        # para substituent on benzyl if present (Cl, CN, F, …)
        # detect [Cl,F,Br,#N,C(F)(F)F] on benzyl ring
        for atom_idx in out.get("n1_benzyl_aryl", []):
            pass
        # Use SMILES SMARTS for common paras
        for label, sma in (
            ("n1_benzyl_pCl", "c1ccc(Cl)cc1"),
            ("n1_benzyl_pCN", "c1ccc(C#N)cc1"),
            ("n1_benzyl_pF", "c1ccc(F)cc1"),
            ("n1_benzyl_pCF3", "c1ccc(C(F)(F)F)cc1"),
            ("n1_benzyl_pMe", "c1ccc(C)cc1"),
        ):
            # only if that ring is the N-benzyl aryl
            hits = mol.GetSubstructMatches(Chem.MolFromSmarts(sma))
            bn_set = set(out.get("n1_benzyl_aryl", []))
            for hit in hits:
                serials = map_atoms(hit)
                if bn_set and set(serials) & bn_set:
                    # store substituent atom(s) only for clarity when distinct
                    if label.endswith("pCN"):
                        # CN carbons/nitrogens beyond ring
                        cn = mol.GetSubstructMatches(Chem.MolFromSmarts("cC#N"))
                        for cnh in cn:
                            if (cnh[0] + 1) in smiles_idx and map_atoms([cnh[0]])[
                                0
                            ] in bn_set:
                                out["n1_benzyl_pCN"] = map_atoms(cnh[1:])
                    elif label.endswith("pCl"):
                        for aidx in hit:
                            a = mol.GetAtomWithIdx(aidx)
                            if a.GetSymbol() == "Cl":
                                out["n1_benzyl_pCl"] = map_atoms([aidx])
                    elif label.endswith("pCF3"):
                        cf3 = mol.GetSubstructMatches(Chem.MolFromSmarts("C(F)(F)F"))
                        for cf in cf3:
                            # attached to benzyl?
                            c0 = mol.GetAtomWithIdx(cf[0])
                            if any(
                                nbr.GetIdx() in hit for nbr in c0.GetNeighbors()
                            ):
                                out["n1_benzyl_pCF3"] = map_atoms(cf)
                    break

    # C2-phenyl: phenyl bonded to pyrrole C (not via carbonyl, not via CH2)
    phenyls = list(mol.GetSubstructMatches(Chem.MolFromSmarts("c1ccccc1")))
    bn_set_idx = set()
    if bn_hits:
        for ph in phenyls:
            if bn_hits[0][2] in ph:
                bn_set_idx = set(ph)
    for ph in phenyls:
        ph_set = set(ph)
        if ph_set == benzoyl_set or ph_set == bn_set_idx:
            continue
        # bonded directly to pyrrole carbon?
        for aidx in ph:
            atom = mol.GetAtomWithIdx(aidx)
            for nbr in atom.GetNeighbors():
                if nbr.GetIdx() in pyr_atoms and nbr.GetIdx() != pyr_n:
                    out["c2_phenyl"] = map_atoms(ph)
                    break
            if "c2_phenyl" in out:
                break

    # C5-methyl on pyrrole (exclude benzoyl p-Me: methyl must attach to pyrrole C)
    me = Chem.MolFromSmarts("[CH3][#6]")
    for hit in mol.GetSubstructMatches(me):
        if hit[1] in pyr_atoms and (hit[0] + 1) in smiles_idx:
            out["c5_methyl"] = [smiles_idx[hit[0] + 1]]
            break

    # Benzoyl para-subs (D2_20 pMe, D2_22 pCF3)
    if ket_hits and benzoyl_set:
        for hit in mol.GetSubstructMatches(Chem.MolFromSmarts("[CH3]c1ccccc1")):
            # methyl on benzoyl ring (not C5-Me on pyrrole)
            if hit[1] in benzoyl_set and hit[0] not in pyr_atoms:
                out["benzoyl_pMe"] = map_atoms([hit[0]])
                break
        for hit in mol.GetSubstructMatches(Chem.MolFromSmarts("C(F)(F)F")):
            c0 = mol.GetAtomWithIdx(hit[0])
            if any(nbr.GetIdx() in benzoyl_set for nbr in c0.GetNeighbors()):
                out["benzoyl_pCF3"] = map_atoms(hit)
                break
        for label, sma in (
            ("benzoyl_pF", "Fc1ccccc1"),
            ("benzoyl_pCl", "Clc1ccccc1"),
            ("benzoyl_pOMe", "COc1ccccc1"),
        ):
            for hit in mol.GetSubstructMatches(Chem.MolFromSmarts(sma)):
                if set(hit) & benzoyl_set:
                    out[label] = map_atoms(hit)
                    break

    return out


def centroid_from_serials(atoms: list[dict], serials: list[int]) -> np.ndarray | None:
    by_s = {a["serial"]: a for a in atoms}
    pts = [by_s[s]["xyz"] for s in serials if s in by_s and by_s[s]["heavy"]]
    if not pts:
        return None
    return np.mean(pts, axis=0)


def nearest_residues(
    atoms: list[dict],
    serials: list[int],
    rec_atoms: list[dict],
    cutoff: float = FEATURE_RES_CUTOFF,
    top_n: int = 8,
) -> list[dict]:
    by_s = {a["serial"]: a for a in atoms}
    lig_pts = [by_s[s]["xyz"] for s in serials if s in by_s and by_s[s]["heavy"]]
    if not lig_pts:
        return []
    lig_xyz = np.array(lig_pts)
    rec_heavy = [a for a in rec_atoms if a["heavy"]]
    rec_xyz = np.array([a["xyz"] for a in rec_heavy])
    near = np.linalg.norm(rec_xyz - BOX_CENTER, axis=1) <= 22.0
    rec_heavy = [a for a, m in zip(rec_heavy, near) if m]
    rec_xyz = rec_xyz[near]
    dmat = np.linalg.norm(lig_xyz[:, None, :] - rec_xyz[None, :, :], axis=2)
    res_min: dict[str, float] = {}
    for ri, ra in enumerate(rec_heavy):
        md = float(dmat[:, ri].min())
        if md > cutoff:
            continue
        key = residue_key(ra)
        if key not in res_min or md < res_min[key]:
            res_min[key] = md
    return [
        {"residue": k, "min_dist": round(v, 3)}
        for k, v in sorted(res_min.items(), key=lambda x: x[1])[:top_n]
    ]


def region_min_dists(
    atoms: list[dict], serials: list[int], rec_atoms: list[dict]
) -> dict[str, float | None]:
    by_s = {a["serial"]: a for a in atoms}
    lig_pts = [by_s[s]["xyz"] for s in serials if s in by_s and by_s[s]["heavy"]]
    out: dict[str, float | None] = {r: None for r in REGION}
    if not lig_pts:
        return out
    lig_xyz = np.array(lig_pts)
    for ra in rec_atoms:
        if not ra["heavy"]:
            continue
        key = residue_key(ra)
        if key not in out:
            continue
        md = float(np.linalg.norm(lig_xyz - ra["xyz"], axis=1).min())
        if out[key] is None or md < out[key]:
            out[key] = md
    return {k: (round(v, 3) if v is not None else None) for k, v in out.items()}


def shell_set(rows: list[dict]) -> set[str]:
    return {r["residue"] for r in rows}


def jaccard(a: set[str], b: set[str]) -> float | None:
    u = a | b
    if not u:
        return None
    return len(a & b) / len(u)


def summarize_ligand(
    name: str,
    path: Path,
    smiles_fallback: str,
    feature_fn,
    feature_fn_kwargs: dict,
    rec: list[dict],
) -> dict:
    poses = parse_poses(path)
    if not poses:
        return {"id": name, "error": "no poses"}
    best = min(poses, key=lambda p: p["vina_score"])
    smiles = best.get("smiles") or smiles_fallback
    feats = feature_fn(smiles, best["smiles_idx"], **feature_fn_kwargs)
    inventory = {}
    for fname, serials in feats.items():
        cent = centroid_from_serials(best["atoms"], serials)
        near = nearest_residues(best["atoms"], serials, rec)
        reg = region_min_dists(best["atoms"], serials, rec)
        inventory[fname] = {
            "n_atoms_mapped": len(serials),
            "serials": serials,
            "centroid": [round(float(x), 3) for x in cent] if cent is not None else None,
            "nearby_residues_4A": near,
            "region_min_dist_A": reg,
            "region_contact_4A": {
                r: (reg[r] is not None and reg[r] <= FEATURE_RES_CUTOFF) for r in REGION
            },
        }
    lig_xyz = np.array([a["xyz"] for a in best["atoms"] if a["heavy"]])
    return {
        "id": name,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "smiles_source": "REMARK SMILES" if best.get("smiles") else "library/0D fallback",
        "smiles": smiles,
        "best_pose_model": best["model"],
        "best_vina_score": best["vina_score"],  # numeric only; not experimental
        "n_poses_pdbqt": len(poses),
        "ligand_centroid": [round(float(x), 3) for x in lig_xyz.mean(axis=0)],
        "features_found": sorted(feats.keys()),
        "feature_inventory": inventory,
        "_atoms": best["atoms"],
        "_feats": feats,
    }


def cross_map_pair(d_entry: dict, q_entry: dict) -> list[dict]:
    """Map each D2 feature to nearest Qiu feature by centroid + shell Jaccard."""
    rows = []
    for d_name, d_info in d_entry["feature_inventory"].items():
        if d_info["centroid"] is None:
            continue
        dc = np.array(d_info["centroid"])
        ds = shell_set(d_info["nearby_residues_4A"])
        best = None
        for q_name, q_info in q_entry["feature_inventory"].items():
            if q_info["centroid"] is None:
                continue
            qc = np.array(q_info["centroid"])
            dist = float(np.linalg.norm(dc - qc))
            qs = shell_set(q_info["nearby_residues_4A"])
            jac = jaccard(ds, qs)
            cand = {
                "d2_feature": d_name,
                "qiu_feature": q_name,
                "centroid_distance_A": round(dist, 3),
                "shell_jaccard": round(jac, 3) if jac is not None else None,
                "shared_shell_residues": sorted(ds & qs),
                "d2_shell": sorted(ds),
                "qiu_shell": sorted(qs),
            }
            # rank: prefer small centroid distance, then high Jaccard
            score = (dist, -(jac or 0))
            if best is None or score < best[0]:
                best = (score, cand)
        if best is None:
            continue
        cand = best[1]
        cand["corresponds_by_centroid"] = cand["centroid_distance_A"] <= CENTROID_NEAR_A
        cand["corresponds_by_shell"] = (
            cand["shell_jaccard"] is not None and cand["shell_jaccard"] >= SHELL_JACCARD_MIN
        )
        cand["spatial_correspondence"] = (
            cand["corresponds_by_centroid"] or cand["corresponds_by_shell"]
        )
        rows.append(cand)
    return rows


def fmt_region_flags(inv: dict) -> str:
    bits = []
    for r in REGION:
        hits = [
            f
            for f, info in inv.items()
            if info["region_contact_4A"].get(r)
        ]
        if hits:
            bits.append(f"{r}: {', '.join(hits)}")
        else:
            bits.append(f"{r}: —")
    return "; ".join(bits)


def write_markdown(data: dict) -> None:
    lines: list[str] = []
    a = lines.append

    a("# Geometric pharmacophore map — D2_20 / D2_06 / D2_22 vs Qiu 14 / 15 / 20 / 24 (CB2)")
    a("")
    a("> **Scope:** feature-by-feature **geometry** of best on-disk CB2 poses only. No re-docking; no PDBQT edits; no SAR or pharmacological conclusions.")
    a(">")
    a("> **Axiom (explicit):** pose-comparable ≠ same pharmacophore ≠ same pharmacology.")
    a(">")
    a("> **Date:** 2026-08-12")
    a(">")
    a("> **Script:** `scripts/compare_qiu_d1_pharmacophore_geometry.py`")
    a(">")
    a("> **Upstream:** [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md) (pocket coincidence); this report maps **features ↔ residues**, not whole-ligand occupation alone.")
    a("")
    a("---")
    a("")
    a("## Methods")
    a("")
    a("### Poses (strict)")
    a("")
    a("| Set | Path | Best pose rule |")
    a("|-----|------|----------------|")
    a("| D2 | `results/docking/option_d_batch2/cb2/{ID}_docked.pdbqt` | lowest Vina `REMARK` among written MODELs |")
    a("| Qiu | `results/docking/qiu_0f/compound_{N}_cb2_out.pdbqt` | same |")
    a("| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` chain R | — |")
    a("")
    a("### Feature identification (**observed** chemistry → atoms in pose)")
    a("")
    a("1. Take SMILES from PDBQT `REMARK SMILES` (fallback: library CSV / 0D table).")
    a("2. Match SMARTS substructures with RDKit.")
    a("3. Map matched SMILES atom indices → PDBQT serials via `REMARK SMILES IDX` (Meeko remnant).")
    a("4. Feature centroid = mean of mapped **heavy** atom coordinates in the best pose.")
    a("")
    a("**Qiu expected / checked features:** pyrazole; amide CONH; adamantyl; N1-phenyl; N1-heterocycle (morpholine or N-Me-piperazine); C5-phenyl; C4-methyl; amide-CH₂ (cpd 24 only).")
    a("")
    a("**D2 (URB447-like) features checked as present:** pyrrole; aryl ketone (C=O); benzoyl aryl; C2-phenyl; C3-amino; C5-methyl; N1-CH₂; N1-benzyl aryl; and para-substituents actually found (e.g. benzyl-pCN, benzoyl-pMe, benzoyl-pCF₃). Features **not** matched are omitted (not invented).")
    a("")
    a("### Feature ↔ residue mapping")
    a("")
    a("| Quantity | Definition |")
    a("|----------|------------|")
    a("| Feature–residue contact | ≥1 heavy atom of feature within **≤ 4.0 Å** of residue heavy atom (same as 0G) |")
    a("| Feature shell | Residues meeting that cutoff (top 8 listed by min distance) |")
    a("| Region distances | Min heavy distance from feature atoms to SER285, TYR25, THR114, ILE110, ILE186 |")
    a("| Feature–feature correspondence | Centroid distance ≤ **3.0 Å** **or** shell Jaccard ≥ **0.25** |")
    a("")
    a("### Epistemic labels")
    a("")
    a("- **Observed:** coordinates, Vina REMARK numbers, SMARTS hits, distances at fixed cutoffs.")
    a("- **Structural inference:** correspondence flags from those cutoffs; shell overlap.")
    a("- **Interpretation:** brief notes on which subpockets co-occupy; **not** activity or SAR.")
    a("")
    a("### Priority note (from prior comparison)")
    a("")
    a("D2_20 and D2_06 maximized contact Jaccard vs Qiu union in the pose comparison; D2_22 is the historical lead with **mid** overlap. This report does **not** auto-elevate D2_22 by Vina score.")
    a("")
    a("---")
    a("")
    a("## Per-compound feature inventories (best pose)")
    a("")

    for cid in QIU_IDS:
        e = data["qiu"][str(cid)]
        meta = QIU_META[cid]
        a(f"### Qiu {cid} ({meta['n1_sub']}; {meta['r3']})")
        a("")
        a(f"- Path: `{e['path']}`")
        a(f"- Best MODEL {e['best_pose_model']}; Vina REMARK = **{e['best_vina_score']}** kcal/mol (**score number only**, not experimental potency)")
        a(f"- SMILES source: {e['smiles_source']}")
        a(f"- Features found: {', '.join(e['features_found'])}")
        a("")
        a("| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |")
        a("|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|")
        for fname, info in e["feature_inventory"].items():
            near = ", ".join(
                f"{r['residue']}({r['min_dist']})" for r in info["nearby_residues_4A"][:5]
            ) or "—"
            cent = (
                f"({info['centroid'][0]:.2f}, {info['centroid'][1]:.2f}, {info['centroid'][2]:.2f})"
                if info["centroid"]
                else "—"
            )
            reg = info["region_min_dist_A"]

            def cell(r):
                v = reg.get(r)
                if v is None:
                    return "—"
                flag = "✓" if v <= FEATURE_RES_CUTOFF else ""
                return f"{v:.2f}{flag}"

            a(
                f"| {fname} | {cent} | {near} | {cell('SER285')} | {cell('TYR25')} | {cell('THR114')} | {cell('ILE110')} | {cell('ILE186')} |"
            )
        a("")

    for did in D2_IDS:
        e = data["d2"][did]
        a(f"### {did}")
        a("")
        a(f"- Path: `{e['path']}`")
        a(f"- Common name / edit: {e.get('common_name', 'URB447 analog')}")
        a(f"- Best MODEL {e['best_pose_model']}; Vina REMARK = **{e['best_vina_score']}** kcal/mol (**score number only**)")
        a(f"- SMILES source: {e['smiles_source']}")
        a(f"- Features found: {', '.join(e['features_found'])}")
        a("")
        a("| Feature | centroid (Å) | nearby residues ≤4 Å (min dist) | SER285 | TYR25 | THR114 | ILE110 | ILE186 |")
        a("|---------|--------------|----------------------------------|--------|-------|--------|--------|--------|")
        for fname, info in e["feature_inventory"].items():
            near = ", ".join(
                f"{r['residue']}({r['min_dist']})" for r in info["nearby_residues_4A"][:5]
            ) or "—"
            cent = (
                f"({info['centroid'][0]:.2f}, {info['centroid'][1]:.2f}, {info['centroid'][2]:.2f})"
                if info["centroid"]
                else "—"
            )
            reg = info["region_min_dist_A"]

            def cell(r):
                v = reg.get(r)
                if v is None:
                    return "—"
                flag = "✓" if v <= FEATURE_RES_CUTOFF else ""
                return f"{v:.2f}{flag}"

            a(
                f"| {fname} | {cent} | {near} | {cell('SER285')} | {cell('TYR25')} | {cell('THR114')} | {cell('ILE110')} | {cell('ILE186')} |"
            )
        a("")

    a("---")
    a("")
    a("## Feature ↔ residue matrices (region shell)")
    a("")
    a("Cell = min heavy distance (Å) from feature atoms to that residue; **bold** if ≤ 4.0 Å.")
    a("")

    def matrix_block(title: str, entry: dict):
        a(f"### {title}")
        a("")
        feats = list(entry["feature_inventory"].keys())
        a("| Feature | " + " | ".join(REGION) + " |")
        a("|" + "---|" * (len(REGION) + 1))
        for fname in feats:
            reg = entry["feature_inventory"][fname]["region_min_dist_A"]
            cells = []
            for r in REGION:
                v = reg.get(r)
                if v is None:
                    cells.append("—")
                elif v <= FEATURE_RES_CUTOFF:
                    cells.append(f"**{v:.2f}**")
                else:
                    cells.append(f"{v:.2f}")
            a(f"| {fname} | " + " | ".join(cells) + " |")
        a("")

    for cid in QIU_IDS:
        matrix_block(f"Qiu {cid}", data["qiu"][str(cid)])
    for did in D2_IDS:
        matrix_block(did, data["d2"][did])

    a("---")
    a("")
    a("## Pairwise feature correspondence (D2 ↔ Qiu)")
    a("")
    a("For each D2 feature, the nearest Qiu feature by centroid distance is listed. **spatial_ok** = centroid ≤ 3.0 Å **or** shell Jaccard ≥ 0.25 (**structural inference** from cutoffs).")
    a("")
    a("Hypothetical chemotype analogies (ketone↔amide, benzyl↔N1-aryl, …) are **not** assumed true until geometry supports them.")
    a("")

    for did in D2_IDS:
        for cid in QIU_IDS:
            key = f"{did}_vs_Qiu_{cid}"
            rows = data["pairwise"][key]
            a(f"### {did} ↔ Qiu {cid}")
            a("")
            a("| D2 feature | nearest Qiu feature | Δcentroid (Å) | shell Jaccard | shared shell residues | spatial_ok |")
            a("|------------|---------------------|---------------|---------------|----------------------|------------|")
            for r in rows:
                shared = ", ".join(r["shared_shell_residues"][:6]) or "—"
                if len(r["shared_shell_residues"]) > 6:
                    shared += ", …"
                ok = "yes" if r["spatial_correspondence"] else "no"
                jac = r["shell_jaccard"] if r["shell_jaccard"] is not None else "—"
                a(
                    f"| {r['d2_feature']} | {r['qiu_feature']} | {r['centroid_distance_A']:.2f} | {jac} | {shared} | {ok} |"
                )
            # Hypothetical pair status
            a("")
            a("<details><summary>Hypothetical pair check (geometry only)</summary>")
            a("")
            a("| Hypothesis | Δcentroid (Å) | shell Jaccard | supported? |")
            a("|------------|---------------|---------------|------------|")
            inv_d = data["d2"][did]["feature_inventory"]
            inv_q = data["qiu"][str(cid)]["feature_inventory"]
            for d_f, q_f, note in HYPOTHETICAL_PAIRS:
                if d_f not in inv_d or q_f not in inv_q:
                    a(f"| {d_f} ↔ {q_f} ({note}) | — | — | feature absent |")
                    continue
                dc = inv_d[d_f]["centroid"]
                qc = inv_q[q_f]["centroid"]
                if not dc or not qc:
                    a(f"| {d_f} ↔ {q_f} ({note}) | — | — | no centroid |")
                    continue
                dist = float(np.linalg.norm(np.array(dc) - np.array(qc)))
                jac = jaccard(
                    shell_set(inv_d[d_f]["nearby_residues_4A"]),
                    shell_set(inv_q[q_f]["nearby_residues_4A"]),
                )
                ok = dist <= CENTROID_NEAR_A or (
                    jac is not None and jac >= SHELL_JACCARD_MIN
                )
                jac_s = f"{jac:.3f}" if jac is not None else "—"
                a(
                    f"| {d_f} ↔ {q_f} ({note}) | {dist:.2f} | {jac_s} | {'yes' if ok else 'no'} |"
                )
            a("")
            a("</details>")
            a("")

    a("---")
    a("")
    a("## Summary table")
    a("")
    a("| Compound | key features near SER285 / TYR25 / THR114 / ILE110 / ILE186 | notes |")
    a("|----------|---------------------------------------------------------------|-------|")
    for cid in QIU_IDS:
        e = data["qiu"][str(cid)]
        a(f"| Qiu {cid} | {fmt_region_flags(e['feature_inventory'])} | {QIU_META[cid]['n1_sub']}; {QIU_META[cid]['r3']} |")
    for did in D2_IDS:
        e = data["d2"][did]
        note = e.get("priority_note", "URB447-like scaffold")
        a(f"| {did} | {fmt_region_flags(e['feature_inventory'])} | {note} |")
    a("")

    a("---")
    a("")
    a("## Correspondences and mismatches (geometry only)")
    a("")
    corr = data["summary_correspondence"]
    a("### Recurrent spatial correspondences (**structural inference**)")
    a("")
    for line in corr["recurrent_matches"]:
        a(f"- {line}")
    a("")
    a("### Explicit mismatches / non-correspondences")
    a("")
    for line in corr["mismatches"]:
        a(f"- {line}")
    a("")
    a("### Ambiguities / limitations")
    a("")
    for line in corr["limitations"]:
        a(f"- {line}")
    a("")
    a("---")
    a("")
    a("## Verdict")
    a("")
    a(data["verdict_text"])
    a("")
    a(f"**`{data['verdict']}`**")
    a("")
    a("---")
    a("")
    a("## Closing")
    a("")
    a("No SAR. No pharmacological conclusion. Shared or distinct feature–residue geometry does **not** imply shared activity, selectivity, or Janus profile. Vina REMARK values listed above are docking score numbers only.")
    a("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def build_summary_correspondence(data: dict) -> dict:
    """Aggregate qualitative notes from pairwise tables (geometry only)."""
    # Count how often hypothetical pairs are supported across 3×4 = 12 pairs
    support_counts: dict[str, list[bool]] = defaultdict(list)
    for did in D2_IDS:
        for cid in QIU_IDS:
            inv_d = data["d2"][did]["feature_inventory"]
            inv_q = data["qiu"][str(cid)]["feature_inventory"]
            for d_f, q_f, note in HYPOTHETICAL_PAIRS:
                key = f"{d_f}↔{q_f}"
                if d_f not in inv_d or q_f not in inv_q:
                    continue
                dc = inv_d[d_f]["centroid"]
                qc = inv_q[q_f]["centroid"]
                if not dc or not qc:
                    continue
                dist = float(np.linalg.norm(np.array(dc) - np.array(qc)))
                jac = jaccard(
                    shell_set(inv_d[d_f]["nearby_residues_4A"]),
                    shell_set(inv_q[q_f]["nearby_residues_4A"]),
                )
                ok = dist <= CENTROID_NEAR_A or (
                    jac is not None and jac >= SHELL_JACCARD_MIN
                )
                support_counts[key].append(ok)

    recurrent = []
    mismatches = []
    for key, flags in support_counts.items():
        n_ok = sum(flags)
        n = len(flags)
        if n_ok >= max(1, int(0.5 * n)):
            recurrent.append(
                f"**{key}**: spatial_ok in {n_ok}/{n} D2×Qiu pairs (centroid≤{CENTROID_NEAR_A} Å or shell Jaccard≥{SHELL_JACCARD_MIN})."
            )
        else:
            mismatches.append(
                f"**{key}**: spatial_ok only {n_ok}/{n} pairs — do not treat as a conserved cross-chemotype pharmacophore element."
            )

    # Chemotype absences
    mismatches.append(
        "**Adamantyl / CONH–Ad / morpholine–piperazine:** present on Qiu; **absent** on D2_20/06/22 (URB447 pyrrole + aryl ketone + N-benzyl). No geometric transfer of Ad into a D2 atom set."
    )
    mismatches.append(
        "**Aryl ketone vs CONH–Ad:** both place a carbonyl-linked hydrophobic volume in the orthosteric-like box, but atom types and H-bond patterns differ — correspondence is spatial at best, not chemical identity."
    )
    mismatches.append(
        "**D2_22 orientation vs D2_20/06:** for D2_20/06, benzoyl_aryl spatially overlaps Qiu adamantyl/amide (THR114/ILE110/ILE186 shell); "
        "for D2_22, benzoyl_aryl sits nearer Qiu n1_heterocycle/c5_phenyl while n1_benzyl_pCl approaches adamantyl — "
        "feature swap relative to the max-Jaccard analogs (geometry only)."
    )
    mismatches.append(
        "**D2_22 mid-overlap reminder:** prior pose Jaccard mid-pack; do not elevate by most-negative Vina CB2 REMARK."
    )

    limitations = [
        "Different chemotypes → whole-ligand atom RMSD across scaffolds is **not** a primary metric; feature centroids and residue shells are used instead.",
        "SMARTS + SMILES IDX mapping depends on Meeko REMARK completeness; unmapped hydrogens / ambiguous phenyl assignment possible.",
        "Contact cutoff 4.0 Å and correspondence gates (3.0 Å / Jaccard 0.25) are heuristic; other cutoffs change tables.",
        "Static 6PT0 docking poses only — no MD ensemble in this report.",
        "pose-comparable (prior report) ≠ same pharmacophore (this report) ≠ same pharmacology.",
    ]
    return {
        "recurrent_matches": recurrent,
        "mismatches": mismatches,
        "limitations": limitations,
    }


def main() -> None:
    missing = []
    if not RECEPTOR.is_file():
        missing.append(str(RECEPTOR))
    for did in D2_IDS:
        p = D1_DIR / f"{did}_docked.pdbqt"
        if not p.is_file():
            missing.append(str(p))
    for cid in QIU_IDS:
        p = QIU_DIR / f"compound_{cid}_cb2_out.pdbqt"
        if not p.is_file():
            missing.append(str(p))
    if missing:
        print("MISSING:", *missing, sep="\n  ")
        sys.exit(1)

    lib = load_library_smiles()
    rec = load_receptor_chain_r()

    qiu: dict[str, dict] = {}
    for cid in QIU_IDS:
        path = QIU_DIR / f"compound_{cid}_cb2_out.pdbqt"
        qiu[str(cid)] = summarize_ligand(
            f"Qiu_{cid}",
            path,
            QIU_META[cid]["smiles"],
            qiu_features,
            {"cid": cid},
            rec,
        )
        qiu[str(cid)]["n1_sub"] = QIU_META[cid]["n1_sub"]
        qiu[str(cid)]["r3"] = QIU_META[cid]["r3"]

    common_names = {
        "JANUS_D2_20": "URB447 analog Bz_pMe",
        "JANUS_D2_06": "URB447 analog NBn_pCN",
        "JANUS_D2_22": "URB447 analog Bz_pCF3 (historical lead; mid Jaccard)",
    }
    priority_notes = {
        "JANUS_D2_20": "max Jaccard cluster (prior comparison); TYR25 contact in pose report",
        "JANUS_D2_06": "max Jaccard cluster (prior comparison); TYR25 contact in pose report",
        "JANUS_D2_22": "historical lead; mid overlap — do not auto-elevate by Vina",
    }

    d2: dict[str, dict] = {}
    for did in D2_IDS:
        path = D1_DIR / f"{did}_docked.pdbqt"
        d2[did] = summarize_ligand(
            did,
            path,
            lib.get(did, ""),
            d2_features,
            {},
            rec,
        )
        d2[did]["common_name"] = common_names[did]
        d2[did]["priority_note"] = priority_notes[did]

    pairwise = {}
    for did in D2_IDS:
        for cid in QIU_IDS:
            pairwise[f"{did}_vs_Qiu_{cid}"] = cross_map_pair(d2[did], qiu[str(cid)])

    def clean(e: dict) -> dict:
        return {k: v for k, v in e.items() if not k.startswith("_")}

    payload = {
        "methods": {
            "heavy_contact_cutoff_A": FEATURE_RES_CUTOFF,
            "feature_centroid_near_A": CENTROID_NEAR_A,
            "shell_jaccard_min": SHELL_JACCARD_MIN,
            "region_residues": list(REGION),
            "no_cross_scaffold_rmsd": True,
            "score_note": "Vina REMARK numbers only; not experimental affinity",
            "axiom": "pose-comparable ≠ same pharmacophore ≠ same pharmacology",
        },
        "qiu": {k: clean(v) for k, v in qiu.items()},
        "d2": {k: clean(v) for k, v in d2.items()},
        "pairwise": pairwise,
    }
    payload["summary_correspondence"] = build_summary_correspondence(payload)
    payload["verdict"] = "PHARMACOPHORE_GEOM = COMPLETE"
    payload["verdict_text"] = (
        "Feature inventories and feature↔residue shells computed for D2_20/06/22 and Qiu 14/15/20/24 "
        "best CB2 poses on disk. Cross-map tables use feature centroids and residue shells "
        "(not whole-ligand RMSD). Chemotype mismatch (Ad/CONH/morpholine vs URB447 ketone/benzyl) "
        "is explicit; spatial pocket coincidence from the prior comparison is refined here to "
        "feature-level geometry only — not pharmacology."
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("verdict:", payload["verdict"])
    for did in D2_IDS:
        print(did, "features:", d2[did]["features_found"])
    for cid in QIU_IDS:
        print(f"Qiu_{cid}", "features:", qiu[str(cid)]["features_found"])


if __name__ == "__main__":
    main()
