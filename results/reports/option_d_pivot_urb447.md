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

## Criterio / guía

Ver actualización en [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md) y nota en historial [`h1_h5_design_history.md`](h1_h5_design_history.md).
