# JANUSFORGE — Resumen ejecutivo de investigación

**Tipo:** síntesis ejecutiva (no bitácora; no informe científico primario)  
**Fecha:** 2026-08-17  
**Autoridad:** `docs/JANUSFORGE_RESEARCH_STATE.md` · `results/reports/JANUSFORGE_RECOVERED_RESEARCH_STATE.md` · `results/reports/JANUS_DECISION_LEDGER_v1.0.md` · `results/reports/JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md`  
**HEAD de referencia (decisiones científicas):** `c43c0b7` — *Add 0Q SMRF and 0Q.1 scientific audit*  
**Regla de lectura:** cada estado operativo exige fuente (path + commit cuando tracked). Los conflictos listados **no están resueltos** en este documento.

---

## 1. Qué es Janusforge y la pregunta científica

**Janusforge** es un programa de descubrimiento computacional orientado a ligandos *Yin-Yang* (“Janus cannabinoids”): compuestos **monomoleculares** con perfil dual **CB1 antagonista + CB2 agonista**, con brújula inicial cannabis-first (THCV como PoC imperfecto) y filtro de indicación **fibrosis** (IPF como gate *después* de un perfil de receptor limpio).

**Pregunta científica central:** ¿Existe —y puede priorizarse computacionalmente— un ligando monomolecular con perfil CB1-ant / CB2-ago útil en fibrosis, con filtro de indicación (p. ej. IPF) **después** de un perfil de receptor limpio?

**Fuentes:** `README.md` · `docs/guia_maestra_biotecnologia_quimiotipos.md` · commit `daaa269` (2026-08-06).

La pregunta evolucionó en tres capas documentadas:

| Capa | Contenido | Fuente |
|------|-----------|--------|
| **Diseño / NCE** | ¿Janusforge como motor docking/MD/NCE puede inventar o priorizar un Janus novedoso? | `results/reports/qiu_0q_independent_scientific_audit.md` · `c43c0b7` |
| **Mecanismo / precedentes** | ¿Qué pares históricos sostienen un “switch” estructural reproducible (mono-CB2 vs fenotipo Janus dual)? | `results/reports/qiu_0q_smrf_matrix.md` · `results/reports/qiu_0q1_final_cursor_vs_gemini.md` · `c43c0b7` |
| **Calibración documental** | ¿Qué precedentes Janus tienen identidad + número primario recuperado en corpus local? | `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` · untracked 2026-08-17 |

---

## 2. Hipótesis original

| Elemento | Contenido | Fuente |
|----------|-----------|--------|
| **Norte químico inicial** | Cannabis-first: Δ9-**THCV** como PoC imperfecto + análogos THCV-like (H1–H5) | `docs/quimioma_cannabico_cb1_cb2.md` |
| **Comparador** | URB447 = design comparator, no norte inicial | Idem |
| **Arquitectura normativa** | CB1-ant + CB2-ago; fibrosis = gate posterior | `docs/guia_maestra_biotecnologia_quimiotipos.md` · `daaa269` |
| **White space declarado (2026-08-06)** | Concepto Janus×fibrosis = prior art; núcleo defendible = NCE periférico + datos IPF | `docs/literatura_prioridad_y_novelty.md` |

**Tres “conmutadores” distintos (no fusionar):**

| Uso | Significado | Fuente |
|-----|-------------|--------|
| Flip THCV | Signo CB1 dosis/ocupación-dependiente | `docs/mecanismo_flip_thcv_cb1.md` |
| Switch Qiu | N1-orto-morfolina como interruptor Yin-Yang en pirazol | Qiu 2023 SI; `qiu_0d_structure_verification.md` · `72ff659` |
| SMRF | Cambio de eficacia (p. ej. CB2 ago↔inv) ≠ ley dual CB1/CB2 | `qiu_0q_smrf_matrix.md` · `c43c0b7` |

---

## 3. Trayectoria A → J

| Etapa | Qué pasó | Fuente | Commit |
|-------|----------|--------|--------|
| **A** Hipótesis inicial | Janus monomolecular × fibrosis | `README.md` | `daaa269` |
| **B** THCV / H1–H5 | Serie fitocannabinoide; lead proxy H1_02c | `results/reports/md_membrane_20ns_summary.md` | `2abb3c3` |
| **C** Option D / URB447 | Pivot sintético post H1 NO-GO | `results/reports/option_d_pivot_urb447.md` | `82ce0f5` |
| **D** D2_22 | Designado lead docking (dual Vina top) | `results/reports/option_d_batch_d1_gate_summary.md` | `e2e0fe9` |
| **E** NO-GO D2_22 | Trinquete CB1 fallido; MD pesada pausada | `results/reports/md_d2_22_20ns_summary.md` | `485bb00` |
| **F** Qiu | Plan pirazol + Batch1 docking light; 0D estructuras PASS | `next_iter_pyrazole_qiu_plan.md`; `qiu_0d_structure_verification.md` | `57551db` / `72ff659` |
| **G** 0Q | **D NO-GO** path docking/NCE anclado Qiu | `qiu_0q_independent_scientific_audit.md` | `c43c0b7` (1ª `d0e483f`) |
| **H** 0Q-SMRF | Matriz switch histórica; Option B **ACTIVE**; 0M **RESERVE** | `qiu_0q_smrf_matrix.md` | `c43c0b7` |
| **I** 0Q.1 | **EXPAND** literatura; mono-CB2 YES; Yin-Yang law NO | `qiu_0q1_final_cursor_vs_gemini.md` | `c43c0b7` |
| **J** Round1 | Calibración documental GOLD=0; **PIPELINE STOP** (scope Round1) | `ROUND1.9_MASTER_EVIDENCE_STATE.md` | untracked |

---

## 4. Líneas principales investigadas

| Fase / eje | Objetos y alcance | Fuente |
|------------|-------------------|--------|
| **H1–H5 fitocannabinoide** | Serie THCV-like; lead proxy **JANUS_H1_02** → **JANUS_H1_02c**; controles Δ9-THCV, Δ9-THC | `JANUSFORGE_RECOVERED_RESEARCH_STATE.md` §3D; `md_membrane_20ns_summary.md` |
| **Option D / URB447** | Panel **JANUS_D2_***; lead **JANUS_D2_22** (Bz_pCF3); runners D2_05/10/15/29; semilla URB447 | `option_d_pivot_urb447.md`; `option_d_batch_d1_gate_summary.md` |
| **Qiu pirazol (docking light)** | **QIU_14**, QIU_01–07 + refs URB447/GW/THCV/THC; compuestos publicados 14, 15, 16, 20, 24 (0D PASS) | `next_iter_pyrazole_qiu_plan.md`; `qiu_0d_structure_verification.md` · `72ff659` |
| **0Q destroy-hypothesis** | ¿Path compute Janusforge anclado Qiu-14 es viable? | `qiu_0q_independent_scientific_audit.md` · `c43c0b7` |
| **0Q-SMRF / 0Q.1** | Matriz switch histórico; A-pairs MRI2687/MRI2594; HU-308 / ago-3 / (R)-1; claim-split mono-CB2 vs Yin-Yang | `qiu_0q_smrf_matrix.md`; `qiu_0q1_final_cursor_vs_gemini.md` |
| **Round1 calibración** | 9 precedentes Janus en **REVIEW_REQUIRED** (AM1710, GW405833, CP-55,940, HU-308, Vicasinabin/RG7774, APD371/Olorinab, WIN 55,212-2, LEI-101, URB447) | `ROUND1.9_MASTER_EVIDENCE_STATE.md` §3B |
| **Soft-drug Makriyannis** | Sharma 2013 / Nikas 2015 / Kulkarni 2016 — integración fenotipo vs ADME | `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` |
| **Precedentes mapa** | URB447, GW405833, AM1710, Qiu-14 | `docs/mapa_ligandos_janus_cb1_cb2.md` |

---

## 5. Descartes definitivos (con motivo)

| Objeto | Veredicto | Motivo | Fuente | Commit |
|--------|-----------|--------|--------|--------|
| **H1_02c** / eje fitocannabinoide | **NO-GO** | No gana vs THCV en POPC 20 ns (gates plan) | `md_membrane_20ns_summary.md` | pivot `82ce0f5` |
| **JANUS_D2_22** como lead funcional | **NO-GO** | COM TM3–TM6 ≈ THC (12.35 vs 12.06 Å), no contención THCV; Vina no predice trinquete | `md_d2_22_20ns_summary.md` | `485bb00` |
| Path **docking/MD/NCE** Janusforge anclado Qiu | **D NO-GO** | Prior art Janus desde 2009; Qiu sin potencias OA; compute prematuro | `qiu_0q_independent_scientific_audit.md` §0/§13 | `c43c0b7` |
| Soft-drug → fenotipo **Janus** | **NO INTEGRABLE** | Leads Sharma/Nikas/Kulkarni = agonistas CB1 | `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` | untracked |
| Soft-drug → **ADME** | **CONDICIONAL** | DoA / ester→ácido documentados; dimensión distinta al fenotipo | Idem | untracked |

**No son “descartados”:** gaps potencias Qiu OA, tablas Valenzano/Khanolkar unrecovered, 0M RESERVE, EXPAND literario — son *no demostrado / pendiente*, no NO-GO del espacio fibrosis (`JANUSFORGE_RECOVERED_RESEARCH_STATE.md` §4F).

---

## 6. Estado científico actual

### Evidencia sólida documentada

| Hallazgo | Soporte | Fuente |
|----------|---------|--------|
| Perfil Janus CB1-ant/CB2-ago **existe** en literatura (multi-scaffold) | URB447 IC50; GW/AM1710 relectura; Qiu-14 cualitativo SI | `qiu_0q_smrf_matrix.md` · LoVerme 2009; Dhop 2017; Qiu 2023 |
| Switch **mono-CB2** ago↔inv **reproducible** (Class A) | MRI2687↔MRI2594 Fig. 6; ago-3→(R)-1 Tables 3–4 | `qiu_0q1_final_cursor_vs_gemini.md` · PMC6713262; PMC11117691 |
| **NO** ley estructural Yin-Yang universal dual CB1/CB2 | A-pairs confirman mono-CB2; CB1 permanece ago-class en MRI | `qiu_0q1_final_cursor_vs_gemini.md` §3–§5 |
| Identidades Qiu 14/15/20/24 verificadas (0D) | SI/figuras locales | `qiu_0d_structure_verification.md` · `72ff659` |
| Concepto Janus×fibrosis = prior art (2026-08-06) | Patentes + literatura | `docs/literatura_prioridad_y_novelty.md` |
| NO-GO trinquete D2_22 = autoridad operativa | MD 20 ns métricas frías | `md_d2_22_20ns_summary.md` · `485bb00` |
| 0Q D NO-GO compute = autoridad operativa | Destroy-hypothesis audit | `qiu_0q_independent_scientific_audit.md` · `c43c0b7` |

### Incertidumbres abiertas

| Área | Qué falta | Fuente |
|------|-----------|--------|
| Potencias Qiu 14/15/16/20/24 | Ki/IC50/EC50/Emax OA **NOT FOUND** | `qiu_0q_independent_scientific_audit.md`; `qiu_0q_smrf_matrix.md` §Hypothesis table |
| SAR regioisómeros Qiu 14 vs 15/16 | Fenotipo activo/inactivo **NOT DETERMINABLE** sin PDF | `JANUSFORGE_RECOVERED_RESEARCH_STATE.md` §6 |
| Precedentes Janus en corpus | **GOLD_CONFIRMED = 0**; 9 en **REVIEW_REQUIRED** | `ROUND1.9_MASTER_EVIDENCE_STATE.md` §3A–3B |
| PDF/tablas primarias | Khanolkar Tables 1–2; Valenzano PDF/Fig.1 **NOT_FOUND** | `ROUND1.5_*`; `ROUND1.6_*`–`ROUND1.8_*` |
| Mecanismo Qiu S173/S285 | Solo docking/MD (**COMPUTATIONAL**) | `qiu_0q_smrf_matrix.md` |
| Co-cristales switch A-pairs | MRI / (R)-1 co-crystal **NOT FOUND** | `qiu_0q1_final_cursor_vs_gemini.md` §6 |
| Wet H1-a (0M) | Handoff **ausente en HEAD**; RESERVE en master | Supersession Audit **U2**; `origin/master` |

---

## 7. Mapa de estados operativos

### CURRENT (decisiones vigentes)

| Dominio | Estado | Fuente | Commit |
|---------|--------|--------|--------|
| D2_22 lead | **NO-GO** | `md_d2_22_20ns_summary.md` | `485bb00` |
| 0Q compute / docking / NCE | **NO-GO** (path) | `qiu_0q_independent_scientific_audit.md` | `c43c0b7` |
| 0Q-SMRF | **ACTIVE** / **MODERATE** | `qiu_0q_smrf_matrix.md` | `c43c0b7` |
| 0Q.1 | **EXPAND** (literatura only) | `qiu_0q1_final_cursor_vs_gemini.md` | `c43c0b7` |
| 0M wet H1-a | **RESERVE** (no critical path) | `qiu_0q_smrf_matrix.md` (+ handoff `@ origin/master`) | `c43c0b7` |
| Round1 calibración | **STOP** (GOLD=0) | `ROUND1.9_MASTER_EVIDENCE_STATE.md` §3E | untracked |
| H1/membrana | **NO-GO** eje prioritario | `md_membrane_20ns_summary.md` | `2abb3c3` |
| Soft-drug fenotipo | **NO INTEGRABLE** | `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` | untracked |
| Soft-drug ADME | **CONDICIONAL** | Idem | untracked |

### CONFLICT (sin cierre documental — no resueltos aquí)

| ID | Par | Fuente |
|----|-----|--------|
| **C1** | `next_iter_pyrazole_qiu_plan.md` ACTIVE docking (`57551db`) vs 0Q D NO-GO (`c43c0b7`) | `JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md` §5 |
| **C2** | Soft “lead / go exploratorio débil” D2_22 vs MD NO-GO | `docs/criterio_exito_janus.md`; `docs/mapa_ligandos_janus_cb1_cb2.md` vs `485bb00` |
| **C3** | Cannabis-first (`quimioma_*`) vs norte sintético post-H1 | `JANUSFORGE_RECOVERED_RESEARCH_STATE.md` §11 #2 |
| **C4** | `DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX.md` NOT_IN_CORPUS vs audit soft-drug que llena gap | Recovered State §11 #5 |
| **C5** | Gemini Round1 “resolved” vs Cursor REVIEW_REQUIRED | `ROUND1.3_CROSS_VALIDATION.md`; Recovered State §11 #6 |

### UNRESOLVED (ámbitos distintos; no inferir supersesión)

| ID | Par | Fuente |
|----|-----|--------|
| **U1** | Round1.9 **PIPELINE STOP** vs 0Q-SMRF **ACTIVE** / 0Q.1 **EXPAND** | Scopes distintos; Supersession Audit §5 |
| **U2** | Autoridad 0M handoff en HEAD actual | Archivo ausente WT; RESERVE en `origin/master` |

### RESERVE / EXPAND / STOP (workstreams)

| Workstream | Estado | Alcance | Fuente |
|------------|--------|---------|--------|
| **0Q-SMRF** | **ACTIVE** / **MODERATE** | Matriz histórica molecular switch; **sin** docking/NCE/MD | `qiu_0q_smrf_matrix.md` · `c43c0b7` |
| **0Q.1** | **EXPAND** | Literatura / claim-split; mono-CB2 YES; Yin-Yang law NO | `qiu_0q1_final_cursor_vs_gemini.md` · `c43c0b7` |
| **0M wet H1-a** | **RESERVE** | No critical path; requiere decisión formal para salir de RESERVE | SMRF status lock; handoff `@ origin/master` |
| **Round1 recovery** | **STOP** (compute) | Recuperar primarios; **no** promover Gold | `ROUND1.9_MASTER_EVIDENCE_STATE.md` |

### HISTORICAL (trazabilidad; ≠ instrucción operativa)

| Item | Fuente | Commit |
|------|--------|--------|
| 0M = **BLOCKED** | `qiu_0m_h1a_wet_handoff.md` | `db46e9a` — **SUPERSEDED** por RESERVE |
| Qiu docking ACTIVE pre-0Q | `next_iter_pyrazole_qiu_plan.md` | `57551db` — contenido sin patch post-0Q |
| D2_22 designado lead | gate D1 | `e2e0fe9` — **SUPERSEDED** por NO-GO |

---

## 8. Qué significa Round1 STOP y por qué Janusforge entero NO está detenido

**Round1 STOP** = **PIPELINE STOP** de la *calibración documental Gold* (scope Round1): **GOLD_CONFIRMED = 0**; **9** precedentes en **REVIEW_REQUIRED**; prohibido promover Gold sin primario recuperado; prohibido cómputo/candidatos nuevos *en ese pipeline*.

**Fuente:** `ROUND1.9_MASTER_EVIDENCE_STATE.md` §3E · `docs/JANUSFORGE_RESEARCH_STATE.md` §10.

**Esto NO significa “Janusforge entero detenido”.** Round1 STOP acota la calibración documental Gold. En paralelo, tracked post-0Q: **0Q-SMRF ACTIVE** y **0Q.1 EXPAND** (literatura only). La relación Round1↔SMRF = **U1** (UNRESOLVED; no fusionar scopes).

Un lector que lea solo Round1.9 podría concluir parada total del programa; la bitácora maestra y este resumen aclaran que el stop es **scope-local** a Round1, no program-wide.

---

## 9. Líneas cerradas

Sin nueva decisión formal + commit, **no reabrir** (`docs/JANUSFORGE_RESEARCH_STATE.md` §7):

1. H1_02c / eje fitocannabinoide como lead Track1 — `md_membrane_20ns_summary.md`
2. JANUS_D2_22 como lead funcional — `md_d2_22_20ns_summary.md` / `485bb00`
3. Janusforge como motor **docking / MD / NCE** anclado Qiu-14 — `qiu_0q_independent_scientific_audit.md` / `c43c0b7`
4. Soft-drug Makriyannis como **path fenotipo Janus** (ADME sigue CONDICIONAL, dimensión distinta) — `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md`
5. Promoción **REVIEW_REQUIRED → GOLD** sin primario recuperado — Round1.9

**Cerrado como frontier de diseño compute:** docking/NCE/MD campaigns (0Q D NO-GO + bans SMRF/0Q.1).

---

## 10. Líneas abiertas

| Workstream | Estado | Alcance permitido | Fuente |
|------------|--------|-------------------|--------|
| **0Q-SMRF** | ACTIVE / MODERATE | Matriz histórica molecular switch; **sin** docking/NCE/MD | `qiu_0q_smrf_matrix.md` · `c43c0b7` |
| **0Q.1** | EXPAND | Literatura / claim-split; mono-CB2 YES; Yin-Yang law NO | `qiu_0q1_final_cursor_vs_gemini.md` · `c43c0b7` |
| **Round1 recovery** | STOP (compute) | Recuperar primarios; no promover Gold | `ROUND1.9_MASTER_EVIDENCE_STATE.md` |
| **0M wet H1-a** | RESERVE | No critical path; requiere decisión formal para salir de RESERVE | SMRF status lock; handoff `@ origin/master` |

**Frontier documentada:** ¿Qué pares históricos sostienen switch mono-CB2 vs fenotipo Janus Class-B, con claim-split estricto? — `qiu_0q_smrf_matrix.md`; `qiu_0q1_final_cursor_vs_gemini.md`.

---

## 11. Próximos pasos documentales (solo respaldados)

### A. Recuperación documental (Round1 scope)
- Anclar PDF/tablas Valenzano; Tables 1–2 Khanolkar; potencias OA Qiu 14/15/16/20/24
- **No** promover Gold; **no** cómputo en pipeline Round1
- Fuente: `ROUND1.9_MASTER_EVIDENCE_STATE.md`; Recovered State §12

### B. Expansión SMRF / 0Q.1
- Completar matriz / claim-split mono-CB2 vs Yin-Yang; cerrar gaps OA Qiu
- **Sin** NCE / docking / MD
- Fuente: `qiu_0q1_final_*`; `qiu_0q_smrf_matrix.md`

### C. Experimental futuro
- **0M = RESERVE** — no arrancar wet H1-a como ruta crítica mientras SMRF corre
- Cualquier wet futuro requiere decisión formal (handoff en master; gap U2 en HEAD)
- Fuente: `qiu_0q_smrf_matrix.md`

**No** listar docking/MD/NCE como “siguiente acción” (fuentes lo prohíben).

---

## 12. Prohibiciones operativas

1. **No** docking / MD / NCE / QSAR / modelado nuevo como siguiente paso programático (`qiu_0q_independent_scientific_audit.md`; bans SMRF/0Q.1; Round1.9 §3E).
2. **No** reabrir NO-GO (H1, D2_22, path compute Qiu) sin decisión explícita + commit.
3. **No** promover **REVIEW_REQUIRED → GOLD** sin primario recuperado (`ROUND1.9`).
4. **No** resolver CONFLICTOs C1–C5 por inferencia — marcar hasta patch explícito (`JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md`).
5. **No** tratar Gemini/Cursor como evidencia primaria (`ROUND1.3_*`; Recovered State §9).
6. **No** fusionar dimensiones soft-drug: fenotipo NO INTEGRABLE ≠ ADME CONDICIONAL (`AUDIT_CONTROLLED_DEACTIVATION_*`).
7. **No** confundir flip THCV, switch Qiu y SMRF como un solo “conmutador” (Recovered State §3C).
8. **No** usar docs legacy con soft “lead D2_22 / go exploratorio débil” como autoridad operativa (`485bb00` prevalece).
9. **No** nueva investigación, docking/MD/NCE, ni conversión REVIEW_REQUIRED → CONFIRMED en este resumen.

---

## 13. Mapa de fuentes (paths y commits)

| Decisión | Path | Commit | Estado |
|----------|------|--------|--------|
| Mission / hipótesis Janus | `README.md`; `docs/guia_maestra_biotecnologia_quimiotipos.md` | `daaa269` | CURRENT (misión) |
| H1_02c NO-GO | `results/reports/md_membrane_20ns_summary.md` | `2abb3c3` / pivot `82ce0f5` | CURRENT |
| D2_22 NO-GO | `results/reports/md_d2_22_20ns_summary.md` | `485bb00` | CURRENT |
| Soft D2_22 “go exploratorio” | `docs/criterio_exito_janus.md`; `docs/mapa_ligandos_janus_cb1_cb2.md` | pre/`57551db` | **CONFLICT** vs MD |
| next_iter Qiu ACTIVE docking | `results/reports/next_iter_pyrazole_qiu_plan.md` | `57551db` | **CONFLICT** vs 0Q |
| 0Q D NO-GO compute | `results/reports/qiu_0q_independent_scientific_audit.md` | `c43c0b7` | CURRENT |
| 0Q-SMRF ACTIVE/MODERATE; 0M RESERVE | `results/reports/qiu_0q_smrf_matrix.md` | `c43c0b7` | CURRENT |
| 0M = BLOCKED (histórico) | `qiu_0m_h1a_wet_handoff.md` @ `db46e9a` | `db46e9a` | HISTORICAL (≠ CURRENT) |
| 0Q.1 EXPAND | `results/reports/qiu_0q1_final_cursor_vs_gemini.md` | `c43c0b7` | CURRENT |
| Round1 STOP; GOLD=0; REVIEW=9 | `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` | untracked | CURRENT *scope Round1* |
| Soft-drug fenotipo / ADME | `results/reports/AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` | untracked | CURRENT |
| Bitácora maestra | `docs/JANUSFORGE_RESEARCH_STATE.md` | `a010385` | CURRENT (mapa) |
| Inventario / ledger / supersesión | `JANUSFORGE_RECOVERED_RESEARCH_STATE.md`; `JANUS_DECISION_LEDGER_v1.0.md`; `JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md` | reports/ | Mapas de autoridad |

---

## 14. Estado Git conocido (snapshot al crear este doc)

| Ítem | Valor |
|------|--------|
| **HEAD** | `a010385` — *docs: add master research state log* (`docs/JANUSFORGE_RESEARCH_STATE.md`) |
| **origin/master** | `8d3a34a` — Merge PR #6 (incluye PR5) |
| **Decisions científicas post-0Q** | Commit `c43c0b7` (0Q + SMRF + 0Q.1) — autoridad para veredictos CURRENT |
| **Staged / unstaged diff** | Vacío en tracked (según Recovered State §1) |

### Material relevante ausente o untracked en HEAD

| Categoría | Ejemplos | Implicación |
|-----------|----------|-------------|
| **En `origin/master`, no en WT @ HEAD** | `qiu_0m_h1a_wet_handoff.md`, `qiu_0p_external_evidence_table.md`, `janusforge_dossier_estado_programa.md`, `cro_package_h1a/SEND/*` | Memoria post-0D parcial; gap **U2** |
| **Untracked reports (17 ago)** | `ROUND1.9_*`, `AUDIT_CONTROLLED_DEACTIVATION_*`, `DOCUMENTARY_CB_*`, `JANUSFORGE_RECOVERED_*`, `JANUSFORGE_SUPERSESSION_*`, `JANUS_DECISION_LEDGER_*` | Calibración Gold y audits no versionados en HEAD |
| **Untracked data** | `data/papers/**` (SI Qiu, OCR, soft-drug extracts, API JSON) | Primarios locales no en git |
| **Artefactos MD gitignored** | `results/md/membrane/` | Métricas D2_22/H1 no reproducibles desde git alone |
| **Decision Ledger Audit v1.0** | No hay archivo en repo | Clasificaciones SUPERSEDED/UNRESOLVED citadas en Supersession Audit §6 |

→ Un externo debe confirmar qué commit/rama usar como autoridad única (`a010385` vs `8d3a34a` vs `c43c0b7` para decisiones científicas).

---

## 15. Lectura mínima para retomar el proyecto

1. `docs/JANUSFORGE_RESEARCH_STATE.md` (mapa maestro)
2. Este resumen (`docs/JANUSFORGE_RESEARCH_EXECUTIVE_SUMMARY.md`)
3. `results/reports/JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md`
4. `results/reports/JANUS_DECISION_LEDGER_v1.0.md`
5. Veredictos CURRENT: `md_d2_22_20ns_summary.md`; `qiu_0q_independent_scientific_audit.md`; `qiu_0q_smrf_matrix.md`; `qiu_0q1_final_cursor_vs_gemini.md`; `ROUND1.9_MASTER_EVIDENCE_STATE.md`
6. Solo como fuentes CONFLICT: `docs/criterio_exito_janus.md`; `docs/mapa_ligandos_janus_cb1_cb2.md`; `next_iter_pyrazole_qiu_plan.md`

**No** empezar por Gemini pastes ni por docs con soft “lead D2_22 / go exploratorio débil” como si fueran CURRENT.

---

*Fin síntesis ejecutiva. Derivado de bitácora maestra y documentos de autoridad; no sustituye informes primarios. Conflictos C1–C5 y UNRESOLVED U1–U2 permanecen abiertos.*
