# RESEARCH STATE — Janusforge CB₂ (congelación analítica)

**Fecha:** 2026-08-20  
**Rama:** `feat/cb2-hubs-functional-topology-test` (desde `task/static-ligacn-topology` @ `5365ab4`)  
**Tipo:** Dual validation CLOSED (topología × PrefCoup) + topología estática LigACN **CLOSED**; núcleo dinámico / función Gαi2 sigue bloqueado  
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
DOCKING: STOP
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
NEW_SEARCH: STOP
CONTRACT_v1.0: ARCHIVED_HISTORICAL
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
MODO: CLOSED_DUAL_VALIDATION / READ_ONLY_DATA
STATIC_GRAPH_ANALYSIS: CLOSED
DUAL_VALIDATION_HUBS: CLOSED
SINK_SET_T: EXTRACTED  # Arg131(3x50), Asp240(6x30), Ser303(8x47), Ser69(2x39)
CB2_MINIMAL_GI_CORE: BLOCKED_PENDING_DYNAMIC_VALIDATION
CB1_COMPARISON: BLOCKED
DATA_PROVENANCE: PARTIAL  # SI/SD1–3 local; traj/Box = ENLACE_REGISTRADO
TECHNICAL_SEARCH_TRAJ: STOP
ACTIVE_ACTION: HUMAN_REVIEW_JOINT  # TOTAL STOP after dual validation
# Explicit: NOT Fase I; no CB2_Gi_NETWORK_CANDIDATE (requires CORE_CANDIDATE_SUPPORTED)
RESEARCH_STATUS: DUAL_VALIDATION_CLOSED__CORE_TOPOLOGICAL_ONLY
```

**[OBSERVACIÓN_PROPIA]** Diseño químico / de_novo / docking / Phase I **STOP**.  
**[INTERNAL_REANALYSIS]** Dual validation de 6 hubs fijos → **`CORE_TOPOLOGICAL_ONLY`** (arquitectura de red sin evidencia funcional PrefCoup suficiente). Topología ≠ necesidad causal Gi. Prohibido: “switch”, “núcleo universal probado”, `CORE_FOUND`.

---

## Entregable cerrado — dual validation hubs (A/B)

**Informe:** [`results/network_core/hubs_dual_validation_report.md`](results/network_core/hubs_dual_validation_report.md)  
**JSON:** [`results/network_core/hubs_dual_validation_report.json`](results/network_core/hubs_dual_validation_report.json)  
**Script:** [`scripts/network_core/test_hubs_dual_validation.py`](scripts/network_core/test_hubs_dual_validation.py)  
**Literatura PRIMARY:** Morales-Pastor et al. DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)

| Campo | Valor |
|-------|--------|
| Hubs (fijos) | ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46) |
| Test A | **`TOPOLOGICAL_BOTTLENECK_SUPPORTED`** — primary `%Disconn` p≈0.001 vs 1000 exact (in,out)-degree-matched nulls |
| Test B | **`FUNCTIONAL_ENRICHMENT_NOT_SUPPORTED`** — Fisher PrefCoup_Gi p≈0.23 (membership ≠ atribución estadística; mutaciones listadas por separado) |
| Test C | Skipped (requiere A∧B) |
| Combined | **`CORE_TOPOLOGICAL_ONLY`** — network architecture without sufficient functional evidence |
| Formal name | *not assigned* (`CB2_Gi_NETWORK_CANDIDATE` only if `CORE_CANDIDATE_SUPPORTED`) |

**Safeguard B:** position membership (p.ej. N291A, R302A ∈ PrefCoup_Gi tras filtro expr.) ≠ sesgo estadísticamente atribuible al *set* vs background.

---

## Entregable cerrado — topología estática

**Informe lead:** [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md)  
**Métricas:** [`results/network_core/static_ligacn_topology_metrics.json`](results/network_core/static_ligacn_topology_metrics.json)  
**Veredicto:** [`results/network_core/static_topological_verdict.json`](results/network_core/static_topological_verdict.json)  
**Script:** [`scripts/network/analyze_static_ligacn_topology.py`](scripts/network/analyze_static_ligacn_topology.py)

| Campo | Valor |
|-------|--------|
| `STATIC_TOPOLOGICAL_BOTTLENECKS` | **`TOPOLOGICAL_HUBS_IDENTIFIED`** |
| Source Set S (verificado) | `8D0:1`, `SER:285`, `PHE:87` |
| AUSENTE (no sustituidos) | `TRP:258`, `PHE:183` (fuera de WT_degeneracy; sí hay columnas `*-LIG` en SD2 Inactive) |
| Sink Set T | ARG:131, ASP:240, SER:303, SER:69 (4/4 reachable) |
| Hubs enriquecidos (no-S/T) | ALA:83, ALA:79, ASN:291, ASN:295, LEU:287, ARG:302 |
| Límite | Solo propiedades de la red agregada publicada — **no** causalidad Gi; arquitectura candidata ≠ switch |

**Futuro parked (no ahora):** conservación dinámica de hubs + enriquecimiento en posiciones que alteran preferentemente Gαi2 — ver § *Separación en cuatro niveles*.

---

## Separación en cuatro niveles (directiva PI — cierre epistemológico)

**Naming:** no decir «switch found». El programa pasó de buscar un *switch* único a identificar una **arquitectura candidata de transmisión de señal**. Hubs estáticos ≠ microswitches automáticos.

| # | Nivel | Dominio | Pregunta | Estatus |
|---|-------|---------|----------|---------|
| 1 | **ESTADO GLOBAL** | TM3–TM6 | ¿Puede CB2 adoptar la conformación activa? | 🟢 **Sí** — generalización OOS (Phase G) |
| 2 | **MICROESTADO** | Trp258 / Ser285 / ECL2 | ¿Cómo modifica cada ligando esa conformación? | 🟡 Dependiente del estado; sin pose rígida universal (micronetwork) |
| 3 | **RED DE COMUNICACIÓN** | TM7 / TM2 / NPxxY / H8 | ¿Hacia dónde se propaga la perturbación? | 🟢 Hubs topológicos estáticos identificables (`STATIC_TOPOLOGICAL_BOTTLENECKS` = `TOPOLOGICAL_HUBS_IDENTIFIED`: ALA79, ALA83, LEU287, ASN291, ASN295, ARG302). S verificado **sin** forzar TRP258/PHE183 (**AUSENTE**) |
| 4 | **FUNCIÓN** | Gαi2; CB1 vs CB2 | ¿Controlan realmente esos hubs a Gαi2 y de forma distinta en CB1? | ⚪ Dual A/B: **B NOT_SUPPORTED** (PrefCoup Fisher n.s.) — frontera real permanece; veredicto conjunto **`CORE_TOPOLOGICAL_ONLY`** |

**[HIPÓTESIS_ABIERTA]** Nivel 4 permanece abierto: bottleneck topológico estático (A SUPPORTED) **no** implica enriquecimiento PrefCoup del set (B NOT_SUPPORTED). CB1 sigue `BLOCKED`.

### Dual validation (CLOSED — 2026-08-20)

Hubs fijos × knockout degree-matched (A) × SD1 PrefCoup Fisher (B) → **`CORE_TOPOLOGICAL_ONLY`**.  
Deliverable: `results/network_core/hubs_dual_validation_report.md`. **TOTAL STOP** — joint human review.

### Experimento frontera dinámica (parked — NO EJECUTAR)

> ¿Los hubs topológicos estáticos se conservan en dinámica?

**No es:** otro docking, librería química, ni retune de Contract.

**Estado gobernanza:** `CB2_MINIMAL_GI_CORE = BLOCKED_PENDING_DYNAMIC_VALIDATION` · `CB1_COMPARISON = BLOCKED` · `DUAL_VALIDATION_HUBS = CLOSED`

**Protocolo (histórico / dinámico):** [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md)  
**Informe previo (core dinámico INDETERMINATE):** [`results/network_core/cb2_minimal_gi_core_report.md`](results/network_core/cb2_minimal_gi_core_report.md)  
**Auditoría:** [`results/network_core/data_audit.md`](results/network_core/data_audit.md)  
**Proveniencia:** [`results/network_core/provenance_recovery_log.md`](results/network_core/provenance_recovery_log.md)

---

## Diagrama de estado

```
LITERATURA / DATOS PÚBLICOS
        │
        ├── 1 ESTADO GLOBAL (TM3–TM6)     🟢 Phase G OOS
        ├── 2 MICROESTADO (Trp258/Ser285/ECL2)  🟡 state-dependent
        ├── CB2 LigACN SD1–3 local ✓
        ├── Sink Set T EXTRACTED ✓
        └── traj GPCRmd / Box MSM = ENLACE only
                  │
                  ▼
        3 RED DE COMUNICACIÓN (estática)
        STATIC LigACN TOPOLOGY  →  CLOSED
        DUAL VALIDATION A/B     →  CLOSED
        verdict: CORE_TOPOLOGICAL_ONLY
        (A bottleneck SUPPORTED; B PrefCoup NOT)
        ≠ switch; no CB2_Gi_NETWORK_CANDIDATE
                  │
                  ▼
        4 FUNCIÓN (Gαi2 / CB1) — FRONTERA
        DYNAMIC MINIMAL Gi CORE
        BLOCKED_PENDING_DYNAMIC_VALIDATION
                  │
                  ▼
                 TOTAL STOP (joint human review)
```

---

## Registro provisional — tabla de resultados (literatura / abierto)

**[LITERATURA_PRIMARIA]** / **[HIPÓTESIS_ABIERTA]** / **[INTERNAL_REANALYSIS]**

| Pregunta | Estado |
|----------|--------|
| ¿Hay una red CB2→efector intracelular? | 🟢 Establecido por literatura (ACN/LigACN; Morales-Pastor 2025, DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID 40500255) |
| ¿Qué hubs/bottlenecks topológicos tiene LigACN WT estático hacia Sink T? | 🟢 **`TOPOLOGICAL_HUBS_IDENTIFIED`** — ver `static_ligacn_topology_report.md` (**no** causal; arquitectura candidata, no switch) |
| ¿La red está concentrada en Trp258/Ser285? | 🔴 No como “único switch”; Trp258 **AUSENTE** del grafo WT_degeneracy; Ser285 es miembro de S (contacto ligando verificado) |
| ¿TM7 participa especialmente en ruta agonismo/Gi? | 🟢 Apoyado (literatura + hubs ASN:291/295, LEU:287, ARG:302 en mapa estático) |
| ¿CB2 posee una única coordenada conformacional suficiente para Gi? | 🔴 No demostrado |
| ¿Los 6 hubs son bottleneck topológico degree-matched? | 🟢 **A SUPPORTED** (`TOPOLOGICAL_BOTTLENECK_SUPPORTED`, p≈0.001) — ver dual validation |
| ¿El set está enriquecido en PrefCoup_Gαi2 (Fisher, expr≥25%)? | 🔴 **B NOT_SUPPORTED** (p≈0.23) — membership parcial ≠ atribución estadística |
| ¿Candidate conjunto topología∧función? | 🔴 **`CORE_TOPOLOGICAL_ONLY`** — no `CB2_Gi_NETWORK_CANDIDATE` |
| ¿Los hubs estáticos controlan Gαi2 y difieren en CB1? | ⚪ **Frontera real** — `BLOCKED_PENDING_DYNAMIC_VALIDATION` |

---

## Mapa epistemológico (cuatro niveles — PI)

| Nivel | Dominio | Estatus | Evidencia clave |
|-------|---------|---------|-----------------|
| **1 — ESTADO GLOBAL** | TM3–TM6 | 🟢 **Sí (OOS)** | **[OBSERVACIÓN_PROPIA]** Phase G: 8GUR (2.32) ≈ 6KPF (2.30) ≪ 5ZTY (3.95); veredicto **GENERALIZES** |
| **2 — MICROESTADO** | Trp258 / Ser285 / ECL2 | 🟡 **Estado-dependiente** | **[OBSERVACIÓN_PROPIA]** Micronetwork **INDETERMINATE** (6PT0 identical / 6KPF distinct); sin pose rígida universal; Phase H **INDETERMINATE** |
| **3 — RED DE COMUNICACIÓN** | TM7 / TM2 / NPxxY / H8 | 🟢 **Hubs estáticos ID** | **[INTERNAL_REANALYSIS]** `TOPOLOGICAL_HUBS_IDENTIFIED` (ALA79, ALA83, LEU287, ASN291, ASN295, ARG302); S sin forzar TRP258/PHE183; **≠** microswitches |
| **4 — FUNCIÓN** | Gαi2; diferencia CB1 | ⚪ **Frontera** | **[HIPÓTESIS_ABIERTA]** No demostrado; `BLOCKED_PENDING_DYNAMIC_VALIDATION` / `CB1_COMPARISON = BLOCKED` |

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
| Proveniencia de datos | **PARTIAL** — SD1–3 + MOESM2 + Sink T local; traj/Box ENLACE_REGISTRADO |
| Topología estática LigACN | **CLOSED** — `STATIC_TOPOLOGICAL_BOTTLENECKS = TOPOLOGICAL_HUBS_IDENTIFIED` |
| Núcleo mínimo dinámico CB2→Gi | **BLOCKED_PENDING_DYNAMIC_VALIDATION** — el mapa estático **no** lo responde |

---

## Índice — síntesis consolidada (`docs/synthesis/`)

| Documento | Contenido |
|-----------|-----------|
| [`docs/synthesis/CB2_STRUCTURE_ATLAS.md`](docs/synthesis/CB2_STRUCTURE_ATLAS.md) | Atlas PDB: 5ZTY, 6PT0, 6KPF, 8GUS/UR/UQ/UT, 12IY/IZ/JA, 8X3L, 9U7L; Level-0; Phase F/G |
| [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) | Par enantiomérico; 8GUS experimental; Soethoudt/Hanuš; micronetwork INDETERMINATE; **contradicciones abiertas** |
| [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md) | ACN/LigACN (Morales-Pastor 2025); MSM (Dutta & Shukla 2023); Trp258 no switch único; frontera MD |
| [`docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](docs/synthesis/MINIMAL_CORE_REANALYSIS_PROTOCOL.md) | Protocolo dinámico (histórico); core sigue `BLOCKED_PENDING_DYNAMIC_VALIDATION` |
| [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md) | Topología estática LigACN→T (**CLOSED**) |
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

## Próximo paso — STOP para revisión humana

**[OBSERVACIÓN_PROPIA]**

1. Cuatro niveles registrados — niveles 1–3 con estatus; nivel 4 = frontera Gαi2 / CB1 (**no** ejecutada).
2. Topología estática **CLOSED** — arquitectura candidata de transmisión de señal; hubs ≠ microswitches. Ver `static_ligacn_topology_report.md`.
3. Experimento frontera **parked** (conservación dinámica + enriquecimiento Gαi2) — `CB2_MINIMAL_GI_CORE = BLOCKED_PENDING_DYNAMIC_VALIDATION`; sin recovery traj/MSM salvo autorización PI.
4. **STOP.** Sin docking, sin de novo, sin librería química, sin «Fase I», sin retune Contract v1.0.

---

## Lectura recomendada al reanudar sesión

1. **Este archivo** (`RESEARCH_STATE.md`) — sección *Separación en cuatro niveles*
2. [`results/network_core/static_ligacn_topology_report.md`](results/network_core/static_ligacn_topology_report.md)
3. [`results/network_core/provenance_recovery_log.md`](results/network_core/provenance_recovery_log.md)
4. [`docs/synthesis/CB2_ALLOSTERIC_NETWORK.md`](docs/synthesis/CB2_ALLOSTERIC_NETWORK.md)
5. [`docs/synthesis/HU308_HU433_PARADOX.md`](docs/synthesis/HU308_HU433_PARADOX.md) — contradicciones abiertas

---

*Fin RESEARCH_STATE.md. 2026-08-20 — cierre epistemológico (cuatro niveles); static topology CLOSED; función Gαi2 = frontera; dynamic Gi core BLOCKED_PENDING_DYNAMIC_VALIDATION.*
