# Qiu 0N — Scoped orthogonal MD stability protocol

# **0N = READY / NOT EXECUTED**

> **Protocol date:** 2026-08-13  
> **Scope:** Preparation / design only. **No MD, docking, NCE, wet work.** **No modify PDBQT or existing results.**  
> **No invented thresholds or literature values.** Unjustified knobs → explicit **TBD**.  
> **Ge SI / full LRIP reproduction:** still **NOT READY** (see companions). This document is a **scoped** orthogonal stability protocol that does **not** claim Ge agonist/antagonist signatures are available in-repo.  
> **Companions:** [`qiu_0n_ge2023_benchmark_protocol.md`](qiu_0n_ge2023_benchmark_protocol.md) · [`qiu_0n_reproducibility_gap_analysis.md`](qiu_0n_reproducibility_gap_analysis.md) · [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md) · [`qiu_0n_status.md`](qiu_0n_status.md)

---

## Status distinction (do not conflate)

| Track | Verdict | Meaning |
|-------|---------|---------|
| **Full Ge LRIP reproduction** (SI signatures, R/R², ΔE gates, MM-PBSA-WSAS) | **NOT READY** | ACS SI blocked; TBD-0N-03/04/05/06/07 open — unchanged |
| **This document: scoped MD structural-coherence protocol** | **READY / NOT EXECUTED** | Design complete enough to *authorize later*; **zero compute run** |

Hard stops from governance lock remain: **0N ≠ agonism/EC₅₀**; **H1-a** is sole pharmacological arbiter; no in silico PASS/KILL.

---

## Final table (decision surface)

| Pregunta | Diseño | Coste local | Coste cloud | Tiempo | Evidencia que aporta | Limitación |
|----------|--------|-------------|-------------|--------|----------------------|------------|
| ¿La pose 0F MODEL 1 de Qiu-14 en CB2 6PT0 es estable/coherente en membrana POPC a escala de precedencia local? | MINIMAL: 1× Qiu-14, OpenMM/lipid17/GAFF2, **20 ns** (precedente D2_22 / panel membrana), 1 réplica, métricas estructurales | **Estimates TBD calibrated** — electricidad/host sunk; GPU local GTX 1060–class documentada | N/A si local | **~0.7–1.3 días / 20 ns** (plan membrana GTX 1060); D2_22 wall ~12 h documentado para 20 ns | Persistencia de pose / contactos / RMSD-RMSF — info **antes de pagar H1-a** | 1 réplica; ≠ Ge 115 ns; ≠ función |
| ¿Hay control de stack (agonista conocido) que valide que el pipeline no “rompe” todo? | ROBUST (+control): +1 complejo control (ej. WIN-55,212-2 u otro ref. Ge active-CB2) misma pila | ×2 vs minimal (orden) | ×2 vs minimal (orden) | ×2 wall (secuencial) | Si control falla → Qiu-14 = **INCONCLUSIVE** por stack | Control ligand prep/pose **TBD**; no es Ge-exact |
| ¿Un análogo canónico (D2_20) o Qiu-15 aporta contraste geométrico? | ROBUST opcional: +1 comparator (D2_20 **o** Qiu-15, no ambos por defecto) | +1× complex | +1× | +1× | Contraste occupation/persistence vs Qiu-14 | Chemotipo D2 ≠ Qiu; no farmacología |
| ¿Concordancia LRIP vs firmas Ge (R>0.84, ΔE<−10)? | **OUT OF SCOPE** hasta SI ingest | — | — | — | No aportable honestamente ahora | SI **NOT READY** |
| ¿Agonismo / EC₅₀ / PASS H1-a? | **FORBIDDEN** | — | — | — | Ninguna — wet only | Hard stop |

**Coste cloud ($):** **estimates TBD calibrated** (no tarifas cloud firmes en repo). Usar rangos de wall-time local como ancla de calibración, no precios inventados.

---

## RECOMENDACIÓN

**Diseñar y dejar listo el escenario MINIMAL (Qiu-14 × 20 ns × 1 réplica, métricas estructurales); no ejecutar hasta autorización explícita.** No lanzar Ge-LRIP ni 115 ns “como Ge” mientras SI esté bloqueada. Si se autoriza cómputo, preferir MINIMAL primero; ROBUST solo si el coste extra (control +/o comparator) se justifica antes de H1-a RFQ spend.

**GO / NO-GO propuesto para decidir si *ejecutar* 0N**

| Decisión | Cuándo |
|----------|--------|
| **GO execute (scoped MD)** | Usuario autoriza explícitamente GPU + acepta motor OpenMM/lipid17/GAFF2 (TBD-0N-11 waiver) + acepta que el output es SUPPORT/INCONCLUSIVE/AGAINST **estructural**, no farmacológico + CRO/H1-a path no se retrasa por esperar 0N |
| **NO-GO execute** | Prioridad absoluta = enviar RFQs H1-a sin paralelizar GPU; o se exige Ge-exact LRIP (entonces permanece **NOT READY** hasta SI); o no se acepta waiver de stack/cargas |

**Debe autorizarse explícitamente antes de cualquier ejecución**

1. Gasto de GPU / tiempo de máquina (local y/o cloud).  
2. Waiver documentado TBD-0N-11 (OpenMM/lipid17/GAFF2 ≠ AMBER18/Lipid14/GAFF) y TBD-0N-12 (cargas: path local vs RESP).  
3. Escenario elegido: **MINIMAL** vs **ROBUST** (y lista exacta de complejos).  
4. Congelación de pose seed (MODEL 1 existente; **sin** re-dock / sin editar PDBQT).  
5. Confirmación de que LRIP/Ge signatures **no** se interpretarán (fuera de alcance hasta SI).  
6. Labels de salida pre-registrados (§9) — sin retuning post-hoc.

---

## 1. Exact scientific question — CAN vs CANNOT

### 0N (this scoped protocol) CAN answer

- Whether the **existing** Qiu-14 CB2 0F **MODEL 1** pose, embedded in a POPC membrane system built with the **documented local stack**, remains **structurally coherent** over the chosen MD window (pose retention, ligand/protein RMSD/RMSF behavior, persistence of key contact shells already noted in 0G/0H — as **observables**, not as new “binding constants”).  
- Whether instability, ligand egress, or catastrophic TM/backbone blow-up appears at the **same order of timescale** as prior project membrane MD (**20 ns** precedent).  
- Optionally (ROBUST): whether a declared control or one geometric comparator behaves differently under the **same** stack (still structural).

### 0N CANNOT answer

- CB2 **agonism**, **antagonism**, **EC₅₀**, **Ki**, or any pharmacological PASS/KILL.  
- Concordance with Ge et al. **LRIP signatures** (R / R² / ΔE gates) — SI tables **not in repo** → full Ge reproduction remains **NOT READY**.  
- That docking Vina scores (0F–0J) equal affinity or function (hard stop).  
- Exact Ge AMBER18 + Lipid14 + RESP + Delphi/WSAS fidelity with the default janusforge membrane path.  
- Whether to skip or rewrite H1-a — **H1-a remains arbiter**.

**User objective (honest):** use MD as an **orthogonal structural benchmark** so that interactions/states for Qiu-14 (+ tight comparators if authorized) are judged stable/coherent enough to add information **before paying H1-a** — not to replace H1-a.

---

## 2. Compounds worth simulating + justification

| Priority | Compound | Simulate? | Justification (tight) |
|----------|----------|-----------|------------------------|
| **P0** | **Qiu-14** | **Yes — primary** | Validation vehicle for H1-a story; full 0D–0H chain; governance lock ligand; 0F MODEL 1 seed exists |
| **P1 (optional ROBUST)** | **JANUS_D2_20** *or* **Qiu-15** | At most **one** | D2_20: highest geometric overlap / canonical_like vs Qiu map (0G/0H/0I) without elevating by Vina. Qiu-15: same chemotype family + TYR25 shell note — pick **either** for contrast, not both by default |
| **Defer** | Qiu-20 | No (default) | Near-identical occupation to 14 (0G Jaccard contacts 1.00 vs 14) — little orthogonal info per ns |
| **Defer** | Qiu-24 | No (default) | Rotated N1-morph documented; secondary unless pose-rotation hypothesis is the question |
| **Defer / avoid** | JANUS_D2_06 | No (default) | Redundant with D2_20 for this question (same canonical pattern) |
| **Do not** | JANUS_D2_22 | **No** for this 0N scoped ask | Already **NO-GO** as functional lead after CB1 membrane MD; CB2 feature_swap; not the H1-a validation vehicle |

**Rule:** do **not** simulate everything. Default authorization target = **Qiu-14 alone**.

---

## 3. Starting structure / receptor and how obtained

| Asset | Path | Role |
|-------|------|------|
| Receptor CB2 active | `data/targets/cb2/6PT0_rec.pdbqt` | Program CB2 structure (prep summary: `data/targets/receptor_prep_summary.json`, box `6PT0_rec.box.txt`) |
| Receptor PDB (non-PDBQT) | **Missing** — `data/targets/cb2/6PT0_rec.pdb` | Conversion/prep for membrane build = **TBD** at execution (must not silently invent; document method when authorized) |
| Qiu-14 ligand PDBQT | `results/docking/qiu_0e/compound_14_lig.pdbqt` | Ligand prep (0E) |
| Pose seed | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` **MODEL 1** | **Locked seed** — no pose shopping; no PDBQT rewrite |
| Pose PDB | **Missing** — `…/compound_14_cb2_out.pdb` | Export for MD build = **TBD** at execution (read-only transform from existing MODEL 1; do not re-dock) |

**Provenance:** local AutoDock Vina 0F on 6PT0 — **not** Ge docking (TBD-0N-01). Acceptable for *orthogonal stability of our pose*, not for “Ge reproduction.”

---

## 4. Proposed simulation system

Aligned with **documented local membrane precedent** and Ge *composition themes* where published — without claiming CHARMM-GUI/AMBER18 identity:

| Element | Proposal | Source |
|---------|----------|--------|
| Bilayer | POPC | Ge main text; local `amber14/lipid17` POPC |
| Water | TIP3P | Ge + local script |
| Salt | 0.15 M NaCl (+ neutralize) | Ge + local |
| Builder | `packmol-memgen` (OpenMM path) **or** CHARMM-GUI if later waived | Local: [`scripts/run_md_openmm_membrane_lead.py`](../../scripts/run_md_openmm_membrane_lead.py); Ge: CHARMM-GUI (**REQUIERE DECISIÓN** / TBD) |
| Box / lipid counts | Ge *typical* ~95³ Å, ~240 POPC — **not** forced as exact Qiu-14 counts | Exact Qiu-14 atom/lipid counts = **TBD** until built |
| Barostat (local path) | `MonteCarloMembraneBarostat` XY iso / Z free (precedent) | `md_membrane_20ns_plan.md` — ≠ Ge anisotropic scaling wording |
| Temperature (local path) | **300 K** (precedent runs) | Local docs; Ge sampling T = **298.15 K** → difference = **TBD** if Ge-fidelity claimed |

---

## 5. Force field + params (justified or TBD)

| Component | Local stack (demonstrated) | Ge et al. 2023 (main text) | For this scoped 0N |
|-----------|----------------------------|----------------------------|--------------------|
| Protein | `amber14-all` | FF14SB | Use local unless AMBER track authorized (**TBD-0N-11**) |
| Lipid | lipid17 POPC | Lipid14 | Same |
| Ligand | GAFF2 (OpenFF / `gaff-2.11`) | GAFF + **RESP** HF/6-31G\* | Local GAFF2 path **or** RESP if fidelity track — **TBD-0N-12** |
| Engine | OpenMM CUDA (Docker on Windows) | AMBER 18 PMEMD.cuda | Local unless waived otherwise |
| Min / equil (local precedent) | Min → NVT+NPT membrane equil ~**1 ns** → production | Ge: 5×10k min restraints; heat 0→300 K; then 115 ns total | For MINIMAL: **follow local membrane script defaults** (documented). Ge schedule only if fidelity track CLEARED |
| Timestep / constraints | As in local script (SHAKE/H-constraints per OpenMM setup) | 1 fs heat; 2 fs eq/sample; SHAKE H | Do not invent new knobs — use script defaults or Ge literals if AMBER track |
| Nonbonded cutoff / PME | **TBD** (not fully specified in Ge 2023 Methods extract; local = script defaults) | NO ESPECIFICADO in Ge audit | **TBD** — freeze to script/version hash at auth |

---

## 6. Minimum reasonable duration

| Precedent | Duration | Citation |
|-----------|----------|----------|
| Local membrane MD (H1 panel, D2_22) | **20 ns** production (+ ~1 ns equil) | `md_membrane_20ns_plan.md`, `md_membrane_20ns_summary.md`, `md_d2_22_20ns_summary.md` |
| Ge et al. production | **115 ns** / complex; analysis last **100 ns** | Ge main text / 0N benchmark protocol |
| Local soluble smoke | **2 ns** | `md_lead_2ns_summary.md` — too short as primary membrane answer |

**Minimum reasonable for this scoped protocol:** **20 ns** production — the **only** membrane length with completed project precedent.  
**Not claimed as “optimal.”** Longer windows (e.g. toward Ge 115 ns) are **ROBUST / fidelity** options, not required for MINIMAL readiness.  
Equilibration length inside a Ge-like 115 ns total remains **TBD-0N-08** if that track is chosen.

---

## 7. Number of replicas

| Source | Replica policy |
|--------|----------------|
| Ge main text (audit) | Multi-replica **not stated** → **TBD-0N-09** |
| Local membrane runs | **1 replica** × 20 ns (explicit limitation in summaries) |
| Membrane plan “critical reading” | Suggests ≥3 seeds **if** go is marginal — aspirational note in plan, **not** a locked Ge/project requirement for 0N |

**For MINIMAL:** **1 replica** (matches demonstrated local practice; mark statistical weakness).  
**For ROBUST:** replica/seed count = **TBD** until user sets n (do not invent n=3 as mandatory without auth).

---

## 8. Predefined metrics (structural / coherence only)

Emit metrics that are **already in the local membrane toolkit** or are plain structural observables. **Do not** invent numeric PASS cutoffs.

### In scope (MINIMAL)

1. **Run integrity:** production completes (`EXIT_CODE=0` / script `status: ok`); no obvious blow-up.  
2. **Ligand heavy-atom RMSD** vs starting MODEL 1 frame (time series + mean±sd) — report values; **no invented cutoff**.  
3. **Protein Cα RMSD** (and optional TM-focused RMSD if CB2 TM ranges are pre-declared at auth — ranges used previously were for **CB1 5TGZ UniProt**; CB2 6PT0 TM index map = **TBD**).  
4. **RMSF** (ligand atoms; protein residues in orthosteric shell from 0G/0H contact lists as **descriptive**).  
5. **Interaction persistence:** % frames with contacts already highlighted in 0G/0H (distance criteria must be those **already used in project scripts** or declared before run — e.g. prior H-bond proxy 3.5 Å in membrane script; **do not invent new Å/angle gates**).  
6. **Membrane sanity (recommended if script exposes):** area/lipid, thickness, or lipid RMSD if available — prior reports noted these were often **not** reported → treat as **TBD** if not in tooling.

### Out of scope until SI / fidelity CLEARED

- LRIP / MM-GBSA per-residue vectors vs Ge Tables S1–S4/S7.  
- R > 0.84 / R² > 0.7 / ΔE better than −10 kcal/mol **agonist call** (Ge literals exist in paper but **cannot be applied** without signatures + energy pipeline — keep **out of minimal scenario**).  
- MM-PBSA-WSAS / Delphi.

### CB2 “benchmark-backed” metrics

Only Ge-published analysis window (5000 frames / last 100 ns) and energy gates are “benchmark-backed” — and they require SI + energy stack → **not** part of MINIMAL READY protocol. No other CB2 MD numeric benchmark tables are verified in-repo for Qiu-14.

---

## 9. SUPPORT / INCONCLUSIVE / AGAINST (structural coherence only)

Map carefully to locked ES labels from Ge-LRIP governance; **vocabulary for this MD doc** (user request):

| This MD protocol label | Maps to Ge-track lock (approx.) | Meaning (**structural / stability / coherence vs starting pose & membrane integrity**) |
|------------------------|----------------------------------|----------------------------------------------------------------------------------------|
| **SUPPORT** | ~ `consistente` / CONSISTENT WITH BENCHMARK | Under pre-registered metrics and controls, the complex **supports** that the 0F MODEL 1 interaction pose remains **coherent/stable enough** over the run window to add orthogonal structural info before H1-a |
| **AGAINST** | ~ `no consistente` / INCONSISTENT | Clear **structural** failure modes (e.g. ligand leaves pocket / catastrophic instability / contacts of interest collapse in a way that **undercuts** trusting that pose as a stable structural hypothesis) under the same pre-registered readouts |
| **INCONCLUSIVE** | ~ `inconcluso` / INCONCLUSIVE | Cannot decide honestly: missing control, unfinished run, stack/charge waiver conflict, metrics conflict, CB2 TM definitions unset, or results dominated by single-replica noise |

**Why these labels (and why not pharmacology):**

- They answer *stability/coherence of a computational pose ensemble*, not *receptor signaling*.  
- They are **not** pharmacological PASS / FAIL / KILL.  
- **H1-a** alone decides CB2 function for the program.  
- **No numeric threshold** (RMSD Å, % contact) is invented here to auto-fire SUPPORT/AGAINST — the call is a **pre-registered qualitative reading** of the metric panel + controls, logged before opening results when possible.

**Forbidden readings:** “SUPPORT ⇒ agonist”; “AGAINST ⇒ inactive”; “INCONCLUSIVE ⇒ skip H1-a.”

---

## 10. Controls needed

| Control | MINIMAL | ROBUST | Role |
|---------|---------|--------|------|
| Pose lock (MODEL 1 only) | **Required** | Required | Anti pose-shopping |
| Analysis freeze (scripts/hashes) | **Required** | Required | Anti post-hoc tuning |
| Known CB2 agonist on same stack/receptor | Optional | **Strongly recommended** | If control unstable → Qiu-14 **INCONCLUSIVE** |
| Apo or antagonist arm | No | Optional / **TBD** | Not required for scoped stability |
| Empty-membrane / integrity metrics | If tooling allows | Yes if tooling allows | Build sanity |
| Blind to H1-a outcome | N/A until wet | N/A | 0N must not wait on wet to be “valid structural” |

---

## 11–12. Option A (local PC) vs Option B (cloud GPU)

### Option A — Local PC (documented stack)

| Item | Value |
|------|-------|
| Hardware (documented) | OpenMM **CUDA**; prior runs via Docker GPU passthrough; wall-time table for **GTX 1060 6GB** |
| Throughput (membrane POPC estimate) | **~15–30 ns/day** (`md_membrane_20ns_plan.md`) |
| 20 ns wall (estimate) | **~0.7–1.3 days / complex** (+ equil ~1–2 h; build minutes–tens of minutes) |
| D2_22 empirical wall | ~**12 h** for 20 ns (log window 2026-08-10T14:24Z → 2026-08-11T02:34Z) — **same order** as plan |
| 115 ns Ge-like (if ever authorized) | Order **~5–6×** longer than 20 ns per complex (`qiu_0n_ge2023_reproduction_protocol.md`) — **estimate TBD calibrated** |
| Cost $ | Host/electricity **estimates TBD calibrated** (no $ table in repo) |
| Limitations | Single consumer GPU; Windows **requires Docker/WSL** (AmberTools not win-64); script historically CB1-oriented — CB2 6PT0 adaptation **TBD** at auth; not Ge-exact |

### Option B — Cloud GPU

| Item | Value |
|------|-------|
| Hardware | Modern CUDA GPU instance (**exact SKU TBD** at auth) |
| Time | Scale from local ns/day using instance throughput — **estimates TBD calibrated**; expect wall **shorter** than GTX 1060 if GPU is faster, not guaranteed without benchmark smoke |
| Cost $ | **Estimates TBD calibrated** (no firm cloud invoice anchors in repo) |
| Limitations | Data egress / IP hygiene (no public push of coords/DCD); env must reproduce `environment-md-membrane.yml` + Docker patterns; still ≠ Ge AMBER18 unless rebuilt |

---

## 13. MINIMAL (low-cost) vs ROBUST

| | **MINIMAL** | **ROBUST** (adds) |
|--|-------------|-------------------|
| Complexes | Qiu-14 only | + positive control (± one of D2_20 **or** Qiu-15) |
| Duration | **20 ns** production (local precedent) | Longer window **TBD** (e.g. approach Ge 115 ns) and/or more seeds (**TBD-0N-09**) |
| Engine | OpenMM/lipid17/GAFF2 with explicit waiver | Same **or** AMBER18/Lipid14/RESP track if separately authorized |
| Metrics | Structural RMSD/RMSF/contact persistence/run integrity | + membrane integrity suite; + control-gated interpretation; still **no** Ge LRIP unless SI CLEARED |
| Labels | SUPPORT / INCONCLUSIVE / AGAINST (structural) | Same labels; control failure forces INCONCLUSIVE |
| Cost / time | 1× baseline | ~2–3× (control + optional comparator) plus any longer ns |
| What ROBUST does **not** buy alone | Ge signature concordance; pharmacological truth | — |

---

## 14. TBD list (keep TBD — do not invent)

| ID | Item |
|----|------|
| TBD-0N-MD-01 | Exact export path 6PT0 + MODEL 1 → membrane-ready PDB (no PDBQT mutation in place) |
| TBD-0N-MD-02 | CB2 TM residue index map for TM-RMSD (prior UniProt ranges were CB1) |
| TBD-0N-MD-03 | Contact persistence definition freeze (which 0G/0H shells; distance/angle = script literals only) |
| TBD-0N-MD-04 | Whether CHARMM-GUI or packmol-memgen is the authorized builder |
| TBD-0N-MD-05 | T = 300 K (local) vs 298.15 K (Ge) if any Ge-likeness claimed |
| TBD-0N-MD-06 | Cloud SKU + $/hr calibration |
| TBD-0N-MD-07 | ROBUST replica count / seeds |
| TBD-0N-MD-08 | Positive-control ligand identity + pose provenance |
| TBD-0N-11 | OpenMM/lipid17/GAFF2 vs AMBER18/Lipid14/GAFF (from Ge gap matrix) |
| TBD-0N-12 | RESP vs Meeko/AM1-BCC charge path |
| TBD-0N-03/04/05/06/07 | Ge SI signatures + GB/PB/ΔE — **block LRIP only**; do not block scoped structural MD if LRIP stays out of scope |
| TBD-0N-08/09 | Ge equilibration split / replicas — relevant only if 115 ns Ge-like track chosen |

---

## 15. No invented thresholds

This protocol **does not** set numeric cutoffs such as “RMSD < X Å = SUPPORT” or “contact > Y% = GO.”  
Ge literals (R > 0.84, ΔE better than −10 kcal/mol, −0.1 kcal/mol residue keep) are **cited only as Ge-published** and are **not applicable** in the MINIMAL scenario without SI + energy pipeline.  
Prior membrane go/no-go rules in Track-1 plans applied to **different ligands/questions** and are **not** reused as silent Qiu-14 thresholds.

---

## Relation to master roadmap

- **Preparation only** under this file.  
- Critical path remains **CRO → wet H1-a** (`cro_package_h1a/SEND/`).  
- 0N scoped MD is **optional parallel compute**, not a gate.  
- Full Ge LRIP track stays **NOT READY** until SI ingest + fidelity re-audit.

---

## Pointers

- Status: [`qiu_0n_status.md`](qiu_0n_status.md)  
- **Prep blockers closure (stack / 6PT0 / TM / cost):** [`qiu_0n_prep_blockers_closure.md`](qiu_0n_prep_blockers_closure.md) → execution verdict **`0N = BLOCKED`** (waivers + Docker/CUDA ops)  
- Ge parameter audit (NOT READY for LRIP): [`qiu_0n_ge2023_benchmark_protocol.md`](qiu_0n_ge2023_benchmark_protocol.md)  
- Gap analysis: [`qiu_0n_reproducibility_gap_analysis.md`](qiu_0n_reproducibility_gap_analysis.md)  
- Governance / hard stops: [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md)  
- Evidence context: [`qiu_0i_evidence_matrix.md`](qiu_0i_evidence_matrix.md)  
- Local MD capability: [`md_d2_22_20ns_summary.md`](md_d2_22_20ns_summary.md) · [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md)

**No MD executed under this document.**
