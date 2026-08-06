#!/usr/bin/env python3
"""Hard separation gate for H1–H5 Batch-1 vs THCV / THC (LOCAL + public summary).

Gate (affinity proxy only; NOT functional Janus success):
  dual = mean(CB1_vina, CB2_vina)   # more negative = better occupancy
  pass iff:
    (1) dual_candidate < dual_THCV
    (2) gap_vs_THC = dual_candidate - dual_THC
        and |favorable gap| clearly exceeds THCV–THC separation (~0.20):
        (dual_THC - dual_candidate) > 0.40
        i.e. favorable gap magnitude > 2 × ~0.20 kcal/mol

Writes:
  - results/hits/h1_h5_batch1/gate_detail.md  (gitignored; may include SMILES)
  - results/reports/h1_h5_batch1_gate_summary.md  (public; IDs + scores only)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Hard gate thresholds (documented)
THCV_THC_REF_GAP = 0.20  # kcal/mol magnitude from retrospective (~0.20)
CLEAR_GAP_MIN = 0.40  # clearly > ~0.20 → use 2× as "claro"


def _fmt(x) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    return f"{float(x):.3f}"


def evaluate(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    for col in ("cb1_vina", "cb2_vina"):
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work["dual"] = work[["cb1_vina", "cb2_vina"]].mean(axis=1)

    thcv = work[work["name"] == "delta9-THCV"]
    thc = work[work["name"] == "delta9-THC"]
    if thcv.empty or thc.empty:
        raise ValueError("Scores CSV must include delta9-THCV and delta9-THC references")

    dual_thcv = float(thcv.iloc[0]["dual"])
    dual_thc = float(thc.iloc[0]["dual"])
    thcv_thc_gap = dual_thcv - dual_thc  # negative if THCV better

    rows = []
    for _, r in work.iterrows():
        dual = None if pd.isna(r["dual"]) else float(r["dual"])
        vs_thcv = None if dual is None else dual - dual_thcv
        vs_thc = None if dual is None else dual - dual_thc
        gap_mag_vs_thc = None if dual is None else dual_thc - dual
        better_than_thcv = dual is not None and dual < dual_thcv
        clear_vs_thc = gap_mag_vs_thc is not None and gap_mag_vs_thc > CLEAR_GAP_MIN
        is_cand = str(r.get("role", "")) == "design_candidate"
        passes = bool(is_cand and better_than_thcv and clear_vs_thc)
        rows.append(
            {
                **{k: r.get(k) for k in ("name", "common_name", "role", "smiles")},
                "cb1_vina": None if pd.isna(r["cb1_vina"]) else float(r["cb1_vina"]),
                "cb2_vina": None if pd.isna(r["cb2_vina"]) else float(r["cb2_vina"]),
                "dual": dual,
                "vs_thcv": vs_thcv,
                "vs_thc": vs_thc,
                "gap_mag_vs_thc": gap_mag_vs_thc,
                "better_than_thcv": better_than_thcv,
                "clear_gap_vs_thc": clear_vs_thc,
                "pass_gate": passes,
            }
        )

    out = pd.DataFrame(rows)
    out.attrs["dual_thcv"] = dual_thcv
    out.attrs["dual_thc"] = dual_thc
    out.attrs["thcv_thc_gap"] = thcv_thc_gap
    return out


def write_detail(eval_df: pd.DataFrame, path: Path, scores_path: Path) -> None:
    dual_thcv = eval_df.attrs["dual_thcv"]
    dual_thc = eval_df.attrs["dual_thc"]
    thcv_thc_gap = eval_df.attrs["thcv_thc_gap"]
    n_pass = int(eval_df["pass_gate"].sum())
    n_cand = int((eval_df["role"] == "design_candidate").sum())

    lines = [
        "# H1–H5 Batch 1 — gate detail (LOCAL / gitignored)",
        "",
        "> Contains SMILES. **Do not commit/push this file.**",
        "",
        f"- Scores: `{scores_path.as_posix()}`",
        f"- dual_THCV = {_fmt(dual_thcv)}; dual_THC = {_fmt(dual_thc)}; "
        f"THCV−THC gap = {_fmt(thcv_thc_gap)} kcal/mol",
        f"- Hard gate: dual < THCV **and** (dual_THC − dual) > {CLEAR_GAP_MIN:.2f} "
        f"(clearly > ~{THCV_THC_REF_GAP:.2f})",
        f"- Passed: **{n_pass}/{n_cand}** design candidates",
        "",
        "| ID | hyp/role | SMILES | CB1 | CB2 | dual | vs THCV | vs THC | pass |",
        "|----|----------|--------|-----|-----|------|---------|--------|------|",
    ]
    # Attach hypothesis from full CSV if present beside scores
    for _, r in eval_df.iterrows():
        lines.append(
            f"| {r['name']} | {r['role']} | `{r.get('smiles', '')}` | "
            f"{_fmt(r['cb1_vina'])} | {_fmt(r['cb2_vina'])} | {_fmt(r['dual'])} | "
            f"{_fmt(r['vs_thcv'])} | {_fmt(r['vs_thc'])} | "
            f"{'PASS' if r['pass_gate'] else 'fail'} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_public_summary(eval_df: pd.DataFrame, path: Path, scores_path: Path) -> None:
    dual_thcv = eval_df.attrs["dual_thcv"]
    dual_thc = eval_df.attrs["dual_thc"]
    thcv_thc_gap = eval_df.attrs["thcv_thc_gap"]
    n_pass = int(eval_df["pass_gate"].sum())
    n_cand = int((eval_df["role"] == "design_candidate").sum())

    lines = [
        "# H1–H5 Batch 1 — gate summary (public)",
        "",
        "> **No SMILES.** Structures and pose files stay local/gitignored. "
        "Vina = affinity/pose proxy only — not functional Janus success "
        "(see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).",
        "",
        f"- Fecha: 2026-08-06",
        f"- Panel local: `data/libraries/h1_h5_batch1.csv` (gitignored)",
        f"- Scores: `{scores_path.relative_to(ROOT).as_posix() if scores_path.is_relative_to(ROOT) else scores_path}` (gitignored)",
        f"- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness moderado (8–16)",
        "",
        "## Métrica de gate duro",
        "",
        f"- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)",
        f"- Referencias en el mismo run: dual_THCV = **{_fmt(dual_thcv)}**, "
        f"dual_THC = **{_fmt(dual_thc)}**, gap THCV−THC = **{_fmt(thcv_thc_gap)}** kcal/mol",
        f"- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > {CLEAR_GAP_MIN:.2f}` "
        f"(claramente > separación THCV–THC ≈ {THCV_THC_REF_GAP:.2f})",
        "",
        f"**Resultado agregado:** {n_pass}/{n_cand} candidatos de diseño pasaron el gate.",
        "",
        "## Tabla (IDs + scores)",
        "",
        "| ID | role | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |",
        "|----|------|-----|-----|------|---------|--------|-------------|",
    ]
    for _, r in eval_df.iterrows():
        gate = "—"
        if r["role"] == "design_candidate":
            gate = "PASS" if r["pass_gate"] else "fail"
        elif r["role"] in {"seed", "anti_seed"}:
            gate = "ref"
        lines.append(
            f"| {r['name']} | {r['role']} | {_fmt(r['cb1_vina'])} | {_fmt(r['cb2_vina'])} | "
            f"{_fmt(r['dual'])} | {_fmt(r['vs_thcv'])} | {_fmt(r['vs_thc'])} | {gate} |"
        )

    lines += [
        "",
        "## Veredicto",
        "",
    ]
    if n_pass == 0:
        lines.append(
            "Ningún análogo Batch-1 supera el gate duro de separación proxy frente a THCV/THC. "
            "Coherente con el hallazgo retrospectivo: el scaffold THCV-like no se separa fácilmente "
            "por afinidad Vina sola. Seguir con SAR / función; no declarar hit Janus por score."
        )
    else:
        passed = eval_df[eval_df["pass_gate"]]["name"].tolist()
        lines.append(
            f"Pasaron gate proxy: {', '.join(passed)}. "
            "Sigue siendo **solo** ocupación/afinidad — gates funcionales 1–3 siguen abiertos."
        )

    lines += [
        "",
        "## IP",
        "",
        "- CSV/SDF/PDBQT de candidatos: gitignored (`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).",
        "- Detalle con SMILES (local): `results/hits/h1_h5_batch1/gate_detail.md`.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--scores",
        type=Path,
        default=ROOT / "results/docking/h1_h5_batch1/retrospective_scores.csv",
    )
    ap.add_argument(
        "--detail",
        type=Path,
        default=ROOT / "results/hits/h1_h5_batch1/gate_detail.md",
    )
    ap.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "results/reports/h1_h5_batch1_gate_summary.md",
    )
    ap.add_argument(
        "--stats-json",
        type=Path,
        default=ROOT / "results/hits/h1_h5_batch1/gate_stats.json",
    )
    args = ap.parse_args()

    if not args.scores.exists():
        print(f"BLOQUEO: missing scores {args.scores}")
        return 2

    df = pd.read_csv(args.scores)
    eval_df = evaluate(df)
    write_detail(eval_df, args.detail, args.scores)
    write_public_summary(eval_df, args.summary, args.scores)

    payload = {
        "metric": {
            "dual": "mean(cb1_vina, cb2_vina)",
            "pass_rule": (
                f"dual < dual_THCV AND (dual_THC - dual) > {CLEAR_GAP_MIN} "
                f"(clearly > ~{THCV_THC_REF_GAP} THCV-THC separation)"
            ),
            "dual_thcv": eval_df.attrs["dual_thcv"],
            "dual_thc": eval_df.attrs["dual_thc"],
            "thcv_thc_gap": eval_df.attrs["thcv_thc_gap"],
            "clear_gap_min": CLEAR_GAP_MIN,
        },
        "n_pass": int(eval_df["pass_gate"].sum()),
        "n_candidates": int((eval_df["role"] == "design_candidate").sum()),
        "rows": eval_df.drop(columns=["smiles"], errors="ignore").to_dict(
            orient="records"
        ),
    }
    args.stats_json.parent.mkdir(parents=True, exist_ok=True)
    args.stats_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Detail (gitignored): {args.detail}")
    print(f"Public summary:      {args.summary}")
    print(f"Stats:               {args.stats_json}")
    print(
        f"Gate: {payload['n_pass']}/{payload['n_candidates']} design candidates PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
