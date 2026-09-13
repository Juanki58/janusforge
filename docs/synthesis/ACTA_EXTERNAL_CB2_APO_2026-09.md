# ACTA — Congelación de síntesis EXTERNAL CB2_APO (2026-09)

**Fecha:** 2026-09-13  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Tipo:** **DOCUMENTATION ONLY** — acta de cierre del capítulo EXTERNAL CB2_APO; **no** compute nuevo.  
**Autoridad de flags:** [`RESEARCH_STATE.md`](../../RESEARCH_STATE.md)  
**Linaje DEEP_PAUSE (P2):** commit **`67df445`** (acta P2 / congelación profunda) · Gate 1 MSM GPCRmd **`2dcff23`**  
**Anclas EXTERNAL de este capítulo:** landmarks **`862dc42`** · own MSM N=200 **`22d2af1`** · higiene notebook **`3edaeae`**

---

## 1. Alcance

### 1.1 Capítulo EXTERNAL CB2_APO (cerrado aquí)

Reanálisis **EXTERNAL** sobre depósito Dutta & Shukla 2023 (DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)), usando:

- Pickles `Final_MSM` (cinética CB1 vs CB2; sin coordenadas).
- PDBs Main_Figure_6 (refs geométricos).
- Zip local `CB2_APO.zip` (extracción estratificada; **sin** unpack de ~142 GB).

Experimentos del capítulo (pre-registros en `docs/synthesis/`):

| Línea | Pre-reg / evidencia |
|-------|---------------------|
| Cinética Final_MSM | `EXPERIMENT_EXTERNAL_DUTTA_MSM.md` · `results/network_core/external_dutta_msm_compare.md` |
| Contactos PDB snapshot | `EXPERIMENT_CB2_STATE_PDB_CONTACTS.md` · `cb2_state_pdb_contacts.md` |
| Pilot filename inactive/active | `EXPERIMENT_CB2_APO_PILOT_CONTACTS.md` |
| MSM-state contacts (Gate 0 filelist) | `EXPERIMENT_CB2_MSM_STATE_CONTACTS.md` · `DATA_REQUEST_DUTTA_SHUKLA_MSM.md` |
| ESMDynamic + fallback TM6/toggle | `EXPERIMENT_CB2_ESMDYNAMIC.md` · `cb2_esmdynamic.md` · `cb2_apo_tm6_toggle.md` |
| Own MSM estratificado | `EXPERIMENT_CB2_APO_OWN_MSM.md` · `cb2_apo_own_msm_report.md` |
| Landmark geométrico | `EXPERIMENT_CB2_LANDMARK_CONTACTS.md` · `cb2_landmark_contacts.md` |

### 1.2 Compuertas previas (permanecen locked)

| Gate | Status | Ancla |
|------|--------|-------|
| **P1** hubs dinámicos GPCRmd | `CLOSED (NOT_SUPPORTED)` | `31a881c` |
| **LigACN estático** | `CORE_TOPOLOGICAL_ONLY` | `cfb2a51` |
| **P2** MSM GPCRmd | `CLOSED (INSUFFICIENT_SAMPLING)` | `2dcff23` / acta `67df445` |
| **P2 A/B/C** | `ABORTED` · arquitectura **NOT DECIDED** | Gate 1 |
| **P3 / P4 / P6** | `BLOCKED` | freeze YAML |
| **P5** | `HYPOTHESIS_READY` · ejecución **BLOCKED_PENDING_DECISION** | independiente; no sustituto de P2 |
| Satélites **X8 / X1** | cerrados; no reabren P2 | 2026-09-09 |

Este acta **no** sustituye el acta P2 de `67df445`; lo **extiende** con el cierre del capítulo EXTERNAL CB2_APO.

---

## 2. Tabla de veredictos (locked)

| Ítem | Veredicto | Nota breve |
|------|-----------|------------|
| Landmark contacts (geométrico) | **`EXT_LANDMARK_CONTACTS_STABLE`** | mean Jaccard≈0.82; path turnover≈0.14; frac_core≈0.65 · tip `862dc42` |
| Geometría ≠ MSM | **`EXT_LANDMARK_GEOMETRIC_NEQ_MSM = TRUE`** | hard lock |
| Soft vs PDB snapshot B | **`EXT_LANDMARK_SOFT_DISAGREE_PDB_B`** | anotación; no promoción de ensemble |
| Own MSM (X8-like, N=200) | **`EXT_OWN_MSM_NON_CONVERGENT`** | ITS Δ late-vs-mid≈0.80; soft CK pass **no** anula ITS · `22d2af1` |
| Own MSM contacts / soft A/B/C | **ABORTED** | sin redes inventadas |
| PDB snapshot contacts | **`EXT_PDB_CONTACTS_STATE_DEPENDENT`** | 6 PDBs; clase snapshot B |
| Pilot APO filename | **`EXT_APO_PILOT_CONTACTS_INDETERMINATE`** | soft disagree vs PDB-B |
| MSM-state contacts (Dutta labels) | **`EXT_MSM_STATE_CONTACTS_INDETERMINATE_NO_ALIGNMENT`** | **blocker filelist** traj↔pickle |
| ESMDynamic | **`EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE`** | stack / VRAM / shard; no descarga forzada |
| TM6/toggle fallback | **`EXT_APO_TM6_TOGGLE_INDETERMINATE`** | filename ≠ macroestado MSM |
| Cinética Final_MSM CB1 vs CB2 | **`EXT_KINETICS_CB1_CB2_DISTINCT`** | sin coords → A/B/C estructural `INDETERMINATE_NO_TRAJECTORIES` |

---

## 3. Qué afirmamos / qué no afirmamos

### Afirmamos (notebook-honest)

1. Bajo etiquetado **geométrico** a 6 refs PDB, los mapas de contacto VdW+0.5 son **similares entre landmarks** (`STABLE`).
2. Ese resultado **no** es un MSM cinético; proximidad RMSD **≠** identidad metastable.
3. Nuestro MSM propio sobre zip estratificado (hasta N=200) **no** converge en ITS bajo criterios pre-registrados; contactos abortados correctamente.
4. Contactos por macroestado Dutta siguen **bloqueados** sin filelist ordenado (no fabricamos alineación lex/zip).
5. ESMDynamic **no** estuvo disponible en el entorno; no se inventó proxy MSM.
6. P1 / P2 / LigACN / A/B/C **siguen** en el estado del freeze `67df445` + excepciones ya registradas.
7. La credibilidad del proyecto en este punto es **síntesis locked + gates que dispararon**, no más runs `NON_CONVERGENT` ni narrativa AI especulativa.

### No afirmamos

1. Mecanismo CB2→Gi resuelto; switch único; red plenamente distribuida demostrada.
2. Arquitectura A/B/C (RED_ESTABLE / RUTAS_POR_ESTADO / DISTRIBUIDA) **decidida**.
3. P2 GPCRmd reabierto o `CONVERGENT`.
4. Identidad `OWN_Sk` ≡ Dutta I1–I4 / Inactive–Active.
5. Que el soft-disagree geométrico vs snapshot PDB-B “refute” o “confirme” el paper.
6. Cinética ensemble propia (tiempos de transición, π MSM) a partir de landmarks o filename classes.
7. Validación experimental de ESMDynamic sobre CB2 en este lab.

---

## 4. Lectura epistémica

**Geometría (suave A):** los contactos por landmark se comportan como una red de contactos **estable / similar** a lo largo del camino inactive→…→active en espacio RMSD. Eso es compatible con una lectura tipo **RED_ESTABLE a nivel de mapa de contactos geométricos** — **solo** en ese sentido soft, y **solo** bajo asignación por proximidad.

**Snapshot B (soft-disagree):** los 6 PDBs estáticos del paper dieron clase **STATE_DEPENDENT**. Trajectories etiquetadas geométricamente (y pilots filename) **no** reproducen esa clase. Lectura obligatoria: **desacuerdo de clase de mapa**, no veredicto de falsación del depósito ni promoción de un modelo A/B/C de ensemble.

**Cinética: undecided.** Own MSM `NON_CONVERGENT`; P2 GPCRmd `INSUFFICIENT_SAMPLING`; contactos por estado Dutta sin filelist. **No sabemos** si el control es estable / rutas-por-estado / distribuido a nivel de paisaje Markoviano.

**Regla vigente:** `DECISION_RULE = DISCRIMINATION_ONLY` (ancla `bb7b57a`). Interés ≠ umbral de reopen.

---

## 5. Locks explícitos (reafirmados)

```text
DEEP_PAUSE                         = TRUE          # permanece
REPOSITORY                         = SEALED
COMPUTATION                        = PAUSED        # salvo decisión humana explícita
P2_MSM_TRANSITIONS                 = CLOSED (INSUFFICIENT_SAMPLING)  # no reopen
P2_NETWORK_A_B_C                   = ABORTED
ARCHITECTURE_A_B_C                 = NOT DECIDED
Gi / docking / de novo / hub hunt  = STOP
POST_HOC_EXCUSES                   = FORBIDDEN
FILELIST_FABRICATION               = FORBIDDEN
ESMDYNAMIC_FORCED_DOWNLOAD         = NOT AUTHORIZED (este acta)
OWN_MSM_FURTHER_SCALE              = HUMAN DECISION ONLY
DISCRIMINATION_ONLY                = TRUE
```

---

## 6. Próximas decisiones humanas (solo)

No “correr script X mañana.” Tres opciones estratégicas, mutuamente excluyentes en prioridad inmediata:

1. **Muestreo masivo / adaptativo** (línea P2 GPCRmd u own MSM con N cualitativamente mayor y criterios de Gate 1 pre-registrados de nuevo) — inversión de recurso, no piloto incremental.
2. **P5 membrana** (hipótesis independiente; **no** rescate de P1/P2) — requiere autorización de ejecución aparte.
3. **Esperar filelist** traj↔MSM de autores (borrador en `DATA_REQUEST_DUTTA_SHUKLA_MSM.md`) — email **manual**; sin automatización; sin re-descarga de 142 GB.

Cualquier compute nuevo exige orden PI explícita que nombre **qué hipótesis discrimina**.

---

## 7. YAML de cierre (capítulo EXTERNAL)

```yaml
CHAPTER: EXTERNAL_CB2_APO
STATUS: SYNTHESIS_FROZEN
DATE: 2026-09-13
DEEP_PAUSE: TRUE
P2_REOPEN: FALSE
EXT_LANDMARK_CONTACTS: EXT_LANDMARK_CONTACTS_STABLE
EXT_LANDMARK_GEOMETRIC_NEQ_MSM: TRUE
EXT_LANDMARK_SOFT_DISAGREE_PDB_B: TRUE
EXT_OWN_MSM: EXT_OWN_MSM_NON_CONVERGENT
EXT_OWN_MSM_CONTACTS: ABORTED
EXT_MSM_STATE_CONTACTS: INDETERMINATE_NO_ALIGNMENT
EXT_ESMDYNAMIC: INDETERMINATE_UNAVAILABLE
EXT_KINETICS_FINAL_MSM: EXT_KINETICS_CB1_CB2_DISTINCT
STRUCTURAL_ABC_ENSEMBLE: NOT_DECIDED
KINETICS_OWN: UNDECIDED
NEXT: HUMAN_STRATEGIC_CHOICE  # massive sampling OR P5 OR wait filelist
```

---

*Fin acta EXTERNAL CB2_APO. Congela síntesis; no autoriza compute; no reabre P2; no envía email; no escala MSM; no descarga ESMDynamic.*
