# Qiu 0N — Status one-pager

> **Fidelity audit:** 2026-08-12  
> **Scoped MD protocol (structural):** 2026-08-13 — [`qiu_0n_md_protocol_ready.md`](qiu_0n_md_protocol_ready.md)  
> **Prep blockers closure (stack / 6PT0 / TM / cost):** 2026-08-13 — [`qiu_0n_prep_blockers_closure.md`](qiu_0n_prep_blockers_closure.md) → **`0N = BLOCKED`** (exec)  
> **Benchmark protocol (parameter matrix):** [`qiu_0n_ge2023_benchmark_protocol.md`](qiu_0n_ge2023_benchmark_protocol.md)  
> **Gap analysis / Ge LRIP verdict:** [`qiu_0n_reproducibility_gap_analysis.md`](qiu_0n_reproducibility_gap_analysis.md)  
> **Governance lock (hard stops):** [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md)

## Status (two tracks — do not conflate)

| Track | Status |
|-------|--------|
| **Full Ge LRIP reproduction** (SI signatures, R/R², ΔE, MM-PBSA-WSAS) | **`NOT READY`** (execution blocked) — unchanged |
| **Scoped orthogonal MD stability protocol** (structural coherence only) | Design **`READY / NOT EXECUTED`**; **execute `BLOCKED`** — [`qiu_0n_prep_blockers_closure.md`](qiu_0n_prep_blockers_closure.md) |

Parameter audit counts (Ge track): **28 VERIFICADO** · **18 NO ESPECIFICADO** · **12 REQUIERE DECISIÓN**.

Main article recovered (Europe PMC OA). ACS SI (`cn3c00580_si_001.pdf` / `cn3c00580_si_002.xlsx`) **blocked** (Cloudflare 403) → signature tables / MD templates not ingested → **Ge LRIP still NOT READY**.

| Field | Value |
|-------|-------|
| Pharmacological arbiter | **H1-a CRO** (critical path unchanged) |
| 0N role | Optional parallel compute — **not a gate**, **not H1-a substitute** |
| Ge-track labels (LOCKED) | `consistente` \| `no consistente` \| `inconcluso`  
| | (= CONSISTENT WITH BENCHMARK \| INCONSISTENT \| INCONCLUSIVE) |
| Scoped MD labels (structural only) | **SUPPORT** \| **INCONCLUSIVE** \| **AGAINST** — **not** pharmacological PASS |

> **Note on prior wording:** `READY / NOT EXECUTED (Gated)` in the governance lock meant *protocol documented*. Execution readiness for **auditable Ge LRIP** under the stricter fidelity definition remains **NOT READY** until SI + critical TBDs close. The **scoped MD** doc is READY as preparation only (no run). Hard stops unchanged.

## Hard stops (LOCKED)

1. Do **not** reinterpret docking **0F–0J** as function.
2. **Zero** post-hoc tuning to force Qiu-14 agonist.
3. **No** in silico pharmacological PASS / KILL / FAIL.
4. **No MD / LRIP** until explicit auth; Ge LRIP additionally requires fidelity CLEARED (SI).

## Assets checklist

| Mark | Asset | Path |
|------|-------|------|
| [✓] | CB2 active | `data/targets/cb2/6PT0_rec.pdbqt` |
| [✓] | Qiu-14 ligand | `results/docking/qiu_0e/compound_14_lig.pdbqt` |
| [✓] | Seed pose 0F QC | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` MODEL 1 |
| [✓] | Ge main PDF (OA) | `data/papers/ge_2023_acs_chem_neurosci/cn3c00580_europepmc.pdf` |
| [✓] | Scoped MD protocol | `results/reports/qiu_0n_md_protocol_ready.md` |
| [✓] | Prep blockers closure | `results/reports/qiu_0n_prep_blockers_closure.md` |
| [!] | Membrane/MD engine | OpenMM+lipid17 pending TBD-0N-11 waiver + Docker/CUDA |
| [X] | SI numeric tables / MD templates | ACS SI blocked — TBD-0N-03/04 |

## Fidelity TBD (keep TBD — do not invent)

| IDs | Topic |
|-----|-------|
| TBD-0N-01/02 | Docking engine/grid + active/inactive PDBs |
| TBD-0N-03/04 | IP signatures S1–S4/S7 + MD/GBSA templates (`cn3c00580_si_001.pdf` / `cn3c00580_si_002.xlsx`) |
| TBD-0N-05/06 | GB/PB exact knobs |
| TBD-0N-07/08/09 | ΔE (−10 kcal/mol gate), equilibration, replicas |
| TBD-0N-11/12 | AMBER18/Lipid14/GAFF/RESP → OpenMM/lipid17/GAFF2/AM1-BCC validation |
| TBD-0N-MD-* | Scoped MD prep knobs — listed in [`qiu_0n_md_protocol_ready.md`](qiu_0n_md_protocol_ready.md) §14 |

## Next ops (document only)

1. **Critical path:** send `cro_package_h1a/SEND/` RFQs.
2. **Pre-exec Ge LRIP:** obtain ACS SI via institutional/browser access; extract tables — **pending**.
3. **Scoped MD:** protocol READY as design; prep blockers audited → **`0N = BLOCKED`** for execute ([`qiu_0n_prep_blockers_closure.md`](qiu_0n_prep_blockers_closure.md)); **do not execute** until waivers + Docker/CUDA restore + GPU auth (prefer H1-a RFQs).
4. **Gate:** 115 ns MD + LRIP **BLOCKED** for Ge track until SI fidelity + explicit auth.

**No MD executed under these audits.**
