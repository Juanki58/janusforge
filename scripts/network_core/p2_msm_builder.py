#!/usr/bin/env python3
"""P2 Stage-1 convergence — own MSM on GPCRmd WT dyn2126 (Morales-Pastor).

Governance
----------
- REAL DATA ONLY: local GPCRmd/1540 WT trajectories (5× .xtc + .psf).
- NOT dry / synthetic; NOT Dutta–Shukla MSM as template.
- Convergence artifacts only: ITS, PCCA+, populations, frame assignments.
- NO A/B/C network extraction, NO biological state interpretation,
  NO P5 / docking / de novo, NO auto-advance of P2 gate.

Pipeline
--------
Cα pairwise distances (TM1–TM7, human CB2 UniProt / GPCRdb spans)
  → tICA → K-means → MSM → implied timescales → PCCA+

CLI::

    micromamba run -n janus_p1 python scripts/network_core/p2_msm_builder.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TRAJ_DIR = ROOT / "data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126"
MANIFEST_PATH = (
    ROOT / "data/external/morales_pastor_2025/trajectories/MANIFEST.json"
)
OUT_DIR = ROOT / "results" / "msm_model"

# Human CB2 (CNR2 / P34972) TM helix spans — GPCRdb, same as
# scripts/conformational/residue_maps.py TM_HELICES["cb2"].
CB2_TM_HELICES: dict[str, tuple[int, int]] = {
    "TM1": (31, 56),
    "TM2": (67, 91),
    "TM3": (107, 132),
    "TM4": (148, 172),
    "TM5": (193, 217),
    "TM6": (239, 264),
    "TM7": (276, 300),
}

PSF_NAME = "24306_dyn_2126.psf"
XTC_NAMES = [
    "24307_trj_2126.xtc",
    "24308_trj_2126.xtc",
    "24309_trj_2126.xtc",
    "24310_trj_2126.xtc",
    "24311_trj_2126.xtc",
]

# Analysis hyperparameters (fixed a priori for this Stage-1 run)
TICA_LAG_FRAMES = 5
TICA_DIM = 5
# Keep microstate count modest vs ~2k frames to avoid empty-state fragmentation.
N_MICROSTATES = 25
KMEANS_MAX_ITER = 500
KMEANS_SEED = 20260821
ITS_LAGS_FRAMES = (1, 2, 5, 10, 15, 20, 25, 30, 40, 50)
N_ITS = 8
# GPCRmd WT deposits typically store ~1 frame/ns; MDA dt often reports 1.0.
# Treat lag axis in frames; also report ns assuming 1 ns/frame (documented).
FRAME_DT_NS = 1.0
# Flatness: relative change of slowest ITS between last two lag thirds.
ITS_FLAT_REL_TOL = 0.25
ITS_MARGINAL_REL_TOL = 0.50
FEATURES_CACHE = OUT_DIR / "features_tm_ca_pairwise.npz"
SHA_CACHE = OUT_DIR / "sha256_verification.json"


def _sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def verify_manifest(
    manifest_path: Path, traj_dir: Path, cache_path: Path | None = SHA_CACHE
) -> dict[str, Any]:
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    base = manifest_path.parent

    cached: dict[str, Any] | None = None
    if cache_path is not None and cache_path.is_file():
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            cached = None
    cached_by_path = {
        r["path"]: r
        for r in (cached or {}).get("files", [])
        if isinstance(r, dict) and "path" in r and r.get("sha256")
    }

    rows: list[dict[str, Any]] = []
    all_ok = True
    for entry in data.get("files", []):
        rel = entry["path"]
        path = base / rel
        expected = entry["sha256"].lower()
        if not path.is_file():
            rows.append(
                {
                    "path": rel,
                    "status": "MISSING",
                    "expected_sha256": expected,
                }
            )
            all_ok = False
            continue
        size = path.stat().st_size
        prev = cached_by_path.get(rel)
        if (
            prev
            and int(prev.get("bytes", -1)) == size
            and prev.get("expected_sha256", "").lower() == expected
            and prev.get("sha_ok") is True
        ):
            got = str(prev["sha256"]).lower()
            reused = True
        else:
            got = _sha256_file(path)
            reused = False
        ok = got == expected and size == int(entry.get("bytes", size))
        all_ok = all_ok and ok
        rows.append(
            {
                "path": rel,
                "bytes": size,
                "expected_bytes": entry.get("bytes"),
                "sha256": got,
                "expected_sha256": expected,
                "sha_ok": ok,
                "status": "OK" if ok else "MISMATCH",
                "sha_reused_from_cache": reused,
            }
        )
    required = [PSF_NAME, *XTC_NAMES]
    for name in required:
        p = traj_dir / name
        if not p.is_file():
            all_ok = False
            rows.append({"path": str(p), "status": "REQUIRED_MISSING"})
    result = {
        "manifest": str(manifest_path.relative_to(ROOT)),
        "all_ok": all_ok,
        "files": rows,
    }
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def _pkg_versions() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in (
        "numpy",
        "scipy",
        "sklearn",
        "matplotlib",
        "MDAnalysis",
        "deeptime",
        "mdtraj",
    ):
        try:
            mod = __import__(name if name != "sklearn" else "sklearn")
            out[name] = getattr(mod, "__version__", "unknown")
        except Exception as exc:  # noqa: BLE001
            out[name] = f"MISSING ({type(exc).__name__})"
    out["python"] = sys.version.split()[0]
    return out


def _ca_selection_string() -> str:
    parts = [
        f"(resid {a}:{b})" for a, b in CB2_TM_HELICES.values()
    ]
    return "protein and name CA and (" + " or ".join(parts) + ")"


def extract_tm_ca_pairwise_distances(
    psf: Path, xtcs: list[Path], cache_path: Path | None = FEATURES_CACHE
) -> tuple[list[np.ndarray], dict[str, Any]]:
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import self_distance_array

    if cache_path is not None and cache_path.is_file():
        z = np.load(cache_path, allow_pickle=True)
        names = [str(x) for x in z["replica_names"].tolist()]
        if names == [x.name for x in xtcs]:
            features = [z[f"replica_{i}"] for i in range(len(xtcs))]
            meta = json.loads(str(z["meta_json"]))
            meta["loaded_from_cache"] = str(cache_path.relative_to(ROOT))
            return features, meta

    sel = _ca_selection_string()
    features: list[np.ndarray] = []
    per_traj: list[dict[str, Any]] = []
    ca_resids: list[int] | None = None
    n_ca = 0

    for xtc in xtcs:
        u = mda.Universe(str(psf), str(xtc))
        atoms = u.select_atoms(sel)
        if atoms.n_atoms == 0:
            raise RuntimeError(f"No TM Cα selected for {xtc.name}")
        if ca_resids is None:
            ca_resids = [int(r) for r in atoms.resids]
            n_ca = atoms.n_atoms
        elif list(atoms.resids) != ca_resids:
            raise RuntimeError(f"Cα resid mismatch in {xtc.name}")

        rows = []
        for _ts in u.trajectory:
            d = self_distance_array(atoms.positions)
            rows.append(d.astype(np.float64))
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
        "selection": sel,
        "tm_helices_human_cb2_uniprot": {
            k: {"start": v[0], "end": v[1]} for k, v in CB2_TM_HELICES.items()
        },
        "source": "scripts/conformational/residue_maps.py TM_HELICES['cb2'] (GPCRdb)",
        "n_ca": n_ca,
        "ca_resids": ca_resids,
        "n_pairwise_features": int(n_ca * (n_ca - 1) // 2),
        "distance_unit": "angstrom",
        "per_trajectory": per_traj,
        "frame_dt_ns_assumed": FRAME_DT_NS,
        "frame_dt_note": (
            "Lag/ITS reported in frames; ns scale assumes GPCRmd-typical "
            f"{FRAME_DT_NS} ns/frame (MDA dt often uninformative on these XTC)."
        ),
        "loaded_from_cache": None,
    }
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            cache_path,
            replica_names=np.array([x.name for x in xtcs]),
            meta_json=np.array(json.dumps(meta)),
            **{f"replica_{i}": f for i, f in enumerate(features)},
        )
    return features, meta


def fit_tica_kmeans(
    trajs: list[np.ndarray],
) -> tuple[list[np.ndarray], Any, Any, dict[str, Any]]:
    from deeptime.clustering import KMeans
    from deeptime.decomposition import TICA

    tica = TICA(lagtime=TICA_LAG_FRAMES, dim=TICA_DIM)
    tica.fit(trajs)
    model = tica.fetch_model()
    tica_trajs = [model.transform(x) for x in trajs]

    km = KMeans(
        n_clusters=N_MICROSTATES,
        max_iter=KMEANS_MAX_ITER,
        fixed_seed=KMEANS_SEED,
        n_jobs=1,
        progress=None,
    )
    km.fit(tica_trajs)
    dtrajs = [km.transform(x).astype(np.int32) for x in tica_trajs]
    info = {
        "tica_lag_frames": TICA_LAG_FRAMES,
        "tica_dim": TICA_DIM,
        "n_microstates": N_MICROSTATES,
        "kmeans_seed": KMEANS_SEED,
        "kmeans_max_iter": KMEANS_MAX_ITER,
    }
    return dtrajs, model, km.fetch_model(), info


def _fit_msm_at_lag(dtrajs: list[np.ndarray], lag: int):
    from deeptime.markov import TransitionCountEstimator
    from deeptime.markov.msm import MaximumLikelihoodMSM

    counts = (
        TransitionCountEstimator(lagtime=lag, count_mode="sliding")
        .fit(dtrajs)
        .fetch_model()
    )
    # Restrict to largest strongly connected set (deeptime API).
    try:
        counts = counts.submodel_largest(
            connectivity_threshold=0.0, directed=True
        )
    except TypeError:
        counts = counts.submodel_largest()
    if counts.n_states < 1:
        raise RuntimeError("empty count model after connectivity restriction")
    msm = (
        MaximumLikelihoodMSM(reversible=True, sparse=False)
        .fit(counts)
        .fetch_model()
    )
    return msm, counts


def compute_implied_timescales(
    dtrajs: list[np.ndarray], lags: tuple[int, ...], n_its: int
) -> dict[str, Any]:
    its_rows: list[dict[str, Any]] = []
    its_matrix: list[list[float]] = []
    usable_lags: list[int] = []

    for lag in lags:
        if min(len(d) for d in dtrajs) <= lag + 2:
            continue
        try:
            msm, _counts = _fit_msm_at_lag(dtrajs, lag)
            k = min(n_its, max(0, msm.n_states - 1))
            if k == 0:
                ts_list = [float("nan")] * n_its
            else:
                ts = msm.timescales(k=k)
                ts_list = [float(x) for x in np.asarray(ts).ravel()]
                while len(ts_list) < n_its:
                    ts_list.append(float("nan"))
            its_matrix.append(ts_list[:n_its])
            usable_lags.append(int(lag))
            its_rows.append(
                {
                    "lag_frames": int(lag),
                    "lag_ns_assumed": float(lag * FRAME_DT_NS),
                    "timescales_frames": ts_list[:n_its],
                    "n_states_connected": int(msm.n_states),
                }
            )
        except Exception as exc:  # noqa: BLE001
            its_rows.append(
                {
                    "lag_frames": int(lag),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    return {
        "lags_frames": usable_lags,
        "lags_ns_assumed": [float(l * FRAME_DT_NS) for l in usable_lags],
        "n_its_requested": n_its,
        "its_frames": its_matrix,
        "per_lag": its_rows,
    }


def assess_its_convergence(its_data: dict[str, Any]) -> dict[str, Any]:
    """Heuristic ITS flattening of the slowest process vs lag."""
    lags = its_data.get("lags_frames") or []
    mat = its_data.get("its_frames") or []
    per_lag = its_data.get("per_lag") or []
    connected = [
        int(r["n_states_connected"])
        for r in per_lag
        if "n_states_connected" in r
    ]

    if len(lags) < 3 or not mat:
        return {
            "verdict": "NON_CONVERGENT",
            "reason": "insufficient successful ITS lag points",
            "slowest_rel_change": None,
            "recommended_lag_frames": None,
        }

    arr = np.asarray(mat, dtype=float)
    slowest = arr[:, 0]
    finite_pos = np.isfinite(slowest) & (slowest > 0)
    n_finite = int(np.sum(finite_pos))
    n_bad = int(np.sum(~finite_pos))

    # Pathological spectra (NaN/Inf/negative) dominate → non-convergent.
    if n_finite < 3 or n_bad >= max(1, len(slowest) // 2):
        # Prefer smallest lag that still has ≥2 connected states, else 1.
        rec = None
        for r in per_lag:
            if int(r.get("n_states_connected", 0)) >= 2:
                rec = int(r["lag_frames"])
                break
        if rec is None and lags:
            rec = int(lags[0])
        return {
            "verdict": "NON_CONVERGENT",
            "reason": (
                f"pathological ITS spectrum: {n_bad}/{len(slowest)} lags with "
                "non-finite or non-positive slowest timescale; "
                f"connected-state counts={connected}"
            ),
            "slowest_rel_change": None,
            "recommended_lag_frames": rec,
            "n_finite_slowest": n_finite,
            "connected_states_per_lag": connected,
        }

    lags_a = np.asarray(lags, dtype=float)[finite_pos]
    slow = slowest[finite_pos]
    n = slow.size
    t = max(1, n // 3)
    late = float(np.mean(slow[-t:]))
    mid = float(np.mean(slow[-2 * t : -t] if n >= 2 * t else slow[:t]))
    rel = abs(late - mid) / max(abs(mid), 1e-12)

    if rel <= ITS_FLAT_REL_TOL and late > lags_a[-1]:
        verdict = "CONVERGENT"
    elif rel <= ITS_MARGINAL_REL_TOL:
        verdict = "MARGINAL"
    else:
        verdict = "NON_CONVERGENT"

    rec = int(lags_a[-t])
    for lag, ts in zip(lags_a[-t:], slow[-t:]):
        if ts > lag:
            rec = int(lag)
            break
    # Prefer a lag with ≥2 connected microstates when possible
    for r in per_lag:
        if int(r.get("lag_frames", -1)) == rec and int(
            r.get("n_states_connected", 0)
        ) < 2:
            for r2 in per_lag:
                if int(r2.get("n_states_connected", 0)) >= 2:
                    rec = int(r2["lag_frames"])
                    break
            break

    return {
        "verdict": verdict,
        "reason": (
            f"slowest ITS relative change late-vs-mid thirds = {rel:.3f} "
            f"(flat≤{ITS_FLAT_REL_TOL}, marginal≤{ITS_MARGINAL_REL_TOL})"
        ),
        "slowest_rel_change": rel,
        "late_mean_frames": late,
        "mid_mean_frames": mid,
        "recommended_lag_frames": rec,
        "n_finite_slowest": n_finite,
        "connected_states_per_lag": connected,
    }


def choose_n_metastable(msm: Any, max_states: int = 8) -> dict[str, Any]:
    """Pick PCCA+ count from spectral gap among leading eigenvalues."""
    if msm.n_states < 2:
        return {
            "n_metastable": 1,
            "eigenvalues": (
                [float(x) for x in np.asarray(msm.eigenvalues(1)).ravel()]
                if msm.n_states >= 1
                else []
            ),
            "method": "single_connected_state",
            "spectral_gaps": [],
        }
    k = min(max_states + 1, msm.n_states)
    ev = np.asarray(msm.eigenvalues(k), dtype=float)
    if ev.size < 3:
        n = 2
        return {
            "n_metastable": n,
            "eigenvalues": ev.tolist(),
            "method": "fallback_min2",
            "spectral_gaps": [],
        }
    gaps = []
    for i in range(1, len(ev) - 1):
        gaps.append(
            {
                "after_index": i,
                "n_states_if_cut": i + 1,
                "gap": float(abs(ev[i]) - abs(ev[i + 1])),
            }
        )
    cand = [g for g in gaps if 2 <= g["n_states_if_cut"] <= max_states]
    if not cand:
        n = 2
        method = "fallback_min2"
    else:
        best = max(cand, key=lambda g: g["gap"])
        n = int(best["n_states_if_cut"])
        method = "max_spectral_gap"
    n = min(n, msm.n_states)
    return {
        "n_metastable": n,
        "eigenvalues": [float(x) for x in ev],
        "spectral_gaps": gaps,
        "method": method,
    }


def build_msm_pcca(
    dtrajs: list[np.ndarray], lag: int, n_metastable: int | None
) -> dict[str, Any]:
    msm, _counts = _fit_msm_at_lag(dtrajs, lag)
    gap_info = choose_n_metastable(msm)
    n_meta = int(n_metastable or gap_info["n_metastable"])
    n_meta = max(1, min(n_meta, msm.n_states))

    symbols = np.asarray(msm.count_model.state_symbols, dtype=np.int32)
    lookup = np.full(N_MICROSTATES, -1, dtype=np.int32)

    if msm.n_states < 2 or n_meta < 2:
        # Single isolable set — trivial assignment; skip PCCA+ API.
        micro_to_macro = np.zeros(msm.n_states, dtype=np.int32)
        meta_stat = np.array([1.0], dtype=float)
        n_meta = 1
        gap_info = {
            **gap_info,
            "n_metastable": 1,
            "method": gap_info.get("method", "single_connected_state"),
            "note": "PCCA+ skipped: <2 connected microstates at chosen lag",
        }
        for local_i, sym in enumerate(symbols):
            if 0 <= int(sym) < N_MICROSTATES:
                lookup[int(sym)] = 0
    else:
        pcca = msm.pcca(n_meta)
        micro_to_macro = np.asarray(pcca.assignments, dtype=np.int32)
        meta_stat = np.asarray(
            pcca.coarse_grained_stationary_probability, dtype=float
        )
        for local_i, sym in enumerate(symbols):
            if 0 <= int(sym) < N_MICROSTATES and local_i < len(micro_to_macro):
                lookup[int(sym)] = int(micro_to_macro[local_i])

    frame_macro: list[np.ndarray] = []
    for d in dtrajs:
        m = lookup[np.clip(d, 0, N_MICROSTATES - 1)].copy()
        in_set = np.isin(d, symbols)
        m[~in_set] = -1
        frame_macro.append(m)

    all_lab = np.concatenate(frame_macro)
    assigned = all_lab[all_lab >= 0]
    pop_frames = []
    n_assigned = int(assigned.size)
    for s in range(n_meta):
        c = int(np.sum(assigned == s))
        pop_frames.append(
            {
                "macrostate": s,
                "n_frames": c,
                "population_pct_of_assigned_frames": (
                    100.0 * c / n_assigned if n_assigned else 0.0
                ),
                "stationary_probability_pcca": (
                    float(meta_stat[s]) if s < meta_stat.size else float("nan")
                ),
            }
        )

    ts_at_lag: list[float] = []
    if msm.n_states >= 2:
        ts_at_lag = [
            float(x)
            for x in np.asarray(
                msm.timescales(k=min(N_ITS, msm.n_states - 1))
            ).ravel()
        ]

    return {
        "msm": msm,
        "lag_frames": lag,
        "n_connected_microstates": int(msm.n_states),
        "n_metastable": n_meta,
        "spectral_gap_selection": gap_info,
        "populations": pop_frames,
        "n_frames_assigned": n_assigned,
        "n_frames_unassigned": int(np.sum(all_lab < 0)),
        "frame_macro": frame_macro,
        "micro_to_macro": micro_to_macro.tolist(),
        "state_symbols": symbols.tolist(),
        "timescales_at_lag_frames": ts_at_lag,
    }


def plot_its(its_data: dict[str, Any], assessment: dict[str, Any], out_png: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    lags = its_data["lags_frames"]
    mat = np.asarray(its_data["its_frames"], dtype=float)
    fig, ax = plt.subplots(figsize=(7.5, 5.0), dpi=140)
    if len(lags) and mat.size:
        for i in range(mat.shape[1]):
            ax.plot(lags, mat[:, i], "o-", ms=3.5, lw=1.2, label=f"ITS {i + 1}")
        ax.plot(lags, lags, "k--", lw=1.0, label="τ = lag")
    ax.set_xlabel("Lag time (frames)")
    ax.set_ylabel("Implied timescale (frames)")
    ax.set_title(
        "P2 GPCRmd WT MSM — implied timescales\n"
        f"verdict={assessment.get('verdict')} "
        f"(assumed {FRAME_DT_NS} ns/frame)"
    )
    ax.legend(loc="best", fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png)
    plt.close(fig)


def provisional_label(its_verdict: str) -> str:
    """Human-facing lean — does NOT auto-advance the P2 gate."""
    if its_verdict == "CONVERGENT":
        return "READY_FOR_NETWORK_STAGE"
    # MARGINAL and NON_CONVERGENT lean insufficient for Stage-2 networks
    return "P2_INSUFFICIENT_SAMPLING"


def write_reports(
    out_dir: Path,
    payload: dict[str, Any],
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "p2_msm_convergence_report.json"
    md_path = out_dir / "p2_msm_convergence_report.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    its = payload["implied_timescales_assessment"]
    pops = payload["populations"]
    lines = [
        "# P2 MSM convergence report — GPCRmd WT dyn2126",
        "",
        f"**Generated (UTC):** {payload['generated_utc']}",
        f"**Scope:** Stage-1 convergence ONLY (no A/B/C networks, no biology).",
        f"**Data:** Morales-Pastor / GPCRmd publication 1540 / dyn2126 (5 WT replicas).",
        "",
        "## SHA256 verification",
        "",
        f"- Manifest: `{payload['sha256_verification']['manifest']}`",
        f"- All OK: **{payload['sha256_verification']['all_ok']}**",
        "",
        "## Software",
        "",
    ]
    for k, v in payload["software_versions"].items():
        lines.append(f"- `{k}`: {v}")
    lines += [
        "",
        "## Featurization",
        "",
        "- Type: pairwise Cα distances among TM1–TM7",
        "- Numbering: **human CB2 UniProt (P34972) / GPCRdb spans**",
        "",
    ]
    for name, span in CB2_TM_HELICES.items():
        lines.append(f"- **{name}:** {span[0]}–{span[1]}")
    feat = payload["featurization"]
    lines += [
        "",
        f"- n_Cα: {feat['n_ca']}",
        f"- n_pairwise_features: {feat['n_pairwise_features']}",
        f"- n_replicas: {payload['n_replicas']}",
        f"- n_frames_total: {payload['n_frames_total']}",
        f"- frames_per_replica: {payload['frames_per_replica']}",
        "",
        "## Implied timescales",
        "",
        f"- **ITS verdict:** `{its['verdict']}`",
        f"- Detail: {its['reason']}",
        f"- Lag used for MSM/PCCA+: **{payload['lag_used_frames']} frames** "
        f"(~{payload['lag_used_frames'] * FRAME_DT_NS:.0f} ns assumed)",
        f"- Plot: `{payload['artifacts']['implied_timescales_png']}`",
        f"- ITS JSON: `{payload['artifacts']['implied_timescales_json']}`",
        "",
        "## PCCA+",
        "",
        f"- **n_metastable (mathematically isolable):** "
        f"**{payload['n_metastable_pcca']}**",
        f"- Selection method: `{payload['spectral_gap_selection']['method']}`",
        "",
        "## Populations (% of assigned frames)",
        "",
        "| Macrostate | n_frames | population % | π (PCCA stationary) |",
        "|------------|----------|--------------|---------------------|",
    ]
    for row in pops:
        lines.append(
            f"| {row['macrostate']} | {row['n_frames']} | "
            f"{row['population_pct_of_assigned_frames']:.2f} | "
            f"{row['stationary_probability_pcca']:.4f} |"
        )
    lines += [
        "",
        "## Assignments",
        "",
        f"- `{payload['artifacts']['frame_assignments_npz']}`",
        f"- `{payload['artifacts']['dtrajs_micro_npz']}`",
        "",
        "## Provisional label (human decision — NOT auto-advanced)",
        "",
        f"- Lean: **`{payload['provisional_label_for_human']}`**",
        "- Gate remains open for human: declare `P2_INSUFFICIENT_SAMPLING` "
        "vs proceed to network stage.",
        "",
        "## Explicit stop",
        "",
        "- No persistence/communication network extraction.",
        "- No biological interpretation of macrostates.",
        "- No P5 / docking / de novo.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path, json_path


def run(out_dir: Path) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    sha = verify_manifest(MANIFEST_PATH, TRAJ_DIR)
    if not sha["all_ok"]:
        raise SystemExit(
            f"SHA256 verification failed — aborting MSM. Details: {json.dumps(sha, indent=2)}"
        )

    psf = TRAJ_DIR / PSF_NAME
    xtcs = [TRAJ_DIR / n for n in XTC_NAMES]
    for p in [psf, *xtcs]:
        if not p.is_file():
            raise SystemExit(f"Missing required file: {p}")

    print("[P2] Featurizing TM Cα pairwise distances …")
    traj_features, feat_meta = extract_tm_ca_pairwise_distances(psf, xtcs)
    n_frames_total = int(sum(t.shape[0] for t in traj_features))
    frames_per = [int(t.shape[0]) for t in traj_features]

    print("[P2] tICA + K-means …")
    dtrajs, _tica_model, _km_model, cluster_info = fit_tica_kmeans(traj_features)

    print("[P2] Implied timescales …")
    its_data = compute_implied_timescales(dtrajs, ITS_LAGS_FRAMES, N_ITS)
    assessment = assess_its_convergence(its_data)
    its_png = out_dir / "implied_timescales.png"
    its_json = out_dir / "implied_timescales.json"
    plot_its(its_data, assessment, its_png)
    its_json.write_text(
        json.dumps({"its": its_data, "assessment": assessment}, indent=2),
        encoding="utf-8",
    )

    lag = assessment.get("recommended_lag_frames") or 10
    # Clamp to a lag that succeeded
    ok_lags = its_data.get("lags_frames") or [10]
    if lag not in ok_lags:
        lag = int(ok_lags[min(len(ok_lags) // 2, len(ok_lags) - 1)])

    print(f"[P2] MSM + PCCA+ at lag={lag} …")
    msm_pack = build_msm_pcca(dtrajs, lag=lag, n_metastable=None)

    # Save assignments
    dtraj_path = out_dir / "dtrajs_microstates.npz"
    assign_path = out_dir / "frame_macrostate_assignments.npz"
    np.savez_compressed(
        dtraj_path,
        **{f"replica_{i}": d for i, d in enumerate(dtrajs)},
        replica_names=np.array(XTC_NAMES),
    )
    np.savez_compressed(
        assign_path,
        **{f"replica_{i}": a for i, a in enumerate(msm_pack["frame_macro"])},
        replica_names=np.array(XTC_NAMES),
        n_metastable=np.array([msm_pack["n_metastable"]]),
        lag_frames=np.array([lag]),
        micro_to_macro=np.asarray(msm_pack["micro_to_macro"], dtype=np.int32),
    )

    label = provisional_label(assessment["verdict"])
    payload: dict[str, Any] = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stage": "P2_STAGE1_CONVERGENCE_ONLY",
        "auto_advanced": False,
        "data_source": {
            "path": str(TRAJ_DIR.relative_to(ROOT)),
            "gpcrmd_publication_id": 1540,
            "dynamic_id": 2126,
            "psf": PSF_NAME,
            "xtcs": XTC_NAMES,
            "dutta_shukla_role": "NOT_USED",
        },
        "sha256_verification": sha,
        "software_versions": _pkg_versions(),
        "featurization": feat_meta,
        "clustering": cluster_info,
        "n_replicas": len(xtcs),
        "n_frames_total": n_frames_total,
        "frames_per_replica": frames_per,
        "implied_timescales": its_data,
        "implied_timescales_assessment": assessment,
        "lag_used_frames": lag,
        "lag_used_ns_assumed": float(lag * FRAME_DT_NS),
        "n_metastable_pcca": msm_pack["n_metastable"],
        "spectral_gap_selection": msm_pack["spectral_gap_selection"],
        "n_connected_microstates": msm_pack["n_connected_microstates"],
        "timescales_at_lag_frames": msm_pack["timescales_at_lag_frames"],
        "populations": msm_pack["populations"],
        "n_frames_assigned": msm_pack["n_frames_assigned"],
        "n_frames_unassigned": msm_pack["n_frames_unassigned"],
        "provisional_label_for_human": label,
        "artifacts": {
            "implied_timescales_png": str(its_png.relative_to(ROOT)),
            "implied_timescales_json": str(its_json.relative_to(ROOT)),
            "frame_assignments_npz": str(assign_path.relative_to(ROOT)),
            "dtrajs_micro_npz": str(dtraj_path.relative_to(ROOT)),
            "report_md": "results/msm_model/p2_msm_convergence_report.md",
            "report_json": "results/msm_model/p2_msm_convergence_report.json",
        },
        "stop": {
            "networks": False,
            "biology_interpretation": False,
            "p5_docking_denovo": False,
        },
    }
    # Drop bulky MSM object before JSON
    write_reports(out_dir, payload)
    # Re-write JSON without non-serializable leftovers (already clean)
    (out_dir / "p2_msm_convergence_report.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    print("[P2] Done.")
    print(f"  ITS verdict: {assessment['verdict']}")
    print(f"  PCCA+ n_metastable: {msm_pack['n_metastable']}")
    print(f"  Provisional lean: {label}")
    print(f"  Report: {out_dir / 'p2_msm_convergence_report.md'}")
    return payload


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--out-dir",
        type=Path,
        default=OUT_DIR,
        help="Output directory (default: results/msm_model)",
    )
    args = p.parse_args(argv)
    run(args.out_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
