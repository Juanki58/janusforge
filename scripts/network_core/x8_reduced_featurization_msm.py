#!/usr/bin/env python3
"""X8 — Reduced featurization MSM vs high-D baseline (Gate-1 diagnosis).

Pre-registration: docs/synthesis/EXPERIMENT_X8_REDUCED_FEATURIZATION.md
Governance: satellite discrimination only; does NOT reopen P2 A/B/C / P5 / docking.

CLI::

    micromamba run -n janus_p1 python scripts/network_core/x8_reduced_featurization_msm.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from p2_msm_builder import (  # noqa: E402
    FRAME_DT_NS,
    ITS_LAGS_FRAMES,
    KMEANS_MAX_ITER,
    KMEANS_SEED,
    MANIFEST_PATH,
    N_ITS,
    N_MICROSTATES,
    PSF_NAME,
    SHA_CACHE,
    TICA_DIM,
    TICA_LAG_FRAMES,
    TRAJ_DIR,
    XTC_NAMES,
    assess_its_convergence,
    compute_implied_timescales,
    fit_tica_kmeans,
    provisional_label,
    verify_manifest,
)

OUT_DIR = ROOT / "results" / "msm_model"
PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_X8_REDUCED_FEATURIZATION.md"

# Fixed a priori — 24 Cα–Cα pairs (see EXPERIMENT_X8_REDUCED_FEATURIZATION.md)
REDUCED_CA_PAIRS: tuple[tuple[int, int], ...] = (
    (131, 245),
    (131, 240),
    (131, 258),
    (128, 245),
    (211, 258),
    (207, 258),
    (215, 245),
    (215, 240),
    (201, 258),
    (258, 291),
    (258, 295),
    (258, 285),
    (245, 291),
    (240, 295),
    (264, 295),
    (131, 295),
    (131, 291),
    (83, 291),
    (79, 291),
    (87, 285),
    (183, 258),
    (268, 285),
    (287, 295),
    (302, 295),
)

PAIR_ROLES: tuple[str, ...] = (
    "Arg3.50-Lys6.35",
    "Arg3.50-Asp6.30",
    "Arg3.50-Trp6.48",
    "Tyr3.47region-Lys6.35",
    "Pro5.50-Trp6.48",
    "TM5mid-Trp6.48",
    "TM5IC-Lys6.35",
    "TM5IC-Asp6.30",
    "TM5mid2-Trp6.48",
    "Trp6.48-Asn7.45",
    "Trp6.48-Asn7.49",
    "Trp6.48-Ser7.39",
    "Lys6.35-Asn7.45",
    "Asp6.30-Asn7.49",
    "TM6Cterm-Asn7.49",
    "Arg3.50-Asn7.49",
    "Arg3.50-Asn7.45",
    "Ala2.53-Asn7.45",
    "Ala2.49-Asn7.45",
    "Phe87-Ser285",
    "PheECL2-Trp6.48",
    "Ser6.58-Ser7.39",
    "Leu7.41-Asn7.49",
    "Arg8.46-Asn7.49",
)

BASELINE = {
    "commit": "2dcff23",
    "n_features": 15753,
    "n_frames": 1995,
    "its_verdict": "NON_CONVERGENT",
    "connected_states_per_lag": [25, 25, 8, 1, 8, 1, 8, 1, 1, 1],
    "report": "results/msm_model/p2_msm_convergence_report.md",
}


def extract_reduced_ca_distances(
    psf: Path, xtcs: list[Path]
) -> tuple[list[np.ndarray], dict[str, Any]]:
    import MDAnalysis as mda

    needed = sorted({r for pair in REDUCED_CA_PAIRS for r in pair})
    sel = "protein and name CA and (" + " or ".join(f"resid {r}" for r in needed) + ")"

    features: list[np.ndarray] = []
    per_traj: list[dict[str, Any]] = []
    resid_to_idx: dict[int, int] | None = None

    for xtc in xtcs:
        u = mda.Universe(str(psf), str(xtc))
        atoms = u.select_atoms(sel)
        found = {int(r): i for i, r in enumerate(atoms.resids)}
        if resid_to_idx is None:
            resid_to_idx = found
            missing = [r for r in needed if r not in found]
            if missing:
                raise RuntimeError(f"Missing Cα residues for reduced set: {missing}")
        elif {int(r) for r in atoms.resids} != set(resid_to_idx):
            raise RuntimeError(f"Cα resid mismatch in {xtc.name}")

        idx_pairs = [
            (resid_to_idx[a], resid_to_idx[b]) for a, b in REDUCED_CA_PAIRS
        ]
        rows = []
        for _ts in u.trajectory:
            pos = atoms.positions
            row = np.empty(len(idx_pairs), dtype=np.float64)
            for k, (i, j) in enumerate(idx_pairs):
                d = pos[i] - pos[j]
                row[k] = float(np.sqrt(np.dot(d, d)))
            rows.append(row)
        arr = np.asarray(rows, dtype=np.float64)
        features.append(arr)
        per_traj.append(
            {
                "xtc": xtc.name,
                "n_frames": int(arr.shape[0]),
                "n_features": int(arr.shape[1]),
                "dt_reported_by_mda": float(u.trajectory.dt),
            }
        )

    meta = {
        "featurization": "reduced_ca_pairwise_preregistered",
        "n_features": len(REDUCED_CA_PAIRS),
        "pairs": [
            {"i": a, "j": b, "role": PAIR_ROLES[k]}
            for k, (a, b) in enumerate(REDUCED_CA_PAIRS)
        ],
        "selection": sel,
        "distance_unit": "angstrom",
        "per_trajectory": per_traj,
        "frame_dt_ns_assumed": FRAME_DT_NS,
        "preregistration": str(PREREG.relative_to(ROOT)),
    }
    return features, meta


def materially_improves(assessment: dict[str, Any], its_data: dict[str, Any]) -> dict[str, Any]:
    """Locked definition from EXPERIMENT_X8_REDUCED_FEATURIZATION.md."""
    per_lag = its_data.get("per_lag") or []
    connected = [
        int(r["n_states_connected"])
        for r in per_lag
        if "n_states_connected" in r
    ]
    n_success = len(connected)
    n_collapse = sum(1 for c in connected if c <= 1)
    n_finite = int(assessment.get("n_finite_slowest") or 0)
    verdict = str(assessment.get("verdict"))
    reason = str(assessment.get("reason") or "")
    pathological = ("pathological ITS spectrum" in reason) or (
        n_finite < 3 and verdict == "NON_CONVERGENT"
    )

    cond1 = n_finite >= 3
    cond2 = n_success > 0 and n_collapse < (n_success / 2.0)
    rel = assessment.get("slowest_rel_change")
    from p2_msm_builder import ITS_MARGINAL_REL_TOL

    if verdict in ("CONVERGENT", "MARGINAL"):
        cond3 = True
        cond3_note = f"assessment verdict={verdict}"
    elif (
        verdict == "NON_CONVERGENT"
        and not pathological
        and cond1
        and cond2
        and rel is not None
        and float(rel) <= ITS_MARGINAL_REL_TOL
    ):
        cond3 = True
        cond3_note = (
            f"NON_CONVERGENT but non-pathological with rel_change={rel:.3f}"
            f"≤{ITS_MARGINAL_REL_TOL}"
        )
    else:
        cond3 = False
        cond3_note = (
            f"fails flattening clause (verdict={verdict}, pathological={pathological}, "
            f"rel={rel})"
        )

    ok = bool(cond1 and cond2 and cond3)
    return {
        "materially_improves": ok,
        "cond1_finite_positive_its_ge3": cond1,
        "cond2_connected_not_majority_collapse": cond2,
        "cond3_qualitative_flattening": cond3,
        "cond3_note": cond3_note,
        "n_finite_slowest": n_finite,
        "n_successful_lags": n_success,
        "n_lags_connected_le1": n_collapse,
        "connected_states_per_lag": connected,
        "its_verdict": verdict,
        "pathological_like_baseline": pathological,
    }


def assign_verdict(improve: dict[str, Any], indeterminate: str | None) -> str:
    if indeterminate:
        return "X8_INDETERMINATE"
    if improve["materially_improves"]:
        return "X8_REPRESENTATION_LIMITED"
    return "X8_SAMPLING_LIMITED"


def plot_its(its_data: dict[str, Any], assessment: dict[str, Any], out_png: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lags = its_data.get("lags_frames") or []
    mat = np.asarray(its_data.get("its_frames") or [], dtype=float)
    fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=140)
    if len(lags) and mat.size:
        for i in range(mat.shape[1]):
            ax.plot(lags, mat[:, i], "o-", ms=3.5, lw=1.2, label=f"ITS {i + 1}")
        ax.plot(lags, lags, "k--", lw=1.0, label="τ = lag")
    ax.set_xlabel("Lag time (frames)")
    ax.set_ylabel("Implied timescale (frames)")
    ax.set_title(
        "X8 reduced featurization MSM — implied timescales\n"
        f"verdict={assessment.get('verdict')} "
        f"(assumed {FRAME_DT_NS} ns/frame; n_feat={len(REDUCED_CA_PAIRS)})"
    )
    ax.legend(loc="best", fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png)
    plt.close(fig)


def write_reports(payload: dict[str, Any]) -> tuple[Path, Path]:
    out_dir = OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "x8_reduced_featurization_report.json"
    md_path = out_dir / "x8_reduced_featurization_report.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    its_a = payload["implied_timescales_assessment"]
    imp = payload["material_improvement"]
    lines = [
        "# X8 — Reduced featurization MSM (Gate-1 diagnosis)",
        "",
        f"**Generated (UTC):** {payload['generated_utc']}",
        f"**Pre-registration:** `{payload['preregistration']}`",
        f"**X8 verdict:** `{payload['x8_verdict']}`",
        "",
        "## Scope",
        "",
        "- Same 1995 frames / 5 WT replicas as P2 baseline.",
        "- Reduced featurization only; **no** A/B/C architecture claim.",
        "- P2 remains **CLOSED (INSUFFICIENT_SAMPLING)** regardless of X8.",
        "",
        "## Baseline (`2dcff23`)",
        "",
        f"- Features: **{BASELINE['n_features']}** TM Cα pairwise",
        f"- ITS: **`{BASELINE['its_verdict']}`**",
        f"- Connected states/lag: `{BASELINE['connected_states_per_lag']}`",
        "",
        "## Reduced features",
        "",
        f"- **n = {len(REDUCED_CA_PAIRS)}** Cα–Cα distances (fixed a priori)",
        "",
    ]
    for k, (a, b) in enumerate(REDUCED_CA_PAIRS):
        lines.append(f"- {k + 1}. `{a}–{b}` ({PAIR_ROLES[k]})")
    lines += [
        "",
        "## Hyperparameters",
        "",
        f"- tICA lag={TICA_LAG_FRAMES}, dim={TICA_DIM}",
        f"- K-means microstates={N_MICROSTATES}, seed={KMEANS_SEED}",
        f"- ITS lags={list(ITS_LAGS_FRAMES)}",
        "",
        "## ITS assessment",
        "",
        f"- Verdict: **`{its_a.get('verdict')}`**",
        f"- Reason: {its_a.get('reason')}",
        f"- n_finite_slowest: {its_a.get('n_finite_slowest')}",
        f"- connected_states_per_lag: `{its_a.get('connected_states_per_lag')}`",
        f"- slowest_rel_change: {its_a.get('slowest_rel_change')}",
        "",
        "## Material improvement checklist",
        "",
        f"- cond1 finite ITS ≥3: **{imp['cond1_finite_positive_its_ge3']}**",
        f"- cond2 no majority collapse: **{imp['cond2_connected_not_majority_collapse']}**",
        f"- cond3 flattening: **{imp['cond3_qualitative_flattening']}** ({imp['cond3_note']})",
        f"- materially_improves: **{imp['materially_improves']}**",
        "",
        "## Verdict",
        "",
        f"**`{payload['x8_verdict']}`**",
        "",
        f"- Provisional P2 lean (unchanged gate): `{payload['provisional_p2_label']}`",
        "",
        "## Artifacts",
        "",
        f"- `{payload['artifacts']['its_png']}`",
        f"- `{payload['artifacts']['its_json']}`",
        f"- `{payload['artifacts']['report_json']}`",
        "",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md_path, json_path


def run(out_dir: Path = OUT_DIR) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    indeterminate: str | None = None

    sha = verify_manifest(MANIFEST_PATH, TRAJ_DIR, cache_path=SHA_CACHE)
    if not sha.get("all_ok"):
        indeterminate = "manifest SHA verification failed"

    psf = TRAJ_DIR / PSF_NAME
    xtcs = [TRAJ_DIR / n for n in XTC_NAMES]
    for p in [psf, *xtcs]:
        if not p.is_file():
            indeterminate = f"missing required file: {p}"

    versions: dict[str, str] = {}
    for name in ("numpy", "MDAnalysis", "deeptime", "matplotlib", "sklearn"):
        try:
            mod = __import__(name if name != "sklearn" else "sklearn")
            versions[name] = getattr(mod, "__version__", "unknown")
        except Exception as exc:  # noqa: BLE001
            versions[name] = f"MISSING ({type(exc).__name__})"
            indeterminate = indeterminate or f"missing package {name}"
    versions["python"] = sys.version.split()[0]

    features: list[np.ndarray] = []
    feat_meta: dict[str, Any] = {}
    dtrajs: list[np.ndarray] = []
    cluster_info: dict[str, Any] = {}
    its_data: dict[str, Any] = {"lags_frames": [], "its_frames": [], "per_lag": []}
    assessment: dict[str, Any] = {
        "verdict": "NON_CONVERGENT",
        "reason": "not run",
    }
    improve: dict[str, Any] = {
        "materially_improves": False,
        "cond1_finite_positive_its_ge3": False,
        "cond2_connected_not_majority_collapse": False,
        "cond3_qualitative_flattening": False,
        "cond3_note": "not run",
        "n_finite_slowest": 0,
        "n_successful_lags": 0,
        "n_lags_connected_le1": 0,
        "connected_states_per_lag": [],
        "its_verdict": "NON_CONVERGENT",
        "pathological_like_baseline": True,
    }

    if indeterminate is None:
        try:
            features, feat_meta = extract_reduced_ca_distances(psf, xtcs)
            dtrajs, _tica, _km, cluster_info = fit_tica_kmeans(features)
            its_data = compute_implied_timescales(dtrajs, ITS_LAGS_FRAMES, N_ITS)
            assessment = assess_its_convergence(its_data)
            improve = materially_improves(assessment, its_data)
        except Exception as exc:  # noqa: BLE001
            indeterminate = f"{type(exc).__name__}: {exc}"

    x8_verdict = assign_verdict(improve, indeterminate)

    its_png = out_dir / "x8_implied_timescales.png"
    its_json = out_dir / "x8_implied_timescales.json"
    if its_data.get("lags_frames"):
        plot_its(its_data, assessment, its_png)
    its_json.write_text(
        json.dumps(
            {"implied_timescales": its_data, "assessment": assessment},
            indent=2,
        ),
        encoding="utf-8",
    )

    n_frames = int(sum(len(f) for f in features)) if features else 0
    payload: dict[str, Any] = {
        "experiment": "X8_REDUCED_FEATURIZATION",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "preregistration": str(PREREG.relative_to(ROOT)),
        "baseline": BASELINE,
        "sha256_verification": sha,
        "software_versions": versions,
        "featurization": feat_meta,
        "clustering": cluster_info,
        "n_frames_total": n_frames,
        "n_replicas": len(XTC_NAMES),
        "implied_timescales": its_data,
        "implied_timescales_assessment": assessment,
        "material_improvement": improve,
        "x8_verdict": x8_verdict,
        "indeterminate_reason": indeterminate,
        "provisional_p2_label": provisional_label(str(assessment.get("verdict"))),
        "governance": {
            "reopens_p2_abc": False,
            "p2_status_remains": "CLOSED (INSUFFICIENT_SAMPLING)",
            "no_docking": True,
            "no_de_novo": True,
            "no_new_hub_hunt": True,
        },
        "artifacts": {
            "its_png": str(its_png.relative_to(ROOT)),
            "its_json": str(its_json.relative_to(ROOT)),
            "report_json": "results/msm_model/x8_reduced_featurization_report.json",
            "report_md": "results/msm_model/x8_reduced_featurization_report.md",
        },
    }
    write_reports(payload)
    # refresh report_json with full payload (write_reports wrote earlier stub path)
    (out_dir / "x8_reduced_featurization_report.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    return payload


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="X8 reduced featurization MSM")
    p.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = p.parse_args(argv)
    payload = run(args.out_dir)
    print(f"X8_VERDICT={payload['x8_verdict']}")
    print(f"ITS={payload['implied_timescales_assessment'].get('verdict')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
