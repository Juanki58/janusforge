#!/usr/bin/env python3
"""Rank panel scores and test seed vs anti_seed separation (affinity proxy only)."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FOCUS_ROLES_JANUS = {"seed", "design_comparator"}
ANTI_ROLES = {"anti_seed"}


def _fmt(x) -> str:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "—"
    return f"{float(x):.3f}"


def _mean(vals: list[float]) -> float | None:
    return statistics.mean(vals) if vals else None


def _median(vals: list[float]) -> float | None:
    return statistics.median(vals) if vals else None


def analyze(df: pd.DataFrame) -> dict:
    work = df.copy()
    for col in ("cb1_vina", "cb2_vina"):
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work["dual_mean"] = work[["cb1_vina", "cb2_vina"]].mean(axis=1)

    ranked_cb1 = work.sort_values("cb1_vina", ascending=True, na_position="last")
    ranked_cb2 = work.sort_values("cb2_vina", ascending=True, na_position="last")
    ranked_dual = work.sort_values("dual_mean", ascending=True, na_position="last")

    janus = work[work["role"].isin(FOCUS_ROLES_JANUS)]
    anti = work[work["role"].isin(ANTI_ROLES)]
    controls = work[work["role"].isin({"control", "secondary", "interesting"})]

    def group_stats(g: pd.DataFrame) -> dict:
        return {
            "n": int(len(g)),
            "names": [str(x) for x in g["name"].tolist()],
            "cb1_mean": _mean([float(x) for x in g["cb1_vina"].dropna()]),
            "cb2_mean": _mean([float(x) for x in g["cb2_vina"].dropna()]),
            "dual_mean": _mean([float(x) for x in g["dual_mean"].dropna()]),
            "cb1_median": _median([float(x) for x in g["cb1_vina"].dropna()]),
            "cb2_median": _median([float(x) for x in g["cb2_vina"].dropna()]),
            "dual_median": _median([float(x) for x in g["dual_mean"].dropna()]),
        }

    stats = {
        "janus_focus": group_stats(janus),
        "anti_seed": group_stats(anti),
        "other": group_stats(controls),
    }

    # Separation: more negative dual_mean for Janus focus vs anti_seed
    j_dual = stats["janus_focus"]["dual_mean"]
    a_dual = stats["anti_seed"]["dual_mean"]
    j_cb1 = stats["janus_focus"]["cb1_mean"]
    a_cb1 = stats["anti_seed"]["cb1_mean"]
    j_cb2 = stats["janus_focus"]["cb2_mean"]
    a_cb2 = stats["anti_seed"]["cb2_mean"]

    gap_dual = None if j_dual is None or a_dual is None else j_dual - a_dual
    # Favorable separation if Janus focus docks *better* (more negative) than anti-seeds
    favorable_dual = gap_dual is not None and gap_dual < -0.25
    # Anti-seeds better (or roughly tied): expected for affinity-only on orthosteric pocket
    anti_better_or_tie = gap_dual is not None and gap_dual >= -0.25

    # Per-compound spotlight
    def pick(name_substr: str) -> dict | None:
        m = work[work["name"].str.contains(name_substr, case=False, na=False)]
        if m.empty:
            m = work[work["common_name"].astype(str).str.contains(name_substr, case=False, na=False)]
        if m.empty:
            return None
        r = m.iloc[0]
        return {
            "name": str(r["name"]),
            "common_name": str(r.get("common_name", "")),
            "role": str(r["role"]),
            "cb1_vina": None if pd.isna(r["cb1_vina"]) else float(r["cb1_vina"]),
            "cb2_vina": None if pd.isna(r["cb2_vina"]) else float(r["cb2_vina"]),
            "dual_mean": None if pd.isna(r["dual_mean"]) else float(r["dual_mean"]),
        }

    spotlight = {
        "THCV": pick("THCV") or pick("delta9-THCV"),
        "URB447": pick("URB447"),
        "THC": pick("delta9-THC") if work["name"].str.contains("delta9-THC").any() else pick("THC"),
        "THCP": pick("THCP"),
    }
    # Fix THC pick: exact anti_seed THC not THCV/THCP
    thc_rows = work[(work["role"] == "anti_seed") & (work["common_name"] == "THC")]
    if not thc_rows.empty:
        r = thc_rows.iloc[0]
        spotlight["THC"] = {
            "name": str(r["name"]),
            "common_name": str(r["common_name"]),
            "role": str(r["role"]),
            "cb1_vina": None if pd.isna(r["cb1_vina"]) else float(r["cb1_vina"]),
            "cb2_vina": None if pd.isna(r["cb2_vina"]) else float(r["cb2_vina"]),
            "dual_mean": None if pd.isna(r["dual_mean"]) else float(r["dual_mean"]),
        }

    thcv = spotlight.get("THCV") or {}
    thc = spotlight.get("THC") or {}
    thcv_vs_thc = None
    if thcv.get("dual_mean") is not None and thc.get("dual_mean") is not None:
        thcv_vs_thc = float(thcv["dual_mean"]) - float(thc["dual_mean"])

    nuance = ""
    if favorable_dual and thcv_vs_thc is not None and thcv_vs_thc > -0.25:
        nuance = (
            " Matiz: el gap grupal lo empuja sobre todo URB447; "
            f"THCV vs THC en dual es solo {_fmt(thcv_vs_thc)} kcal/mol "
            "(poca separación scaffold-scaffold)."
        )

    verdict = {
        "gap_dual_janus_minus_anti": gap_dual,
        "gap_cb1": None if j_cb1 is None or a_cb1 is None else j_cb1 - a_cb1,
        "gap_cb2": None if j_cb2 is None or a_cb2 is None else j_cb2 - a_cb2,
        "gap_thcv_minus_thc_dual": thcv_vs_thc,
        "favorable_affinity_separation": favorable_dual,
        "anti_better_or_tie": anti_better_or_tie,
        "interpretation": (
            (
                "URB447/THCV muestran afinidad proxy dual media más favorable "
                "(más negativa) que las anti-semillas (Δ≥0.25 kcal/mol)."
                + nuance
            )
            if favorable_dual
            else "No hay separación favorable clara por afinidad Vina: "
            "anti-semillas (THC/THCP) empatan o superan a THCV/URB447 en el "
            "proxy dual. Esperable: docking mide ocupación/afinidad de pose, "
            "no agonismo vs antagonismo ni el flip CB1."
        ),
    }

    return {
        "stats": stats,
        "verdict": verdict,
        "spotlight": spotlight,
        "ranked_cb1": ranked_cb1,
        "ranked_cb2": ranked_cb2,
        "ranked_dual": ranked_dual,
        "table": work.sort_values("dual_mean", ascending=True, na_position="last"),
    }


def write_report(analysis: dict, cfg: dict, scores_path: Path, report_path: Path) -> None:
    dock = cfg.get("docking", {})
    t = analysis["table"]
    v = analysis["verdict"]
    st = analysis["stats"]
    spot = analysis["spotlight"]

    lines = [
        "# Validación retrospectiva — panel quimioma (11 compuestos)",
        "",
        "> **Aviso científico:** AutoDock Vina reporta un **proxy de afinidad/pose** "
        "(kcal/mol; más negativo ≈ mejor ocupación del pocket). "
        "**No** demuestra agonismo vs antagonismo, ni el flip CB1 de THCV, ni "
        "eficacia antifibrótica. Ver [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md) "
        "(anti-criterio: score alto sin coherencia funcional).",
        "",
        f"- Fecha análisis: 2026-08-06",
        f"- Scores: `{scores_path.relative_to(ROOT).as_posix() if scores_path.is_relative_to(ROOT) else scores_path.as_posix()}`",
        f"- Receptores: CB1 **{cfg['targets']['cb1']['pdb']}** (estado antagonista/inactivo); "
        f"CB2 **{cfg['targets']['cb2']['pdb']}** (agonista/activo)",
        f"- Exhaustiveness: **{dock.get('exhaustiveness', 8)}**; seed: **{dock.get('seed', 42)}**; "
        f"pH ligandos: **{dock.get('ph', 7.4)}**",
        "- Cajas: centro = centroide del ligando co-cristalizado (ver `data/targets/*/box.json`)",
        "- Protonación: fenoles neutros; dimorphite-dl solo para ácidos carboxílicos (THCVA)",
        "",
        "## Tabla de scores",
        "",
        "| Compuesto | role | CB1 Vina | CB2 Vina | Dual mean |",
        "|-----------|------|----------|----------|-----------|",
    ]
    for _, r in t.iterrows():
        lines.append(
            f"| {r.get('common_name', r['name'])} ({r['name']}) | {r['role']} | "
            f"{_fmt(r['cb1_vina'])} | {_fmt(r['cb2_vina'])} | {_fmt(r['dual_mean'])} |"
        )

    lines += [
        "",
        "## Foco: semillas Janus vs anti-semillas",
        "",
        "| Grupo | n | CB1 mean | CB2 mean | Dual mean |",
        "|-------|---|----------|----------|-----------|",
        f"| seed + design_comparator | {st['janus_focus']['n']} | "
        f"{_fmt(st['janus_focus']['cb1_mean'])} | {_fmt(st['janus_focus']['cb2_mean'])} | "
        f"{_fmt(st['janus_focus']['dual_mean'])} |",
        f"| anti_seed | {st['anti_seed']['n']} | "
        f"{_fmt(st['anti_seed']['cb1_mean'])} | {_fmt(st['anti_seed']['cb2_mean'])} | "
        f"{_fmt(st['anti_seed']['dual_mean'])} |",
        "",
        "### Spotlight",
        "",
        "| Ligando | role | CB1 | CB2 | Dual |",
        "|---------|------|-----|-----|------|",
    ]
    for key in ("THCV", "URB447", "THC", "THCP"):
        s = spot.get(key)
        if not s:
            lines.append(f"| {key} | — | — | — | — |")
            continue
        lines.append(
            f"| {s['common_name'] or s['name']} | {s['role']} | "
            f"{_fmt(s['cb1_vina'])} | {_fmt(s['cb2_vina'])} | {_fmt(s['dual_mean'])} |"
        )

    sep = "SÍ (favorable por afinidad proxy)" if v["favorable_affinity_separation"] else "NO"
    lines += [
        "",
        "## ¿Hay separación según el criterio operativo?",
        "",
        f"- **Separación favorable seed/URB447 vs anti-semillas (dual mean):** {sep}",
        f"- Gap dual (Janus − anti): `{_fmt(v['gap_dual_janus_minus_anti'])}` kcal/mol "
        "(negativo = Janus mejor afinidad proxy)",
        f"- Gap CB1: `{_fmt(v['gap_cb1'])}`; gap CB2: `{_fmt(v['gap_cb2'])}`",
        "",
        f"**Lectura:** {v['interpretation']}",
        "",
        "### Relación con `criterio_exito_janus.md`",
        "",
        "- Gates 1–3 (flip CB1, CB2 ago, anti-semilla) son **funcionales / SAR**, no de Vina.",
        "- Este panel solo pregunta si el **mapa de roles del CSV** se refleja en rankings "
        "de afinidad proxy en bolsillos antagonista (CB1) y agonista (CB2).",
        "- Un score Vina fuerte de THC/THCP **no** las convierte en hits Janus "
        "(anti-criterio explícito del documento de éxito).",
        "",
        "## Ranking dual (mejor → peor afinidad proxy)",
        "",
    ]
    for i, (_, r) in enumerate(analysis["ranked_dual"].iterrows(), 1):
        lines.append(
            f"{i}. **{r.get('common_name', r['name'])}** (`{r['role']}`) "
            f"dual={_fmt(r['dual_mean'])} (CB1={_fmt(r['cb1_vina'])}, CB2={_fmt(r['cb2_vina'])})"
        )

    lines += [
        "",
        "## Archivos",
        "",
        "- Ligandos: `data/processed/panel_ligands/`",
        "- Receptores / boxes: `data/targets/cb1/`, `data/targets/cb2/`",
        "- Poses: `results/docking/retrospective_panel/`",
        "- Stats JSON: `results/hits/retrospective_panel_stats.json`",
        "",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=ROOT / "configs/cb1_cb2.yaml")
    ap.add_argument(
        "--scores",
        type=Path,
        default=ROOT / "results/docking/retrospective_panel/retrospective_scores.csv",
    )
    ap.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results/reports/retrospective_panel_separation.md",
    )
    ap.add_argument(
        "--stats-json",
        type=Path,
        default=ROOT / "results/hits/retrospective_panel_stats.json",
    )
    args = ap.parse_args()

    if not args.scores.exists():
        print(f"BLOQUEO: no hay scores en {args.scores}. Ejecuta run_retrospective_dock.py")
        return 2

    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    df = pd.read_csv(args.scores)
    analysis = analyze(df)
    write_report(analysis, cfg, args.scores, args.report)

    payload = {
        "stats": analysis["stats"],
        "verdict": analysis["verdict"],
        "spotlight": analysis["spotlight"],
        "rows": analysis["table"].to_dict(orient="records"),
    }
    args.stats_json.parent.mkdir(parents=True, exist_ok=True)
    args.stats_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Report: {args.report}")
    print(f"Stats: {args.stats_json}")
    print("Verdict:", analysis["verdict"]["interpretation"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
