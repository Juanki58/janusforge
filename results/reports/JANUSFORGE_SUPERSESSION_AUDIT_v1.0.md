# JANUSFORGE — SUPERSESSION AUDIT v1.0

**Tipo:** auditoría documental de estados operativos (ACTIVE / GO / NO-GO / STOP / RESERVE / BLOCKED / EXPAND / variantes)  
**Fecha:** 2026-08-17  
**HEAD verificado:** `c43c0b77c0cfb0070e8da40982cf0020d40b4539` (`cursor/pr5-0q-audit-smrf-0q1-clean`)  
**Único archivo creado:** este informe  
**Prohibiciones respetadas:** sin borrar docs; sin cambiar historia/resultados científicos; sin editar fuentes; sin docking/MD/NCE; sin commit.

---

## 1. Method

1. **Authority inputs (read-only):**
   - Decision Ledger Audit v1.0 (respuesta de auditoría 2026-08-17; clasificaciones CURRENT / SUPERSEDED / CONFLICT / UNRESOLVED / HISTORICAL) — *no hay archivo en repo; conclusiones citadas en §6*
   - `results/reports/JANUS_DECISION_LEDGER_v1.0.md`
   - `results/reports/JANUSFORGE_RECOVERED_RESEARCH_STATE.md`
2. **Evidence:** open the actual files; `git log` / `git show` / `git ls-files` / `git cat-file` for commit SHAs and presence on HEAD vs `origin/master`.
3. **Scope of “operational status”:** declarations that frame *next work* or program state — ACTIVE / ACTIVO / GO / NO-GO / STOP / PIPELINE STOP / RESERVE / BLOCKED / descartado / EXPAND (when it selects next workstream). Evidence statuses (GOLD_CONFIRMED, REVIEW_REQUIRED, LEVEL0_*) audited only when they co-declare pipeline STOP.
4. **Supersession rule:** a later decision **supersedes** only if (a) same operational domain and (b) later source/commit explicitly replaces or the Decision Ledger Audit lists SUPERSEDED. **Do not invent** supersession across distinct scopes → mark **UNRESOLVED**. Opposing statuses without a closing patch → **CONFLICT** (not auto-SUPERSEDED).
5. **Banner column:** recommended only; **no banners applied** in this audit.

---

## 2. Supersession table (all audited docs)

| path | commit | declared status | later superseding decision | superseding commit | correct status as historical | needs SUPERSEDED banner? (Y/N) |
|------|--------|-----------------|----------------------------|--------------------|------------------------------|--------------------------------|
| `results/reports/md_d2_22_20ns_summary.md` | `485bb00` (2026-08-11) | **NO-GO** trinquete CB1; D2_22 **descartado**; GPU pausada; “go exploratorio débil” **already marked superseded in-file** | — (self is authority for lead NO-GO) | — | **CURRENT** NO-GO (lead). Prior soft GO = SUPERSEDED *inside* this file | **N** |
| `docs/criterio_exito_janus.md` | last touch `7025f1d` (2026-08-11 08:02; *before* `485bb00`) | “**Lead Track 1 / Opción D: JANUS_D2_22** … no-go trinquete / **go exploratorio débil**”; Track D “(activo)” | D2_22 **descartado**; go exploratorio **superseded** (`md_d2_22_20ns_summary.md`) | `485bb00` | Soft lead/GO framing = **SUPERSEDED** / CONFLICT residual vs MD | **Y** |
| `docs/mapa_ligandos_janus_cb1_cb2.md` | last touch `57551db` (2026-08-11) | “**JANUS_D2_22 es el lead** … **go exploratorio débil**”; “**eje Qiu activo**” | Same D2_22 NO-GO (`485bb00`); Qiu docking ACTIVE later **CONFLICT** vs 0Q D NO-GO (not closed) | `485bb00` (D2_22); 0Q = `d0e483f`/`c43c0b7` (CONFLICT, not supersession) | Soft D2_22 lead/GO = **SUPERSEDED**; “eje Qiu activo” = **CONFLICT** (not SUPERSEDED) | **Y** (for D2_22 soft lead/GO language) |
| `results/reports/next_iter_pyrazole_qiu_plan.md` | created `485bb00`; last `57551db` | Title/**Status:** eje Qiu **ACTIVO (docking only)**; MD pausada | 0Q **D — NO-GO** path docking-NCE; SMRF/0Q.1 ban reopen docking | `d0e483f` / `c43c0b7` | **CONFLICT** — HISTORICAL ACTIVE pre-0Q; **no** patch of supersession on this file | **N** *(do not invent SUPERSEDED; see CONFLICT)* |
| `docs/lecciones_aprendidas_track1.md` | last `57551db` | D2_22 **Descartado** (NO-GO) = aligned; “**Eje Qiu pirazol \| Activo (docking only)**” | Qiu ACTIVE vs 0Q D NO-GO | `c43c0b7` | D2_22 row = **CURRENT**; Qiu ACTIVE row = **CONFLICT** | **N** (CONFLICT on Qiu ACTIVE line only) |
| `results/reports/option_d_pivot_urb447.md` | last `57551db` | D2_22 **descartado**; MD **pausada**; Qiu docking done context | — | — | **CURRENT** for D2_22 NO-GO / MD pause | **N** |
| `results/reports/option_d_batch_d1_gate_summary.md` | last `485bb00` | Ex-lead; **D2_22 descartado** (NO-GO); GPU pausada | — | — | **CURRENT** | **N** |
| `results/reports/md_membrane_20ns_summary.md` | `2abb3c3` (2026-08-09) | **NO-GO** Track 1 fitocannabinoide / H1_02c vs THCV | Pivot Option D (`82ce0f5`) then D2_22 closed (`485bb00`) — does **not** reopen H1 | — | **CURRENT** as H1/membrane axis NO-GO | **N** |
| `results/reports/qiu_pyrazole_batch1_gate_summary.md` | `57551db` | Docking Batch 1 done; **MD pausada** (gate result, not program ACTIVE claim) | 0Q bans *new* docking campaigns; does not rewrite this historical gate | `c43c0b7` | **CURRENT** as historical gate snapshot | **N** |
| `results/reports/qiu_0q_independent_scientific_audit.md` | HEAD `c43c0b7` (1ª `d0e483f` 2026-08-13) | **D — NO-GO** path Janusforge docking/NCE | Reaffirmed by SMRF / 0Q.1; not revoked | — | **CURRENT** (path compute). **CONFLICT** with next_iter ACTIVE | **N** |
| `results/reports/qiu_0q_smrf_matrix.md` | `c43c0b7` (1ª `b3402e3`) | Option B **ACTIVE**; `0Q-SMRF = MODERATE`; Option A **0M = RESERVE**; no reopen docking/NCE | 0Q.1-FINAL locks MODERATE **unchanged** | — | **CURRENT** | **N** |
| `results/reports/qiu_0q1_final_cursor_vs_gemini.md` | `c43c0b7` | **EXPAND** (literature/claim-split only); mono-CB2 **YES**; Yin-Yang law **NO**; no NCE/docking/MD | No later tracked revocation | — | **CURRENT** | **N** |
| `results/reports/qiu_0q1_primary_audit_A_pairs.md` | `c43c0b7` | Intermediate 0Q.1; recommends **EXPAND**; SMRF MODERATE unchanged | FINAL (`qiu_0q1_final_*`) is authority for EXPAND | `c43c0b7` (same ship) | **CURRENT** as input; FINAL supersedes only as *ranking of deliverable*, same EXPAND | **N** |
| `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` | **UNTRACKED** (doc 2026-08-17) | **PIPELINE = STOP**; GOLD_CONFIRMED=0; REVIEW=9 | Relation to SMRF ACTIVE / 0Q.1 EXPAND = **UNRESOLVED** (distinct scopes) | — | **CURRENT** *within Round1 documentary calibration*; not program-wide authority | **N** |
| Round1.x siblings declaring **PIPELINE STOP** (e.g. `ROUND1.3_CROSS_VALIDATION.md`, `ROUND1.4_*`, `ROUND1.8_*`, `DOCUMENTARY_CB_AFFINITY_EFFICACY_MATRIX.md`, `ROUND1_ORDEN12_*`) | mostly untracked | **PIPELINE = STOP** (Round1 calibration) | Same UNRESOLVED vs SMRF/0Q.1 scopes | — | **CURRENT** for Round1 pipeline discipline | **N** |
| `qiu_0m_h1a_wet_handoff.md` @ `db46e9a` (not in HEAD WT) | `db46e9a` (2026-08-12) | **`0M = BLOCKED`** | Refresh **`0M = RESERVE`** while SMRF ACTIVE | `58b6c6b` / `origin/master` text; SMRF lock `c43c0b7` | **SUPERSEDED** (BLOCKED → RESERVE) | **Y** *if that blob is opened* |
| `qiu_0m_h1a_wet_handoff.md` @ `origin/master` | via `58b6c6b` / master merge | **`0M = RESERVE`**; WET NOT EXECUTED | Aligns with SMRF Option A | — | **CURRENT** (on master); **absent from HEAD** | **N** (file missing on this branch) |
| `results/reports/cro_package_h1a/02_ficha_h1a.md` | on `origin/master` line; may be absent HEAD | Conditional “0M = BLOCKED” if TBD missing | Program status = RESERVE (SMRF), not live BLOCKED verdict | — | Operational *gate language*, not CURRENT program BLOCKED | **N** |
| `docs/quimioma_cannabico_cb1_cb2.md` | early (`cf3f26a` era; cannabis-first) | “**Norte operativo** … cannabis-first / THCV” | Pivot Option D / post-H1 NO-GO / post-0Q (Recovered State CONFLICT #2) | `82ce0f5`+ | **CONFLICT** of “norte” framing (not a clean GO/STOP supersession) | **N** |
| `docs/guia_maestra_biotecnologia_quimiotipos.md` | `82ce0f5`+ | Post-H1: sintéticos Janus prioritarios; H1 NO-GO cited | Partially dated vs post-0Q; not opposing ACTIVE docking claim | — | **CURRENT** as Norma L0; note Recovered State “parcialmente desfasada vs post-0Q” | **N** |
| `docs/ip_gate_janusforge.md` | tracked | **Status: OPERATIVE PROTOCOL** | Unrelated to D2_22/0Q path decisions | — | **CURRENT** (protocol) | **N** |
| `results/reports/AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` | untracked 2026-08-17 | Soft-drug fenotipo **NO INTEGRABLE**; ADME CONDICIONAL | No later revocation found | — | **CURRENT** (integration audit) | **N** |

### Brief notes (special-attention set)

| Doc | Note |
|-----|------|
| **next_iter** | Still self-describes Qiu docking **ACTIVE**; never edited after 0Q → **CONFLICT**, not SUPERSEDED. |
| **criterio / mapa** | Soft “lead / go exploratorio débil” survives past `485bb00` → **SUPERSEDED** language still readable as operative → banner **Y**. |
| **D2_22 MD summary** | Authority for lead **NO-GO**; already labels prior soft GO as superseded. |
| **0Q** | CURRENT D NO-GO compute path. |
| **0Q-SMRF** | CURRENT ACTIVE / MODERATE / 0M RESERVE. |
| **0Q.1** | CURRENT EXPAND (literature only). |
| **0M** | CURRENT = **RESERVE** (SMRF + master handoff). Historical **BLOCKED** (`db46e9a`) = SUPERSEDED. Handoff **missing on HEAD**. |
| **Round1.9** | CURRENT STOP *for Round1 calibration*; vs SMRF/EXPAND = **UNRESOLVED** (do not invent program-wide supersession). |

---

## 3. Documents needing SUPERSEDED banner (recommended only — do not apply)

| # | path | Why (banner text sketch — not applied) |
|---|------|----------------------------------------|
| 1 | `docs/criterio_exito_janus.md` | Soft “Lead … go exploratorio débil” superseded by `md_d2_22_20ns_summary.md` / `485bb00` (Decision Ledger Audit: SUPERSEDED soft GO + CONFLICT residual). |
| 2 | `docs/mapa_ligandos_janus_cb1_cb2.md` | Same soft lead/GO language; still present after `57551db`. |
| 3 | `qiu_0m_h1a_wet_handoff.md` @ commit `db46e9a` only | Historical **`0M = BLOCKED`** superseded by **`0M = RESERVE`** (`58b6c6b` / `origin/master` + SMRF). Not present on HEAD WT. |

**Not listed as SUPERSEDED-banner (would invent supersession):**

- `next_iter_pyrazole_qiu_plan.md` / Qiu ACTIVE rows in `lecciones_aprendidas_track1.md` → Decision Ledger Audit = **CONFLICT** (optional *CONFLICT / STALE STATUS* banner is a separate recommendation, not SUPERSEDED).
- Round1.9 / SMRF / 0Q.1 → **UNRESOLVED** scope relation.

---

## 4. Documents CURRENT (no supersession)

| path | Current operational reading |
|------|----------------------------|
| `results/reports/md_d2_22_20ns_summary.md` | D2_22 lead **NO-GO**; MD/GPU heavy **paused** |
| `results/reports/qiu_0q_independent_scientific_audit.md` | **D NO-GO** docking-NCE path |
| `results/reports/qiu_0q_smrf_matrix.md` | SMRF **ACTIVE** / **MODERATE**; 0M **RESERVE** |
| `results/reports/qiu_0q1_final_cursor_vs_gemini.md` | **EXPAND** (literature/claim-split); mono-CB2 YES; Yin-Yang law NO |
| `results/reports/qiu_0q1_primary_audit_A_pairs.md` | 0Q.1 input; EXPAND; MODERATE lock |
| `results/reports/option_d_pivot_urb447.md` | D2_22 descartado; MD pausada |
| `results/reports/option_d_batch_d1_gate_summary.md` | Ex-lead; D2_22 descartado |
| `results/reports/md_membrane_20ns_summary.md` | H1/membrane **NO-GO** |
| `results/reports/qiu_pyrazole_batch1_gate_summary.md` | Historical Batch 1 gate (MD pausada) |
| `docs/lecciones_aprendidas_track1.md` | D2_22 descartado **CURRENT**; Qiu ACTIVE line excluded (CONFLICT) |
| `qiu_0m_h1a_wet_handoff.md` @ `origin/master` | **RESERVE** (file absent on HEAD) |
| `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` | Round1 **PIPELINE STOP** / GOLD=0 (scope-local) |
| Round1.x STOP siblings | Same Round1 pipeline discipline |
| `docs/ip_gate_janusforge.md` | OPERATIVE PROTOCOL |
| `results/reports/AUDIT_CONTROLLED_DEACTIVATION_INTEGRATION_v1.0.md` | Soft-drug NO INTEGRABLE (fenotipo) |

---

## 5. CONFLICT / UNRESOLVED pairs (from prior audit; do not resolve)

### CONFLICT (Decision Ledger Audit — documented)

| ID | Pair | Why not SUPERSEDED |
|----|------|-------------------|
| C1 | `next_iter_pyrazole_qiu_plan.md` **ACTIVE docking** (`57551db`) vs `qiu_0q_independent_scientific_audit.md` **D NO-GO** (`d0e483f`/`c43c0b7`) | Same compute/docking domain; **no** edit/archive of `next_iter_*` after 0Q. Satellites: Qiu ACTIVE in `lecciones_aprendidas_track1.md`; “eje Qiu activo” in `mapa_ligandos_*`. |
| C2 | Soft D2_22 “lead / go exploratorio débil” in `criterio_exito_janus.md` + `mapa_ligandos_janus_cb1_cb2.md` vs MD **NO-GO** (`485bb00`) | Soft language never patched; MD report is authority. Soft GO content = SUPERSEDED; *documents* remain CONFLICT until banner/edit. |
| C3 (Recovered State) | `docs/quimioma_cannabico_cb1_cb2.md` cannabis-first norte vs guia/pivot/post-H1 synthetic north | Framing conflict; not a clean ACTIVE/STOP supersession card. |

### UNRESOLVED (Decision Ledger Audit — do not invent supersession)

| ID | Pair | Why UNRESOLVED |
|----|------|----------------|
| U1 | Round1.9 **PIPELINE STOP** (2026-08-17, untracked) vs 0Q-SMRF **ACTIVE** / 0Q.1 **EXPAND** (`c43c0b7`) | Texts declare **different scopes** (Round1 Gold/calibration vs SMRF literature matrix). No joint authority doc. Ledger v1.0 “CONFLICTO de próximo paso” = **over-classification** per Decision Ledger Audit → keep **UNRESOLVED**. |
| U2 | Authority of 0M handoff **on this HEAD** | SMRF cites path; file **absent** on HEAD; RESERVE exists on `origin/master`. Gap ≠ revocation. |

---

## 6. Source of truth for banner recommendations

Cite **Decision Ledger Audit v1.0** classifications (2026-08-17; response-only audit of `JANUS_DECISION_LEDGER_v1.0.md`):

| Classification | Items used here |
|----------------|-----------------|
| **CURRENT** | D2_22 NO-GO; 0Q D NO-GO (path compute); 0Q-SMRF ACTIVE/MODERATE; 0Q.1 EXPAND; 0M RESERVE (via SMRF) |
| **SUPERSEDED** | “Go exploratorio débil” / prior soft D2_22 gate; `0M = BLOCKED` (`db46e9a`) vs later RESERVE |
| **CONFLICT** | next_iter ACTIVE docking vs 0Q D NO-GO; legacy soft D2_22 docs vs MD NO-GO |
| **UNRESOLVED** | Round1.9 PIPELINE STOP ↔ SMRF ACTIVE / 0Q.1 EXPAND (distinct scopes); 0M handoff presence on HEAD |
| **HISTORICAL** | Qiu docking ACTIVE @ `57551db` as chronological pre-0Q state (tree content unchanged) |

Supporting inventory (not competing authority): `JANUS_DECISION_LEDGER_v1.0.md` §cards 1–5 + CONFLICTOs A–C; `JANUSFORGE_RECOVERED_RESEARCH_STATE.md` §7 / §11.

**Banner policy derived:** recommend **SUPERSEDED** banner only for Decision Ledger Audit **SUPERSEDED** (or documents whose only operative claim is that superseded soft status). Do **not** apply SUPERSEDED banners to **CONFLICT** or **UNRESOLVED** pairs.

---

## Parent return

| Field | Value |
|-------|--------|
| **Path** | `results/reports/JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md` |
| **Count needing SUPERSEDED banners** | **3** (2 on HEAD WT + 1 historical blob) |
| **Paths** | `docs/criterio_exito_janus.md`; `docs/mapa_ligandos_janus_cb1_cb2.md`; `qiu_0m_h1a_wet_handoff.md` @ `db46e9a` (not in HEAD WT) |
| **Source files edited** | **None** (only this audit file created) |

---

*Fin `JANUSFORGE_SUPERSESSION_AUDIT_v1.0.md`.*
