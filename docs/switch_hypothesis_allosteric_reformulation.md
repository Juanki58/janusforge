# REFORMULACIÓN DE LA HIPÓTESIS DEL CONMUTADOR MOLECULAR (SWITCH)

**Fecha de emisión:** 2026-08-19  
**Modo operativo:** Documental / Gobernanza Metodológica  
**Estado del Repositorio:** `READ-ONLY` | `DE_NOVO_GENERATION = STOP` | `THRESHOLD_MODIFICATION = STOP`

---

## 1. Estado de Control y Gobernanza del Proyecto

| Parámetro de Gobernanza | Estado Asignado | Alcance y Restricciones |
| :--- | :---: | :--- |
| **`THCV_ORTHOSTERIC_DESIGN`** | **`PAUSED`** | Pausada la optimización directa en la cavidad ortostérica de Δ⁹-THCV. El corpus THCV (seed, mapping, análogos ensayados, Contract v1.0) permanece como evidencia histórica; **no descartado**. |
| **`RETROSPECTIVE_AUDIT_PHASES_A_E`** | **`CLOSED_AND_ARCHIVED`** | Fases A–E concluidas y archivadas en `results/docking/` (Phase E: `screening_patents_thcv_fase_e.md`). Auditoría externa cuadrantes A–D: `EXTERNAL_AUDIT: CLOSED` (`external_audit_four_quadrants.md`). |
| **`SWITCH_HYPOTHESIS`** | **`OPEN_REFORMULATED`** | Hipótesis abierta hacia el espacio alostérico y multiestado conformacional. |
| **`CALIBRATION_MULTI_STATE`** | **`CLOSED`** | Calibración multiconformacional CB₂ cerrada 2026-08-19. Síntesis: [`cb2_multistate_calibration_synthesis.md`](cb2_multistate_calibration_synthesis.md). |
| **`ALLOSTERIC_FRAMEWORK`** | **`HYPOTHESIS_PENDING_CALIBRATION`** | Marco alostérico **hipótesis pendiente de calibración** — **no** afirmar `ALLOSTERIC_FRAMEWORK = TRUE`. Ver balance epistemológico y síntesis multistate. |
| **`CONTRACT_v1.0`** | **`FROZEN`** | Umbrales y reglas inalteradas (sin retune). Fuente: `configs/thcv_design_constraints.yaml`, `docs/thcv_design_constraints.md`. |
| **`DE_NOVO_GENERATION`** | **`STOP`** | Prohibida la generación o diseño de análogos químicos. |
| **`THRESHOLD_MODIFICATION`** | **`STOP`** | Prohibido modificar umbrales contractuales sin autorización explícita del PI. |

**Balance epistemológico y calibración (PI, 2026-08-19):** ver [`epistemic_balance_calibration_2026-08-19.md`](epistemic_balance_calibration_2026-08-19.md). Resume la distinción **calibrar ≠ retocar** (§3), los criterios de éxito de la etapa multi-estado (§4), el contraste de etapa diseño vs descubrimiento de reglas (§5), el valor de HU-433 / O-1966 / HU-308 como **casos de calibración** (no moléculas a «hacer pasar»), el panel multi-estado CB₂ propuesto y la gobernanza consolidada A–E. `ALLOSTERIC_FRAMEWORK = HYPOTHESIS_PENDING_CALIBRATION` — **not** `TRUE`.

---

## 2. Nueva Pregunta Motriz de Investigación

> **"¿Es posible estabilizar alostéricamente un estado funcional favorable de CB₂ sin promover una señalización central funcionalmente equivalente en CB₁?"**

Esta formulación sustituye como eje rector del workstream `SWITCH_HYPOTHESIS` la búsqueda de encaje ortostérico THCV-like bajo Contract v1.0. **No** reabre generación de_novo ni retune de umbrales.

---

## 3. Balance del Aprendizaje en la Vía Ortostérica (Fases A–E)

La vía de diseño centrada en el bolsillo ortostérico de Δ⁹-THCV queda **pausada, no descartada**. La evidencia acumulada en las Fases A–E demuestra:

1. **Hiper-restricción estérica en CB₁ inactivo:** La cavidad ocluida impone un cuello de botella de volumen crítico. Las colas pentilo (C₅) de cannabinoides naturales clásicos y los núcleos voluminosos sintéticos (Serie Qiu) colisionan sistemáticamente con los límites físicos del receptor.
2. **Desacople ortogonal demostrado (Aparición de Q3):** Casos como CBDA y THCVA demostraron que la restricción de polaridad (TPSA ≥ 70 Å²) y el empaquetamiento ortostérico son dimensiones independientes.
3. **Límite del enfoque ortostérico rígido:** Intentar satisfacer simultáneamente la exclusión en CB₁, la activación en CB₂ y la restricción polar dentro del bolsillo ortostérico primario define un espacio de diseño sumamente angosto bajo modelos estáticos.
4. **Discrepancia lit-activo vs grid estático (Phase E):** HU-433 y O-1966 son agonistas CB₂ documentados que **fallan** Contract v1.0 bajo 6PT0 — **casos de calibración**, no objetivos de retune. La pregunta legítima es qué conformaciones explican los positivos, **no** qué parámetros cambiar para que pasen. Ver [`epistemic_balance_calibration_2026-08-19.md`](epistemic_balance_calibration_2026-08-19.md) §3–§5.

**Conclusión epistemológica (precisa):** Contract v1.0 describe una hipótesis geométrica estática; la actividad CB₂ conocida **no está necesariamente contenida** en esa hipótesis. Esto **no** implica que el docking sea inútil.

**Resultados medidos consolidados (bloque A–E):**

- **Q1 (GLOBAL PASS — falsificación Contract v1.0):** **0** compuestos (`external_audit_four_quadrants.md`).
- **Contract v1.0 NO falsificado** en paneles retrospectivos ensayados.
- **Bloque A–C:** **0 / 9** GLOBAL_v1.0 PASS (4 Qiu dockados + 5 naturales; Qiu-16 excluido) — `retrospective_synthesis_qiu_natural.md`.
- **THCV semilla:** C3 clearance CB1 @ clash 3.0 Å = **0.75 Å** (WARN/FAIL vs umbral ≥ 0.8 Å); TPSA 29.5 Å² — `interaction_mapping_thcv_vs_gold.md`.

> **Nota de integridad (medido vs narrativa):** En la auditoría Phase D y el cierre externo de cuadrantes, el **único Q3 limpio medido** (estructural FAIL / periférico PASS) es **CBDA** (TPSA 77.8 Å²). **THCVA** mide PERIPHERAL **FAIL** (TPSA 66.8 Å² < 70.0) y cuadrante **Q4**, no Q3 — `screening_precedents_fase_d.md`, `external_audit_four_quadrants.md` §3.2. El desacople ortogonal queda demostrado; el precedente Q3 evaluable es uno, no dos.

- **Phase E:** Q1=**0**; HU-433, O-1966 → **Q4** (lit-activo, contract FAIL) — `screening_patents_thcv_fase_e.md`.

**Trazabilidad Fases A–E:** Phase A `challenge_qiu_blind_evaluation.md`; Phase B `audit_qiu_decoupled_layers.md`; Phase C `screening_natural_cannabinoids_fase_c.md`; Phase D `screening_precedents_fase_d.md`; Phase E `screening_patents_thcv_fase_e.md`; síntesis `retrospective_synthesis_qiu_natural.md`, `external_audit_four_quadrants.md`.

---

## 4. Desacople de Dimensiones Farmacológicas

Separación conceptual estricta de **cinco planos independientes**. Ninguno sustituye a otro; fusionarlos en un único veredicto computacional fue precisamente lo que el bloque retrospectivo A–E permitió **descomponer** — sin convertir esa descomposición en nuevos criterios de diseño.

```
AFINIDAD/OCUPACIÓN  ≠  MODULACIÓN ALOSTÉRICA  ≠  ESTADO CONFORMACIONAL  ≠  EFICACIA FUNCIONAL  ≠  DISTRIBUCIÓN TISULAR
```

| Plano | Qué describe | Qué **no** implica |
|-------|--------------|-------------------|
| **Afinidad / ocupación ortostérica** | Unión al bolsillo canónico; proxies geométricos Contract v1.0 (C3, C9/C11, Ser285, etc.) | Eficacia, sesgo conformacional, selectividad tisular |
| **Modulación alostérica** | Ligando en sitio **extraortostérico** que modula la respuesta del receptor (ocupado o no) sin competir por el mismo volumen que agonistas clásicos | Mejor score Vina, PASS contractual, perfil Janus demostrado |
| **Estado conformacional** | Población de estados R ↔ R\* (inactivo ↔ activo / acoplado G); referencias estructurales del proyecto: **5TGZ** CB₁ antagonista/inactivo, **6PT0** CB₂ agonista/acoplado (`configs/cb1_cb2.yaml`) | Que un snapshot de docking demuestre transición o activación |
| **Eficacia funcional** | Señal medida en ensayo (cAMP, β-arrestina, tejido, in vivo) | Distancia a microswitch, clearance geométrico, TPSA |
| **Distribución tisular (periférica / SNC)** | PK, BBB, restricción anatómica, química de acceso | Consecuencia automática de modulación alostérica o de TPSA elevada |

**Prohibiciones epistemológicas reafirmadas:**

- **Docking estático no predice eficacia.** Scores Vina y clearances geométricos miden compatibilidad estérica de poses Mode 1; no equivalen a afinidad experimental, agonismo, antagonismo ni perfil Janus funcional (`retrospective_synthesis_qiu_natural.md` §D).
- **Alostería no garantiza distribución periférica.** TPSA ≥ 70 Å² es heurística contractual, no prueba de exclusión BBB (`external_audit_four_quadrants.md` §4). La modulación alostérica opera en el plano receptor; la distribución tisular exige evidencia PK/tejido independiente.

---

## 5. Marco Conceptual Alostérico y Precedentes Estructurales

### A. Precedentes experimentales: ZCZ011 (PAM) vs ORG27569 (NAM) — distinguir evidencia de literatura de hipótesis del proyecto

Estos compuestos **no** forman parte del corpus computacional janusforge (sin evaluación docking ni funcional propia en repo). Se registran como **precedentes conceptuales externos**:

| Compuesto | Rol en literatura (resumen) | Evidencia experimental (literatura) | Relación con hipótesis del proyecto |
|-----------|----------------------------|-----------------------------------|-------------------------------------|
| **ZCZ011** | PAM selectivo CB₂ descrito en publicaciones | Modulación alostérica positiva CB₂ reportada in vitro (no replicada en janusforge) | **Precedente conceptual:** sitios extraortostéricos pueden sesgar respuesta CB₂ — **≠** compuesto del programa, **≠** demostración del perfil Janus deseado |
| **ORG27569** | PAM CB₁ descrito en publicaciones | Modulación alostérica positiva CB₁ reportada in vitro (no replicada en janusforge) | **Precedente conceptual:** PAM CB₁ puede potenciar señal CB₁ — **refuerza la pregunta motriz** (evitar equivalencia funcional central indeseada), **≠** diseño validado del programa |

La existencia de moduladores alostéricos en literatura demuestra **viabilidad biológica general** del mecanismo. **No** demuestra que janusforge disponga hoy de un par PAM-CB₂ / NAM-CB₁ óptimo ni evidencia computacional directa en el repositorio.

### B. Hipótesis de trabajo **no demostradas** (registro explícito)

Las siguientes proposiciones son **hipótesis plausibles**, no hechos establecidos en janusforge:

1. **Divergencia extraortostérica:** Sitios alostéricos pueden ofrecer selectividad de subtipo CB₂ vs CB₁ sin requerir encaje ortostérico THCV-like bajo Contract v1.0.
2. **Modulación del equilibrio de estados:** Moduladores alostéricos pueden sesgar poblaciones conformacionales (p. ej. favorecer estado funcional favorable CB₂) independientemente de la ocupación ortostérica clásica.
3. **Microswitches como nodos mecánicos posibles:** Residuos F200(3.36) / W356(6.48) en CB₁ y F117 / W258 / **Ser285** en CB₂ (`src/analysis/interaction_mapping.py`, `run_benchmark_gold_exam_a.py`) son nodos **plausibles** para explicar cambios de eficacia en literatura y en la matriz SMRF mono-CB₂ (`qiu_0q_smrf_matrix.md`, `qiu_0q1_final_cursor_vs_gemini.md`). **No** se afirma que modulación alostérica sobre esos nodos esté demostrada en este programa.

**Salvedad obligatoria:** **No** afirmar que existe un PAM-CB₂ / NAM-CB₁ óptimo en el proyecto. **No** reclamar evidencia computacional directa de alosteria en el repo más allá del marco conformacional de referencia (5TGZ / 6PT0) y la continuidad documental SMRF.

---

## 6. Estado Operativo

```yaml
STATUS_SUMMARY:
  CALIBRATION_MULTI_STATE: CLOSED  # docs/cb2_multistate_calibration_synthesis.md
  ORTHOSTERIC_LINE: PAUSED  # pausado, no descartado
  RETROSPECTIVE_AUDIT_PHASES_A_E: CLOSED_AND_ARCHIVED
  ALLOSTERIC_FRAMEWORK: HYPOTHESIS_PENDING_CALIBRATION  # NOT TRUE
  ALLOSTERIC_SWITCH_LINE: OPEN_HYPOTHESIS
  DESIGN_GENERATION: STOP
  EXPERIMENTAL_VALIDATION_REQUIREMENT: MANDATORY
  NEXT_FOCUS: experimental_validation  # NOT retune, NOT blind PAM/NAM generation
```

**Prohibición de auto-diseño prematuro:** Este documento **no** convierte la hipótesis reformulada en criterios de diseño, umbrales nuevos ni Contract v2.0 implícito. Cualquier pantalla ortostérica futura sigue sujeta a Contract **v1.0 FROZEN**. `DE_NOVO_GENERATION` y `THRESHOLD_MODIFICATION` permanecen en **STOP** hasta nueva directiva PI.

**Requisito de validación experimental (mandatorio):** Cualquier avance más allá de este marco documental exige evidencia experimental independiente del docking estático, como mínimo:

- **Afinidad / ocupación** (Ki, Kd, radioligando) desacoplada de eficacia.
- **Eficacia funcional** (cAMP, β-arrestina, ensayos tisulares) en CB₁ y CB₂ por separado.
- **Permeabilidad / distribución** (PK, BBB, tejido) — no inferible de TPSA ni de mecanismo alostérico.

Hasta entonces, `SWITCH_HYPOTHESIS` permanece en **`OPEN_REFORMULATED`**: pregunta motriz y gobernanza registradas; **no** pipeline de generación química.

---

## Trazabilidad (referencia rápida)

| Tema | Ruta |
|------|------|
| Target prep / redock | `results/reports/TARGET_PREP_REDOCK_QC.md` |
| Exam A Gold | `results/docking/benchmark_gold_exam_a.md` |
| THCV seed + QC | `results/docking/thcv_seed_evaluation.md`, `results/docking/qc_seed_thcv_audit.md` |
| Interaction mapping | `results/docking/interaction_mapping_thcv_vs_gold.md` |
| Contract v1.0 | `configs/thcv_design_constraints.yaml`, `docs/thcv_design_constraints.md` |
| Fases A–E + auditoría | `results/docking/external_audit_four_quadrants.md`, `results/docking/screening_patents_thcv_fase_e.md` |
| Balance epistemológico / calibración | `docs/epistemic_balance_calibration_2026-08-19.md` |
| Cierre calibración multistate CB₂ | `docs/cb2_multistate_calibration_synthesis.md` |
| Phase E — patentes / lit | `results/docking/screening_patents_thcv_fase_e.md` |
| Gobernanza programa | `docs/JANUSFORGE_RESEARCH_STATE.md`, `results/reports/JANUS_DECISION_LEDGER_v1.0.md` |

---

*Fin `docs/switch_hypothesis_allosteric_reformulation.md`. Documento de gobernanza únicamente.*
