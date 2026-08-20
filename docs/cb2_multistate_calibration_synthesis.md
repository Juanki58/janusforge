# CB₂ — Síntesis de cierre: calibración multiconformacional

**Fecha de cierre:** 2026-08-19  
**Modo:** Documental / READ-ONLY — **sin docking, sin moléculas nuevas, sin retune de umbrales, sin commit**  
**Audiencia:** PI y colaboradores que citen el estado del programa Janusforge

---

## 1. Propósito y alcance

Este documento **cierra formalmente** la etapa de calibración multiconformacional CB₂ iniciada en el marco epistemológico de [`epistemic_balance_calibration_2026-08-19.md`](epistemic_balance_calibration_2026-08-19.md) y ejecutada en [`results/docking/cb2_multistate_calibration.md`](../results/docking/cb2_multistate_calibration.md) (JSON: [`cb2_multistate_calibration.json`](../results/docking/cb2_multistate_calibration.json)).

**Pregunta respondida:**

> ¿Qué conformaciones del receptor CB₂ permiten explicar los positivos conocidos (HU-308, HU-433, O-1966) que el modelo estático Contract v1.0 / 6PT0 no explicaba?

**Pregunta explícitamente NO respondida (prohibida):**

> ¿Qué parámetros hay que cambiar para que HU-433 y O-1966 pasen Contract v1.0?

Ver §3 (calibrar ≠ retocar) en el balance epistemológico.

---

## 2. Gobernanza de cierre

```yaml
# ESTADO DEL PROYECTO TRAS CIERRE CALIBRACIÓN MULTI-ESTADO (2026-08-19)
CALIBRATION_MULTI_STATE: CLOSED
CONTRACT_v1.0: FROZEN          # testigo histórico / clasificador hiper-restringido — preservar, NO retunear
ALLOSTERIC_FRAMEWORK: HYPOTHESIS_PENDING_CALIBRATION   # NOT TRUE; NOT refutado como línea de investigación
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
```

| Parámetro | Estado | Nota |
|-----------|--------|------|
| `CALIBRATION_MULTI_STATE` | **CLOSED** | Run completado 2026-08-19 08:58 UTC; síntesis en este documento |
| `CONTRACT_v1.0` | **FROZEN** | Permanece como **testigo histórico** del observador estático 6PT0 + proxies THCV/HU-308. No se retunea |
| `ALLOSTERIC_FRAMEWORK` | **HYPOTHESIS_PENDING_CALIBRATION** | No se eleva a TRUE; tampoco se descarta la línea alostérica como investigación futura |
| `DE_NOVO_GENERATION` | **STOP** | Sin generación química |
| `THRESHOLD_MODIFICATION` | **STOP** | Sin modificación de umbrales contractuales |

**Mantra obligatorio:**

```text
CALIBRAR ≠ RETOCAR

Calibración   = explorar espacio conformacional del receptor (observador)
Retocar       = mover reglas hasta que casos incómodos desaparezcan (overfitting)
```

El Contract v1.0 (`configs/thcv_design_constraints.yaml`, `docs/thcv_design_constraints.md`) **permanece congelado** como registro histórico de la hipótesis geométrica estática v1.0. Este cierre **no** implica PASS retroactivo de HU-433 / O-1966 bajo v1.0.

---

## 3. Integridad Level-0 (receptores y controles)

Verificación formal registrada en el audit biofísico. Correcciones críticas respecto a etiquetas PI originales:

| PDB | Etiqueta PI (corregida) | Anotación experimental verificada | Res (Å) | Estado |
|-----|-------------------------|-----------------------------------|---------|--------|
| **6PT0** | Activo WIN + Gi | CB2 agonist-bound (WIN 55,212-2 / WI5) + Gi cryo-EM | 3.2 | **VERIFIED** — referencia Contract v1.0 |
| **5ZTY** | ~~Activo Gi~~ → **Inactivo/antagonista** | CB2 inactive/antagonist (AM10257 / 9JU) crystal; T4L fusion (Li et al. Cell 2019) | 2.8 | **VERIFIED** — PI label «activo Gi» **contradice** anotación PDB; procesado como estado inactivo |
| **6KPF** | Activo cryo-EM | CB2 agonist-bound (E3R) + Gi cryo-EM | 2.9 | **VERIFIED** |
| **5VEU** | ~~Inactivo antagonista~~ → **EXCLUIDO** | **NOT CB2** — Human Cytochrome P450 3A5 (CYP3A5, ligando RIT/HEM) | 2.91 | **BLOCKED** — ID erróneo; columna permanece vacía sin sustitución automática |

**Control negativo SR141716 (Rimonabant):** identidad **INDETERMINATE** (InChIKey mismatch PubChem vs esperado). Todas las celdas de acomodación: **INDET**. No se infiere veredicto estructural a partir de este control en este run.

**Protocolo de prep uniforme (todos los estados VERIFIED):** monómero CB2; eliminación uniforme de aguas, iones, ligando co-cristalizado, lípidos, Gi/Gβγ, nanobodies; protonación Meeko pH 7.4. Prohibida retención selectiva de aguas estructurales.

---

## 4. Contexto Phase E — discrepancia lit-activo vs Contract v1.0

Antes de la calibración multistate, Phase E (`results/docking/screening_patents_thcv_fase_e.md`) registró:

| Compuesto | Rol | Experimental (lit) | STRUCTURAL (6PT0) | PERIPHERAL | Cuadrante | GLOBAL |
|-----------|-----|-------------------|-------------------|------------|-----------|--------|
| **HU-308** | Referencia gold | CB₂ agonista; Ki ~22.7 nM | *(referencia Exam A)* | — | — | — |
| **HU-433** | Caso calibración | CB₂ agonista; Ki 12.2 nM | **FAIL** | **FAIL** (TPSA 38.69 Å²) | **Q4** | **FAIL** |
| **O-1966** | Caso calibración | CB₂ agonista parcial; Ki 23±2.1 nM | **FAIL** | **FAIL** (TPSA 38.69 Å²) | **Q4** | **FAIL** |

**Sub-checks estructurales Phase E (6PT0 estático):**

- **HU-433:** CB1 C9/C11 Δvol 6.0 Å (>1.0); CB2 C3 occupancy 6.75 Å (>2.5); TPSA 38.69 Å² (<70).
- **O-1966:** CB1 C9/C11 Δvol 1.5 Å (>1.0); CB2 C3 occupancy 7.28 Å (>2.5); TPSA 38.69 Å² (<70).

**Interpretación previa (balance epistemológico §6):** la discrepancia lit-activo ↔ FAIL contractual señalaba límite del observador estático, **no** error de molécula ni mecanismo alostérico demostrado.

**Resolución post-calibración:** el run multistate demuestra que HU-433 y O-1966 **sí** alcanzan acomodación ortostérica favorable (ACOMODADO Vina) en 6PT0, 5ZTY y 6KPF. La discrepancia Phase E se explica por **criterios adicionales congelados v1.0** (ocupación sub-box C3, umbrales Ser285/proxies geométricos, TPSA, Δvol CB1), **no** por imposibilidad de pose ortostérica rígida en la cavidad CB₂.

Ver [`epistemic_balance_calibration_2026-08-19.md`](epistemic_balance_calibration_2026-08-19.md) §6–§8 y [`switch_hypothesis_allosteric_reformulation.md`](switch_hypothesis_allosteric_reformulation.md) §3–§4.

---

## 5. Matriz de scores — resumen obligatorio 4×4

Protocolo congelado: grid 20×20×20 Å; centro COM ligando co-cristalizado; Vina seed 42; exhaustiveness 16; num_modes 9; pH 7.4.

| Ligando | 6PT0 (agonist-bound) | 5ZTY (inactive/antagonist) | 6KPF (agonist-bound) | 5VEU (CYP3A5 — BLOCKED) |
|---------|----------------------|----------------------------|----------------------|---------------------------|
| **HU-308** | −9.46 / **ACOMODADO** | −9.50 / **ACOMODADO** | −9.58 / **ACOMODADO** | BLOCKED |
| **HU-433** | −9.87 / **ACOMODADO** | −9.24 / **ACOMODADO** | −9.26 / **ACOMODADO** | BLOCKED |
| **O-1966** | −8.91 / **ACOMODADO** | −9.37 / **ACOMODADO** | −9.74 / **ACOMODADO** | BLOCKED |
| **SR141716** | INDET | INDET | INDET | INDET |

> **Advertencia interpretativa:** «mejor score» ≠ «fármaco activo». El resultado principal es convergencia/divergencia de acomodación estructural entre positivos de literatura.

### 5.1 Contactos clave (mejor modo por celda)

| Ligando | Estado | Score | Ser285 (Å) | Trp258 (Å) | Phe183 (Å) | min heavy (Å) |
|---------|--------|-------|------------|------------|------------|---------------|
| HU-308 | 6PT0 | −9.47 | 3.33 | 5.15 | 3.64 | 2.54 |
| HU-308 | 5ZTY | −9.50 | 3.64 | 3.67 | 3.42 | 2.39 |
| HU-308 | 6KPF | −9.58 | 2.70 | 4.20 | 3.43 | 2.70 |
| HU-433 | 6PT0 | −9.87 | 3.06 | 6.47 | 3.48 | 3.06 |
| HU-433 | 5ZTY | −9.24 | 3.50 | 6.97 | 3.40 | 3.24 |
| HU-433 | 6KPF | −9.26 | 3.06 | 4.51 | 3.43 | 2.42 |
| O-1966 | 6PT0 | −8.91 | 3.18 | 4.97 | 3.50 | 3.18 |
| O-1966 | 5ZTY | −9.37 | 4.02 | 3.64 | 3.69 | 3.17 |
| O-1966 | 6KPF | −9.74 | 2.75 | 3.38 | 3.39 | 2.60 |

**Mejor estado explicado por ligando:**

| Ligando | Mejor estado | Score | Nota |
|---------|--------------|-------|------|
| HU-308 | 6KPF | −9.58 | Referencia gold — calibración positiva |
| HU-433 | 6PT0 | −9.87 | Caso calibración — discrepancia Contract v1.0/6PT0 |
| O-1966 | 6KPF | −9.74 | Caso calibración — discrepancia Contract v1.0/6PT0 |

### 5.2 Movilidad ECL2 (ensemble experimental)

Desplazamiento Cα tras alineación Kabsch (referencia 6PT0): Phe183 máx. 0.97 Å; Ile110 máx. 0.90 Å entre 6PT0 / 5ZTY / 6KPF. **No** se alcanza umbral de INDUCED-FIT PARCIAL documentado por movilidad ECL2. Las acomodaciones observadas **no** requieren invocar plasticidad local extrema para explicarse.

---

## 6. Conclusiones obligatorias de cierre

### 6.1 Acomodación demostrada

**HU-308, HU-433 y O-1966 convergen en ACOMODADO** sobre los tres estados CB₂ verificados (**6PT0, 5ZTY, 6KPF**). La cavidad ortostérica CB₂ es **plena y compatible** con los tres agonistas de literatura, tanto en conformaciones agonista-bound (6PT0, 6KPF) como en el estado inactivo/antagonista cristalino (5ZTY).

Patrón conformacional: **convergencia detectada** — los tres comparten acomodación favorable en `['6PT0', '5ZTY', '6KPF']` (JSON `discrepancy_hu433_o1966.hu308/433/o1966_accommodated_states`).

### 6.2 Naturaleza de Contract v1.0

Contract v1.0 codifica **filtros geométricos/de distancia arbitrarios** (sub-box C3, proximidad Ser285, Δvol CB1 C9/C11, TPSA ≥ 70 Å², etc.) derivados de una **hipótesis estática concreta** (snapshot 6PT0 + marco HU-308). Estos criterios son **restricciones del observador v1.0**, **no condiciones necesarias** de unión CB₂ ni de activación funcional.

El FAIL Phase E de HU-433 / O-1966 bajo v1.0 **no demuestra** que esas moléculas «no puedan unirse ortostéricamente»; demuestra que **no satisfacen el paquete geométrico congelado** que el contrato exige.

### 6.3 Precaución alostérica

**Descartar** la afirmación de que la actividad de HU-433 / O-1966 **requiere necesariamente** un mecanismo alostérico. La evidencia actual de calibración multistate apoya la **Categoría 1** del árbol de discriminación:

> **Compatibilidad ortostérica conservada entre estados**

(`discrepancy_hu433_o1966.category_id: 1`)

`ALLOSTERIC_FRAMEWORK` permanece en **`HYPOTHESIS_PENDING_CALIBRATION`**:

- **NOT TRUE** — no hay evidencia computacional directa de modulación alostérica para estos compuestos en este run.
- **NOT refutado** como línea de investigación futura — el marco alostérico sigue siendo pregunta abierta del workstream SWITCH (ver [`switch_hypothesis_allosteric_reformulation.md`](switch_hypothesis_allosteric_reformulation.md)), simplemente **no es necesario** para explicar la acomodación ortostérica observada de estos activos.

Las categorías 2–4 del árbol (preferencia por conformación alternativa, induced-fit, alosteria/vestibular) **no** se seleccionan como explicación primaria del panel calibrado.

### 6.4 Integridad Level-0 reafirmada

- **5VEU excluido:** PDB erróneo (CYP3A5 ≠ CB2); columna BLOCKED sin sustitución.
- **5ZTY corregido:** antagonista AM10257, **no** activo Gi acoplado.
- **SR141716:** control INDET por identidad química no verificada; sin inferencia estructural.

---

## 7. Cuatro posibilidades mutuamente excluyentes — veredicto

| # | Hipótesis | Evidencia en calibración multistate | Veredicto |
|---|-----------|-------------------------------------|-----------|
| 1 | Compatibilidad ortostérica conservada entre estados | HU-433 y O-1966 ACOMODADO en 6PT0, 5ZTY, 6KPF; convergencia con HU-308 | **SELECCIONADA** |
| 2 | Preferencia por conformación activa alternativa | Mejor score HU-433→6PT0; O-1966→6KPF; pero ACOMODADO en todos | Secundaria — no explica FAIL v1.0 |
| 3 | Plasticidad local / induced fit | ECL2 no móvil suficiente (≤1 Å); no requerido | **No soportada** como explicación principal |
| 4 | Sin explicación ortostérica → alostérica/vestibular | Contradicha por ACOMODADO universal en cavidad ortostérica | **Descartada** para este panel |

---

## 8. Implicaciones epistemológicas

1. **Contract v1.0 NO falsificado** — Q1 = 0 en paneles A–E se mantiene; el contrato sigue siendo un clasificador hiper-restrictivo válido como **testigo histórico**, no como teorema de activación CB₂.
2. **Observador estático insuficiente** — un solo snapshot 6PT0 + reglas v1.0 **no agota** el espacio de poses ortostéricas compatibles con agonismo CB₂ documentado; la calibración multistate lo demuestra empíricamente **sin retunear**.
3. **Desacople de capas confirmado** — estructural (Vina/acomodación) ≠ periférico (TPSA) ≠ funcional (Contract GLOBAL). Ver `audit_qiu_decoupled_layers.md`.
4. **Próximo paso NO es retune** — cualquier avance requiere validación experimental (afinidad, eficacia, PK) o nuevas hipótesis **fuera** de Contract v1.0, no ajuste post-hoc de umbrales.

---

## 9. Trazabilidad

| Tema | Ruta |
|------|------|
| **Este documento (cierre)** | `docs/cb2_multistate_calibration_synthesis.md` |
| Audit biofísico multistate | `results/docking/cb2_multistate_calibration.md` |
| JSON machine-readable | `results/docking/cb2_multistate_calibration.json` |
| Poses docked | `results/docking/cb2_multistate_poses/` |
| Balance epistemológico | `docs/epistemic_balance_calibration_2026-08-19.md` |
| Switch / alosteria | `docs/switch_hypothesis_allosteric_reformulation.md` |
| Phase E — discrepancia origen | `results/docking/screening_patents_thcv_fase_e.md` |
| Exam A — HU-308 gold | `results/docking/benchmark_gold_exam_a.md` |
| Contract v1.0 congelado | `configs/thcv_design_constraints.yaml`, `docs/thcv_design_constraints.md` |
| Desacople capas | `results/docking/audit_qiu_decoupled_layers.md` |

---

*Fin `docs/cb2_multistate_calibration_synthesis.md`. Documento de cierre de calibración multiconformacional CB₂ — READ-ONLY.*
