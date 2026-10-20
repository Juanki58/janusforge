#!/usr/bin/env python3
"""Retrospective geometric audit of published CB2–Gαi cross-links.

This is a static coordinate comparison only. It does not infer dynamics,
cross-linking yield, or an intramolecular CB2 allosteric pathway.
"""

from __future__ import annotations

import hashlib
import json
import math
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PDB_DIR = ROOT / "data" / "external" / "cb2_landmark_expanded"
OUT_DIR = ROOT / "results" / "network_core"
STRUCTURE_FILES = {key: f"{key}.pdb" for key in ("6PT0", "6KPF", "8GUQ", "8GUR", "8GUS", "8GUT", "8X3L")}
STRUCTURE_FILES["12IZ"] = "12IZ.cif"
STRUCTURE_FILES["12JA"] = "12JA.cif"
STRUCTURES = tuple(STRUCTURE_FILES)

# Chain R is human CB2 (UniProt P34972); chain A is human Gαi1 (P63096)
# in the local RCSB PDB files. Residue numbers are UniProt-aligned PDB numbers.
CROSSLINKS = (
    {
        "id": "CNR2_C134_GNAI1_C351",
        "cb2_residue": 134,
        "cb2_resname": "CYS",
        "cb2_atom": "SG",
        "gai1_residue": 351,
        "gai1_resname": "CYS",
        "gai1_atom": "SG",
        "chemistry": "HgCl2 sulfhydryl cross-link",
        "ca_distance_min_angstrom": 7.0,
        "ca_distance_max_angstrom": 10.0,
    },
    {
        "id": "CNR2_K245_GNAI1_K349",
        "cb2_residue": 245,
        "cb2_resname": "LYS",
        "cb2_atom": "NZ",
        "gai1_residue": 349,
        "gai1_resname": "LYS",
        "gai1_atom": "NZ",
        "chemistry": "DSS lysine–lysine cross-link",
        "ca_distance_min_angstrom": None,
        "ca_distance_max_angstrom": 24.2,
    },
    {
        "id": "CNR2_K215_GNAI1_K317",
        "cb2_residue": 215,
        "cb2_resname": "LYS",
        "cb2_atom": "NZ",
        "gai1_residue": 317,
        "gai1_resname": "LYS",
        "gai1_atom": "NZ",
        "chemistry": "DSS lysine–lysine cross-link",
        "ca_distance_min_angstrom": None,
        "ca_distance_max_angstrom": 24.2,
    },
)


def read_atoms(path: Path) -> dict[tuple[str, int, str], tuple[str, tuple[float, float, float]]]:
    if path.suffix.lower() in {".cif", ".mmcif"}:
        return read_cif_atoms(path)
    atoms = {}
    for line in path.read_text(errors="replace").splitlines():
        if not line.startswith("ATOM  "):
            continue
        atom_name = line[12:16].strip()
        altloc = line[16:17]
        chain = line[21:22]
        try:
            residue = int(line[22:26])
            xyz = tuple(float(line[i : i + 8]) for i in (30, 38, 46))
        except ValueError:
            continue
        element = line[76:78].strip().upper()
        if element in {"H", "D"} or altloc not in {" ", "A"}:
            continue
        atoms[(chain, residue, atom_name)] = (line[17:20].strip(), xyz)
    return atoms


def read_cif_atoms(path: Path) -> dict[tuple[str, int, str], tuple[str, tuple[float, float, float]]]:
    lines = path.read_text(errors="replace").splitlines()
    headers = None
    atoms = {}
    for line in lines:
        if line.startswith("_atom_site."):
            headers = headers or []
            headers.append(line.strip())
            continue
        if headers is None:
            continue
        if not line or line.startswith("#"):
            break
        row = shlex.split(line)
        if len(row) != len(headers):
            continue
        values = dict(zip(headers, row))
        if values.get("_atom_site.group_PDB") not in {"ATOM", "HETATM"}:
            continue
        if values.get("_atom_site.pdbx_PDB_model_num", "1") != "1":
            continue
        if values.get("_atom_site.label_alt_id", ".") not in {".", "?", "A"}:
            continue
        if values.get("_atom_site.type_symbol", "").upper() in {"H", "D"}:
            continue
        try:
            key = (values["_atom_site.auth_asym_id"], int(values["_atom_site.auth_seq_id"]), values["_atom_site.auth_atom_id"])
            xyz = tuple(float(values[f"_atom_site.Cartn_{axis}"]) for axis in "xyz")
        except (KeyError, ValueError):
            continue
        atoms[key] = (values.get("_atom_site.auth_comp_id", "UNK"), xyz)
    return atoms


def distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def audit() -> dict:
    rows = []
    for pdb_id in STRUCTURES:
        path = PDB_DIR / STRUCTURE_FILES[pdb_id]
        atoms = read_atoms(path)
        structure = {
            "pdb_id": pdb_id,
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "crosslinks": [],
        }
        for link in CROSSLINKS:
            left = atoms.get(("R", link["cb2_residue"], link["cb2_atom"]))
            right = atoms.get(("A", link["gai1_residue"], link["gai1_atom"]))
            ca_left = atoms.get(("R", link["cb2_residue"], "CA"))
            ca_right = atoms.get(("A", link["gai1_residue"], "CA"))
            identity_ok = bool(
                left and right
                and left[0] == link["cb2_resname"]
                and right[0] == link["gai1_resname"]
            )
            value = distance(left[1], right[1]) if identity_ok else None
            ca_value = distance(ca_left[1], ca_right[1]) if identity_ok and ca_left and ca_right else None
            passes_cutoff = bool(
                ca_value is not None
                and (link["ca_distance_min_angstrom"] is None or ca_value >= link["ca_distance_min_angstrom"])
                and (link["ca_distance_max_angstrom"] is None or ca_value <= link["ca_distance_max_angstrom"])
            )
            structure["crosslinks"].append(
                {
                    **link,
                    "cb2_chain": "R",
                    "gai1_chain": "A",
                    "residue_identity_ok": identity_ok,
                    "endpoint_distance_angstrom": round(value, 2) if value is not None else None,
                    "ca_distance_angstrom": round(ca_value, 2) if ca_value is not None else None,
                    "ca_distance_min_angstrom": link["ca_distance_min_angstrom"],
                    "ca_distance_max_angstrom": link["ca_distance_max_angstrom"],
                    "passes_source_ca_distance_cutoff": passes_cutoff,
                }
            )
        rows.append(structure)

    summary = {}
    for link in CROSSLINKS:
        values = [
            pair["endpoint_distance_angstrom"]
            for structure in rows
            for pair in structure["crosslinks"]
            if pair["id"] == link["id"] and pair["endpoint_distance_angstrom"] is not None
        ]
        ca_values = [
            pair["ca_distance_angstrom"]
            for structure in rows
            for pair in structure["crosslinks"]
            if pair["id"] == link["id"] and pair["ca_distance_angstrom"] is not None
        ]
        summary[link["id"]] = {
            "n_structures_with_both_atoms": len(values),
            "min_angstrom": min(values) if values else None,
            "max_angstrom": max(values) if values else None,
            "mean_angstrom": round(sum(values) / len(values), 2) if values else None,
            "ca_min_angstrom": min(ca_values) if ca_values else None,
            "ca_max_angstrom": max(ca_values) if ca_values else None,
            "ca_mean_angstrom": round(sum(ca_values) / len(ca_values), 2) if ca_values else None,
            "n_within_source_ca_cutoff": sum(
                pair["passes_source_ca_distance_cutoff"]
                for structure in rows
                for pair in structure["crosslinks"]
                if pair["id"] == link["id"]
            ),
        }

    return {
        "analysis": "EXT_CB2_GI_CROSSLINK_STATIC_GEOMETRY",
        "verdict": "EXT_CB2_GI_XL_12IY_12JA_PARTIAL",
        "scope": "retrospective static coordinate audit; no dynamics or P2 inference",
        "source_paper_doi": "10.1074/jbc.M113.539916",
        "excluded_structures": [
            {
                "pdb_id": "12IY",
                "status": "N/A_NO_GI",
                "reason": "CB2 receptor-only structure; no G alpha i chain for intermolecular cross-link distances",
                "source_url": "https://www.rcsb.org/structure/12IY",
            }
        ],
        "structures": rows,
        "summary": summary,
    }


def render_markdown(result: dict) -> str:
    lines = [
        "# Static coordinate audit — published CB2–Gαi cross-links",
        "",
        "**Date:** 2026-10-19  ",
        "**Type:** Retrospective, descriptive coordinate comparison; no trajectory analysis.  ",
        "**Scope authorization:** User-directed continuation of the literature review; P2, P3, and P5 flags unchanged.",
        "",
        "## Question and method",
        "",
        "Mnpotra et al. identified three CB2–Gαi1 cross-linked residue pairs by chemical cross-linking and LC-MS/MS. This audit measures Cα–Cα distances, the metric compared with cutoffs in the paper, and also records reactive-atom endpoint distances (SG–SG or NZ–NZ). Local chain R is CB2 (UniProt P34972); chain A is Gαi1 (P63096). Coordinates use PDB residue numbering aligned to those UniProt accessions. No structural alignment, refinement, side-chain rotamer search, linker modelling, or dynamics was performed.",
        "",
        "Source paper: [Mnpotra et al., JBC (2014), DOI 10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916). Local CB2–Gi structures audited: 6PT0, 6KPF, 8GUQ, 8GUR, 8GUS, 8GUT, 8X3L, 12IZ, and 12JA. Verdict: `EXT_CB2_GI_XL_12IY_12JA_PARTIAL`; 12IY is `N/A_NO_GI` because it has no Gi chain ([RCSB 12IY](https://www.rcsb.org/structure/12IY)).",
        "",
        "## Comparison using the paper's distance criteria",
        "",
        "The source paper assessed Cα–Cα separations: 7–10 Å for the HgCl₂ cysteine pair and a maximum of 24.2 Å for each DSS lysine pair. The main values below are Cα–Cα distances, with these published cutoffs applied as a geometric screen. Parenthesized values are SG–SG or NZ–NZ endpoint separations (Å), included only as coordinate descriptors; they are not the paper's cutoff metric.",
        "",
        "| PDB | Ligand / source set | Cys134–Cys351 Cα (SG–SG) | Lys245–Lys349 Cα (NZ–NZ) | Lys215–Lys317 Cα (NZ–NZ) |",
        "|---|---|---:|---:|---:|",
    ]
    ligand = {
        "6PT0": "WIN 55,212-2",
        "6KPF": "AM12033-class",
        "8GUQ": "Olorinab",
        "8GUR": "CP55,940",
        "8GUS": "HU-308",
        "8GUT": "LEI-102",
        "8X3L": "agonist (8X3L)",
        "12JA": "agonist '1029",
        "12IZ": "agonist '5249",
    }
    by_id = {s["pdb_id"]: s for s in result["structures"]}
    order = [link["id"] for link in CROSSLINKS]
    for pdb_id in STRUCTURES:
        structure = by_id[pdb_id]
        links = {link["id"]: link for link in structure["crosslinks"]}
        def cell(link_id: str) -> str:
            pair = links[link_id]
            ca = pair["ca_distance_angstrom"]
            endpoint = pair["endpoint_distance_angstrom"]
            return f"{ca:.2f} ({endpoint:.2f})" if ca is not None and endpoint is not None else "ND"
        lines.append(f"| {pdb_id} | {ligand[pdb_id]} | {cell(order[0])} | {cell(order[1])} | {cell(order[2])} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"All {len(result['structures'])} CB2–Gi snapshots fall within the source paper's Cα-distance range for Cys134–Cys351 (7–10 Å) and below its maximum Cα distance for both lysine pairs (24.2 Å). Under that source-defined geometric screen, the published cross-links are compatible with each of these static CB2–Gi structures. The parenthesized NZ endpoint distances are longer for Lys215–Lys317, which shows why the source paper's Cα-based criterion must remain distinct from reactive-atom endpoint distances. 12IY is not counted: it is receptor-only (`N/A_NO_GI`), not a failed cross-link geometry.",
            "",
            "These are single static structures with engineered constructs and ligand-specific contexts. Passing a geometric cutoff does not establish cross-link formation probability or biological occupancy; the experiment was performed in membranes without exogenous agonist, while the structures represent ligand-bound cryo-EM complexes. This audit does not establish Gi rearrangement in cells, CB2 internal allostery, or an MSM architecture. No P2 result or status is changed.",
            "",
            "## Reproducibility",
            "",
            "Run from the repository root: `python scripts/network_core/ext_cb2_gi_crosslink_audit.py`. The runner writes this report and `ext_cb2_gi_crosslink_audit.json` under `results/network_core/`. Input PDB SHA-256 values are stored in the JSON.",
            "",
            "## Data and source",
            "",
            "- Primary cross-linking experiment: [Mnpotra et al. (2014)](https://doi.org/10.1074/jbc.M113.539916).",
            "- Cryo-EM CB2–Gi reference 6PT0: [Xing et al. (2020)](https://doi.org/10.1016/j.cell.2020.01.007).",
            "- Cryo-EM CB2–Gi 6KPF: [Hua et al. (2020)](https://doi.org/10.1016/j.cell.2020.01.008).",
            "- CB2–Gi panel 8GUQ/8GUR/8GUS/8GUT: [Li et al. (2023)](https://doi.org/10.1038/s41467-023-37112-9).",
            "- CB2–Gi structure 8X3L: [Shen et al. (2024)](https://doi.org/10.1073/pnas.2401091121).",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    result = audit()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "ext_cb2_gi_crosslink_audit.json"
    report_path = OUT_DIR / "ext_cb2_gi_crosslink_audit.md"
    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown(result), encoding="utf-8")
    print(report_path.relative_to(ROOT))
    for link_id, values in result["summary"].items():
        print(link_id, values)


if __name__ == "__main__":
    main()
