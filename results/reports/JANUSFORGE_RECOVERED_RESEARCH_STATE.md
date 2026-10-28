# JANUSFORGE — RECOVERED RESEARCH STATE

**Tipo:** inventario / memoria recuperada (solo estado local + git)  
**Fecha de recuperación:** 2026-08-17  
**Prohibiciones respetadas:** sin nueva investigación, sin docking/MD/QSAR, sin modificar hipótesis, sin borrar/sobrescribir docs científicos previos, sin commit, sin tocar README.  
**Único archivo nuevo:** este informe.

---

## 1. Estado git (snapshot)

| Ítem | Valor |
|------|--------|
| **HEAD** | `c43c0b7` — `cursor/pr5-0q-audit-smrf-0q1-clean` |
| **Mensaje HEAD** | Add 0Q SMRF and 0Q.1 scientific audit (2026-08-16) |
| **origin/master** | `8d3a34a` — Merge PR #6 (incluye PR5) |
| **master local** | `7213cf9` — Add PDF export of Qiu 0P… (atrasado vs origin) |
| **Worktrees** | Solo uno: `C:/Users/juanc/projects/janusforge` @ `c43c0b7` |
| **Staged / unstaged diff** | Vacío (`git diff` / `git diff --cached` sin cambios tracked) |
| **Tracked files** | ~83 paths |
| **Untracked relevante** | Round1\* / AUDIT\_\* / DOCUMENTARY\_\* / `qiu_0q2f_*` / `data/papers/**` / boxes receptores / `.micromamba/` |

### Ramas (locales + remotas vistas)

- Activa: `cursor/pr5-0q-audit-smrf-0q1-clean`
- Limpias remotas mergeadas: `pr1`…`pr5`-clean, `qiu-protocol-ip-cro-0p`, `master`
- Variantes dirty locales: `cursor/pr1…pr5` (sin `-clean`), `cursor/qiu-protocol-ip-cro-0p`

### Log condensado (arco científico, no dump)

```
daaa269 Initial: CB1-ant / CB2-ago screening scaffold
… → H1–H5 batches → md_membrane → 82ce0f5 Pivot URB447 (H1 NO-GO)
… → e2e0fe9 Designate JANUS_D2_22 lead → 485bb00 D2_22 biophysical NO-GO + Qiu plan
… → 57551db Qiu pyrazole docking → 72ff659 Qiu 0D structures
… (en origin/master, no todos en WT): 0M CRO, 0P external table, dossier
… → c43c0b7 / 8d3a34a 0Q + SMRF + 0Q.1
```

### Qué hay en `origin/master` y **no** está en el working tree actual

Ejemplos (diff HEAD→origin/master): `qiu_0p_external_evidence_table.md`, `qiu_0m_h1a_wet_handoff.md`, `janusforge_dossier_estado_programa.md`, `cro_package_h1a/SEND/*`, `docs/borrador_libro_janusforge.md`.  
**Implicación:** la memoria “completa” del programa post-0D no está toda materializada en el checkout actual; parte vive solo en git remoto/master.

### Diff resumen

- Working tree vs index: **sin cambios tracked**.
- Untracked: documentación Round1 (2026-08-16/17), auditoría soft-drug, matriz documental, SI/papers bajo `data/papers/` (masivo).

---

## 2. Inventario documental (paths que existen)

### Presentes en working tree — `docs/`

| Path | Rol |
|------|-----|
| `docs/guia_maestra_biotecnologia_quimiotipos.md` | Norma Nivel 0 Track1/Track2 |
| `docs/criterio_exito_janus.md` | Gates éxito pre-ensayo |
| `docs/quimioma_cannabico_cb1_cb2.md` | Brújula química (cannabis-first histórico) |
| `docs/literatura_fibrosis_cb1_cb2.md` | Memoria biológica fibrosis |
| `docs/literatura_prioridad_y_novelty.md` | Prior art / novelty |
| `docs/mapa_ligandos_janus_cb1_cb2.md` | Precedentes URB447/GW/AM1710/Qiu-14 |
| `docs/mecanismo_flip_thcv_cb1.md` | Flip bifásico THCV CB1 |
| `docs/lecciones_aprendidas_track1.md` | Estado post D2_22 + Qiu Batch1 |
| `docs/quimiotipos_varinas_thcv.md`, `apendice_ip_supply_botanico.md`, `README.md` | Soporte |

### Presentes en WT — `results/reports/` (ciencia / gates tracked o untracked)

**Track1 / Option D / Qiu docking (tracked):**  
`h1_h5_*`, `md_*`, `option_d_*`, `next_iter_pyrazole_qiu_plan.md`, `qiu_pyrazole_batch1_gate_summary.md`, `qiu_0d_structure_verification.md`, `retrospective_panel_separation.md`

**0Q SMRF (tracked):**  
`qiu_0q_independent_scientific_audit.md`, `qiu_0q_smrf_matrix.md`, `qiu_0q_smrf_pairs.csv`, `qiu_0q1_*`

**Untracked (Round1 + audits 16–17 ago):**  
`ROUND1*`, `ROUND1B*`, `CB2_Experimental_Master_Dataset_*`, `QUARANTINE_LOG.md`, `DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX.md`, `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md`, `qiu_0q2f_regioisomer_14_15_16_audit.md` (+ CSV)

### Directorios pedidos no usados como raíz científica

`research/`, `literature/`, `notes/`, `analysis/`, `prompts/` — **no** aparecen como árboles de trabajo principales.  
`data/papers/` — **sí** (masivo, untracked): SI Qiu, OCR, API JSON, PDFs recon, soft-drug extracts.  
`scripts/` — pipeline docking/MD/análisis (tracked).

### Keywords halladas en nombres

`janus`, `cb1`/`cb2`, `thcv`, `gw405833`, `am1710`, `qiu`, `pyrazole`, `d2_22`, `novelty`, `audit`, `candidate`, `gold`, `controlled`/`deactivation`, `smrf`, `gemini` (solo en `qiu_0q1_final_cursor_vs_gemini.md`).

---

## 3. Historia de investigación (A–I)

### A. Hipótesis científica inicial

Ligando **monomolecular** con perfil **CB1 antagonista + CB2 agonista** (“Janus” / “Yin-Yang”), orientado a **fibrosis** (IPF como filtro de indicación *después* del receptor). Fuente: `README.md`; `docs/guia_maestra_*`; commit `daaa269` (2026-08-06).

### B. Molécula / familia original buscada

**Cannabis-first:** Δ9-**THCV** como PoC natural imperfecto + análogos **THCV-like** (hipótesis H1–H5). URB447 como *design comparator*, no norte inicial (`docs/quimioma_cannabico_cb1_cb2.md`).

### C. Significado exacto del “conmutador” CB1/CB2 (no confundir)

En el corpus coexisten **tres** usos documentados:

| Uso | Significado documentado | Fuente |
|-----|-------------------------|--------|
| **Flip THCV** | Cambio de **signo CB1** dosis/ocupación-dependiente (ant → ago parcial a alta ocupación); no es dual Yin-Yang | `docs/mecanismo_flip_thcv_cb1.md` |
| **Switch Qiu / Yin-Yang** | Sustitución **N1-orto-morfolina** (vs meta/para) como “interruptor” bifuncional **CB1-ant + CB2-ago** en pirazol | Qiu abstract/SI; `qiu_0d_*`; `qiu_0q_*`; 0P en master |
| **SMRF molecular switch** | Cambio estructural que invierte **modo de eficacia** (p.ej. CB2 ago↔inv), a menudo vía bulk→Trp6.48; **≠** ley universal dual CB1/CB2 | `qiu_0q_smrf_matrix.md`; `qiu_0q1_final_*` |

### D. Candidatos investigados (IDs / anclas)

| Fase | Objetos |
|------|---------|
| H1–H5 | Serie THCV-like; lead proxy **JANUS_H1_02** → **JANUS_H1_02c** |
| Controles | Δ9-THCV, Δ9-THC |
| Option D | Panel **JANUS_D2_***; lead docking **JANUS_D2_22** (Bz_pCF3); runners D2_05/10/15/29; semilla **URB447** |
| Qiu Batch1 docking | **QIU_14**, QIU_01–07 + refs URB447/GW/THCV/THC |
| Qiu publicados (0D+) | Cpd **14, 15, 16, 20, 24** (identidades SI) |
| Precedentes mapa | URB447, GW405833, AM1710, Qiu-14 |
| SMRF A-pairs | MRI2687/MRI2594; HU-308 / ago-3 /(R)-1 |

### E. Candidatos / ejes descartados

| Objeto | Decisión |
|--------|----------|
| Eje H1–H5 / H1_02c como lead | **NO-GO** membrana POPC (`md_membrane_20ns_summary.md`; pivot `82ce0f5`) |
| **JANUS_D2_22** como lead funcional | **NO-GO** trinquete CB1 (`md_d2_22_20ns_summary.md`; commit `485bb00`) |
| Path “Janusforge = motor docking/NCE anclado Qiu-14” | Clasificación **D NO-GO** (`qiu_0q_independent_scientific_audit.md`) |
| Soft-drug Makriyannis como fenotipo Janus | **NO INTEGRABLE** (agonistas CB1) — `AUDIT_CONTROLLED_DEACTIVATION_*` |

### F. Tabla de descartes (evidencia)

| Candidato / path | Motivo | Evidencia | Fuente | Definitivo vs provisional |
|------------------|--------|-----------|--------|---------------------------|
| H1_02c / fitocannabinoide | No mejora panel vs THCV en POPC 20 ns | TM6 RMSD, H-bond, gates plan | `md_membrane_20ns_summary.md` | **Definitivo como eje prioritario**; 1 réplica = priorización |
| D2_22 | COM TM3–TM6 ≈ THC, no contención THCV; Vina≠trinquete | MD 20 ns métricas | `md_d2_22_20ns_summary.md`; `485bb00` | **NO-GO científico del lead** (no “pausa”); MD pesada **pausada** aparte |
| Docking-NCE Qiu-first | Concepto Janus + fibrosis ya publicados; Qiu sin potencias OA; compute prematuro | Primarios / patentes | `qiu_0q_independent_scientific_audit.md` §13 | **D** path compute; espacio fibrosis **no E** |
| Soft-drug → Janus | Leads = CB1 agonists | Sharma/Nikas/Kulkarni | `AUDIT_CONTROLLED_DEACTIVATION_*` | Fenotipo **NO INTEGRABLE**; ADME **CONDICIONAL** |

### G. Precedentes literarios ya explorados (local)

URB447 (2009); GW405833 / AM1710 (Valenzano 2005; Khanolkar 2007; Dhopeshwarkar 2017 “Janus”); Qiu 2023 Yin-Yang; Li/Hua 2019 5ZTY + MRI pair; Kosar 2024 HU-308/(R)-1; Cinar / MRI-1867 CB1+iNOS; patentes WO2022026478 / US20230234928; soft-drug Sharma 2013 / Nikas 2015 / Kulkarni 2016. Detalle: §8 y `docs/literatura_prioridad_y_novelty.md`.

### H. Cuándo se descubrió que la dirección ya estaba cubierta

| Fecha (doc) | Hallazgo |
|-------------|----------|
| 2026-08-06 | Novelty audit: concepto Janus×fibrosis = prior art; white space = NCE+datos (`literatura_prioridad_y_novelty.md`) |
| 2026-08-10 | Mapa ligandos: URB447/GW/AM1710/Qiu-14 precedentes; hueco = fibrosis *in vivo* monomolecular |
| 2026-08-13 | 0Q destroy: docking-NCE redundante; patentes fibrosis dual |
| 2026-08-17 | Soft-drug chemotype ≠ Janus (audit) |

### I. Dirección que quedó viva tras descartes

Documentada en capas (ver **CONFLICTOS** §12 del informe usuario):

1. **Post D2_22 (11 ago):** eje **pirazol Qiu-like** — docking light activo; MD pausada (`next_iter_pyrazole_qiu_plan.md`; `lecciones_aprendidas_track1.md`).
2. **Post 0Q (13 ago):** **NO-GO** del path compute-NCE; puerta estrecha = datos Qiu + tools comerciales wet.
3. **0Q-SMRF (13–15 ago):** Option **B ACTIVE** (`0Q-SMRF = MODERATE`); Option **A 0M = RESERVE**; 0Q.1 = **EXPAND** (literatura/claim-split), **sin** NCE/docking/MD.
4. **Round1.9 (17 ago):** **PIPELINE = STOP** (documental; GOLD_CONFIRMED = 0).

---

## 4. Distinción crítica — clasificación A–E

| Documento / tema | Clasificación | Base explícita |
|------------------|---------------|----------------|
| Khanolkar 2007 / AM1710 (mapa, Option D ancla) | **B** historical precedent | `mapa_ligandos_*`; `option_d_pivot_*` |
| Valenzano 2005 / GW405833 (idem) | **B** | Idem |
| AM1710 / GW en Round1.x | **D** pending validation evidence | `ROUND1.9`: REVIEW_REQUIRED; Tables/PDF unrecovered |
| Controlled-deactivation 2013/2015/2016 | **E** other (+ CONDICIONAL ADME; **no** dirección Janus) | `AUDIT_CONTROLLED_DEACTIVATION_*`: NO INTEGRABLE fenotipo |
| Qiu 14 en Track1 post-D2_22 | Fue **A** (eje activo docking) luego cuestionado por 0Q | `next_iter_*` vs `qiu_0q_*` D |
| 0Q-SMRF / EXPAND | Trabajo documental activo ≠ diseño NCE | `qiu_0q_smrf_matrix.md` |

**No confundir:** validación documental Round1 (quién posee números) ≠ norte de diseño Track1.

---

## 5. JANUS_D2_22 — reconstrucción exacta

| Pregunta | Respuesta documentada |
|----------|------------------------|
| **Por qué creado** | SAR Option D / Batch 2–D1 derivados URB447/Yin-Yang; hipótesis Bz_pCF3 |
| **Hipótesis** | Scaffold sintético con dual Vina alto → posible trinquete CB1 inactivo vs panel THCV/THC |
| **Cálculos** | Docking dual 5TGZ/6PT0 (exh=8); dual = **−11.277** (top Batch D1) |
| **Experimentos in silico** | MD membrana POPC 20 ns OpenMM CUDA sobre CB1 5TGZ (`janus_md_memb20_d2_22`) |
| **Resultados clave** | TM6 RMSD mean 1.03±0.33 Å; COM TM3–TM6 **12.35** ≈ THC **12.06**, no THCV **13.07**; ángulo ~THC |
| **Archivos resultado** | `results/reports/md_d2_22_20ns_summary.md`; artefactos gitignored `results/md/membrane/JANUS_D2_22/` |
| **Commit NO-GO** | `485bb00` (2026-08-11) — “Document D2_22 biophysical NO-GO and pause toward Qiu pyrazole iteration” |
| **Por qué descartado** | **NO-GO de trinquete CB1** — no contención tipo THCV; Vina no predijo restricción |
| **Qué lo reemplazó** | Plan **pirazol Qiu** (`next_iter_pyrazole_qiu_plan.md`) |
| **NO-GO vs pausa** | **Lead = NO-GO científico definitivo** en docs de fallo. **GPU/MD pesada = pausada**. No es “paused lead”. |

---

## 6. Qiu / pirazol — nomenclatura y estado

### Compuestos publicados Qiu

| ID | Qué es | Verificado | No verificado | Conclusión local |
|----|--------|------------|---------------|------------------|
| **14** | Orto-morfolina + adamantil-carboxamida; highlight Yin-Yang | Identidad 0D YES; Fig.S5 CB1-ant+CB2-ago cualitativo | Ki/IC50/EC50/Emax OA; S173/S285 experimental | Janus **cualitativo** un lab; potencias **NOT FOUND OA** |
| **15** | Meta-morfolina | Identidad YES; paneles S11/S12 presentes | Fenotipo activo/inactivo; potencias | **NOT DETERMINABLE** pérdida vs 14 (`qiu_0q2f`) |
| **16** | Para-morfolina | Identidad YES; paneles S11–S13 | Idem | **NOT DETERMINABLE** |
| **20** | Orto-4-metilpiperazinilo | Identidad 0D YES | Farmacología OA | Identidad OK; potencia NF |
| **24** | Orto-morfolina + CH₂-adamantilo | Identidad 0D YES | Farmacología OA; “steric clash” = docking | Identidad OK; clash **COMP only** |

### IDs de panel / pasos proyecto

| ID | Representa | Estado documentado |
|----|------------|-------------------|
| **QIU_14** (Batch1) | Reconstrucción docking pre-0D (luego corregida carboxamida en 0D) | Rank-gate **fail** vs URB447 |
| **QIU_01/02/03** | Para / meta / sin morfolina (negativos/SAR) | Rank-gate **PASS** (proxy Vina ≠ α) |
| **0D** | Verificación estructural 14/15/20/24 | **PASS 4/4** |
| **0E–0L, 0N** | PDBQT/docking/pose/QC/hipótesis/CRO specs (commits en historial `qiu-protocol`) | **No en WT actual**; existen en historial de ramas |
| **0M** | Wet H1-a handoff | En **origin/master**; SMRF lo marca **RESERVE** |
| **0P** | Tabla evidencia externa primaria | En **origin/master** (autoridad vs Cursor-internal) |
| **0Q** | Destroy-hypothesis audit | **D NO-GO** path docking-NCE |
| **0Q-SMRF** | Matriz histórica molecular switch | **MODERATE**; **ACTIVE** |
| **0Q.1** | Audit A-pairs + Cursor vs Gemini | **EXPAND**; mono-CB2 YES; Yin-Yang NO |
| **0Q.2 / 0Q.2F** | Expand pares / regioisómeros 14–16 | 0Q.2F **untracked** en WT |

---

## 7. Tabla de decisiones científicas

| Fecha | Decisión | Objeto | Motivo | Evidencia | Estado |
|-------|----------|--------|--------|-----------|--------|
| 2026-08-06 | Congelar Norma L0 | Guía maestra Track1/2 | Separar discovery vs supply | `guia_maestra_*` | Vigente (parcialmente desfasada vs post-0Q) |
| 2026-08-06 | Novelty: concept=prior art | Janus×fibrosis | Literatura/patentes | `literatura_prioridad_y_novelty.md` | Vigente |
| 2026-08-09 | **NO-GO** | H1_02c / eje fitocannabinoide | MD POPC no gana vs THCV | `md_membrane_20ns_summary.md` | Cerrado |
| 2026-08-09/10 | **PIVOT** Option D | URB447 / Yin-Yang | Tras NO-GO H1 | `option_d_pivot_urb447.md`; `82ce0f5` | Histórico (luego D2_22 cerrado) |
| 2026-08-10 | Designar lead | JANUS_D2_22 | Top dual Vina | `e2e0fe9`; gate D1 | **Superseded** |
| 2026-08-11 | **NO-GO** lead | D2_22 | Trinquete CB1 fallido | `md_d2_22_20ns_summary.md`; `485bb00` | **Definitivo** |
| 2026-08-11 | **PAUSE** GPU/MD | Cómputo pesado | Post NO-GO | Mismos + `lecciones_*` | Vigente |
| 2026-08-11 | Activar Qiu docking | Pirazol Batch1 | Reemplazo D2_22 | `next_iter_*`; `57551db` | Histórico / tensionado por 0Q |
| 2026-08-11 | 0D PASS | Estructuras 14/15/20/24 | SI/figuras | `qiu_0d_*` | Vigente |
| 2026-08-13 | **D NO-GO** | Path docking-NCE Qiu | Prior art + gaps Qiu | `qiu_0q_independent_*` | Vigente para compute path |
| 2026-08-13 | SMRF ACTIVE / 0M RESERVE | Workstream B | Post-0Q | `qiu_0q_smrf_matrix.md` | Vigente en docs 0Q |
| 2026-08-15 | **EXPAND** | 0Q.1 A-pairs | Mono-CB2 real; no Yin-Yang law | `qiu_0q1_final_*` | Vigente |
| 2026-08-16/17 | GOLD=0; **PIPELINE STOP** | Round1 calibration | Primarios unrecovered | `ROUND1.9_*` | Vigente documental |
| 2026-08-17 | Soft-drug NO INTEGRABLE (fenotipo) | Sharma/Nikas/Kulkarni | Agonistas CB1 | `AUDIT_CONTROLLED_DEACTIVATION_*` | Vigente |

---

## 8. Inventario literario local (primarios ya hallados)

| Título / ancla | Autores (corto) | Año | DOI | Claim soportado en repo | Status |
|----------------|-----------------|-----|-----|-------------------------|--------|
| URB447 BMCL | LoVerme et al. | 2009 | 10.1016/j.bmcl.2008.12.059 | Primer Janus periférico CB1-ant/CB2-ago (IC50) | **REVIEW_REQUIRED** (Round1; no Gold) |
| GW405833 Neuropharmacology | Valenzano et al. | 2005 | 10.1016/j.neuropharm.2004.12.008 | Identidad + partial ago ~50% (abstract) | **REVIEW_REQUIRED** (PDF/tables NF) |
| AM1710 JMC | Khanolkar et al. | 2007 | 10.1021/jm070441u | 4b=AM1710; 5=AM1714 (abstract) | **REVIEW_REQUIRED** (Tables NF) |
| Two Janus Cannabinoids | Dhopeshwarkar et al. | 2017 | 10.1124/jpet.116.236539 | Relectura Janus GW/AM | Citado; no Gold lock |
| Qiu Yin-Yang Bioorg Chem | Qiu et al. | 2023 | 10.1016/j.bioorg.2023.106377 | Diseño pirazol; 14 cualitativo SI | Identidad **CONFIRMED** (SI); potencias **UNKNOWN**/NF OA |
| CB2 crystal 5ZTY | Li/Hua et al. | 2019 | 10.1016/j.cell.2018.12.011 | MRI2594/2687 switch mono-CB2 | **CONFIRMED** (0Q.1) |
| HU-308 → (R)-1 | Kosar et al. | 2024 | 10.1021/acscentsci.3c01461 | Switch mono-CB2 via phenyl | **CONFIRMED** (0Q.1) |
| Controlled-deactivation | Sharma / Nikas / Kulkarni | 2013/15/16 | 10.1021/jm4016075 etc. | Soft-drug THC/HHC; **ago CB1** | **CONFIRMED** fenotipo ago; **NO** Janus |
| HU-308 PNAS | Hanuš et al. | 1999 | 10.1073/pnas.96.25.14228 | CB2 ago tool | **REVIEW_REQUIRED** Gold |
| Vicasinabin Frontiers | Grether et al. | 2024 | 10.3389/fphar.2024.1426446 | hCB2 cAMP EC50 | **REVIEW_REQUIRED** |
| Olorinab ACS MCL | Han et al. | 2017 | 10.1021/acsmedchemlett.7b00396 | β-arrestin 6.2 nM | **REVIEW_REQUIRED** |
| WO2022026478 / US20230234928 | Makriyannis et al. | 2022/23 | (patentes) | Claims mixed CB1-ant/CB2-ago fibrosis | Inventario; ≠ FTO |

URLs adicionales en cada report citado; no se añaden búsquedas nuevas.

---

## 9. Gemini / Cursor — timeline (≠ evidencia primaria)

| Fecha | Evento | Path |
|-------|--------|------|
| ~2026-08-13 | Gemini paste usado en reconciliación 0Q.1 | Temp `Se ha pegado el markdown(4).md` (citado); resultado en `qiu_0q1_final_cursor_vs_gemini.md` — **acuerdo** Cursor=Gemini en A-pairs |
| 2026-08-16 | Round1.3: Gemini “AM1710/GW resolved” **rechazado** | `ROUND1.3_CROSS_VALIDATION.md` |
| 2026-08-17 | Round1.4–1.9: claims Gemini 5a / 11.2/89 / 14±2/48±4 → NOT_FOUND / REJECT | `ROUND1.4`…`ROUND1.9` |

**Regla documentada:** Gemini ≠ autoridad primaria.

---

## 10. Mapa de trazabilidad (conclusiones clave)

| Conclusión | Path | Commit / fecha | Sección |
|------------|------|----------------|---------|
| Hipótesis Janus inicial | `README.md`; `daaa269` | 2026-08-06 | README / initial |
| H1 NO-GO + pivot D | `md_membrane_20ns_summary.md`; `option_d_pivot_urb447.md` | `82ce0f5` | Go/no-go; Decisión |
| D2_22 NO-GO | `md_d2_22_20ns_summary.md` | `485bb00` 2026-08-11 | Veredicto frío; Análisis falla |
| Qiu reemplaza D2_22 | `next_iter_pyrazole_qiu_plan.md` | mismo commit | Por qué este eje |
| 0D estructuras | `qiu_0d_structure_verification.md` | `72ff659` | Tabla 0D |
| 0Q D NO-GO compute | `qiu_0q_independent_scientific_audit.md` | en `c43c0b7` | §0 / §13 |
| SMRF MODERATE + EXPAND | `qiu_0q_smrf_matrix.md`; `qiu_0q1_final_*` | `c43c0b7` | Status lock; §5 |
| GOLD=0 STOP | `ROUND1.9_MASTER_EVIDENCE_STATE.md` | untracked 2026-08-17 | §3E |
| Soft-drug ≠ Janus | `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` | untracked 2026-08-17 | §1 |

---

## 11. CONFLICTOS DETECTADOS (sin resolver)

1. **`docs/criterio_exito_janus.md` + `docs/mapa_ligandos_janus_cb1_cb2.md`** aún presentan D2_22 como lead con “no-go trinquete / **go exploratorio débil**” vs **`md_d2_22_20ns_summary.md` / `lecciones_aprendidas_track1.md` / `option_d_pivot_urb447.md` / commit `485bb00`**: D2_22 **descartado**, go exploratorio **superseded**.
2. **`docs/quimioma_cannabico_cb1_cb2.md`** mantiene norte **cannabis-first THCV** vs **`guia_maestra_*` / pivot Option D / lecciones**: norte sintético post H1 NO-GO.
3. **`qiu_0q_independent_*` = D NO-GO** path docking-NCE vs **`next_iter_pyrazole_qiu_plan.md` / lecciones** (eje Qiu docking activo) vs **`origin/master` 0M CRO H1-a** (paquete wet) vs **SMRF: 0M=RESERVE**.
4. **Round1.9 PIPELINE STOP** (17 ago) vs workstream **0Q-SMRF ACTIVE / EXPAND** (15 ago) — ambos documentales, pero distintos “próximos pasos” explícitos.
5. **DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX.md** (17 ago) dice soft-drug **NOT_IN_LOCAL_CORPUS** vs **`AUDIT_CONTROLLED_DEACTIVATION_*`** (mismo día) que llena el gap con Sharma/Nikas/Kulkarni.
6. **Gemini Round1 “resolved”** vs **Cursor Round1.3–1.9 REVIEW_REQUIRED** (conflicto explícitamente registrado, no “votado”).

---

## 12. Único siguiente paso recomendado (solo desde estado documentado)

**Recuperar / anclar en el working tree las fuentes primarias que bloquean Round1.9 (PDF/tablas Valenzano; Tables 1–2 Khanolkar; potencias OA Qiu 14/15/16/20/24) y/o completar el EXPAND literario 0Q-SMRF — sin reabrir docking, MD, NCE ni promoción Gold.**

Justificación: `ROUND1.9` §3E fija **PIPELINE = STOP** para cómputo; `qiu_0q1_final_*` fija **EXPAND** = literatura/claim-framing only; `qiu_0q_smrf_matrix.md` marca SMRF **ACTIVE** y 0M **RESERVE**.

---

*Fin inventario `JANUSFORGE_RECOVERED_RESEARCH_STATE.md`.*
