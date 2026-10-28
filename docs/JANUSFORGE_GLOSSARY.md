# JANUSFORGE — Glosario metodológico y técnico

**Tipo:** referencia normativa de lectura (no informe científico)  
**Fecha:** 2026-08-18  
**Autoridad de mapeo:** `docs/JANUSFORGE_RESEARCH_STATE.md` · `results/reports/JANUS_DECISION_LEDGER_v1.0.md` · commit `c43c0b7` (decisiones post-0Q)  
**Prohibiciones de este doc:** sin nueva investigación química; sin alterar estados de compuestos; sin resolver conflictos C1–C5.

---

## 1. Acrónimos operativos y metodológicos (0M, 0Q, SMRF, Level 0)

### Definiciones metodológicas (intención PI)

| ID | Expansión | Definición |
|----|-----------|------------|
| **0M** | Zero Mechanistic Assumption | No asumir acoplamientos, sesgo de señalización ni conformaciones activas/inactivas sin evidencia biofísica directa en el ensayo correspondiente. |
| **0Q** | Zero Quality Compromise / Zero Quantity Inflation | No inflar datasets con datos ruidosos, secundarios o agregados; preferir un dato atómico verificable sobre volumen. |
| **SMRF** | Selectivity & Metabolic Restriction Filters / Framework | Filtros secuenciales de diseño/selección: exclusión SNC, cinética soft-drug, selectividad de blanco limpia, antes de filtrado fenotípico. |
| **Level 0** | Nivel 0 / Norma L0 | Falsificación documental directa contra PDF/tablas primarias; sin transcripciones de terceros, ChEMBL no auditado ni texto LLM como fuente primaria. |

### Uso documentado en el corpus Janusforge (CURRENT)

En informes tracked post-0Q (`c43c0b7`), los mismos identificadores aparecen con alcance distinto al de las definiciones metodológicas anteriores. Esta subsección registra ese uso **sin** declarar cuál sentido prevalece.

| ID | Uso en corpus CURRENT | Fuente | Commit / nota |
|----|----------------------|--------|---------------|
| **0M** | Workstream wet **H1-a** (Option A); estado operativo **RESERVE** (no critical path). Histórico **BLOCKED** @ `db46e9a` en `qiu_0m_h1a_wet_handoff.md` = HISTORICAL (≠ CURRENT). | `results/reports/qiu_0q_smrf_matrix.md`; handoff `@ origin/master` (ausente en HEAD → U2) | `c43c0b7` |
| **0Q** | Auditoría científica independiente → veredicto **D NO-GO** del path docking/MD/NCE anclado Qiu-14. | `results/reports/qiu_0q_independent_scientific_audit.md` | `c43c0b7` (1ª `d0e483f`) |
| **0Q-SMRF / SMRF** | Matriz histórica de “molecular switch” (mono-CB2 vs fenotipo Yin-Yang dual); Option B **ACTIVE** / **MODERATE**; **sin** reopen docking/NCE/MD. | `results/reports/qiu_0q_smrf_matrix.md` | `c43c0b7` |
| **0Q.1** | Expansión literaria / claim-split; mono-CB2 YES; Yin-Yang law NO. | `results/reports/qiu_0q1_final_cursor_vs_gemini.md` | `c43c0b7` |
| **Level 0** | Certificación documental Round1: `LEVEL0_CONFIRMED = 0`; compuestos foco en **REVIEW_REQUIRED**. | `results/reports/ROUND1_LEVEL0_CERTIFICATION_v1.0.md`; `ROUND1.9_MASTER_EVIDENCE_STATE.md` | untracked 2026-08-17 |

**Nota de lectura:** Recovered State §3C distingue tres “conmutadores” no intercambiables: flip THCV, switch Qiu (N1-orto-morfolina), SMRF (cambio de eficacia p. ej. CB2 ago↔inv ≠ ley dual CB1/CB2).

---

## 2. Categorías oficiales del estado de evidencia

Estados usados en la calibración documental Round1 y en informes de auditoría. Preferir **REVIEW_REQUIRED** sobre promoción falsa.

| Categoría | Definición |
|-----------|------------|
| **PRIMARY_VERIFIED** | Identidad del compuesto **y** dato cuantitativo relevante recuperados del primario (PDF/tabla/figura) con ubicación exacta verificable en el documento fuente. |
| **PRIMARY_PARTIAL** | Elementos primarios recuperados de forma incompleta (p. ej. solo abstract, binding sin fila funcional homogénea, tabla citada pero no abierta). |
| **REVIEW_REQUIRED** | Bloqueo documentado impide promoción; el compuesto permanece en revisión hasta cerrar identidad, ensayo, especie, Emax o estructura. |
| **CONTRADICTED** | El primario recuperado demuestra misasignación de fila/columna, especie, ensayo o normalización respecto al claim auditado. |
| **GOLD_CONFIRMED** | Pasa simultáneamente identidad primaria, dato cuantitativo, bloqueos de ensayo/homogeneidad y reglas Level 0 / Subset A–B exigidas por Round1. |
| **BLINDED / QUARANTINE** | Dato retenido fuera del pipeline de promoción: cuarentena histórica (`QUARANTINE_LOG.md`), holds Q11-*, o compuestos Qiu en estado **QIU_BLINDED** / HOLD hasta verificación primaria. |

**Estado consolidado Round1.9 (2026-08-17):** `GOLD_CONFIRMED = 0`; **9** compuestos Janus-relevantes en **REVIEW_REQUIRED** (AM1710, GW405833, CP-55,940, HU-308, Vicasinabin/RG7774, APD371/Olorinab, WIN 55,212-2, LEI-101, URB447). Fuente: `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` §3A–3B.

---

## 3. Términos farmacológicos y de ensayo

### Subset A / Subset B

Subconjuntos de **homogeneidad de ensayo** para comparación cuantitativa (Round1 stratification). cAMP ≠ GTPγS; preferir subconjunto vacío a homogeneidad falsa.

| Subset | Criterio simultáneo (resumen) |
|--------|-------------------------------|
| **Subset A** | hCB2 + cAMP funcional + células intactas comparables + EC50 explícito + Emax explícito y trazable + primario verificado + ubicación fuente verificable. **Sin** GTPγS. |
| **Subset B** | hCB2 + [³⁵S]GTPγS + preparación identificada + EC50/métrica funcional explícita + Emax explícito + primario verificable. AM1710 solo aquí *si* califica — nunca como equivalente cAMP. |

Estado Round1: Subset A = **0** confirmados; Subset B = **0** confirmados. Fuente: `results/reports/ROUND1_ASSAY_STRATIFICATION_v1.0.md`.

### Janus / Janus Ligand

Ligando **monomolecular** con perfil dual normativo **CB1 antagonista + CB2 agonista** (“Yin-Yang” / “Janus cannabinoid”). No confundir con combo de dos fármacos (p. ej. AM6545 + AM1241) ni con flip dosis-dependiente de THCV. Filtro de indicación fibrosis (IPF) = gate **posterior** al perfil de receptor. Fuente misión: `README.md`; `docs/guia_maestra_biotecnologia_quimiotipos.md`.

### Controlled Deactivation / soft-drug

Estrategia de **desactivación controlada** (serie Makriyannis): éster carboxílico lábil → metabolito ácido inactivo; duración de acción modulable. En corpus Janusforge, dimensión **fenotipo Janus** (CB1-ant/CB2-ago) auditada como **NO INTEGRABLE** para leads Sharma/Nikas/Kulkarni (agonistas CB1); dimensión **ADME** = **CONDICIONAL** (distinta). Fuente: `results/reports/AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md`. **Soft-drug** ≠ automáticamente periferia SNC ni perfil Janus.

---

## 4. Estados de control operativo

### STOP (Round1)

**PIPELINE STOP** / **Round1 STOP:** congelar cómputo y promoción de candidatos sobre datos no certificados en el pipeline de calibración documental Gold (recuperación de primarios, no promover REVIEW → GOLD). **No** implica detener Janusforge entero: workstreams post-0Q (SMRF **ACTIVE**, 0Q.1 **EXPAND**) operan en scope distinto (U1 = UNRESOLVED). Fuente: `ROUND1.9_MASTER_EVIDENCE_STATE.md` §3E; `docs/JANUSFORGE_RESEARCH_STATE.md` §10.

### Taxonomía de estados operativos (RESEARCH_STATE)

Breve referencia para lectura de informes; detalle en `docs/JANUSFORGE_RESEARCH_STATE.md` §5–§9 y `JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md`.

| Estado | Significado breve |
|--------|-------------------|
| **CURRENT** | Decisión o informe vigente en el dominio declarado; autoridad operativa hasta supersesión explícita. |
| **CONFLICT** | Dos fuentes del mismo dominio declaran estados opuestos sin patch de cierre (p. ej. C1: Qiu ACTIVE vs 0Q D NO-GO). |
| **UNRESOLVED** | Pregunta de scope sin autoridad conjunta (p. ej. U1: Round1 STOP vs SMRF ACTIVE). |
| **RESERVE** | Workstream vivo pero no en ruta crítica (p. ej. 0M wet H1-a CURRENT). |
| **EXPAND** | Siguiente trabajo autorizado = expansión documental/literaria only (p. ej. 0Q.1). |
| **HISTORICAL** | Estado registrado en commit/fecha anterior; no operativo actual (p. ej. 0M BLOCKED @ `db46e9a`). |
| **SUPERSEDED** | Decisión posterior reemplaza explícitamente la anterior en el mismo dominio (p. ej. BLOCKED → RESERVE para 0M). |

Otros estados frecuentes en tablas de decisión: **ACTIVE**, **NO-GO**, **MODERATE**, **BLOCKED**, **GO** — siempre leer el **scope** del informe que los declara.

---

## 5. Cobertura vs auditoría de legibilidad (checklist)

Términos clave que un lector externo debe poder resolver en este glosario:

| Término | § | Cubierto |
|---------|---|----------|
| 0M (metodológico + corpus) | 1 | ✓ |
| 0Q (metodológico + corpus) | 1 | ✓ |
| SMRF / 0Q-SMRF | 1 | ✓ |
| Level 0 / Norma L0 | 1 | ✓ |
| PRIMARY_VERIFIED | 2 | ✓ |
| PRIMARY_PARTIAL | 2 | ✓ |
| REVIEW_REQUIRED | 2 | ✓ |
| CONTRADICTED | 2 | ✓ |
| GOLD_CONFIRMED / GOLD | 2 | ✓ |
| BLINDED / QUARANTINE | 2 | ✓ |
| Subset A | 3 | ✓ |
| Subset B | 3 | ✓ |
| Janus / Janus Ligand | 3 | ✓ |
| Controlled Deactivation / soft-drug | 3 | ✓ |
| STOP Round1 / PIPELINE STOP | 4 | ✓ |
| CURRENT / CONFLICT / UNRESOLVED | 4 | ✓ |
| RESERVE / EXPAND / HISTORICAL / SUPERSEDED | 4 | ✓ |
| 0Q.1 | 1 (corpus) | ✓ |
| U1 / U2 (scope) | 4 (UNRESOLVED) | ✓ |
| C1–C5 (solo referencia; no resueltos) | — | referenciados en RESEARCH_STATE §8 |

**Referencias de navegación:** mapa maestro `docs/JANUSFORGE_RESEARCH_STATE.md`; resumen ejecutivo `docs/JANUSFORGE_RESEARCH_EXECUTIVE_SUMMARY.md`; auditoría de supersesión `results/reports/JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md`.
