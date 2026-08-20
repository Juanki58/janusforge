# RESEARCH STATE — Janusforge CB₂ (congelación analítica)

**Fecha:** 2026-08-20  
**Rama:** `feat/cb2-minimal-gi-core-reanalysis`  
**Tipo:** Reanálisis READ-ONLY de datos públicos (núcleo mínimo CB2→Gαi) — **cerrado**  
**Bitácora extendida:** [`docs/JANUSFORGE_RESEARCH_STATE.md`](docs/JANUSFORGE_RESEARCH_STATE.md)

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[OBSERVACIÓN_PROPIA]** | Datos generados por el proyecto (Phase F/G/H, micronetwork, Contract v1.0, distancias medidas desde JSON del repo) |
| **[LITERATURA_PRIMARIA]** | Evidencia publicada externa — requiere DOI, PMID o PDB |
| **[INTERNAL_REANALYSIS]** | Reanálisis sobre objetos públicos recuperados |
| **[HIPÓTESIS_ABIERTA]** | Afirmación mecanística no demostrada en el repo |
| **[INDETERMINATE]** | Bloqueado / irreproducible / datos incompletos |

---

## Gobernanza vigente

```yaml
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
CONTRACT_v1.0: ARCHIVED_HISTORICAL
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
MODO: READ_ONLY / PUBLIC_DATA_REANALYSIS
ACTIVE_ACTION: MINIMAL_CORE_REANALYSIS_COMPLETE_STOP
# Explicit: NOT Fase I
RESEARCH_STATUS: MINIMAL_CORE_REANALYSIS_INDETERMINATE
```

**[OBSERVACIÓN_PROPIA]** Diseño químico / de_novo / docking / Phase I **STOP**.  
**[INTERNAL_REANALYSIS]** Reanálisis de red ejecutado bajo protocolo cerrado → **`FINAL_VERDICT=INDETERMINATE`** (recuperación incompleta). Ver `results/network_core/`. **DETENER EJECUCIÓN.**

---

## Cambio de objeto (directiva PI)

**[HIPÓTESIS_ABIERTA]** El programa **no** concluye un «switch»; pregunta si existe un **mecanismo mínimo** demostrable con datos públicos.

**Pregunta frontera (única):**

> ¿Existe un núcleo mínimo de la red conformacional de CB2 que sea necesario para el acoplamiento a Gαi y cuya arquitectura sea diferente en CB1?

**Protocolo:** [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md)  
**Informe (recovery-first):** [`results/network_core/cb2_minimal_gi_core_report.md`](results/network_core/cb2_minimal_gi_core_report.md)  
**Auditoría:** [`results/network_core/data_audit.md`](results/network_core/data_audit.md)  
Veredictos: **`CORE_FOUND`** | **`NETWORK_DISTRIBUTED`** | **`CB2_SPECIFIC_CORE`** | **`INDETERMINATE`** — asignado: **`INDETERMINATE`**.  
CB1_COMPARISON: **`INDETERMINATE`**.

---

## Diagrama de estado

```
LITERATURA / DATOS PÚBLICOS
        │
        ├── CB2 ACN + Gαi2       ✓
        ├── CB2 MSM              ✓
        ├── CB1 MSM              ✓
        └── datos mutacionales   ✓
                  │
                  ▼
        PREGUNTA ABIERTA
        "¿Existe un núcleo mínimo CB2→Gi diferencial de CB1?"
                  │
                  ▼
             REANÁLISIS
             READ-ONLY
             (protocolo cerrado;
              NOT Fase I)
                  │
                  ▼
                 STOP
```

**[OBSERVACIÓN_PROPIA]** «✓» = disponibilidad / hallazgo **publicado** verificado en literatura (DOI/PMID/PDB/depósitos). **No** significa que Janusforge haya descargado trayectorias ni computado un núcleo mínimo.

---

## Registro provisional — tabla de resultados (literatura / abierto)

**[LITERATURA_PRIMARIA]** / **[HIPÓTESIS_ABIERTA]** — **no** son «resultado propio» de un núcleo computado en este repo.

| Pregunta | Estado |
|----------|--------|
| ¿Hay una red CB2→efector intracelular? | 🟢 Establecido por literatura (ACN/LigACN; Morales-Pastor 2025, DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID 40500255) |
| ¿Nodos asociados a preferencia Gαi2 tienen mayor conectividad/proximidad a alta transmisión? | 🟢 Establecido por literatura (mismo) |
| ¿La red está concentrada en Trp258/Ser285? | 🔴 No; es distribuida (LigACN vía TM7, TM2/3/6, motivos conservados) |
| ¿TM7 participa especialmente en ruta agonismo/Gi? | 🟢 Apoyado fuertemente (Morales-Pastor 2025; Dutta & Shukla 2023, DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)) |
| ¿CB2 posee una única coordenada conformacional suficiente para Gi? | 🔴 No demostrado / probablemente insuficiente (seis estados metaestables; Phase G≠suficiencia funcional) |
| ¿Existe un núcleo mínimo CB2-Gi funcionalmente diferente de CB1? | ⚪ **`INDETERMINATE`** en reanálisis interno (recovery incompleta: sinks T, traj, Supp Data 4, grafo CB1) — ver `results/network_core/` |

---

## Mapa epistemológico (resumen)

| Nivel | Dominio | Estatus | Evidencia clave |
|-------|---------|---------|-----------------|
| **1 — Macro** | TM3–TM6; separación activo/inactivo | 🟢 **DEMOSTRADO** | **[OBSERVACIÓN_PROPIA]** Phase G: 8GUR (2.32) ≈ 6KPF (2.30) ≪ 5ZTY (3.95); veredicto **GENERALIZES** |
| **2 — Micro-red** | Trp258/Ser285/Phe183; par HU-308/HU-433 | 🟡 **LÍMITE ESTÁTICO** | **[OBSERVACIÓN_PROPIA]** Micronetwork **INDETERMINATE** (6PT0 identical / 6KPF distinct); Phase H **INDETERMINATE** |
| **3 — Dinámica / red** | ACN, LigACN, MSM, núcleo mínimo | 🔴 **FRONTERA** | **[LITERATURA_PRIMARIA]** ACN distribuida (Morales-Pastor 2025); MSM 6 estados (Dutta & Shukla 2023); **[HIPÓTESIS_ABIERTA]** núcleo mínimo diferencial CB2 vs CB1 **no resuelto** |

---

## Contradicciones abiertas (registro maestro)

**[OBSERVACIÓN_PROPIA]** Tabla canónica en [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) §7. Resumen — **sin armonización post hoc**:

| Tema | Evidencia en conflicto | Estado |
|------|------------------------|--------|
| **HU-433** | Ki radioligando menor vs potencia biológica mayor (Smoum 2015, DOI [10.1073/pnas.1503395112](https://doi.org/10.1073/pnas.1503395112); PMID 26124120); GTPγS Emax no siempre significativo; orientaciones distintas propuestas; Phase H INDETERMINATE | **ABIERTA** |
| **AM630** | Inverse agonist (cAMP −152%) vs comportamiento casi neutral (GTPγS −22%) en Soethoudt 2017 (DOI [10.1038/ncomms13958](https://doi.org/10.1038/ncomms13958); PMID 28045051); Phase H = PROTEAN | **ABIERTA** |
| **Trp258^6.48** | Literatura: continuo funcional vía toggle (Ganzoni 2026, DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)) **y** ACN distribuida **no** reducida a Trp258 (Morales-Pastor 2025) vs proyecto: micronetwork INDETERMINATE (6PT0 enmascara / 6KPF detecta) | **ABIERTA** |
| **WIN 55,212-2** | cAMP full agonist (98%) vs GTPγS partial agonist (49%) — Soethoudt 2017 | **ABIERTA** |
| **Docking → función** | Rachman 2026: template activo/inactivo no predice clase funcional; Phase E lit-activos FAIL Contract v1.0 | **ABIERTA** |
| **8GUS vs 6PT0** | Pose experimental HU-308 (PDB **8GUS**) vs colapso centroide en docking 6PT0 | **ABIERTA** |

> **Regla:** todas las filas = **ABIERTA**. No se inventa resolución. La corrección «Trp258 no es switch único» (**[LITERATURA_PRIMARIA]**) **no** cierra la fila Trp258 del paradox del par HU-308/HU-433.

---

## Cierre ordenado de fases conformacionales

| Fase | Veredicto | Fecha cierre | Fuente |
|------|-----------|--------------|--------|
| **F** — Huella conformacional | COMPLETE | 2026-08-19 | `results/conformational/fase_f_conformational_fingerprint.md` |
| **G** — Generalización 8GUR OOS | **GENERALIZES** (Q1); Q2 PARTIAL | 2026-08-19 | `results/conformational/fase_g_generalization_report.md` |
| **H** — Ordinal funcional H0/H1 | **INDETERMINATE** | 2026-08-19 | `results/conformational/fase_h_ordinal_functional_report.md` |
| **Micronetwork** HU-308 vs HU-433 | **INDETERMINATE** | 2026-08-20 | `results/conformational/micronetwork_modes_report.md` |

### Notas de cierre

**[OBSERVACIÓN_PROPIA]**

- **Phase G:** coordenada macro CB2_STATE_DISTANCE generaliza out-of-sample a **8GUR** (CP55,940 + Gi, ciego).
- **Phase H:** HU-433 sin fila Gi comparable forzada; AM630 = PROTEAN; proyección conformacional insuficiente para ordinal.
- **Micronetwork:** plasticidad de estado — no promover DISTINCT 6KPF como ley del par enantiomérico.
- **Retenidos por directiva PI:** GENERALIZES / INDETERMINATE / INDETERMINATE — no reinterpretar.

---

## Congelación analítica

| Ámbito | Estado |
|--------|--------|
| Retrospectivo A–E (`results/docking/`) | **CLOSED_AND_ARCHIVED** — read-only |
| Calibración multistate | **CLOSED** (2026-08-19) |
| Contract v1.0 | **ARCHIVED_HISTORICAL** — testigo 6PT0, no predictor funcional |
| de_novo / threshold / docking / diseño ortostérico | **STOP** / **PAUSED** |
| Fase I | **NO ABIERTA** — no usar ese nombre para el reanálisis |
| SMRF / 0Q.1 literatura | Documental; no reabre compute (ver bitácora extendida) |
| Núcleo mínimo | **PREGUNTA ABIERTA** — protocolo pre-registrado; **no computado** |

---

## Índice — síntesis consolidada (`docs/synthesis/`)

| Documento | Contenido |
|-----------|-----------|
| [`docs/synthesis/CB2_STRUCTURE_ATLAS.md`](docs/synthesis/CB2_STRUCTURE_ATLAS.md) | Atlas PDB: 5ZTY, 6PT0, 6KPF, 8GUS/UR/UQ/UT, 12IY/IZ/JA, 8X3L, 9U7L; Level-0; Phase F/G |
| [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) | Par enantiomérico; 8GUS experimental; Soethoudt/Hanuš; micronetwork INDETERMINATE; **contradicciones abiertas** |
| [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) | ACN/LigACN (Morales-Pastor 2025); MSM (Dutta & Shukla 2023); Trp258 no switch único; frontera MD |
| [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md) | Protocolo cerrado READ-ONLY; outcomes CORE_FOUND / NETWORK_DISTRIBUTED / INDETERMINATE |
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

## Próximo paso — protocolo luego STOP (NO Fase I)

**[HIPÓTESIS_ABIERTA]**

1. Seguir [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md) si el PI autoriza reanálisis READ-ONLY sobre datos públicos.
2. Asignar exactamente uno de: `CORE_FOUND` | `NETWORK_DISTRIBUTED` | `INDETERMINATE`.
3. **STOP** de nuevo. Sin diseño químico, sin retune Contract v1.0, sin «Fase I».

---

## Lectura recomendada al reanudar sesión

1. **Este archivo** (`RESEARCH_STATE.md`)
2. [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md)
3. [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md)
4. [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) — contradicciones abiertas
5. [`docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md`](docs/synthesis/DOCKING_LIMITS_AND_GOVERNANCE.md)

---

*Fin RESEARCH_STATE.md. Congelación analítica 2026-08-20 — documentación únicamente; objeto = núcleo mínimo (pregunta abierta).*
