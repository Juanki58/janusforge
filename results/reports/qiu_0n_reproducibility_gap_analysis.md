# Qiu 0N — Ge et al. 2023 reproducibility gap analysis

> **Audit date:** 2026-08-12  
> **Companion:** [`qiu_0n_ge2023_benchmark_protocol.md`](qiu_0n_ge2023_benchmark_protocol.md)  
> **Governance (hard stops preserved):** [`qiu_0n_ge2023_reproduction_protocol.md`](qiu_0n_ge2023_reproduction_protocol.md)  
> **Execution:** **NONE** (no MD / docking / rescoring / LRIP). **No invented parameters.**

---

## Verdict

# **NOT READY**

| Class | Count |
|-------|------:|
| **VERIFICADO EN PUBLICACIÓN/SI** | **28** |
| **NO ESPECIFICADO** | **18** |
| **REQUIERE DECISIÓN** | **12** |

**READY** would require enough verified knobs to run an **auditable** Ge-style LRIP call on Qiu-14 without inventing critical inputs. SI signature tables and MD templates are missing → **NOT READY**.

---

## Top blockers for execution (ordered)

1. **SI numeric IP / signature tables (S1–S4, S7) inaccessible** — ACS Cloudflare 403; no OA mirror found. Cannot compute R/R² vs Ge’s published signatures without inventing vectors.  
2. **SI MD input templates + analysis scripts inaccessible** (`cn3c00580_si_001.pdf` Associated Content).  
3. **SI RMSD workbook inaccessible** (`cn3c00580_si_002.xlsx`).  
4. **Exact CB2 PDB / model for Ge active vs inactive arms not stated** in 2023 Methods (deferred to prior work) — structure fidelity TBD.  
5. **Engine mismatch:** Ge = AMBER18 + Lipid14 + GAFF + RESP; janusforge membrane precedent = OpenMM + lipid17 + GAFF2 — substitution **REQUIERE DECISIÓN**, must not be assumed equivalent.  
6. **GB/PB exact knobs + ΔE definition** incomplete in main text (Hawkins/Delphi named; igb/radii/grid/ε and which ΔE term for −10 kcal/mol gate unspecified).  
7. **No explicit GPU authorization** after fidelity — hard stop remains.

---

## Accessible vs blocked (this session)

| Source | Result |
|--------|--------|
| Europe PMC main PDF | **OK** → `data/papers/ge_2023_acs_chem_neurosci/cn3c00580_europepmc.pdf` |
| Text extract | **OK** → `.../cn3c00580_europepmc_extract.txt` |
| Unpaywall | **OK** (CC-BY hybrid; SI not OA-hosted) |
| ACS SI PDF/XLSX | **Blocked** (403 / Cloudflare) |
| NCBI PMC viewer | **Blocked** (reCAPTCHA/POW) |
| Figshare/other SI mirror | **Not found** |

See `data/papers/ge_2023_acs_chem_neurosci/ACCESS_LOG.md`.

---

## Critical TBD map (do not fill)

| ID | Gap | Blocks |
|----|-----|--------|
| TBD-0N-01 | Docking engine/grid/exhaustiveness | Pose provenance vs Ge |
| TBD-0N-02 | Exact active/inactive CB2 structures | System identity |
| TBD-0N-03 | Numeric mean IP signatures (S1–S4/S7) | **LRIP call** |
| TBD-0N-04 | MD/GBSA input templates (SI) | Protocol fidelity |
| TBD-0N-05 | GBSA igb/saltcon/dielectric/nonpolar | Energy reproducibility |
| TBD-0N-06 | Delphi/PB radii/grid/ε | PBSA-WSAS |
| TBD-0N-07 | Exact ΔE for −10 kcal/mol gate | Agonist criterion |
| TBD-0N-08 | Equilibration length inside 115 ns | Schedule fidelity |
| TBD-0N-09 | Replica / seed policy | Statistics |
| TBD-0N-10 | Full per-residue tables beyond highlights | Signature completeness |
| TBD-0N-11 | OpenMM/lipid17/GAFF2 vs AMBER18/Lipid14/GAFF | Stack choice |
| TBD-0N-12 | RESP vs Meeko/AM1-BCC for Qiu-14 | Charge fidelity |

---

## What we *can* do with current software (if later authorized)

| Capability | Status |
|------------|--------|
| Seed Qiu-14 CB2 pose from existing 0F MODEL 1 | Assets exist |
| Run *some* POPC membrane MD (OpenMM/lipid17/GAFF2) | Script + D2_22 precedent (CB1, 20 ns) — **not Ge-exact** |
| Aim for 115 ns duration as a setting | Feasible in principle; **not authorized** |
| Exact Ge AMBER18 + Lipid14 + RESP + Delphi WSAS | **Not demonstrated** in janusforge |
| LRIP vs published Ge SI signatures | **Blocked** until SI ingest |
| Emit CONSISTENT / INCONSISTENT / INCONCLUSIVE | Labels predefined; **no run** |

---

## Asset existence (Qiu-14 / CB2)

**Present:**  
`data/targets/cb2/6PT0_rec.pdbqt`, `data/targets/cb2/6PT0_rec.box.txt`, `data/targets/receptor_prep_summary.json`, `results/docking/qiu_0e/compound_14_lig.pdbqt`, `results/docking/qiu_0f/compound_14_cb2_out.pdbqt`, `scripts/run_md_openmm_membrane_lead.py`, `results/reports/md_d2_22_20ns_summary.md`

**Missing for Ge-faithful 0N:**  
SI PDF/XLSX contents; `6PT0_rec.pdb`; inactive-CB2 0N system; Ge MD templates; signature CSV/tables in repo.

---

## Relation to prior “READY / NOT EXECUTED (Gated)” wording

| Document | Meaning of READY |
|----------|------------------|
| `qiu_0n_ge2023_reproduction_protocol.md` (2026-08-12 lock) | Protocol/governance **written**; execution **gated** |
| **This gap analysis** | Auditable reproduction without inventing critical knobs |

These are **not contradictory** if distinguished: governance protocol exists; **execution readiness = NOT READY** until SI + critical TBDs close. Hard stops, H1-a arbiter, and labels (`consistente` / `no consistente` / `inconcluso`) remain locked.

---

## Blind controls & outcomes (summary)

- Blind locks: pose, signatures, thresholds, engine waiver, analysis freeze (§8 of benchmark protocol).  
- Outcomes only: **CONSISTENT WITH BENCHMARK** | **INCONSISTENT** | **INCONCLUSIVE** — never pharmacological PASS/KILL.  
- **H1-a** remains arbiter.

---

## Ge vs 0F/0G vs 0N (one-line)

**0F/0G** = docking geometry. **Ge** = membrane MD + LRIP function prediction validated by assay. **0N** would add a Ge-style *hypothesis* concordance label for Qiu-14 — it does **not** replace wet H1-a and is **NOT READY** to run.

---

## Required to flip to READY (checklist)

- [ ] SI PDF + XLSX obtained and filed under `data/papers/ge_2023_acs_chem_neurosci/`  
- [ ] Tables S1–S4/S7 (and needed S5/S6) extracted as auditable tables (no invention)  
- [ ] MD templates reviewed; TBD-0N-04/05/06/07 closed or explicitly waived in writing  
- [ ] TBD-0N-11/12 engine/charge path decided  
- [ ] Blind controls pre-registered  
- [ ] Separate explicit authorization to compute  

Until then: **NOT READY** · **115 ns MD + LRIP BLOCKED**.
