#!/usr/bin/env python3
"""EXTERNAL — ESMDynamic soft proxy on human CB2 (P34972).

Pre-registration: docs/synthesis/EXPERIMENT_CB2_ESMDYNAMIC.md

This runner records availability / blockers and, if maps are present, scores
LigACN-hub overlap. It does NOT reopen P2, claim Gi mechanism, or substitute
MSM-state contact probabilities.

Outputs:
  results/network_core/cb2_esmdynamic.{md,json}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from dynamic_pipeline import HUBS, HUB_LABELS  # noqa: E402

OUT_DIR = ROOT / "results" / "network_core"
OUT_JSON = OUT_DIR / "cb2_esmdynamic.json"
OUT_MD = OUT_DIR / "cb2_esmdynamic.md"
PREREG = ROOT / "docs" / "synthesis" / "EXPERIMENT_CB2_ESMDYNAMIC.md"
CACHE = ROOT / "data" / "external" / "_tmp_esmdynamic"
PROTEOME_TABLE = CACHE / "proteome_table"

UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

PROTEIN_ID = "sp_P34972_CNR2_HUMAN"
PROTEOME_ARCHIVE = "human_proteome_preds_04.tar.xz"
PAPER_DOI = "10.1038/s41467-026-76361-2"
CODE_URL = "https://github.com/ShuklaGroup/esmdynamic"
WEIGHTS_DOI = "10.13012/B2IDB-3773897_V2"

THR_D = 0.5
THR_D_STRICT = 0.7
THR_F = 0.7
MIN_SEP = 6
N_NULL = 200
SEED = 20260912
TEMP_K = 320

HUB_UP = {int(h["label"].split(":")[1]) for h in HUBS}


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


def probe_environment() -> dict[str, Any]:
    """Early availability gate — document blockers without downloading weights."""
    blockers: list[str] = []
    notes: list[str] = []

    docker = shutil.which("docker")
    docker_ok = False
    docker_err = None
    if docker:
        try:
            subprocess.check_output(
                ["docker", "info"],
                stderr=subprocess.STDOUT,
                text=True,
                timeout=20,
            )
            docker_ok = True
        except Exception as e:
            docker_err = str(e)[:300]
            blockers.append("docker_daemon_unavailable")
    else:
        blockers.append("docker_binary_missing")
        docker_err = "docker not on PATH"

    torch_ok = False
    cuda_ok = False
    torch_ver = None
    try:
        import torch  # type: ignore

        torch_ok = True
        torch_ver = str(torch.__version__)
        cuda_ok = bool(torch.cuda.is_available())
    except Exception:
        blockers.append("torch_not_installed_in_runner_env")

    esm_ok = False
    try:
        import esm  # type: ignore  # noqa: F401

        esm_ok = True
    except Exception:
        blockers.append("esmdynamic_package_not_installed")

    gpu_name = None
    vram_mb = None
    try:
        smi = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total",
                "--format=csv,noheader,nounits",
            ],
            text=True,
            timeout=15,
        ).strip()
        if smi:
            parts = [p.strip() for p in smi.splitlines()[0].split(",")]
            gpu_name = parts[0]
            vram_mb = float(parts[1]) if len(parts) > 1 else None
            if vram_mb is not None and vram_mb < 10000:
                notes.append(
                    f"gpu_vram_{vram_mb:.0f}MB_below_comfortable_ESMFold_margin"
                )
                blockers.append("gpu_vram_likely_insufficient_for_esmdynamic")
    except Exception as e:
        notes.append(f"nvidia_smi_failed:{str(e)[:120]}")

    proteome_row = None
    if PROTEOME_TABLE.is_file():
        for line in PROTEOME_TABLE.read_text(encoding="utf-8", errors="replace").splitlines():
            if PROTEIN_ID in line:
                proteome_row = line.strip()
                break
        notes.append("proteome_table_lists_CNR2_in_preds_04_shard")
        notes.append(
            "human_proteome_preds_04.tar.xz_is_multi_GB_full_shard_not_fetched_this_session"
        )
        blockers.append("proteome_shard_too_large_to_fetch_for_single_protein")
    else:
        notes.append("proteome_table_missing_local_copy")

    # Prefer real inference only if stack is ready; otherwise UNAVAILABLE.
    runnable = bool(esm_ok and torch_ok and (docker_ok or cuda_ok))
    if not runnable and "esmdynamic_inference_stack_incomplete" not in blockers:
        blockers.append("esmdynamic_inference_stack_incomplete")

    return {
        "docker_present": bool(docker),
        "docker_daemon_ok": docker_ok,
        "docker_error": docker_err,
        "torch_ok": torch_ok,
        "torch_version": torch_ver,
        "cuda_ok": cuda_ok,
        "esm_package_ok": esm_ok,
        "gpu_name": gpu_name,
        "vram_mb": vram_mb,
        "proteome_id": PROTEIN_ID,
        "proteome_archive": PROTEOME_ARCHIVE,
        "proteome_table_row": proteome_row,
        "proteome_table_sha256": sha256_file(PROTEOME_TABLE)
        if PROTEOME_TABLE.is_file()
        else None,
        "runnable_inference": runnable,
        "blockers": blockers,
        "notes": notes,
        "paper_doi": PAPER_DOI,
        "code_url": CODE_URL,
        "weights_doi": WEIGHTS_DOI,
        "sequence_len": len(UNIPROT_P34972),
        "sequence_sha256": hashlib.sha256(UNIPROT_P34972.encode()).hexdigest(),
    }


def load_dynamic_map(path: Path) -> np.ndarray:
    arr = np.loadtxt(path)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"expected square map, got {arr.shape} from {path}")
    return arr.astype(np.float64)


def score_maps(
    dyn: np.ndarray, freq: np.ndarray | None
) -> dict[str, Any]:
    n = dyn.shape[0]
    if n != len(UNIPROT_P34972):
        return {
            "status": "SEQ_MISMATCH",
            "map_len": n,
            "uniprot_len": len(UNIPROT_P34972),
        }

    edges: list[tuple[int, int, float, float | None]] = []
    for i in range(n):
        for j in range(i + MIN_SEP, n):
            d = float(dyn[i, j])
            f = float(freq[i, j]) if freq is not None else None
            if d >= THR_D:
                edges.append((i + 1, j + 1, d, f))

    e_dyn = {(a, b) for a, b, _, _ in edges}
    e_switch = {
        (a, b)
        for a, b, d, f in edges
        if f is not None and f <= THR_F and d >= THR_D
    }

    def hub_touching(edge_set: set[tuple[int, int]]) -> set[tuple[int, int]]:
        return {e for e in edge_set if e[0] in HUB_UP or e[1] in HUB_UP}

    ht = hub_touching(e_dyn)
    hub_edge_frac = (len(ht) / len(e_dyn)) if e_dyn else 0.0
    degrees = {
        h["label"]: sum(
            1 for a, b in e_dyn if a == int(h["label"].split(":")[1]) or b == int(h["label"].split(":")[1])
        )
        for h in HUBS
    }
    n_hubs_touch = sum(1 for v in degrees.values() if v >= 1)

    rng = np.random.default_rng(SEED)
    null_fracs = []
    residues = np.arange(1, n + 1)
    for _ in range(N_NULL):
        fake = set(int(x) for x in rng.choice(residues, size=6, replace=False))
        frac = (
            sum(1 for a, b in e_dyn if a in fake or b in fake) / len(e_dyn)
            if e_dyn
            else 0.0
        )
        null_fracs.append(frac)
    null_fracs_a = np.asarray(null_fracs, dtype=np.float64)
    p_emp = float(np.mean(null_fracs_a >= hub_edge_frac)) if e_dyn else 1.0

    if not e_dyn:
        primary = "EXT_ESMDYNAMIC_INDETERMINATE"
    elif p_emp <= 0.05 and n_hubs_touch >= 4:
        primary = "EXT_ESMDYNAMIC_HUB_ENRICHED"
    elif p_emp > 0.05 or n_hubs_touch < 4:
        primary = "EXT_ESMDYNAMIC_HUB_NOT_ENRICHED"
    else:
        primary = "EXT_ESMDYNAMIC_INDETERMINATE"

    if primary == "EXT_ESMDYNAMIC_HUB_ENRICHED":
        soft = "EXT_ESMDYNAMIC_SOFT_COMPAT_PDB_B"
    elif primary == "EXT_ESMDYNAMIC_HUB_NOT_ENRICHED":
        soft = "EXT_ESMDYNAMIC_SOFT_COMPAT_PILOT_INDET"
    else:
        soft = "EXT_ESMDYNAMIC_SOFT_COMPARE_NA"

    return {
        "status": "OK",
        "n_edges_dyn": len(e_dyn),
        "n_edges_switch": len(e_switch),
        "hub_edge_frac_dyn": hub_edge_frac,
        "hub_degrees_dyn": degrees,
        "n_hubs_touching": n_hubs_touch,
        "null_mean_frac": float(null_fracs_a.mean()),
        "null_p_emp_upper": p_emp,
        "verdict_primary": primary,
        "verdict_soft": soft,
        "thresholds": {
            "tau_d": THR_D,
            "tau_d_strict": THR_D_STRICT,
            "tau_f": THR_F,
            "min_sep": MIN_SEP,
            "temp_K": TEMP_K,
        },
    }


def find_local_maps() -> dict[str, Path | None]:
    """Optional: user-dropped dynamic/frequency txt maps under CACHE."""
    dyn = None
    freq = None
    candidates = list(CACHE.rglob(f"*dynamic_prob*{TEMP_K}K*")) + list(
        CACHE.rglob("*dynamic_prob*.txt")
    )
    for p in candidates:
        if p.is_file() and p.suffix in {".txt", ".csv"}:
            dyn = p
            break
    for p in list(CACHE.rglob(f"*frequency_pred*{TEMP_K}K*")) + list(
        CACHE.rglob("*frequency_pred*.txt")
    ):
        if p.is_file():
            freq = p
            break
    return {"dynamic_prob": dyn, "frequency_pred": freq}


def build_unavailable(env: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "branch": git_branch(),
        "experiment": "EXTERNAL_ESMDYNAMIC",
        "preregistration": str(PREREG.relative_to(ROOT)),
        "epistemology": {
            "not_msm_state_contacts": True,
            "does_not_reopen_P2_CONVERGENT": True,
            "no_Gi_claim": True,
            "no_experimental_validation_on_CB2": True,
            "verdicts_provisional_soft": True,
        },
        "input": {
            "uniprot": "P34972",
            "protein_id_proteome": PROTEIN_ID,
            "sequence_len": len(UNIPROT_P34972),
            "hubs": HUBS,
        },
        "environment": env,
        "maps": None,
        "metrics": None,
        "verdicts": {
            "EXT_ESMDYNAMIC": "EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE",
            "EXT_ESMDYNAMIC_SOFT_COMPARE": "EXT_ESMDYNAMIC_SOFT_COMPARE_NA",
            "P2_STATUS_UNCHANGED": "CLOSED_INSUFFICIENT_SAMPLING",
            "EXT_MSM_FILELIST": "NOT_FABRICATED",
            "FALLBACK": "EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME",
        },
        "fallback_proposed": {
            "name": "EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME",
            "script": "scripts/network_core/cb2_apo_tm6_toggle.py",
            "note": "filename inactive/active start-label proxy; not MSM states",
        },
        "pi_summary_es": (
            "ESMDynamic no se pudo ejecutar en esta sesión "
            "(Docker daemon caído, sin torch/esmdynamic en el env, VRAM GTX 1060 "
            "6 GB insuficiente con margen, y el shard proteoma CNR2 ~multi-GB). "
            "Veredicto: EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE. "
            "No sustituye contactos MSM; no reabre P2. "
            "Se ejecuta el fallback TM6/toggle sobre CB2_APO local."
        ),
    }


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    env = payload["environment"]
    lines = [
        "# EXTERNAL — ESMDynamic soft proxy (human CB2 / P34972)",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `{payload['preregistration']}`",
        "",
        "## Epistemology",
        "",
        "- AI/sequence proxy only — **not** MSM-state contact probabilities.",
        "- Does **not** reopen P2 as CONVERGENT; no Gi claim.",
        "- No experimental validation of ESMDynamic on CB2 in this lab.",
        "- Verdicts `EXT_ESMDYNAMIC_*` are provisional/soft.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_ESMDYNAMIC']}`**",
        f"- Soft compare: `{v['EXT_ESMDYNAMIC_SOFT_COMPARE']}`",
        f"- P2 unchanged: `{v['P2_STATUS_UNCHANGED']}`",
        f"- Filelist fabrication: `{v['EXT_MSM_FILELIST']}`",
        f"- Fallback: `{v.get('FALLBACK')}`",
        "",
        "## Software / data pointers",
        "",
        f"- Paper DOI: `{env['paper_doi']}`",
        f"- Code: {env['code_url']}",
        f"- Weights / proteome DOI: `{env['weights_doi']}`",
        f"- Proteome ID: `{env['proteome_id']}` → archive `{env['proteome_archive']}`",
        "",
        "## Environment blockers",
        "",
    ]
    for b in env.get("blockers", []):
        lines.append(f"- `{b}`")
    lines += ["", "### Notes", ""]
    for n in env.get("notes", []):
        lines.append(f"- {n}")
    lines += [
        "",
        f"- docker_daemon_ok=`{env.get('docker_daemon_ok')}`",
        f"- torch_ok=`{env.get('torch_ok')}` cuda_ok=`{env.get('cuda_ok')}` "
        f"esm_ok=`{env.get('esm_package_ok')}`",
        f"- GPU=`{env.get('gpu_name')}` VRAM_MB=`{env.get('vram_mb')}`",
        "",
        "## PI summary (ES)",
        "",
        payload.get("pi_summary_es", ""),
        "",
        "## Forbidden claims (reminder)",
        "",
        "- No MSM substitute; no P2 CONVERGENT; no Gi; no fake filelist alignment.",
        "",
    ]
    if payload.get("metrics"):
        m = payload["metrics"]
        lines += [
            "## Metrics (if maps present)",
            "",
            f"- status=`{m.get('status')}` n_edges_dyn=`{m.get('n_edges_dyn')}` "
            f"hub_frac=`{m.get('hub_edge_frac_dyn')}` p_emp=`{m.get('null_p_emp_upper')}`",
            "",
        ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maps-dir",
        type=Path,
        default=None,
        help="Optional directory with dynamic_prob/frequency_pred txt maps",
    )
    args = parser.parse_args()

    if not PREREG.is_file():
        raise SystemExit(f"Pre-registration missing: {PREREG}")

    env = probe_environment()
    local = find_local_maps()
    if args.maps_dir:
        CACHE.mkdir(parents=True, exist_ok=True)
        # allow explicit dir override via env scan of that path
        os.environ.setdefault("ESMDYNAMIC_MAPS", str(args.maps_dir))
        for p in args.maps_dir.rglob("*"):
            if "dynamic_prob" in p.name and p.suffix == ".txt" and local["dynamic_prob"] is None:
                local["dynamic_prob"] = p
            if "frequency_pred" in p.name and p.suffix == ".txt" and local["frequency_pred"] is None:
                local["frequency_pred"] = p

    if local["dynamic_prob"] is not None and env.get("runnable_inference"):
        # Prefer scoring real maps if somehow present AND stack ok — still soft.
        dyn = load_dynamic_map(local["dynamic_prob"])
        freq = (
            load_dynamic_map(local["frequency_pred"])
            if local["frequency_pred"] is not None
            else None
        )
        metrics = score_maps(dyn, freq)
        payload = build_unavailable(env)
        payload["maps"] = {
            "dynamic_prob": str(local["dynamic_prob"]),
            "frequency_pred": str(local["frequency_pred"])
            if local["frequency_pred"]
            else None,
        }
        payload["metrics"] = metrics
        payload["verdicts"]["EXT_ESMDYNAMIC"] = metrics.get(
            "verdict_primary", "EXT_ESMDYNAMIC_INDETERMINATE"
        )
        payload["verdicts"]["EXT_ESMDYNAMIC_SOFT_COMPARE"] = metrics.get(
            "verdict_soft", "EXT_ESMDYNAMIC_SOFT_COMPARE_NA"
        )
        payload["pi_summary_es"] = (
            "Mapas ESMDynamic locales puntuados (soft). "
            f"Veredicto: {payload['verdicts']['EXT_ESMDYNAMIC']}."
        )
    elif local["dynamic_prob"] is not None and not env.get("runnable_inference"):
        # Maps dropped without runnable stack — still score (published maps path).
        dyn = load_dynamic_map(local["dynamic_prob"])
        freq = (
            load_dynamic_map(local["frequency_pred"])
            if local["frequency_pred"] is not None
            else None
        )
        metrics = score_maps(dyn, freq)
        payload = build_unavailable(env)
        payload["environment"]["notes"].append("scored_user_supplied_maps_without_local_inference")
        payload["maps"] = {
            "dynamic_prob": str(local["dynamic_prob"]),
            "frequency_pred": str(local["frequency_pred"])
            if local["frequency_pred"]
            else None,
            "source": "user_supplied_or_cache",
        }
        payload["metrics"] = metrics
        if metrics.get("status") == "OK":
            payload["verdicts"]["EXT_ESMDYNAMIC"] = metrics["verdict_primary"]
            payload["verdicts"]["EXT_ESMDYNAMIC_SOFT_COMPARE"] = metrics["verdict_soft"]
            payload["verdicts"].pop("FALLBACK", None)
            payload["pi_summary_es"] = (
                "Se puntuaron mapas ESMDynamic ya disponibles en caché local "
                f"(sin inferencia). Veredicto: {metrics['verdict_primary']}."
            )
        else:
            payload["verdicts"]["EXT_ESMDYNAMIC"] = (
                "EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE"
            )
    else:
        payload = build_unavailable(env)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    print(f"[cb2_esmdynamic] wrote {OUT_MD.relative_to(ROOT)}")
    print(f"[cb2_esmdynamic] {payload['verdicts']['EXT_ESMDYNAMIC']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
