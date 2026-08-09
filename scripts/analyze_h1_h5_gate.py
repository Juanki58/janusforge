#!/usr/bin/env python3
"""Hard separation gate for H1–H5 design batches vs THCV / THC.

Gate (affinity proxy only; NOT functional Janus success):
  dual = mean(CB1_vina, CB2_vina)   # more negative = better occupancy
  pass iff:
    (1) dual_candidate < dual_THCV
    (2) (dual_THC - dual_candidate) > 0.40

Writes:
  - results/hits/h1_h5_batchN/gate_detail.md  (gitignored; may include SMILES)
  - results/reports/h1_h5_batchN_gate_summary.md  (public; IDs + scores only)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

THCV_THC_REF_GAP = 0.20
CLEAR_GAP_MIN = 0.40

BATCH_LABELS = {
    "h1_h5_batch1": "Iteración 1 — librería de diseño (H1–H5)",
    "h1_h5_batch2": "Iteración 2 — H1×H2 híbridos + volumen 1′",
    "h1_h5_batch3": "Iteración 3 — refino JANUS_H1_02 (1′-Me)",
    "option_d_batch1": "Opción D — panel sintético URB447 / Yin-Yang (Batch 1)",
    "option_d_batch2": "Opción D — SAR URB447 (Batch 2, fase ligera)",
}
ASPIRATION_GAP_VS_THC = 0.80

# Roles evaluated by the hard separation gate (not refs)
GATE_EVAL_ROLES = frozenset(
    {
        "design_candidate",
        "design_comparator",
        "yin_yang_published",
        "ex_lead_phytocannabinoid",
    }
)


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
    thcv_thc_gap = dual_thcv - dual_thc

    rows = []
    for _, r in work.iterrows():
        dual = None if pd.isna(r["dual"]) else float(r["dual"])
        vs_thcv = None if dual is None else dual - dual_thcv
        vs_thc = None if dual is None else dual - dual_thc
        gap_mag_vs_thc = None if dual is None else dual_thc - dual
        better_than_thcv = dual is not None and dual < dual_thcv
        clear_vs_thc = gap_mag_vs_thc is not None and gap_mag_vs_thc > CLEAR_GAP_MIN
        is_cand = str(r.get("role", "")) in GATE_EVAL_ROLES
        passes = bool(is_cand and better_than_thcv and clear_vs_thc)
        rows.append(
            {
                **{
                    k: r.get(k)
                    for k in ("name", "common_name", "role", "smiles", "hypothesis")
                },
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


def _hyp_label(r: pd.Series) -> str:
    h = r.get("hypothesis")
    if h is not None and str(h) not in {"", "nan", "None"}:
        return str(h)
    return str(r.get("role", ""))


def write_detail(
    eval_df: pd.DataFrame, path: Path, scores_path: Path, batch: str
) -> None:
    dual_thcv = eval_df.attrs["dual_thcv"]
    dual_thc = eval_df.attrs["dual_thc"]
    thcv_thc_gap = eval_df.attrs["thcv_thc_gap"]
    n_pass = int(eval_df["pass_gate"].sum())
    n_cand = int(eval_df["role"].isin(GATE_EVAL_ROLES).sum())
    label = BATCH_LABELS.get(batch, batch)

    lines = [
        f"# {label} — gate detail (LOCAL / gitignored)",
        "",
        "> Contains SMILES. **Do not commit/push this file.**",
        "",
        f"- Scores: `{scores_path.as_posix()}`",
        f"- dual_THCV = {_fmt(dual_thcv)}; dual_THC = {_fmt(dual_thc)}; "
        f"THCV−THC gap = {_fmt(thcv_thc_gap)} kcal/mol",
        f"- Hard gate: dual < THCV **and** (dual_THC − dual) > {CLEAR_GAP_MIN:.2f} "
        f"(clearly > ~{THCV_THC_REF_GAP:.2f})",
        f"- Passed: **{n_pass}/{n_cand}** evaluated ligands",
        "",
        "| ID | hyp/role | SMILES | CB1 | CB2 | dual | vs THCV | vs THC | pass |",
        "|----|----------|--------|-----|-----|------|---------|--------|------|",
    ]
    for _, r in eval_df.iterrows():
        lines.append(
            f"| {r['name']} | {_hyp_label(r)} | `{r.get('smiles', '')}` | "
            f"{_fmt(r['cb1_vina'])} | {_fmt(r['cb2_vina'])} | {_fmt(r['dual'])} | "
            f"{_fmt(r['vs_thcv'])} | {_fmt(r['vs_thc'])} | "
            f"{'PASS' if r['pass_gate'] else 'fail'} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _option_d_verdict(eval_df: pd.DataFrame, n_pass: int, n_cand: int) -> str:
    """Critical reading: do published synthetics beat phytocannabinoid Track1 lead?"""
    by = {r["name"]: r for _, r in eval_df.iterrows()}
    passed = eval_df[eval_df["pass_gate"]]["name"].tolist()
    synth = [
        n
        for n in ("URB447", "AM1710", "GW405833")
        if n in by and str(by[n]["role"]) in GATE_EVAL_ROLES
    ]
    synth_pass = [n for n in synth if n in passed]
    ex = by.get("JANUS_H1_02c")
    parts = [
        f"**Resultado:** {n_pass}/{n_cand} PASS"
        + (f" ({', '.join(passed)})." if passed else "."),
        f"Sintéticos publicados evaluados: {', '.join(synth) or 'ninguno'}; "
        f"PASS: {', '.join(synth_pass) or 'ninguno'}.",
    ]
    if ex is not None and ex["dual"] is not None:
        parts.append(
            f"**Ex-lead fitocannabinoide H1_02c:** dual={_fmt(ex['dual'])}, "
            f"gap vs THC={_fmt(ex.get('gap_mag_vs_thc'))} "
            f"({'PASS' if ex['pass_gate'] else 'fail'} en este run) — "
            "contexto post NO-GO MD membrana; no reabre Track 1 como eje."
        )
    urb = by.get("URB447")
    if urb is not None and urb["dual"] is not None:
        parts.append(
            f"**URB447 (semilla sintética Track D):** dual={_fmt(urb['dual'])}, "
            f"gap vs THC={_fmt(urb.get('gap_mag_vs_thc'))} "
            f"({'PASS' if urb['pass_gate'] else 'fail'})."
        )
    parts.append(
        "Umbrales = mismos que H1–H5 (dual < THCV y gap vs THC > 0.40). "
        "Vina = afinidad/pose proxy; **no** éxito Janus funcional. "
        "Qiu 2023 citado en docs, sin SMILES en panel (estructura no en PubChem fiable)."
    )
    return " ".join(parts)


def _option_d_batch2_verdict(eval_df: pd.DataFrame, n_pass: int, n_cand: int) -> str:
    """Batch 2: URB447 SAR light docking — filter + rank; MD deferred."""
    n_fail = n_cand - n_pass
    passed = eval_df[eval_df["pass_gate"]].sort_values("dual")
    top = passed.head(5)
    top_txt = (
        ", ".join(
            f"{r['name']} (dual={_fmt(r['dual'])}, gap={_fmt(r['gap_mag_vs_thc'])})"
            for _, r in top.iterrows()
        )
        if len(top)
        else "ninguno"
    )
    urb = eval_df[eval_df["name"] == "URB447"]
    urb_txt = ""
    if not urb.empty and urb.iloc[0]["dual"] is not None:
        u = urb.iloc[0]
        urb_txt = (
            f" Semilla URB447: dual={_fmt(u['dual'])}, "
            f"gap vs THC={_fmt(u.get('gap_mag_vs_thc'))} "
            f"({'PASS' if u['pass_gate'] else 'fail'})."
        )
    return (
        f"**Resultado Batch 2 (fase ligera):** {n_pass}/{n_cand} PASS; "
        f"{n_fail} fail. Top por dual: {top_txt}.{urb_txt} "
        "MD / OpenMM **diferida** — solo docking CPU Vina. "
        "Vina = afinidad/pose proxy; **no** éxito Janus funcional."
    )


def _batch3_verdict(eval_df: pd.DataFrame, n_pass: int, n_cand: int) -> str:
    """Critical reading vs Batch-1 control JANUS_H1_02 and aspiration gap ~0.80."""
    by = {r["name"]: r for _, r in eval_df.iterrows()}

    def dual(name: str) -> float | None:
        r = by.get(name)
        return None if r is None or r["dual"] is None else float(r["dual"])

    def gap_thc(name: str) -> float | None:
        r = by.get(name)
        if r is None or r.get("gap_mag_vs_thc") is None:
            return None
        return float(r["gap_mag_vs_thc"])

    ctrl = "JANUS_H1_02"
    ctrl_dual = dual(ctrl)
    ctrl_gap = gap_thc(ctrl)
    ctrl_pass = bool(by[ctrl]["pass_gate"]) if ctrl in by else False

    refinements = [
        n
        for n in (
            "JANUS_H1_02a",
            "JANUS_H1_02b",
            "JANUS_H1_02c",
            "JANUS_H1_02d",
            "JANUS_H1_02e",
            "JANUS_H1_02f",
        )
        if n in by
    ]
    passed = eval_df[eval_df["pass_gate"]]["name"].tolist()
    aspirants = [
        n
        for n in [ctrl, *refinements]
        if gap_thc(n) is not None and gap_thc(n) > ASPIRATION_GAP_VS_THC
    ]
    better_than_ctrl = [
        n
        for n in refinements
        if ctrl_dual is not None and dual(n) is not None and dual(n) < ctrl_dual
    ]

    parts = [
        f"**Resultado:** {n_pass}/{n_cand} PASS"
        + (f" ({', '.join(passed)})." if passed else "."),
    ]
    if ctrl in by:
        parts.append(
            f"**Control H1_02:** dual={_fmt(ctrl_dual)}, gap vs THC={_fmt(ctrl_gap)} "
            f"({'PASS' if ctrl_pass else 'fail'} en este run)."
        )
    if better_than_ctrl:
        parts.append(
            f"Refinos con dual mejor (más negativo) que H1_02: {', '.join(better_than_ctrl)}."
        )
    else:
        parts.append(
            "Ningún refino mejora dual respecto al control H1_02 en este run."
        )
    if aspirants:
        parts.append(
            f"Aspiración gap vs THC > {ASPIRATION_GAP_VS_THC:.2f}: "
            f"{', '.join(aspirants)}."
        )
    else:
        parts.append(
            f"Ningún análogo alcanza aspiración gap vs THC > {ASPIRATION_GAP_VS_THC:.2f} "
            "(no es requisito único del gate duro)."
        )
    parts.append(
        "Vina = afinidad/pose proxy; gates funcionales 1–3 siguen abiertos. **No hay hit Janus.**"
    )
    return " ".join(parts)


def _batch2_verdict(eval_df: pd.DataFrame, n_pass: int, n_cand: int) -> str:
    """Critical reading: did H1×H2 help, or does COOH kill CB1 again?"""
    by = {r["name"]: r for _, r in eval_df.iterrows()}

    def dual(name: str) -> float | None:
        r = by.get(name)
        return None if r is None or r["dual"] is None else float(r["dual"])

    def cb1(name: str) -> float | None:
        r = by.get(name)
        return None if r is None or r["cb1_vina"] is None else float(r["cb1_vina"])

    acids = [n for n in ("JANUS_H1H2_01", "JANUS_H1H2_03") if n in by]
    esters = [n for n in ("JANUS_H1H2_02", "JANUS_H1H2_04") if n in by]
    neutrals = [n for n in ("JANUS_H1_03", "JANUS_H1_04") if n in by]
    thcv_cb1 = cb1("delta9-THCV")

    acid_cb1_weak = False
    if thcv_cb1 is not None and acids:
        acid_cb1_weak = all(
            cb1(n) is not None and cb1(n) > thcv_cb1 + 0.5  # noqa: weaker = less negative
            for n in acids
        )

    passed = eval_df[eval_df["pass_gate"]]["name"].tolist()
    parts = [
        f"**Resultado:** {n_pass}/{n_cand} PASS"
        + (f" ({', '.join(passed)})." if passed else "."),
    ]
    if acid_cb1_weak:
        parts.append(
            "**Veredicto H1×H2:** el COOH aromático vuelve a debilitar CB1 "
            "(ácidos H1H2 claramente peores que THCV en eje CB1) — el híbrido "
            "no rescata la lección de Batch 1; 1′-volumen no anula el castigo del ácido."
        )
    elif any(n in passed for n in acids + esters):
        parts.append(
            "**Veredicto H1×H2:** al menos un híbrido ácido/éster pasó gate — "
            "señal de que 1′+periferia puede compensar; sigue siendo proxy Vina, no Janus."
        )
    else:
        parts.append(
            "**Veredicto H1×H2:** ningún híbrido ácido/éster pasa gate; "
            "priorizar volumen 1′ en andamiaje neutro si los H1_0x mejoran."
        )

    neu_pass = [n for n in neutrals if n in passed]
    if neu_pass:
        parts.append(
            f"Volumen 1′ neutro: PASS en {', '.join(neu_pass)} — coherente con Batch 1 "
            "(rama bencílica mueve la aguja)."
        )
    elif neutrals:
        parts.append(
            "Volumen 1′ neutro (Et/cPr): no supera gate en este run — 1′-Me de Batch 1 "
            "sigue siendo el único hit proxy marginal."
        )

    parts.append(
        "Vina = afinidad/pose proxy; gates funcionales 1–3 siguen abiertos. **No hay hit Janus.**"
    )
    return " ".join(parts)


def write_public_summary(
    eval_df: pd.DataFrame,
    path: Path,
    scores_path: Path,
    batch: str,
    exhaustiveness: int | None,
    seed: int | None,
) -> None:
    dual_thcv = eval_df.attrs["dual_thcv"]
    dual_thc = eval_df.attrs["dual_thc"]
    thcv_thc_gap = eval_df.attrs["thcv_thc_gap"]
    n_pass = int(eval_df["pass_gate"].sum())
    n_cand = int(eval_df["role"].isin(GATE_EVAL_ROLES).sum())
    label = BATCH_LABELS.get(batch, batch)
    scores_rel = (
        scores_path.relative_to(ROOT).as_posix()
        if scores_path.is_relative_to(ROOT)
        else str(scores_path)
    )
    exh_txt = str(exhaustiveness) if exhaustiveness is not None else "12"
    seed_txt = str(seed) if seed is not None else "42"
    agg_label = (
        "ligandos evaluados (sintéticos / ex-lead)"
        if batch.startswith("option_d")
        else "candidatos de diseño"
    )

    lines = [
        f"# {label} — gate summary (public)",
        "",
        "> **No SMILES.** Structures and pose files stay local/gitignored. "
        "Vina = affinity/pose proxy only — not functional Janus success "
        "(see [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).",
        "",
        f"- Fecha: {date.today().isoformat()}",
        f"- Panel local: `data/libraries/{batch}.csv` (gitignored)",
        f"- Scores: `{scores_rel}` (gitignored)",
        f"- Receptores: CB1 5TGZ / CB2 6PT0; exhaustiveness={exh_txt}; seed={seed_txt}",
        "",
        "## Métrica de gate duro",
        "",
        "- `dual = mean(CB1_vina, CB2_vina)` (más negativo = mejor ocupación)",
        f"- Referencias en el mismo run: dual_THCV = **{_fmt(dual_thcv)}**, "
        f"dual_THC = **{_fmt(dual_thc)}**, gap THCV−THC = **{_fmt(thcv_thc_gap)}** kcal/mol",
        f"- **PASS** solo si: (1) `dual < dual_THCV` y (2) `(dual_THC − dual) > {CLEAR_GAP_MIN:.2f}` "
        f"(claramente > separación THCV–THC ≈ {THCV_THC_REF_GAP:.2f})",
        "",
        f"**Resultado agregado:** {n_pass}/{n_cand} {agg_label} pasaron el gate. "
        f"Exhaustiveness={exh_txt}; seed={seed_txt}.",
        "",
        "## Tabla (IDs + scores; sin SMILES)",
        "",
        "| ID | hipótesis | SMILES válido | CB1 | CB2 | dual | vs THCV | vs THC | ¿pasa gate? |",
        "|----|-----------|---------------|-----|-----|------|---------|--------|-------------|",
    ]
    for _, r in eval_df.iterrows():
        gate = "—"
        role = str(r["role"])
        if role in GATE_EVAL_ROLES:
            gate = "PASS" if r["pass_gate"] else "fail"
        elif role in {"seed", "anti_seed"}:
            gate = "ref"
        hyp = _hyp_label(r)
        if role in {"seed", "anti_seed"}:
            hyp = "REF"
        smiles_ok = "sí" if r.get("smiles") not in (None, "", float("nan")) else "—"
        # smiles always present in scores; design rows are valid if docked
        if r["cb1_vina"] is not None and r["cb2_vina"] is not None:
            smiles_ok = "sí"
        lines.append(
            f"| {r['name']} | {hyp} | {smiles_ok} | {_fmt(r['cb1_vina'])} | "
            f"{_fmt(r['cb2_vina'])} | {_fmt(r['dual'])} | {_fmt(r['vs_thcv'])} | "
            f"{_fmt(r['vs_thc'])} | {gate} |"
        )

    # Aspiration note (Batch 3+ / Option D): flag gaps vs THC > ~0.80
    aspir = eval_df[
        eval_df["role"].isin(GATE_EVAL_ROLES)
        & eval_df["gap_mag_vs_thc"].notna()
        & (eval_df["gap_mag_vs_thc"] > ASPIRATION_GAP_VS_THC)
    ]["name"].tolist()
    if batch in {"h1_h5_batch3", "option_d_batch1", "option_d_batch2"}:
        lines += [
            "",
            "## Aspiración (informativa)",
            "",
            f"- Gap vs THC > ~{ASPIRATION_GAP_VS_THC:.2f} kcal/mol: "
            + (
                ", ".join(aspir)
                if aspir
                else "ninguno en este run (no es requisito único del gate)"
            ),
            "",
        ]

    # Batch 2: ranked PASS list + fail count (public IDs only)
    if batch == "option_d_batch2":
        n_fail = n_cand - n_pass
        passed_rank = eval_df[eval_df["pass_gate"]].sort_values("dual")
        lines += [
            "",
            "## Top PASS (rank por dual; sin SMILES)",
            "",
            f"- PASS: **{n_pass}** · fail: **{n_fail}** · evaluados: **{n_cand}**",
            "",
            "| rank | ID | hipótesis | CB1 | CB2 | dual | gap vs THC |",
            "|------|----|-----------|-----|-----|------|------------|",
        ]
        for i, (_, r) in enumerate(passed_rank.iterrows(), start=1):
            lines.append(
                f"| {i} | {r['name']} | {_hyp_label(r)} | {_fmt(r['cb1_vina'])} | "
                f"{_fmt(r['cb2_vina'])} | {_fmt(r['dual'])} | "
                f"{_fmt(r['gap_mag_vs_thc'])} |"
            )
        if n_pass == 0:
            lines.append("| — | — | — | — | — | — | — |")
        lines += [
            "",
            "## IDs filtrados (PASS) rankeados por dual",
            "",
        ]
        if n_pass:
            for i, (_, r) in enumerate(passed_rank.iterrows(), start=1):
                lines.append(
                    f"{i}. `{r['name']}` — dual={_fmt(r['dual'])}, "
                    f"gap vs THC={_fmt(r['gap_mag_vs_thc'])}"
                )
        else:
            lines.append("_Ningún ID pasó el gate duro en este run._")
        lines.append("")

    lines += ["", "## Veredicto", ""]
    if batch == "h1_h5_batch2":
        lines.append(_batch2_verdict(eval_df, n_pass, n_cand))
    elif batch == "h1_h5_batch3":
        lines.append(_batch3_verdict(eval_df, n_pass, n_cand))
    elif batch == "option_d_batch1":
        lines.append(_option_d_verdict(eval_df, n_pass, n_cand))
    elif batch == "option_d_batch2":
        lines.append(_option_d_batch2_verdict(eval_df, n_pass, n_cand))
    elif n_pass == 0:
        lines.append(
            "Ningún análogo supera el gate duro de separación proxy frente a THCV/THC. "
            "Coherente con el hallazgo retrospectivo: el scaffold THCV-like no se separa "
            "fácilmente por afinidad Vina sola. Seguir con SAR / función; no declarar hit Janus."
        )
    else:
        passed = eval_df[eval_df["pass_gate"]]["name"].tolist()
        if batch == "h1_h5_batch1":
            lines.append(
                f"**{n_pass}/{n_cand} PASS (solo {', '.join(passed)}), y es marginal** "
                f"(gap vs THC {_fmt(float(eval_df[eval_df['pass_gate']].iloc[0]['gap_mag_vs_thc']))} "
                f"kcal/mol, umbral {CLEAR_GAP_MIN:.2f}). "
                "H2 (ácidos/ésteres) empeoran dual por CB1 débil — esperable y no = fallo de "
                "periferia. **No hay hit Janus**; hace falta binding/función. "
                "Lección → Batch 2: H1×H2 + volumen 1′ "
                "(ver [`h1_h5_design_history.md`](h1_h5_design_history.md))."
            )
        else:
            lines.append(
                f"Pasaron gate proxy: {', '.join(passed)}. "
                "Sigue siendo **solo** ocupación/afinidad — gates funcionales 1–3 siguen abiertos."
            )

    if batch.startswith("option_d"):
        ip_paths = (
            "`data/libraries/option_d*`, `results/docking/option_d*`, "
            "`results/hits/option_d*`"
        )
        pivot = (
            "- Pivot Track D: [`option_d_pivot_urb447.md`](option_d_pivot_urb447.md); "
            "NO-GO membrana: [`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md)."
        )
    else:
        ip_paths = (
            "`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`"
        )
        pivot = ""
    lines += [
        "",
        "## IP",
        "",
        f"- CSV/SDF/PDBQT de panel: gitignored ({ip_paths}).",
        f"- Detalle con SMILES (local): `results/hits/{batch}/gate_detail.md`.",
    ]
    if pivot:
        lines.append(pivot)
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--batch",
        type=str,
        default="h1_h5_batch1",
        help="Batch id (e.g. h1_h5_batch1, h1_h5_batch2)",
    )
    ap.add_argument("--scores", type=Path, default=None)
    ap.add_argument("--detail", type=Path, default=None)
    ap.add_argument("--summary", type=Path, default=None)
    ap.add_argument("--stats-json", type=Path, default=None)
    ap.add_argument("--full-csv", type=Path, default=None, help="Optional hyp/notes merge")
    ap.add_argument("--exhaustiveness", type=int, default=12)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    batch = args.batch
    scores = args.scores or ROOT / f"results/docking/{batch}/retrospective_scores.csv"
    detail = args.detail or ROOT / f"results/hits/{batch}/gate_detail.md"
    summary = args.summary or ROOT / f"results/reports/{batch}_gate_summary.md"
    stats_json = args.stats_json or ROOT / f"results/hits/{batch}/gate_stats.json"
    full_csv = args.full_csv or ROOT / f"data/libraries/{batch}_full.csv"

    if not scores.exists():
        print(f"BLOQUEO: missing scores {scores}")
        return 2

    df = pd.read_csv(scores)
    if full_csv.exists() and "hypothesis" not in df.columns:
        full = pd.read_csv(full_csv)
        keep = [c for c in ("name", "hypothesis", "notes") if c in full.columns]
        if len(keep) > 1:
            df = df.merge(full[keep], on="name", how="left")

    eval_df = evaluate(df)
    write_detail(eval_df, detail, scores, batch)
    write_public_summary(
        eval_df, summary, scores, batch, args.exhaustiveness, args.seed
    )

    payload = {
        "batch": batch,
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
            "exhaustiveness": args.exhaustiveness,
            "seed": args.seed,
        },
        "n_pass": int(eval_df["pass_gate"].sum()),
        "n_candidates": int(eval_df["role"].isin(GATE_EVAL_ROLES).sum()),
        "rows": eval_df.drop(columns=["smiles"], errors="ignore").to_dict(
            orient="records"
        ),
    }
    stats_json.parent.mkdir(parents=True, exist_ok=True)
    stats_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Detail (gitignored): {detail}")
    print(f"Public summary:      {summary}")
    print(f"Stats:               {stats_json}")
    print(
        f"Gate: {payload['n_pass']}/{payload['n_candidates']} design candidates PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
