# H1–H5 design history (public)

> **No SMILES.** Solo IDs, lecciones de gate proxy y política IP.  
> Vina = afinidad/pose — no éxito Janus funcional ([`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).

## Política IP (constante)

- SMILES / SDF / PDBQT / CSV de análogos de diseño: **solo** paths gitignored  
  (`data/libraries/h1_h5*`, `data/processed/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- Informes públicos en `results/reports/`: IDs, scores, pass/fail — **sin estructuras**.
- No publicar estructuras concretas en `docs/`.

## Iteración 1 — librería de diseño (Batch 1)

- Resumen: [`h1_h5_batch1_gate_summary.md`](h1_h5_batch1_gate_summary.md)
- Panel local: `data/libraries/h1_h5_batch1.csv` (gitignored)
- Hipótesis muestreadas: H1 (cadena/rama), H2 (ácido/éster), H3 (ω-F), H4 (9,10-H2), H5 (ArOMe lite)
- Gate duro: `dual < dual_THCV` **y** `(dual_THC − dual) > 0.40`
- **Resultado:** 1/7 PASS — solo **JANUS_H1_02** (1′-metil en THCV neutro), marginal
- **Lección:** la rama 1′-Me movió la aguja; ácidos/ésteres H2 debilitaron CB1 (dual peor). No hit Janus.

## Iteración 2 — H1×H2 + volumen 1′ (Batch 2)

- Resumen: [`h1_h5_batch2_gate_summary.md`](h1_h5_batch2_gate_summary.md)
- Panel local: `data/libraries/h1_h5_batch2.csv` (gitignored)
- Diseño: híbridos 1′-rama × THCVA (COOH / éster metílico) + volumen mayor en 1′ sobre THCV neutro (etil, ciclopropilo)
- Misma métrica de gate; refs delta9-THCV / delta9-THC en el mismo run
- Pregunta crítica: ¿el híbrido mejora, o el COOH mata CB1 otra vez?
- **Resultado:** 0/6 PASS. El COOH/éster **mata CB1 otra vez** (CB1 ≪ THCV); volumen 1′ neutro (Et/cPr) no supera el umbral claro vs THC. 1′-Me (Batch 1) sigue siendo el único PASS proxy marginal.
- Lecciones: ver “Lecciones técnicas” en el resumen Batch 2.

## Cierre — barrido rápido (Batch 1–2)

- **Fin de fase** de exploración rápida H1–H5 (hipótesis anchas: cadena/rama, ácidos/ésteres, ω-F, 9,10-H2, ArOMe lite, híbridos H1×H2, volumen 1′ Et/cPr).
- Único PASS proxy marginal acumulado: **JANUS_H1_02** (1′-metilo sobre scaffold THCV-like neutro).
- Vina estático ≠ éxito Janus funcional; gates 1–3 siguen abiertos.

## Iteración 3 — refino JANUS_H1_02 / 1′-Me (Batch 3)

- Plan: [`h1_h5_batch3_plan.md`](h1_h5_batch3_plan.md)
- Resumen: [`h1_h5_batch3_gate_summary.md`](h1_h5_batch3_gate_summary.md)
- Panel local: `data/libraries/h1_h5_batch3.csv` (gitignored)
- Diseño: 1′-Me fijo + ω-F / bioisóstero de cadena / F en rama / cadena corta / éteres de fenol (sin COOH/COOMe); control H1_02 regenerado en el mismo run
- **Resultado:** 5/7 PASS. Control H1_02 se reproduce (PASS). Solo **JANUS_H1_02c** mejora dual vs control y alcanza aspiración gap vs THC > 0.80 (0.856). Éteres de fenol (OMe/OEt) no ayudan.
- **Lección:** priorizar extremo de cadena no polar sobre enmascarar fenol; periferia ácida sigue prohibida. Vina ≠ Janus.
- **Lead #1 in silico:** **JANUS_H1_02c**. Gap 0.856 = proxy Vina; ω-F PASS sin batir H1_02; MD 2 ns en agua vs THCV = mixto/débil ([`md_lead_2ns_summary.md`](md_lead_2ns_summary.md)).
- **Batch membrane completo (2026-08-09):** POPC 20 ns × 3 (H1_02c, THCV, THC) OK. Resumen público: [`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md). Gate Track 1: **NO-GO** — lead no congela TM6 mejor que THCV; H-bond fenólico se recupera vs agua pero no bate THCV; diferenciación vs THC parcial (fenol sí, TM3–TM6 no). 1 réplica / 20 ns ≠ α.

## Pivot Opción D (2026-08-10) — eje sintético URB447 / Yin-Yang

- Decisión: **abandonar como eje principal** el andamiaje fitocannabinoide THCV-like tras NO-GO membrana. THCV / H1_02c quedan como control / PoC / *ex-lead*, no lead de desarrollo.
- Documento: [`option_d_pivot_urb447.md`](option_d_pivot_urb447.md)
- Primer panel retrospectivo: [`option_d_batch1_gate_summary.md`](option_d_batch1_gate_summary.md) (URB447, AM1710, GW405833 + refs; sin SMILES públicos de NCE)
- Qiu 2023: cita de clase Yin-Yang; **sin** SMILES en panel (no CID/SMILES público fiable)

## Opción D Batch 2 (2026-08-10) — fase ligera docking

- **Fase ligera docking done; MD diferida.** Solo Vina CPU dual 5TGZ/6PT0 (exh=8, seed=42); sin OpenMM.
- Panel local SAR mínimo alrededor de URB447 (`JANUS_D2_*`) + refs; SMILES gitignored.
- Resumen público (IDs + scores): [`option_d_batch2_gate_summary.md`](option_d_batch2_gate_summary.md)
- Lista filtrada rankeada por dual lista para priorizar; MD solo si se reabre sobre top PASS.

## Opción D Batch D1 (2026-08-10) — derivados; docking done; MD paused

- **Batch D1** = alias del cribado de derivados URB447 / Yin-Yang (reutiliza run Batch 2; no se rehizo Vina).
- Resumen público: [`option_d_batch_d1_gate_summary.md`](option_d_batch_d1_gate_summary.md)
- **MD pausada** (no OpenMM, no membrana).

## Scripts (genéricos; sin SMILES de análogos)

- `scripts/generate_h1_h5_candidates.py` — Batch 1
- `scripts/generate_h1_h5_batch2.py` — Batch 2
- `scripts/generate_h1_h5_batch3.py` — Batch 3
- `scripts/analyze_h1_h5_gate.py` — gate + informes (`--batch h1_h5_batchN` o `option_d_batchN`)
- `scripts/generate_option_d_batch1.py` — panel Track D Batch 1 (publicado + refs; gitignored)
- `scripts/generate_option_d_batch2.py` — panel Track D Batch 2 SAR URB447 (gitignored)
- `scripts/run_md_openmm_lead.py` — MD OpenMM lead vs THCV en agua (poses locales gitignored)
- `scripts/run_md_openmm_membrane_lead.py` — MD OpenMM POPC membrane lead vs THCV vs THC
- Prep/dock: `scripts/prepare_panel_3d.py`, `scripts/run_retrospective_dock.py`
