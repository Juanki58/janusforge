# Red alostérica CB₂ — ACN, microswitches y frontera dinámica

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

## 1. Alcance y estatus epistemológico

**[HIPÓTESIS_ABIERTA]** Este documento sintetiza la **red de comunicación alostérica (ACN)** y los nodos microswitch relevantes para CB₂ en el contexto Janusforge. El mapa mecanístico detallado permanece en:

> [`docs/cb2_allosteric_switch_map.md`](../cb2_allosteric_switch_map.md) — **HIPÓTESIS / ACTIVE_MAPPING documental**, **≠** mecanismo confirmado, **≠** pipeline de diseño activo.

```yaml
ALLOSTERIC_FRAMEWORK: HYPOTHESIS_PENDING_CALIBRATION   # NOT TRUE
cb2_allosteric_switch_map.md: HYPOTHESIS_ONLY
DE_NOVO_GENERATION: STOP
```

---

## 2. ACN / LigACN — Morales-Pastor *et al.* 2025

**[LITERATURA_PRIMARIA]** **Referencia verificada:** Morales-Pastor, A. *et al.* «Multiple intramolecular triggers converge to preferential G protein coupling in the CB2R.» *Nature Communications* **16**, 5265 (2025). DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID 40500255; PDB **6KPC**, **5ZTY**, **6KPF**.

**[LITERATURA_PRIMARIA]** Datos públicos declarados: SI + Supplementary Data 1–4; MD en GPCRmd [dynadb/publications/1540](https://gpcrmd.org/dynadb/publications/1540/); código [GPCRmd/prefcoup_cb2r](https://github.com/GPCRmd/prefcoup_cb2r). Disponibilidad publicada ≠ descarga/cómputo local en Janusforge.

### Hallazgos centrales (literatura externa)

**[LITERATURA_PRIMARIA]**

- Mutagénesis sistemática (**360 mutaciones puntuales**) + perfilado **Gαi2** y **β-arrestin1** + simulaciones MD.
- Define **LigACN** (ligand-stabilized communication network): 100 caminos más cortos bolsillo ortostérico → sinks intracelulares; transmisión = degeneracy en esos caminos.
- La **ACN** completa transmite información del ligando al sitio intracelular; mutaciones perturbadoras convergen en motivos conservados:
  - **DRY** (TM3)
  - **Sitio de unión de sodio**
  - **CWxP** (TM6)
  - **NPxxY** (TM7)
  - **PIF** (Pro-interrupt, TM5)
- Mutantes **PrefCoup Gαi2** más cercanos a aristas de alta transmisión y con mayor conectividad vs mutantes que conservan Gαi2 + β-arrestin1 (comparación reportada en el paper).
- Panel MD: **34** mutantes (**14** PrefCoup Gαi2, **20** Coup Gαi2_βarr1) + WT; **~2.6 μs/mutante** desde **5ZTY**.
- LigACN **no** se reduce a **Trp258^6.48**: comunicación fuerte vía **TM7** (superior/inferior), inferiores de **TM2/TM3/TM6**, y motivos conservados bolsillo → interfaz intracelular.

### Corrección vs hipótesis previa de «switch único»

**[LITERATURA_PRIMARIA]** Trp258 puede ser un nodo importante (también Ganzoni 2026, DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B)), pero la evidencia publicada de LigACN **no** soporta un conmutador único en Trp258.

**[HIPÓTESIS_ABIERTA]** Pregunta frontera del programa: núcleo mínimo diferencial CB2→Gαi vs CB1 — ver [`MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](MINIMAL_CORE_REANALYSIS_PROTOCOL.md). Outcomes: `CORE_FOUND` | `NETWORK_DISTRIBUTED` | `INDETERMINATE`. **No computado** aquí.

### Implicación para Janusforge (Nivel 2–3)

**[OBSERVACIÓN_PROPIA]** Phase G = **GENERALIZES**; Phase H = **INDETERMINATE**; micronetwork = **INDETERMINATE** — macro válida, no suficiente.

**[HIPÓTESIS_ABIERTA]** La eficacia funcional y el sesgo de vía **no** son función escalar de distancia ortostérica estática. La ACN integra perturbaciones distribuidas — coherente con esos INDETERMINATE, pero **no** demostrado como ley operativa en Janusforge.

---

## 3. Trp258^6.48 — nodo importante, no switch único

**[LITERATURA_PRIMARIA]** **Referencia verificada:** Ganzoni, R. L. Z. *et al.* «Single-position ligand modifications tune CB₂R activity by targeting the toggle switch.» *Chemical Science* (2026). DOI [10.1039/D6SC00062B](https://doi.org/10.1039/D6SC00062B).

### Hallazgos centrales (literatura externa)

**[LITERATURA_PRIMARIA]**

- Derivados del scaffold **HU-308** con modificaciones en **una sola posición** acceden a un **continuo funcional** vía modulación de **Trp258^6.48**:
  - agonismo total
  - agonismo parcial
  - antagonismo neutral
  - inverse agonismo parcial
- Ligandos de baja eficacia muestran comportamiento **protean** según ensayo — subraya dependencia de contexto.
- Compuesto (S)-1 (derivado CF₃): perfil sesgado; MD sugiere contacto cercano con Trp258^6.48.

**[LITERATURA_PRIMARIA]** Esto **no** contradice la ACN distribuida de Morales-Pastor 2025: Trp258 puede modular eficacia localmente **sin** ser el único nodo necesario de la red hacia Gαi. La contradicción del par HU-308/HU-433 permanece **ABIERTA** — no armonizar post hoc ([`HU308_HU433_PARADOX.md`](HU308_HU433_PARADOX.md) §7).

### Puente con micronetwork Janusforge

**[OBSERVACIÓN_PROPIA]**

| Estado | Δ Trp258 HU-308 vs HU-433 | torsion_Trp258 |
|--------|---------------------------|----------------|
| 6PT0 | 1.32 Å | 0° (ambos) |
| 6KPF | 0.32 Å | 33.14° (ambos) |

**[OBSERVACIÓN_PROPIA]** La plasticidad de Trp258 entre estados receptor (6PT0 vs 6KPF) explica por qué el stack estático no unifica el par enantiomérico — veredicto micronetwork **INDETERMINATE**; fila Trp258 = **ABIERTA**.

---

## 3b. Paisaje MSM — Dutta & Shukla 2023 (refuerzo)

**[LITERATURA_PRIMARIA]** Dutta, S. & Shukla, D. *Commun Biol* **6**, 485 (2023). DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1); PMC **PMC10163236**. Código: [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation.git). MSM/features/trayectorias: depósito Box citado en Data availability del paper.

**[LITERATURA_PRIMARIA]**

- En CB2, **W6.48** se mueve principalmente por **rotación**; TM5/TM6/TM7 intracelulares participan en la transición activa.
- VAMPnets: **seis estados metaestables** para CB2 — no una sola transición binaria.
- La rotación del toggle tiene efecto mínimo reportado sobre movimientos intracelulares en ese análisis.

> Distinto de **Li *et al.* 2023** (DOI [10.1038/s41467-023-37112-9](https://doi.org/10.1038/s41467-023-37112-9); PMID 36922494) — cryo-EM **8GUS/8GUR/…**, no el MSM.

---

## 4. Nodos estructurales clave

### 4.1 Ser285^7.39 (microswitch TM7)

**[OBSERVACIÓN_PROPIA]** Nodo clásico de activación class-A; proxy Contract v1.0 (contacto ≤ 3.5 Å).

**[OBSERVACIÓN_PROPIA]** Calibración multistate: distancias Ser285 2.7–3.5 Å para HU-308/HU-433/O-1966 según estado (`cb2_multistate_calibration_synthesis.md` §5.1).

**[LITERATURA_PRIMARIA]** **No** demostrado como requisito universal — Morales-Pastor 2025 (DOI [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0); PMID 40500255) muestra múltiples rutas ACN hacia Gαi2 preferencial.

### 4.2 Phe183 (ECL2)

**[OBSERVACIÓN_PROPIA]** Desplazamiento ECL2 medido en Phase F (p. ej. 6KPF Δ ~27 Å vs 6PT0).

**[OBSERVACIÓN_PROPIA]** Nodo compartido entre rutas vestibulares (Ec21a) y contacto ortostérico en calibración.

**[LITERATURA_PRIMARIA]** Mutaciones F183A ablacionan PAM Ec21a en literatura (Wang *et al.* 2026, DOI [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6); PMID 42115595; PDB **9U7L**).

### 4.3 Motivos conservados (PIF, DRY, NPxxY)

**[LITERATURA_PRIMARIA]**

| Motif | Ubicación | Rol en ACN (Morales-Pastor 2025) |
|-------|-----------|----------------------------------|
| **PIF** | TM5 | Transmisión activación; perturbado en clusters PrefCoupGαi2 |
| **DRY** | TM3 | Bloqueo iónico / activación; nodo de red |
| **NPxxY** | TM7 | Acoplamiento G-proteína; contactos alterados por mutantes |
| **CWxP** | TM6 | Microswitch TM6; acoplado a Trp258 |

**[OBSERVACIÓN_PROPIA]** Estos motivos conectan la capa macro (Phase G: separación activo/inactivo) con la capa micro (Phase H/micronetwork: INDETERMINATE).

---

## 5. Modulación ECL2 / vestíbulo — precedentes externos

**[LITERATURA_PRIMARIA]**

| Modulador | Subtipo | PDB | Mecanismo reportado | Selectividad CB1/CB2 |
|-----------|---------|-----|---------------------|----------------------|
| **Ec21a** | PAM CB2 | **9U7L** | «Plug» ECL2; reduce k_off agonista; nodos S268^6.58, K278^7.32, P176/P178, F183 | Alta — no activo en CB1 |
| **ORG27569** | NAM CB1 | **6KQI** | Contacto F237^4.46; switch F155–F237 | Solo CB1 |
| **ZCZ011** | PAM CB1 | **7WV9** | Rearrangement TM2 hacia activo | Solo CB1; **sin actividad alostérica CB2 reportada** |

**[HIPÓTESIS_ABIERTA]** **Nota de gobernanza:** ORG27569 y ZCZ011 son precedentes **CB1** que refuerzan la pregunta motriz del programa (evitar equivalencia funcional CB1 al modificar CB2) — **no** son plantillas de diseño validadas para CB2 en Janusforge. Ver [`cb2_allosteric_switch_map.md`](../cb2_allosteric_switch_map.md) §Ruta B.

**[LITERATURA_PRIMARIA]** **8X3L** (Shen *et al.* 2024, DOI [10.1073/pnas.2401091121](https://doi.org/10.1073/pnas.2401091121); PDB **8X3L**): complejo CB2–G con implicaciones de selectividad entropy-driven — entra en atlas estructural, no en pipeline activo.

---

## 6. Agua, membrana y frontera MD (Nivel 3)

### Estado actual en Janusforge

| Capa | Estatus | Fuente |
|------|---------|--------|
| Macro TM3–TM6 | 🟢 **DEMOSTRADO** (Phase G GENERALIZES) | **[OBSERVACIÓN_PROPIA]** `fase_g_generalization_report.md` |
| Micro-red Trp258/Ser285/Phe183 | 🟡 **LÍMITE ESTÁTICO** (INDETERMINATE) | **[OBSERVACIÓN_PROPIA]** `micronetwork_modes_report.md`, `fase_h_ordinal_functional_report.md` |
| Dinámica (rotámeros, agua, k_off, μs) | 🔴 **FRONTERA** | Explícitamente fuera del stack estático |

### Elementos dinámicos no capturados por docking estático

**[OBSERVACIÓN_PROPIA]**

1. **Rotámeros Trp258** — torsion χ1/χ2 varía entre 6PT0 (0° en poses docked) y 6KPF (33° en co-cristal/micronetwork).
2. **Redes de agua estructurales** — eliminadas uniformemente en prep Level-0 (`cb2_multistate_calibration_synthesis.md` §3); no retenidas selectivamente.
3. **Cinética k_off** — **[LITERATURA_PRIMARIA]** mecanismo propuesto para Ec21a (Wang *et al.* 2026, DOI [10.1038/s41467-026-72923-6](https://doi.org/10.1038/s41467-026-72923-6); PMID 42115595); no medido en repo.
4. **Membrana / colesterol** — CLR404 en 6PT0; **[HIPÓTESIS_ABIERTA]** modulación lipídica documentada en literatura (Ruta C del switch map).
5. **MD μs** — **[LITERATURA_PRIMARIA]** Morales-Pastor 2025 y Ganzoni 2026 usan MD externa; **[OBSERVACIÓN_PROPIA]** **ninguna MD μs ejecutada post-congelación en Janusforge**.

**[HIPÓTESIS_ABIERTA]** **Mantra:** incorporar dinámica explícita **antes** de reclamar predictor de eficacia Gi desde geometría estática.

---

## 7. Integración con calibración multistate (proyecto)

**[OBSERVACIÓN_PROPIA]** La calibración cerrada (`docs/cb2_multistate_calibration_synthesis.md`) demostró **Categoría 1** para HU-433/O-1966: compatibilidad ortostérica conservada en 6PT0/5ZTY/6KPF.

**[HIPÓTESIS_ABIERTA]** **Esto NO invalida el mapeo alostérico.** Significa que la actividad CB₂ documentada **no requiere** invocar sitios extraortostéricos para explicar acomodación en el panel calibrado. Las rutas A/B/C del switch map permanecen como espacio hipotético futuro.

---

## 8. Hipótesis falsificable (formulación formal — no testada en repo)

**[HIPÓTESIS_ABIERTA]**

> Modulación alostérica CB2-selectiva (tipo Ec21a, vestíbulo ECL2) puede estabilizar estado funcional favorable **sin** promover señal CB1 funcionalmente equivalente.

**Estado:** hipótesis documentada en [`switch_hypothesis_allosteric_reformulation.md`](../switch_hypothesis_allosteric_reformulation.md); **no** testada experimentalmente en Janusforge.

---

## 9. Mapa de documentos

| Documento | Rol |
|-----------|-----|
| [`MINIMAL_CORE_REANALYSIS_PROTOCOL.md`](MINIMAL_CORE_REANALYSIS_PROTOCOL.md) | Protocolo cerrado READ-ONLY; pregunta núcleo mínimo CB2 vs CB1 |
| [`cb2_allosteric_switch_map.md`](../cb2_allosteric_switch_map.md) | Mapa rutas A/B/C — **HIPÓTESIS** |
| [`switch_hypothesis_allosteric_reformulation.md`](../switch_hypothesis_allosteric_reformulation.md) | Pregunta motriz alostérica (histórico; objeto actual = núcleo mínimo) |
| [`cb2_mechanistic_frontier_synthesis.md`](../cb2_mechanistic_frontier_synthesis.md) | Cadena tres capas macro/micro/dinámica |
| [`CB2_STRUCTURE_ATLAS.md`](CB2_STRUCTURE_ATLAS.md) | Plantillas PDB |
| [`DOCKING_LIMITS_AND_GOVERNANCE.md`](DOCKING_LIMITS_AND_GOVERNANCE.md) | Límites estáticos + gobernanza |
| [`../../RESEARCH_STATE.md`](../../RESEARCH_STATE.md) | Estado frontera + gobernanza YAML |

---

*Fin red alostérica CB₂. Literatura externa citada como referencia; mapa interno = hipótesis hasta validación experimental.*
