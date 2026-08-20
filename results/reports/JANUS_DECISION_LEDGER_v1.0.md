# JANUS DECISION LEDGER

**Tipo:** inventario de decisiones científicas (fuente + commit + estado)  
**Versión:** v1.0  
**Fecha de recuperación:** 2026-08-17  
**Índice usado (solo mapa):** `results/reports/JANUSFORGE_RECOVERED_RESEARCH_STATE.md`  
**Método:** abrir fuentes citadas + `git show` / `git log`; sin nueva investigación; sin inferir resolución de conflictos.  
**HEAD al inventariar:** `c43c0b7` (`cursor/pr5-0q-audit-smrf-0q1-clean`) — *Add 0Q SMRF and 0Q.1 scientific audit* (2026-08-16)

**Prohibiciones respetadas:** sin docking/MD/NCE; sin commit; sin hipótesis nuevas; sin elegir ganador entre CONFLICTOs.

---

## Decision cards (one per priority item)

### 1. 485bb00 — NO-GO científico D2_22

| Campo | Valor |
|-------|--------|
| **ID** | D2_22-NOGO |
| **Path (informe exacto)** | `results/reports/md_d2_22_20ns_summary.md` |
| **Paths satélite tocados en el mismo commit** | `docs/lecciones_aprendidas_track1.md`; `results/reports/option_d_batch_d1_gate_summary.md`; `results/reports/option_d_pivot_urb447.md`; `docs/README.md`; **A** `results/reports/next_iter_pyrazole_qiu_plan.md` |
| **Commit** | `485bb0012209fe922dd7c0bf5d92455c2dbc4497` |
| **Mensaje commit** | Document D2_22 biophysical NO-GO and pause toward Qiu pyrazole iteration. |
| **Fecha commit** | 2026-08-11 08:05:39 +0200 |
| **Fecha en informe** | 2026-08-11 (Status / Análisis de la falla) |
| **Decisión** | **NO-GO de trinquete CB1** — D2_22 **descartado como lead funcional** (ex-lead docking únicamente). GPU/MD pesada **pausada**. El “go exploratorio débil” previo queda **superseded** por este veredicto. |
| **Evidencia utilizada** | MD POPC 20 ns CB1 5TGZ (`results/md/membrane/JANUS_D2_22/metrics_summary.json`, `frame_metrics.csv`, `d2_22_5tgz_popc.csv`); comparación vs panel en `md_membrane_20ns_summary.md` (COM TM3–TM6 12.35 ≈ THC 12.06, no THCV 13.07; ángulo ~THC; Vina −11.277 no predice restricción); docking lead context `option_d_batch_d1_gate_summary.md` |
| **Estado actual** | **NO-GO** (lead D2_22). MD pesada = **STOP/PAUSE** operativa documentada en el mismo informe. |
| **¿Superseded?** | **NOT SUPERSEDED** como NO-GO del lead. (Sí supersede el “go exploratorio débil” anterior.) Nota: `docs/criterio_exito_janus.md` / `docs/mapa_ligandos_janus_cb1_cb2.md` aún pueden presentar lenguaje pre-NO-GO → **CONFLICTO DETECTADO** documental (no anula el informe MD). |

---

### 2. 0Q — D NO-GO docking-NCE

| Campo | Valor |
|-------|--------|
| **ID** | 0Q-D-NOGO |
| **Path (informe exacto)** | `results/reports/qiu_0q_independent_scientific_audit.md` |
| **Commit (en HEAD / rama limpia)** | `c43c0b77c0cfb0070e8da40982cf0020d40b4539` (2026-08-16) — *Add 0Q SMRF and 0Q.1 scientific audit* |
| **Primera aparición en historial** | `d0e483f` 2026-08-13 20:23:03 +0200 — *Add independent destroy-hypothesis CB1/CB2 scientific audit (0Q).* (rama `pr5` dirty); también `f520ad5` 2026-08-15 |
| **Fecha en informe** | 2026-08-13 |
| **Decisión** | Clasificación **D — NO-GO** sobre la hipótesis Janusforge-como-motor **docking / MD / diseño NCE** anclado en Qiu-14. Espacio fibrosis **no E**. |
| **Evidencia utilizada (claves del informe)** | URB447 LoVerme 2009 (PMC3690177); Qiu 2023 + SI Fig. S5 (cualitativo; potencias OA NOT FOUND); WO2022026478 / US20230234928; Mallat 2007; RCSB CB2 entries; lenabasum Ph2b fail; locales SI `data/papers/mmc1_document.txt`, `image15_ocr.txt`, textos de patentes locales — ver §1–§13 / §14 |
| **Estado actual** | **NO-GO** del **path compute-NCE/docking**. |
| **¿Superseded?** | **NOT SUPERSEDED** para el path compute. Docs posteriores lo **reafirman**: `qiu_0q_smrf_matrix.md` (“SMRF no reabre docking/NCE”); `qiu_0q1_final_cursor_vs_gemini.md` (ban explícito NCE/docking/MD). |

---

### 3. 0Q.1 — EXPAND / mono-CB2 YES / Yin-Yang law NO

| Campo | Valor |
|-------|--------|
| **ID** | 0Q.1-EXPAND |
| **Path (informe exacto / FINAL)** | `results/reports/qiu_0q1_final_cursor_vs_gemini.md` |
| **Path audit Cursor (input)** | `results/reports/qiu_0q1_primary_audit_A_pairs.md` |
| **Commit** | `c43c0b7` (2026-08-16); primera cadena: `d81e5f4` (0Q.1 primary), `8ed0bea` (0Q.1-FINAL), `f520ad5` / `c43c0b7` |
| **Fecha en informe FINAL** | 2026-08-15 |
| **Decisión** | Recomendación **EXPAND** (literatura / claim-split only). Pares A: **YES** switch **mono-CB2**; **NO** ley estructural Yin-Yang dual CB1/CB2. Global SMRF permanece **MODERATE**. |
| **Evidencia utilizada** | Li/Hua *Cell* 2019 PMC6713262 (MRI2594/MRI2687 Fig. 6); Kosar *ACS Cent. Sci.* 2024 PMC11117691 (ago-3 / (R)-1 Tables 3–4); matriz padre `qiu_0q_smrf_matrix.md`; input Gemini pegado (Temp) = confirmación, no autoridad primaria |
| **Estado actual** | **EXPAND** |
| **¿Superseded?** | **NOT SUPERSEDED** (sin doc/commit posterior que revoque EXPAND en el corpus tracked de HEAD). |

---

### 4. 0Q-SMRF — MODERATE / ACTIVE

| Campo | Valor |
|-------|--------|
| **ID** | 0Q-SMRF |
| **Path (informe exacto)** | `results/reports/qiu_0q_smrf_matrix.md` |
| **Artefacto machine-readable** | `results/reports/qiu_0q_smrf_pairs.csv` |
| **Commit** | `c43c0b7` (2026-08-16); primera aparición historial: `b3402e3` (Add 0Q-SMRF…) |
| **Fecha en informe** | 2026-08-13 |
| **Decisión** | Veredicto `0Q-SMRF = **MODERATE**`. Workstream Option **B = ACTIVE**; Option **A (0M) = RESERVE**. No reabre docking/NCE. |
| **Evidencia utilizada** | Matriz histórica pares A/B/C/D; Class A: MRI2687↔MRI2594; HU-308/ago-3→(R)-1; Class B Janus: URB447, GW405833, AM1710, Qiu-14 (cualitativo); rechazo de potencias Qiu hypotéticas como hecho |
| **Estado actual** | **ACTIVE** / **MODERATE** |
| **¿Superseded?** | **NOT SUPERSEDED** — 0Q.1-FINAL (2026-08-15) declara MODERATE **unchanged**. Tensión documental con Round1.9 PIPELINE STOP → ver CONFLICTOs (no revoca el status lock SMRF en su propio texto). |

---

### 5. next_iter_pyrazole_qiu_plan.md

| Campo | Valor |
|-------|--------|
| **ID** | NEXT-ITER-QIU |
| **Path** | `results/reports/next_iter_pyrazole_qiu_plan.md` |
| **¿Existe en WT?** | **Sí** (presente) |
| **Commit creación** | `485bb00` 2026-08-11 08:05:39 +0200 (**A**dd) |
| **Último commit que lo toca** | `57551db` 2026-08-11 08:20:14 +0200 — *Start Qiu pyrazole iteration with light dual docking (MD paused).* |
| **Fecha en documento** | 2026-08-11 |
| **Decisión documentada en el archivo** | Eje pirazol Qiu **ACTIVO (docking only)**; MD/OpenMM **pausada**; trigger = descarte D2_22 |
| **Evidencia citada por el plan** | `md_d2_22_20ns_summary.md`; `qiu_pyrazole_batch1_gate_summary.md`; `option_d_pivot_urb447.md`; `docs/lecciones_aprendidas_track1.md`; DOI Qiu 2023 |
| **Estado según el propio archivo** | **ACTIVE** (docking light) |
| **¿Superseded?** | **CONFLICTO DETECTADO** — el archivo **nunca fue editado** tras 0Q (`git log` solo 485bb00 → 57551db, ambos 2026-08-11). 0Q (doc 2026-08-13; commits `d0e483f`/`c43c0b7`) declara **D NO-GO** del path docking-NCE; SMRF/0Q.1 **prohíben** reabrir docking/NCE. **No hay commit ni patch en `next_iter_*` que registre supersesión.** Por fechas/commits: el plan **precede** a 0Q y permanece en el árbol sin actualización de estado → coexistencia sin cierre documental. |

---

## Ledger table

| ID | Path | Commit | Date | Decision | Status | Superseded by |
|----|------|--------|------|----------|--------|---------------|
| D2_22-NOGO | `results/reports/md_d2_22_20ns_summary.md` | `485bb00` | 2026-08-11 | NO-GO trinquete CB1; lead D2_22 descartado; MD pesada pausada | **NO-GO** | **NOT SUPERSEDED** (lead). CONFLICTO residual con docs legacy pre-NO-GO |
| 0Q-D-NOGO | `results/reports/qiu_0q_independent_scientific_audit.md` | `c43c0b7` (1ª: `d0e483f`) | Doc 2026-08-13 / commit 2026-08-16 | **D** NO-GO path docking-NCE Janusforge | **NO-GO** (path compute) | **NOT SUPERSEDED** (reafirmado por SMRF / 0Q.1) |
| 0Q.1-EXPAND | `results/reports/qiu_0q1_final_cursor_vs_gemini.md` | `c43c0b7` | 2026-08-15 | **EXPAND**; mono-CB2 **YES**; Yin-Yang law **NO** | **EXPAND** | **NOT SUPERSEDED** |
| 0Q-SMRF | `results/reports/qiu_0q_smrf_matrix.md` | `c43c0b7` | 2026-08-13 | **MODERATE**; Option B **ACTIVE**; 0M **RESERVE** | **ACTIVE** / **MODERATE** | **NOT SUPERSEDED** (0Q.1 lock); tensión vs Round1.9 STOP |
| NEXT-ITER-QIU | `results/reports/next_iter_pyrazole_qiu_plan.md` | `485bb00` / last `57551db` | 2026-08-11 | Eje Qiu docking **activo**; MD pausada | Doc = **ACTIVE** | **CONFLICTO DETECTADO** vs 0Q D NO-GO (sin patch de supersesión) |
| ROUND1.9 (contexto) | `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` | **UNTRACKED** | 2026-08-17 | GOLD_CONFIRMED=0; **PIPELINE = STOP** | **STOP** (documental Round1) | No en HEAD tracked; **CONFLICTO** de “próximo paso” vs SMRF ACTIVE / 0Q.1 EXPAND |

---

## What is the CURRENT scientific decision of JANUS?

From the ledger only (no winner by inference):

1. **D2_22** remains a **scientific NO-GO** as functional lead (`md_d2_22_20ns_summary.md` / `485bb00`).
2. **Compute path docking/MD/NCE** remains **D NO-GO** (`qiu_0q_independent_scientific_audit.md`; reaffirmed by SMRF and 0Q.1 bans).
3. **Simultaneously ACTIVE / EXPAND** (tracked, post-0Q): **0Q-SMRF = MODERATE + ACTIVE** and **0Q.1 = EXPAND** (literature/claim-split; mono-CB2 YES; Yin-Yang law NO) — both under `c43c0b7`.
4. **Simultaneously** the file `next_iter_pyrazole_qiu_plan.md` still self-describes Qiu docking as **ACTIVE** (last touch `57551db`, 2026-08-11) with **no superseding edit** after 0Q → **CONFLICTO DETECTADO**.
5. **Simultaneously** untracked **Round1.9** (2026-08-17) sets documentary calibration **PIPELINE = STOP** / GOLD=0 → **CONFLICTO** of next-step framing vs SMRF ACTIVE / 0Q.1 EXPAND.
6. **0M wet** remains **RESERVE** in the SMRF status lock (handoff may exist on `origin/master`, not critical path while SMRF runs).

**CONFLICTOs (list only; unresolved):**  
(A) `next_iter_*` ACTIVE docking vs 0Q **D NO-GO** compute;  
(B) Round1.9 **PIPELINE STOP** vs 0Q-SMRF **ACTIVE** / 0Q.1 **EXPAND**;  
(C) legacy docs still soft on D2_22 vs MD NO-GO report.

---

## next_iter vs 0Q

| Evento | Fecha | Commit |
|--------|-------|--------|
| D2_22 NO-GO + **creación** `next_iter_pyrazole_qiu_plan.md` | 2026-08-11 08:05 | `485bb00` |
| Update plan / start light dual docking (MD paused); last touch to `next_iter_*` | 2026-08-11 08:20 | `57551db` |
| 0Q independent audit **D NO-GO** (fecha documento) | 2026-08-13 | (texto) |
| 0Q añadido en historial (1ª) | 2026-08-13 20:23 | `d0e483f` |
| 0Q + SMRF + 0Q.1 en HEAD limpio | 2026-08-16 10:59 | `c43c0b7` |

**Por qué el plan “sigue existiendo” (solo fechas/commits):** fue **añadido** en `485bb00` y **última modificación** en `57551db` (ambos 11 ago). 0Q entra **después** (`d0e483f` 13 ago / `c43c0b7` 16 ago). **Ningún commit posterior modifica o archiva `next_iter_pyrazole_qiu_plan.md`.** Por tanto coexisten en el árbol: plan con status **ACTIVE docking** (11 ago) y auditoría **D NO-GO docking-NCE** (13–16 ago) **sin registro de supersesión en el plan** → **CONFLICTO DETECTADO**, no “plan borrado” ni “plan actualizado a STOP”.

---

## Verificación 485bb00 (`git show --stat`)

```
485bb00 Document D2_22 biophysical NO-GO and pause toward Qiu pyrazole iteration.
 docs/README.md                                    |  5 +-
 docs/lecciones_aprendidas_track1.md               | 27 +++++---
 results/reports/md_d2_22_20ns_summary.md          | 20 +++++-
 results/reports/next_iter_pyrazole_qiu_plan.md    | 56 +++++++++++++++++++++++
 results/reports/option_d_batch_d1_gate_summary.md |  7 +-
 results/reports/option_d_pivot_urb447.md          | 14 ++--
 6 files changed, 103 insertions(+), 26 deletions(-)
```

---

### 6. SWITCH-HYPOTHESIS-REFORM — OPEN / alostérico (2026-08-19)

| Campo | Valor |
|-------|--------|
| **ID** | SWITCH-HYPOTHESIS-REFORM |
| **Path** | `docs/switch_hypothesis_allosteric_reformulation.md` |
| **Fecha** | 2026-08-19 |
| **Decisión** | Reformulación metodológica: `THCV_ORTHOSTERIC_DESIGN` **PAUSED** (no descartado); `RETROSPECTIVE_AUDIT_PHASES_A_D` **CLOSED_AND_ARCHIVED**; `SWITCH_HYPOTHESIS` **OPEN_REFORMULATED**; pregunta rectora alostérica registrada; `DE_NOVO_GENERATION` / `THRESHOLD_MODIFICATION` **STOP**; Contract v1.0 **FROZEN**. |
| **Evidencia citada** | Bloque A–D (`external_audit_four_quadrants.md`); THCV seed/mapping; SMRF/0Q.1 (continuidad literaria). |
| **Estado actual** | **OPEN_HYPOTHESIS** — sin criterios de diseño ni moléculas nuevas. |
| **¿Superseded?** | **NOT SUPERSEDED** — complementa (no revoca) 0Q D NO-GO del path compute ortostérico. |

---

*Fin ledger `JANUS_DECISION_LEDGER_v1.0.md`.*
