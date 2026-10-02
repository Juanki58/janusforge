#!/usr/bin/env python3
"""Phase G — 8GUR out-of-sample generalization of CB2 conformational coordinate."""

from __future__ import annotations

import argparse
import hashlib
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

from scripts.conformational.align_multistate import run_alignment  # noqa: E402
from scripts.conformational.extract_fingerprint import (  # noqa: E402
    FEATURE_NAMES as PHASE_F_FEATURES,
    extract_fingerprint,
)
from scripts.conformational.pdb_utils import (  # noqa: E402
    atom_xyz,
    ca_coords_by_resseq,
    dihedral,
    read_atoms,
)
from scripts.conformational.residue_maps import (  # noqa: E402
    MICROSWITCHS,
    STRUCTURES,
    TM_HELICES,
)

OUT_DIR = ROOT / "results/conformational"
JSON_OUT = OUT_DIR / "fase_g_generalization_report.json"
MD_OUT = OUT_DIR / "fase_g_generalization_report.md"

CB2_OOS_IDS = ("6PT0", "6KPF", "8GUR", "5ZTY")
CB2_ACTIVE_REFS = ("6PT0", "6KPF")
CB2_NEGATIVE = "5ZTY"
CB2_BLIND = "8GUR"

CB1_IDS = ("5TGZ", "5XRA")
CB1_ACTIVE = "5XRA"
CB1_INACTIVE = "5TGZ"

EXPLORATORY_DELTA_CUTOFF_A = 2.0  # exploratory only — not confirmatory

GOVERNANCE = {
    "PHASE_G": "COMPLETE",
    "CONTRACT_v1.0": "FROZEN",
    "DE_NOVO_GENERATION": "STOP",
    "THRESHOLD_MODIFICATION": "STOP",
    "ALLOSTERIC_FRAMEWORK": "HYPOTHESIS_PENDING_CALIBRATION",
    "EXPLORATORY_DELTA_CUTOFF": "documented_as_exploratory_only",
}

# CB1 uses CB2-homolog features except Ser268 (absent in CB1 map).
CB1_G_FEATURE_NAMES = (
    "tm3_tm6_ic_distance_A",
    "tm3_tm5_centroid_displacement_A",
    "trp258_chi1_deg",
    "trp258_chi2_deg",
    "phe183_ecl2_ca_displacement_A",
    "phe183_aromatic_tilt_deg",
)
# Phase G feature vector (CB2 coordinate space).
G_FEATURE_NAMES = (
    "tm3_tm6_ic_distance_A",
    "tm3_tm5_centroid_displacement_A",
    "trp258_chi1_deg",
    "trp258_chi2_deg",
    "ser268_chi1_deg",
    "phe183_ecl2_ca_displacement_A",
    "phe183_aromatic_tilt_deg",
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _helix_centroid(atoms, receptor: str, helix_idx: int) -> np.ndarray:
    lo, hi = TM_HELICES[receptor][helix_idx]
    ca = ca_coords_by_resseq(atoms, range(lo, hi + 1))
    if not ca:
        raise RuntimeError(f"No Cα for helix {helix_idx} in {receptor}")
    return np.mean(np.stack(list(ca.values())), axis=0)


def extract_g_metrics(
    pdb_path: Path,
    receptor: str,
    pdb_id: str,
    reference_phe_ca: np.ndarray | None = None,
) -> dict[str, Any]:
    """Extract Phase G metrics reusing Phase F helpers where applicable."""
    ms = MICROSWITCHS[receptor]
    spec = next(s for s in STRUCTURES if s.pdb_id == pdb_id)
    chains = {spec.chain} if spec.chain else None
    atoms = read_atoms(pdb_path, chains=chains)

    arg_ca = atom_xyz(atoms, ms.arg350, "ARG", "CA")
    lys_ca = atom_xyz(atoms, ms.lys635, "LYS", "CA")
    if arg_ca is None or lys_ca is None:
        raise RuntimeError(f"Missing Arg3.50/Lys6.35 in {pdb_id}")
    tm3_tm6 = float(np.linalg.norm(arg_ca - lys_ca))

    tm3_cent = _helix_centroid(atoms, receptor, 2)
    tm5_cent = _helix_centroid(atoms, receptor, 4)
    tm3_tm5_disp = float(np.linalg.norm(tm3_cent - tm5_cent))

    trp_n = atom_xyz(atoms, ms.trp648, "TRP", "N")
    trp_ca = atom_xyz(atoms, ms.trp648, "TRP", "CA")
    trp_cb = atom_xyz(atoms, ms.trp648, "TRP", "CB")
    trp_cg = atom_xyz(atoms, ms.trp648, "TRP", "CG")
    trp_cd1 = atom_xyz(atoms, ms.trp648, "TRP", "CD1")
    if any(x is None for x in (trp_n, trp_ca, trp_cb, trp_cg, trp_cd1)):
        raise RuntimeError(f"Missing Trp6.48 in {pdb_id}")
    trp_chi1 = dihedral(trp_n, trp_ca, trp_cb, trp_cg)
    trp_chi2 = dihedral(trp_ca, trp_cb, trp_cg, trp_cd1)

    ser268_chi1 = float("nan")
    if ms.ser658:
        ser_n = atom_xyz(atoms, ms.ser658, "SER", "N")
        ser_ca = atom_xyz(atoms, ms.ser658, "SER", "CA")
        ser_cb = atom_xyz(atoms, ms.ser658, "SER", "CB")
        ser_og = atom_xyz(atoms, ms.ser658, "SER", "OG")
        if all(x is not None for x in (ser_n, ser_ca, ser_cb, ser_og)):
            ser268_chi1 = dihedral(ser_n, ser_ca, ser_cb, ser_og)

    phe_ca = atom_xyz(atoms, ms.phe_ecl2, "PHE", "CA")
    phe_cz = atom_xyz(atoms, ms.phe_ecl2, "PHE", "CZ")
    if phe_ca is None or phe_cz is None:
        raise RuntimeError(f"Missing Phe ECL2 in {pdb_id}")
    ecl2_disp = (
        float(np.linalg.norm(phe_ca - reference_phe_ca))
        if reference_phe_ca is not None
        else 0.0
    )
    aromatic_vec = phe_cz - phe_ca
    aromatic_tilt = math.degrees(
        math.acos(
            np.clip(
                abs(aromatic_vec[2]) / (np.linalg.norm(aromatic_vec) + 1e-9),
                -1.0,
                1.0,
            )
        )
    )

    vec = np.array(
        [
            tm3_tm6,
            tm3_tm5_disp,
            trp_chi1,
            trp_chi2,
            ser268_chi1,
            ecl2_disp,
            aromatic_tilt,
        ],
        dtype=float,
    )
    return {
        "pdb_id": pdb_id,
        "receptor": receptor,
        "state_label": spec.state_label,
        "features": {k: round(float(v), 4) for k, v in zip(G_FEATURE_NAMES, vec)},
        "feature_vector": [round(float(v), 4) for v in vec],
    }


def extract_cb1_g_metrics(
    pdb_path: Path,
    pdb_id: str,
    reference_phe_ca: np.ndarray,
) -> dict[str, Any]:
    """CB1 coordinate features (no Ser268 — CB2-specific vestibular node)."""
    ms = MICROSWITCHS["cb1"]
    spec = next(s for s in STRUCTURES if s.pdb_id == pdb_id)
    chains = {spec.chain} if spec.chain else None
    atoms = read_atoms(pdb_path, chains=chains)

    arg_ca = atom_xyz(atoms, ms.arg350, "ARG", "CA")
    lys_ca = atom_xyz(atoms, ms.lys635, "LYS", "CA")
    tm3_tm6 = float(np.linalg.norm(arg_ca - lys_ca))
    tm3_cent = _helix_centroid(atoms, "cb1", 2)
    tm5_cent = _helix_centroid(atoms, "cb1", 4)
    tm3_tm5_disp = float(np.linalg.norm(tm3_cent - tm5_cent))

    trp_n = atom_xyz(atoms, ms.trp648, "TRP", "N")
    trp_ca = atom_xyz(atoms, ms.trp648, "TRP", "CA")
    trp_cb = atom_xyz(atoms, ms.trp648, "TRP", "CB")
    trp_cg = atom_xyz(atoms, ms.trp648, "TRP", "CG")
    trp_cd1 = atom_xyz(atoms, ms.trp648, "TRP", "CD1")
    trp_chi1 = dihedral(trp_n, trp_ca, trp_cb, trp_cg)
    trp_chi2 = dihedral(trp_ca, trp_cb, trp_cg, trp_cd1)

    phe_ca = atom_xyz(atoms, ms.phe_ecl2, "PHE", "CA")
    phe_cz = atom_xyz(atoms, ms.phe_ecl2, "PHE", "CZ")
    ecl2_disp = float(np.linalg.norm(phe_ca - reference_phe_ca))
    aromatic_vec = phe_cz - phe_ca
    aromatic_tilt = math.degrees(
        math.acos(
            np.clip(
                abs(aromatic_vec[2]) / (np.linalg.norm(aromatic_vec) + 1e-9),
                -1.0,
                1.0,
            )
        )
    )

    vec = np.array(
        [tm3_tm6, tm3_tm5_disp, trp_chi1, trp_chi2, ecl2_disp, aromatic_tilt],
        dtype=float,
    )
    return {
        "pdb_id": pdb_id,
        "receptor": "cb1",
        "state_label": spec.state_label,
        "features": {k: round(float(v), 4) for k, v in zip(CB1_G_FEATURE_NAMES, vec)},
        "feature_vector": [round(float(v), 4) for v in vec],
    }


def _normalize_cb1(
    vectors: dict[str, np.ndarray],
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    fit_ids = CB1_IDS
    mat = np.stack([vectors[i] for i in fit_ids])
    mean = mat.mean(axis=0)
    std = mat.std(axis=0)
    std[std < 1e-9] = 1.0
    norm = {k: (vectors[k] - mean) / std for k in vectors}
    return norm, {
        "fit_ids": list(fit_ids),
        "mean": mean.tolist(),
        "std": std.tolist(),
        "feature_names": list(CB1_G_FEATURE_NAMES),
    }


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]
    return obj


def _normalize(
    vectors: dict[str, np.ndarray],
    fit_ids: tuple[str, ...],
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    mat = np.stack([vectors[i] for i in fit_ids])
    mean = mat.mean(axis=0)
    std = mat.std(axis=0)
    std[std < 1e-9] = 1.0
    norm = {k: (vectors[k] - mean) / std for k in vectors}
    return norm, {
        "fit_ids": list(fit_ids),
        "mean": mean.tolist(),
        "std": std.tolist(),
        "feature_names": list(G_FEATURE_NAMES),
    }


def _dist(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def _verdict_oos(
    distances: dict[str, float],
    active_ids: tuple[str, ...],
    negative_id: str,
    blind_id: str,
) -> tuple[str, str]:
    d_blind = distances[blind_id]
    d_neg = distances[negative_id]
    d_active_mean = float(np.mean([distances[i] for i in active_ids]))
    d_active_max = max(distances[i] for i in active_ids)

    sep_blind_neg = d_neg - d_blind
    sep_blind_active_mean = d_active_mean - d_blind

    if d_blind >= d_neg:
        return (
            "FALSIFIED",
            f"{blind_id} ({d_blind:.3f}) ≥ inactive {negative_id} ({d_neg:.3f}); "
            "blind active falls in or beyond inactive region.",
        )
    if d_blind <= d_active_max + 0.5 and sep_blind_neg > 1.0:
        return (
            "GENERALIZES",
            f"{blind_id} ({d_blind:.3f}) clusters with active refs "
            f"(mean {d_active_mean:.3f}, max {d_active_max:.3f}) and "
            f"separates from {negative_id} ({d_neg:.3f}); Δ(blind→inactive)={sep_blind_neg:.3f} norm units.",
        )
    if sep_blind_neg > 0 and sep_blind_active_mean >= -0.5:
        return (
            "PARTIAL",
            f"Trend toward active cluster (blind {d_blind:.3f} vs inactive {d_neg:.3f}) "
            f"but margin vs active mean ({d_active_mean:.3f}) is not robust.",
        )
    return (
        "FALSIFIED",
        f"Separation not reproduced: blind {d_blind:.3f}, active mean {d_active_mean:.3f}, "
        f"inactive {d_neg:.3f}.",
    )


def _level0_verify(manifest: dict, metrics: dict[str, dict]) -> dict[str, Any]:
    notes: list[str] = []
    ok = True
    blind_entry = next(
        (e for e in manifest["aligned_structures"] if e["pdb_id"] == CB2_BLIND),
        None,
    )
    if blind_entry is None:
        ok = False
        notes.append("8GUR missing from alignment manifest.")
    else:
        if blind_entry.get("receptor") != "cb2":
            ok = False
            notes.append("8GUR receptor identity not CB2.")
        if blind_entry.get("chain") != "R":
            ok = False
            notes.append(f"8GUR chain expected R, got {blind_entry.get('chain')}.")
        if blind_entry.get("ligand_resname") != "9GF":
            notes.append(
                f"Ligand resname {blind_entry.get('ligand_resname')} (expected 9GF CP55,940)."
            )
        if blind_entry.get("state_label") != "active_agonist_cp55940_gi":
            notes.append(f"State label: {blind_entry.get('state_label')}.")
        if blind_entry.get("tm_ca_pairs", 0) < 30:
            ok = False
            notes.append("Too few TM Cα pairs for 8GUR alignment.")
    if CB2_BLIND not in metrics:
        ok = False
        notes.append("8GUR fingerprint extraction failed.")
    return {
        "passed": ok,
        "pdb_id": CB2_BLIND,
        "resolution_A": 2.84,
        "receptor": "CB2",
        "chain": "R",
        "ligand": "CP55,940 (9GF)",
        "state": "active_agonist_cp55940_gi",
        "notes": notes,
    }


def _load_thcv_secondary() -> dict[str, Any]:
    thcv_json = ROOT / "results/docking/thcv_seed/thcv_seed_evaluation.json"
    if not thcv_json.exists():
        return {"available": False, "note": "THCV seed evaluation JSON absent"}
    data = json.loads(thcv_json.read_text(encoding="utf-8"))
    thcv = data.get("thcv", {})
    return {
        "available": True,
        "source": str(thcv_json),
        "cb2": {
            "docked_receptor_state": "6PT0 (active agonist)",
            "affinity_kcal_mol": thcv.get("cb2", {}).get("affinity"),
            "microswitch_distances_A": thcv.get("cb2", {}).get("microswitch_distances"),
            "interpretation": (
                "Sonda mecanística ONLY — pose docked contra 6PT0 activo; "
                "NO prueba funcional agonista/antagonista/modulador."
            ),
        },
        "cb1": {
            "docked_receptor_state": "5TGZ (inactive antagonist-bound)",
            "affinity_kcal_mol": thcv.get("cb1", {}).get("affinity"),
            "microswitch_distances_A": thcv.get("cb1", {}).get("microswitch_distances"),
            "interpretation": (
                "Espacio CB1 separado — docked contra 5TGZ inactivo; "
                "NO comparable numéricamente a distancias CB2."
            ),
        },
        "epistemology": "Q3 observation only; not mixed with CB2 OOS distances.",
    }


def run_evaluation(skip_align: bool = False) -> dict[str, Any]:
    manifest = run_alignment() if not skip_align else json.loads(
        (ROOT / "data/targets/multistate_aligned/alignment_manifest.json").read_text(
            encoding="utf-8"
        )
    )

    ref_phe_ca = atom_xyz(
        read_atoms(ROOT / "data/targets/multistate_aligned/6PT0_aligned.pdb", chains={"R"}),
        MICROSWITCHS["cb2"].phe_ecl2,
        "PHE",
        "CA",
    )
    if ref_phe_ca is None:
        raise RuntimeError("Reference Phe183 missing in 6PT0")

    metrics: dict[str, dict] = {}
    input_hashes: dict[str, str] = {}
    for pid in CB2_OOS_IDS:
        entry = next(e for e in manifest["aligned_structures"] if e["pdb_id"] == pid)
        pdb_path = ROOT / entry["aligned_pdb"]
        input_hashes[pid] = _sha256(pdb_path)
        metrics[pid] = extract_g_metrics(
            pdb_path, "cb2", pid, reference_phe_ca=ref_phe_ca
        )

    level0 = _level0_verify(manifest, metrics)
    if not level0["passed"]:
        result = {
            "governance": GOVERNANCE,
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "level0": level0,
            "q1_oos_verdict": "INDETERMINATE",
            "q1_oos_rationale": "Level-0 verification failed for 8GUR.",
            "input_hashes": input_hashes,
        }
        _write_outputs(result, manifest, metrics)
        return result

    vectors = {k: np.array(v["feature_vector"], dtype=float) for k, v in metrics.items()}
    norm_fit_ids = tuple(i for i in CB2_OOS_IDS if i != CB2_BLIND)
    norm, norm_meta = _normalize(vectors, norm_fit_ids)

    active_vecs = [vectors[i] for i in CB2_ACTIVE_REFS]
    active_centroid = np.mean(np.stack(active_vecs), axis=0)
    active_centroid_norm = np.mean(
        np.stack([norm[i] for i in CB2_ACTIVE_REFS]), axis=0
    )

    distances_raw: dict[str, float] = {}
    distances_norm: dict[str, float] = {}
    for pid in CB2_OOS_IDS:
        distances_raw[pid] = round(_dist(vectors[pid], active_centroid), 4)
        distances_norm[pid] = round(_dist(norm[pid], active_centroid_norm), 4)

    verdict, rationale = _verdict_oos(
        distances_norm, CB2_ACTIVE_REFS, CB2_NEGATIVE, CB2_BLIND
    )

    # Leave-one-out (Q2): centroid from 6PT0 only; reuse OOS normalization.
    loo_centroid_norm = norm["6PT0"]
    loo_distances: dict[str, float] = {}
    for pid in ("6KPF", CB2_BLIND, CB2_NEGATIVE):
        loo_distances[pid] = round(_dist(norm[pid], loo_centroid_norm), 4)
    loo_active_d = loo_distances["6KPF"]
    loo_blind_d = loo_distances[CB2_BLIND]
    loo_neg_d = loo_distances[CB2_NEGATIVE]
    if loo_blind_d >= loo_neg_d:
        loo_verdict = "FALSIFIED"
        loo_rationale = (
            f"{CB2_BLIND} ({loo_blind_d:.3f}) ≥ inactive {CB2_NEGATIVE} ({loo_neg_d:.3f}) "
            "under 6PT0-only reference."
        )
    elif loo_blind_d <= loo_active_d + 0.5 and (loo_neg_d - loo_blind_d) > 1.0:
        loo_verdict = "GENERALIZES"
        loo_rationale = (
            f"{CB2_BLIND} ({loo_blind_d:.3f}) near held-out active 6KPF ({loo_active_d:.3f}) "
            f"and separates from {CB2_NEGATIVE} ({loo_neg_d:.3f}) with 6PT0-only centroid."
        )
    elif loo_neg_d > loo_blind_d:
        loo_verdict = "PARTIAL"
        loo_rationale = (
            f"Trend preserved (blind {loo_blind_d:.3f} < inactive {loo_neg_d:.3f}) "
            f"but margin vs 6KPF ({loo_active_d:.3f}) not robust under LOO."
        )
    else:
        loo_verdict = "FALSIFIED"
        loo_rationale = "LOO separation not reproduced."

    # CB1 cross-reference (separate normalized space).
    cb1_metrics: dict[str, dict] = {}
    ref_phe_cb1 = atom_xyz(
        read_atoms(ROOT / "data/targets/multistate_aligned/5TGZ_aligned.pdb", chains={"A"}),
        MICROSWITCHS["cb1"].phe_ecl2,
        "PHE",
        "CA",
    )
    cb1_distances: dict[str, float] = {}
    if ref_phe_cb1 is not None:
        for pid in CB1_IDS:
            entry = next(
                (e for e in manifest["aligned_structures"] if e["pdb_id"] == pid), None
            )
            if entry is None:
                continue
            cb1_metrics[pid] = extract_cb1_g_metrics(
                ROOT / entry["aligned_pdb"],
                pid,
                reference_phe_ca=ref_phe_cb1,
            )
        cb1_vectors = {
            k: np.array(v["feature_vector"], dtype=float) for k, v in cb1_metrics.items()
        }
        cb1_norm, cb1_norm_meta = _normalize_cb1(cb1_vectors)
        cb1_active_centroid_norm = cb1_norm[CB1_ACTIVE]
        for pid in CB1_IDS:
            cb1_distances[pid] = round(
                _dist(cb1_norm[pid], cb1_active_centroid_norm), 4
            )

    thcv = _load_thcv_secondary()

    # Exploratory raw-metric deltas vs 6PT0 (not confirmatory).
    exploratory: dict[str, dict[str, float]] = {}
    ref_feats = metrics["6PT0"]["features"]
    for pid in CB2_OOS_IDS:
        exploratory[pid] = {
            k: round(metrics[pid]["features"][k] - ref_feats[k], 4)
            for k in G_FEATURE_NAMES
        }

    result: dict[str, Any] = {
        "governance": GOVERNANCE,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "branch": "feat/fase-g-conformational-validation",
        "level0": level0,
        "input_hashes": input_hashes,
        "normalization": norm_meta,
        "active_centroid_from": list(CB2_ACTIVE_REFS),
        "cb2_state_distance": {
            "raw": distances_raw,
            "normalized": distances_norm,
            "feature_names": list(G_FEATURE_NAMES),
        },
        "metrics_by_pdb": metrics,
        "exploratory_delta_vs_6PT0": exploratory,
        "exploratory_delta_cutoff_A": EXPLORATORY_DELTA_CUTOFF_A,
        "exploratory_note": (
            f"Δ ≥ {EXPLORATORY_DELTA_CUTOFF_A} Å (or any numeric cutoff) is EXPLORATORY only; "
            "not used as confirmatory validation evidence."
        ),
        "q1_oos_verdict": verdict,
        "q1_oos_rationale": rationale,
        "q2_loo": {
            "reference": "6PT0",
            "blind": ["6KPF", CB2_BLIND],
            "negative": CB2_NEGATIVE,
            "distances_normalized": loo_distances,
            "normalization": "reuse OOS fit (6PT0, 6KPF, 5ZTY); centroid 6PT0 only",
            "verdict": loo_verdict,
            "rationale": loo_rationale,
        },
        "q3_thcv": thcv,
        "cb1_cross_reference": {
            "note": "Separate normalized CB1 coordinate space — NOT comparable to CB2 distances.",
            "active_reference": CB1_ACTIVE,
            "inactive": CB1_INACTIVE,
            "feature_names": list(CB1_G_FEATURE_NAMES),
            "distances_normalized": cb1_distances,
            "metrics": cb1_metrics,
        },
        "alignment_manifest_excerpt": [
            e for e in manifest["aligned_structures"] if e["pdb_id"] in CB2_OOS_IDS
        ],
    }
    _write_outputs(result, manifest, metrics)
    return result


def _write_outputs(
    result: dict[str, Any],
    manifest: dict,
    metrics: dict[str, dict],
) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(_json_safe(result), indent=2), encoding="utf-8")
    MD_OUT.write_text(_render_md(result, manifest, metrics), encoding="utf-8")


def _render_md(
    result: dict[str, Any],
    manifest: dict,
    metrics: dict[str, dict],
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Phase G — Generalización out-of-sample 8GUR (CB2)",
        "",
        f"**Generado:** {ts}  ",
        f"**Rama:** `{result.get('branch', 'feat/fase-g-conformational-validation')}`",
        "",
        "## Bloque de gobernanza",
        "",
        "```yaml",
        *[f"{k}: {v}" for k, v in result["governance"].items()],
        "```",
        "",
        "## Level-0 — 8GUR",
        "",
    ]
    l0 = result["level0"]
    lines.extend(
        [
            f"- **Verificación:** {'PASS' if l0['passed'] else 'FAIL'}",
            f"- **PDB:** {l0['pdb_id']} ({l0['resolution_A']} Å cryo-EM)",
            f"- **Receptor:** {l0['receptor']} cadena `{l0.get('chain', 'R')}`",
            f"- **Ligando:** {l0['ligand']} (retirado para huella conformacional)",
            f"- **Estado:** {l0['state']}",
        ]
    )
    for n in l0.get("notes", []):
        lines.append(f"- Nota: {n}")

    lines.extend(
        [
            "",
            "## Q1 — ¿El coordinate separa activo/inactivo out-of-sample?",
            "",
            f"**Veredicto Q1:** **{result['q1_oos_verdict']}**",
            "",
            f"> {result['q1_oos_rationale']}",
            "",
            "### Distancias CB2_STATE_DISTANCE (espacio CB2 normalizado; centroide activo 6PT0+6KPF)",
            "",
            "| PDB | Estado | Distancia (norm) | Distancia (raw) |",
            "|-----|--------|------------------|-----------------|",
        ]
    )
    for pid in CB2_OOS_IDS:
        state = metrics[pid]["state_label"]
        dn = result["cb2_state_distance"]["normalized"][pid]
        dr = result["cb2_state_distance"]["raw"][pid]
        tag = " **blind**" if pid == CB2_BLIND else ""
        lines.append(f"| {pid}{tag} | {state} | {dn} | {dr} |")

    lines.extend(
        [
            "",
            "### Métricas conformacionales (raw)",
            "",
            "| PDB | TM3–TM6 IC (Å) | TM3–TM5 disp (Å) | Trp258 χ1 (°) | Trp258 χ2 (°) | "
            "Ser268 χ1 (°) | Phe183 disp (Å) | Phe183 tilt (°) |",
            "|-----|---------------|------------------|---------------|---------------|"
            "---------------|-----------------|-----------------|",
        ]
    )
    for pid in CB2_OOS_IDS:
        f = metrics[pid]["features"]
        lines.append(
            f"| {pid} | {f['tm3_tm6_ic_distance_A']} | {f['tm3_tm5_centroid_displacement_A']} | "
            f"{f['trp258_chi1_deg']} | {f['trp258_chi2_deg']} | {f['ser268_chi1_deg']} | "
            f"{f['phe183_ecl2_ca_displacement_A']} | {f['phe183_aromatic_tilt_deg']} |"
        )

    lines.extend(
        [
            "",
            f"### Cutoff exploratorio (NO confirmatorio): Δ ≥ {EXPLORATORY_DELTA_CUTOFF_A} Å vs 6PT0",
            "",
            "| PDB | Δ TM3–TM6 | Δ TM3–TM5 | Δ Trp258 χ1 | Δ Ser268 χ1 | Δ Phe183 disp |",
            "|-----|-----------|-----------|-------------|-------------|---------------|",
        ]
    )
    for pid in CB2_OOS_IDS:
        e = result.get("exploratory_delta_vs_6PT0", {}).get(pid, {})
        lines.append(
            f"| {pid} | {e.get('tm3_tm6_ic_distance_A', '—')} | "
            f"{e.get('tm3_tm5_centroid_displacement_A', '—')} | "
            f"{e.get('trp258_chi1_deg', '—')} | {e.get('ser268_chi1_deg', '—')} | "
            f"{e.get('phe183_ecl2_ca_displacement_A', '—')} |"
        )

    lines.extend(
        [
            "",
            f"> {result.get('exploratory_note', '')}",
            "",
            "## Q2 — Leave-one-out (centroide 6PT0 solo)",
            "",
            f"**Veredicto Q2:** **{result.get('q2_loo', {}).get('verdict', '—')}**",
            "",
            f"> {result.get('q2_loo', {}).get('rationale', '')}",
            "",
            "| PDB | Distancia LOO (norm) | Rol |",
            "|-----|----------------------|-----|",
        ]
    )
    loo = result.get("q2_loo", {}).get("distances_normalized", {})
    roles = {"6KPF": "blind (active ref held out)", CB2_BLIND: "blind OOS", CB2_NEGATIVE: "negativo"}
    for pid, d in loo.items():
        lines.append(f"| {pid} | {d} | {roles.get(pid, '')} |")

    lines.extend(
        [
            "",
            "## Q3 — THCV (sonda mecanística; NO prueba funcional)",
            "",
        ]
    )
    thcv = result.get("q3_thcv", {})
    if thcv.get("available"):
        lines.append(f"- Fuente: `{thcv.get('source')}`")
        for space in ("cb2", "cb1"):
            block = thcv.get(space, {})
            lines.append(f"- **{space.upper()}:** estado docked = {block.get('docked_receptor_state')}")
            lines.append(f"  - Afinidad: {block.get('affinity_kcal_mol')} kcal/mol")
            lines.append(f"  - Microswitches pose: {block.get('microswitch_distances_A')}")
            lines.append(f"  - {block.get('interpretation')}")
    else:
        lines.append("- THCV seed JSON no disponible.")

    cb1 = result.get("cb1_cross_reference", {})
    lines.extend(
        [
            "",
            "## CB1 cross-reference (espacio normalizado SEPARADO)",
            "",
            f"> {cb1.get('note', '')}",
            "",
            "| PDB | Estado | Distancia CB1 (norm vs 5XRA activo) |",
            "|-----|--------|-------------------------------------|",
        ]
    )
    for pid, d in cb1.get("distances_normalized", {}).items():
        st = cb1.get("metrics", {}).get(pid, {}).get("state_label", "")
        lines.append(f"| {pid} | {st} | {d} |")

    lines.extend(
        [
            "",
            "## Alineamiento TM (Level-0 infra)",
            "",
            "| PDB | TM Cα pares | RMSD post (Å) | Cadena |",
            "|-----|-------------|---------------|--------|",
        ]
    )
    for entry in result.get("alignment_manifest_excerpt", []):
        lines.append(
            f"| {entry['pdb_id']} | {entry['tm_ca_pairs']} | {entry['rmsd_after_A']} | "
            f"{entry.get('chain', '—')} |"
        )

    lines.extend(
        [
            "",
            "## Scripts",
            "",
            "- `scripts/conformational/evaluate_8gur_generalization.py`",
            "- `scripts/conformational/align_multistate.py`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skip-align", action="store_true")
    args = ap.parse_args()
    result = run_evaluation(skip_align=args.skip_align)
    print(f"Q1 verdict: {result['q1_oos_verdict']}")
    print(f"JSON: {JSON_OUT}")
    print(f"Report: {MD_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
