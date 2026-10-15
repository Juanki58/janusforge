# JANUSFORGE — Documentación de investigación: arquitectura permanente v1.0

**Tipo:** propuesta de arquitectura documental (solo diseño)  
**Fecha:** 2026-08-17  
**Estado:** PROPOSAL — no ejecutada  
**Prohibiciones respetadas:** sin mover/borrar archivos; sin commit; sin docking/MD/NCE/investigación nueva.

---

## Gaps de base (preferidos vs sustitutos)

| Preferido | Estado | Sustituto usado |
|-----------|--------|-----------------|
| `results/reports/JANUSFORGE_RESEARCH_MASTER_STATE_v1.0.md` | **AUSENTE** | `results/reports/JANUSFORGE_RECOVERED_RESEARCH_STATE.md` |
| `results/reports/JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md` | **AUSENTE** | Conclusiones de supersesión en `JANUS_DECISION_LEDGER_v1.0.md` + CONFLICTOS §11 de Recovered State; Round1.9 / 0Q / SMRF / 0Q.1 |

**Implicación:** esta arquitectura asume que MASTER_STATE y SUPERSESSION_AUDIT se **crearán** en la migración (no existen aún). Hasta entonces, Recovered State + Decision Ledger son el puente operativo.

---

## 1. Problema — por qué falla la documentación actual

1. **Docs “ACTIVE” sin cierre.** Archivos con status propio (`next_iter_pyrazole_qiu_plan.md` = ACTIVE docking) no se actualizan cuando llega un veredicto posterior (0Q = D NO-GO compute). El árbol conserva claims contradictorios sin banner ni enlace de supersesión.
2. **Entrada fragmentada.** `docs/README.md` indexa norma L0 + Track1 histórico (THCV/D2_22/Qiu plan) pero **no** apunta a 0Q/SMRF/Round1.9. Un investigador nuevo lee “norte” desfasado.
3. **Round1 untracked.** Cadena ROUND1* / GOLD / Level0 / R1.9 vive en el WT sin estar en HEAD → desaparece en clone limpio / otro checkout / otro modelo.
4. **Checkout incompleto vs `origin/master`.** 0M handoff, 0P, dossier, CRO SEND existen en remoto y no en el WT actual → “memoria completa” no es reproducible desde un solo árbol.
5. **Conflictos sin árbitro.** Ledger lista CONFLICTOs A–C (next_iter vs 0Q; Round1.9 STOP vs SMRF ACTIVE; docs legacy D2_22) pero no hay un único documento canónico que diga *qué manda ahora* por capa (compute / literatura / calibración documental).
6. **Herramientas ≠ evidencia.** Gemini/Cursor aparecen como “resolved” en un hilo y como REJECTED en Round1.3–1.9; sin regla de autoridad, el siguiente chat reinstala el error.
7. **Sobrevivencia cero ante cambio de contexto.** Sin entry point único + lifecycle CURRENT/SUPERSEDED, cambio de conversación/modelo/investigador = re-descubrimiento ad hoc y reescritura silenciosa.

---

## 2. Entry point único (reconstruir estado científico)

### Canónico propuesto (permanente)

```
docs/research/README.md
```

**Rol:** única puerta de entrada. ≤1 página. Contiene solo:

- Enlace al **Source of Truth “qué está haciendo JANUS ahora”** (ver §10).
- Enlace a `docs/research/JANUSFORGE_RESEARCH_MASTER_STATE.md` (estado científico reconstruible).
- Enlace a `docs/decisions/JANUS_DECISION_LEDGER.md` (decisiones + CONFLICTOs abiertos).
- Enlace a `docs/decisions/JANUSFORGE_SUPERSESSION_AUDIT.md` (mapa CURRENT ↔ SUPERSEDED).
- Orden de lectura de handoff (§7).
- Regla: *Gemini/ChatGPT/Cursor ≠ evidencia primaria*.

### Documento de estado (cuerpo)

```
docs/research/JANUSFORGE_RESEARCH_MASTER_STATE.md
```

Versión con semver en frontmatter (`v1.x`). Los snapshots históricos van a `docs/superseded/` o se versionan por rename (`…_v1.0.md` archived), **nunca** se editan en silencio.

**Puente actual (hasta migración):**  
`results/reports/JANUSFORGE_RECOVERED_RESEARCH_STATE.md` + `results/reports/JANUS_DECISION_LEDGER_v1.0.md`.

---

## 3. Estructura mínima (propósito)

```
docs/
  research/          # Estado vivo + entry point
  decisions/         # Ledger + supersesión + CONFLICTOs
  literature/        # Memoria literaria / novelty (estable)
  handoff/           # (opcional) protocolo + checklist nuevo investigador
  superseded/        # (opcional) copias archivadas con banner; no borrar originales hasta fase 3

results/reports/     # Informes de campaña (gates, audits, MD, Round1, 0Q.*)
```

| Path | PURPOSE |
|------|---------|
| **`docs/research/`** | North star operativo: README entry + MASTER_STATE + “NOW” card. Responde: hipótesis viva, paths cerrados, workstream ACTIVE, gaps. |
| **`docs/decisions/`** | Decision cards inmutables + ledger + SUPERSESSION_AUDIT. Responde: qué se decidió, cuándo, con qué evidencia, si está superseded. |
| **`docs/literature/`** | Brújula literaria estable (fibrosis, novelty, mapa ligandos, mecanismos). No es el “qué hacemos ahora”; se actualiza solo con claim-split / prior art. |
| **`results/reports/`** | Artefactos de campaña fechados: gates MD/docking, 0D–0Q, Round1.x, soft-drug audits, matrices. **Append-only por defecto.** |
| **`docs/handoff/`** *(opcional, esencial)* | `NEW_RESEARCHER.md` — orden de lectura + checklist de gaps (tracked vs untracked; WT vs origin/master). |
| **`docs/superseded/`** *(opcional)* | Destino de *copias* archivadas o índice de paths SUPERSEDED. Preferible **banner in-place** + índice en SUPERSESSION_AUDIT; carpeta solo si hace falta snapshot físico. |

**Fuera de esta arquitectura (no mover en propuesta):** `data/papers/` (corpus bruto), `scripts/`, `results/md/` (artefactos numéricos), `docs/guia_maestra_*` (Norma L0 — permanece en `docs/` raíz o se enlaza desde literature/research).

---

## 4. Tipos de documento y naming

| Tipo | Prefijo / patrón | Dónde | Ejemplo |
|------|------------------|-------|---------|
| Entry / índice | `README.md` | `docs/research/` | — |
| Estado maestro | `JANUSFORGE_RESEARCH_MASTER_STATE.md` (+ `_vX.Y` al archivar) | `docs/research/` | — |
| “Qué hacemos ahora” | `JANUSFORGE_NOW.md` | `docs/research/` | §10 |
| Decision ledger | `JANUS_DECISION_LEDGER_vX.Y.md` | `docs/decisions/` | — |
| Supersesión | `JANUSFORGE_SUPERSESSION_AUDIT_vX.Y.md` | `docs/decisions/` | — |
| Norma L0 | sin prefijo campaña | `docs/` (existente) | `guia_maestra_*` |
| Literatura estable | descriptivo snake | `docs/literature/` (migración desde `docs/*`) | `literatura_fibrosis_*` |
| Gate / batch | `{serie}_*_gate_summary.md` | `results/reports/` | `h1_h5_batch3_gate_summary.md` |
| MD / docking report | `md_*` / `qiu_0{letra}_*` | `results/reports/` | `md_d2_22_20ns_summary.md` |
| Auditoría científica | `*_audit*.md` / `AUDIT_*_vX.Y.md` | `results/reports/` | `qiu_0q_independent_scientific_audit.md` |
| Calibración documental | `ROUND1*` / `ROUND1.N_*` | `results/reports/` | `ROUND1.9_MASTER_EVIDENCE_STATE.md` |
| Matriz / dataset | `*_matrix.md` / `*_Dataset_*` | `results/reports/` | `qiu_0q_smrf_matrix.md` |
| Handoff wet/CRO | `*_handoff.md` / `cro_package_*` | `results/reports/` (o subcarpeta existente) | `qiu_0m_h1a_wet_handoff.md` |

**Reglas de nombre:**

- Versión semver en docs de estado/ledger/audit (`_v1.0`).
- Fecha ISO en frontmatter, no solo en el cuerpo.
- Un informe = un veredicto; no reutilizar el mismo path para “corregir” historia.
- IDs de decisión estables (`D2_22-NOGO`, `0Q-D-NOGO`, `0Q-SMRF`, …) como en el Ledger.

---

## 5. Lifecycle: CURRENT vs SUPERSEDED vs HISTORICAL

| Estado | Significado | Acción documental |
|--------|-------------|-------------------|
| **CURRENT** | Autoridad vigente para su *capa* | Listado en MASTER_STATE + SUPERSESSION_AUDIT; enlazado desde NOW |
| **SUPERSEDED** | Reemplazado por un doc/commit posterior explícito | Banner al tope + enlace “Superseded by: path”; entrada en SUPERSESSION_AUDIT; **texto histórico intacto** |
| **HISTORICAL** | Cerrado / no autoridad, pero no “mentira” | Sin banner de superseded si nunca fue contradicho; aparece en Recovered/ledger como cerrado (ej. H1 NO-GO) |
| **CONFLICT** | Dos CURRENT aparentes sin resolución | Solo en ledger §CONFLICTOs; **prohibido** “elegir ganador” en silencio |

**Vínculo a SUPERSESSION_AUDIT (a crear):**  
`docs/decisions/JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md` — tabla path → status → superseded_by → commit/fecha → capa (compute | lead | literature-expand | documentary-calibration | wet).

**Ejemplos ya detectados (para poblar el audit, no resolver aquí):**

| Path | Status propuesto | Notas |
|------|------------------|-------|
| `md_d2_22_20ns_summary.md` | CURRENT (NO-GO lead) | Definitivo |
| `next_iter_pyrazole_qiu_plan.md` | SUPERSEDED *o* CONFLICT | Sin patch post-0Q → hoy CONFLICT |
| `qiu_0q_independent_scientific_audit.md` | CURRENT (compute D NO-GO) | Reafirmado SMRF/0Q.1 |
| `qiu_0q_smrf_matrix.md` | CURRENT (workstream B) | ACTIVE / MODERATE |
| `qiu_0q1_final_cursor_vs_gemini.md` | CURRENT (EXPAND) | — |
| `ROUND1.9_MASTER_EVIDENCE_STATE.md` | CURRENT (calibración) | PIPELINE STOP; capa distinta a SMRF |
| `docs/criterio_exito_janus.md` (lenguaje D2_22) | SUPERSEDED parcial / CONFLICT | vs MD NO-GO |

**Nota:** banners SUPERSEDED **aún no aplicados** (§8). Esta propuesta no los aplica.

---

## 6. Reglas — qué va dónde

| Material | Destino | No va en |
|----------|---------|----------|
| **Round1 / Round1.x / GOLD / Level0 / quarantine** | `results/reports/` (trackear en git); índice + veredicto GOLD=0 en MASTER_STATE | `docs/research/` (solo resumen + enlace) |
| **0Q / SMRF / 0Q.1 / 0Q.2F** | `results/reports/`; status lock → MASTER_STATE + NOW | Sobrescribir `next_iter_*` sin audit |
| **MD / docking / gate summaries** | `results/reports/`; decisión → card en ledger | Editar el summary antiguo para “arreglar” el veredicto |
| **Soft-drug / controlled-deactivation audits** | `results/reports/`; conclusión fenotipo → MASTER_STATE §descartes | Mezclar con calibración Round1 Gold |
| **Decision cards / CONFLICTOs** | `docs/decisions/` | Chat / transcript como única copia |
| **Literatura fibrosis / novelty / mapa ligandos** | `docs/literature/` (tras migración) | `results/reports/` salvo extractos de campaña |
| **Primarios PDF/SI/OCR** | `data/papers/` | Sustituir un report Round1 por “yo vi el PDF en el chat” |
| **Handoff wet/CRO** | `results/reports/` (+ estado RESERVE/BLOCKED en NOW) | Activar wet sin actualizar NOW/ledger |

**Capas (no colapsar):**

1. **Compute / NCE** — 0Q D NO-GO.  
2. **Lead molecular** — D2_22 NO-GO; H1 NO-GO.  
3. **Literature EXPAND / SMRF** — ACTIVE / MODERATE.  
4. **Documentary calibration (Round1)** — PIPELINE STOP / GOLD=0.  
5. **Wet 0M** — RESERVE.

Un doc puede ser CURRENT en su capa y no autorizar otra capa.

---

## 7. Handoff protocol — orden de lectura (nuevo investigador)

Tiempo objetivo: **30–45 min** antes de tocar ciencia.

1. `docs/research/README.md` *(entry; tras migración)*  
2. `docs/research/JANUSFORGE_NOW.md` — **qué manda ahora**  
3. `docs/research/JANUSFORGE_RESEARCH_MASTER_STATE.md`  
4. `docs/decisions/JANUS_DECISION_LEDGER.md` — especialmente CONFLICTOs abiertos  
5. `docs/decisions/JANUSFORGE_SUPERSESSION_AUDIT.md`  
6. Primarios de workstream vivo:  
   - `results/reports/qiu_0q_independent_scientific_audit.md`  
   - `results/reports/qiu_0q_smrf_matrix.md`  
   - `results/reports/qiu_0q1_final_cursor_vs_gemini.md`  
7. Calibración: `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md`  
8. Descartes clave: `md_d2_22_20ns_summary.md`, `md_membrane_20ns_summary.md`, `AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md`  
9. Norma L0: `docs/guia_maestra_biotecnologia_quimiotipos.md` (contexto; no override de NOW)  
10. Checklist handoff: `docs/handoff/NEW_RESEARCHER.md` — ¿Round1 tracked? ¿0M/0P en este checkout? ¿rama vs `origin/master`?

**Puente pre-migración (orden actual):**  
Recovered State → Decision Ledger → 0Q → SMRF → 0Q.1 → Round1.9 → audits soft-drug.

**Regla de chat:** el nuevo agente lee disco primero; transcript solo para gaps marcados en handoff.

---

## 8. Qué NO hacer

1. **No editar en silencio la historia.** Corrección = nuevo doc o nueva versión + entrada en SUPERSESSION_AUDIT.  
2. **No borrar** informes superseded; banner + enlace.  
3. **No aplicar banners todavía** hasta existir SUPERSESSION_AUDIT poblado (fase 2). Esta propuesta **no** los aplica.  
4. **No promover** claims Gemini/ChatGPT/Cursor a CONFIRMED/Gold sin primario recuperado.  
5. **No colapsar capas** (STOP Round1 ≠ STOP SMRF EXPAND; NO-GO compute ≠ borrar literatura).  
6. **No dejar untracked** material que defina estado (Round1*, NOW, MASTER_STATE, ledger).  
7. **No usar `docs/README.md` legacy como SoT** sin reescribirlo hacia `docs/research/README.md`.  
8. **No reabrir docking/MD/NCE** desde un plan ACTIVE obsoleto sin pasar por ledger + NOW.  
9. **No “votar” CONFLICTOs** en un chat; registrar o resolver con decisión fechada en ledger.

---

## 9. Plan de migración (propuesta — no ejecutar)

### Fase 0 — Congelar inventario (1 sesión)
- Confirmar gaps: MASTER_STATE / SUPERSESSION_AUDIT ausentes.  
- Listar untracked crítico (Round1*, AUDIT_*, DOCUMENTARY_*, 0Q.2F).  
- Diff WT ↔ `origin/master` (0M, 0P, dossier).

### Fase 1 — Crear esqueleto vacío
- Crear dirs: `docs/research/`, `docs/decisions/`, `docs/literature/`, `docs/handoff/` (± `docs/superseded/`).  
- Escribir `docs/research/README.md` + stub `JANUSFORGE_NOW.md` + stub MASTER_STATE (contenido inicial = resumen de Recovered State).  
- Copiar/promover Decision Ledger → `docs/decisions/` (o stub que enlace al de `results/reports/` hasta move lógico).  
- **Sin moves masivos aún.**

### Fase 2 — SUPERSESSION_AUDIT v1.0
- Poblar tabla desde Ledger CONFLICTOs + Recovered §11.  
- Marcar CURRENT por capa; dejar CONFLICT explícito donde no hay patch.  
- **Aún sin banners** en archivos viejos (o banners solo en 3–5 paths piloto).

### Fase 3 — Routing, no reescritura
- Trackear Round1* + audits en git.  
- Actualizar `docs/README.md` → redirect de una línea a `docs/research/README.md`.  
- Enlazar literatura existente desde `docs/literature/README.md` (links; move físico opcional y posterior).  
- Añadir banner SUPERSEDED solo tras fila en audit.

### Fase 4 — Handoff operable
- `docs/handoff/NEW_RESEARCHER.md` con orden §7 + checklist checkout.  
- Una pasada de prueba: nuevo chat / modelo lee solo entry point y reconstruye NOW sin transcript.

### Fase 5 — Higiene continua
- Todo informe nuevo nace en `results/reports/` con frontmatter status.  
- Todo cambio de workstream toca **NOW + ledger + audit** en el mismo cambio lógico.  
- Archivar versiones MASTER_STATE al bumpear minor.

**Fuera de alcance de migración:** borrar `data/papers/`, re-ejecutar cómputo, “arreglar” Gold, resolver CONFLICTOs científicos.

---

## 10. Single source of truth — “qué está haciendo JANUS ahora”

**Path canónico propuesto:**

```
docs/research/JANUSFORGE_NOW.md
```

**Contrato del archivo (máx. ~40 líneas):**

| Campo | Contenido |
|-------|-----------|
| Fecha / commit HEAD de referencia | ISO + hash |
| Hipótesis de programa | Janus CB1-ant + CB2-ago (fibrosis = filtro 2º) |
| Compute / NCE / docking / MD | **NO-GO** (cita 0Q) |
| Lead molecular vigente | **Ninguno** (H1 NO-GO; D2_22 NO-GO) |
| Workstream ACTIVE | **0Q-SMRF** MODERATE + **0Q.1 EXPAND** (literatura / claim-split only) |
| Wet 0M | **RESERVE** |
| Calibración Round1 | **PIPELINE STOP**; GOLD_CONFIRMED = 0 |
| CONFLICTOs abiertos | Lista corta → enlace ledger |
| Prohibido ahora | docking, MD, NCE, promoción Gold sin primario |
| Siguiente paso permitido | Anclar primarios bloqueantes y/o EXPAND literario (según Recovered §12) |

**Autoridad:** si un report de campaña contradice NOW sin entrada de supersesión, **NOW gana para “qué hacer”** solo después de que el ledger registre la decisión; hasta entonces = CONFLICT, no improvisar.

**Puente pre-migración (SoT temporal explícito):**

```
results/reports/JANUS_DECISION_LEDGER_v1.0.md
  § “What is the CURRENT scientific decision of JANUS?”
```

más el resumen de workstream en:

```
results/reports/JANUSFORGE_RECOVERED_RESEARCH_STATE.md
  §12 (único siguiente paso documentado)
```

Cuando existan `docs/research/JANUSFORGE_NOW.md` + MASTER_STATE, el Ledger deja de ser SoT de “ahora” y pasa a ser **registro de decisiones**; NOW absorbe el rol operativo.

---

## Resumen ejecutivo (parent)

| Ítem | Valor |
|------|-------|
| **Este archivo** | `results/reports/JANUSFORGE_DOCUMENTATION_ARCHITECTURE_v1.0.md` |
| **Entry point propuesto** | `docs/research/README.md` |
| **SoT “qué hace JANUS ahora”** | `docs/research/JANUSFORGE_NOW.md` (puente: Decision Ledger §CURRENT) |
| **Estado reconstruible** | `docs/research/JANUSFORGE_RESEARCH_MASTER_STATE.md` |
| **Dirs** | `research/` estado+entry · `decisions/` ledger+supersesión · `literature/` memoria estable · `results/reports/` campañas · opcional `handoff/` + `superseded/` |
| **Gaps** | MASTER_STATE y SUPERSESSION_AUDIT preferidos **ausentes**; arquitectura los crea en migración |

*Fin propuesta v1.0 — no ejecutada.*
