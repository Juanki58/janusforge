#!/usr/bin/env python3
"""EXTERNAL — CB2_APO own MSM (deeptime) → contacts/π by OUR states.

Pre-registration: docs/synthesis/EXPERIMENT_CB2_APO_OWN_MSM.md

Governance
----------
- EXTERNAL reanalysis of local Dutta CB2_APO trajs only.
- Does NOT reopen P2 GPCRmd as CONVERGENT.
- Our macrostates OWN_Sk ≠ Dutta I1–I4; no pickle alignment.
- No Gi claims; docking STOP.
- Do NOT unpack entire 142 GB zip — stratified cache only.

CLI::

    micromamba run -n janus_p1 python scripts/network_core/cb2_apo_own_msm.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from p2_msm_builder import (  # noqa: E402
    ITS_FLAT_REL_TOL,
    ITS_MARGINAL_REL_TOL,
    assess_its_convergence,
    choose_n_metastable,
    compute_implied_timescales,
)

PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_CB2_APO_OWN_MSM.md"
TRAJ_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO"
ZIP_PATH = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO.zip"
TOPOLOGY = TRAJ_DIR / "CB2-APO_inactive_pr_1-strip.prmtop"
CACHE_DIR = TRAJ_DIR / "_cache_own_msm"
NC_DIR = CACHE_DIR / "nc"
FEAT_CACHE = CACHE_DIR / "features_x8_ca.npz"
MANIFEST_CACHE = CACHE_DIR / "extract_manifest.json"

OUT_MSM = ROOT / "results" / "msm_model"
OUT_NET = ROOT / "results" / "network_core"
OUT_JSON = OUT_MSM / "cb2_apo_own_msm_report.json"
OUT_MD = OUT_MSM / "cb2_apo_own_msm_report.md"
OUT_ITS_PNG = OUT_MSM / "cb2_apo_own_msm_its.png"
OUT_ITS_JSON = OUT_MSM / "cb2_apo_own_msm_its.json"
OUT_CONTACT_JSON = OUT_NET / "cb2_apo_own_msm_contacts.json"
OUT_CONTACT_MD = OUT_NET / "cb2_apo_own_msm_contacts.md"

# Locked a priori (EXPERIMENT_CB2_APO_OWN_MSM.md)
N_PER_STATE_DEFAULT = 50
TICA_LAG_FRAMES = 5
TICA_DIM = 5
N_MICROSTATES = 50
KMEANS_MAX_ITER = 500
KMEANS_SEED = 20260912
ITS_LAGS_FRAMES = (1, 2, 5, 10, 15, 20, 25, 30, 40, 50)
N_ITS = 8
FRAME_DT_NS_ASSUMED = 0.1
CK_SOFT_REL_FROB = 0.35
MAX_CACHE_BYTES = 8 * (1 << 30)
MAX_WALL_S = 4 * 3600
EXPECT_N_ATOMS = 4566
CONTACT_FRAMES_CAP = 200
P_IJ_THR = 0.1
THR_J_STABLE = 0.80
THR_FRAC_PRIVATE_B = 0.15
THR_J_DIFFUSE = 0.55
EXTRACT_SEED = 20260912

# X8 UniProt pairs (fixed)
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

UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

AA3_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "CYX": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIE": "H",
    "HID": "H",
    "HIP": "H",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _pkg_versions() -> dict[str, str]:
    out: dict[str, str] = {}
    for name in ("numpy", "scipy", "sklearn", "matplotlib", "MDAnalysis", "deeptime"):
        try:
            mod = __import__(name if name != "sklearn" else "sklearn")
            out[name] = getattr(mod, "__version__", "unknown")
        except Exception as exc:  # noqa: BLE001
            out[name] = f"MISSING ({type(exc).__name__})"
    out["python"] = sys.version.split()[0]
    return out


def git_branch() -> str:
    try:
        import subprocess

        r = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        return (r.stdout or "").strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def nw_align(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> tuple[str, str]:
    n, m = len(a), len(b)
    score = np.zeros((n + 1, m + 1), dtype=np.int32)
    ptr = np.zeros((n + 1, m + 1), dtype=np.uint8)
    for i in range(1, n + 1):
        score[i, 0] = i * gap
        ptr[i, 0] = 1
    for j in range(1, m + 1):
        score[0, j] = j * gap
        ptr[0, j] = 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            s = match if ai == b[j - 1] else mismatch
            diag = score[i - 1, j - 1] + s
            up = score[i - 1, j] + gap
            left = score[i, j - 1] + gap
            best, p = diag, 0
            if up > best:
                best, p = up, 1
            if left > best:
                best, p = left, 2
            score[i, j] = best
            ptr[i, j] = p
    i, j = n, m
    ra: list[str] = []
    rb: list[str] = []
    while i > 0 or j > 0:
        p = ptr[i, j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if i > 0 and j > 0 and p == 0:
            ra.append(a[i - 1])
            rb.append(b[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or p == 1):
            ra.append(a[i - 1])
            rb.append("-")
            i -= 1
        else:
            ra.append("-")
            rb.append(b[j - 1])
            j -= 1
    return "".join(reversed(ra)), "".join(reversed(rb))


def map_uniprot_to_topo(topology: Path) -> dict[str, Any]:
    import MDAnalysis as mda

    u = mda.Universe(str(topology))
    residues = [r for r in u.residues if r.resname not in ("ACE", "NME")]
    pdb_resids: list[int] = []
    pdb_aas: list[str] = []
    for r in residues:
        aa = AA3_TO_1.get(r.resname)
        if aa is None:
            continue
        pdb_resids.append(int(r.resid))
        pdb_aas.append(aa)
    pdb_seq = "".join(pdb_aas)
    up_aln, pdb_aln = nw_align(UNIPROT_P34972, pdb_seq)
    up_i = 0
    pdb_i = 0
    up_to_topo: dict[int, int] = {}
    n_match = 0
    n_aligned = 0
    for ua, pa in zip(up_aln, pdb_aln):
        if ua != "-":
            up_i += 1
        if pa != "-":
            resid = pdb_resids[pdb_i]
            pdb_i += 1
            if ua != "-":
                up_to_topo[up_i] = resid
                n_aligned += 1
                if ua == pa:
                    n_match += 1
    identity = float(n_match) / float(n_aligned) if n_aligned else 0.0

    needed = sorted({r for pair in REDUCED_CA_PAIRS for r in pair})
    mapped_pairs: list[dict[str, Any]] = []
    missing: list[int] = []
    for k, (a, b) in enumerate(REDUCED_CA_PAIRS):
        ta = up_to_topo.get(a)
        tb = up_to_topo.get(b)
        ok = ta is not None and tb is not None
        if not ok:
            missing.extend([x for x in (a, b) if x not in up_to_topo])
        mapped_pairs.append(
            {
                "uniprot": [a, b],
                "topo": [ta, tb],
                "role": PAIR_ROLES[k],
                "ok": ok,
            }
        )
    return {
        "alignment_identity": identity,
        "n_protein_residues": len(pdb_resids),
        "up_to_topo": {str(k): v for k, v in up_to_topo.items()},
        "mapped_pairs": mapped_pairs,
        "missing_uniprot": sorted(set(missing)),
        "all_pairs_ok": len(missing) == 0,
        "topo_resids_needed": sorted(
            {int(p["topo"][0]) for p in mapped_pairs if p["ok"]}
            | {int(p["topo"][1]) for p in mapped_pairs if p["ok"]}
        ),
    }


def list_zip_nc_by_state(zip_path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"inactive": [], "active": []}
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            base = Path(name).name
            if not base.endswith("-strip.nc"):
                continue
            if "_inactive_" in base:
                out["inactive"].append(name)
            elif "_active_" in base:
                out["active"].append(name)
    for k in out:
        out[k] = sorted(out[k])
    return out


def choose_stratified(pool: list[str], n: int, rng: np.random.Generator) -> list[str]:
    if len(pool) < n:
        raise RuntimeError(f"pool size {len(pool)} < requested {n}")
    idx = np.linspace(0, len(pool) - 1, n, dtype=int)
    chosen = sorted(set(int(i) for i in idx))
    while len(chosen) < n:
        extra = int(rng.integers(0, len(pool)))
        if extra not in chosen:
            chosen.append(extra)
    return [pool[i] for i in sorted(chosen)[:n]]


def cache_nbytes() -> int:
    if not CACHE_DIR.is_dir():
        return 0
    total = 0
    for p in CACHE_DIR.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def extract_stratified(n_per_state: int, skip_extract: bool) -> dict[str, Any]:
    NC_DIR.mkdir(parents=True, exist_ok=True)
    if skip_extract and MANIFEST_CACHE.is_file():
        man = json.loads(MANIFEST_CACHE.read_text(encoding="utf-8"))
        files = man.get("files") or {}
        ok_files = True
        for st in ("inactive", "active"):
            for name in files.get(st, []):
                if not (NC_DIR / name).is_file():
                    ok_files = False
                    break
        if ok_files and len(files.get("inactive", [])) == n_per_state:
            man["reused"] = True
            return man

    if not ZIP_PATH.is_file():
        return {"ok": False, "reason": "zip_missing", "path": str(ZIP_PATH)}

    by_state = list_zip_nc_by_state(ZIP_PATH)
    rng = np.random.default_rng(EXTRACT_SEED)
    chosen: dict[str, list[str]] = {}
    for st in ("inactive", "active"):
        members = choose_stratified(by_state[st], n_per_state, rng)
        chosen[st] = members

    # Drop orphan .nc not in the current stratified set so scale-up stays
    # within the locked ≤8 GB cache budget (pilot leftovers otherwise accumulate).
    keep_names = {Path(m).name for members in chosen.values() for m in members}
    for orphan in NC_DIR.glob("*.nc"):
        if orphan.name not in keep_names:
            try:
                orphan.unlink()
            except OSError:
                pass

    extracted: dict[str, list[str]] = {"inactive": [], "active": []}
    bytes_written = 0
    t0 = time.time()
    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        for st in ("inactive", "active"):
            for member in chosen[st]:
                if time.time() - t0 > MAX_WALL_S:
                    return {
                        "ok": False,
                        "reason": "EXT_OWN_MSM_CACHE_LIMIT",
                        "detail": "walltime during extract",
                        "partial": extracted,
                    }
                # cache_nbytes() already includes files written this run — do not
                # add bytes_written (that double-counts and aborts scale-up early).
                if cache_nbytes() > MAX_CACHE_BYTES:
                    return {
                        "ok": False,
                        "reason": "EXT_OWN_MSM_CACHE_LIMIT",
                        "detail": "disk during extract",
                        "partial": extracted,
                        "cache_nbytes": cache_nbytes(),
                        "max_cache_bytes": MAX_CACHE_BYTES,
                    }
                dest = NC_DIR / Path(member).name
                if not dest.is_file():
                    with zf.open(member) as src, dest.open("wb") as dst:
                        while True:
                            chunk = src.read(1 << 20)
                            if not chunk:
                                break
                            dst.write(chunk)
                            bytes_written += len(chunk)
                extracted[st].append(dest.name)

    man = {
        "ok": True,
        "n_per_state": n_per_state,
        "dir": str(NC_DIR.relative_to(ROOT)),
        "files": extracted,
        "zip_members": {k: [Path(m).name for m in v] for k, v in chosen.items()},
        "pool_sizes": {k: len(v) for k, v in by_state.items()},
        "bytes_written_this_run": bytes_written,
        "cache_nbytes": cache_nbytes(),
        "reused": False,
        "seed": EXTRACT_SEED,
    }
    MANIFEST_CACHE.write_text(json.dumps(man, indent=2), encoding="utf-8")
    return man


def _featurize_one(args: tuple[str, str, list[int], list[tuple[int, int]]]) -> dict[str, Any]:
    """Worker: featurize one traj. Args are plain types for pickling."""
    top_s, nc_s, topo_resids, topo_pairs = args
    import MDAnalysis as mda

    u = mda.Universe(top_s, nc_s)
    if int(u.atoms.n_atoms) != EXPECT_N_ATOMS:
        return {
            "ok": False,
            "file": Path(nc_s).name,
            "error": f"n_atoms={u.atoms.n_atoms} expected {EXPECT_N_ATOMS}",
        }
    sel = "protein and name CA and (" + " or ".join(f"resid {r}" for r in topo_resids) + ")"
    atoms = u.select_atoms(sel)
    found = {int(r): i for i, r in enumerate(atoms.resids)}
    missing = [r for r in topo_resids if r not in found]
    if missing:
        return {"ok": False, "file": Path(nc_s).name, "error": f"missing_ca={missing}"}
    idx_pairs = [(found[a], found[b]) for a, b in topo_pairs]
    rows = []
    for _ts in u.trajectory:
        pos = atoms.positions
        row = np.empty(len(idx_pairs), dtype=np.float64)
        for k, (i, j) in enumerate(idx_pairs):
            d = pos[i] - pos[j]
            row[k] = float(np.sqrt(np.dot(d, d)))
        rows.append(row)
    arr = np.asarray(rows, dtype=np.float64)
    return {
        "ok": True,
        "file": Path(nc_s).name,
        "n_frames": int(arr.shape[0]),
        "n_features": int(arr.shape[1]),
        "dt_mda": float(u.trajectory.dt),
        "features": arr,
    }


def featurize_all(
    topology: Path,
    nc_files: list[Path],
    map_info: dict[str, Any],
    max_workers: int,
) -> tuple[list[np.ndarray], list[str], dict[str, Any]]:
    topo_pairs = [
        (int(p["topo"][0]), int(p["topo"][1])) for p in map_info["mapped_pairs"] if p["ok"]
    ]
    topo_resids = sorted({r for a, b in topo_pairs for r in (a, b)})

    if FEAT_CACHE.is_file():
        z = np.load(FEAT_CACHE, allow_pickle=True)
        names = [str(x) for x in z["traj_names"].tolist()]
        want = [p.name for p in nc_files]
        if names == want:
            feats = [z[f"traj_{i}"] for i in range(len(names))]
            meta = json.loads(str(z["meta_json"]))
            meta["loaded_from_cache"] = str(FEAT_CACHE.relative_to(ROOT))
            return feats, names, meta

    jobs = [
        (str(topology), str(p), topo_resids, topo_pairs) for p in nc_files
    ]
    results: list[dict[str, Any] | None] = [None] * len(jobs)
    t0 = time.time()
    workers = max(1, int(max_workers))
    if workers == 1 or len(jobs) == 1:
        for i, job in enumerate(jobs):
            results[i] = _featurize_one(job)
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(_featurize_one, job): i for i, job in enumerate(jobs)}
            for fut in as_completed(futs):
                i = futs[fut]
                results[i] = fut.result()

    features: list[np.ndarray] = []
    names: list[str] = []
    per: list[dict[str, Any]] = []
    for r in results:
        assert r is not None
        if not r.get("ok"):
            raise RuntimeError(f"featurize failed: {r}")
        features.append(np.asarray(r["features"], dtype=np.float64))
        names.append(str(r["file"]))
        per.append(
            {
                "file": r["file"],
                "n_frames": r["n_frames"],
                "n_features": r["n_features"],
                "dt_mda": r["dt_mda"],
            }
        )

    meta = {
        "featurization": "x8_reduced_ca_uniprot_mapped_to_topo",
        "n_features": len(topo_pairs),
        "pairs": map_info["mapped_pairs"],
        "alignment_identity": map_info["alignment_identity"],
        "per_trajectory": per,
        "n_frames_total": int(sum(a.shape[0] for a in features)),
        "frame_dt_ns_assumed": FRAME_DT_NS_ASSUMED,
        "featurize_wall_s": float(time.time() - t0),
        "max_workers": workers,
        "preregistration": str(PREREG.relative_to(ROOT)),
    }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    save = {f"traj_{i}": features[i] for i in range(len(features))}
    np.savez_compressed(
        FEAT_CACHE,
        traj_names=np.asarray(names, dtype=object),
        meta_json=json.dumps(meta),
        **save,
    )
    meta["saved_cache"] = str(FEAT_CACHE.relative_to(ROOT))
    return features, names, meta


def fit_tica_kmeans(trajs: list[np.ndarray]) -> tuple[list[np.ndarray], Any, Any, dict[str, Any]]:
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
    try:
        counts = counts.submodel_largest(connectivity_threshold=0.0, directed=True)
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


def soft_ck_test(dtrajs: list[np.ndarray], lag: int) -> dict[str, Any]:
    """Soft CK: ||T(2τ) - T(τ)^2||_F / ||T(2τ)||_F on overlapping state set."""
    if lag < 1:
        return {"status": "CK_SOFT_NA", "reason": "lag<1"}
    lag2 = 2 * lag
    if min(len(d) for d in dtrajs) <= lag2 + 2:
        return {"status": "CK_SOFT_NA", "reason": "trajs_too_short_for_2lag"}
    try:
        msm1, _ = _fit_msm_at_lag(dtrajs, lag)
        msm2, _ = _fit_msm_at_lag(dtrajs, lag2)
    except Exception as exc:  # noqa: BLE001
        return {"status": "CK_SOFT_NA", "reason": f"{type(exc).__name__}: {exc}"}

    sym1 = np.asarray(msm1.count_model.state_symbols, dtype=np.int32)
    sym2 = np.asarray(msm2.count_model.state_symbols, dtype=np.int32)
    common = sorted(set(sym1.tolist()) & set(sym2.tolist()))
    if len(common) < 2:
        return {
            "status": "CK_SOFT_NA",
            "reason": "fewer_than_2_shared_states",
            "n_shared": len(common),
        }

    def _P_on(msm, symbols_common: list[int]) -> np.ndarray:
        full_sym = np.asarray(msm.count_model.state_symbols, dtype=np.int32)
        loc = {int(s): i for i, s in enumerate(full_sym)}
        P = np.asarray(msm.transition_matrix, dtype=float)
        n = len(symbols_common)
        out = np.zeros((n, n), dtype=float)
        for i, si in enumerate(symbols_common):
            for j, sj in enumerate(symbols_common):
                out[i, j] = P[loc[si], loc[sj]]
        # renormalize rows that have mass in common set
        row_sum = out.sum(axis=1, keepdims=True)
        row_sum[row_sum <= 0] = 1.0
        return out / row_sum

    P1 = _P_on(msm1, common)
    P2 = _P_on(msm2, common)
    pred = P1 @ P1
    denom = float(np.linalg.norm(P2, "fro"))
    if denom <= 1e-12:
        return {"status": "CK_SOFT_NA", "reason": "zero_frobenius_T2"}
    err = float(np.linalg.norm(P2 - pred, "fro") / denom)
    status = "CK_SOFT_PASS" if err <= CK_SOFT_REL_FROB else "CK_SOFT_FAIL"
    return {
        "status": status,
        "lag_frames": lag,
        "lag2_frames": lag2,
        "rel_frobenius_error": err,
        "threshold": CK_SOFT_REL_FROB,
        "n_shared_states": len(common),
    }


def build_msm_pcca(dtrajs: list[np.ndarray], lag: int) -> dict[str, Any]:
    msm, _counts = _fit_msm_at_lag(dtrajs, lag)
    gap_info = choose_n_metastable(msm, max_states=8)
    n_meta = int(gap_info["n_metastable"])
    n_meta = max(1, min(n_meta, msm.n_states))
    symbols = np.asarray(msm.count_model.state_symbols, dtype=np.int32)
    lookup = np.full(N_MICROSTATES, -1, dtype=np.int32)

    if msm.n_states < 2 or n_meta < 2:
        micro_to_macro = np.zeros(msm.n_states, dtype=np.int32)
        meta_stat = np.array([1.0], dtype=float)
        n_meta = 1
        gap_info = {
            **gap_info,
            "n_metastable": 1,
            "note": "PCCA+ skipped: <2 connected microstates",
        }
        for local_i, sym in enumerate(symbols):
            if 0 <= int(sym) < N_MICROSTATES:
                lookup[int(sym)] = 0
    else:
        pcca = msm.pcca(n_meta)
        micro_to_macro = np.asarray(pcca.assignments, dtype=np.int32)
        meta_stat = np.asarray(pcca.coarse_grained_stationary_probability, dtype=float)
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
    pops = []
    n_assigned = int(assigned.size)
    for s in range(n_meta):
        c = int(np.sum(assigned == s))
        pops.append(
            {
                "macrostate": f"OWN_S{s}",
                "macro_index": s,
                "n_frames": c,
                "population_pct_of_assigned_frames": (
                    100.0 * c / n_assigned if n_assigned else 0.0
                ),
                "pi_pcca": float(meta_stat[s]) if s < meta_stat.size else float("nan"),
            }
        )

    return {
        "lag_frames": lag,
        "n_connected_microstates": int(msm.n_states),
        "n_metastable": n_meta,
        "spectral_gap_selection": gap_info,
        "populations": pops,
        "n_frames_assigned": n_assigned,
        "n_frames_unassigned": int(np.sum(all_lab < 0)),
        "frame_macro": frame_macro,
        "note_states": "OWN_Sk are OUR PCCA+ macros — NOT Dutta I1–I4",
    }


def stage0_verdict(its_assess: dict[str, Any], ck: dict[str, Any]) -> dict[str, str]:
    v = str(its_assess.get("verdict") or "NON_CONVERGENT")
    reason = str(its_assess.get("reason") or "")
    ck_st = str(ck.get("status") or "CK_SOFT_NA")
    pathological = "pathological ITS spectrum" in reason or (
        int(its_assess.get("n_finite_slowest") or 0) < 3 and v == "NON_CONVERGENT"
    )
    if v == "CONVERGENT":
        stage = "EXT_OWN_MSM_INTERPRETABLE"
    elif v == "MARGINAL":
        stage = (
            "EXT_OWN_MSM_MARGINAL"
            if ck_st in ("CK_SOFT_PASS", "CK_SOFT_NA")
            else "EXT_OWN_MSM_MARGINAL_CK_WEAK"
        )
    elif pathological or "insufficient successful ITS" in reason:
        stage = "EXT_OWN_MSM_INSUFFICIENT_SAMPLING"
    else:
        stage = "EXT_OWN_MSM_NON_CONVERGENT"

    allow_contacts = stage in (
        "EXT_OWN_MSM_INTERPRETABLE",
        "EXT_OWN_MSM_MARGINAL",
        "EXT_OWN_MSM_MARGINAL_CK_WEAK",
    )
    return {
        "EXT_OWN_MSM_STAGE0": stage,
        "ITS_VERDICT": v,
        "CK_SOFT": ck_st,
        "ALLOW_CONTACTS": "YES" if allow_contacts else "NO",
        "P2_STATUS_UNCHANGED": "CLOSED_INSUFFICIENT_SAMPLING",
        "DUTTA_STATES": "NOT_ALIGNED_OWN_STATES_ONLY",
    }


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
        "CB2_APO own MSM — implied timescales\n"
        f"verdict={assessment.get('verdict')} "
        f"(assumed {FRAME_DT_NS_ASSUMED} ns/frame)"
    )
    ax.legend(loc="best", fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png)
    plt.close(fig)


def edge_key(u: str, v: str) -> tuple[str, str]:
    return (u, v) if u <= v else (v, u)


def jaccard(a: set[tuple[str, str]], b: set[tuple[str, str]]) -> float:
    if not a and not b:
        return 0.0
    union = a | b
    return float(len(a & b) / len(union)) if union else 0.0


def accumulate_vdw_on_frames(
    topology: Path,
    nc_path: Path,
    frame_indices: list[int],
) -> tuple[np.ndarray, list[str], int]:
    """Return count matrix, labels, n_frames_used for selected frames (P1 VdW+0.5)."""
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import capped_distance

    from p1_dynamic_hub_validation import CONTACT_DEF, _MAX_CUT, _SLACK, _VDW, res_label

    u = mda.Universe(str(topology), str(nc_path))
    sel = u.select_atoms("protein")
    heavy = sel.select_atoms("not name H*")
    elements: list[str] = []
    for atom in heavy:
        el = (atom.element if hasattr(atom, "element") else "").upper()
        if not el or el == "DUMMY":
            el = "".join(c for c in atom.name if c.isalpha())[:2].upper()
            if el.startswith("CL"):
                el = "CL"
            elif el.startswith("BR"):
                el = "BR"
            else:
                el = el[:1] if el else "C"
        if el not in _VDW:
            el = "C"
        elements.append(el)
    labels = [res_label(rn, int(ri)) for rn, ri in zip(heavy.resnames, heavy.resids)]
    unique_labels = sorted(
        set(labels), key=lambda x: (x.split(":")[0], int(x.split(":")[1]))
    )
    label_index = {lab: i for i, lab in enumerate(unique_labels)}
    atom_lab_idx = np.asarray([label_index[lab] for lab in labels], dtype=np.int32)
    radii = np.asarray([_VDW[e] for e in elements], dtype=np.float64)
    protein_mask = np.ones(len(unique_labels), dtype=bool)
    resnums = np.asarray([int(lab.split(":")[1]) for lab in unique_labels], dtype=np.int32)
    n = len(unique_labels)
    counts = np.zeros((n, n), dtype=np.int32)
    exclude_seq = bool(CONTACT_DEF["exclude_sequential_protein"])
    n_used = 0
    for fi in frame_indices:
        if fi < 0 or fi >= u.trajectory.n_frames:
            continue
        u.trajectory[fi]
        pos = heavy.positions
        pairs = capped_distance(pos, pos, max_cutoff=_MAX_CUT, return_distances=True)
        if pairs[0].size == 0:
            n_used += 1
            continue
        idx, dist = pairs
        mask = idx[:, 0] < idx[:, 1]
        idx = idx[mask]
        dist = dist[mask]
        lim = radii[idx[:, 0]] + radii[idx[:, 1]] + _SLACK
        hit = dist < lim
        idx = idx[hit]
        if idx.size == 0:
            n_used += 1
            continue
        li = atom_lab_idx[idx[:, 0]]
        lj = atom_lab_idx[idx[:, 1]]
        same = li != lj
        li, lj = li[same], lj[same]
        seen: set[tuple[int, int]] = set()
        for a, b in zip(li.tolist(), lj.tolist()):
            if a > b:
                a, b = b, a
            key = (a, b)
            if key in seen:
                continue
            seen.add(key)
            if exclude_seq and protein_mask[a] and protein_mask[b]:
                if abs(int(resnums[a]) - int(resnums[b])) == 1:
                    continue
            counts[a, b] += 1
            counts[b, a] += 1
        n_used += 1
    return counts, unique_labels, n_used


def edges_from_counts(counts: np.ndarray, labels: list[str], n_used: int) -> set[tuple[str, str]]:
    thr_count = int(np.ceil(P_IJ_THR * n_used)) if n_used else 1
    edges: set[tuple[str, str]] = set()
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            if counts[i, j] >= thr_count:
                edges.add(edge_key(labels[i], labels[j]))
    return edges


def run_contacts(
    topology: Path,
    nc_files: list[Path],
    frame_macro: list[np.ndarray],
    n_meta: int,
    populations: list[dict[str, Any]],
) -> dict[str, Any]:
    rng = np.random.default_rng(EXTRACT_SEED)
    # Collect (traj_i, frame_j) per macro
    by_macro: dict[int, list[tuple[int, int]]] = {s: [] for s in range(n_meta)}
    for ti, labs in enumerate(frame_macro):
        for fi, lab in enumerate(labs):
            if int(lab) >= 0:
                by_macro[int(lab)].append((ti, fi))

    state_edges: dict[str, set[tuple[str, str]]] = {}
    state_meta: dict[str, Any] = {}
    for s in range(n_meta):
        name = f"OWN_S{s}"
        pool = by_macro[s]
        if not pool:
            state_edges[name] = set()
            state_meta[name] = {"n_frames_available": 0, "n_frames_used": 0, "n_edges": 0}
            continue
        if len(pool) > CONTACT_FRAMES_CAP:
            pick = rng.choice(len(pool), size=CONTACT_FRAMES_CAP, replace=False)
            sample = [pool[int(i)] for i in pick]
        else:
            sample = pool

        # group by traj
        by_traj: dict[int, list[int]] = {}
        for ti, fi in sample:
            by_traj.setdefault(ti, []).append(fi)

        counts_acc: np.ndarray | None = None
        labels: list[str] | None = None
        n_used = 0
        for ti, frames in by_traj.items():
            c, labs, nu = accumulate_vdw_on_frames(topology, nc_files[ti], frames)
            if counts_acc is None:
                counts_acc = c.astype(np.int32)
                labels = labs
            else:
                if labs != labels:
                    raise RuntimeError("label mismatch across trajs")
                counts_acc += c
            n_used += nu
        assert counts_acc is not None and labels is not None
        edges = edges_from_counts(counts_acc, labels, n_used)
        state_edges[name] = edges
        state_meta[name] = {
            "n_frames_available": len(pool),
            "n_frames_used": n_used,
            "n_edges": len(edges),
        }

    names = [f"OWN_S{s}" for s in range(n_meta)]
    pairwise = []
    jaccs = []
    fracs = []
    for i, a in enumerate(names):
        ea = state_edges[a]
        priv = []
        for j, b in enumerate(names):
            if i >= j:
                continue
            eb = state_edges[b]
            jac = jaccard(ea, eb)
            jaccs.append(jac)
            pairwise.append({"a": a, "b": b, "jaccard": jac})
        for b in names:
            if a == b:
                continue
            eb = state_edges[b]
            if ea:
                priv.append(len(ea - eb) / len(ea))
        fracs.append(float(np.mean(priv)) if priv else 0.0)

    mean_j = float(np.mean(jaccs)) if jaccs else float("nan")
    mean_fp = float(np.mean(fracs)) if fracs else float("nan")

    if n_meta < 2 or not any(state_edges[n] for n in names):
        contact_verdict = "EXT_OWN_MSM_CONTACTS_INDETERMINATE"
    elif mean_j >= THR_J_STABLE and mean_fp < THR_FRAC_PRIVATE_B:
        contact_verdict = "EXT_OWN_MSM_CONTACTS_STABLE"
    elif mean_fp >= THR_FRAC_PRIVATE_B:
        contact_verdict = "EXT_OWN_MSM_CONTACTS_STATE_DEPENDENT"
    elif mean_j < THR_J_DIFFUSE and mean_fp < THR_FRAC_PRIVATE_B:
        contact_verdict = "EXT_OWN_MSM_CONTACTS_DIFFUSE"
    else:
        contact_verdict = "EXT_OWN_MSM_CONTACTS_INDETERMINATE"

    return {
        "verdict": contact_verdict,
        "mean_pairwise_jaccard": mean_j,
        "mean_frac_private": mean_fp,
        "pairwise_jaccard": pairwise,
        "per_state": {
            k: {
                **state_meta[k],
                "pi_pcca": next(
                    (p["pi_pcca"] for p in populations if p["macrostate"] == k),
                    None,
                ),
            }
            for k in names
        },
        "note": "OWN_Sk ≠ Dutta I1–I4; soft A/B/C at contact-map level only",
    }


def write_abort_contacts(reason: str, stage0: dict[str, str]) -> None:
    payload = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "aborted": True,
        "reason": reason,
        "verdicts": {
            **stage0,
            "EXT_OWN_MSM_CONTACTS": "ABORTED",
        },
        "note": "Contacts aborted — no fabricated A/B/C architecture",
    }
    OUT_NET.mkdir(parents=True, exist_ok=True)
    OUT_CONTACT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# CB2_APO own MSM — contacts (ABORTED)",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Reason:** `{reason}`",
        f"**Stage-0:** `{stage0.get('EXT_OWN_MSM_STAGE0')}`",
        "",
        "Contacts **not** computed. No A/B/C story invented.",
        "",
        "- Our states ≠ Dutta I1–I4.",
        "- P2 remains CLOSED (INSUFFICIENT_SAMPLING).",
        "",
    ]
    OUT_CONTACT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_msm_report(payload: dict[str, Any]) -> None:
    OUT_MSM.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    v = payload["verdicts"]
    its = payload["implied_timescales_assessment"]
    lines = [
        "# EXTERNAL — CB2_APO **own** MSM report",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_APO_OWN_MSM.md`",
        f"**Commit tip (at run):** see git after commit",
        "",
        "## Epistemology",
        "",
        "- EXTERNAL own MSM on stratified local `CB2_APO` trajs (not full 142 GB unpack).",
        "- **Our states `OWN_Sk` ≠ Dutta I1–I4**; no Final_MSM pickle alignment.",
        "- Does **not** reopen P2 GPCRmd as CONVERGENT. No Gi / docking.",
        "",
        "## Verdicts",
        "",
        f"- **Stage-0:** `{v['EXT_OWN_MSM_STAGE0']}`",
        f"- ITS: `{v['ITS_VERDICT']}`",
        f"- Soft CK: `{v['CK_SOFT']}`",
        f"- Allow contacts: `{v['ALLOW_CONTACTS']}`",
        f"- P2 unchanged: `{v['P2_STATUS_UNCHANGED']}`",
        f"- Dutta states: `{v['DUTTA_STATES']}`",
        "",
        "## Sampling",
        "",
        f"- N per filename class (inactive/active): **{(payload.get('sampling') or {}).get('n_per_state', 'NA')}**",
        f"- N trajs total: **{(payload.get('sampling') or {}).get('n_trajs', 'NA')}**",
        f"- n_frames_total: **{(payload.get('featurization') or {}).get('n_frames_total', 'NA')}**",
        f"- Cache: `{(payload.get('sampling') or {}).get('cache_dir', 'NA')}`",
        f"- Assumed frame dt: **{FRAME_DT_NS_ASSUMED} ns** (MDA dts recorded in JSON)",
        "",
        "## Featurization",
        "",
        "- X8-like 24 Cα–Cα (UniProt → topo via alignment)",
        f"- Alignment identity: `{(payload.get('residue_map') or {}).get('alignment_identity')}`",
        f"- All pairs OK: `{(payload.get('residue_map') or {}).get('all_pairs_ok')}`",
        "",
        "## MSM / ITS",
        "",
        f"- tICA lag={TICA_LAG_FRAMES}, dim={TICA_DIM}; K-means K={N_MICROSTATES}",
        f"- **ITS verdict:** `{(its or {}).get('verdict')}`",
        f"- Detail: {(its or {}).get('reason')}",
        f"- Recommended lag: **{(its or {}).get('recommended_lag_frames')}** frames",
        f"- Soft CK: `{payload.get('soft_ck', {})}`",
        f"- ITS plot: `{OUT_ITS_PNG.relative_to(ROOT)}`",
        "",
        "## PCCA+ / π (our states)",
        "",
    ]
    pops = payload.get("populations") or []
    if pops:
        lines += [
            "| Macrostate | n_frames | pop % | π (PCCA) |",
            "|------------|----------|-------|----------|",
        ]
        for p in pops:
            lines.append(
                f"| `{p['macrostate']}` | {p['n_frames']} | "
                f"{p['population_pct_of_assigned_frames']:.2f} | {p['pi_pcca']:.4f} |"
            )
    else:
        lines.append("_No populations (Stage-0 abort before PCCA+)._")
    lines += [
        "",
        "## Contacts",
        "",
        f"- See `results/network_core/cb2_apo_own_msm_contacts.md`",
        f"- Contact verdict (if run): `{payload.get('contacts_verdict', 'ABORTED_OR_PENDING')}`",
        "",
        "## Software",
        "",
    ]
    for k, val in payload.get("software_versions", {}).items():
        lines.append(f"- `{k}`: {val}")
    lines += [
        "",
        "## Hard locks",
        "",
        "- P2 CLOSED (INSUFFICIENT_SAMPLING) — unchanged",
        "- No fake alignment to Dutta pickles",
        "- No Gi / docking",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def write_contact_report(payload: dict[str, Any], stage0: dict[str, str]) -> None:
    OUT_NET.mkdir(parents=True, exist_ok=True)
    full = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "aborted": False,
        "verdicts": {
            **stage0,
            "EXT_OWN_MSM_CONTACTS": payload["verdict"],
        },
        "metrics": payload,
    }
    OUT_CONTACT_JSON.write_text(json.dumps(full, indent=2), encoding="utf-8")
    lines = [
        "# CB2_APO own MSM — per-state contacts (OUR states)",
        "",
        f"**Generated (UTC):** `{full['generated_utc']}`",
        f"**Contact verdict:** `{payload['verdict']}`",
        f"**Stage-0:** `{stage0.get('EXT_OWN_MSM_STAGE0')}`",
        "",
        "## Epistemology",
        "",
        "- Edges by **our** `OWN_Sk` macros only.",
        "- **≠** Dutta I1–I4. Soft contact-map class ≠ P2 A/B/C architecture.",
        "",
        "## Metrics",
        "",
        f"- mean pairwise Jaccard = **{payload['mean_pairwise_jaccard']:.4f}**",
        f"- mean frac_private = **{payload['mean_frac_private']:.4f}**",
        "",
        "### Per state",
        "",
        "| State | n_frames_used | n_edges | π_pcca |",
        "|-------|---------------|---------|--------|",
    ]
    for k, info in payload["per_state"].items():
        pi = info.get("pi_pcca")
        pi_s = f"{pi:.4f}" if isinstance(pi, float) else "na"
        lines.append(
            f"| `{k}` | {info.get('n_frames_used')} | {info.get('n_edges')} | {pi_s} |"
        )
    lines += ["", "### Pairwise Jaccard", ""]
    for row in payload.get("pairwise_jaccard") or []:
        lines.append(f"- `{row['a']}` vs `{row['b']}`: {row['jaccard']:.4f}")
    lines += ["", "*Fin.*", ""]
    OUT_CONTACT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-per-state", type=int, default=N_PER_STATE_DEFAULT)
    ap.add_argument("--max-workers", type=int, default=4)
    ap.add_argument("--skip-extract", action="store_true")
    ap.add_argument(
        "--force-contacts",
        action="store_true",
        help="Dev only: run contacts even if Stage-0 would abort (not for primary PI run)",
    )
    args = ap.parse_args()
    t_wall0 = time.time()

    if not PREREG.is_file():
        print("[own_msm] FATAL: pre-registration missing", PREREG)
        return 2
    if not TOPOLOGY.is_file():
        payload = {
            "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "verdicts": {
                "EXT_OWN_MSM_STAGE0": "EXT_OWN_MSM_INDETERMINATE",
                "ALLOW_CONTACTS": "NO",
            },
            "error": "topology_missing",
        }
        write_msm_report(
            {
                **payload,
                "branch": git_branch(),
                "sampling": {},
                "featurization": {},
                "residue_map": {},
                "implied_timescales_assessment": {},
                "software_versions": _pkg_versions(),
            }
        )
        write_abort_contacts("topology_missing", payload["verdicts"])
        return 1

    print("[own_msm] mapping UniProt → topo …")
    map_info = map_uniprot_to_topo(TOPOLOGY)
    if not map_info["all_pairs_ok"]:
        print("[own_msm] FATAL: pair map incomplete", map_info["missing_uniprot"])
        v = {
            "EXT_OWN_MSM_STAGE0": "EXT_OWN_MSM_INDETERMINATE",
            "ITS_VERDICT": "NA",
            "CK_SOFT": "CK_SOFT_NA",
            "ALLOW_CONTACTS": "NO",
            "P2_STATUS_UNCHANGED": "CLOSED_INSUFFICIENT_SAMPLING",
            "DUTTA_STATES": "NOT_ALIGNED_OWN_STATES_ONLY",
        }
        write_msm_report(
            {
                "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "branch": git_branch(),
                "verdicts": v,
                "sampling": {},
                "featurization": {},
                "residue_map": map_info,
                "implied_timescales_assessment": {},
                "software_versions": _pkg_versions(),
            }
        )
        write_abort_contacts("featurization_map_fail", v)
        return 1

    print(f"[own_msm] extracting stratified {args.n_per_state}+{args.n_per_state} …")
    extract = extract_stratified(args.n_per_state, skip_extract=args.skip_extract)
    if not extract.get("ok"):
        v = {
            "EXT_OWN_MSM_STAGE0": extract.get("reason", "EXT_OWN_MSM_INDETERMINATE"),
            "ITS_VERDICT": "NA",
            "CK_SOFT": "CK_SOFT_NA",
            "ALLOW_CONTACTS": "NO",
            "P2_STATUS_UNCHANGED": "CLOSED_INSUFFICIENT_SAMPLING",
            "DUTTA_STATES": "NOT_ALIGNED_OWN_STATES_ONLY",
        }
        write_msm_report(
            {
                "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "branch": git_branch(),
                "verdicts": v,
                "sampling": {
                    "n_per_state": args.n_per_state,
                    "n_trajs": "NA",
                    "cache_dir": str(CACHE_DIR.relative_to(ROOT)),
                    "extract": extract,
                },
                "featurization": {},
                "residue_map": map_info,
                "implied_timescales_assessment": {},
                "software_versions": _pkg_versions(),
            }
        )
        write_abort_contacts(str(extract.get("reason")), v)
        return 1

    nc_files: list[Path] = []
    for st in ("inactive", "active"):
        for name in extract["files"][st]:
            nc_files.append(NC_DIR / name)

    print(f"[own_msm] featurizing {len(nc_files)} trajs (workers={args.max_workers}) …")
    features, names, feat_meta = featurize_all(
        TOPOLOGY, nc_files, map_info, max_workers=args.max_workers
    )
    print(f"[own_msm] frames_total={feat_meta['n_frames_total']}")

    # Monkeypatch FRAME_DT_NS in compute path via local wrapper
    print("[own_msm] tICA + K-means …")
    dtrajs, _tica, _km, tica_info = fit_tica_kmeans(features)

    print("[own_msm] ITS grid …")
    # compute_implied_timescales uses FRAME_DT_NS from p2 — overwrite reporting below
    its_data = compute_implied_timescales(dtrajs, ITS_LAGS_FRAMES, N_ITS)
    # rewrite assumed ns for our dt
    its_data["lags_ns_assumed"] = [
        float(l * FRAME_DT_NS_ASSUMED) for l in its_data.get("lags_frames") or []
    ]
    for row in its_data.get("per_lag") or []:
        if "lag_frames" in row:
            row["lag_ns_assumed"] = float(row["lag_frames"] * FRAME_DT_NS_ASSUMED)

    assessment = assess_its_convergence(its_data)
    # Patch tolerances note (same constants)
    assessment["tol_flat"] = ITS_FLAT_REL_TOL
    assessment["tol_marginal"] = ITS_MARGINAL_REL_TOL

    OUT_MSM.mkdir(parents=True, exist_ok=True)
    plot_its(its_data, assessment, OUT_ITS_PNG)
    OUT_ITS_JSON.write_text(json.dumps(its_data, indent=2), encoding="utf-8")

    lag = int(assessment.get("recommended_lag_frames") or 1)
    print(f"[own_msm] soft CK at lag={lag} …")
    ck = soft_ck_test(dtrajs, lag)
    verdicts = stage0_verdict(assessment, ck)
    print(f"[own_msm] Stage-0={verdicts['EXT_OWN_MSM_STAGE0']}")

    populations: list[dict[str, Any]] = []
    msm_pack: dict[str, Any] | None = None
    contacts_verdict = "ABORTED"
    if verdicts["ALLOW_CONTACTS"] == "YES" or args.force_contacts:
        print(f"[own_msm] MSM + PCCA+ at lag={lag} …")
        msm_pack = build_msm_pcca(dtrajs, lag)
        populations = msm_pack["populations"]
        # save assignments
        np.savez_compressed(
            OUT_MSM / "cb2_apo_own_msm_assignments.npz",
            **{f"macro_{i}": msm_pack["frame_macro"][i] for i in range(len(dtrajs))},
            traj_names=np.asarray(names, dtype=object),
            n_metastable=np.array([msm_pack["n_metastable"]]),
        )
        if verdicts["ALLOW_CONTACTS"] == "YES" or args.force_contacts:
            if msm_pack["n_metastable"] >= 1:
                print("[own_msm] per-state contacts …")
                try:
                    cpay = run_contacts(
                        TOPOLOGY,
                        nc_files,
                        msm_pack["frame_macro"],
                        msm_pack["n_metastable"],
                        populations,
                    )
                    contacts_verdict = cpay["verdict"]
                    write_contact_report(cpay, verdicts)
                except Exception as exc:  # noqa: BLE001
                    print(f"[own_msm] contacts failed: {exc}")
                    write_abort_contacts(f"contacts_error:{type(exc).__name__}", verdicts)
                    contacts_verdict = "ABORTED"
            else:
                write_abort_contacts("n_metastable<1", verdicts)
    else:
        write_abort_contacts(verdicts["EXT_OWN_MSM_STAGE0"], verdicts)

    wall_s = float(time.time() - t_wall0)
    payload = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "branch": git_branch(),
        "preregistration": str(PREREG.relative_to(ROOT)),
        "verdicts": verdicts,
        "sampling": {
            "n_per_state": args.n_per_state,
            "n_trajs": len(nc_files),
            "cache_dir": str(CACHE_DIR.relative_to(ROOT)),
            "extract": {k: extract[k] for k in extract if k != "zip_members"},
            "traj_names": names,
            "filename_class_note": (
                "inactive/active in filenames = deposit start-structure class, "
                "NOT our MSM states"
            ),
        },
        "residue_map": {
            "alignment_identity": map_info["alignment_identity"],
            "all_pairs_ok": map_info["all_pairs_ok"],
            "n_protein_residues": map_info["n_protein_residues"],
            "mapped_pairs": map_info["mapped_pairs"],
        },
        "featurization": feat_meta,
        "tica_kmeans": tica_info,
        "implied_timescales_assessment": assessment,
        "implied_timescales": {
            "lags_frames": its_data.get("lags_frames"),
            "n_its": N_ITS,
            "plot": str(OUT_ITS_PNG.relative_to(ROOT)),
            "json": str(OUT_ITS_JSON.relative_to(ROOT)),
        },
        "soft_ck": ck,
        "lag_used_frames": lag,
        "populations": populations,
        "n_metastable_pcca": (msm_pack or {}).get("n_metastable"),
        "contacts_verdict": contacts_verdict,
        "software_versions": _pkg_versions(),
        "topology_sha256": sha256_file(TOPOLOGY)[:16] + "…",
        "wall_s": wall_s,
        "budgets": {
            "max_cache_bytes": MAX_CACHE_BYTES,
            "max_wall_s": MAX_WALL_S,
            "cache_nbytes": cache_nbytes(),
        },
        "epistemology": {
            "own_states_ne_dutta_I1_I4": True,
            "p2_reopened": False,
            "gi_claims": False,
            "docking": False,
            "full_zip_unpacked": False,
        },
    }
    write_msm_report(payload)
    print(f"[own_msm] wrote {OUT_MD}")
    print(f"[own_msm] Stage-0={verdicts['EXT_OWN_MSM_STAGE0']} contacts={contacts_verdict}")
    print(f"[own_msm] wall_s={wall_s:.1f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
