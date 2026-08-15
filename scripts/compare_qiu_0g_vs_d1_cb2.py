#!/usr/bin/env python3
"""Geometric CB2 pose comparison: Option D batch2 (D1) vs Qiu 0G (14/15/20/24).

Read-only: uses existing *_docked.pdbqt / *_cb2_out.pdbqt on disk.
No Vina re-run; no PDBQT modification.

Contact cutoffs match scripts/analyze_qiu_0g_poses.py (heavy ≤ 4.0 Å).
Scores are Vina REMARK values only — not experimental affinity.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_qiu_0g_poses import (  # noqa: E402
    BOX_CENTER,
    HEAVY_CUTOFF,
    analyze_contacts,
    load_receptor_chain_r,
    parse_pdbqt_atoms,
    parse_smiles_idx,
    residue_key,
)

RECEPTOR = ROOT / "data" / "targets" / "cb2" / "6PT0_rec.pdbqt"
D1_DIR = ROOT / "results" / "docking" / "option_d_batch2" / "cb2"
QIU_DIR = ROOT / "results" / "docking" / "qiu_0f"
REPORT_JSON = ROOT / "results" / "reports" / "qiu_0g_vs_d1_cb2_pose_comparison_data.json"

QIU_IDS = (14, 15, 20, 24)
# 0G shared contact core + highlighted region residues
REGION_RESIDUES = ("SER285", "TYR25", "THR114", "ILE110", "ILE186")
QIU_CORE_0G = (
    "ILE110",
    "ILE186",
    "LEU191",
    "PHE87",
    "PHE91",
    "PHE94",
    "PHE183",
    "PHE281",
    "PRO184",
    "SER285",
    "THR114",
    "TRP194",
    "VAL113",
)

D1_EXPECTED = (
    [f"JANUS_D2_{i:02d}" for i in range(1, 33)]
    + ["URB447", "GW405833", "delta9-THCV", "delta9-THC"]
)

# Pose-comparable gates (geometry/occupation; not score ranking)
CENTROID_NEAR_CONSENSUS_A = 3.0
JACCARD_VS_CONSENSUS_MIN = 0.40
REGION_SHELL_MIN_HITS = 3  # of 5 highlighted residues


def parse_poses(pdbqt_path: Path) -> list[dict]:
    """Parse MODEL blocks with VINA RESULT (written poses only)."""
    text = pdbqt_path.read_text(encoding="utf-8", errors="replace")
    models: list[dict] = []
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
        # SMILES may be same-line or next line after REMARK SMILES
        smiles = None
        m_smi = re.search(r"REMARK SMILES\s+(\S+)", part)
        if m_smi:
            smiles = m_smi.group(1)
        else:
            m_smi2 = re.search(r"REMARK SMILES\s*\n\s*(\S+)", part)
            if m_smi2:
                smiles = m_smi2.group(1)
        atoms = parse_pdbqt_atoms(part)
        for i, a in enumerate(atoms, start=1):
            a["serial"] = i
        models.append(
            {
                "model": int(m_model.group(1)),
                "vina_score": float(m_vina.group(1)),
                "rmsd_lb": float(m_vina.group(2)),
                "rmsd_ub": float(m_vina.group(3)),
                "smiles": smiles,
                "smiles_idx": parse_smiles_idx(part),
                "atoms": atoms,
            }
        )
    return models


def ligand_heavy_centroid(atoms: list[dict]) -> np.ndarray:
    xyz = np.array([a["xyz"] for a in atoms if a["heavy"]])
    if len(xyz) == 0:
        raise ValueError("no heavy atoms")
    return xyz.mean(axis=0)


def contact_set(contacts: dict) -> set[str]:
    return {r["residue"] for r in contacts["contact_residues"]}


def jaccard(a: set[str], b: set[str]) -> float | None:
    u = a | b
    if not u:
        return None
    return len(a & b) / len(u)


def atom_cloud_overlap(
    atoms_a: list[dict], atoms_b: list[dict], shell_A: float = 2.0
) -> dict:
    """Fraction of heavy atoms in A within shell_A of any heavy atom in B (and vice versa).

    Cross-chemotype whole-ligand RMSD is not used; this is a pocket-occupation proxy.
    """
    a = np.array([x["xyz"] for x in atoms_a if x["heavy"]])
    b = np.array([x["xyz"] for x in atoms_b if x["heavy"]])
    if len(a) == 0 or len(b) == 0:
        return {"frac_a_near_b": None, "frac_b_near_a": None, "mean_frac": None}
    dmat = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2)
    frac_a = float((dmat.min(axis=1) <= shell_A).mean())
    frac_b = float((dmat.min(axis=0) <= shell_A).mean())
    return {
        "shell_A": shell_A,
        "frac_a_near_b": round(frac_a, 3),
        "frac_b_near_a": round(frac_b, 3),
        "mean_frac": round(0.5 * (frac_a + frac_b), 3),
    }


def region_occupation(contacts: set[str]) -> dict:
    hits = [r for r in REGION_RESIDUES if r in contacts]
    return {
        "residues_checked": list(REGION_RESIDUES),
        "hits": hits,
        "n_hits": len(hits),
        "flags": {r: (r in contacts) for r in REGION_RESIDUES},
    }


def moiety_notes(smiles: str | None, compound_id: str) -> dict:
    """Structural moiety presence for orientation notes (observed SMARTS only)."""
    out: dict = {"smiles_available": bool(smiles), "labels": []}
    if not smiles:
        return out
    try:
        from rdkit import Chem
    except ImportError:
        out["note"] = "rdkit unavailable"
        return out
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        out["note"] = "SMILES parse failed"
        return out
    checks = {
        "adamantyl": "C12CC3CC(CC(C3)C1)C2",
        "amide_CONH": "[CX3](=O)[NX3]",
        "ketone_aryl": "[c][CX3](=O)[c]",
        "morpholine": "N1CCOCC1",
        "piperazine": "N1CCNCC1",
        "pyrazole_nn": "n1nccc1",
        "pyrrole_like": "n1cccc1",
        "N_benzyl": "[NX3]Cc1ccccc1",
        "CF3": "C(F)(F)F",
    }
    for name, sma in checks.items():
        pat = Chem.MolFromSmarts(sma)
        if pat is not None and mol.HasSubstructMatch(pat):
            out["labels"].append(name)
    out["compound_id"] = compound_id
    return out


def summarize_compound(
    name: str,
    path: Path,
    rec: list[dict],
) -> dict:
    poses = parse_poses(path)
    if not poses:
        return {"id": name, "path": str(path), "error": "no MODEL/VINA poses"}
    best = min(poses, key=lambda p: p["vina_score"])
    cent = ligand_heavy_centroid(best["atoms"])
    contacts = analyze_contacts(best["atoms"], rec)
    cset = contact_set(contacts)
    return {
        "id": name,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "n_poses_pdbqt": len(poses),
        "pose_scores": [
            {
                "model": p["model"],
                "vina_score": p["vina_score"],
                "rmsd_lb": p["rmsd_lb"],
                "rmsd_ub": p["rmsd_ub"],
            }
            for p in poses
        ],
        "best_pose_model": best["model"],
        "best_vina_score": best["vina_score"],
        "ligand_centroid": [round(float(x), 3) for x in cent],
        "dist_to_box_center_A": round(float(np.linalg.norm(cent - BOX_CENTER)), 3),
        "n_heavy": sum(1 for a in best["atoms"] if a["heavy"]),
        "contacts": contacts,
        "contact_residue_set": sorted(cset),
        "region_0g": region_occupation(cset),
        "qiu_core_overlap": {
            "shared": sorted(cset & set(QIU_CORE_0G)),
            "n_shared": len(cset & set(QIU_CORE_0G)),
            "n_core": len(QIU_CORE_0G),
            "frac_core": round(len(cset & set(QIU_CORE_0G)) / len(QIU_CORE_0G), 3),
        },
        "moiety_labels": moiety_notes(best.get("smiles"), name),
        "_best_atoms": best["atoms"],  # dropped before JSON write
        "_centroid": cent,
        "_cset": cset,
    }


def pose_comparable_flag(
    dist_to_qiu_mean: float,
    jaccard_vs_qiu_union: float | None,
    region_hits: int,
) -> dict:
    """Heuristic geometric classification (documented thresholds)."""
    jac_ok = jaccard_vs_qiu_union is not None and jaccard_vs_qiu_union >= JACCARD_VS_CONSENSUS_MIN
    cent_ok = dist_to_qiu_mean <= CENTROID_NEAR_CONSENSUS_A
    region_ok = region_hits >= REGION_SHELL_MIN_HITS
    if cent_ok and jac_ok:
        label = "pose_comparable"
    elif cent_ok and region_ok:
        label = "pose_partially_comparable"
    elif cent_ok or (jac_ok and region_ok):
        label = "pose_partially_comparable"
    else:
        label = "pose_different"
    return {
        "label": label,
        "centroid_near_qiu_mean": cent_ok,
        "jaccard_ok": jac_ok,
        "region_shell_ok": region_ok,
        "criteria": {
            "centroid_max_A": CENTROID_NEAR_CONSENSUS_A,
            "jaccard_min": JACCARD_VS_CONSENSUS_MIN,
            "region_min_hits": REGION_SHELL_MIN_HITS,
        },
    }


def main() -> None:
    missing = []
    if not RECEPTOR.is_file():
        missing.append(str(RECEPTOR))
    for cid in QIU_IDS:
        p = QIU_DIR / f"compound_{cid}_cb2_out.pdbqt"
        if not p.is_file():
            missing.append(str(p))
    for name in D1_EXPECTED:
        p = D1_DIR / f"{name}_docked.pdbqt"
        if not p.is_file():
            missing.append(str(p))

    inventory = {
        "receptor": str(RECEPTOR.relative_to(ROOT)).replace("\\", "/"),
        "receptor_exists": RECEPTOR.is_file(),
        "d1_dir": str(D1_DIR.relative_to(ROOT)).replace("\\", "/"),
        "qiu_dir": str(QIU_DIR.relative_to(ROOT)).replace("\\", "/"),
        "d1_expected_n": len(D1_EXPECTED),
        "d1_found": [n for n in D1_EXPECTED if (D1_DIR / f"{n}_docked.pdbqt").is_file()],
        "qiu_found": [
            cid
            for cid in QIU_IDS
            if (QIU_DIR / f"compound_{cid}_cb2_out.pdbqt").is_file()
        ],
        "missing": missing,
    }

    if missing:
        out = {
            "verdict": "NEEDS REVIEW",
            "inventory": inventory,
            "error": "missing required files",
        }
        REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
        REPORT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"MISSING FILES → wrote {REPORT_JSON}")
        for m in missing:
            print("  ", m)
        sys.exit(1)

    rec = load_receptor_chain_r()

    qiu: dict[str, dict] = {}
    for cid in QIU_IDS:
        path = QIU_DIR / f"compound_{cid}_cb2_out.pdbqt"
        qiu[str(cid)] = summarize_compound(f"Qiu_{cid}", path, rec)

    d1: dict[str, dict] = {}
    for name in D1_EXPECTED:
        path = D1_DIR / f"{name}_docked.pdbqt"
        d1[name] = summarize_compound(name, path, rec)

    # Qiu consensus pocket (same as 0G mean centroid)
    qiu_cents = np.array([qiu[str(c)]["_centroid"] for c in QIU_IDS])
    qiu_mean = qiu_cents.mean(axis=0)
    qiu_sets = [qiu[str(c)]["_cset"] for c in QIU_IDS]
    qiu_union = set.union(*qiu_sets)
    qiu_intersection = set.intersection(*qiu_sets)

    pairwise = {}
    classifications = {}
    for name, entry in d1.items():
        row = {
            "d1_id": name,
            "best_vina_score": entry["best_vina_score"],  # score-comparable column
            "dist_to_qiu_mean_centroid_A": round(
                float(np.linalg.norm(entry["_centroid"] - qiu_mean)), 3
            ),
            "vs_qiu": {},
        }
        for cid in QIU_IDS:
            q = qiu[str(cid)]
            d_cent = float(np.linalg.norm(entry["_centroid"] - q["_centroid"]))
            jac = jaccard(entry["_cset"], q["_cset"])
            cloud = atom_cloud_overlap(entry["_best_atoms"], q["_best_atoms"], shell_A=2.0)
            row["vs_qiu"][str(cid)] = {
                "centroid_distance_A": round(d_cent, 3),
                "contact_jaccard": round(jac, 3) if jac is not None else None,
                "shared_residues": sorted(entry["_cset"] & q["_cset"]),
                "n_shared": len(entry["_cset"] & q["_cset"]),
                "atom_cloud_overlap_2A": cloud,
            }
        jac_union = jaccard(entry["_cset"], qiu_union)
        jac_inter = jaccard(entry["_cset"], qiu_intersection)
        row["jaccard_vs_qiu_union"] = round(jac_union, 3) if jac_union is not None else None
        row["jaccard_vs_qiu_intersection"] = (
            round(jac_inter, 3) if jac_inter is not None else None
        )
        row["region_0g"] = entry["region_0g"]
        row["qiu_core_frac"] = entry["qiu_core_overlap"]["frac_core"]
        row["pose_class"] = pose_comparable_flag(
            row["dist_to_qiu_mean_centroid_A"],
            jac_union,
            entry["region_0g"]["n_hits"],
        )
        # mean cloud overlap vs four Qiu refs
        clouds = [
            row["vs_qiu"][str(c)]["atom_cloud_overlap_2A"]["mean_frac"]
            for c in QIU_IDS
            if row["vs_qiu"][str(c)]["atom_cloud_overlap_2A"]["mean_frac"] is not None
        ]
        row["mean_atom_cloud_overlap_vs_qiu"] = (
            round(float(np.mean(clouds)), 3) if clouds else None
        )
        pairwise[name] = row
        classifications[name] = row["pose_class"]["label"]

    # Drop non-JSON working fields
    def clean(entry: dict) -> dict:
        return {k: v for k, v in entry.items() if not k.startswith("_")}

    results = {
        "methods": {
            "poses_d1": "results/docking/option_d_batch2/cb2/*_docked.pdbqt MODEL blocks only",
            "poses_qiu": "results/docking/qiu_0f/compound_{14,15,20,24}_cb2_out.pdbqt MODEL blocks only",
            "receptor": str(RECEPTOR.relative_to(ROOT)).replace("\\", "/"),
            "heavy_contact_cutoff_A": HEAVY_CUTOFF,
            "box_center_ref": BOX_CENTER.tolist(),
            "qiu_consensus_centroid": [round(float(x), 3) for x in qiu_mean],
            "qiu_intersection_residues": sorted(qiu_intersection),
            "qiu_union_n": len(qiu_union),
            "atom_cloud_shell_A": 2.0,
            "pose_comparable_criteria": {
                "centroid_to_qiu_mean_max_A": CENTROID_NEAR_CONSENSUS_A,
                "jaccard_vs_qiu_union_min": JACCARD_VS_CONSENSUS_MIN,
                "region_residues": list(REGION_RESIDUES),
                "region_min_hits": REGION_SHELL_MIN_HITS,
            },
            "score_note": "Vina REMARK scores are score-comparable only; never experimental affinity",
            "no_whole_ligand_cross_chemotype_rmsd": True,
        },
        "inventory": inventory,
        "qiu_refs": {k: clean(v) for k, v in qiu.items()},
        "d1_compounds": {k: clean(v) for k, v in d1.items()},
        "pairwise_geometry": pairwise,
        "classification_counts": {
            lab: sum(1 for v in classifications.values() if v == lab)
            for lab in ("pose_comparable", "pose_partially_comparable", "pose_different")
        },
        "classification_by_id": classifications,
        "verdict": "COMPARISON = COMPLETE",
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {REPORT_JSON}")
    print("inventory D1:", len(inventory["d1_found"]), "Qiu:", inventory["qiu_found"])
    print("classification:", results["classification_counts"])
    # Highlight D2_22
    d22 = pairwise["JANUS_D2_22"]
    print(
        "D2_22:",
        d22["pose_class"]["label"],
        "dist_qiu_mean=",
        d22["dist_to_qiu_mean_centroid_A"],
        "jac_union=",
        d22["jaccard_vs_qiu_union"],
        "region=",
        d22["region_0g"]["hits"],
        "vina=",
        d22["best_vina_score"],
    )
    # Top by jaccard then cloud
    ranked = sorted(
        pairwise.values(),
        key=lambda r: (
            r["jaccard_vs_qiu_union"] or 0,
            -(r["dist_to_qiu_mean_centroid_A"] or 99),
            r["mean_atom_cloud_overlap_vs_qiu"] or 0,
        ),
        reverse=True,
    )
    print("Top pose-overlap (by Jaccard vs Qiu union):")
    for r in ranked[:8]:
        print(
            f"  {r['d1_id']}: jac={r['jaccard_vs_qiu_union']} "
            f"d={r['dist_to_qiu_mean_centroid_A']} "
            f"cloud={r['mean_atom_cloud_overlap_vs_qiu']} "
            f"{r['pose_class']['label']}"
        )


if __name__ == "__main__":
    main()
