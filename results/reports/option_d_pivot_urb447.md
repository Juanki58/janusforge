# Opción D — pivot a andamiajes sintéticos URB447 / Yin-Yang

> Documento público (castellano). **Sin SMILES ni estructuras de NCE.**  
> Decisión: 2026-08-09/10 · Trigger: NO-GO MD membrana Track 1.

## Decisión

Tras el gate de membrana POPC 20 ns ([`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md)), el andamiaje **fitocannabinoide THCV-like** (serie 1′-Me / lead **JANUS_H1_02c**) **no** se prioriza como eje principal de Track 1.

**Opción D (elegida):** pasar el norte operativo de Track 1 a **scaffolds sintéticos Janus / Yin-Yang** anclados en literatura — en primer lugar **URB447** (comparador de diseño ya en el quimioma) y ligandos Yin-Yang **ya publicados** (p. ej. AM1710, GW405833; Qiu 2023 como referencia de clase sin SMILES en panel local hasta CID/SMILES público fiable).

## Qué queda de THCV / H1–H5

| Rol | Estado |
|-----|--------|
| **THCV** | Control / PoC natural del perfil Janus imperfecto — **no** lead de desarrollo |
| **H1–H5 / H1_02c** | Serie cerrada como eje; H1_02c puede figurar como *ex-lead* de contraste en paneles locales |
| **Track 1 actual** | Prioriza scaffold sintético Janus (URB447 → SAR Yin-Yang) |

## Sin overclaim IP

- El perfil CB1-ant / CB2-ago (“Janus”, “Yin-Yang”) **ya existe** en literatura (LoVerme 2009; Dhopeshwarkar 2017; Qiu 2023).
- Este pivot **no** reivindica novelty de concepto; busca ejecución (separación proxy → función → fibrosis) sobre chemotipos sintéticos publicados como ancla.
- Paneles locales `option_d*` / poses: gitignored. Informes públicos: IDs + scores.

## Primer lote operativo

- Panel local: `data/libraries/option_d_batch1.csv` (gitignored)
- Gate proxy dual 5TGZ/6PT0: [`option_d_batch1_gate_summary.md`](option_d_batch1_gate_summary.md)
- Scripts: `scripts/generate_option_d_batch1.py`, `scripts/prepare_panel_3d.py`, `scripts/run_retrospective_dock.py`, `scripts/analyze_h1_h5_gate.py --batch option_d_batch1`

## Batch 2 — fase ligera (docking done; MD diferida)

- **Estado (2026-08-10):** fase ligera de docking CPU **completada**. MD / OpenMM **diferida** (no membrana, no agua en este lote).
- Panel local SAR URB447: `data/libraries/option_d_batch2.csv` (gitignored; IDs `JANUS_D2_*` + refs URB447 / GW405833 / THCV / THC)
- Gate proxy: [`option_d_batch2_gate_summary.md`](option_d_batch2_gate_summary.md) — lista filtrada rankeada por dual; sin SMILES públicos
- Scripts: `scripts/generate_option_d_batch2.py`, `scripts/analyze_h1_h5_gate.py --batch option_d_batch2`
- MD membrana 20 ns POPC sobre JANUS_D2_22: **completo** luego **NO-GO funcional** ([`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md)) — no reabrir Track 1 fitocannabinoide

## Batch D1 — derivados URB447 / Yin-Yang (docking done; MD completo; lead descartado)

- **Estado (2026-08-11):** Batch D1 = cribado de **derivados** (mismo panel/run que Batch 2). Docking CPU dual 5TGZ/6PT0 **done**; **MD membrana 20 ns POPC completo** (OpenMM GPU; JANUS_D2_22; `EXIT_CODE=0`).
- Alias público: [`option_d_batch_d1_gate_summary.md`](option_d_batch_d1_gate_summary.md) — tabla filtrada rankeada por dual; sin SMILES; apunta a scores/poses `option_d_batch2` (gitignored)
- No se rehizo Vina (36×2 docks reutilizados). Top PASS histórico: JANUS_D2_22, JANUS_D2_05, JANUS_D2_10, JANUS_D2_15, JANUS_D2_29
- **JANUS_D2_22:** *ex-lead docking* (dual −11.277) — **descartado funcionalmente** (NO-GO trinquete CB1). MD + análisis: [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md).
- **Cómputo pesado:** **pausado** (GPU liberada). No más docking/MD sobre este eje sin autorización.
- **Próximo eje (plan, no ejecución):** andamiaje **pirazol rígido Qiu-like** (Compuesto 14; S173/TM6) — [`next_iter_pyrazole_qiu_plan.md`](next_iter_pyrazole_qiu_plan.md).

## Criterio / guía

Ver actualización en [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md) y nota en historial [`h1_h5_design_history.md`](h1_h5_design_history.md).

**Lecciones consolidadas (post descarte D2_22):** [`docs/lecciones_aprendidas_track1.md`](../../docs/lecciones_aprendidas_track1.md) — Vina ≠ α (2ª vez: H1_02c y D2_22); gate URB447 demasiado fácil; D2_22 descartado; GPU pausa; siguiente = plan pirazol Qiu.

## Precedente literario (mapa Janus)

**URB447** ancla el pivot Opción D como precedente *conceptual* (Janus limpio + periferia), **no** como el ligando de mayor afinidad CB2 del panel de referencia: AM1710 y GW405833 pasan mejor el corte nM (~Kd ≈ 8.5 nM ↔ −11 kcal/mol); el hueco **fibrosis *in vivo* con un único Janus** de esas familias sigue abierto. Mapa completo: [`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md).
