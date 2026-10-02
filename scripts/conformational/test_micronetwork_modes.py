#!/usr/bin/env python3
"""
Micronetwork local-mode test — HU-308 vs HU-433 on 6PT0 and 6KPF.

Computes frozen LOCAL_MICROSWITCH_VECTOR per probe and applies FROZEN verdict:
  DISTINCT_LOCAL_MODES: Δd > 0.3 Å in ≥2 distance components OR Δχ₁ > 10°
  IDENTICAL_LOCAL_MODES: neither criterion met
  INDETERMINATE: missing poses or state disagreement (plasticity)

Cross-link: results/conformational/micronetwork_falsification_report.md
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

from scripts.conformational.pdb_utils import (  # noqa: E402
    atom_xyz,
    dihedral,
    read_atoms,
)
from scripts.conformational.residue_maps import MICROSWITCHS, STRUCTURES  # noqa: E402

DESCRIPTOR_NAMES = (
    "dist_Trp258_A",
    "dist_Phe183_A",
    "dist_Ser285_A",
    "torsion_Trp258_deg",
)
DISTANCE_KEYS = DESCRIPTOR_NAMES[:3]
DIST_DELTA_A = 0.3
TORSION_DELTA_DEG = 10.0
MIN_DIST_COMPONENTS = 2

MS = MICROSWITCHS["cb2"]
REF_PDB_ID = "6PT0"
POSE_ROOT = ROOT / "data/docking_poses/micronetwork_test"
OUT_DIR = ROOT / "results/conformational"
FALSIFICATION_LINK = OUT_DIR / "micronetwork_falsification_report.md"

# Co-crystal control vectors from micronetwork_falsification_report (frozen reference)
CONTROL_VECTORS = {
    "6PT0": [4.92, 4.21, 3.35, 0.00],
    "6KPF": [3.87, 3.86, 3.07, 33.14],
    "8GUR_CP55940": [4.89, 4.55, 2.61, 22.03],
    "5ZTY_AM10257": [3.91, 4.16, 4.49, 46.24],
}

PROBES = ("HU-308", "HU-433")
STATES = ("6PT0", "6KPF")


def _trp258_indole_atoms(atoms: list) -> list[np.ndarray]:
    indole_names = {"CG", "CD1", "NE1", "CE2", "CD2", "CZ2", "CH2", "CZ3", "CE3"}
    return [
        xyz.copy()
        for rn, _ch, rs, an, xyz in atoms
        if rs == MS.trp648 and rn.upper() == "TRP" and an in indole_names
    ]


def _phe183_ring_centroid(atoms: list) -> np.ndarray | None:
    ring_names = {"CG", "CD1", "CE1", "CZ", "CE2", "CD2"}
    coords = [
        xyz.copy()
        for rn, _ch, rs, an, xyz in atoms
        if rs == MS.phe_ecl2 and rn.upper() == "PHE" and an in ring_names
    ]
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
    return dihedral(n, ca, cb, cg), dihedral(ca, cb, cg, cd1)


def _angular_deviation(chi1: float, chi2: float, ref_chi1: float, ref_chi2: float) -> float:
    def _delta(a: float, b: float) -> float:
        d = abs(a - b) % 360
        return min(d, 360 - d)

    return math.sqrt(_delta(chi1, ref_chi1) ** 2 + _delta(chi2, ref_chi2) ** 2)


def _parse_ligand_heavy_coords_pdbqt(pdbqt_path: Path) -> list[np.ndarray]:
    coords: list[np.ndarray] = []
    in_model = False
    for line in pdbqt_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("MODEL"):
            in_model = True
            continue
        if line.startswith("ENDMDL"):
            break
        if not in_model or not line.startswith(("ATOM", "HETATM")):
            continue
        elem = line[77:79].strip() if len(line) >= 79 else line[12:14].strip()[0]
        if elem.upper() == "H":
            continue
        coords.append(
            np.array(
                [float(line[30:38]), float(line[38:46]), float(line[46:54])],
                dtype=float,
            )
        )
    return coords


def _min_dist_to_atoms(query: list[np.ndarray], target: list[np.ndarray]) -> float:
    min_d = float("inf")
    for q in query:
        for t in target:
            min_d = min(min_d, float(np.linalg.norm(q - t)))
    return min_d


def _resolve_receptor_pdb(pdb_id: str) -> tuple[Path, str | None]:
    spec = next((s for s in STRUCTURES if s.pdb_id == pdb_id), None)
    chain = spec.chain if spec else None
    for candidate in (
        ROOT / f"data/targets/cb2_multistate/{pdb_id}_clean.pdb",
        ROOT / f"data/targets/cb2/{pdb_id}_clean.pdb",
    ):
        if candidate.exists():
            return candidate, chain
    raise FileNotFoundError(f"No clean receptor PDB for {pdb_id}")


def _pose_path(pdb_id: str, ligand_id: str) -> Path:
    return POSE_ROOT / pdb_id / ligand_id / f"{ligand_id}_docked.pdbqt"


def compute_vector_from_docked_pose(
    pdb_id: str,
    docked_pdbqt: Path,
    ref_chi1: float,
    ref_chi2: float,
) -> dict[str, Any] | None:
    receptor_pdb, chain = _resolve_receptor_pdb(pdb_id)
    chains = {chain} if chain else None
    rec_atoms = read_atoms(receptor_pdb, chains=chains)
    lig_coords = _parse_ligand_heavy_coords_pdbqt(docked_pdbqt)
    if not lig_coords:
        return None

    lig_centroid = np.mean(np.stack(lig_coords), axis=0)
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
        "receptor_pdb": str(receptor_pdb),
        "docked_pdbqt": str(docked_pdbqt),
    }


def _pair_verdict(v_a: list[float], v_b: list[float]) -> dict[str, Any]:
    deltas = [abs(a - b) for a, b in zip(v_a, v_b)]
    dist_deltas = deltas[:3]
    torsion_delta = deltas[3]
    n_dist_over = sum(1 for d in dist_deltas if d > DIST_DELTA_A)
    torsion_over = torsion_delta > TORSION_DELTA_DEG

    if n_dist_over >= MIN_DIST_COMPONENTS or torsion_over:
        verdict = "DISTINCT_LOCAL_MODES"
    else:
        verdict = "IDENTICAL_LOCAL_MODES"

    return {
        "verdict": verdict,
        "delta_vector": dict(zip(DESCRIPTOR_NAMES, [round(d, 4) for d in deltas])),
        "distance_components_over_0.3A": n_dist_over,
        "torsion_over_10deg": torsion_over,
        "criteria": {
            "DIST_DELTA_A": DIST_DELTA_A,
            "MIN_DIST_COMPONENTS": MIN_DIST_COMPONENTS,
            "TORSION_DELTA_DEG": TORSION_DELTA_DEG,
        },
    }


def _aggregate_verdict(per_state: dict[str, dict[str, Any]]) -> dict[str, Any]:
    state_verdicts = {s: per_state[s]["pair_verdict"]["verdict"] for s in STATES}
    missing = [s for s in STATES if per_state[s].get("status") != "COMPUTED"]
    if missing:
        return {
            "verdict": "INDETERMINATE",
            "reason": f"Missing or failed poses for states: {missing}",
            "per_state_verdicts": state_verdicts,
        }

    unique = set(state_verdicts.values())
    if len(unique) == 1:
        return {
            "verdict": state_verdicts["6PT0"],
            "reason": "Reproducible across 6PT0 and 6KPF",
            "per_state_verdicts": state_verdicts,
        }

    return {
        "verdict": "INDETERMINATE",
        "reason": (
            "State disagreement (plasticity): "
            f"6PT0={state_verdicts['6PT0']}, 6KPF={state_verdicts['6KPF']}. "
            "Difference in one state not reproduced in the other."
        ),
        "per_state_verdicts": state_verdicts,
        "plasticity_note": True,
    }


def run_test() -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    ref_pdb, ref_chain = _resolve_receptor_pdb(REF_PDB_ID)
    ref_atoms = read_atoms(ref_pdb, chains={ref_chain} if ref_chain else None)
    ref_chi = _trp258_chi1_chi2(ref_atoms)
    if ref_chi is None:
        raise RuntimeError("Cannot extract Trp258 chi from 6PT0 reference")
    ref_chi1, ref_chi2 = ref_chi

    probes: dict[str, Any] = {}
    for lig in PROBES:
        probes[lig] = {"by_state": {}}
        for pdb_id in STATES:
            pose = _pose_path(pdb_id, lig)
            entry: dict[str, Any] = {"pose_path": str(pose)}
            if not pose.exists():
                entry["status"] = "NO_POSE"
                entry["vector"] = None
            else:
                desc = compute_vector_from_docked_pose(pdb_id, pose, ref_chi1, ref_chi2)
                if desc is None:
                    entry["status"] = "EXTRACTION_FAILED"
                    entry["vector"] = None
                else:
                    entry["status"] = "COMPUTED"
                    entry["vector"] = desc["vector"]
                    entry["components"] = desc["components"]
                    entry["docked_pdbqt"] = desc["docked_pdbqt"]
            probes[lig]["by_state"][pdb_id] = entry

    per_state: dict[str, Any] = {}
    for pdb_id in STATES:
        v308 = probes["HU-308"]["by_state"][pdb_id].get("vector")
        v433 = probes["HU-433"]["by_state"][pdb_id].get("vector")
        if v308 is None or v433 is None:
            per_state[pdb_id] = {
                "status": "INCOMPLETE",
                "pair_verdict": {"verdict": "INDETERMINATE", "reason": "missing pose(s)"},
            }
        else:
            pv = _pair_verdict(v308, v433)
            per_state[pdb_id] = {
                "status": "COMPUTED",
                "HU-308_vector": v308,
                "HU-433_vector": v433,
                "pair_verdict": pv,
            }

    primary = _aggregate_verdict(per_state)

    return {
        "test": "micronetwork_local_modes",
        "timestamp_utc": timestamp,
        "primary_question": (
            "¿HU-308 y HU-433 presentan microdescriptores locales reproduciblemente diferentes?"
        ),
        "cross_link": str(FALSIFICATION_LINK.relative_to(ROOT)),
        "descriptor_definition": {
            "name": "LOCAL_MICROSWITCH_VECTOR",
            "components": list(DESCRIPTOR_NAMES),
            "frozen_verdict_criteria": {
                "DISTINCT_LOCAL_MODES": (
                    f"Δd > {DIST_DELTA_A} Å in ≥{MIN_DIST_COMPONENTS} distance components "
                    f"OR Δtorsion > {TORSION_DELTA_DEG}°"
                ),
                "IDENTICAL_LOCAL_MODES": "neither criterion met",
                "INDETERMINATE": "missing poses or state disagreement",
            },
        },
        "reference_trp258_canonical_6PT0": {
            "chi1": round(ref_chi1, 2),
            "chi2": round(ref_chi2, 2),
        },
        "control_vectors_cocrystal": CONTROL_VECTORS,
        "probes": probes,
        "per_state_comparison": per_state,
        "primary_verdict": primary,
    }


def write_report(result: dict[str, Any]) -> Path:
    pv = result["primary_verdict"]
    lines = [
        "# Micronetwork local modes — HU-308 vs HU-433",
        "",
        f"**Generado:** {result['timestamp_utc']}  ",
        "**Branch:** `feat/micronetwork-falsification-test`",
        "",
        f"**Pregunta primaria:** {result['primary_question']}",
        "",
        f"**Enlace falsificación previa:** [`{result['cross_link']}`]({result['cross_link']})",
        "",
        "## Veredicto definitivo",
        "",
        f"**`{pv['verdict']}`**",
        "",
        f"*{pv.get('reason', '')}*",
        "",
        "## Criterios congelados (resolución estructural, no incertidumbre de docking)",
        "",
        "| Criterio | Regla |",
        "|----------|-------|",
        f"| DISTINCT_LOCAL_MODES | Δd > {DIST_DELTA_A} Å en ≥{MIN_DIST_COMPONENTS} componentes de distancia "
        f"**o** Δtorsion > {TORSION_DELTA_DEG}° |",
        "| IDENTICAL_LOCAL_MODES | Ningún criterio cumplido |",
        "| INDETERMINATE | Poses ausentes o discrepancia entre 6PT0 y 6KPF |",
        "",
        "## LOCAL_MICROSWITCH_VECTOR por sonda y estado",
        "",
        "| Estado | Sonda | Pose | dist_Trp258 (Å) | dist_Phe183 (Å) | dist_Ser285 (Å) | torsion_Trp258 (°) |",
        "|--------|-------|------|-----------------|-----------------|-----------------|-------------------|",
    ]

    for pdb_id in STATES:
        for lig in PROBES:
            info = result["probes"][lig]["by_state"][pdb_id]
            raw_pose = info.get("docked_pdbqt") or info.get("pose_path", "—")
            try:
                pose = str(Path(raw_pose).relative_to(ROOT)) if raw_pose != "—" else "—"
            except ValueError:
                pose = raw_pose
            if info.get("vector"):
                c = info["components"]
                lines.append(
                    f"| {pdb_id} | {lig} | `{pose}` | "
                    f"{c['dist_Trp258_A']:.2f} | {c['dist_Phe183_A']:.2f} | "
                    f"{c['dist_Ser285_A']:.2f} | {c['torsion_Trp258_deg']:.2f} |"
                )
            else:
                lines.append(
                    f"| {pdb_id} | {lig} | — | — | — | — | — ({info['status']}) |"
                )

    lines.extend(["", "## Comparación HU-308 vs HU-433 por estado", ""])
    for pdb_id in STATES:
        st = result["per_state_comparison"][pdb_id]
        pv_s = st.get("pair_verdict", {})
        lines.append(f"### {pdb_id}")
        if st.get("status") == "COMPUTED":
            dv = pv_s.get("delta_vector", {})
            lines.extend([
                f"- **Veredicto estado:** `{pv_s['verdict']}`",
                f"- Δdist_Trp258 = {dv.get('dist_Trp258_A', '—')} Å",
                f"- Δdist_Phe183 = {dv.get('dist_Phe183_A', '—')} Å",
                f"- Δdist_Ser285 = {dv.get('dist_Ser285_A', '—')} Å",
                f"- Δtorsion_Trp258 = {dv.get('torsion_Trp258_deg', '—')}°",
                f"- Componentes dist > {DIST_DELTA_A} Å: {pv_s.get('distance_components_over_0.3A')}",
                "",
            ])
        else:
            lines.append(f"- **Estado:** INCOMPLETE — {pv_s.get('reason', '')}")
            lines.append("")

    lines.extend([
        "## Controles co-cristal (vectores de referencia, sin re-dock)",
        "",
        "| Control | dist_Trp258 | dist_Phe183 | dist_Ser285 | torsion_Trp258 |",
        "|---------|-------------|-------------|-------------|----------------|",
    ])
    for name, vec in result["control_vectors_cocrystal"].items():
        lines.append(
            f"| {name} | {vec[0]:.2f} | {vec[1]:.2f} | {vec[2]:.2f} | {vec[3]:.2f} |"
        )

    lines.extend([
        "",
        "## Scripts",
        "",
        "- `scripts/run_micronetwork_directed_dock.py`",
        "- `scripts/conformational/test_micronetwork_modes.py`",
        "",
    ])

    report_path = OUT_DIR / "micronetwork_modes_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    result = run_test()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "micronetwork_modes_report.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    report_path = write_report(result)

    print(f"Veredicto: {result['primary_verdict']['verdict']}")
    print(f"JSON: {json_path}")
    print(f"Reporte: {report_path}")
    for pdb_id in STATES:
        st = result["per_state_comparison"][pdb_id]
        if st.get("HU-308_vector"):
            print(f"  {pdb_id} HU-308: {[round(v, 3) for v in st['HU-308_vector']]}")
            print(f"  {pdb_id} HU-433: {[round(v, 3) for v in st['HU-433_vector']]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
