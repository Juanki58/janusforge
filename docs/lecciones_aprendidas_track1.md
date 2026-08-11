# Lecciones aprendidas — Track 1 (hasta MD membrana D2_22)

> Castellano. Tono crítico y operativo. **Sin SMILES ni estructuras de NCE.**  
> Corte temporal: post MD POPC 20 ns de **JANUS_D2_22** (2026-08-11).  
> No sustituye informes de gate ni la Guía Maestra; consolida lo que el proyecto ya pagó en cómputo y diseño.

---

## 1. Contexto

**Objetivo del programa:** ligando monomolecular con perfil **CB1 antagonista + CB2 agonista** (Janus / Yin-Yang) orientado a **fibrosis** (IPF como lectura biológica secundaria, no como gate de docking).

**Arco Track 1 hasta aquí:**

1. **Cannabis-first / THCV-like:** THCV como PoC natural imperfecto → serie H1–H5 (análogos) → lead proxy **JANUS_H1_02c**.
2. **MD membrana H1_02c:** NO-GO vs THCV en POPC 20 ns → cierre del eje fitocannabinoide como *lead de desarrollo*.
3. **Opción D:** pivot a scaffolds sintéticos anclados en literatura (**URB447** primero; AM1710 / GW405833 / clase Qiu como comparadores), SAR Batch 2/D1 → lead docking **JANUS_D2_22**.
4. **MD membrana D2_22:** run OK; análisis de falla → **D2_22 descartado** como lead funcional (NO-GO trinquete CB1). GPU pausada.

Marco normativo: [`guia_maestra_biotecnologia_quimiotipos.md`](guia_maestra_biotecnologia_quimiotipos.md). Pivot: [`../results/reports/option_d_pivot_urb447.md`](../results/reports/option_d_pivot_urb447.md).

---

## 2. Lecciones de docking / gate

| Lección | Por qué importa |
|---------|-----------------|
| **Vina ≠ agonismo/antagonismo ni α** | Score dual 5TGZ/6PT0 mide afinidad/pose proxy en conformaciones fijas. No clasifica eficacia, flip de dosis ni bifuncionalidad. Usarlo como ranking, no como veredicto farmacológico. |
| **Gate vs THCV/THC demasiado fácil en scaffold URB447** | Batch D1: **34/34 PASS** con los umbrales heredados de H1–H5 (`dual < dual_THCV` y gap vs THC > 0.40). En esa familia el gate deja de discriminar; hay que **priorizar por ranking** (dual, ejes, SAR) y no celebrar “PASS masivo”. |
| **URB447 gana el proxy frente a fitocannabinoides** | En paneles retrospectivos, el comparador sintético empuja separación dual vs THC más que THCV solo. Eso justifica el pivot de *andamiaje*, no un claim de superioridad funcional. |
| **H1_02c: PASS Vina, NO-GO membrana** | El lead fitocannabinoide pasó el gate duro de docking y falló el paquete geométrico en POPC. **Docking PASS no autoriza ensayo** si el siguiente gate (MD / función) falla. |
| **D2_22: misma lección, segunda vez** | Dual Vina −11.277 (mejor del Batch D1) → MD POPC sin trinquete; COM solapa THC. **Vina no predice restricción funcional** — no repetir el ciclo “top score → MD única → sorpresa”. |

Detalle Batch D1: [`../results/reports/option_d_batch_d1_gate_summary.md`](../results/reports/option_d_batch_d1_gate_summary.md). Flip / α: [`mecanismo_flip_thcv_cb1.md`](mecanismo_flip_thcv_cb1.md).

---

## 3. Lecciones de diseño H1–H5

Serie cerrada como eje; útil como *ex-lead* y control de contraste.

| Observación | Lectura fría |
|-------------|--------------|
| **1′-Me movió la aguja** | Único cambio que dio PASS proxy marginal (H1_02 → refino H1_02c). Señal SAR real, no magia de librería. |
| **Et / cPr en 1′ no** | Más volumen en la misma posición no superó el umbral claro vs THC; no escalar “más grueso = mejor”. |
| **COOH / COOMe hunden CB1 en Vina estático** | Periferia ácida/éster en anillo A derrumba CB1 (~−6 vs THCV ~−8.9) aunque CB2 aguante; dual se va al suelo. |
| **H1×H2 falló** | Combinar a ciegas “rama que ayuda” × “periferia ácida deseable” **no** rescata CB1. No mezclar hipótesis periféricas sin evidencia de que el pozo CB1 lo tolera. |

Historial (sin estructuras): [`../results/reports/h1_h5_design_history.md`](../results/reports/h1_h5_design_history.md).

---

## 4. Lecciones de MD

| Escala | Qué salió | Qué no se puede afirmar |
|--------|-----------|-------------------------|
| **2 ns agua** | Señales mixtas/débiles (H1_02c vs THCV); fenol peor que en membrana. | Estabilidad o trinquete; ranking funcional. |
| **20 ns POPC — H1_02c** | **NO-GO** vs plan: no congela TM6 mejor que THCV; H-bond recupera vs agua pero no bate THCV; vs THC solo el fenol separa con claridad. | “El andamiaje THCV-like está muerto para siempre” — sí está muerto como *eje prioritario* con esta evidencia. |
| **20 ns POPC — D2_22** | Run OK. COM 12.35 Å ≈ THC (12.06), no contención THCV (13.07); TM6 RMSD bajo = hélice estable pero “atrapada” más abierta (hipótesis: carboxamida/Bz_pCF3 no bloquea TM6). **Descarte funcional.** | Agonismo CB1, perfil Janus, o “mejor que URB447/Qiu-14”. El overlap COM–THC es evidencia **en contra del trinquete**, no prueba de agonismo. |
| **1 réplica × 20 ns** | Útil para priorizar, descartar y detectar explosiones. | **No demuestra función** ni agonismo. |
| **Infra** | GPU/calor y Docker son riesgo del proyecto. Tras D2_22: **pausa de cómputo pesado** (GPU liberada). | Que un `EXIT_CODE=0` iguale biología. |

Informes: [`../results/reports/md_lead_2ns_summary.md`](../results/reports/md_lead_2ns_summary.md) · [`../results/reports/md_membrane_20ns_summary.md`](../results/reports/md_membrane_20ns_summary.md) · [`../results/reports/md_d2_22_20ns_summary.md`](../results/reports/md_d2_22_20ns_summary.md).

---

## 5. Lecciones de literatura / novelty

| Hecho | Implicación para janusforge |
|-------|-----------------------------|
| **Janus × fibrosis = prior art** (concepto) | No reivindicar el *rationale*. Claims teóricos de uso no son el activo. |
| **White space = NCE + datos** | Producto defendible = química nueva (o SAR no obvio) **más** evidencia experimental (función receptor → fibrosis), no otro informe Vina. |
| **URB447 = ancla conceptual limpia** | Antagonista neutro CB1 + ago CB2; periferia. **AM1710 / GW** pasan mejor el corte nM en CB2, con CB1 más sucio / mecanismo más enredado. Elegir ancla ≠ elegir el más potente en nM. |
| **Hueco operativo** | Janus **monomolecular** no probado de forma convincente en **fibrosis in vivo** (bleomicina/IPF) en los precedentes del mapa. Ahí está el vacío experimental, no en “inventar Janus”. |
| **IP de divulgación** | **No publicar SMILES de NCE en GitHub público.** Informes = IDs + scores; estructuras en paths gitignored. |

Novelty: [`literatura_prioridad_y_novelty.md`](literatura_prioridad_y_novelty.md). Mapa: [`mapa_ligandos_janus_cb1_cb2.md`](mapa_ligandos_janus_cb1_cb2.md).

---

## 6. Lecciones de proceso

| Práctica | Lección |
|----------|---------|
| **Track 1 vs Track 2** | Ejecución diaria = discovery in silico / pre-ensayo (Track 1). Supply / breeding / fermentación (Track 2) no se “cierra”, pero no desplaza cómputo ni diseño. |
| **MD pausable / diferible** | Docking Batch 2 se cerró sin OpenMM; MD solo con lead y autorización. Tras NO-GO D2_22: **pausa GPU** — no acoplar MD a cada PASS de gate. |
| **Visor local** | Útil para poses y trayectorias listadas; el servidor FastAPI debe estar **levantado** (`lanzar_visor.bat` / app en `127.0.0.1:8765`). Sin proceso, la UI no inventa datos. |

---

## 7. Estado actual y decisiones

| Ítem | Estado |
|------|--------|
| **JANUS_D2_22** | **Descartado** como lead funcional (NO-GO trinquete CB1). Sigue como *ex-lead docking* Batch D1 (dual −11.277). |
| **Eje URB447 / Batch D1 flexible** | Cerrado como prioridad de trinquete; no más MD sobre D2_22 ni runners-up sin rediseño de hipótesis. |
| **Eje H1–H5** | Cerrado como lead; H1_02c = contraste / ex-lead. |
| **Cómputo pesado** | **Pausado** (GPU liberada). |
| **Próximo eje** | Plan metodológico **pirazol rígido Qiu-like** (Compuesto 14; S173/TM6; sin margen de rotación) — **solo documentación**, sin docking/MD ahora. Ver [`../results/reports/next_iter_pyrazole_qiu_plan.md`](../results/reports/next_iter_pyrazole_qiu_plan.md). |

Análisis de falla: [`../results/reports/md_d2_22_20ns_summary.md`](../results/reports/md_d2_22_20ns_summary.md) § Análisis de la falla biofísica. Criterio formal: [`criterio_exito_janus.md`](criterio_exito_janus.md).

---

## 8. Enlaces

| Documento | Rol |
|-----------|-----|
| [`../results/reports/md_d2_22_20ns_summary.md`](../results/reports/md_d2_22_20ns_summary.md) | MD 20 ns POPC — D2_22 + análisis de falla / descarte |
| [`../results/reports/next_iter_pyrazole_qiu_plan.md`](../results/reports/next_iter_pyrazole_qiu_plan.md) | Plan pausado — iteración pirazol Qiu-like |
| [`../results/reports/md_membrane_20ns_summary.md`](../results/reports/md_membrane_20ns_summary.md) | MD 20 ns POPC — H1_02c / THCV / THC |
| [`../results/reports/option_d_batch_d1_gate_summary.md`](../results/reports/option_d_batch_d1_gate_summary.md) | Gate Batch D1 (34/34 PASS; D2_22 = ex-lead) |
| [`../results/reports/option_d_pivot_urb447.md`](../results/reports/option_d_pivot_urb447.md) | Decisión pivot Opción D |
| [`mapa_ligandos_janus_cb1_cb2.md`](mapa_ligandos_janus_cb1_cb2.md) | Precedentes URB447 / GW / AM1710 / Qiu-14 |
| [`literatura_prioridad_y_novelty.md`](literatura_prioridad_y_novelty.md) | Prior art vs white space |
| [`mecanismo_flip_thcv_cb1.md`](mecanismo_flip_thcv_cb1.md) | Flip CB1 / Vina ≠ α |
| [`guia_maestra_biotecnologia_quimiotipos.md`](guia_maestra_biotecnologia_quimiotipos.md) | Norma Track 1 / Track 2 |
| [`criterio_exito_janus.md`](criterio_exito_janus.md) | Gates de éxito pre-ensayo |
| [`../results/reports/h1_h5_design_history.md`](../results/reports/h1_h5_design_history.md) | Lecciones SAR H1–H5 |

---

*Última actualización: 2026-08-11 — D2_22 descartado; plan pirazol Qiu pausado.*
