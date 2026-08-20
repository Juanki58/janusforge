# CB2 Research Roadmap — informational value order (P1–P6)

**Fecha:** 2026-08-21  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Autoridad de freeze / estado:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md)  
**Tipo:** **DOCUMENTATION ONLY** — sin docking, sin de novo, sin download/ejecución de trayectorias, sin MD nuevo

### Objetivo primario (desplazamiento)

**Caracterizar el mecanismo de control conformacional de CB2** — sea un switch local, una red distribuida, o una arquitectura estado-dependiente.  
**No** es objetivo principal “encontrar el switch.”

### Estado operativo

| Flag | Valor |
|------|--------|
| `RESEARCH_STATUS` | **`ROADMAP_ACTIVE_PREP`** |
| `DYNAMIC_REANALYSIS` | **`BLOCKED_PENDING_TRAJECTORIES`** |
| `COMPUTATION` (análisis de traj) | **PAUSED** hasta datos |
| `STATIC_LIGACN` | **`CORE_TOPOLOGICAL_ONLY`** (ancla `cfb2a51`) |
| `DOCKING` / `DE_NOVO` | **STOP** |
| Jerarquía A/B/C | Preservada (`c2869b0`); **`Q_membrana` = P5** (parked) |

Cada pregunta **abre o cierra una sola puerta**. No hay “fases a completar” — hay **valor informativo** ordenado.

### Leyenda epistemológica

| Prefijo | Significado |
|---------|-------------|
| **[OBSERVACIÓN_PROPIA]** | Datos generados por el proyecto (Phase F/G/H, micronetwork, Contract v1.0) |
| **[LITERATURA_PRIMARIA]** | Evidencia publicada — DOI / PMID / PDB |
| **[INTERNAL_REANALYSIS]** | Reanálisis sobre objetos públicos recuperados |
| **[HIPÓTESIS_ABIERTA]** | Afirmación mecanística no demostrada en el repo |
| **[INDETERMINATE]** | Bloqueado / datos incompletos |
| **[SUPPORTED_INTERPRETATION]** | Inferencia acotada a datos en mano |

---

## Mapa P1–P6 (una puerta por pregunta)

```
P1. Do static hubs survive dynamically?
P2. Do routes change across microstates?
P3. Are dynamic routes related to Gi?
P4. Does CB1 use a different architecture?
P5. Does lipid environment modify that architecture?
P6. Is there a chemical intervention that can shift it?
```

| # | Pregunta | Puerta que cierra / abre | Dependencia |
|---|----------|--------------------------|-------------|
| **P1** | ¿Persisten los hubs estáticos como nodos dinámicos? | Subred persistente vs artefactos del grafo agregado | Traj recuperables |
| **P2** | ¿Cambian las rutas entre microestados / metaestables? | Redistribución vs arquitectura fija | P1 (redes dinámicas) |
| **P3** | ¿Las rutas dinámicas se relacionan con Gi? | Topología ↔ función (sin asumir switch) | P1–P2 + mutagénesis |
| **P4** | ¿CB1 usa otra arquitectura? | Especificidad de receptor | P1–P3 (o paralelo lit.) |
| **P5** | ¿El entorno lipídico modifica esa arquitectura? | `Q_membrana` / Nivel B | Arquitectura de P1–P3 |
| **P6** | ¿Hay intervención química que la desplace? | Perturbación usable (no “mejor pose”) | Mecanismo P1–P5 |

**Prohibido ahora:** docking, de novo, MD nuevo, download de traj. Prep documental + proveniencia solamente.

---

## P1 — Do static hubs survive dynamically?

**Puerta:** ¿Los seis hubs del mapa estático son nodos dinámicos reales (persistencia **y** comunicación), o solo cuellos de botella del grafo agregado?

### Hallazgos del repo (previos)

| Evidencia | Tag | Fuente |
|-----------|-----|--------|
| Seis hubs: ALA79(2.49), ALA83(2.53), LEU287(7.41), ASN291(7.45), ASN295(7.49), ARG302(8.46) | **[INTERNAL_REANALYSIS]** | Topología LigACN WT → Sink T |
| Test A: bottleneck degree-matched **SUPPORTED** (p≈0.001) | **[INTERNAL_REANALYSIS]** | Dual validation `cfb2a51` |
| Test B: PrefCoup_Gαi2 **NOT_SUPPORTED** (p≈0.23) | **[INTERNAL_REANALYSIS]** | Mismo entregable |
| Veredicto conjunto **`CORE_TOPOLOGICAL_ONLY`** | **[INTERNAL_REANALYSIS]** | `hubs_dual_validation_report.md` |
| Hipótesis “6 hubs = núcleo funcional Gi” **eliminada** | **[INTERNAL_REANALYSIS]** | Test B — sin sobreclaim “sin relación con Gi” |

**Deliverables:**  
[`results/network_core/hubs_dual_validation_report.md`](../../results/network_core/hubs_dual_validation_report.md) ·  
[`results/network_core/static_ligacn_topology_report.md`](../../results/network_core/static_ligacn_topology_report.md)

### Literatura ancla

| Paper | Tag | DOI / PMID | Rol para P1 |
|-------|-----|------------|-------------|
| Morales-Pastor et al. 2025 | **[LITERATURA_PRIMARIA]** | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID [40500255](https://pubmed.ncbi.nlm.nih.gov/40500255/) | LigACN distribuida; MD WT/mutantes; base de hubs estáticos |
| Dutta & Shukla 2023 | **[LITERATURA_PRIMARIA]** | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) | MSM / metaestables — objeto para supervivencia dinámica |

### Protocolo epistemológico (cuando haya traj — NOT NOW)

Dos redes separadas — **no** colapsar a `W = -ln(p)`:

```
TRAJECTORIES
   ├──► PERSISTENCE NETWORK   W_contact = f(p_ij)
   └──► COMMUNICATION NETWORK W_info = f(correlation / MI / TE)
```

Sin umbral a priori >50%. Medir flujo, distribución, réplicas; luego vs null.  
**Pre-registro técnico (canónico):** [`DYNAMIC_REANALYSIS_PROTOCOL.md`](DYNAMIC_REANALYSIS_PROTOCOL.md) · hist. [`MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](MINIMAL_CORE_REANALYSIS_PROTOCOL.md) · `ARCHIVED_NEXT_CALCULATION` en `RESEARCH_STATE.md`.

**Entry point técnico P1 (andamiaje data-blind):**  
`scripts/network_core/run_dynamic_hub_persistence.py` · pipeline seco + null + self-tests: `scripts/network_core/dynamic_pipeline.py --self-test`

### Bloqueo actual

**[INDETERMINATE]** `DYNAMIC_REANALYSIS = BLOCKED_PENDING_TRAJECTORIES` · `DATA_PROVENANCE_AUDIT: PARTIAL` (GPCRmd 1540 / Box = `ENLACE_REGISTRADO`).

| Si P1… | Lectura |
|--------|---------|
| Hubs en **ambas** redes + estabilidad | Evidencia de **subred persistente** (nunca “switch”) |
| Solo persistencia, o ausencia en comunicación | Hubs = arquitectura estática, no transmisión dinámica |
| Null no separa | Sin core prefabricado |

---

## P2 — Do routes change across microstates?

**Puerta:** ¿La comunicación es una subred fija o se **redistribuye** entre metaestables / microestados?

### Hallazgos del repo (previos)

| Evidencia | Tag | Fuente |
|-----------|-----|--------|
| Phase G: macro TM3–TM6 **GENERALIZES** OOS (8GUR) | **[OBSERVACIÓN_PROPIA]** | `fase_g_generalization_report.md` → `MACRO_COORDINATE = VALIDATED_OUT_OF_SAMPLE` |
| Phase H: ordinal funcional **INDETERMINATE** | **[OBSERVACIÓN_PROPIA]** | `fase_h_ordinal_functional_report.md` |
| Micronetwork HU-308 / HU-433 **INDETERMINATE** (6PT0 enmascara / 6KPF distingue) | **[OBSERVACIÓN_PROPIA]** | `micronetwork_modes_report.md` |
| Macro ≠ eficacia fina | **[SUPPORTED_INTERPRETATION]** | Coherente con ACN distribuida |

### Literatura ancla

| Paper | Tag | DOI | Rol para P2 |
|-------|-----|-----|-------------|
| Dutta & Shukla 2023 | **[LITERATURA_PRIMARIA]** | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) | ~6 metaestables CB1/CB2; paisajes distintos |
| Morales-Pastor et al. 2025 | **[LITERATURA_PRIMARIA]** | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0) | LigACN / transmisión no reducida a un nodo |
| Ganzoni et al. 2026 | **[LITERATURA_PRIMARIA]** | [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B) | Continuo funcional vía Trp258^6.48 — nodo local, no arquitectura global |
| Smoum et al. 2015 | **[LITERATURA_PRIMARIA]** | [10.1073/pnas.1503395112](https://doi.org/10.1073/pnas.1503395112) | Paradoxo HU-308 / HU-433 — microestado abierto |

**Síntesis:** [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) · [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md)

| Si P2… | Lectura |
|--------|---------|
| Rutas estables entre estados | Arquitectura rígida (candidato a “subred”) |
| Rutas sustituidas / estado-específicas | Redistribución — `CORE_TOPOLOGICAL_ONLY` era propiedad del agregado |

---

## P3 — Are dynamic routes related to Gi?

**Puerta:** ¿Los nodos/rutas dinámicas se enriquecen hacia lectura Gαi2 (y/o β-arr), sin afirmar switch?

### Hallazgos del repo (previos)

| Evidencia | Tag | Fuente |
|-----------|-----|--------|
| PrefCoup Fisher sobre **set estático** de 6 hubs **NOT_SUPPORTED** | **[INTERNAL_REANALYSIS]** | Dual validation Test B (`cfb2a51`) |
| `CB2_Gi_NETWORK_CANDIDATE = NOT_ESTABLISHED` | Gobernanza | `RESEARCH_STATE.md` |
| `CB2_MINIMAL_GI_CORE = NOT_FOUND` | Gobernanza | Protocolo mínimo cerrado |
| Membership parcial (p.ej. N291A, R302A) ≠ atribución al set | **[SUPPORTED_INTERPRETATION]** | Safeguard B |

### Literatura ancla

| Paper | Tag | DOI / PMID | Rol para P3 |
|-------|-----|------------|-------------|
| Morales-Pastor et al. 2025 | **[LITERATURA_PRIMARIA]** | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID [40500255](https://pubmed.ncbi.nlm.nih.gov/40500255/) | ~360 mutantes; PrefCoup Gαi2 vs Coup Gαi2_βarr1; LigACN hacia sinks intracelulares |

**[HIPÓTESIS_ABIERTA]** Relación dinámica↔Gi puede existir en **otros** nodos, combinaciones, o métricas — Test B solo elimina el set estático de seis como núcleo PrefCoup.

| Si P3… | Lectura |
|--------|---------|
| Enriquecimiento dinámico + revisión humana | Posible candidatura `CB2_Gi_NETWORK_CANDIDATE` (nunca automática) |
| Sin enriquecimiento | Arquitectura física ≠ salida Gi (extiende Test B al régimen dinámico) |

---

## P4 — Does CB1 use a different architecture?

**Puerta:** ¿El control conformacional CB2 es específico de receptor o compartido con CB1?

### Estado en el repo

| Flag | Valor |
|------|--------|
| `CB1_COMPARISON` | **BLOCKED** |
| Fase G | Solo CB2 OOS (8GUR) |

### Literatura ancla

| Paper | Tag | DOI | Rol para P4 |
|-------|-----|-----|-------------|
| Dutta & Shukla 2023 | **[LITERATURA_PRIMARIA]** | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) | Paisajes CB1 vs CB2 ya contrastados en MSM publicado |

**[HIPÓTESIS_ABIERTA]** Comparación arquitectónica propia (hubs / rutas dinámicas CB1 vs CB2) requiere datos + desbloqueo explícito — no ahora.

| Si P4… | Lectura |
|--------|---------|
| Arquitectura distinta | Mecanismo CB2-específico (apoya diseño selectivo futuro) |
| Arquitectura compartida | Control a nivel de clase cannabinoid GPCR |

---

## P5 — Does lipid environment modify that architecture?

**Puerta:** `Q_membrana` — ¿hubs TM7–H8 / base TM2 intrínsecos o gobernados por microdominios de colesterol / lípidos aniónicos?

### Gobernanza (preservar)

| Elemento | Estado |
|----------|--------|
| Nivel A (canónico) | **ACTIVE_BASELINE** |
| Nivel B (colesterol / PS / CHS) | **FUTURE_PRIORITY_HYPOTHESIS** = **esta pregunta** |
| Nivel C (T / redox / pH) | **ARCHIVED_NOT_JUSTIFIED** |
| `Q_MEMBRANA` | **PARKED** — DO NOT RUN |
| `MEMBRANE_MILIEU` | **FUTURE_HYPOTHESIS** |
| Ancla A/B/C | `c2869b0` |

### Literatura ancla

| Paper | Tag | DOI / PMID | Rol para P5 |
|-------|-----|------------|-------------|
| Yeliseev et al. 2021 | **[LITERATURA_PRIMARIA]** | [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6); PMID [33580091](https://pubmed.ncbi.nlm.nih.gov/33580091/) | Colesterol / MRI-2646: basal ↑; cambio de clase de eficacia |
| Kimura et al. 2012 | **[LITERATURA_PRIMARIA]** | [10.1074/jbc.M111.268425](https://doi.org/10.1074/jbc.M111.268425) | PS / lípidos aniónicos — pliegue funcional |
| Vukoti et al. 2012 | **[LITERATURA_PRIMARIA]** | [10.1371/journal.pone.0046290](https://doi.org/10.1371/journal.pone.0046290) | CHS / PS — reconstitución / activación G |

**[HIPÓTESIS_ABIERTA]** Acoplamiento electrostático H8 (p.ej. Arg302^8.46) con lípidos aniónicos — tema de campo; **no** demostrado por Test B ni por `Q_membrana`.

Si se reanuda: **Nivel B primero**, no temperatura/oxidación/pH. Sin MD de colesterol hasta decisión conjunta.

| Si P5… | Lectura |
|--------|---------|
| Arquitectura cambia con lípido | Eje B de la hipótesis multivariable (pesos aún no cuantificados) |
| Arquitectura estable | Hubs más “intrínsecos”; membrana modula otra capa |

---

## P6 — Is there a chemical intervention that can shift it?

**Puerta:** ¿Existe una **perturbación química** que mueva la red / equilibrio hacia un estado funcional concreto **en un contexto de membrana dado**?

### Hallazgos del repo (previos)

| Evidencia | Tag | Fuente |
|-----------|-----|--------|
| Contract v1.0 demasiado restrictivo | **[OBSERVACIÓN_PROPIA]** | `ORTHOSTERIC_DESIGN = PAUSED` |
| Docking / de novo **STOP** | Gobernanza | No es camino a P6 ahora |
| Phase H / micronetwork **INDETERMINATE** | **[OBSERVACIÓN_PROPIA]** | Eficacia fina no leída desde macro/pose |
| Pregunta reformulada (parked) | Narrativa PI | No “molécula con forma dada” |

### Literatura ancla

| Paper | Tag | DOI | Rol para P6 |
|-------|-----|-----|-------------|
| Ganzoni et al. 2026 | **[LITERATURA_PRIMARIA]** | [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B) | Modificaciones de una posición en scaffold HU-308 → continuo funcional vía Trp258 |
| Smoum et al. 2015 | **[LITERATURA_PRIMARIA]** | [10.1073/pnas.1503395112](https://doi.org/10.1073/pnas.1503395112) | Enantiómeros HU-308/HU-433 — Ki ≠ potencia biológica |
| Morales-Pastor et al. 2025 | **[LITERATURA_PRIMARIA]** | [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0) | Muchos puntos de entrada a LigACN — no un solo switch químico |
| Yeliseev et al. 2021 | **[LITERATURA_PRIMARIA]** | [10.1038/s41598-021-83245-6](https://doi.org/10.1038/s41598-021-83245-6) | Misma molécula, clase distinta según colesterol |

**Explicitamente NO demostrado:** estrategia química usable ya en mano.

| Si P6… | Lectura |
|--------|---------|
| Perturbación reproduce desplazamiento de red/estado | Intervención alineada con mecanismo (P1–P5) |
| No | Química sigue mal formulada o mecanismo incompleto |

---

## Cómo encajan Phase G/H, seis hubs y dual validation

```
Phase G (MACRO) 🟢 GENERALIZES
        │
        ▼
Phase H / micronetwork 🟡 INDETERMINATE  ──► alimenta P2 (microestados)
        │
        ▼
Static LigACN + 6 hubs 🟢 bottlenecks
        │
        ▼
Dual validation cfb2a51
  A 🟢 topological · B 🔴 PrefCoup
  → CORE_TOPOLOGICAL_ONLY ──► cierra “6 hubs = switch Gi”
        │
        ▼
P1–P3 (dinámica / Gi)  BLOCKED_PENDING_TRAJECTORIES
P4 (CB1)               BLOCKED
P5 (lípido)            Q_membrana PARKED = Nivel B
P6 (química)           STOP docking/de novo hasta mecanismo
```

**Anclas de linaje:** `cfb2a51` (dual-test → topología-only) · `c2869b0` (A/B/C + `Q_membrana`) · `2a1193c` / tip docs freeze.

---

## Índice cruzado

| Documento | Uso en roadmap |
|-----------|----------------|
| [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) | Autoridad de flags / freeze |
| [`CB2_ALLOSTERIC_NETWORK.md`](CB2_ALLOSTERIC_NETWORK.md) | Morales-Pastor, Dutta–Shukla, Trp258 |
| [`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md) | Smoum / Ganzoni; contradicciones abiertas |
| [`MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](MINIMAL_CORE_REANALYSIS_PROTOCOL.md) | Protocolo dinámico (dos redes; sin umbral 50%) |
| [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md) | PDB / Level-0 / Phase F/G |
| [`DOCKING_LIMITS_AND_GOVERNANCE.md`](DOCKING_LIMITS_AND_GOVERNANCE.md) | Por qué P6 ≠ docking score |
| Dual validation report | Ancla `cfb2a51` — entrada a P1/P3 |

---

## Próximo paso (prep only)

1. Mantener **`ROADMAP_ACTIVE_PREP`** — documentación y proveniencia.  
2. **No** descongelar `DYNAMIC_REANALYSIS` hasta traj recuperables.  
3. **No** abrir P5/P6 compute; **no** docking / de novo / MD.  
4. Al reanudar: P1 primero (ambas redes), una puerta a la vez.

---

*Fin CB2_RESEARCH_ROADMAP.md — P1–P6 por valor informativo; objetivo = mecanismo de control conformacional CB2.*
