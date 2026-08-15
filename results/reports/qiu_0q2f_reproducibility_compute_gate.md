# 0Q.2f — €0 reproducibility audit & compute gate (Janus A / Vasiljevik)

**Date:** 2026-08-15  
**Branch:** `cursor/qiu-protocol-ip-cro-0p`  
**Purpose:** Squeeze **existing** project reports + already-cited primary sources into one gate: is there a **concrete, falsifiable computational question** that uses data/structures we already have and does **not** invent a Janus rule?  
**This is not a new lit review.** No new families. No NCE. No docking campaign. No MD.

**Authority chain (synthesize / verify only):**

| Report | Role |
|--------|------|
| `qiu_0q2c_dataset_audit.md` | Janus A census + assay facts |
| `qiu_0q2d_janus_a_sar_analysis.md` | Structures + cross-scaffold honesty |
| `qiu_0q2_vasiljevik_sar_audit.md` | V-19 identity correction + 19/27/30 matrix |
| `qiu_0q2b_cb1_cb2_structural_regions.md` | PDB inventory; Janus co-structures **NOT FOUND** |
| `qiu_0q1_primary_audit_A_pairs.md` | MRI / HU = **not Janus** (what **not** to compute) |

**Scope ligands:** URB447 · Qiu-14 · Vasiljevik-27 · Vasiljevik-30 (Janus **A**) + Vasiljevik-19 (same-series Janus **OFF** contrast).

---

## Gate verdict (mandatory)

| Question | Answer |
|----------|--------|
| Is there a concrete computational question that is **falsifiable**, uses **existing** structures/data, and does **not invent a Janus rule**? | **NO** |
| **INFORMÁTICA status** | **INFORMÁTICA = CERRADA** |
| Recommended return track | **0M / H1-a decision track** (`qiu_0m_h1a_wet_handoff.md`; Option A currently **RESERVE**) |

**If YES were true, this section would state:** question · required inputs · method class · success criterion · cost €0.  
**It is not true.** No such question survives the bans below.

---

## Why compute closes (logic, not preference)

A €0 compute step that stays honest must satisfy **all** of:

1. **Inputs already exist** (ligand identity + experimental co-structure or matched published poses — not docked guesses).  
2. **Falsifiable** without inventing a Janus SAR/mechanism rule.  
3. **Does not** treat mono-CB2 Class-A (MRI / HU) as Janus evidence.

Checklist against remaining options:

| Candidate compute | Why it fails the gate |
|-------------------|------------------------|
| Dock V-19 / V-27 / V-30 / URB447 / Qiu-14 into CB1/CB2 | Invents poses; invents Janus “explanation”; banned |
| MD of any Janus A or V-19 in receptor | Same; no co-structure seed |
| Pose comparison of **published** co-structures only (5TGZ, 5ZTY, 6PT0, 8GUS, …) | Already inventoried in 0Q.2b; **none bind Janus A / V-19**; comparing WIN/AM10257/HU-308 **cannot falsify** Janus of V-27/30 or Qiu-14 without a bridging rule |
| Overlay Qiu-14 2D on AM10257 (5ZTY) because both are pyrazole-3-carboxamides | AM10257 = **opposite** dual (CB1 ago + CB2 inv) — wrong phenotype; any Janus transfer = invented rule |
| Overlay Vasiljevik AAI on WIN (6PT0) | WIN = nonselective **agonist**; V-19 is dual ago (related) but V-27/30 Janus arms have **no** co-structure; cannot test CB1 ago→ant flip computationally without inventing pose→phenotype map |
| Re-run / extend Qiu SI docking (S173/S285) or MRI/HU Trp6.48 MD | Explicitly tagged **COMPUTATIONAL / not Janus evidence** in 0Q.2c–0Q.2b; mono-CB2 ≠ Janus |
| 2D Tanimoto / fragment counts among the five ligands | Already done as chemistry in 0Q.2d; not a receptor compute question; yields no new falsifiable Janus claim |

**What can be computed without inventing a rule:** only **non-predictive inventory** already completed (PDB lists, SMILES consolidation, assay tables). That work is **done**. Further informatics does not unlock a new falsifiable Janus question from current inputs.

---

## Consolidation table — five ligands

Identity for **V-19** follows `qiu_0q2_vasiljevik_sar_audit.md` (experimental body / NMR / HRMS): **(1-butyl-7-methoxy-1H-indol-3-yl)(naphthalen-1-yl)methanone** (7-OMe-JWH-073), **not** the duplicated 2,3-difluorophenyl ethanone heading (that ethanone is compound **37**).

| Field | **Vasiljevik-19** (OFF) | **Vasiljevik-27** (A) | **Vasiljevik-30** (A) | **URB447** (A) | **Qiu-14** (A) |
|-------|-------------------------|------------------------|------------------------|----------------|----------------|
| **1. Definitive structure** | IUPAC: (1-butyl-7-methoxy-1H-indol-3-yl)(naphthalen-1-yl)methanone. Scaffold: 7-OMe-N-butylindole + **C3 1-naphthoyl**. SMILES (from corrected IUPAC): `CCCCn1cc(C(=O)c2cccc3ccccc23)c2cccc(OC)c21` | IUPAC: 1-butyl-7-methoxy-3-(naphthalen-1-ylmethyl)-1H-indole. SMILES: `CCCCn1cc(Cc2cccc3ccccc23)c2cccc(OC)c21` | IUPAC: 1-butyl-7-methoxy-3-(naphthalen-2-yl)-1H-indole. SMILES: `CCCCn1cc(-c2ccc3ccccc3c2)c2cccc(OC)c21` | IUPAC: [4-amino-1-(4-chlorobenzyl)-2-methyl-5-phenyl-1H-pyrrol-3-yl](phenyl)methanone. SMILES: `CC1=C(C(=C(N1CC2=CC=C(C=C2)Cl)C3=CC=CC=C3)N)C(=O)C4=CC=CC=C4` (PubChem CID 25195055) | IUPAC (0D/SI): *N*-(adamantan-1-yl)-4-methyl-1-(2-morpholinophenyl)-5-phenyl-1*H*-pyrazole-3-carboxamide. SMILES: `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` |
| **2. CB1 / CB2 data** | CB1 Ki **1.7±0.3 nM** (mCB1); CB2 Ki **0.81±0.4 nM** (hCB2). Function: **dual agonist** | CB1 Ki **15.4±2.2 nM**; CB2 Ki **10.9±3.1 nM**. Function: CB1 **neutral ant** + CB2 **ago** | CB1 Ki **37.3±11.8 nM**; CB2 Ki **26.5±1.5 nM**. Function: CB1 **neutral ant** + CB2 **ago** | CB1 IC50 **313±72 nM** (rat cereb., [³H]WIN); CB2 IC50 **41±23 nM** (hCB2 CHO). Function: CB1 **neutral ant** + CB2 **ago** | Direction only OA: CB1 **antagonist**, CB2 **agonist** (cAMP). Numeric IC50/EC50/Emax: **NF OA** (main paywalled) |
| **3. Assay type** | Binding Ki ([³H]CP); AC inhibition screen + CRC (Neuro2A CB1 / CHO-hCB2) | Same + **ant of agonist 3** (Fig 3B); in vivo hypothermia block | Same as V-27 | Binding IC50; CB1 [³⁵S]GTPγS vs WIN; CB2 cAMP (isoproterenol) | SI cAMP (Fig S5A/B); ctrl CP55,940 / rimonabant |
| **4. Experimental conditions** | Same lab/paper V2013; AC @ **10 µM** screen; Ki selected set; species mix mCB1 / hCB2 | Identical platforms to V-19 within V2013; CHO-WT null for 27/30 | Identical to V-27 | LoVerme 2009: rat CB1 bind / hCB2 bind / mCB2 func HEK — same paper package | Qiu 2023 SI same-lab direction assays; potencies behind paywall |
| **5. Effect magnitude** | CB1 AC @10 µM **51%**; AC IC50 **~45 nM** (ago). CB2 AC @10 µM **52%** (ago). EC50/Emax CB2: **NR** | CB1 AC @10 µM **18%** (little CRC inhib.); antagonizes ago **3**. CB2 Table1 AC **33%**; Fig 4 narrative **~40–50%**. EC50/Emax: **NR** | CB1 AC @10 µM **16%**; ant of **3**. CB2 Table1 AC **21%**; Fig 4 ago-class. EC50/Emax: **NR** | CB1 GTPγS EC50 vs WIN **4.9±0.8 µM**; **no** basal GTPγS ↓. CB2: ↓ cAMP @ **1 µM**; EC50/Emax: **NF** | Magnitudes **NF OA** (direction closed only) |
| **6. Crystal / cryo-EM for ligand or close related** | **Ligand co-structure: NOT FOUND.** Closest chemotype in PDB: **WIN 55,212-2** in CB2–Gi **6PT0** (aminoalkylindole **agonist** — not Janus; not V-19). JWH-073 parent = tool ago in V2013, **no** receptor structure | **NOT FOUND** for 27. Same AAI family → only WIN/6PT0 as distant relative (wrong phenotype for CB1 ant arm) | **NOT FOUND** for 30. Same as V-27 | **NOT FOUND** for URB447. No close pyrrole–benzoyl co-structure cited in program inventory | **NOT FOUND** for Qiu-14. Scaffold-related: **AM10257** in CB2 **5ZTY** (pyrazole-3-carboxamide) = **opposite** dual — **not** usable as Janus template |
| **7. What can be computed without inventing a rule** | 2D identity vs 27/30 already locked; **no** pose→Janus test without docking invention | Phenotype vs 19 is **experimental** fact; compute cannot add falsifiable Janus locus without co-structures | Same as V-27 | Binding/func package complete enough as literature fact; no structural seed for €0 mechanism compute | Direction A; potencies blocked OA; docking claims in SI = **not** evidence — do not recompute |

**Janus grade reminder:** 19 = **D / OFF** (dual ago). 27, 30, URB447, Qiu-14 = **A** (Qiu-14 = direction A; potencies open).

---

## Closely related structures (already cited) — usable vs trap

| PDB / ligand | Why it looks tempting | Gate use for Janus A / V-19 |
|--------------|----------------------|-----------------------------|
| **6PT0** — WIN–CB2–Gi | AAI / indole chemotype near Vasiljevik | **Inventory only.** WIN is dual **agonist**-class tool. Pose comparison ≠ falsify V-27/30 CB1 antagonism |
| **5ZTY** — AM10257–CB2 | Pyrazole-3-carboxamide near Qiu | **Trap.** Opposite dual phenotype. Do **not** dock Qiu-14 into 5ZTY as Janus proof |
| **8GUS** — HU-308–CB2 | Active CB2 | **0Q.1 mono-CB2** parent. **Not Janus.** Do not compute Trp6.48 bulk for Yin-Yang |
| **5TGZ** — AM6538–CB1 inactive | Inactive CB1 pocket | No Janus ligand bound. Xing docking of GW405833 here = **COMP** only (and GW is grade **B**, out of A set) |
| MRI2687 / MRI2594 / (R)-1 | Strong mono-CB2 ago↔inv pairs | **What not to compute for Janus** — Class A for **mono-CB2**, explicitly **not** Yin-Yang (0Q.1) |

---

## What not to compute (0Q.1 relevance)

| Topic | Status for **this** gate |
|-------|---------------------------|
| MRI2687 ↔ MRI2594 Trp6.48 docking/MD | Excellent **mono-CB2** story; **banned** as Janus compute seed |
| HU-308 / ago-3 → (R)-1 phenyl | Same — CB2 efficacy flip; **no** CB1 ant switch shown |
| Promoting Trp6.48 as “Janus structural switch” | **REJECT** (locked 0Q.2b) |
| Filling Qiu-15/16/20/24 pharmacology via docking | **Banned**; OA phenotype NF |

---

## Explicit compute-gate form

### Concrete computational question?

**NO.**

### If YES (template — not applicable)

- **Question:** —  
- **Required inputs:** —  
- **Method class:** —  
- **Success criterion:** —  
- **Cost:** €0  

### If NO (applicable)

**INFORMÁTICA = CERRADA**

Further docking, MD, pose invention, or cross-scaffold pharmacophore modeling on Janus A / Vasiljevik **does not** meet the reproducibility gate with current inputs.

**Recommend:** return to **0M / H1-a decision track** — wet/ops path for Qiu-14 CB2-first (`results/reports/qiu_0m_h1a_wet_handoff.md`), currently **`0M = RESERVE`**, with SMRF literature work having extracted what OA primary sources allow. Do **not** spend compute budget inventing a Janus structural rule.

---

## Locks carried forward

| Lock | Value |
|------|-------|
| Janus A count | **4** (URB447, Qiu-14, V-27, V-30) |
| Best same-series OFF contrast | **V-19** (dual ago; naphthoyl identity corrected) |
| STRONG Janus structural ON/OFF pair | **0** |
| Janus ligand co-structures | **NOT FOUND** |
| €0 compute that falsifies/proves Janus mechanism without inventing a rule | **NONE** |
| INFORMÁTICA | **CERRADA** |

---

## Paths

| File | Path |
|------|------|
| This gate | `results/reports/qiu_0q2f_reproducibility_compute_gate.md` |
| Parents | `qiu_0q2c_dataset_audit.md`, `qiu_0q2d_janus_a_sar_analysis.md`, `qiu_0q2_vasiljevik_sar_audit.md`, `qiu_0q2b_cb1_cb2_structural_regions.md`, `qiu_0q1_primary_audit_A_pairs.md` |
| Decision return | `qiu_0m_h1a_wet_handoff.md` |

---

*End 0Q.2f. Squeeze complete; computing ends.*
