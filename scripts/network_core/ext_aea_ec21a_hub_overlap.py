#!/usr/bin/env python3
"""EXTERNAL — Geometric AEA/HU308 × Ec21a plug × hubs TM7 (static PDBs).

Pre-reg: docs/synthesis/EXPERIMENT_EXT_AEA_EC21A_HUB_OVERLAP.md
8GUS via MDAnalysis; 9U7L via Bio.PDB MMCIFParser (ligands A1EOL/9GF).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "network_core"
PDB_DIR = ROOT / "data" / "external" / "cb2_landmark_expanded"
PDB_8GUS = PDB_DIR / "8GUS.pdb"
CIF_9U7L = PDB_DIR / "9U7L.cif"

HUBS_TM7 = {287: "LEU287", 291: "ASN291", 295: "ASN295"}
VESTIBULE = {
    268: "SER268",
    278: "LYS278",
    183: "PHE183",
    186: "ILE186",
    176: "PRO176",
    178: "PRO178",
}
TM_RANGES = {
    "TM1": (27, 51),
    "TM5": (185, 217),
    "TM6": (230, 260),
    "TM7": (270, 300),
}
NEAR = 5.0
SHELL = 8.0
AA = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    "MSE", "HSD", "HIE", "HID", "HIP", "CYX",
}


def _min_dist(a: np.ndarray, b: np.ndarray) -> float:
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2))
    return float(d.min())


def _class(d: float | None) -> str:
    if d is None:
        return "MISSING"
    if d < NEAR:
        return "NEAR_LIGAND"
    if d < SHELL:
        return "SHELL"
    return "DISTAL"


def _helix_membership(resid: int) -> list[str]:
    return [h for h, (lo, hi) in TM_RANGES.items() if lo <= resid <= hi]


def _mda_heavy(u, resid: int, chain: str = "R") -> np.ndarray | None:
    sel = u.select_atoms(f"protein and segid {chain} and resid {resid} and not name H*")
    if len(sel) == 0:
        sel = u.select_atoms(f"protein and resid {resid} and not name H*")
    if len(sel) == 0:
        return None
    return sel.positions.astype(float)


def _mda_ligand(u, resname: str) -> np.ndarray | None:
    sel = u.select_atoms(f"resname {resname} and not name H*")
    return None if len(sel) == 0 else sel.positions.astype(float)


def _bio_load_9u7l():
    from Bio.PDB import MMCIFParser

    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("9U7L", str(CIF_9U7L))
    model = next(structure.get_models())
    chain = model["R"]
    protein: dict[int, np.ndarray] = {}
    ligands: dict[str, np.ndarray] = {}
    for res in chain:
        het, resid, _ = res.id
        name = res.get_resname().strip()
        coords = []
        for atom in res:
            if atom.element == "H":
                continue
            coords.append(atom.coord)
        if not coords:
            continue
        arr = np.asarray(coords, dtype=float)
        if het == " " and name in AA:
            protein[int(resid)] = arr
        else:
            ligands[name] = arr
    return protein, ligands


def main() -> int:
    import MDAnalysis as mda

    OUT.mkdir(parents=True, exist_ok=True)
    run_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not PDB_8GUS.exists() or not CIF_9U7L.exists():
        verdict = "EXT_AEA_EC21A_HUB_OVERLAP_INDETERMINATE"
        (OUT / "ext_aea_ec21a_hub_overlap.json").write_text(
            json.dumps({"verdict": verdict, "run_utc": run_utc}, indent=2) + "\n"
        )
        (OUT / "ext_aea_ec21a_hub_overlap.md").write_text(f"**`{verdict}`**\n")
        print(verdict)
        return 1

    u8 = mda.Universe(str(PDB_8GUS))
    ko3 = _mda_ligand(u8, "KO3")
    prot9, lig9 = _bio_load_9u7l()
    a1eol = lig9.get("A1EOL")
    cp55 = lig9.get("9GF")

    hub_rows = []
    n_near_hu = n_near_ec = n_shell_ec = 0
    for resid, name in HUBS_TM7.items():
        c8 = _mda_heavy(u8, resid, "R")
        c9 = prot9.get(resid)
        d_hu = _min_dist(c8, ko3) if c8 is not None and ko3 is not None else None
        d_ec = _min_dist(c9, a1eol) if c9 is not None and a1eol is not None else None
        d_cp = _min_dist(c9, cp55) if c9 is not None and cp55 is not None else None
        cls_hu, cls_ec, cls_cp = _class(d_hu), _class(d_ec), _class(d_cp)
        if cls_hu == "NEAR_LIGAND":
            n_near_hu += 1
        if cls_ec == "NEAR_LIGAND":
            n_near_ec += 1
        if cls_ec in ("NEAR_LIGAND", "SHELL"):
            n_shell_ec += 1
        hub_rows.append(
            {
                "hub": name,
                "resid": resid,
                "helices": _helix_membership(resid),
                "aea_primary_TM1_TM7_member": bool(
                    set(_helix_membership(resid)) & {"TM1", "TM7"}
                ),
                "aea_alt_TM5_TM6_member": bool(
                    set(_helix_membership(resid)) & {"TM5", "TM6"}
                ),
                "min_A_to_HU308_KO3": d_hu,
                "class_HU308": cls_hu,
                "min_A_to_Ec21a_A1EOL": d_ec,
                "class_Ec21a": cls_ec,
                "min_A_to_CP55_9GF": d_cp,
                "class_CP55": cls_cp,
            }
        )

    vest_rows = []
    for resid, name in VESTIBULE.items():
        c9 = prot9.get(resid)
        d_ec = _min_dist(c9, a1eol) if c9 is not None and a1eol is not None else None
        hub_ds = []
        for hresid in HUBS_TM7:
            ch = prot9.get(hresid)
            if c9 is not None and ch is not None:
                hub_ds.append(_min_dist(c9, ch))
        vest_rows.append(
            {
                "residue": name,
                "resid": resid,
                "min_A_to_Ec21a": d_ec,
                "class_Ec21a": _class(d_ec),
                "min_A_to_nearest_TM7_hub": min(hub_ds) if hub_ds else None,
            }
        )

    hubs_tm7 = all("TM7" in r["helices"] for r in hub_rows)
    ec_distal = all(r["class_Ec21a"] == "DISTAL" for r in hub_rows)
    if n_near_hu >= 2 and n_shell_ec >= 1:
        verdict = "EXT_AEA_EC21A_HUB_OVERLAP_STRONG"
    elif hubs_tm7 and (
        ec_distal
        or n_near_hu >= 1
        or any(r["class_CP55"] in ("NEAR_LIGAND", "SHELL") for r in hub_rows)
    ):
        verdict = "EXT_AEA_EC21A_HUB_OVERLAP_PARTIAL"
    elif all(
        r["class_HU308"] == "DISTAL" and r["class_Ec21a"] == "DISTAL" for r in hub_rows
    ):
        verdict = "EXT_AEA_EC21A_HUB_OVERLAP_ABSENT"
    else:
        verdict = "EXT_AEA_EC21A_HUB_OVERLAP_PARTIAL"

    payload = {
        "experiment": "EXTERNAL_AEA_EC21A_HUB_OVERLAP",
        "pre_reg": "docs/synthesis/EXPERIMENT_EXT_AEA_EC21A_HUB_OVERLAP.md",
        "run_utc": run_utc,
        "verdict": verdict,
        "thresholds_A": {"NEAR_LIGAND": NEAR, "SHELL": SHELL},
        "tm_ranges": TM_RANGES,
        "structures": {
            "HU308": {"pdb": str(PDB_8GUS.relative_to(ROOT)), "ligand": "KO3"},
            "Ec21a_CP55": {
                "cif": str(CIF_9U7L.relative_to(ROOT)),
                "ligands": ["A1EOL", "9GF"],
                "ligands_found": sorted(lig9.keys()),
            },
        },
        "hubs": hub_rows,
        "vestibule_residues": vest_rows,
        "counts": {
            "n_hubs_NEAR_HU308": n_near_hu,
            "n_hubs_NEAR_Ec21a": n_near_ec,
            "n_hubs_SHELL_or_NEAR_Ec21a": n_shell_ec,
        },
        "governance": {
            "AEA_TRAJ_UNPACK": False,
            "docking": "STOP",
            "P2_REOPEN": False,
            "Gi_FUNCTIONAL_CLAIM": False,
            "helix_membership_neq_atomistic_AEA_tunnel": True,
        },
        "dois": [
            "10.1016/j.jbc.2026.111434",
            "10.1038/s41467-023-37112-9",
            "10.1038/s41467-026-72923-6",
        ],
    }
    (OUT / "ext_aea_ec21a_hub_overlap.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    def fmt(d):
        return "—" if d is None else f"{d:.2f}"

    lines = [
        "# EXTERNAL — Geometric AEA/HU308 × Ec21a × hubs TM7",
        "",
        f"**Run UTC:** `{run_utc}`  ",
        "**Pre-reg:** `docs/synthesis/EXPERIMENT_EXT_AEA_EC21A_HUB_OVERLAP.md`  ",
        "**Mode:** static PDBs only — **no** AEA traj unpack, **no** docking.",
        "",
        "## Verdict",
        "",
        f"**`{verdict}`**",
        "",
        "> Hubs L287/N291/N295 son miembros de **TM7** (corredor AEA primario a nivel de hélice).  ",
        "> Capas: bolsillo ortostérico/HU-308 vs plug Ec21a vestibular (ECL2).  ",
        "> Helix membership ≠ tunnel atomístico AEA (trajs no desempaquetadas).",
        "",
        "## Hub distances (Å, heavy-atom min)",
        "",
        "| Hub | HU308 (KO3) | class | Ec21a (A1EOL) | class | CP55 (9GF) | class | AEA TM1–7 helix |",
        "|-----|------------:|-------|--------------:|-------|-----------:|-------|-----------------|",
    ]
    for r in hub_rows:
        lines.append(
            f"| {r['hub']} | {fmt(r['min_A_to_HU308_KO3'])} | **{r['class_HU308']}** | "
            f"{fmt(r['min_A_to_Ec21a_A1EOL'])} | **{r['class_Ec21a']}** | "
            f"{fmt(r['min_A_to_CP55_9GF'])} | {r['class_CP55']} | {r['aea_primary_TM1_TM7_member']} |"
        )
    lines += [
        "",
        "## Ec21a vestibule residues vs nearest TM7 hub",
        "",
        "| Residue | min Å → Ec21a | class | min Å → nearest hub TM7 |",
        "|---------|--------------:|-------|------------------------:|",
    ]
    for r in vest_rows:
        lines.append(
            f"| {r['residue']} | {fmt(r['min_A_to_Ec21a'])} | {r['class_Ec21a']} | "
            f"{fmt(r['min_A_to_nearest_TM7_hub'])} |"
        )
    lines += [
        "",
        "## Governance",
        "",
        "```text",
        f"VERDICT: {verdict}",
        "AEA_TRAJ_UNPACK: FALSE",
        "DOCKING: STOP",
        "P2_REOPEN: FALSE",
        "Gi_FUNCTIONAL_CLAIM: FALSE",
        "```",
        "",
        "---",
        "",
        "*Fin EXTERNAL geometric overlap.*",
        "",
    ]
    (OUT / "ext_aea_ec21a_hub_overlap.md").write_text("\n".join(lines), encoding="utf-8")
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
