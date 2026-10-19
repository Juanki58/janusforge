# Límites del docking estático y gobernanza — CB₂ Janusforge

**Fecha:** 2026-08-20  
**Modo:** Documental / READ-ONLY — **sin docking, sin MD, sin cómputo nuevo**  
**Rama:** `docs/cb2-atlas-and-epistemological-consolidation`

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[OBSERVACIÓN_PROPIA]** | Datos generados por el proyecto (Phase F/G/H, micronetwork, Contract v1.0, distancias medidas desde JSON del repo) |
| **[LITERATURA_PRIMARIA]** | Evidencia publicada externa — requiere DOI, PMID o PDB |
| **[HIPÓTESIS_ABIERTA]** | Afirmación mecanística no demostrada en el repo |

---

## 1. Gobernanza operativa (vigente)

```yaml
RESEARCH_FROZEN_FOR_CONSOLIDATION: true
COMPUTATION_PAUSED: true
DE_NOVO_GENERATION: STOP
DOCKING_PIPELINES: STOP
THRESHOLD_TUNING: STOP
CONTRACT_v1.0: ARCHIVED_HISTORICAL
ACTIVE_ACTION: DOCUMENTATION_CONSOLIDATION_ONLY
RESEARCH_STATUS: RESEARCH_CONSOLIDATED_AT_FRONTIER
```

| Parámetro | Estado | Nota |
|-----------|--------|------|
| `RESEARCH_FROZEN_FOR_CONSOLIDATION` | **true** | Congelación analítica post-fases G/H/micronetwork |
| `COMPUTATION_PAUSED` | **true** | Pipelines computacionales detenidos |
| `DE_NOVO_GENERATION` | **STOP** | Sin moléculas nuevas |
| `DOCKING_PIPELINES` | **STOP** | Sin campañas docking A–E ni nuevas |
| `THRESHOLD_TUNING` | **STOP** | Calibrar ≠ retocar |
| `CONTRACT_v1.0` | **ARCHIVED_HISTORICAL** | Testigo del observador estático 6PT0; **no** predictor funcional |
| `ACTIVE_ACTION` | **DOCUMENTATION_CONSOLIDATION_ONLY** | Única acción autorizada |

---

## 2. Mapa epistemológico de tres niveles

```
NIVEL 1  MACRO TM3–TM6     🟢 DEMOSTRADO en proyecto
NIVEL 2  MICRO-RED         🟡 LÍMITE ESTÁTICO (INDETERMINATE)
NIVEL 3  DINÁMICA           🔴 FRONTERA (requiere MD μs)
```

### Nivel 1 — Macro 🟢 DEMOSTRADO

**[OBSERVACIÓN_PROPIA]** **Phase G** (`results/conformational/fase_g_generalization_report.md`):

| PDB | Distancia normalizada | Estado |
|-----|----------------------|--------|
| 6PT0 | 2.3019 | activo |
| 6KPF | 2.3019 | activo |
| **8GUR** (ciego OOS) | **2.3205** | activo CP55,940 + Gi |
| 5ZTY | 3.9501 | inactivo |

**[OBSERVACIÓN_PROPIA]** **Veredicto:** `GENERALIZES` — 8GUR (2.32) ≈ 6KPF (2.30) ≪ 5ZTY (3.95).

**[LITERATURA_PRIMARIA]** Atlas macro: estados activos comparten núcleo TM con **RMSD Cα ~0.35 Å** entre plantillas activas de alta resolución (Li *et al.* 2023, DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494).

**[OBSERVACIÓN_PROPIA]** La coordenada **CB2_STATE_DISTANCE** del proyecto captura esta proximidad macro.

### Nivel 2 — Micro-red 🟡 LÍMITE ESTÁTICO

**[OBSERVACIÓN_PROPIA]**

- **6KPF** detecta divergencia HU-308/HU-433 (`DISTINCT_LOCAL_MODES`).
- **6PT0** enmascara la misma divergencia (`IDENTICAL_LOCAL_MODES`).
- **Veredicto micronetwork:** `INDETERMINATE` — dependencia del molde conformacional.

**[OBSERVACIÓN_PROPIA]** **Phase H:** veredicto ordinal `INDETERMINATE` — proyección conformacional insuficiente para tiers Gi (≥3 proyecciones requeridas, 1 obtenida).

### Nivel 3 — Dinámica 🔴 FRONTERA

**[HIPÓTESIS_ABIERTA]** El docking estático/semi-flexible **≠** eficacia funcional Gi. Requiere dinámica explícita (rotámeros Trp258, agua, k_off, MD μs) — ver [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) §6.

---

## 3. Por qué el docking estático no predice eficacia determinista

### 3.1 Distinción semántica (definitiva)

| Proposición | Veredicto |
|-------------|-----------|
| `STRUCTURAL_BINDING = PASS` → «será un fármaco activo» | **FALSO** |
| `STRUCTURAL_BINDING = PASS` → «satisface envolvente estérica v1.0» | **VERDADERO** (definición operativa Contract) |
| FAIL lit-activo bajo 6PT0 → «molécula inactiva» | **FALSO** — evidencia de límite del observador |

**[OBSERVACIÓN_PROPIA]** Fuente: [`docs/epistemic_balance_calibration_2026-08-19.md`](../epistemic_balance_calibration_2026-08-19.md) §2.

### 3.2 Desacople de capas (Fases A–E)

**[OBSERVACIÓN_PROPIA]** Phase B (`results/docking/audit_qiu_decoupled_layers.md`) documentó rechazo **concomitante** estructural + periférico en set Qiu. Las cinco dimensiones farmacológicas permanecen **ortogonales**:

```
AFINIDAD  ≠  ALOSTERIA  ≠  ESTADO CONFORMACIONAL  ≠  EFICACIA  ≠  DISTRIBUCIÓN TISULAR
```

### 3.3 Evidencia convergente del proyecto

**[OBSERVACIÓN_PROPIA]**

| Fase | Veredicto | Implicación |
|------|-----------|-------------|
| Phase E | HU-433, O-1966 lit-activos → Q4 FAIL bajo Contract v1.0 | Discrepancia lit ↔ grid estático |
| Calibración multistate | Mismas moléculas **acomodadas** Vina en 6PT0/5ZTY/6KPF | FAIL Phase E = criterios v1.0, no imposibilidad de pose |
| Phase H | INDETERMINATE | Distancia centroide ≠ tier Gi |
| Micronetwork | INDETERMINATE | Microdescriptor depende del estado PDB |

### 3.4 Contract v1.0 — testigo histórico archivado

**[OBSERVACIÓN_PROPIA]** `configs/thcv_design_constraints.yaml` codifica proxies medidos contra **5TGZ** (CB1 inactivo) y **6PT0** (CB2 activo WIN). Tras Phase H:

> Contract v1.0 colapsó como **predictor funcional** pero permanece **ARCHIVED_HISTORICAL** — registro de la hipótesis geométrica estática v1.0, **no** ley mecanística universal.

**[OBSERVACIÓN_PROPIA]** **Mantra:** `CALIBRAR ≠ RETOCAR`. Prohibido retune post-hoc para forzar PASS de lit-activos.

---

## 4. Rachman *et al.* 2026 — advertencia metodológica (literatura verificada)

**[LITERATURA_PRIMARIA]** **Referencia verificada:** Rachman, M. M. *et al.* «Library Docking for Cannabinoid-2 Receptor Ligands.» *Journal of Medicinal Chemistry* (2026). DOI [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PMID 42397716.

**[LITERATURA_PRIMARIA]** **Estructuras de validación:** PDB **12IY** (agonista '5249), **12JA** (agonista '1029); EMDB EMD-76465.

### Hallazgos relevantes para Janusforge (abstract / PDB verificados)

**[LITERATURA_PRIMARIA]**

1. Campaña de docking a escala de biblioteca (**2.6 mil millones** de moléculas) contra CB2, iniciando desde estructura activa **6PT0** (PDB **6PT0**).
2. Mejora de hit rate y afinidad con tamaño de biblioteca; selectividad CB2/CB1 mejorada priorizando interacciones polares ortostéricas.
3. **Advertencia central (PI-cited, verificada):** docking contra estados activos **e inactivos** del receptor **no sesgó de forma fiable** hacia descubrimiento de agonistas vs inverse agonistas — resultado convergente con estudios previos en CB1R.
4. Dos agonistas de nueva química superponen bien con predicciones de docking (cryo-EM 12IY/12JA).

### Implicación epistemológica

**[OBSERVACIÓN_PROPIA]** Incluso campañas de docking de alto rendimiento con validación cryo-EM **no** resuelven la inferencia funcional ordinal (agonismo total vs parcial vs inverse) desde el estado receptor template alone. Esto **corrobora** los veredictos INDETERMINATE de Phase H y la congelación analítica del proyecto.

> **[LITERATURA_PRIMARIA]** **Caveat:** Detalle cuantitativo fino (tablas SI, logAUC exactos) no transcrito aquí — consultar primario DOI [10.1021/acs.jmedchem.6c00835](https://doi.org/10.1021/acs.jmedchem.6c00835); PMID 42397716.

---

## 5. INDETERMINATE como salvaguarda contra falsos positivos

### 5.1 Regla de gobernanza

**[OBSERVACIÓN_PROPIA]** **No reinterpretar INDETERMINATE como PASS/FAIL por inferencia.**

| Fase | Veredicto | Qué NO implica |
|------|-----------|----------------|
| Phase G Q2 | PARTIAL | No invalida Q1 GENERALIZES |
| Phase H H1 | INDETERMINATE | No demuestra que docking predice Gi; tampoco prueba alosteria |
| Micronetwork | INDETERMINATE | No ley del par enantiomérico; plasticidad 6PT0/6KPF |

### 5.2 Por qué INDETERMINATE es informativo

**[OBSERVACIÓN_PROPIA]** Un resultado INDETERMINATE **delimita** el alcance del observador:

- **Phase H:** gaps de datos funcionales (HU-433 sin fila Gi comparable; THCV INDETERMINATE) + colapso de proyección conformacional.
- **Micronetwork:** criterios congelados exigen reproducibilidad cross-state; discrepancia 6PT0/6KPF impide veredicto binario.

**[OBSERVACIÓN_PROPIA]** Forzar PASS o FAIL degradaría el poder falsificador del programa.

---

## 6. Fases A–E — archivo read-only

**[OBSERVACIÓN_PROPIA]**

| Fase | Artefacto | Estado |
|------|-----------|--------|
| A | `results/docking/challenge_qiu_blind_evaluation.md` | ARCHIVED |
| B | `results/docking/audit_qiu_decoupled_layers.md` | ARCHIVED |
| C | `results/docking/screening_natural_cannabinoids_fase_c.md` | ARCHIVED |
| D | `results/docking/screening_precedents_fase_d.md` | ARCHIVED |
| E | `results/docking/screening_patents_thcv_fase_e.md` | ARCHIVED |

**[OBSERVACIÓN_PROPIA]** **Q1 (GLOBAL PASS falsificando Contract):** **0** compuestos en paneles retrospectivos (`external_audit_four_quadrants.md`).

---

## 7. Próximo experimento — solo encuadre (NO ejecutar)

**[HIPÓTESIS_ABIERTA]** Reanudación **solo** con orden PI explícita post-congelación:

1. **Descriptor local pre-registrado** HU-308/HU-433 en panel multi-estado (6PT0, 6KPF, 8GUS) **o**
2. **MD μs** con muestreo Trp258/Ser285 y redes de agua

**[OBSERVACIÓN_PROPIA]** **Prohibido en pausa:** retune Contract, nuevos grids operativos, generación de_novo, campañas docking.

---

## 8. Mapa de síntesis

| Documento | Contenido |
|-----------|-----------|
| [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md) | Plantillas PDB; Phase F/G |
| [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md) | Par enantiomérico; micronetwork; contradicciones abiertas |
| [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) | ACN; Trp258; ECL2 |
| [`../JANUSFORGE_RESEARCH_STATE.md`](../JANUSFORGE_RESEARCH_STATE.md) | Bitácora extendida |
| [`../cb2_mechanistic_frontier_synthesis.md`](../cb2_mechanistic_frontier_synthesis.md) | Síntesis frontera PI |

---

## 9. Cierre

**[OBSERVACIÓN_PROPIA]** **Pausa fija.** No hay bucles computacionales abiertos. El stack estático (Vina + Contract v1.0 archivado + proxies de distancia) es **suficiente para discriminar macro-estados** (activo vs inactivo, Phase G) e **insuficiente para inferir eficacia funcional Gi** sin dinámica explícita (Nivel 3).

---

*Fin límites docking y gobernanza. Documento de consolidación — no autoriza cómputo.*
