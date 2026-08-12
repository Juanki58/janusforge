# Qiu 0N — Ge et al. 2023–style CB2 function-prediction protocol (Qiu-14)

> **Governance lock date:** 2026-08-12  
> **Scope:** Protocol / governance only. **No MD, no docking, no MM-GBSA/PBSA, no LRIP run.**  
> **Ligand:** Qiu compound **14** only.

---

## Executive governance (LOCKED)

| Field | Value |
|-------|-------|
| **Status** | `0N = READY / NOT EXECUTED (Gated)` |
| **Doc** | `results/reports/qiu_0n_ge2023_reproduction_protocol.md` |
| **Status one-pager** | `results/reports/qiu_0n_status.md` |
| **Pharmacological arbiter** | **H1-a CRO** (critical path unchanged) |
| **0N role** | Optional parallel compute track — **not a gate**, **not an H1-a substitute** |
| **Output labels (LOCKED)** | `consistente` \| `no consistente` \| `inconcluso` |

```text
Ge et al. 2023 approach
  → reproduce only as far as published main text + SI allow
  → apply to Qiu-14 (blind vs Ge benchmark signatures)
  → classify 0N result as consistente | no consistente | inconcluso
  → H1-a remains the experimental arbiter
```

Critical path for the program is unchanged: **CRO → wet H1-a**. 0N is an **optional parallel compute track**, not a gate on H1-a and not a substitute for wet pharmacology.

---

## Hard stops (LOCKED — non-negotiable)

1. **Do NOT reinterpret docking 0F–0J as function.**  
   Vina scores, MODEL 1 occupancy, and pose QC (0F–0J) are structural/docking artifacts only. They do **not** count as agonist/antagonist evidence under 0N or H1-a.

2. **Zero post-hoc tuning to force Qiu-14 agonist.**  
   No post-hoc threshold edits, signature cherry-picking, pose re-selection, or force-field tweaks aimed at forcing agonist concordance with the Qiu literature story.

3. **No in silico pharmacological PASS / KILL / FAIL.**  
   Even a perfect LRIP match to Ge agonist signatures is **hypothesis only** until wet H1-a. 0N never awards PASS/KILL/FAIL for H1-a.

Any violation of these hard stops invalidates the 0N run for program decision-making.

---

## Clasificación de resultado (LOCKED — only allowed labels)

0N may emit **exactly one** of:

| Label | Meaning |
|-------|---------|
| **consistente** | Qiu-14 LRIP / metrics match the Ge et al. **agonist** (or, if applicable, **antagonist**) benchmark signature under the **pre-registered** Ge criteria, without post-hoc retuning |
| **no consistente** | Clear mismatch vs the relevant Ge signature under the same pre-registered criteria |
| **inconcluso** | Missing fidelity, unstable MD, incomplete SI signatures, conflicting metrics, or criteria cannot be applied honestly |

**Then** (only when wet H1-a exists): compare 0N label ↔ H1-a experimental outcome as a **concordance check**. That comparison still does **not** rewrite H1-a PASS/KILL.

**Forbidden from 0N alone:** pharmacological PASS / FAIL / KILL; EC₅₀ claims; “Qiu-14 is a CB2 agonist” as a program fact.

---

## Gate de ejecución (LOCKED)

**Do NOT execute 0N** until a fidelity check confirms that Ge et al. parameters needed for an honest reproduction are available from the article and/or SI (or explicitly waived as non-critical with documented rationale).

| Gate state | When |
|------------|------|
| **BLOCKED (current)** | Protocol ready; SI templates / signature tables not yet extracted into repo; no authorization to run MD |
| **CLEARED to execute** | Requires separate user authorization **after** fidelity check closes critical TBDs (or marks them waived) |

**115 ns MD + LRIP remains BLOCKED** until explicit authorization after fidelity verification.

If critical article/SI data are missing → leave as **TBD**. **Do not invent** cutoffs, force-field knobs, residue lists, or signature vectors by inference.

---

## Repo assets checklist (LOCKED snapshot)

| Mark | Asset | Path / note |
|------|-------|-------------|
| [✓] | CB2 active | `data/targets/cb2/6PT0_rec.pdbqt` |
| [✓] | Qiu-14 ligand | `results/docking/qiu_0e/compound_14_lig.pdbqt` |
| [✓] | Seed pose 0F QC | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` **MODEL 1** |
| [!] | Membrane/MD engine | OpenMM + lipid17 pending **TBD-0N-11** |
| [X] | SI numeric tables | pending ingest **TBD-0N-03** |

---

## Next ops (document only — do not execute)

1. **Critical path:** send `results/reports/cro_package_h1a/SEND/` RFQs.
2. **Pre-exec 0N:** ingest Ge SI tables (`cn3c00580_si_001.pdf` / `cn3c00580_si_002.xlsx`) — **pending**; not done in this governance lock; do not invent tables.
3. **Gate:** 115 ns MD + LRIP remains **BLOCKED** until explicit auth after fidelity verification.

---

## 1. Bibliographic identity

| Field | Value |
|-------|-------|
| Title | Discovery of Potent and Selective CB2 Agonists Utilizing a Function-Based Computational Screening Protocol |
| Authors | Haixia Ge, Beihong Ji, Jiahui Fang, Jiayang Wang, Jing Li, Junmei Wang |
| Journal | *ACS Chemical Neuroscience* |
| Year / date | 2023 (published online 2023-10-12) |
| Volume / pages | 14, 3941–3958 |
| DOI | [10.1021/acschemneuro.3c00580](https://doi.org/10.1021/acschemneuro.3c00580) |
| PubMed Central | [PMC10623575](https://pmc.ncbi.nlm.nih.gov/articles/PMC10623575/) |
| SI (PDF) | [cn3c00580_si_001.pdf](https://pubs.acs.org/doi/suppl/10.1021/acschemneuro.3c00580/suppl_file/cn3c00580_si_001.pdf) |
| SI (XLSX RMSD) | [cn3c00580_si_002.xlsx](https://pubs.acs.org/doi/suppl/10.1021/acschemneuro.3c00580/suppl_file/cn3c00580_si_002.xlsx) |

**Classification metrics (cite accurately from paper):**

- Abstract / conclusions also state a rounded **~70%** success rate for the protocol application.
- Detailed evaluation on **42** compounds: functions of **29/42** correctly predicted → **overall prediction accuracy 69%**.
- Of **26** predicted CB2-selective agonists, **16** correctly predicted → **CB2 agonist success rate 62%**.
- Of **16** predicted antagonists / undetermined: **3** correctly as CB2 antagonists + **10** correctly inactive (paper narrative).

Pipeline stated: **docking → MD → MM-GBSA (LRIP decomposition) + MM-PBSA-WSAS → agonist/antagonist (or undetermined) call → cellular calcium mobilization assay**.

---

## 2. What Ge et al. actually did (from main text)

### 2.1 High-level protocol

1. Dock query ligand to CB target (best pose kept if docking score acceptable).
2. Build membrane MD system; run explicit-solvent MD; require stability.
3. Collect thousands of snapshots → **MM-GBSA** per-residue decomposition → **LRIP**.
4. Compare LRIP to signatures of known agonists (active receptors) / antagonists (inactive receptors).
5. End-point **MM-PBSA-WSAS** binding free energy.
6. Classify agonist vs antagonist/undetermined; validate with CHO calcium mobilization (CP55940 / AM630 / rimonabant controls).

### 2.2 Membrane / system composition (stated)

- Builder: **CHARMM-GUI**
- Lipid: **POPC** bilayer
- Water: **TIP3P**
- Salt: **0.15 M Na⁺/Cl⁻**
- Box: rectangle ≈ **95 × 95 × 95 Å³**
- Typical composition: CB receptor + ligand + ~**17 000** TIP3P waters + **58 Cl⁻** + **48 Na⁺** + **240 POPC**

### 2.3 Force field / engine (stated)

| Component | Choice |
|-----------|--------|
| Protein | **FF14SB** |
| Lipids | **Lipid14** |
| Ligand | **GAFF** + **RESP** charges (HF/6-31G\* via Gaussian 16; Antechamber) |
| Engine | **AMBER 18** (`PMEMD.cuda` / `PMEMD.mpi`) |

### 2.4 MD schedule (stated)

- Minimization: five × 10 000 steps; backbone restraints 20 → 10 → 5 → 1 → 0 kcal/mol/Å²
- Relaxation: heat 0 → 300 K in 50 K steps; **0.1 ns** per step; **1 fs** timestep
- Equilibrium + sampling: **2 fs**; T = **298.15 K**; Langevin γ = **5 ps⁻¹**; anisotropic pressure scaling, τ = **2 ps**, P_ref = **1 atm**; SHAKE on H
- **Total MD: 115 ns per complex**
- Postanalysis: **5000** snapshots evenly from **last 100 ns**

### 2.5 Free energy / LRIP (stated)

- LRIP from **MM-GBSA** decomposition (Hawkins et al. GB model) on **5000** snapshots
- Key residue keep if ligand–residue energy **stronger than −0.1 kcal/mol**
- Mean IPs of reference ligands = receptor active/inactive **signature**
- Similarity metrics: ASE, RMSE, AUE, **R²**
- Binding ΔG: **MM-PBSA-WSAS** on **200** of the 5000 snapshots; Delphi for polar solvation
- **Agonist call (paper criterion):** correlation **R > 0.84** (**R² > 0.7**) **and** binding energy **ΔE better than −10 kcal/mol**; else antagonist or undetermined

### 2.6 Hotspot residues reported (illustrative; not a substitute for full SI signatures)

- Agonist-leaning examples: **F2.61, I186, F2.64** (compound **6**); loop **I186** agonist-associated
- Antagonist-leaning examples: **L17, W6.48, V6.51, C7.42** (compound **39**); loop **L17** antagonist-associated
- Shared hotspots cited: **V3.32, T3.33, S7.39, F183, W5.43, I3.29**; loop **F183** for both

### 2.7 Reference ligand sets used for signatures (stated)

- Active CB1: AM-4030, AM-11542, THC, WIN-55,212-2  
- Active CB2: THC, AM-4030, WIN-55,212-2, UR-144  
- Inactive CB1: SR-147778, AM-251, MK-0364, THC  
- Inactive CB2: AM-10257, AM-630, THC  

---

## 3. What we CAN reproduce for Qiu-14 with janusforge assets

| Asset | Status | Path / note |
|-------|--------|-------------|
| CB2 active-state receptor | Available | `data/targets/cb2/6PT0_rec.pdbqt` (+ receptor prep summary under `data/targets/`) |
| Qiu-14 ligand PDBQT | Available (0E PASS) | `results/docking/qiu_0e/compound_14_lig.pdbqt` |
| Qiu-14 CB2 docked poses | Available (0F QC PASS) | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` — **pose seed only**, not function |
| Pose / visual QC chain | Available | 0G–0J reports — geometry only |
| Membrane POPC MD experience | Available (different ligand/receptor) | D2_22 on CB1 5TGZ, OpenMM, 20 ns (`results/reports/md_d2_22_20ns_summary.md`; script `scripts/run_md_openmm_membrane_lead.py`) |
| Conceptual LRIP workflow | Designable | Dock → membrane MD → MM-GBSA decomposition → compare to Ge signatures |

**Engine note (honest):** Ge used **AMBER 18 + CHARMM-GUI + Lipid14/FF14SB/GAFF**. Janusforge membrane precedent is **OpenMM + amber14/lipid17 + GAFF2**. A reproduction may use AMBER (closer fidelity) or OpenMM (local stack); either choice must be declared at execution time and counted in the fidelity gate — **not invented here as equivalent without check**.

---

## 4. Fidelity TBD matrix (LOCKED IDs — keep TBD; do not fill by inference)

Mark **TBD** until confirmed from SI or prior Ge/Wang methods papers — **no inference fills**.

| ID | Item | Why it matters |
|----|------|----------------|
| TBD-0N-01 | Exact docking engine / scoring / grid / exhaustiveness for Ge derivatives | Ge defers docking details to prior work; 0F Vina ≠ automatic Ge docking |
| TBD-0N-02 | Which PDB / model (active vs inactive CB2) for each signature arm | 0N for Qiu-14 CB2-agonist hypothesis likely needs **active** CB2; confirm Ge’s exact structures |
| TBD-0N-03 | Numerical mean IP signature vectors (Tables S1–S4 / S7 etc.) | Needed for R / R² comparison; SI PDF (`cn3c00580_si_001.pdf`) not ingested into repo yet |
| TBD-0N-04 | MD input templates / analysis scripts from SI | SI advertises “templates of the MD input file and trajectory analysis” (`cn3c00580_si_001.pdf` / `cn3c00580_si_002.xlsx`) |
| TBD-0N-05 | Exact GBSA / igb / saltcon / interior dielectric / nonpolar settings | Hawkins GB cited; full MMPBSA.py (or equivalent) knobs TBD |
| TBD-0N-06 | Exact Delphi / PB radii, grid, dielectric for MM-PBSA-WSAS | Polar solvation reproducibility |
| TBD-0N-07 | Exact definition of ΔE in the −10 kcal/mol agonist gate | Which end-point quantity (MM-GBSA vs MM-PBSA-WSAS term) |
| TBD-0N-08 | Equilibration length inside the 115 ns (beyond heating) | Only total 115 ns + last-100-ns sampling stated clearly |
| TBD-0N-09 | Replica policy (n replicas, seeds) | Not stated as multi-replica in main text excerpt |
| TBD-0N-10 | Full per-residue energy tables for reference agonists/antagonists | Beyond hotspot highlights |
| TBD-0N-11 | Whether OpenMM/lipid17/GAFF2 is acceptable substitute for AMBER18/Lipid14/GAFF | Fidelity gate decision — **do not assume yes** |
| TBD-0N-12 | Ligand RESP vs Meeko/AM1-BCC charges for Qiu-14 | Ge used RESP HF/6-31G\*; 0E used Meeko — charge path TBD for 0N |

**ID map (user governance):**

- TBD-0N-01/02 → docking engine/grid + active/inactive PDBs  
- TBD-0N-03/04 → IP signature tables S1–S4/S7 + MD/GBSA input templates (SI: `cn3c00580_si_001.pdf` / `cn3c00580_si_002.xlsx`)  
- TBD-0N-05/06 → GB/PB exact knobs  
- TBD-0N-07/08/09 → ΔE for −10 kcal/mol gate, equilibration, replicas  
- TBD-0N-11/12 → AMBER18/Lipid14/GAFF/RESP → OpenMM/lipid17/GAFF2/AM1-BCC substitution validation  

---

## 5. Proposed 0N workflow (Qiu-14 only) — NOT EXECUTED

**Blind function prediction** vs published Ge agonist/antagonist signatures. No SAR redesign. No extra docking campaigns as a substitute for this MD/LRIP track.

1. **Fidelity check (mandatory before run)** — extract SI signatures + MD templates; resolve TBD-0N-01…12 or waive with written rationale.
2. **Pose seed** — take Qiu-14 MODEL 1 (or pre-registered pose) from `compound_14_cb2_out.pdbqt` on **6PT0**; do **not** re-dock “until agonist-looking.”
3. **Membrane system** — CHARMM-GUI-like POPC + TIP3P + 0.15 M salt; composition target as close as documented (Ge typical counts as guide, not to invent missing knobs).
4. **MD** — aim for Ge-like **115 ns** with analysis on last **100 ns** (or document unavoidable deviation).
5. **MM-GBSA decomposition → LRIP** on 5000 frames if feasible; else document reduced sampling as **inconcluso** risk.
6. **MM-PBSA-WSAS** (or closest available) for the ΔE gate if that quantity is confirmed.
7. **Compare** Qiu-14 IP to Ge **active-CB2 agonist** signature (primary for H1-a story) and, if prepared, inactive-CB2 antagonist signature.
8. **Emit only:** `consistente` | `no consistente` | `inconcluso`.
9. **Archive** configs, seeds, software versions; no H1-a status change.

### Explicit rules (locked)

- **0N ≠ EC₅₀ prediction.** No potency from LRIP/ΔG.
- **0N does NOT change H1-a PASS/KILL.** Wet H1-a is sole pharmacological arbiter.
- If 0N says agonist-like (**consistente** with agonist signature) or antagonist-like — still **hypothesis until wet**.
- **No more docking rounds as substitute for 0N.** Further Vina campaigns do not replace membrane MD → LRIP.

---

## 6. Optional compute budget estimate (rough; not a run plan)

| Item | Rough estimate |
|------|----------------|
| Ge-like production | **~115 ns** / complex (analysis window **100 ns**) |
| Qiu-14 CB2 (primary) | **~115 ns** × 1 replica (minimum honest attempt) |
| Optional inactive-CB2 antagonist arm | **+~115 ns** if dual-signature comparison desired |
| Optional fidelity control (known agonist e.g. WIN on 6PT0) | **+~115 ns** — strongly recommended before trusting Qiu-14 call |
| Ballpark wall time | Same order as prior membrane MD experience, but **~5–6×** longer than the 20 ns D2_22 run per replica (GPU-dependent; **TBD** exact hours) |
| Postanalysis | 5000-frame GBSA decomp + 200-frame PBSA-WSAS — CPU-heavy; duration **TBD** |

**Not authorized to run.** Estimates only.

---

## 7. Relation to program gates

| Gate | Role of 0N |
|------|------------|
| H1-a (wet CB2) | **Unaffected.** Experimental arbiter. |
| H1-b / H2 / H3 | Unaffected. |
| IP / CRO critical path | 0N is **optional parallel compute**; critical path remains **CRO → H1-a**. |
| 0F–0J docking | Pose seed / QC only under Hard stop #1. |

Pointers:

- Status one-pager: [`qiu_0n_status.md`](qiu_0n_status.md)
- IP gate: [`docs/ip_gate_janusforge.md`](../../docs/ip_gate_janusforge.md)
- 0K plan: [`qiu_0k_validation_plan_h1_h2.md`](qiu_0k_validation_plan_h1_h2.md)
- H1-a wet handoff: [`qiu_0m_h1a_wet_handoff.md`](qiu_0m_h1a_wet_handoff.md)
- CRO SEND package: [`cro_package_h1a/SEND/`](cro_package_h1a/SEND/)

---

## 8. Verdict

**`0N = READY / NOT EXECUTED (Gated)`**

Paper (PMC + ACS DOI) was accessible for bibliographic identity, system composition, AMBER/CHARMM-GUI/POPC methods, LRIP criteria, and **69% / 62%** metrics. SI numerical signature tables and MD input templates are **not yet ingested** → listed as TBD; execution remains **gated** until fidelity check. No simulation was run under this document. Governance lock permanently records hard stops, output labels, TBD matrix, and assets checklist — **without executing MD/docking and without inventing SI parameters**.
