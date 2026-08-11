# Próxima iteración — andamiaje pirazol rígido (Qiu 2023) — ACTIVO (docking only)

> Público / castellano. **Sin SMILES ni estructuras de NCE.**  
> Estado: **fase ligera CPU en curso / Batch 1 docking hecho** — **MD/OpenMM pausada**.  
> Trigger: descarte funcional de **JANUS_D2_22** (NO-GO trinquete CB1) + autorización a reanudar eje Qiu.  
> Fecha: 2026-08-11.

## Por qué este eje

| Hecho previo | Implicación |
|--------------|-------------|
| D2_22: top dual Vina (−11.277) + MD POPC sin trinquete | Carboxamida / Bz_pCF3 flexible **no** bloqueó TM6; COM solapó régimen THC → **eje Opción D lead descartado** |
| H1_02c ya falló el mismo patrón (PASS Vina → NO-GO membrana) | No repetir “otro lote URB447-like + score” sin cambiar hipótesis geométrica |
| Compuesto 14 (Qiu et al. 2023) | Pirazol Yin–Yang publicado; morfolina–**S173** (CB1) / **S285** (CB2); núcleo más rígido que el brazo carboxamida de Opción D |

Mapa: [`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md) §3.4. Falla D2_22: [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md).

## Hipótesis de diseño

1. **Rigidez del núcleo pirazol** reduce el margen de rotación que, en D2_22, dejó TM6 “estable pero abierta”.
2. Anclar el brazo tipo **orto-morfolina** hacia el contacto **S173 / entorno TM6** (lectura Qiu), no solo maximizar dual Vina.
3. Mantener dualidad Janus como objetivo de **ensayo** eventual; el proxy in silico sigue siendo ranking, no α.

## Estado operativo (2026-08-11)

| Acción | Estado |
|--------|--------|
| Panel local `data/libraries/qiu_pyrazole_batch1.csv` | **Hecho** (gitignored; QIU_14 + QIU_01–07 + refs) |
| Docking dual 5TGZ/6PT0 (exh=10, seed=42) | **Hecho** — [`qiu_pyrazole_batch1_gate_summary.md`](qiu_pyrazole_batch1_gate_summary.md) |
| Gate | **Rank vs URB447** + gap vs THC > 0.80; legacy THCV-gate solo informativo |
| MD membrana / agua OpenMM | **Pausada** (GPU liberada; no lanzar) |
| Ensayo húmedo | Fuera de Track 1 cómputo |

### Compound 14 SMILES

- **No** hay CID PubChem / depósito ChEMBL fiable en esta recuperación.
- Panel usa reconstrucción desde descriptores publicados (N1-2-morfolinofenilo, C3-adamantilo, C4-Me, C5-Ph) como `QIU_14` — confianza media; Ki/IC₅₀ de tabla **no recuperados**.
- Informes públicos: IDs + scores solamente.

### Lectura Batch 1 (proxy)

Rank-gate PASS: **QIU_02**, **QIU_01**, **QIU_03** (meta / para / sin morfolina).  
**QIU_14 (orto, hipótesis Qiu) falla** el rank vs URB447 en Vina — coherente con “Vina ≠ contacto S173/S285 / α”. No celebrar para/meta como “mejor Janus”; son ocupación proxy.

## Criterios siguientes (cuando se autorice)

1. Inspección de poses locales (gitignored) para H-bond proxy S173/S285 en QIU_14 vs QIU_01/02 — sin MD.
2. Si se sigue en química: SAR dirigido a **orto** + cage, no escalar solo dual Vina de regioisómeros.
3. Ensayo funcional sobre shortlist — no otra MD ciega.
4. Si hay MD: réplicas y métricas de contacto farmacóforo.

## Enlaces

| Documento | Rol |
|-----------|-----|
| [`qiu_pyrazole_batch1_gate_summary.md`](qiu_pyrazole_batch1_gate_summary.md) | Gate Batch 1 (público) |
| [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md) | Falla biofísica / descarte D2_22 |
| [`option_d_pivot_urb447.md`](option_d_pivot_urb447.md) | Pivot Opción D (contexto; D2_22 cerrado) |
| [`docs/lecciones_aprendidas_track1.md`](../../docs/lecciones_aprendidas_track1.md) | Lecciones + estado |
| Qiu et al. 2023 | https://doi.org/10.1016/j.bioorg.2023.106377 |

---

**Status:** eje Qiu **activo** en fase ligera (docking). **MD pausada.**
