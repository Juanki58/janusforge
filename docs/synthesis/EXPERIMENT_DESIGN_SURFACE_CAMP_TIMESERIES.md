# EXPERIMENT_DESIGN — Surface abundance + Gi/cAMP time series (future wet-lab)

**Fecha:** 2026-10-19  
**Tipo:** **DESIGN ONLY** — no ejecutar wet-lab; no compute; no reopen de gates.  
**Capa:** EXTERNAL / assay design (futuro)  
**PI authorization:** YES (orden PI 2026-10-19, tras XL 12IY/12JA).  
**Autoridad de freeze:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md) · [`ACTA_EXTERNAL_CB2_APO_2026-09.md`](ACTA_EXTERNAL_CB2_APO_2026-09.md)

---

## Status flags (locked)

```text
WET_LAB_EXECUTION               = NOT AUTHORIZED (design only)
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)   # unchanged
P2_CONVERGENT_REOPEN            = FORBIDDEN
P5_MEMBRANE                     = HYPOTHESIS_READY; NOT advanced as done
TIER_B_MD                       = FORBIDDEN
KINETIC_PROJECT_GATES           = NOT REOPENED by this design
```

---

## Discrimination question (locked)

> En un eje temporal compartido, ¿los cambios de **abundancia superficial** de CB2 (tráfico/chaperoning) explican, confunden o son ortogonales a la trayectoria de **señal Gi/cAMP** — frente a la hipótesis de que un único endpoint medio de eficacia refleja solo control conformacional?

**Qué discriminaría (afirmativo):**

1. Superficie ↑ (o ↓) **sin** cambio proporcional de cAMP en la misma ventana → confusor de abundancia dominante (lectura Oyagawa).  
2. cAMP cambia de forma **transitoria vs sostenida** a dosis submáximas mientras la superficie es estable → cinética de señal (lectura Sharma) no reducible a tráfico.  
3. Ambos se mueven juntos → no se puede separar sin controles de ocupación/expresión; resultado `INDETERMINATE` honesto.

**Qué NO pretende:**

- Reabrir P2 Gate-1 / declarar CONVERGENT.  
- Avanzar P5 membrana como hecho.  
- Demostrar hubs Janusforge, sesgo intramolecular, o “mecanismo Gi resuelto”.  
- Sustituir BRET/TR-FRET de unión por un mapa de distancias DEER.

---

## Literature anchors

| Paper | DOI | Rol en el diseño |
|-------|-----|------------------|
| Oyagawa et al. *Cell. Mol. Life Sci.* 2025 | [10.1007/s00018-025-05961-w](https://doi.org/10.1007/s00018-025-05961-w) | Tráfico anterógrado / chaperoning: agonistas e inverse agonists pueden **aumentar entrega a superficie** en exposición sostenida; puede coexistir con internalización; **2-AG** distinto en sus condiciones. Confusor para ensayos de **horas**. Registrado: [`TRAFFICKING_CONFOUNDER_CB2_2025.md`](TRAFFICKING_CONFOUNDER_CB2_2025.md) |
| Sharma et al. *IJMS* 2023 | [10.3390/ijms24076406](https://doi.org/10.3390/ijms24076406) | BRET temporal cAMP y β-arrestina-2: a concentraciones submáximas, trayectorias **transitorias vs sostenidas** pueden diferir aunque el análisis medio **no** muestre sesgo significativo. No colapsar a un único endpoint. |

---

## Proposed readouts (design — not executed)

### A) Surface abundance (time series)

| Element | Spec |
|---------|------|
| Construct | CB2 WT (o epitope N-terminal accesible) en sistema heterólogo bien tipado; opcional variante KK C-term (Oyagawa) como control de entrega basal |
| Surface metric | Binding no permeable / Ab anti-epitope en células intactas / citometría superficie; **no** solo Western total |
| Time grid | Basal + puntos cortos (min) + puntos largos (1–6+ h) alineados al eje de señal |
| Ligands | ≥1 agonista de referencia (p. ej. CP55,940), ≥1 inverse agonist, **2-AG** (control negativo de tráfico anterógrado según Oyagawa), vehículo |
| Parallel | Fracción internalizada / total si el ensayo lo permite (coexistencia tráfico↑ + internalización) |

### B) Gi / cAMP signal (time series)

| Element | Spec |
|---------|------|
| Readout | Biosensor BRET/FRET de cAMP (espíritu Sharma) **o** cAMP acumulado con IBMX en ventanas definidas — declarar cuál |
| Optional orthogonal | β-arrestina-2 BRET (Sharma) — **no** requerido para la pregunta primaria superficie↔cAMP |
| Dosing | Curva + **concentración submáxima** fija para trayectorias temporales (donde Sharma vio diferencias) |
| Normalization | Reportar crudo **y** normalizado por superficie (o por expresión total) — ambos, no solo uno |

### C) Coupling rules

1. Mismo stock de células / misma placa cuando sea posible.  
2. Mismos tiempos nominales para superficie y cAMP.  
3. Pre-registrar ventanas “corta” vs “prolongada” antes de mirar datos.  
4. Si solo hay un tiempo largo sin superficie → ensayo **no** interpreta eficacia intrínseca.

---

## Confounders (explicit)

| Confounder | Mitigación de diseño |
|------------|----------------------|
| Chaperoning / abundancia (Oyagawa) | Medir superficie en el mismo eje; no atribuir Emax solo a “eficacia” |
| Internalización concurrente | Medir pool superficial vs total / internalizado |
| Lipofilia / acceso a membrana (Sharma) | Incluir ligando menos lipofílico vs CP55,940; no mezclar endpoints |
| Expresión transient vs estable | Fijar sistema; reportar nivel de expresión |
| Sistemas endógenos no validados | Diseño heterólogo primero; claim endógeno = futuro aparte |
| Over-interpretation a hubs/P2 | Hard stop: este diseño **no** toca MSM ni P5 |

---

## Falsification / decision table (pre-registered spirit)

| Observación | Interpretación permitida | Interpretación prohibida |
|-------------|--------------------------|---------------------------|
| Superficie↑, cAMP plano (misma dosis/tiempo) | Confusor de abundancia plausible | “Demuestra alostería intramolecular” |
| Superficie estable, cAMP transitorio vs sostenido por ligando | Cinética de señal distinta (Sharma-like) | “Prueba sesgo estructural CB2” |
| Ambos covarían perfectamente | No separación; `INDETERMINATE` | Forzar mecanismo único |
| Solo cAMP a 4 h sin superficie | Ensayo inválido para eficacia intrínseca | Rescue narrativo post-hoc |

---

## What this does **not** authorize

1. Ejecución wet-lab sin orden PI aparte.  
2. Reopen P2 como CONVERGENT o Gate-1.  
3. Advance P5 a “done”.  
4. Tier B MD / docking / de novo.  
5. Tratar GRAB-CB2 o sondas fluorescentes como parte de este diseño (siguen **DEFERRED** en PUBLIC_DATA_LEADS §8) salvo orden futura.

---

## Minimal deliverable if ever run

- Tabla tiempo × ligando × (superficie, cAMP [, arrestin]).  
- Figuras de trayectorias + normalización por superficie.  
- Veredicto de diseño: `SURFACE_CAMP_TRAFFIC_CONFOUND` / `SURFACE_STABLE_KINETIC_SIGNAL` / `INDETERMINATE` — **sin** mapear a A/B/C de P2.

---

*Fin. DESIGN ONLY — no wet-lab, no gate reopen.*
