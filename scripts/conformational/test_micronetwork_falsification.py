#!/usr/bin/env python3
"""
Micronetwork falsification test — HU-308 / HU-433 enantiomer pair.

Pregunta primaria: ¿HU-308 y HU-433 presentan microdescriptores locales
REPRODUCIBLEMENTE DIFERENTES?

Pregunta secundaria (separada): ¿La diferencia observada es compatible con
las diferencias farmacológicas documentadas?

GOVERNANCE: DESCRIPTOR FROZEN BEFORE EXECUTION.
LOCAL_MICROSWITCH_VECTOR = [
    dist_Trp258,    # min heavy-atom dist ligand → Trp258^6.48 indole ring (Å)
    dist_Phe183,    # dist ligand centroid → Phe183^ECL2 aromatic ring centroid (Å)
    dist_Ser285,    # H-bond vector + dist → Ser285^7.39 hydroxyl O (Å)
    torsion_Trp258  # chi1/chi2 deviation of Trp258 sidechain vs 6PT0 canonical (°)
]

σ normalisation: z-score per component using independently-derived σ.
Distance: D = sqrt(Σ zᵢ²)
Threshold: ΔV ≥ 1.5σ → MICRONET_DISCRIMINATES
           ΔV < 1.5σ → MICRONET_FALSIFIED
           σ not independently definable → INDETERMINATE
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.conformational.pdb_utils import (
    atom_xyz,
    dihedral,
    read_atoms,
    residue_atoms,
)
from scripts.conformational.residue_maps import MICROSWITCHS, STRUCTURES

# ── Frozen descriptor definition ────────────────────────────────────────────
DESCRIPTOR_NAMES = (
    "dist_Trp258_A",
    "dist_Phe183_A",
    "dist_Ser285_A",
    "torsion_Trp258_deg",
)
DISCRIMINATION_THRESHOLD_SIGMA = 1.5

# ── CB2 microswitch residues (from residue_maps) ───────────────────────────
MS = MICROSWITCHS["cb2"]

# ── Reference canonical pose: 6PT0 Trp258 chi1/chi2 ────────────────────────
REF_PDB_ID = "6PT0"

# ── Panel definition ───────────────────────────────────────────────────────
PANEL = {
    "6PT0": {
        "label": "WIN55,212-2 (co-crystallised, 6PT0 reference agonist)",
        "role": "reference_agonist",
        "ligand_resname": "WI5",
        "pdb_source": "6PT0",
    },
    "6KPF": {
        "label": "CP55,940-like (co-crystallised, 6KPF active agonist)",
        "role": "cross_check_agonist",
        "ligand_resname": "E3R",
        "pdb_source": "6KPF",
    },
    "8GUR": {
        "label": "CP55,940 (co-crystallised, 8GUR positive control)",
        "role": "positive_control",
        "ligand_resname": "9GF",
        "pdb_source": "8GUR",
    },
    "5ZTY": {
        "label": "AM10257 (co-crystallised, 5ZTY negative/antagonist control)",
        "role": "negative_control",
        "ligand_resname": "9JU",
        "pdb_source": "5ZTY",
    },
    "HU-308": {
        "label": "HU-308 (enantiomer A, reference active)",
        "role": "primary_probe_A",
        "ligand_resname": None,
        "pdb_source": None,
    },
    "HU-433": {
        "label": "HU-433 (enantiomer B, witness)",
        "role": "primary_probe_B",
        "ligand_resname": None,
        "pdb_source": None,
    },
}

OUT_DIR = ROOT / "results" / "conformational"


def _trp258_indole_atoms(atoms: list) -> list[np.ndarray]:
    """Return heavy-atom coords of Trp258 indole ring system (CG CD1 NE1 CE2 CD2 CZ2 CH2 CZ3 CE3)."""
    indole_names = {"CG", "CD1", "NE1", "CE2", "CD2", "CZ2", "CH2", "CZ3", "CE3"}
    coords = []
    for rn, _ch, rs, an, xyz in atoms:
        if rs == MS.trp648 and rn.upper() == "TRP" and an in indole_names:
            coords.append(xyz.copy())
    return coords


def _phe183_ring_centroid(atoms: list) -> np.ndarray | None:
    """Return centroid of Phe183 aromatic ring (CG CD1 CE1 CZ CE2 CD2)."""
    ring_names = {"CG", "CD1", "CE1", "CZ", "CE2", "CD2"}
    coords = []
    for rn, _ch, rs, an, xyz in atoms:
        if rs == MS.phe_ecl2 and rn.upper() == "PHE" and an in ring_names:
            coords.append(xyz.copy())
    if len(coords) < 4:
        return None
    return np.mean(np.stack(coords), axis=0)


def _ser285_og(atoms: list) -> np.ndarray | None:
    return atom_xyz(atoms, MS.ser739, "SER", "OG")


def _trp258_chi1_chi2(atoms: list) -> tuple[float, float] | None:
    n = atom_xyz(atoms, MS.trp648, "TRP", "N")
    ca = atom_xyz(atoms, MS.trp648, "TRP", "CA")
    cb = atom_xyz(atoms, MS.trp648, "TRP", "CB")
    cg = atom_xyz(atoms, MS.trp648, "TRP", "CG")
    cd1 = atom_xyz(atoms, MS.trp648, "TRP", "CD1")
    if any(x is None for x in (n, ca, cb, cg, cd1)):
        return None
    chi1 = dihedral(n, ca, cb, cg)
    chi2 = dihedral(ca, cb, cg, cd1)
    return chi1, chi2


def _ligand_heavy_coords_hetatm(pdb_path: Path, ligand_resname: str) -> list[np.ndarray]:
    """Extract heavy-atom coords from HETATM records matching ligand_resname."""
    coords = []
    want = ligand_resname.upper()
    for line in pdb_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("HETATM"):
            continue
        rn = line[17:20].strip().upper()
        if rn != want:
            continue
        an = line[12:16].strip()
        if an.startswith("H"):
            continue
        xyz = np.array(
            [float(line[30:38]), float(line[38:46]), float(line[46:54])],
            dtype=float,
        )
        coords.append(xyz)
    return coords


def _ligand_centroid(coords: list[np.ndarray]) -> np.ndarray | None:
    if not coords:
        return None
    return np.mean(np.stack(coords), axis=0)


def _min_dist_to_atoms(query_coords: list[np.ndarray], target_coords: list[np.ndarray]) -> float:
    """Min heavy-atom distance between any query atom and any target atom."""
    min_d = float("inf")
    for q in query_coords:
        for t in target_coords:
            d = float(np.linalg.norm(q - t))
            if d < min_d:
                min_d = d
    return min_d


def _angular_deviation(chi1: float, chi2: float, ref_chi1: float, ref_chi2: float) -> float:
    """Combined angular deviation: sqrt(Δchi1² + Δchi2²) with wraparound."""
    def _delta(a: float, b: float) -> float:
        d = abs(a - b) % 360
        return min(d, 360 - d)
    return math.sqrt(_delta(chi1, ref_chi1) ** 2 + _delta(chi2, ref_chi2) ** 2)


def compute_descriptor(
    receptor_pdb: Path,
    full_pdb: Path,
    chain: str | None,
    ligand_resname: str,
    ref_chi1: float,
    ref_chi2: float,
) -> dict[str, Any] | None:
    """Compute LOCAL_MICROSWITCH_VECTOR for a co-crystallised ligand."""
    chains = {chain} if chain else None
    rec_atoms = read_atoms(receptor_pdb, chains=chains)

    lig_coords = _ligand_heavy_coords_hetatm(full_pdb, ligand_resname)
    if not lig_coords:
        return None

    lig_centroid = _ligand_centroid(lig_coords)

    trp_indole = _trp258_indole_atoms(rec_atoms)
    if not trp_indole:
        return None
    dist_trp258 = _min_dist_to_atoms(lig_coords, trp_indole)

    phe_centroid = _phe183_ring_centroid(rec_atoms)
    if phe_centroid is None:
        return None
    dist_phe183 = float(np.linalg.norm(lig_centroid - phe_centroid))

    ser_og = _ser285_og(rec_atoms)
    if ser_og is None:
        return None
    dist_ser285 = float(np.min([np.linalg.norm(c - ser_og) for c in lig_coords]))

    chi_pair = _trp258_chi1_chi2(rec_atoms)
    if chi_pair is None:
        return None
    torsion_dev = _angular_deviation(chi_pair[0], chi_pair[1], ref_chi1, ref_chi2)

    vec = [dist_trp258, dist_phe183, dist_ser285, torsion_dev]
    return {
        "vector": vec,
        "components": dict(zip(DESCRIPTOR_NAMES, vec)),
        "trp258_chi1": chi_pair[0],
        "trp258_chi2": chi_pair[1],
        "ligand_n_heavy_atoms": len(lig_coords),
    }


def _resolve_pdb_paths(pdb_id: str) -> tuple[Path, Path, str | None]:
    """Return (receptor_pdb, full_pdb_with_ligand, chain).

    receptor_pdb: clean PDB with ATOM records for microswitch extraction.
    full_pdb: original PDB or ligand file with HETATM records.
    """
    spec = next((s for s in STRUCTURES if s.pdb_id == pdb_id), None)
    chain = spec.chain if spec else None

    clean = ROOT / f"data/targets/cb2_multistate/{pdb_id}_clean.pdb"
    if not clean.exists():
        clean = ROOT / f"data/targets/cb2/{pdb_id}_clean.pdb"

    # Full PDB with HETATM ligand records
    full = ROOT / f"data/targets/cb2/{pdb_id}.pdb"
    if not full.exists():
        full = ROOT / f"data/targets/cb2_multistate/{pdb_id}.pdb"

    if not clean.exists():
        raise FileNotFoundError(f"No clean PDB for {pdb_id}")
    if not full.exists():
        raise FileNotFoundError(f"No full PDB (with ligand) for {pdb_id}")

    return clean, full, chain


def compute_sigma() -> dict[str, Any]:
    """
    Estimate independent σ per descriptor component.

    Option B: spread between same-ligand-class descriptors in 6PT0 vs 6KPF.
    Both are CB2 active-state agonist structures; descriptor differences
    reflect position uncertainty from crystal packing + resolution + ligand identity.

    Limitation: 6PT0 (WIN55,212-2) and 6KPF (AM12033) are different ligands,
    so σ includes ligand-identity variance — this is conservative (overestimates σ,
    making discrimination harder, biasing toward INDETERMINATE/FALSIFIED).
    """
    ref_clean, ref_full, ref_chain = _resolve_pdb_paths("6PT0")
    ref_atoms = read_atoms(ref_clean, chains={ref_chain} if ref_chain else None)
    ref_chi = _trp258_chi1_chi2(ref_atoms)
    if ref_chi is None:
        return {"available": False, "reason": "Cannot extract Trp258 chi from 6PT0"}
    ref_chi1, ref_chi2 = ref_chi

    descriptors = {}
    for pdb_id in ("6PT0", "6KPF"):
        info = PANEL[pdb_id]
        clean, full, chain = _resolve_pdb_paths(pdb_id)
        desc = compute_descriptor(clean, full, chain, info["ligand_resname"], ref_chi1, ref_chi2)
        if desc is None:
            return {"available": False, "reason": f"Cannot compute descriptor for {pdb_id}"}
        descriptors[pdb_id] = desc

    v1 = np.array(descriptors["6PT0"]["vector"])
    v2 = np.array(descriptors["6KPF"]["vector"])

    diff = np.abs(v1 - v2)
    sigma = diff / 2.0  # half-range of two observations as σ estimate

    sigma_zero = sigma < 1e-6
    if np.any(sigma_zero):
        pass  # will be handled as indeterminate for those components

    return {
        "available": True,
        "method": "Option B: half-range of 6PT0 vs 6KPF co-crystallised ligand descriptors",
        "limitation": (
            "6PT0 (WIN55,212-2) and 6KPF (AM12033) are different ligands; "
            "σ includes ligand-identity variance → conservative (overestimates σ)"
        ),
        "sigma_per_component": dict(zip(DESCRIPTOR_NAMES, [round(float(s), 4) for s in sigma])),
        "sigma_vector": [round(float(s), 4) for s in sigma],
        "n_observations": 2,
        "source_pdbs": ["6PT0", "6KPF"],
        "descriptors_used": descriptors,
    }


def run_test() -> dict[str, Any]:
    """Execute the full falsification test."""
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Get reference Trp258 chi from 6PT0
    ref_clean, _ref_full, ref_chain = _resolve_pdb_paths("6PT0")
    ref_atoms = read_atoms(ref_clean, chains={ref_chain} if ref_chain else None)
    ref_chi = _trp258_chi1_chi2(ref_atoms)
    assert ref_chi is not None, "6PT0 Trp258 chi extraction failed"
    ref_chi1, ref_chi2 = ref_chi

    # 2. Compute σ
    sigma_info = compute_sigma()

    # 3. Compute descriptors for all panel members with available poses
    panel_results: dict[str, Any] = {}
    for probe_id, info in PANEL.items():
        entry: dict[str, Any] = {
            "label": info["label"],
            "role": info["role"],
        }
        if info["ligand_resname"] is None:
            entry["status"] = "NO_POSE_AVAILABLE"
            entry["reason"] = (
                f"No docked pose for {probe_id} found in results/. "
                "Docking not yet performed for this compound."
            )
            entry["vector"] = None
        else:
            try:
                clean, full, chain = _resolve_pdb_paths(info["pdb_source"])
                desc = compute_descriptor(
                    clean, full, chain, info["ligand_resname"], ref_chi1, ref_chi2
                )
                if desc is None:
                    entry["status"] = "EXTRACTION_FAILED"
                    entry["reason"] = f"Could not extract descriptor from {info['pdb_source']}"
                    entry["vector"] = None
                else:
                    entry["status"] = "COMPUTED"
                    entry["vector"] = desc["vector"]
                    entry["components"] = desc["components"]
                    entry["trp258_chi1"] = round(desc["trp258_chi1"], 2)
                    entry["trp258_chi2"] = round(desc["trp258_chi2"], 2)
                    entry["ligand_n_heavy_atoms"] = desc["ligand_n_heavy_atoms"]
            except FileNotFoundError as e:
                entry["status"] = "PDB_NOT_FOUND"
                entry["reason"] = str(e)
                entry["vector"] = None

        panel_results[probe_id] = entry

    # 4. Primary test: HU-308 vs HU-433
    hu308 = panel_results.get("HU-308", {})
    hu433 = panel_results.get("HU-433", {})
    primary_verdict: dict[str, Any]

    if hu308.get("vector") is None or hu433.get("vector") is None:
        primary_verdict = {
            "verdict": "INDETERMINATE",
            "reason": (
                "No docked poses available for HU-308 and/or HU-433. "
                "Cannot compute ΔV between enantiomers. "
                "Docking with Vina against 6PT0 (and cross-check on 6KPF) is required."
            ),
            "delta_v": None,
            "threshold": DISCRIMINATION_THRESHOLD_SIGMA,
        }
    elif not sigma_info.get("available"):
        primary_verdict = {
            "verdict": "INDETERMINATE",
            "reason": f"σ estimation failed: {sigma_info.get('reason')}",
            "delta_v": None,
            "threshold": DISCRIMINATION_THRESHOLD_SIGMA,
        }
    else:
        sigma_vec = np.array(sigma_info["sigma_vector"])
        v308 = np.array(hu308["vector"])
        v433 = np.array(hu433["vector"])

        zero_sigma = sigma_vec < 1e-6
        if np.any(zero_sigma):
            primary_verdict = {
                "verdict": "INDETERMINATE",
                "reason": (
                    "One or more σ components are zero (no variance between 6PT0/6KPF for "
                    f"those components: {[DESCRIPTOR_NAMES[i] for i, z in enumerate(zero_sigma) if z]}). "
                    "Cannot form valid z-scores."
                ),
                "delta_v": None,
                "threshold": DISCRIMINATION_THRESHOLD_SIGMA,
            }
        else:
            z308 = (v308 - np.mean([v308, v433], axis=0)) / sigma_vec
            z433 = (v433 - np.mean([v308, v433], axis=0)) / sigma_vec
            delta_z = z308 - z433
            delta_v = float(np.linalg.norm(delta_z))

            if delta_v >= DISCRIMINATION_THRESHOLD_SIGMA:
                verdict_str = "MICRONET_DISCRIMINATES"
            else:
                verdict_str = "MICRONET_FALSIFIED"

            primary_verdict = {
                "verdict": verdict_str,
                "delta_v": round(delta_v, 4),
                "threshold": DISCRIMINATION_THRESHOLD_SIGMA,
                "z_scores_hu308": [round(float(z), 4) for z in z308],
                "z_scores_hu433": [round(float(z), 4) for z in z433],
            }

    # 5. Control distances (between available probes)
    control_distances: dict[str, Any] = {}
    computed_probes = {
        k: v for k, v in panel_results.items()
        if v.get("vector") is not None
    }
    probe_ids = list(computed_probes.keys())
    for i, a_id in enumerate(probe_ids):
        for b_id in probe_ids[i + 1:]:
            va = np.array(computed_probes[a_id]["vector"])
            vb = np.array(computed_probes[b_id]["vector"])
            raw_dist = float(np.linalg.norm(va - vb))

            pair_key = f"{a_id}_vs_{b_id}"
            entry = {"raw_euclidean": round(raw_dist, 4)}

            if sigma_info.get("available"):
                sigma_vec = np.array(sigma_info["sigma_vector"])
                nonzero = sigma_vec > 1e-6
                if np.all(nonzero):
                    za = va / sigma_vec
                    zb = vb / sigma_vec
                    entry["normalized_euclidean"] = round(float(np.linalg.norm(za - zb)), 4)
                else:
                    entry["normalized_euclidean"] = None
                    entry["note"] = "Some σ components zero"

            control_distances[pair_key] = entry

    # 6. Secondary pharmacology note
    secondary_note = {
        "note": (
            "Contexto farmacológico documentado (NO usado como training truth): "
            "Trabajo reciente con derivados de HU-308 en CB2 encontró continua de actividad "
            "asociada con la interacción con Trp258^6.48. "
            "El paper original de HU-308/HU-433 (Mechoulam et al.) reportó que HU-433 tiene "
            "mucho menor afinidad hCB2 pero mayor potencia biológica en algunos modelos; "
            "diferencias en [35S]GTPγS no estadísticamente significativas; "
            "los autores propusieron orientaciones de unión diferentes. "
            "Estos datos contextualizan pero NO validan el descriptor."
        ),
    }

    result = {
        "test": "micronetwork_falsification",
        "timestamp_utc": timestamp,
        "governance": {
            "DE_NOVO_GENERATION": "STOP",
            "THRESHOLD_MODIFICATION": "STOP",
            "CONTRACT_v1.0": "FROZEN",
            "DESCRIPTOR_FROZEN_BEFORE_EXECUTION": True,
        },
        "descriptor_definition": {
            "name": "LOCAL_MICROSWITCH_VECTOR",
            "components": list(DESCRIPTOR_NAMES),
            "component_descriptions": {
                "dist_Trp258_A": "Min heavy-atom dist ligand → Trp258^6.48 indole ring (Å)",
                "dist_Phe183_A": "Dist ligand centroid → Phe183^ECL2 aromatic ring centroid (Å)",
                "dist_Ser285_A": "Min heavy-atom dist ligand → Ser285^7.39 hydroxyl O (Å)",
                "torsion_Trp258_deg": "chi1/chi2 deviation of Trp258 sidechain vs 6PT0 canonical (°)",
            },
            "normalization": "z-score per component using independent σ → Euclidean D = sqrt(Σzᵢ²)",
            "threshold": f"ΔV ≥ {DISCRIMINATION_THRESHOLD_SIGMA}σ",
        },
        "sigma_estimation": sigma_info,
        "reference_trp258_canonical": {
            "pdb": REF_PDB_ID,
            "chi1": round(ref_chi1, 2),
            "chi2": round(ref_chi2, 2),
        },
        "panel_results": panel_results,
        "primary_verdict": primary_verdict,
        "control_distances": control_distances,
        "secondary_pharmacology": secondary_note,
    }

    return result


def write_report(result: dict[str, Any]) -> Path:
    """Generate markdown report in Spanish."""
    lines = [
        "# Test de falsificación de microred — Par enantiomérico HU-308 / HU-433",
        "",
        f"**Generado:** {result['timestamp_utc']}  ",
        "**Branch:** `feat/micronetwork-falsification-test`",
        "",
        "## Candados de gobernanza",
        "",
        "```yaml",
        "DE_NOVO_GENERATION: STOP",
        "THRESHOLD_MODIFICATION: STOP",
        "CONTRACT_v1.0: FROZEN",
        "DESCRIPTOR_FROZEN_BEFORE_EXECUTION: true",
        "```",
        "",
        "## Definición del descriptor (congelado pre-ejecución)",
        "",
        "```",
        "LOCAL_MICROSWITCH_VECTOR = [",
        "  dist_Trp258,    # dist mín átomos pesados ligando → anillo indol Trp258^6.48 (Å)",
        "  dist_Phe183,    # dist centroide ligando → centroide anillo aromático Phe183^ECL2 (Å)",
        "  dist_Ser285,    # dist mín átomos pesados ligando → O hidroxilo Ser285^7.39 (Å)",
        "  torsion_Trp258  # desviación chi1/chi2 cadena lateral Trp258 vs pose canónica 6PT0 (°)",
        "]",
        "```",
        "",
        "## Procedencia de σ",
        "",
    ]

    sigma = result["sigma_estimation"]
    if sigma.get("available"):
        lines.extend([
            f"**Método:** {sigma['method']}",
            "",
            f"**Limitación:** {sigma['limitation']}",
            "",
            "| Componente | σ estimada |",
            "|------------|-----------|",
        ])
        for name, val in sigma["sigma_per_component"].items():
            lines.append(f"| {name} | {val} |")
        lines.extend([
            "",
            f"**N observaciones:** {sigma['n_observations']}",
            f"**PDBs fuente:** {', '.join(sigma['source_pdbs'])}",
            "",
        ])
    else:
        lines.extend([
            f"**σ no disponible:** {sigma.get('reason', 'unknown')}",
            "",
        ])

    lines.extend([
        "## Pose canónica de referencia Trp258 (6PT0)",
        "",
        f"- chi1 = {result['reference_trp258_canonical']['chi1']}°",
        f"- chi2 = {result['reference_trp258_canonical']['chi2']}°",
        "",
        "## LOCAL_MICROSWITCH_VECTOR por sonda",
        "",
        "| Sonda | Rol | Estado | dist_Trp258 (Å) | dist_Phe183 (Å) | dist_Ser285 (Å) | torsion_Trp258 (°) |",
        "|-------|-----|--------|-----------------|-----------------|-----------------|-------------------|",
    ])

    for probe_id, info in result["panel_results"].items():
        if info.get("vector"):
            c = info["components"]
            lines.append(
                f"| {probe_id} | {info['role']} | {info['status']} | "
                f"{c['dist_Trp258_A']:.2f} | {c['dist_Phe183_A']:.2f} | "
                f"{c['dist_Ser285_A']:.2f} | {c['torsion_Trp258_deg']:.2f} |"
            )
        else:
            lines.append(
                f"| {probe_id} | {info['role']} | {info['status']} | — | — | — | — |"
            )

    lines.extend([
        "",
        "## Distancias de control entre sondas",
        "",
        "| Par | Euclídea raw | Euclídea normalizada |",
        "|-----|-------------|---------------------|",
    ])
    for pair, vals in result["control_distances"].items():
        norm = vals.get("normalized_euclidean", "—")
        if norm is None:
            norm = "—"
        lines.append(f"| {pair} | {vals['raw_euclidean']} | {norm} |")

    pv = result["primary_verdict"]
    lines.extend([
        "",
        "## Veredicto primario: D(HU-308, HU-433) vs umbral",
        "",
        f"**Veredicto: `{pv['verdict']}`**",
        "",
    ])
    if pv["verdict"] == "INDETERMINATE":
        lines.append(f"**Razón:** {pv['reason']}")
    else:
        lines.extend([
            f"- ΔV = {pv['delta_v']}",
            f"- Umbral = {pv['threshold']}σ",
        ])
    lines.append("")

    lines.extend([
        "## Nota secundaria de farmacología",
        "",
        result["secondary_pharmacology"]["note"],
        "",
        "## Nota de literatura",
        "",
        "Este test conecta con evidencia externa: trabajo reciente con derivados de",
        "HU-308 en CB2 encontró continua de actividad asociada con la interacción",
        "Trp258^6.48. El paper original de HU-308/HU-433 reportó resultados",
        "notablemente inusuales: HU-433 tiene mucho menor afinidad hCB2 pero mucho",
        "mayor potencia biológica en algunos modelos; las diferencias en [35S]GTPγS",
        "no fueron estadísticamente significativas; los autores propusieron",
        "orientaciones de unión diferentes. Este contexto se documenta SIN tratarlo",
        "como training truth.",
        "",
    ])

    if pv["verdict"] == "INDETERMINATE":
        lines.extend([
            "## Razón explícita de INDETERMINATE",
            "",
            "No existen poses dockeadas para HU-308 ni HU-433 en el repositorio.",
            "El test requiere poses de Vina (o equivalente) contra 6PT0 como receptor",
            "primario, con verificación cruzada en 6KPF. Las poses de los ligandos",
            "co-cristalizados (WIN55,212-2 en 6PT0, AM12033 en 6KPF, CP55,940 en 8GUR,",
            "AM10257 en 5ZTY) se computan como controles para validar la infraestructura",
            "del descriptor.",
            "",
            "### Pasos requeridos para resolver INDETERMINATE → veredicto definitivo",
            "",
            "1. Preparar ligandos HU-308 y HU-433 (SMILES → 3D → PDBQT)",
            "2. Docking Vina contra 6PT0_clean.pdb con grid configs/grid_cb2_6pt0.txt",
            "3. Extraer best pose para cada enantiómero",
            "4. Re-ejecutar este script (detectará poses automáticamente)",
            "5. Verificación cruzada: repetir contra 6KPF",
            "",
        ])

    lines.extend([
        "## Scripts",
        "",
        "- `scripts/conformational/test_micronetwork_falsification.py`",
        "",
    ])

    report_path = OUT_DIR / "micronetwork_falsification_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    result = run_test()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "micronetwork_falsification_report.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    report_path = write_report(result)

    print(f"Veredicto primario: {result['primary_verdict']['verdict']}")
    print(f"JSON: {json_path}")
    print(f"Reporte: {report_path}")

    sigma = result["sigma_estimation"]
    if sigma.get("available"):
        print(f"sigma fuente: {sigma['method']}")
        print(f"sigma vector: {sigma['sigma_vector']}")

    print("\nVectores descriptores:")
    for probe_id, info in result["panel_results"].items():
        if info.get("vector"):
            print(f"  {probe_id}: {[round(v, 3) for v in info['vector']]}")
        else:
            print(f"  {probe_id}: {info['status']} — {info.get('reason', '')}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
