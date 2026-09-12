#!/usr/bin/env python3
"""EXTERNAL fallback — CB2_APO TM6/toggle features by filename inactive/active.

Pre-registration: docs/synthesis/EXPERIMENT_CB2_ESMDYNAMIC.md (fallback section).

Filename inactive/active = simulation start label ONLY — NOT MSM macrostates.
Does NOT reopen P2 as CONVERGENT; no Gi claims; no fake filelist alignment.

Outputs:
  results/network_core/cb2_apo_tm6_toggle.{md,json}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from dynamic_pipeline import HUBS  # noqa: E402
from x8_reduced_featurization_msm import PAIR_ROLES, REDUCED_CA_PAIRS  # noqa: E402

try:
    import MDAnalysis as mda
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required: {e}") from e

TRAJ_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "trajectories" / "CB2_APO"
TOPOLOGY = TRAJ_DIR / "CB2-APO_inactive_pr_1-strip.prmtop"
SAMPLE_DIR = TRAJ_DIR / "_pilot_sample"
PRIMARY = {
    "inactive": TRAJ_DIR / "CB2-APO_inactive_pr_9_frame_99-strip.nc",
    "active": TRAJ_DIR / "CB2-APO_active_pr_10_frame_28-strip.nc",
}
OUT_DIR = ROOT / "results" / "network_core"
OUT_JSON = OUT_DIR / "cb2_apo_tm6_toggle.json"
OUT_MD = OUT_DIR / "cb2_apo_tm6_toggle.md"
PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_CB2_ESMDYNAMIC.md"

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

# Primary toggle subset indices into REDUCED_CA_PAIRS (0-based), locked in prereg
PRIMARY_PAIR_IDX = (0, 1, 2, 4, 9, 10)
IC_OPENING_IDX = (0, 1, 2)  # expect active mean larger
FRAME_CAP = 200
SEED = 20260912
THR_D = 0.8
EXPECT_N_ATOMS = 4566


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_branch() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=ROOT,
                text=True,
            ).strip()
        )
    except Exception:
        return "unknown"


def nw_align(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -1):
    n, m = len(a), len(b)
    dp = np.zeros((n + 1, m + 1), dtype=np.int32)
    ptr = np.zeros((n + 1, m + 1), dtype=np.int8)
    for i in range(1, n + 1):
        dp[i, 0] = i * gap
        ptr[i, 0] = 1
    for j in range(1, m + 1):
        dp[0, j] = j * gap
        ptr[0, j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if a[i - 1] == b[j - 1] else mismatch
            diag = dp[i - 1, j - 1] + s
            up = dp[i - 1, j] + gap
            left = dp[i, j - 1] + gap
            best = max(diag, up, left)
            dp[i, j] = best
            ptr[i, j] = 0 if best == diag else (1 if best == up else 2)
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


def uniprot_to_topo(u: mda.Universe) -> dict[str, Any]:
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
    offsets = [topo - up for up, topo in up_to_topo.items()]
    return {
        "alignment_identity": identity,
        "n_protein_residues": len(pdb_resids),
        "up_to_topo": up_to_topo,
        "median_offset_topo_minus_uniprot": int(np.median(offsets)) if offsets else None,
        "note": "UniProt P34972 → topo resid; expect ~-20 on Dutta construct",
    }


def resolve_trajs(mode: str) -> dict[str, list[Path]]:
    if mode == "sample5":
        if not SAMPLE_DIR.is_dir():
            raise SystemExit(f"Missing sample dir: {SAMPLE_DIR}")
        inactive = sorted(
            p for p in SAMPLE_DIR.glob("*-strip.nc") if "_inactive_" in p.name
        )
        active = sorted(
            p for p in SAMPLE_DIR.glob("*-strip.nc") if "_active_" in p.name
        )
        if len(inactive) < 1 or len(active) < 1:
            raise SystemExit("sample5 empty")
        return {"inactive": inactive, "active": active}
    # primary 1+1
    for st, p in PRIMARY.items():
        if not p.is_file():
            raise SystemExit(f"Missing primary traj: {p}")
    return {"inactive": [PRIMARY["inactive"]], "active": [PRIMARY["active"]]}


def extract_pair_timeseries(
    top: Path,
    nc: Path,
    topo_pairs: list[tuple[int, int]],
    frame_cap: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, dict[str, Any]]:
    u = mda.Universe(str(top), str(nc))
    smoke = {
        "file": nc.name,
        "n_atoms": int(u.atoms.n_atoms),
        "n_frames": int(u.trajectory.n_frames),
        "atoms_ok": int(u.atoms.n_atoms) == EXPECT_N_ATOMS,
        "sha256": sha256_file(nc),
    }
    needed = sorted({r for pair in topo_pairs for r in pair})
    sel = "protein and name CA and (" + " or ".join(f"resid {r}" for r in needed) + ")"
    atoms = u.select_atoms(sel)
    found = {int(r): i for i, r in enumerate(atoms.resids)}
    missing = [r for r in needed if r not in found]
    if missing:
        raise RuntimeError(f"Missing Cα residues in {nc.name}: {missing}")
    idx_pairs = [(found[a], found[b]) for a, b in topo_pairs]
    n_frames = int(u.trajectory.n_frames)
    if n_frames <= frame_cap:
        frame_idx = np.arange(n_frames)
    else:
        frame_idx = np.linspace(0, n_frames - 1, frame_cap, dtype=int)
        # deterministic jitter via seed already set outside
        _ = rng.integers(0, 1)  # keep rng advanced consistently
    rows = []
    for fi in frame_idx:
        u.trajectory[int(fi)]
        pos = atoms.positions
        row = np.empty(len(idx_pairs), dtype=np.float64)
        for k, (i, j) in enumerate(idx_pairs):
            d = pos[i] - pos[j]
            row[k] = float(np.sqrt(np.dot(d, d)))
        rows.append(row)
    return np.asarray(rows, dtype=np.float64), smoke


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d for active - inactive (pooled std)."""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    va, vb = float(np.var(a, ddof=1)), float(np.var(b, ddof=1))
    pooled = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled == 0:
        return 0.0
    return float((np.mean(b) - np.mean(a)) / pooled)


def analyze(mode: str, frame_cap: int) -> dict[str, Any]:
    if not TOPOLOGY.is_file():
        raise SystemExit(f"Missing topology: {TOPOLOGY}")
    if not PREREG.is_file():
        raise SystemExit(f"Missing prereg: {PREREG}")

    u0 = mda.Universe(str(TOPOLOGY))
    mapping = uniprot_to_topo(u0)
    up_to_topo = mapping["up_to_topo"]

    topo_pairs: list[tuple[int, int]] = []
    pair_meta: list[dict[str, Any]] = []
    map_fail = False
    for k, ((ua, ub), role) in enumerate(zip(REDUCED_CA_PAIRS, PAIR_ROLES)):
        ta, tb = up_to_topo.get(ua), up_to_topo.get(ub)
        ok = ta is not None and tb is not None
        if not ok:
            map_fail = True
        topo_pairs.append((int(ta) if ta else -1, int(tb) if tb else -1))
        pair_meta.append(
            {
                "index": k,
                "role": role,
                "uniprot": [ua, ub],
                "topo": [ta, tb],
                "primary": k in PRIMARY_PAIR_IDX,
                "ic_opening": k in IC_OPENING_IDX,
                "map_ok": ok,
            }
        )
    if map_fail or any(a < 0 or b < 0 for a, b in topo_pairs):
        return {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "branch": git_branch(),
            "experiment": "EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME",
            "verdicts": {
                "EXT_APO_TM6_TOGGLE": "EXT_APO_TM6_TOGGLE_INDETERMINATE",
                "reason": "HUB_OR_PAIR_MAP_FAIL",
            },
            "mapping": mapping,
            "pairs": pair_meta,
        }

    trajs = resolve_trajs(mode)
    rng = np.random.default_rng(SEED)
    pooled: dict[str, list[np.ndarray]] = {"inactive": [], "active": []}
    smokes: dict[str, list[dict[str, Any]]] = {"inactive": [], "active": []}
    for st in ("inactive", "active"):
        for nc in trajs[st]:
            arr, smoke = extract_pair_timeseries(
                TOPOLOGY, nc, topo_pairs, frame_cap, rng
            )
            pooled[st].append(arr)
            smokes[st].append(smoke)

    X = {
        st: np.vstack(pooled[st]) if pooled[st] else np.zeros((0, len(topo_pairs)))
        for st in ("inactive", "active")
    }

    feature_rows: list[dict[str, Any]] = []
    for k, meta in enumerate(pair_meta):
        a = X["inactive"][:, k]
        b = X["active"][:, k]
        d = cohens_d(a, b)
        try:
            u_stat, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")
            p_u = float(p_u)
            u_stat = float(u_stat)
        except Exception:
            u_stat, p_u = float("nan"), float("nan")
        feature_rows.append(
            {
                **meta,
                "mean_inactive": float(np.mean(a)),
                "std_inactive": float(np.std(a, ddof=1)) if len(a) > 1 else 0.0,
                "mean_active": float(np.mean(b)),
                "std_active": float(np.std(b, ddof=1)) if len(b) > 1 else 0.0,
                "delta_active_minus_inactive": float(np.mean(b) - np.mean(a)),
                "cohens_d": d,
                "mannwhitney_u": u_stat,
                "mannwhitney_p": p_u,
                "n_frames_inactive": int(len(a)),
                "n_frames_active": int(len(b)),
                "abs_d_ge_0_8": bool(abs(d) >= THR_D) if d == d else False,
            }
        )

    primary = [r for r in feature_rows if r["primary"]]
    n_sep = sum(1 for r in primary if r["abs_d_ge_0_8"])
    ic = [r for r in feature_rows if r["ic_opening"]]
    n_open_sign = sum(
        1 for r in ic if r["delta_active_minus_inactive"] > 0 and r["abs_d_ge_0_8"]
    )
    # Also count opening sign among IC even if weaker, for annotation
    n_open_sign_any = sum(1 for r in ic if r["delta_active_minus_inactive"] > 0)

    if n_sep >= 4 and n_open_sign >= 3:
        primary_v = "EXT_APO_TM6_TOGGLE_SEPARATED"
    elif n_sep < 2:
        primary_v = "EXT_APO_TM6_TOGGLE_OVERLAP"
    else:
        primary_v = "EXT_APO_TM6_TOGGLE_INDETERMINATE"

    hub_up = {int(h["label"].split(":")[1]) for h in HUBS}
    hub_touch = [
        r
        for r in feature_rows
        if r["uniprot"][0] in hub_up or r["uniprot"][1] in hub_up
    ]

    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "branch": git_branch(),
        "experiment": "EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME",
        "preregistration": str(PREREG.relative_to(ROOT)),
        "epistemology": {
            "filename_inactive_active_neq_msm_macrostate": True,
            "not_msm_state_contacts": True,
            "does_not_reopen_P2_CONVERGENT": True,
            "no_Gi_claim": True,
            "fallback_for": "EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE",
        },
        "run_mode": mode,
        "frame_cap": frame_cap,
        "seed": SEED,
        "thresholds": {
            "cohens_d_abs": THR_D,
            "n_primary_for_separated": 4,
            "n_ic_opening_sign_for_separated": 3,
        },
        "topology": {
            "file": TOPOLOGY.name,
            "sha256": sha256_file(TOPOLOGY),
            "path": str(TOPOLOGY.relative_to(ROOT)),
        },
        "mapping": {
            k: v for k, v in mapping.items() if k != "up_to_topo"
        },
        "trajs": {
            st: [{"file": s["file"], "n_frames": s["n_frames"], "n_atoms": s["n_atoms"],
                  "atoms_ok": s["atoms_ok"], "sha256": s["sha256"]} for s in smokes[st]]
            for st in ("inactive", "active")
        },
        "n_frames_pooled": {
            "inactive": int(X["inactive"].shape[0]),
            "active": int(X["active"].shape[0]),
        },
        "features": feature_rows,
        "primary_summary": {
            "n_primary": len(primary),
            "n_abs_d_ge_0_8": n_sep,
            "n_ic_opening_sign_and_d": n_open_sign,
            "n_ic_opening_sign_any": n_open_sign_any,
        },
        "hub_adjacent_features": [
            {
                "role": r["role"],
                "uniprot": r["uniprot"],
                "cohens_d": r["cohens_d"],
                "delta": r["delta_active_minus_inactive"],
            }
            for r in hub_touch
        ],
        "verdicts": {
            "EXT_APO_TM6_TOGGLE": primary_v,
            "EXT_APO_TM6_FILENAME_NEQ_MSM": True,
            "P2_STATUS_UNCHANGED": "CLOSED_INSUFFICIENT_SAMPLING",
            "EXT_MSM_FILELIST": "NOT_FABRICATED",
            "SOFT_COMPARE_PRIOR_PDB_B": (
                "EXT_APO_TM6_SOFT_COMPAT_STATE_DEPENDENT"
                if primary_v == "EXT_APO_TM6_TOGGLE_SEPARATED"
                else "EXT_APO_TM6_SOFT_NOT_CLEAR_STATE_DEPENDENT"
            ),
        },
        "pi_summary_es": (
            f"Fallback TM6/toggle (filename inactive vs active, N_traj="
            f"{len(trajs['inactive'])}+{len(trajs['active'])}): "
            f"**{primary_v}** — primary pairs |d|≥0.8: {n_sep}/6; "
            f"apertura IC (active>inactive y |d|≥0.8): {n_open_sign}/3. "
            "Etiqueta de arranque ≠ macroestado MSM; no reabre P2; "
            "no sustituye ESMDynamic ni contactos MSM."
        ),
    }
    return payload


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    ps = payload.get("primary_summary", {})
    lines = [
        "# EXTERNAL fallback — CB2_APO TM6/toggle (filename inactive vs active)",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `{payload.get('preregistration')}`",
        f"**Run mode:** `{payload.get('run_mode')}`",
        "",
        "## Epistemology",
        "",
        "- Filename `inactive`/`active` = **start-label proxy only** — **≠** MSM macrostate.",
        "- Fallback after `EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE`.",
        "- Does **not** reopen P2 CONVERGENT; no Gi; no fake filelist alignment.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_APO_TM6_TOGGLE']}`**",
        f"- Soft vs PDB state-dependence narrative: `{v.get('SOFT_COMPARE_PRIOR_PDB_B')}`",
        f"- Filename ≠ MSM: `{v['EXT_APO_TM6_FILENAME_NEQ_MSM']}`",
        f"- P2 unchanged: `{v['P2_STATUS_UNCHANGED']}`",
        "",
        "## Mapping",
        "",
        f"- Alignment identity: `{payload['mapping']['alignment_identity']:.4f}`",
        f"- Median topo−UniProt offset: `{payload['mapping'].get('median_offset_topo_minus_uniprot')}`",
        f"- Note: {payload['mapping'].get('note')}",
        "",
        "## Primary toggle summary",
        "",
        f"- |d|≥0.8 among primary 6: **{ps.get('n_abs_d_ge_0_8')}**/6",
        f"- IC opening (active>inactive & |d|≥0.8): **{ps.get('n_ic_opening_sign_and_d')}**/3",
        f"- Frames pooled inactive/active: "
        f"`{payload['n_frames_pooled']['inactive']}` / `{payload['n_frames_pooled']['active']}`",
        "",
        "## Primary features",
        "",
        "| role | UniProt | topo | mean_in | mean_act | Δ | d |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for r in payload["features"]:
        if not r["primary"]:
            continue
        lines.append(
            f"| {r['role']} | {r['uniprot']} | {r['topo']} | "
            f"{r['mean_inactive']:.2f} | {r['mean_active']:.2f} | "
            f"{r['delta_active_minus_inactive']:.2f} | {r['cohens_d']:.2f} |"
        )
    lines += [
        "",
        "## Hub-adjacent distances (descriptive)",
        "",
    ]
    for r in payload.get("hub_adjacent_features", []):
        lines.append(
            f"- `{r['role']}` UniProt={r['uniprot']} d={r['cohens_d']:.2f} "
            f"Δ={r['delta']:.2f} Å"
        )
    lines += [
        "",
        "## PI summary (ES)",
        "",
        payload.get("pi_summary_es", ""),
        "",
        "## Forbidden claims",
        "",
        "- No MSM substitute; no P2 CONVERGENT; no Gi; filename ≠ metastable state.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--mode",
        choices=["sample5", "primary"],
        default="sample5",
        help="sample5 uses _pilot_sample 5+5; primary uses 1+1 pilots",
    )
    ap.add_argument("--frame-cap", type=int, default=FRAME_CAP)
    args = ap.parse_args()

    payload = analyze(args.mode, args.frame_cap)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(f"[cb2_apo_tm6_toggle] wrote {OUT_MD.relative_to(ROOT)}")
    print(f"[cb2_apo_tm6_toggle] {payload['verdicts']['EXT_APO_TM6_TOGGLE']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
