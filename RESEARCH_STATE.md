# RESEARCH STATE — Janusforge CB₂ (congelación analítica)

**Fecha:** 2026-08-20  
**Rama:** `docs/cb2-atlas-and-epistemological-consolidation`  
**Tipo:** Estado de investigación consolidado en frontera — **no** autoriza cómputo nuevo  
**Bitácora extendida:** [`docs/JANUSFORGE_RESEARCH_STATE.md`](docs/JANUSFORGE_RESEARCH_STATE.md)

---

## Gobernanza vigente

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

**Pausa fija.** No hay bucles computacionales abiertos. Reanudar solo con orden PI explícita.

---

## Mapa epistemológico (resumen)

| Nivel | Dominio | Estatus | Evidencia clave |
|-------|---------|---------|-----------------|
| **1 — Macro** | TM3–TM6; separación activo/inactivo | 🟢 **DEMOSTRADO** | Phase G: 8GUR (2.32) ≈ 6KPF (2.30) ≪ 5ZTY (3.95); veredicto **GENERALIZES** |
| **2 — Micro-red** | Trp258/Ser285/Phe183; par HU-308/HU-433 | 🟡 **LÍMITE ESTÁTICO** | Micronetwork **INDETERMINATE** (6PT0 identical / 6KPF distinct); Phase H **INDETERMINATE** |
| **3 — Dinámica** | Rotámeros, agua, k_off, MD μs | 🔴 **FRONTERA** | Docking estático ≠ eficacia Gi; Rachman *et al.* 2026 (DOI 10.1021/acs.jmedchem.6c00835) |

---

## Cierre ordenado de fases conformacionales

| Fase | Veredicto | Fecha cierre | Fuente |
|------|-----------|--------------|--------|
| **F** — Huella conformacional | COMPLETE | 2026-08-19 | `results/conformational/fase_f_conformational_fingerprint.md` |
| **G** — Generalización 8GUR OOS | **GENERALIZES** (Q1); Q2 PARTIAL | 2026-08-19 | `results/conformational/fase_g_generalization_report.md` |
| **H** — Ordinal funcional H0/H1 | **INDETERMINATE** | 2026-08-19 | `results/conformational/fase_h_ordinal_functional_report.md` |
| **Micronetwork** HU-308 vs HU-433 | **INDETERMINATE** | 2026-08-20 | `results/conformational/micronetwork_modes_report.md` |

### Notas de cierre

- **Phase G:** coordenada macro CB2_STATE_DISTANCE generaliza out-of-sample a **8GUR** (CP55,940 + Gi, ciego).
- **Phase H:** HU-433 sin fila Gi comparable forzada; AM630 = PROTEAN; proyección conformacional insuficiente para ordinal.
- **Micronetwork:** plasticidad de estado — no promover DISTINCT 6KPF como ley del par enantiomérico.

---

## Congelación analítica

| Ámbito | Estado |
|--------|--------|
| Retrospectivo A–E (`results/docking/`) | **CLOSED_AND_ARCHIVED** — read-only |
| Calibración multistate | **CLOSED** (2026-08-19) |
| Contract v1.0 | **ARCHIVED_HISTORICAL** — testigo 6PT0, no predictor funcional |
| de_novo / threshold / docking | **STOP** |
| SMRF / 0Q.1 literatura | Documental; no reabre compute (ver bitácora extendida) |

---

## Índice — síntesis consolidada (`docs/synthesis/`)

| Documento | Contenido |
|-----------|-----------|
| [`docs/synthesis/CB2_STRUCTURE_ATLAS.md`](docs/synthesis/CB2_STRUCTURE_ATLAS.md) | Atlas PDB: 5ZTY, 6PT0, 6KPF, 8GUS/UR/UQ/UT, 12IY/IZ/JA, 8X3L, 9U7L; Level-0; Phase F/G |
| [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) | Par enantiomérico; 8GUS experimental; Soethoudt/Hanuš; micronetwork INDETERMINATE |
| [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) | ACN (Morales-Pastor 2025); Trp258 (Ganzoni 2026); ECL2; frontera MD |
| [`docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md`](docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md) | Límites estáticos; Rachman 2026; INDETERMINATE; gobernanza completa |

---

## Índice — artefactos conformacionales

| Artefacto | Ruta |
|-----------|------|
| Phase F report + matrix | `results/conformational/fase_f_conformational_fingerprint.md`, `cb2_state_distance_matrix.json` |
| Phase G report | `results/conformational/fase_g_generalization_report.md` |
| Phase H report | `results/conformational/fase_h_ordinal_functional_report.md` |
| Micronetwork report | `results/conformational/micronetwork_modes_report.md` |
| Micronetwork falsification | `results/conformational/micronetwork_falsification_report.md` |

---

## Índice — documentos de gobernanza relacionados

| Documento | Ruta |
|-----------|------|
| Bitácora maestra (extendida) | `docs/JANUSFORGE_RESEARCH_STATE.md` |
| Síntesis frontera metodológica | `docs/cb2_mechanistic_frontier_synthesis.md` |
| Balance epistemológico | `docs/epistemic_balance_calibration_2026-08-19.md` |
| Reformulación switch | `docs/switch_hypothesis_allosteric_reformulation.md` |
| Mapa alostérico (HIPÓTESIS) | `docs/cb2_allosteric_switch_map.md` |
| Calibración multistate | `docs/cb2_multistate_calibration_synthesis.md` |

---

## Próximo paso — solo encuadre (NO ejecutar)

1. Descriptor local pre-registrado HU-308/HU-433 en panel multi-estado **o** MD μs (Trp258, agua).
2. Requiere orden PI explícita; **no** modifica candados de gobernanza.

---

## Lectura recomendada al reanudar sesión

1. **Este archivo** (`RESEARCH_STATE.md`)
2. [`docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md`](docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md)
3. [`docs/JANUSFORGE_RESEARCH_STATE.md`](docs/JANUSFORGE_RESEARCH_STATE.md) — conflictos, historial, SMRF

---

*Fin RESEARCH_STATE.md. Congelación analítica 2026-08-20 — documentación únicamente.*
