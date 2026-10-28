# Qiu 0N — Ge et al. 2023 benchmark protocol (parameter audit)

> **Audit date:** 2026-08-12  
> **Scope:** Recover article + SI access status; extract **literal** parameters only.  
> **Hard stop:** **NO MD, docking, rescoring, MM-GBSA/PBSA, or LRIP execution.**  
> **No invented knobs:** absent values stay **TBD** / classified below.  
> **Ligand (when later authorized):** Qiu compound **14** only.  
> **Related governance:** [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md) · [`qiu_0n_status.md`](qiu_0n_status.md) · gap analysis [`qiu_0n_reproducibility_gap_analysis.md`](qiu_0n_reproducibility_gap_analysis.md)

---

## Final verdict

# **NOT READY**

Enough main-text MD system settings are published to *describe* a Ge-like run, but critical **SI artifacts** (Tables S1–S4 / S5–S7 signature & Ki tables; MD input templates; RMSD workbook) were **not recoverable** this session. An auditable LRIP comparison to Ge’s agonist/antagonist signatures **cannot** be run without inventing those vectors or undecided engine substitutions. **Do not spend GPU until SI is ingested and this verdict is re-audited under explicit authorization.**

| Count (parameter matrix rows) | N |
|-------------------------------|--:|
| **VERIFICADO EN PUBLICACIÓN/SI** | **28** |
| **NO ESPECIFICADO** | **18** |
| **REQUIERE DECISIÓN** | **12** |

*(Full row list in §4. Counts exclude bibliographic / governance rows.)*

---

## 1. Bibliographic identity (verified)

| Field | Value |
|-------|-------|
| Title | Discovery of Potent and Selective CB2 Agonists Utilizing a Function-Based Computational Screening Protocol |
| Authors | Haixia Ge, Beihong Ji, Jiahui Fang, Jiayang Wang, Jing Li, Junmei Wang |
| Journal | *ACS Chemical Neuroscience* |
| Year | 2023 (published online 2023-10-12) |
| Volume / pages | 14, 3941–3958 |
| DOI | [10.1021/acschemneuro.3c00580](https://doi.org/10.1021/acschemneuro.3c00580) |
| PMCID | [PMC10623575](https://pmc.ncbi.nlm.nih.gov/articles/PMC10623575/) |
| License (Unpaywall) | CC-BY (hybrid OA) |
| SI PDF (advertised) | `cn3c00580_si_001.pdf` — [ACS suppl URL](https://pubs.acs.org/doi/suppl/10.1021/acschemneuro.3c00580/suppl_file/cn3c00580_si_001.pdf) |
| SI XLSX (advertised) | `cn3c00580_si_002.xlsx` — [ACS suppl URL](https://pubs.acs.org/doi/suppl/10.1021/acschemneuro.3c00580/suppl_file/cn3c00580_si_002.xlsx) |

**Benchmark metrics (main text, literal):** overall prediction accuracy **69%** (29/42); CB2 agonist success rate **62%** (16/26); abstract/conclusions also state rounded **~70%**.

**Pipeline (literal):** docking → membrane MD → MM-GBSA decomposition → **LRIP** vs known agonist/antagonist signatures → MM-PBSA-WSAS ΔE gate → cellular calcium mobilization assay.

---

## 2. Article / SI recovery status

| Asset | Status | Path / note |
|-------|--------|-------------|
| Main PDF (Europe PMC OA) | **Recovered** | `data/papers/ge_2023_acs_chem_neurosci/cn3c00580_europepmc.pdf` (~7.9 MB) |
| Text extract | **Recovered** | `data/papers/ge_2023_acs_chem_neurosci/cn3c00580_europepmc_extract.txt` |
| Access log | Written | `data/papers/ge_2023_acs_chem_neurosci/ACCESS_LOG.md` |
| Unpaywall JSON | Recovered | `data/papers/ge_2023_acs_chem_neurosci/cn3c00580_unpaywall_probe.json` |
| ACS SI PDF `cn3c00580_si_001.pdf` | **Blocked** | HTTP 403 / Cloudflare challenge |
| ACS SI XLSX `cn3c00580_si_002.xlsx` | **Blocked** | HTTP 403 / Cloudflare challenge |
| NCBI PMC HTML/PDF | **Blocked** | reCAPTCHA / POW browser gate |
| SI numeric Tables S1–S7 | **Not in repo** | Advertised in Associated Content; **not extracted** |
| MD input templates (SI) | **Not in repo** | Advertised in Associated Content; **not extracted** |

**Governance note:** Prior lock [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md) used status wording `READY / NOT EXECUTED (Gated)` meaning *protocol documented, execution gated*. This audit’s **READY** definition is stricter (auditable reproduction without inventing critical knobs) → current execution readiness = **NOT READY**. Hard stops and H1-a primacy are unchanged.

---

## 3. Classification legend (exactly one per parameter)

| Label | Meaning |
|-------|---------|
| **VERIFICADO EN PUBLICACIÓN/SI** | Stated explicitly in Ge et al. 2023 main text (or would be in recovered SI). |
| **NO ESPECIFICADO** | Not stated in recovered sources; **must not be filled by assumption**. |
| **REQUIERE DECISIÓN** | Program/engine choice needed before any future run (fidelity / local stack); not inventable as “Ge-equivalent” without waiver. |

---

## 4. Parameter matrix (literal extract)

### 4.1 Structure CB2 / receptor models

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-01 | Receptor family | CB1 / CB2 active vs inactive arms for signatures | **VERIFICADO EN PUBLICACIÓN/SI** (concept) |
| P-02 | Exact PDB / cryo-EM IDs used for Ge derivative MD | Not stated in Methods; cites crystal/cryo-EM availability; prep “details… from previous publication” (Ji et al. 2020) | **NO ESPECIFICADO** |
| P-03 | Homology modeling vs experimental structure for 2023 derivatives | Methods: hierarchical methods include homology modeling; docking “same as that of reference ligands” | **NO ESPECIFICADO** (which model for which arm) |
| P-04 | Active-CB2 agonist signature ligands | THC, AM-4030, WIN-55,212-2, UR-144 | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-05 | Inactive-CB2 antagonist signature ligands | AM-10257, AM-630, THC | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-06 | Active-CB1 / inactive-CB1 reference sets | Active CB1: AM-4030, AM-11542, THC, WIN-55,212-2; Inactive CB1: SR-147778, AM-251, MK-0364, THC | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-07 | Qiu-14 target structure for 0N (janusforge) | Local active CB2 **6PT0** (program asset; not Ge’s stated PDB) | **REQUIERE DECISIÓN** |

### 4.2 Preparation / docking

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-08 | Docking engine / scoring / grid / exhaustiveness | Deferred: “details… previous publication” (Ji 2020); not restated in 2023 Methods | **NO ESPECIFICADO** |
| P-09 | Pose selection | “best docking pose”; survive if “decent docking score” | **NO ESPECIFICADO** (numeric score cutoff) |
| P-10 | Protein prep (protonation, loops, termini) | Not restated beyond hierarchy + prior paper | **NO ESPECIFICADO** |
| P-11 | Qiu-14 pose seed for later 0N | Local 0F MODEL 1 on 6PT0 (program choice; ≠ Ge docking) | **REQUIERE DECISIÓN** |

### 4.3 Membrane / composition / solvation / ions

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-12 | Membrane builder | CHARMM-GUI | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-13 | Lipid type | POPC bilayer | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-14 | Water model | TIP3P | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-15 | Salt | 0.15 M Na⁺/Cl⁻ | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-16 | Box | Rectangle ≈ 95 × 95 × 95 Å³ | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-17 | Typical counts | ~17 000 TIP3P; 58 Cl⁻; 48 Na⁺; 240 POPC (+ receptor + ligand) | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-18 | Exact Qiu-14 system atom/lipid counts | Not applicable until built; Ge gives *typical* only | **NO ESPECIFICADO** |

### 4.4 Force field / engine / ligand charges

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-19 | Protein FF | FF14SB | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-20 | Lipid FF | Lipid14 | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-21 | Ligand FF | GAFF | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-22 | Ligand charges | RESP from HF/6-31G\* (Gaussian 16); Antechamber topologies | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-23 | MD engine | AMBER 18 (`PMEMD.cuda` / `PMEMD.mpi`) | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-24 | Janusforge substitute stack | OpenMM + amber14/lipid17 + GAFF2 (local precedent) | **REQUIERE DECISIÓN** (TBD-0N-11) |
| P-25 | Qiu-14 charge path vs Ge RESP | Local 0E Meeko/AM1-BCC-style PDBQT ≠ RESP | **REQUIERE DECISIÓN** (TBD-0N-12) |

### 4.5 Minimization / equilibration / T / P / timestep / duration / replicas

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-26 | Minimization | Five × 10 000 steps; backbone restraints 20 → 10 → 5 → 1 → 0 kcal/mol/Å² | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-27 | Heating / relaxation | 0 → 300 K in 50 K steps; 0.1 ns per step; **1 fs** timestep | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-28 | Equilibrium + sampling thermostat | Langevin γ = 5 ps⁻¹; T = **298.15 K** | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-29 | Barostat | Anisotropic pressure scaling; τ = 2 ps; P_ref = 1 atm | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-30 | Constraints | SHAKE on H | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-31 | Eq/sampling timestep | **2 fs** | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-32 | Total MD length | **115 ns** per complex | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-33 | Length of “equilibrium” vs “sampling” within 115 ns | Only total 115 ns + last-100-ns analysis stated | **NO ESPECIFICADO** |
| P-34 | Replicas / random seeds | Not stated as multi-replica | **NO ESPECIFICADO** |
| P-35 | Nonbonded cutoff / PME grid / etc. | Not stated in 2023 Methods excerpt | **NO ESPECIFICADO** |

### 4.6 Trajectory analysis / LRIP / energies

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-36 | Snapshot count / window | **5000** evenly from **last 100 ns** | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-37 | LRIP method | MM-GBSA per-residue decomposition; Hawkins et al. GB | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-38 | Key-residue energy keep threshold | Stronger than **−0.1 kcal/mol** | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-39 | Signature construction | Mean IPs of reference ligands = active/inactive signature | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-40 | Similarity metrics | ASE, RMSE, AUE, **R²** | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-41 | Agonist call (R) | R > **0.84** (R² > **0.7**) **and** ΔE better than **−10 kcal/mol** | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-42 | Numeric mean IP vectors (Tables S1–S4 / S7) | In SI PDF; **not recovered** | **NO ESPECIFICADO** *(in repo)* |
| P-43 | Compound 6 / 39 example residue energies (S5/S6) | Cited in text for selected residues; full tables in SI | **NO ESPECIFICADO** *(full vectors)* |
| P-44 | Exact GBSA knobs (igb, saltcon, dielectric, nonpolar) | Hawkins cited; AMBER `igb`/MMPBSA.py settings not listed | **NO ESPECIFICADO** |
| P-45 | MM-PBSA-WSAS frames | **200** of the 5000 | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-46 | Polar solvation solver | Delphi | **VERIFICADO EN PUBLICACIÓN/SI** |
| P-47 | Delphi radii / grid / ε_in / ε_out | Not stated | **NO ESPECIFICADO** |
| P-48 | Exact definition of ΔE in −10 kcal/mol gate | Text uses ΔE / ΔGbind interchangeably in places; which end-point term | **NO ESPECIFICADO** |
| P-49 | MD input templates + trajectory analysis scripts | Advertised in SI PDF | **NO ESPECIFICADO** *(blocked)* |
| P-50 | RMSD plots workbook | SI XLSX | **NO ESPECIFICADO** *(blocked)* |

### 4.7 Janusforge mapping knobs (not Ge text)

| ID | Parameter | Literal value (if any) | Class |
|----|-----------|------------------------|-------|
| P-51 | Accept OpenMM/lipid17/GAFF2 as Ge substitute | Not in paper; local stack only | **REQUIERE DECISIÓN** |
| P-52 | Whether to recompute Ge reference signatures locally | Needed if SI vectors unavailable | **REQUIERE DECISIÓN** |
| P-53 | Blind analysis controls (pre-registration) | Program requirement for honest 0N | **REQUIERE DECISIÓN** |
| P-54 | Outcome vocabulary for 0N | CONSISTENT WITH BENCHMARK / INCONSISTENT / INCONCLUSIVE (EN) ≡ consistente / no consistente / inconcluso (ES lock) | **REQUIERE DECISIÓN** *(locked labels; EN aliases below)* |
| P-55 | Pharmacological arbiter | Wet **H1-a** only | **REQUIERE DECISIÓN** *(program lock — not Ge)* |
| P-56 | Authorization to spend GPU | Explicit future user auth after fidelity | **REQUIERE DECISIÓN** |
| P-57 | Inactive-CB2 antagonist arm for Qiu-14 | Optional dual-signature; not mandated by Ge for every query | **REQUIERE DECISIÓN** |
| P-58 | Positive-control fidelity MD (e.g. WIN on 6PT0) before Qiu-14 | Recommended for audit; not Ge-mandated | **REQUIERE DECISIÓN** |

---

## 5. What janusforge can reproduce *exactly* vs only approximately

| Ge component | Exact with current stack? | Note |
|--------------|---------------------------|------|
| CHARMM-GUI POPC + TIP3P + 0.15 M salt membrane MD | **No (exact)** | Local: OpenMM + packmol-memgen / lipid17 POPC ([`scripts/run_md_openmm_membrane_lead.py`](../../scripts/run_md_openmm_membrane_lead.py); D2_22 20 ns on **CB1 5TGZ**) |
| AMBER 18 + Lipid14 + FF14SB + GAFF + RESP | **No** | Not the default janusforge membrane path |
| 115 ns production + last-100-ns / 5000-frame analysis | **Conceptually yes** | Duration is a run setting; **not authorized**; prior membrane runs were **20 ns** |
| Hawkins GB MM-GBSA decomposition → LRIP | **Not implemented as Ge pipeline** | No audited MMPBSA.py / OpenMM GBSA LRIP workflow in-repo for CB2 |
| MM-PBSA-WSAS + Delphi | **No** | Delphi/WSAS path not established in janusforge reports |
| Compare to Ge SI signature tables | **Blocked** | SI not ingested |
| Docking seed for Qiu-14 | **Available (local Vina)** | 0E/0F assets — **not** Ge docking |

**Honest summary:** janusforge can run *a* membrane MD on CB2-like systems with OpenMM/lipid17/GAFF2 after authorization, but that is **not** an exact Ge et al. software reproduction. Exact AMBER18/Lipid14/RESP/Delphi/WSAS fidelity is outside the demonstrated stack unless rebuilt and waived.

---

## 6. Files / structures for Qiu-14 and CB2

| Asset | Exists? | Path |
|-------|---------|------|
| CB2 receptor PDBQT (6PT0) | **Yes** | `data/targets/cb2/6PT0_rec.pdbqt` |
| CB2 box / prep meta | **Yes** | `data/targets/cb2/6PT0_rec.box.txt` · `data/targets/receptor_prep_summary.json` |
| CB2 receptor PDB (non-PDBQT) | **Missing** | `data/targets/cb2/6PT0_rec.pdb` |
| Qiu-14 ligand PDBQT | **Yes** | `results/docking/qiu_0e/compound_14_lig.pdbqt` |
| Qiu-14 CB2 poses (0F) | **Yes** | `results/docking/qiu_0f/compound_14_cb2_out.pdbqt` (MODEL 1 seed) |
| Qiu-14 CB2 pose PDB | **Missing** | `results/docking/qiu_0f/compound_14_cb2_out.pdb` |
| Ge SI signature tables / MD templates | **Missing** | blocked ACS SI |
| Inactive CB2 structure for antagonist arm | **Missing / TBD** | not prepared as 0N asset |
| Membrane MD script (OpenMM) | **Yes** | `scripts/run_md_openmm_membrane_lead.py` |
| Prior membrane MD report (different system) | **Yes** | `results/reports/md_d2_22_20ns_summary.md` |

---

## 7. Full computational pipeline that WOULD run later (NOT launched)

```text
[GATE] SI ingest + fidelity audit → CLEARED + explicit GPU auth
   ↓
0. Pre-register blind controls + outcome labels (§8–9)
1. Pose seed: Qiu-14 MODEL 1 from compound_14_cb2_out.pdbqt on 6PT0
   (no re-dock to force agonist-looking pose)
2. Ligand charges: RESP HF/6-31G* if fidelity track; else document waiver TBD-0N-12
3. Build membrane system: POPC + TIP3P + 0.15 M NaCl (CHARMM-GUI or declared substitute)
4. MD: Ge-like min → heat → eq/sample → 115 ns; archive seeds/versions
5. Collect 5000 frames from last 100 ns (or document reduced sampling → INCONCLUSIVE risk)
6. MM-GBSA per-residue decomp (Hawkins GB) → LRIP; keep E < −0.1 kcal/mol residues
7. Compare IP to Ge active-CB2 agonist signature (from SI or recomputed refs under waiver)
8. MM-PBSA-WSAS on 200 frames (or closest declared method) for −10 kcal/mol ΔE gate
9. Optional: inactive-CB2 antagonist signature arm
10. Emit exactly one label: CONSISTENT WITH BENCHMARK | INCONSISTENT | INCONCLUSIVE
11. Archive; do NOT change H1-a PASS/KILL
```

**Not launched. Not estimated as authorized work.**

---

## 8. Blind analysis controls (anti-tuning)

Pre-register **before** any MD/LRIP:

1. **Pose lock:** MODEL 1 from existing 0F PDBQT only; no pose shopping.
2. **Signature lock:** Ge SI vectors (or pre-declared recomputed reference set) frozen before Qiu-14 analysis.
3. **Threshold lock:** R > 0.84 and ΔE < −10 kcal/mol exactly as published; no post-hoc retuning to force agonist.
4. **Engine lock:** Declare AMBER18 track vs OpenMM substitute + waiver **before** run.
5. **Positive control first (recommended):** known CB2 agonist on same stack; if control fails signature recovery → Qiu-14 call = **INCONCLUSIVE**.
6. **No docking reinterpretation:** 0F–0J scores/occupancy are not function.
7. **Analysis code freeze:** commit analysis scripts/hashes before opening Qiu-14 LRIP results.
8. **Single primary arm:** active-CB2 agonist signature is primary for H1-a story; antagonist arm secondary if run.

---

## 9. Predefined outcomes (not pharmacology)

| Label (EN) | Label (ES lock) | Meaning |
|------------|-----------------|---------|
| **CONSISTENT WITH BENCHMARK** | consistente | Qiu-14 LRIP/ΔE meet pre-registered Ge agonist (or declared antagonist) criteria without retuning |
| **INCONSISTENT** | no consistente | Clear mismatch under same criteria |
| **INCONCLUSIVE** | inconcluso | Missing SI/fidelity, unstable MD, incomplete signatures, conflicting metrics, or criteria cannot be applied honestly |

**None of these = pharmacological activity.** Wet **H1-a** remains the sole arbiter of CB2 function for program PASS/KILL.

---

## 10. Ge et al. method vs 0F/0G — what 0N adds / does not

| Dimension | Ge et al. 2023 | Janusforge 0F / 0G | 0N adds | 0N does **not** |
|-----------|----------------|--------------------|---------|-----------------|
| Goal | Predict agonist vs antagonist/undetermined | Pose QC / geometry vs D1 | Function-*hypothesis* vs Ge LRIP signatures | Replace H1-a; claim EC₅₀ |
| Structure | Membrane MD + energy decomp | Vina pose on 6PT0 | Dynamics + LRIP track | Prove signaling |
| Score | R / R² + ΔE gates | Vina affinity estimate | Benchmark concordance label | Pharmacological PASS/KILL |
| Validation | CHO calcium assay | Visual/geometry QC | Concordance check *after* wet H1-a | Standalone wet substitute |
| Engine | AMBER18 / Lipid14 / RESP | AutoDock Vina + PDBQT | Optional Ge-like MD (if READY) | Exact Ge stack by default |
| Status now | Published | Done (QC) | Protocol audited → **NOT READY** | Execute MD |

---

## 11. Hard stops (unchanged)

1. Do **not** reinterpret docking 0F–0J as function.  
2. **Zero** post-hoc tuning to force Qiu-14 agonist.  
3. **No** in silico pharmacological PASS / KILL / FAIL.  
4. **No calculation** until SI fidelity closes critical TBDs **and** explicit authorization.

---

## 12. Next ops (document only)

1. Obtain SI (`cn3c00580_si_001.pdf`, `cn3c00580_si_002.xlsx`) via institutional ACS access or browser session; place under `data/papers/ge_2023_acs_chem_neurosci/`.  
2. Extract Tables S1–S4 / S5–S7 + MD templates into repo (no invention).  
3. Re-run this audit → only then consider **READY** vs still **NOT READY**.  
4. Critical path remains CRO / H1-a RFQs — unaffected by 0N.

**Pointers:** gap analysis [`qiu_0n_reproducibility_gap_analysis.md`](qiu_0n_reproducibility_gap_analysis.md) · status [`qiu_0n_status.md`](qiu_0n_status.md)
