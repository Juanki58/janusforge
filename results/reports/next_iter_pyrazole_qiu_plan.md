# Próxima iteración — andamiaje pirazol rígido (Qiu 2023) — PLAN PAUSADO

> Público / castellano. **Sin SMILES ni estructuras de NCE.**  
> Estado: **documentación solamente** — **no** se lanza docking ni MD.  
> Trigger: descarte funcional de **JANUS_D2_22** (NO-GO trinquete CB1).  
> Fecha: 2026-08-11.

## Por qué este eje

| Hecho previo | Implicación |
|--------------|-------------|
| D2_22: top dual Vina (−11.277) + MD POPC sin trinquete | Carboxamida / Bz_pCF3 flexible **no** bloqueó TM6; COM solapó régimen THC |
| H1_02c ya falló el mismo patrón (PASS Vina → NO-GO membrana) | No repetir “otro lote URB447-like + score” sin cambiar hipótesis geométrica |
| Compuesto 14 (Qiu et al. 2023) | Pirazol Yin–Yang publicado; morfolina–**S173** (CB1) / **S285** (CB2); núcleo más rígido que el brazo carboxamida de Opción D |

Mapa: [`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md) §3.4. Falla D2_22: [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md).

## Hipótesis de diseño (sin química concreta aquí)

1. **Rigidez del núcleo pirazol** reduce el margen de rotación que, en D2_22, dejó TM6 “estable pero abierta”.
2. Anclar el brazo tipo **orto-morfolina** hacia el contacto **S173 / entorno TM6** (lectura Qiu), no solo maximizar dual Vina.
3. Mantener dualidad Janus como objetivo de **ensayo** eventual; el proxy in silico sigue siendo ranking, no α.

**Fuera de alcance de este documento:** SMILES NCE, librería enumerada, scripts de generación, docks, MD.

## Qué está pausado (explícito)

| Acción | Estado |
|--------|--------|
| Docking dual 5TGZ/6PT0 de panel Qiu-like | **No lanzar** |
| MD membrana / agua OpenMM | **No lanzar** (GPU liberada) |
| Enumeración / CSV de NCE en repo | **No** en este paso |
| Ensayo húmedo | Fuera de Track 1 cómputo; no sustituye el plan |

Reanudar solo con autorización explícita del usuario.

## Criterios de reanudación (cuando se autorice)

1. Hipótesis escrita (este doc o sucesor) + ancla literaria Qiu-14 / mapa.
2. Panel local gitignored; informe público = IDs + scores (sin SMILES NCE).
3. Gate docking: **no** celebrar PASS masivo heredado de umbrales THCV; priorizar ranking + rasgos S173/S285.
4. Si hay MD: réplicas y métricas de contacto farmacóforo — no otra réplica única “por score”.

## Enlaces

| Documento | Rol |
|-----------|-----|
| [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md) | Falla biofísica / descarte D2_22 |
| [`option_d_pivot_urb447.md`](option_d_pivot_urb447.md) | Pivot Opción D (contexto) |
| [`option_d_batch_d1_gate_summary.md`](option_d_batch_d1_gate_summary.md) | Ex-lead docking D2_22 |
| [`docs/lecciones_aprendidas_track1.md`](../../docs/lecciones_aprendidas_track1.md) | Lecciones + estado pausa |
| Qiu et al. 2023 | https://doi.org/10.1016/j.bioorg.2023.106377 |

---

**Status:** plan **pausado**. Sin cómputo pesado hasta nueva orden.
