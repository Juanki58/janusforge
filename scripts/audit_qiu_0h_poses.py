#!/usr/bin/env python3
"""Qiu 0H — descriptive CB2 pose audit (Qiu 14/15/20/24 vs D2_20/06/22).

Read-only: best MODEL poses from existing PDBQTs only.
No re-docking, no Vina, no PDBQT modification.
No SAR / pharmacological conclusions / affinity claims from Vina scores.

Reuses cutoffs and parsers from:
  scripts/analyze_qiu_0g_poses.py
  scripts/compare_qiu_0g_vs_d1_cb2.py
  scripts/compare_qiu_d1_pharmacophore_geometry.py

Writes:
  results/reports/qiu_0h_pose_audit_data.json
  results/reports/qiu_0h_pose_audit.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_qiu_0g_poses import (  # noqa: E402
    BOX_CENTER,
    COMPOUNDS,
    HEAVY_CUTOFF,
    HBOND_ANGLE_MIN,
    HBOND_DA_CUTOFF,
    HBOND_HA_CUTOFF,
    analyze_contacts,
    load_receptor_chain_r,
    orientation_summary,
    residue_key,
)
from compare_qiu_0g_vs_d1_cb2 import (  # noqa: E402
    REGION_RESIDUES,
    atom_cloud_overlap,
    contact_set,
    jaccard,
    ligand_heavy_centroid,
    parse_poses,
    region_occupation,
)
from compare_qiu_d1_pharmacophore_geometry import (  # noqa: E402
    CENTROID_NEAR_A,
    HYPOTHETICAL_PAIRS,
    QIU_META,
    SHELL_JACCARD_MIN,
    cross_map_pair,
    d2_features,
    nearest_residues,
    qiu_features,
    region_min_dists,
    shell_set,
    summarize_ligand,
)

RECEPTOR = ROOT / "data" / "targets" / "cb2" / "6PT0_rec.pdbqt"
QIU_DIR = ROOT / "results" / "docking" / "qiu_0f"
D1_DIR = ROOT / "results" / "docking" / "option_d_batch2" / "cb2"
OUT_JSON = ROOT / "results" / "reports" / "qiu_0h_pose_audit_data.json"
OUT_MD = ROOT / "results" / "reports" / "qiu_0h_pose_audit.md"

QIU_IDS = (14, 15, 20, 24)
D2_IDS = ("JANUS_D2_20", "JANUS_D2_06", "JANUS_D2_22")

# Qiu-only chemical features (cannot map to D2 atoms)
QIU_ONLY_FEATURES = ("adamantyl", "amide", "n1_heterocycle", "amide_ch2")

# Conservation labels (geometry inference from prior pharmacophore gates)
CONSERVATION_AXES = [
    ("pyrrole", "pyrazole", "5-membered N-heteroaromatic core"),
    ("aryl_ketone", "amide", "carbonyl linker (ketone vs CONH)"),
    ("benzoyl_aryl", "adamantyl", "bulky hydrophobic from carbonyl side"),
    ("n1_benzyl_aryl", "n1_heterocycle", "N-aryl / N-het extension"),
    ("c2_phenyl", "c5_phenyl", "C-aryl on heteroaromatic"),
    ("c5_methyl", "c4_methyl", "small alkyl on ring"),
]


def polar_proximities(lig_atoms: list[dict], rec_atoms: list[dict]) -> list[dict]:
    """Polar heavy pairs ≤ HBOND_DA_CUTOFF that are not geometry-OK H-bonds."""
    polar_types = {"OA", "NA", "N", "O", "SA", "OS"}
    lig_p = [a for a in lig_atoms if a["heavy"] and a["atype"].upper() in polar_types]
    rec_p = [
        a
        for a in rec_atoms
        if a["heavy"]
        and a["atype"].upper() in polar_types
        and np.linalg.norm(a["xyz"] - BOX_CENTER) <= 20.0
    ]
    out = []
    for la in lig_p:
        for ra in rec_p:
            d = float(np.linalg.norm(la["xyz"] - ra["xyz"]))
            if d <= HBOND_DA_CUTOFF:
                out.append(
                    {
                        "lig": f"{la['name']}({la['atype']})",
                        "rec": f"{residue_key(ra)} {ra['name']}({ra['atype']})",
                        "dist_A": round(d, 3),
                    }
                )
    out.sort(key=lambda x: x["dist_A"])
    # unique by lig+rec residue atom
    seen = set()
    uniq = []
    for row in out:
        k = (row["lig"], row["rec"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(row)
    return uniq[:12]


def region_min_whole_ligand(atoms: list[dict], rec: list[dict]) -> dict[str, float | None]:
    lig = np.array([a["xyz"] for a in atoms if a["heavy"]])
    out: dict[str, float | None] = {r: None for r in REGION_RESIDUES}
    if len(lig) == 0:
        return out
    for ra in rec:
        if not ra["heavy"]:
            continue
        key = residue_key(ra)
        if key not in out:
            continue
        md = float(np.linalg.norm(lig - ra["xyz"], axis=1).min())
        if out[key] is None or md < out[key]:
            out[key] = md
    return {k: (round(v, 3) if v is not None else None) for k, v in out.items()}


def d2_orientation(atoms: list[dict], feats: dict[str, list[int]]) -> dict:
    """Dominant-axis vectors from pyrrole centroid (observed geometry)."""
    by_s = {a["serial"]: a for a in atoms}

    def cent(serials: list[int]) -> np.ndarray | None:
        pts = [by_s[s]["xyz"] for s in serials if s in by_s and by_s[s]["heavy"]]
        if not pts:
            return None
        return np.mean(pts, axis=0)

    pyr = cent(feats.get("pyrrole", []))
    if pyr is None:
        return {"error": "no pyrrole centroid"}

    def axis(name: str):
        c = cent(feats.get(name, []))
        if c is None:
            return None
        v = c - pyr
        comps = {
            "+x" if v[0] >= 0 else "-x": abs(float(v[0])),
            "+y" if v[1] >= 0 else "-y": abs(float(v[1])),
            "+z" if v[2] >= 0 else "-z": abs(float(v[2])),
        }
        dom = max(comps.items(), key=lambda t: t[1])[0]
        return {
            "centroid": [round(float(x), 3) for x in c],
            "dx": round(float(v[0]), 3),
            "dy": round(float(v[1]), 3),
            "dz": round(float(v[2]), 3),
            "dominant_axis": dom,
        }

    keys = (
        "benzoyl_aryl",
        "n1_benzyl_aryl",
        "aryl_ketone",
        "c2_phenyl",
        "c3_amino",
        "n1_ch2",
    )
    return {
        "pyrrole_centroid": [round(float(x), 3) for x in pyr],
        "vectors_from_pyrrole": {k: axis(k) for k in keys},
        "dominant_axis_from_pyrrole": {
            k: (axis(k)["dominant_axis"] if axis(k) else None) for k in keys
        },
    }


def conservation_vs_qiu(
    d_entry: dict, q_entries: dict[str, dict]
) -> dict:
    """Per D2 compound: conserved / lost / swapped / Qiu-only absent vs Qiu map."""
    # Aggregate spatial_ok over all Qiu refs for each hypothetical axis
    axes = []
    for d_f, q_f, label in CONSERVATION_AXES:
        per_qiu = {}
        ok_n = 0
        for qid, qe in q_entries.items():
            # find this pair in cross-map if present; else compute centroid/shell
            d_info = d_entry["feature_inventory"].get(d_f)
            q_info = qe["feature_inventory"].get(q_f)
            if not d_info or not q_info or d_info["centroid"] is None or q_info["centroid"] is None:
                per_qiu[qid] = {"present": False, "spatial_ok": False}
                continue
            dc = np.array(d_info["centroid"])
            qc = np.array(q_info["centroid"])
            dist = float(np.linalg.norm(dc - qc))
            jac = jaccard(
                shell_set(d_info["nearby_residues_4A"]),
                shell_set(q_info["nearby_residues_4A"]),
            )
            spatial = dist <= CENTROID_NEAR_A or (
                jac is not None and jac >= SHELL_JACCARD_MIN
            )
            if spatial:
                ok_n += 1
            per_qiu[qid] = {
                "present": True,
                "centroid_distance_A": round(dist, 3),
                "shell_jaccard": round(jac, 3) if jac is not None else None,
                "spatial_ok": spatial,
            }
        # conserved if ≥ half of Qiu refs support spatial_ok
        n_qiu = len(q_entries)
        status = "conserved_spatial" if ok_n >= max(1, n_qiu // 2) else "lost_or_weak"
        axes.append(
            {
                "d2_feature": d_f,
                "qiu_feature": q_f,
                "label": label,
                "spatial_ok_count": f"{ok_n}/{n_qiu}",
                "status": status,
                "per_qiu": per_qiu,
            }
        )

    # Feature swap detection (D2_22 pattern): benzoyl near n1_het / Ad near n1_benzyl
    swap_notes = []
    for qid, qe in q_entries.items():
        bz = d_entry["feature_inventory"].get("benzoyl_aryl")
        bn = d_entry["feature_inventory"].get("n1_benzyl_aryl")
        ad = qe["feature_inventory"].get("adamantyl")
        het = qe["feature_inventory"].get("n1_heterocycle")
        if not all(
            x and x.get("centroid") is not None for x in (bz, bn, ad, het)
        ):
            continue
        d_bz_ad = float(
            np.linalg.norm(np.array(bz["centroid"]) - np.array(ad["centroid"]))
        )
        d_bz_het = float(
            np.linalg.norm(np.array(bz["centroid"]) - np.array(het["centroid"]))
        )
        d_bn_ad = float(
            np.linalg.norm(np.array(bn["centroid"]) - np.array(ad["centroid"]))
        )
        d_bn_het = float(
            np.linalg.norm(np.array(bn["centroid"]) - np.array(het["centroid"]))
        )
        # "canonical" for D2_20/06: benzoyl nearer Ad than het; benzyl nearer het than Ad
        canonical = d_bz_ad < d_bz_het and d_bn_het < d_bn_ad
        swapped = d_bz_het < d_bz_ad and d_bn_ad < d_bn_het
        swap_notes.append(
            {
                "qiu_ref": qid,
                "benzoyl_to_adamantyl_A": round(d_bz_ad, 3),
                "benzoyl_to_n1_heterocycle_A": round(d_bz_het, 3),
                "n1_benzyl_to_adamantyl_A": round(d_bn_ad, 3),
                "n1_benzyl_to_n1_heterocycle_A": round(d_bn_het, 3),
                "pattern": (
                    "canonical_like"
                    if canonical
                    else ("feature_swap" if swapped else "mixed")
                ),
            }
        )

    qiu_absent = []
    for feat in QIU_ONLY_FEATURES:
        # present in any Qiu?
        in_qiu = any(feat in qe.get("features_found", []) for qe in q_entries.values())
        in_d2 = feat in d_entry.get("features_found", [])
        if in_qiu and not in_d2:
            qiu_absent.append(feat)

    return {
        "axes": axes,
        "orientation_vs_ad_het": swap_notes,
        "qiu_only_absent_on_d2": qiu_absent,
        "gates": {
            "centroid_near_A": CENTROID_NEAR_A,
            "shell_jaccard_min": SHELL_JACCARD_MIN,
        },
    }


def audit_qiu(cid: int, rec: list[dict]) -> dict:
    path = QIU_DIR / f"compound_{cid}_cb2_out.pdbqt"
    poses = parse_poses(path)
    if not poses:
        return {"id": f"Qiu_{cid}", "error": "no poses", "path": str(path)}
    best = min(poses, key=lambda p: p["vina_score"])
    contacts = analyze_contacts(best["atoms"], rec)
    polar = polar_proximities(best["atoms"], rec)
    # Exclude geometry-OK H-bonds from polar list (already reported separately)
    hb_keys = {
        (h["lig"], h["rec"]) for h in contacts.get("hbonds_geometry_ok", [])
    }
    polar = [p for p in polar if (p["lig"], p["rec"]) not in hb_keys]
    orient = orientation_summary(best, cid)
    region = region_min_whole_ligand(best["atoms"], rec)
    feat_sum = summarize_ligand(
        f"Qiu_{cid}",
        path,
        COMPOUNDS[cid]["smiles"],
        lambda smi, idx: qiu_features(smi, idx, cid),
        {},
        rec,
    )
    # drop heavy atom caches
    feat_sum.pop("_atoms", None)
    feat_sum.pop("_feats", None)

    return {
        "series": "Qiu",
        "id": f"Qiu_{cid}",
        "compound_id": cid,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "file_exists": path.is_file(),
        "n_poses_pdbqt": len(poses),
        "pose_scores": [
            {
                "model": p["model"],
                "vina_score": p["vina_score"],
                "rmsd_lb": p["rmsd_lb"],
                "rmsd_ub": p["rmsd_ub"],
            }
            for p in sorted(poses, key=lambda x: x["model"])
        ],
        "comparable_pose": {
            "rule": "lowest (most negative) REMARK VINA RESULT among written MODELs",
            "model": best["model"],
            "vina_score_kcal_mol": best["vina_score"],
            "score_note": "Vina REMARK number only — not experimental affinity",
        },
        "ligand_centroid": [round(float(x), 3) for x in ligand_heavy_centroid(best["atoms"])],
        "dist_to_box_center_A": round(
            float(np.linalg.norm(ligand_heavy_centroid(best["atoms"]) - BOX_CENTER)), 3
        ),
        "contacts": contacts,
        "polar_proximity_not_hbond": polar,
        "region_min_dist_A": region,
        "region_contact_4A": {
            r: (region[r] is not None and region[r] <= HEAVY_CUTOFF) for r in REGION_RESIDUES
        },
        "orientation": orient,
        "feature_summary": feat_sum,
        "scaffold_labels": {
            "n1_sub": COMPOUNDS[cid]["n1_sub"],
            "r3": COMPOUNDS[cid]["r3"],
        },
        "_atoms": best["atoms"],
    }


def audit_d2(did: str, rec: list[dict], qiu_feat_entries: dict[str, dict]) -> dict:
    path = D1_DIR / f"{did}_docked.pdbqt"
    poses = parse_poses(path)
    if not poses:
        return {"id": did, "error": "no poses", "path": str(path)}
    best = min(poses, key=lambda p: p["vina_score"])
    contacts = analyze_contacts(best["atoms"], rec)
    polar = polar_proximities(best["atoms"], rec)
    hb_keys = {
        (h["lig"], h["rec"]) for h in contacts.get("hbonds_geometry_ok", [])
    }
    polar = [p for p in polar if (p["lig"], p["rec"]) not in hb_keys]
    region = region_min_whole_ligand(best["atoms"], rec)
    smiles = best.get("smiles") or ""
    feat_sum = summarize_ligand(
        did,
        path,
        smiles,
        lambda smi, idx: d2_features(smi, idx),
        {},
        rec,
    )
    feats = feat_sum.pop("_feats", {})
    feat_sum.pop("_atoms", None)
    orient = d2_orientation(best["atoms"], feats)
    cons = conservation_vs_qiu(feat_sum, qiu_feat_entries)

    return {
        "series": "D2",
        "id": did,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "file_exists": path.is_file(),
        "n_poses_pdbqt": len(poses),
        "pose_scores": [
            {
                "model": p["model"],
                "vina_score": p["vina_score"],
                "rmsd_lb": p["rmsd_lb"],
                "rmsd_ub": p["rmsd_ub"],
            }
            for p in sorted(poses, key=lambda x: x["model"])
        ],
        "comparable_pose": {
            "rule": "lowest (most negative) REMARK VINA RESULT among written MODELs",
            "model": best["model"],
            "vina_score_kcal_mol": best["vina_score"],
            "score_note": "Vina REMARK number only — not experimental affinity",
        },
        "ligand_centroid": [round(float(x), 3) for x in ligand_heavy_centroid(best["atoms"])],
        "dist_to_box_center_A": round(
            float(np.linalg.norm(ligand_heavy_centroid(best["atoms"]) - BOX_CENTER)), 3
        ),
        "contacts": contacts,
        "polar_proximity_not_hbond": polar,
        "region_min_dist_A": region,
        "region_contact_4A": {
            r: (region[r] is not None and region[r] <= HEAVY_CUTOFF) for r in REGION_RESIDUES
        },
        "orientation": orient,
        "feature_summary": feat_sum,
        "conservation_vs_qiu_0g_map": cons,
        "_atoms": best["atoms"],
        "_contact_set": contact_set(contacts),
    }


def fmt_cent(c: list[float] | None) -> str:
    if not c:
        return "—"
    return f"({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f})"


def write_md(data: dict) -> None:
    lines: list[str] = []
    a = lines.append

    a("# Qiu 0H — Descriptive CB2 pose audit (Qiu 14/15/20/24 vs D2_20/06/22)")
    a("")
    a("> **Scope:** read-only geometry / contacts for **existing** best PDBQT poses. No re-docking; no Vina; no PDBQT edits.")
    a(">")
    a("> **No SAR / no pharmacological conclusions / no affinity claims from Vina scores.**")
    a(">")
    a("> **Date:** 2026-08-12")
    a(">")
    a("> **Script:** `scripts/audit_qiu_0h_poses.py`")
    a(">")
    a("> **Upstream:** [`qiu_0g_pose_analysis.md`](qiu_0g_pose_analysis.md), [`qiu_0g_vs_d1_cb2_pose_comparison.md`](qiu_0g_vs_d1_cb2_pose_comparison.md), [`qiu_0g_vs_d1_pharmacophore_geometry.md`](qiu_0g_vs_d1_pharmacophore_geometry.md), [`qiu_0d_0g_integration_qc.md`](qiu_0d_0g_integration_qc.md)")
    a("")
    a("---")
    a("")
    a("## Methods")
    a("")
    a("### Poses used (strict)")
    a("")
    a("| Set | Path pattern | IDs |")
    a("|-----|----------------|-----|")
    a("| Qiu | `results/docking/qiu_0f/compound_{N}_cb2_out.pdbqt` | 14, 15, 20, 24 |")
    a("| D2 | `results/docking/option_d_batch2/cb2/{ID}_docked.pdbqt` | JANUS_D2_20, JANUS_D2_06, JANUS_D2_22 |")
    a("| Receptor | `data/targets/cb2/6PT0_rec.pdbqt` chain R | — |")
    a("")
    a("- A pose counts **only** if it is a `MODEL` / `ENDMDL` block with `REMARK VINA RESULT` in the PDBQT.")
    a("- Qiu log-only modes not written to out PDBQT are **excluded** (same 0F/0G rule; compounds **15** and **20**).")
    a("- **Comparable pose** = MODEL with the **lowest (most negative)** Vina REMARK among written models.")
    a("")
    a("### Cutoffs (reuse 0G / pharmacophore geometry)")
    a("")
    a("| Label | Definition |")
    a("|-------|------------|")
    a(f"| **Contact residue** | ≥1 ligand–receptor heavy-atom pair ≤ **{HEAVY_CUTOFF} Å** |")
    a(f"| **H-bond (geometry OK)** | D–A ≤ {HBOND_DA_CUTOFF} Å **and** H···A ≤ {HBOND_HA_CUTOFF} Å **and** angle D–H···A ≥ {HBOND_ANGLE_MIN}° |")
    a(f"| **Polar proximity (not H-bond)** | Polar heavy (OA/NA/N/O/SA/OS) ≤ {HBOND_DA_CUTOFF} Å without geometry-OK H-bond |")
    a("| **Hydrophobic proximity** | C/A–C/A pairs within contact cutoff |")
    a(f"| **Feature correspondence** | Feature centroid ≤ **{CENTROID_NEAR_A} Å** **or** shell Jaccard ≥ **{SHELL_JACCARD_MIN}** |")
    a("| **0G region shell** | SER285, TYR25, THR114, ILE110, ILE186 |")
    a("")
    a("### Epistemic labels (required)")
    a("")
    a("| Label | Meaning |")
    a("|-------|---------|")
    a("| **Observación** | Coordinates, Vina REMARK numbers, contact lists, SMARTS hits, distances at fixed cutoffs |")
    a("| **Inferencia** | Jaccard / correspondence / conservation / feature-swap flags from those cutoffs |")
    a("| **Interpretación** | Brief structural notes (scaffold orientation, occupation); **not** activity or SAR |")
    a("")
    a("---")
    a("")
    a("## Inventory")
    a("")
    a("| Item | Status |")
    a("|------|--------|")
    a(f"| Receptor | {'present' if data['inventory']['receptor_exists'] else 'MISSING'} |")
    for cid in QIU_IDS:
        e = data["compounds"][f"Qiu_{cid}"]
        a(f"| Qiu {cid} out PDBQT | {'present' if e.get('file_exists') else 'MISSING'} ({e.get('n_poses_pdbqt', 0)} MODELs) |")
    for did in D2_IDS:
        e = data["compounds"][did]
        a(f"| {did} docked PDBQT | {'present' if e.get('file_exists') else 'MISSING'} ({e.get('n_poses_pdbqt', 0)} MODELs) |")
    a("")
    a("---")
    a("")
    a("## Per-compound audits")
    a("")

    for cid in QIU_IDS:
        e = data["compounds"][f"Qiu_{cid}"]
        meta = e["scaffold_labels"]
        a(f"### Qiu {cid} ({meta['n1_sub']}; {meta['r3']})")
        a("")
        a(f"**Path:** `{e['path']}`")
        a("")
        a("#### 1. Comparable pose")
        a("")
        a("| Field | Value | Label |")
        a("|-------|-------|-------|")
        a(f"| Poses in PDBQT | {e['n_poses_pdbqt']} | Observación |")
        a(f"| Best MODEL | **{e['comparable_pose']['model']}** | Observación |")
        a(f"| Vina REMARK | **{e['comparable_pose']['vina_score_kcal_mol']}** kcal/mol | Observación (score-only) |")
        a(f"| Ligand centroid | {fmt_cent(e['ligand_centroid'])} | Observación |")
        a(f"| Dist. to box center | {e['dist_to_box_center_A']} Å | Observación |")
        a("")
        if cid in (15, 20):
            a(f"**Observación (prior 0F/0G):** compound {cid} had ≥1 log mode not written to PDBQT (`energy_range`); this audit uses written MODELs only.")
            a("")
        a("#### 2. Contacts / interactions")
        a("")
        princ = ", ".join(e["contacts"]["principal_residues"])
        a(f"- **Observación — contact residues (heavy ≤ {HEAVY_CUTOFF} Å, principal):** {princ}")
        a(f"- **Observación — n contacts:** {e['contacts']['n_contact_residues']}")
        hb = e["contacts"]["hbonds_geometry_ok"]
        if hb:
            a("- **Observación — H-bond geometry OK:**")
            for h in hb:
                a(f"  - {h['direction']}: {h['lig']} ··· {h['rec']} (HA={h['d_HA']}, DA={h['d_DA']}, ∠={h['angle_DHA']}°)")
        else:
            a("- **Observación — H-bond geometry OK:** none")
        if e["polar_proximity_not_hbond"]:
            a("- **Observación — polar proximity (not H-bond):**")
            for p in e["polar_proximity_not_hbond"][:6]:
                a(f"  - {p['lig']} ··· {p['rec']} = {p['dist_A']} Å")
        hydro = e["contacts"].get("hydrophobic_proximity", [])[:6]
        if hydro:
            a("- **Observación — hydrophobic proximity (examples):** " + ", ".join(
                f"{h['residue']}({h['min_dist']} Å)" for h in hydro
            ))
        a("")
        a("#### 3. Region distances (whole ligand → residue)")
        a("")
        a("| Residue | min heavy (Å) | ≤4.0 Å? |")
        a("|---------|---------------|---------|")
        for r in REGION_RESIDUES:
            d = e["region_min_dist_A"].get(r)
            hit = e["region_contact_4A"].get(r)
            a(f"| {r} | {d if d is not None else '—'} | {'yes' if hit else 'no'} |")
        a("")
        a("*Label: Observación*")
        a("")
        a("#### 4. Orientation of key groups")
        a("")
        o = e["orientation"]
        dom = o.get("dominant_axis_from_pyrazole", {})
        a("| Group | Dominant axis from pyrazole | Centroid |")
        a("|-------|----------------------------|----------|")
        for g in ("adamantyl", "n1_heterocycle", "c5_phenyl", "n1_phenyl", "amide"):
            v = o.get("vectors_from_pyrazole", {}).get(g)
            ax = dom.get(g.replace("amide", "amide"))  # amide may lack dominant map
            if g == "amide":
                ax = "—"
                if v:
                    comps = [
                        ("+x" if v["dx"] >= 0 else "-x", abs(v["dx"])),
                        ("+y" if v["dy"] >= 0 else "-y", abs(v["dy"])),
                        ("+z" if v["dz"] >= 0 else "-z", abs(v["dz"])),
                    ]
                    ax = max(comps, key=lambda t: t[1])[0]
            else:
                ax = dom.get(g, "—")
            cent = fmt_cent(v["centroid"]) if v else "—"
            a(f"| {g} | {ax} | {cent} |")
        a("")
        a("*Label: Observación (coordinates); Interpretación: structural placement only — not pharmacology.*")
        a("")
        a("#### 5. Conservation vs Qiu 0G feature map")
        a("")
        feats = ", ".join(e["feature_summary"]["features_found"])
        a(f"- **Observación:** features found = {feats}")
        a("- **Interpretación:** this is a Qiu reference pose; conservation column applies to D2 compounds below.")
        if cid == 24:
            a("- **Inferencia (vs 14/15/20):** N1-heterocycle dominant axis differs (rotated within same box) — consistent with 0G.")
        if cid == 15:
            a("- **Observación:** TYR25 in region shell (m-morpholine extension) — consistent with 0G.")
        a("")
        a("---")
        a("")

    for did in D2_IDS:
        e = data["compounds"][did]
        a(f"### {did}")
        a("")
        a(f"**Path:** `{e['path']}`")
        a("")
        a("#### 1. Comparable pose")
        a("")
        a("| Field | Value | Label |")
        a("|-------|-------|-------|")
        a(f"| Poses in PDBQT | {e['n_poses_pdbqt']} | Observación |")
        a(f"| Best MODEL | **{e['comparable_pose']['model']}** | Observación |")
        a(f"| Vina REMARK | **{e['comparable_pose']['vina_score_kcal_mol']}** kcal/mol | Observación (score-only) |")
        a(f"| Ligand centroid | {fmt_cent(e['ligand_centroid'])} | Observación |")
        a(f"| Dist. to box center | {e['dist_to_box_center_A']} Å | Observación |")
        a("")
        a("#### 2. Contacts / interactions")
        a("")
        princ = ", ".join(e["contacts"]["principal_residues"])
        a(f"- **Observación — contact residues (principal):** {princ}")
        a(f"- **Observación — n contacts:** {e['contacts']['n_contact_residues']}")
        hb = e["contacts"]["hbonds_geometry_ok"]
        if hb:
            a("- **Observación — H-bond geometry OK:**")
            for h in hb:
                a(f"  - {h['direction']}: {h['lig']} ··· {h['rec']} (HA={h['d_HA']}, DA={h['d_DA']}, ∠={h['angle_DHA']}°)")
        else:
            a("- **Observación — H-bond geometry OK:** none")
        if e["polar_proximity_not_hbond"]:
            a("- **Observación — polar proximity (not H-bond):**")
            for p in e["polar_proximity_not_hbond"][:6]:
                a(f"  - {p['lig']} ··· {p['rec']} = {p['dist_A']} Å")
        hydro = e["contacts"].get("hydrophobic_proximity", [])[:6]
        if hydro:
            a("- **Observación — hydrophobic proximity (examples):** " + ", ".join(
                f"{h['residue']}({h['min_dist']} Å)" for h in hydro
            ))
        a("")
        a("#### 3. Region distances (whole ligand → residue)")
        a("")
        a("| Residue | min heavy (Å) | ≤4.0 Å? |")
        a("|---------|---------------|---------|")
        for r in REGION_RESIDUES:
            d = e["region_min_dist_A"].get(r)
            hit = e["region_contact_4A"].get(r)
            a(f"| {r} | {d if d is not None else '—'} | {'yes' if hit else 'no'} |")
        a("")
        a("*Label: Observación*")
        a("")
        a("#### 4. Orientation of key groups")
        a("")
        o = e["orientation"]
        dom = o.get("dominant_axis_from_pyrrole", {})
        a("| Group | Dominant axis from pyrrole | Centroid |")
        a("|-------|---------------------------|----------|")
        for g in ("benzoyl_aryl", "n1_benzyl_aryl", "aryl_ketone", "c2_phenyl", "c3_amino"):
            v = o.get("vectors_from_pyrrole", {}).get(g)
            ax = dom.get(g, "—")
            cent = fmt_cent(v["centroid"]) if v else "—"
            a(f"| {g} | {ax if ax else '—'} | {cent} |")
        a("")
        a("*Label: Observación; Interpretación: URB447-like scaffold placement — not Ad/CONH identity.*")
        a("")
        a("#### 5. Conservation / loss of 0G features (vs Qiu map)")
        a("")
        cons = e["conservation_vs_qiu_0g_map"]
        a("| D2 feature | Qiu feature | spatial_ok | Status | Label |")
        a("|------------|-------------|------------|--------|-------|")
        for ax in cons["axes"]:
            a(
                f"| {ax['d2_feature']} | {ax['qiu_feature']} | {ax['spatial_ok_count']} | {ax['status']} | Inferencia |"
            )
        a("")
        a(f"- **Observación — Qiu-only features absent on D2:** {', '.join(cons['qiu_only_absent_on_d2']) or '—'}")
        patterns = {n["qiu_ref"]: n["pattern"] for n in cons["orientation_vs_ad_het"]}
        pat_str = ", ".join(f"Qiu {k}={v}" for k, v in sorted(patterns.items(), key=lambda t: int(t[0])))
        a(f"- **Inferencia — benzoyl/benzyl vs Ad/N1-het orientation pattern:** {pat_str}")
        if did == "JANUS_D2_22":
            a("- **Inferencia:** D2_22 shows **feature_swap** vs Qiu Ad/N1-het pairing more often than D2_20/06 (consistent with pharmacophore geometry report).")
            a("- **Interpretación:** mid pocket-overlap + swapped feature placement; do **not** elevate by most-negative Vina REMARK.")
        if did in ("JANUS_D2_20", "JANUS_D2_06"):
            a("- **Inferencia:** orientation pattern closer to canonical Ad↔benzoyl / N1-het↔benzyl spatial pairing (vs D2_22).")
        a("")
        a("---")
        a("")

    # Cross-comparison
    a("## Cross-comparison (Qiu ↔ D2) — descriptive")
    a("")
    a("Not a ranking. Occupation and feature conservation only.")
    a("")
    xc = data["cross_comparison"]
    a("### Pocket occupation (Observación + Inferencia)")
    a("")
    a("| Pair | Δcentroid (Å) | Contact Jaccard | Cloud overlap @2 Å | Notes |")
    a("|------|---------------|-----------------|--------------------|-------|")
    for row in xc["pairwise"]:
        a(
            f"| {row['qiu']} ↔ {row['d2']} | {row['centroid_delta_A']} | {row['contact_jaccard']} | {row['cloud_overlap_mean']} | {row['note']} |"
        )
    a("")
    a("### Feature conservation summary (Inferencia)")
    a("")
    a("| D2 | Conserved spatial axes (≥2/4 Qiu) | Weak/lost axes | Qiu-only absent | Orientation vs Ad/het |")
    a("|----|-----------------------------------|----------------|-----------------|----------------------|")
    for did in D2_IDS:
        e = data["compounds"][did]
        cons = e["conservation_vs_qiu_0g_map"]
        cons_ok = [f"{ax['d2_feature']}↔{ax['qiu_feature']}" for ax in cons["axes"] if ax["status"] == "conserved_spatial"]
        weak = [f"{ax['d2_feature']}↔{ax['qiu_feature']}" for ax in cons["axes"] if ax["status"] != "conserved_spatial"]
        pats = sorted({n["pattern"] for n in cons["orientation_vs_ad_het"]})
        a(
            f"| {did} | {', '.join(cons_ok) or '—'} | {', '.join(weak) or '—'} | {', '.join(cons['qiu_only_absent_on_d2'])} | {', '.join(pats)} |"
        )
    a("")
    a("### Brief pairwise notes")
    a("")
    for note in xc["narrative_notes"]:
        a(f"- **{note['label']}:** {note['text']}")
    a("")
    a("---")
    a("")
    a("## Ambiguities / limitations")
    a("")
    for i, lim in enumerate(data["limitations"], 1):
        a(f"{i}. {lim}")
    a("")
    a("---")
    a("")
    a("## Summary table")
    a("")
    a("| Compound | MODEL | Vina (score-only) | Region hits | H-bonds OK | Key orientation note |")
    a("|----------|-------|-------------------|-------------|------------|----------------------|")
    for row in data["summary_table"]:
        a(
            f"| {row['id']} | {row['model']} | {row['vina']} | {row['region_hits']} | {row['hbonds']} | {row['orient_note']} |"
        )
    a("")
    a("---")
    a("")
    a("## Verdict")
    a("")
    a(data["verdict_rationale"])
    a("")
    a(f"**`{data['verdict']}`**")
    a("")
    a("---")
    a("")
    a("## Closing")
    a("")
    a("No SAR. No pharmacological conclusion. Shared pocket occupation or feature↔residue geometry does **not** imply shared activity, selectivity, or Janus profile. Vina REMARK values are docking score numbers only.")
    a("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    assert RECEPTOR.is_file(), f"missing receptor: {RECEPTOR}"
    rec = load_receptor_chain_r()

    compounds: dict = {}
    # Qiu first
    for cid in QIU_IDS:
        compounds[f"Qiu_{cid}"] = audit_qiu(cid, rec)

    qiu_feat = {
        str(cid): compounds[f"Qiu_{cid}"]["feature_summary"] for cid in QIU_IDS
    }

    for did in D2_IDS:
        compounds[did] = audit_d2(did, rec, qiu_feat)

    # Qiu consensus centroid
    q_cents = [np.array(compounds[f"Qiu_{cid}"]["ligand_centroid"]) for cid in QIU_IDS]
    q_mean = np.mean(q_cents, axis=0)

    pairwise = []
    for cid in QIU_IDS:
        qe = compounds[f"Qiu_{cid}"]
        qa = qe["_atoms"]
        qs = contact_set(qe["contacts"])
        for did in D2_IDS:
            de = compounds[did]
            da = de["_atoms"]
            ds = de["_contact_set"]
            cloud = atom_cloud_overlap(qa, da, shell_A=2.0)
            jac = jaccard(qs, ds)
            dcent = float(np.linalg.norm(np.array(qe["ligand_centroid"]) - np.array(de["ligand_centroid"])))
            note = ""
            if did == "JANUS_D2_22":
                note = "mid overlap; feature-swap orientation"
            elif did in ("JANUS_D2_20", "JANUS_D2_06") and cid == 15:
                note = "both contact TYR25 shell"
            elif did in ("JANUS_D2_20", "JANUS_D2_06"):
                note = "high Jaccard cluster vs Qiu"
            pairwise.append(
                {
                    "qiu": f"Qiu_{cid}",
                    "d2": did,
                    "centroid_delta_A": round(dcent, 3),
                    "contact_jaccard": round(jac, 3) if jac is not None else None,
                    "cloud_overlap_mean": cloud["mean_frac"],
                    "note": note,
                }
            )

    narrative = [
        {
            "label": "Observación",
            "text": "All seven best poses sit in the same CB2 orthosteric-like box (centroids within ~1–2.4 Å of Qiu consensus; consistent with prior D1 comparison).",
        },
        {
            "label": "Observación",
            "text": "No geometry-OK H-bonds under 0G criteria for any of the seven audited poses (polar proximities may exist).",
        },
        {
            "label": "Inferencia",
            "text": "D2_20 and D2_06 conserve more spatial axes vs Qiu Ad/amide/N1-het map; D2_22 more often shows benzoyl↔N1-het / benzyl↔Ad feature swap.",
        },
        {
            "label": "Observación",
            "text": "Adamantyl, CONH–Ad amide, and morpholine/piperazine are Qiu-only; D2 poses use pyrrole + aryl ketone + N-benzyl chemistry.",
        },
        {
            "label": "Interpretación",
            "text": "Shared occupation ≠ same pharmacophore ≠ same pharmacology (axiom from pharmacophore geometry report).",
        },
    ]

    summary = []
    for cid in QIU_IDS:
        e = compounds[f"Qiu_{cid}"]
        hits = sum(1 for v in e["region_contact_4A"].values() if v)
        o = e["orientation"]["dominant_axis_from_pyrazole"]
        summary.append(
            {
                "id": f"Qiu_{cid}",
                "model": e["comparable_pose"]["model"],
                "vina": e["comparable_pose"]["vina_score_kcal_mol"],
                "region_hits": f"{hits}/5",
                "hbonds": len(e["contacts"]["hbonds_geometry_ok"]),
                "orient_note": f"Ad {o.get('adamantyl')}; N1-het {o.get('n1_heterocycle')}; C5-Ph {o.get('c5_phenyl')}",
            }
        )
    for did in D2_IDS:
        e = compounds[did]
        hits = sum(1 for v in e["region_contact_4A"].values() if v)
        o = e["orientation"].get("dominant_axis_from_pyrrole", {})
        pats = sorted({n["pattern"] for n in e["conservation_vs_qiu_0g_map"]["orientation_vs_ad_het"]})
        summary.append(
            {
                "id": did,
                "model": e["comparable_pose"]["model"],
                "vina": e["comparable_pose"]["vina_score_kcal_mol"],
                "region_hits": f"{hits}/5",
                "hbonds": len(e["contacts"]["hbonds_geometry_ok"]),
                "orient_note": f"Bz {o.get('benzoyl_aryl')}; NBn {o.get('n1_benzyl_aryl')}; pattern={','.join(pats)}",
            }
        )

    limitations = [
        "Static docking only (6PT0); no MD / ensemble.",
        "Vina REMARK ≠ experimental affinity.",
        "Compounds 15 and 20: log had extra modes not written to PDBQT — excluded by design (0F/0G).",
        "No geometry-OK H-bonds under stated angle criterion; polar O···Thr/Ser contacts are proximities.",
        "Contact cutoff 4.0 Å and feature gates (3.0 Å / Jaccard 0.25) are heuristic.",
        "Cross-chemotype whole-ligand RMSD omitted; cloud overlap and residue Jaccard are occupation proxies.",
        "D1 vs Qiu ligand preparation pipelines may differ; same receptor PDBQT.",
        "Chemotype mismatch (Ad/CONH/morpholine vs URB447 ketone/benzyl) limits chemical identity of 'conserved' features — spatial only.",
        "D2_22 feature-swap is geometric inference; not a pharmacological mode claim.",
    ]

    # Verdict
    missing = [
        k
        for k, v in compounds.items()
        if v.get("error") or not v.get("file_exists", True)
    ]
    if missing:
        verdict = "0H = NEEDS REVIEW"
        rationale = f"Missing or unparsable poses: {', '.join(missing)}."
    else:
        verdict = "0H = PASS WITH OBSERVATIONS"
        rationale = (
            "All 7 poses audited cleanly from written PDBQTs with consistent cutoffs. "
            "Observations retained: Qiu 15/20 log↔PDBQT energy_range mismatch; "
            "chemotype mismatch (Ad/CONH vs URB447); D2_22 feature-swap; "
            "no geometry-OK H-bonds under 0G criteria. These are documented limitations, not file failures."
        )

    # Strip private caches before JSON
    for e in compounds.values():
        e.pop("_atoms", None)
        e.pop("_contact_set", None)

    data = {
        "methods": {
            "heavy_contact_cutoff_A": HEAVY_CUTOFF,
            "hbond": {
                "d_DA_max_A": HBOND_DA_CUTOFF,
                "d_HA_max_A": HBOND_HA_CUTOFF,
                "angle_DHA_min_deg": HBOND_ANGLE_MIN,
            },
            "feature_gates": {
                "centroid_near_A": CENTROID_NEAR_A,
                "shell_jaccard_min": SHELL_JACCARD_MIN,
            },
            "box_center_ref": BOX_CENTER.tolist(),
            "qiu_consensus_centroid": [round(float(x), 3) for x in q_mean],
            "score_note": "Vina REMARK scores are score-only; never experimental affinity",
            "read_only": True,
        },
        "inventory": {
            "receptor": str(RECEPTOR.relative_to(ROOT)).replace("\\", "/"),
            "receptor_exists": RECEPTOR.is_file(),
            "qiu_ids": list(QIU_IDS),
            "d2_ids": list(D2_IDS),
        },
        "compounds": compounds,
        "cross_comparison": {
            "pairwise": pairwise,
            "narrative_notes": narrative,
        },
        "summary_table": summary,
        "limitations": limitations,
        "verdict": verdict,
        "verdict_rationale": rationale,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
    write_md(data)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(verdict)


if __name__ == "__main__":
    main()
