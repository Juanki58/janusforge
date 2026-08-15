# 0Q.2c — Primary-source audit of Janus ligand dataset (no new compounds)

**Date:** 2026-08-15  
**Branch:** `cursor/qiu-protocol-ip-cro-0p`  
**Audited files:** `qiu_0q2c_janus_ligand_dataset.md`, `qiu_0q2c_janus_ligand_dataset.csv`  
**Scope:** Re-verify all **28** listed compounds against primary literature. **No new compounds.** No docking/MD/predictions/reviews used to promote Janus. Discrepancies marked, not silently corrected.

**Janus definition used for grades:** experimental **CB2 agonist** + experimental **CB1 antagonist or inverse agonist** (functional). Binding dual affinity alone ≠ Janus.

| Grade | Meaning |
|-------|---------|
| **A** | Functionally demonstrated on **both** receptors (Janus phenotype) |
| **B** | Partial evidence (one arm incomplete, pathway-ambiguous, or multi-lab recombination with conflict) |
| **C** | Inferred (author claim / narrative without OA-verifiable dual function) |
| **D** | Not demonstrated as Janus (OFF, opposite, mono, binding-only, or assay ANCHOR) |

**Access legend:** OA = open full text used this session; PARTIAL = SI/abstract/mirror only; PAYWALL = main tables not recovered.

---

## ACCESS summary (primary sources this session)

| Source | DOI / PMC | Access |
|--------|-----------|--------|
| LoVerme/Piomelli URB447 *BMCL* 2009 | 10.1016/j.bmcl.2008.12.059; PMC3690177; eScholarship OA PDF | **OA** |
| Vasiljevik *JMC* 2013 | 10.1021/jm400268b; PMC3904296; KU ScholarWorks PDF | **OA** |
| Dhopeshwarkar *JPET* 2017 (GW405833/AM1710 Janus) | 10.1124/jpet.116.236539 | **OA** (JPET HTML) |
| Valenzano *Neuropharmacol* 2005 (GW binding) | 10.1016/j.neuropharm.2004.12.008 | Cited in JPET; **PAYWALL** primary PDF not opened |
| Khanolkar *JMC* 2007 (AM1710/AM1714) | 10.1021/jm070441u | Abstract/secondary citations; **PAYWALL** full tables |
| Qiu *Bioorg. Chem.* 2023 + SI mmc1 | 10.1016/j.bioorg.2023.106377 | Main **PAYWALL**; SI local extract **OA** (Scheme S1, Fig S5/S11–S13 legends) |
| Li/Hua *Cell* 2019 | 10.1016/j.cell.2018.12.011 | **PARTIAL** (prior 0Q.1 mirror + EuropePMC); PMC reCAPTCHA |
| Kosar *ACS Cent. Sci.* 2024 | 10.1021/acscentsci.3c01461; PMC11117691 | **OA** |
| Ross *Br J Pharmacol* 1999 | 10.1038/sj.bjp.0702351; PMC1565857 | **OA** |
| Rinaldi-Carmona *JPET* 1998 / *FEBS Lett* 1994 | SR144528 / SR141716A discovery | Cited; discovery Ki for SR144 used as historical |

---

## Per-compound audit (28)

### JAN-1 — URB447 (8b)

| Field | Finding |
|-------|---------|
| **1. Primary** | LoVerme et al., *Bioorg. Med. Chem. Lett.* **19**, 639–643 (2009). DOI 10.1016/j.bmcl.2008.12.059. |
| **2. Identity** | **YES** — IUPAC in abstract; synthesis Scheme 2; NMR/MS/anal. in notes. SMILES not printed. |
| **3. Binding vs function** | **Separated.** Binding Table 1; CB1 GTPγS text; CB2 cAMP text. |
| **4. CB1** | Binding: [³H]WIN, **rat cerebellum**, IC50 **313±72 nM** (Table 1). Function: GTPγS vs WIN 1 µM, EC50 **4.9±0.8 µM**; **no** basal GTPγS ↓ → **neutral antagonist**. |
| **4. CB2** | Binding: **hCB2 CHO-K1**, IC50 **41±23 nM** (Table 1). Function: **mCB2 HEK-293**, ↓ isoproterenol-cAMP @ **1 µM** (pmol/well quoted) → **agonist**. EC50/Emax: **NOT FOUND**. |
| **5. Comparability** | **HIGH** (same paper; dual func). Species mix rat CB1 / hCB2 binding / mCB2 func — note but still same lab package. |
| **6. JANUS** | **A** |
| **7. Where** | Table 1; GTPγS/cAMP paragraphs; conclusion “first mixed CB1 antagonist/CB2 agonist”. |
| **Discrepancy vs dataset** | None material. Dataset correct. |

### JAN-2 — GW405833

| Field | Finding |
|-------|---------|
| **1. Primary (Janus claim)** | Dhopeshwarkar et al., *JPET* **360**, 300–311 (2017). DOI 10.1124/jpet.116.236539. Binding Ki: Valenzano 2005. |
| **2. Identity** | **YES** — IUPAC in JPET; commercial (Tocris). |
| **3. Binding vs function** | Binding from Valenzano; CB1 **function** in JPET; CB2 **function not re-measured** in Janus paper. |
| **4. CB1** | Binding Ki **4772±1676 nM** (Valenzano, cited). Function JPET: DSE IC50 **2.6 µM**; noncompetitive ant of CP55,940 (AC/ERK/PIP2/internalization); arrestin **time-dependent / ambiguous**. Activity: **noncompetitive antagonist** (not clean neutral). |
| **4. CB2** | Binding Ki **3.92±1.58 nM** hCB2 (Valenzano). Historical “CB2 agonist”; **Yao 2008 / Mancini 2009 protean/inverse caveats** cited in related JPET 2017 pain paper. **No new CB2 ago CRC in Janus JPET.** |
| **5. Comparability** | **MEDIUM → LOW** for true Janus package (CB1 Mackie lab 2017 vs CB2 historical multi-lab). |
| **6. JANUS** | **B** (CB1 ant **A-quality**; CB2 ago arm **not closed in Janus primary** + protean conflict) |
| **7. Where** | JPET Figs 1–4, Table 1 Schild; Valenzano Ki cited in intro. |
| **Discrepancy** | Dataset lists as Janus **ON**. **Overstated** relative to A-grade definition. |

### JAN-3 — AM1710

| Field | Finding |
|-------|---------|
| **1. Primary** | Binding/identity: Khanolkar *JMC* 2007 (10.1021/jm070441u). CB1 Janus func: Dhopeshwarkar *JPET* 2017. CB2 cAMP EC50/Emax: **Dhopeshwarkar & Mackie 2016** (cited in JPET 2017), **not** Khanolkar alone. |
| **2. Identity** | **YES** — IUPAC in JPET; cannabilactone 4b / AM1710. |
| **3. Binding vs function** | Separated across papers. |
| **4. CB1** | Ki rat synaptosomal **360 nM** (95% CI 330–390) Khanolkar. JPET: low-potency **competitive ant/inv** in multiple pathways; DSE attenuates (no IC50); arrestin = **low-efficacy agonist**. Pathway-**non-uniform**. |
| **4. CB2** | Ki hCB2 **6.7 nM** (Khanolkar). cAMP EC50 **11 nM**, Emax **48%** → **partial agonist** (2016 cite in JPET). |
| **5. Comparability** | **MEDIUM** (multi-paper assembly). |
| **6. JANUS** | **B** (dual arms exist experimentally, but CB1 not pathway-uniform antagonist; CB2 potency not from same Janus paper) |
| **7. Where** | Khanolkar binding; JPET CB1 panels; 2016 cAMP cited in JPET intro. |
| **Discrepancy** | Dataset attributes CB2 EC50 as if part of JPET/Khanolkar package without clear 2016 split; calls ON — **overstated vs A**. |

### JAN-4 — Qiu-14

| Field | Finding |
|-------|---------|
| **1. Primary** | Qiu et al., *Bioorg. Chem.* 2023. DOI 10.1016/j.bioorg.2023.106377 + SI mmc1. |
| **2. Identity** | **YES** — SI Scheme S1 / OCR: N1-phenyl **ortho-morpholinyl**, C3-amide **1-adamantyl**. SMILES not in SI text extract. |
| **3. Binding vs function** | SI functional cAMP only for phenotype; main binding tables **PAYWALL**. |
| **4. CB1** | SI Fig **S5B**: cAMP **antagonist** (ctrl rimonabant). IC50/Emax: **NOT FOUND OA**. |
| **4. CB2** | SI Fig **S5A**: cAMP **agonist** (ctrl CP55,940). EC50/Emax: **NOT FOUND OA**. |
| **5. Comparability** | **HIGH** for direction (same SI assays). |
| **6. JANUS** | **A** (direction functionally shown) — **quantitative potencies open gap** |
| **7. Where** | Fig S5 legend: “agonist for CB2 (A) and as antagonist for CB1 (B)”. S173/S285 = **COMPUTATIONAL** (docking/MD) — not used for grade. |
| **Discrepancy** | Dataset ON matches direction; correctly flags potencies NF. |

### JAN-5 — Vasiljevik-27

| Field | Finding |
|-------|---------|
| **1. Primary** | Vasiljevik et al., *J. Med. Chem.* **56**, 4537–4550 (2013). DOI 10.1021/jm400268b. PMC3904296. |
| **2. Identity** | **YES** — IUPAC: 1-butyl-7-methoxy-3-(naphthalen-1-ylmethyl)-1H-indole; synthesis + NMR. |
| **3. Binding vs function** | Separated (Tables 1–2; Figs 3–4). |
| **4. CB1** | Ki **mCB1** **15.4±2.2 nM** (Table 2). AC screen @10 µM: **18%** (Table 1). Fig 3A little AC inhibition; Fig **3B** **antagonizes** AC inhibition by agonist **3**; in vivo blocks 3-hypothermia (Fig 5). → **neutral antagonist**. |
| **4. CB2** | Ki **hCB2** **10.9±3.1 nM**. Table 1 AC @10 µM: **33%**; Fig 4 CRC text: **40–50%** AC inhibition → **agonist** (partial–full class). Emax vs CP: not a single labeled Emax %. |
| **5. Comparability** | **HIGH** |
| **6. JANUS** | **A** |
| **7. Where** | Tables 1–2; Figs 3–4; abstract. |
| **Discrepancy** | Dataset “~40–50%” matches **Fig 4 text**, not Table 1 screen (33%). Marked. |

### JAN-6 — Vasiljevik-30

| Field | Finding |
|-------|---------|
| **1. Primary** | Same as JAN-5. |
| **2. Identity** | **YES** — 1-butyl-7-methoxy-3-(naphthalen-2-yl)-1H-indole. |
| **3. Binding vs function** | Separated. |
| **4. CB1** | Ki **37.3±11.8 nM** (Table 2). AC screen **16%**. Ant of agonist 3 (Fig 3B); hypothermia block (Fig 5). → **neutral antagonist**. |
| **4. CB2** | Ki **26.5±1.5 nM**. Table 1 AC @10 µM: **21%**; Fig 4 text claims 40–50% class with other leads. → **agonist** (author). |
| **5. Comparability** | **HIGH** |
| **6. JANUS** | **A** |
| **7. Where** | Tables 1–2; Figs 3–4. |
| **Discrepancy** | Dataset Ki **37.2** vs primary **37.3±11.8**. Table 1 CB2 AC **21%** vs dataset “ago-class / 40–50%” (Fig 4 narrative). **Marked.** |

### N-URB-5b — 5b

| Field | Finding |
|-------|---------|
| **1. Primary** | LoVerme 2009 Table 1. |
| **2. Identity** | **YES** — (4-amino-2-methyl-5-phenylpyrrol-3-yl)(phenyl)methanone; N1-H precursor. |
| **3–4.** | Binding only: CB1 & CB2 IC50 **>1000 nM**. Function: **NOT FOUND**. |
| **5.** | **HIGH** vs URB447 binding. |
| **6. JANUS** | **D** |
| **Discrepancy** | None. |

### N-URB-8a — 8a

| Field | Finding |
|-------|---------|
| **1. Primary** | LoVerme 2009 Table 1. |
| **2. Identity** | **YES** — 3-benzoyl without 4-NH₂ (Scheme 2). |
| **3–4.** | CB1 IC50 **>1000**; CB2 **498±32 nM**. Function: **NOT FOUND**. |
| **6. JANUS** | **D** |

### N-URB-3c — 3c

| Field | Finding |
|-------|---------|
| **1. Primary** | LoVerme 2009 Table 1. |
| **2. Identity** | **YES** — NH-2-adamantyl amide pyrrole. |
| **3–4.** | CB1 IC50 **70±10**; CB2 **11±4 nM**. Dual **binding** only. Function: **NOT FOUND**. |
| **6. JANUS** | **D** (dual affinity ≠ Janus) |

### N-Q15 / N-Q16 / N-Q20 / N-Q24 — Qiu-15, 16, 20, 24

| Field | Finding |
|-------|---------|
| **1. Primary** | Qiu 2023 SI Scheme S1 (identity); pharmacology main/S11–S13 **figures exist** but **numeric OA extraction NOT FOUND**. |
| **2. Identity** | **YES** (regio/R-group defined in SI OCR): 15 meta-morpholinyl; 16 para-morpholinyl; 20 o-4-methylpiperazinyl; 24 o-morpholinyl + C3 CH₂-1-adamantyl. |
| **3–4.** | Phenotype/potency OA: **NOT FOUND**. Author Yin-Yang loss for non-ortho = **INFERRED** until paywalled tables audited. |
| **5.** | Identity HIGH; pharmacology **UNKNOWN**. |
| **6. JANUS** | **D** (not OA-demonstrated); author narrative alone would be **C** — **not promoted here**. |
| **Discrepancy** | Dataset UNKNOWN is appropriate; do not upgrade via docking Fig S6. |

### N-V19 — Vasiljevik-19

| Field | Finding |
|-------|---------|
| **1. Primary** | Vasiljevik 2013. |
| **2. Identity** | **YES** — 1-(1-butyl-7-methoxy-1H-indol-3-yl)-2-(2,3-difluorophenyl)ethanone. |
| **4. CB1** | Ki **1.7±0.3 nM**; AC **51%** @10 µM; AC IC50 **~45 nM** → **agonist**. |
| **4. CB2** | Ki **0.81±0.4 nM**; AC **52%** → **agonist**. |
| **5.** | **HIGH** |
| **6. JANUS** | **D** (dual ago = OFF) |

### N-V35 — Vasiljevik-35

| Field | Finding |
|-------|---------|
| **1. Primary** | Vasiljevik 2013 Table 1. |
| **2. Identity** | **YES** — 1-butyl-7-methoxy-3-(naphthalen-1-yl)-1H-indole. |
| **4.** | AC screen CB1 **39%**, CB2 **37%** @10 µM. Ki: **NOT FOUND**. Ant-of-agonist: **NOT FOUND**. |
| **6. JANUS** | **B** (PARTIAL screen only) |

### N-V17 — Vasiljevik-17

| Field | Finding |
|-------|---------|
| **1. Primary** | Vasiljevik 2013. |
| **2. Identity** | **YES** |
| **4. CB1** | Ki **387±77**; AC **−4%**. CB2 Ki **281±51**; AC **22%**. |
| **6. JANUS** | **D** |

### N-AM1714 — AM1714

| Field | Finding |
|-------|---------|
| **1. Primary** | Khanolkar 2007 (9-OH cannabilactone vs AM1710 9-OMe). |
| **2. Identity** | **YES** within series (analog 5). |
| **4.** | CB2 selective agonist-class (author); CB1 ant panel matching JPET: **NOT FOUND**. |
| **6. JANUS** | **B** / insufficient → treat as **B** (PARTIAL) |

### X-MRI2687 / X-MRI2594

| Field | Finding |
|-------|---------|
| **1. Primary** | Li/Hua et al., *Cell* **176**, 459–467.e13 (2019). DOI 10.1016/j.cell.2018.12.011. |
| **2. Identity** | **YES** — IUPAC + HRMS in STAR Methods (0Q.1 audit). SMILES NF. |
| **4. MRI2687** | β-arrestin2: CB1 partial ago EC50 **114±15 nM**, Emax **6.0±0.3** fold; CB2 **inverse** EC50 **0.24±0.06 nM**, Emax **0.75±0.04**. |
| **4. MRI2594** | CB1 ago **310±54 nM**, Emax **28±2**; CB2 ago **0.17±0.03 nM**, Emax **2.0±0.2**. |
| **5.** | **HIGH** within Fig 6. |
| **6. JANUS** | **D** (NOT Yin-Yang; CB2 ago↔inv only) |

### X-HU308 / X-R1 / X-ago3

| Field | Finding |
|-------|---------|
| **1. Primary** | Kosar et al., *ACS Cent. Sci.* 2024. DOI 10.1021/acscentsci.3c01461. HU-308 cryo-EM: Li *Nat Commun* 2023 (8GUS). |
| **2. Identity** | **YES** for (R)-1 / ago-3 in Kosar schemes; HU-308 classical. |
| **4. HU-308** | CB2 **agonist**; CB1 Janus ant switch: **NOT FOUND**. |
| **4. (R)-1** | CB2 cAMP pEC50 **6.95**, Emax **−44%** → **inverse agonist**; Kd **39.1 nM**. CB1 ant: **NOT FOUND**. |
| **4. ago-3** | CB2 pEC50 **8.47**, Emax **+112%** → **agonist**. |
| **6. JANUS** | **D** (mono-CB2 flip) |

### X-AM10257

| Field | Finding |
|-------|---------|
| **1. Primary** | Li/Hua *Cell* 2019 (crystal ligand context + β-arrestin2). |
| **2. Identity** | **YES** — IUPAC; PDB 5ZTY. |
| **4.** | CB2 inv/ant (Ki **0.08 nM**; barr2 EC50 **0.20±0.04**, Emax **0.70±0.05**); CB1 **agonist** (author opposite dual). |
| **6. JANUS** | **D** (**opposite** dual) |

### A-CP — CP55,940

| Field | Finding |
|-------|---------|
| **1. Primary** | Ross *Br J Pharmacol* 1999 Table 1 (panel values used in dataset). |
| **2. Identity** | **YES** (tool). |
| **4.** | Ki hCB1 **5.0±0.8 nM**; hCB2 **1.8±0.2 nM**; **agonist**. |
| **6. JANUS** | **D** (ANCHOR) |

### A-WIN — WIN55,212-2

| Field | Finding |
|-------|---------|
| **1. Primary** | Ross 1999 methods/tool use; URB447 GTPγS agonist; cryo-EM CB2–WIN Xing *Cell* 2020. |
| **4.** | Nonselective **agonist** (tool). Exact panel Ki not required for ANCHOR role. |
| **6. JANUS** | **D** (ANCHOR) |

### A-SR144 — SR144528

| Field | Finding |
|-------|---------|
| **1. Primary** | Discovery: Rinaldi-Carmona *JPET* 1998; Ross 1999 Table 1 panel. |
| **4.** | Ross: Ki CB1 **>10 µM**; CB2 **5.6±1.1 nM**. Discovery Ki **0.6 nM** spleen/hCB2 — **do not merge across labs**. Ant/inv at CB2. |
| **6. JANUS** | **D** (ANCHOR) |
| **Discrepancy** | Dataset correctly warns not to merge Ki. |

### A-AM630 — AM630

| Field | Finding |
|-------|---------|
| **1. Primary** | Ross 1999. |
| **4.** | Ki CB1 **5152±567**; CB2 **31.2±12.4 nM**. CB2 GTPγS inv EC50 **76.6 nM**; CB1 weak **partial agonist** @ µM cAMP. |
| **6. JANUS** | **D** (ANCHOR) |

### A-RIM — SR141716A (rimonabant)

| Field | Finding |
|-------|---------|
| **1. Primary** | Rinaldi-Carmona *FEBS Lett* 1994; Ki cited in LoVerme footnote (**1.98±0.36 nM** CB1); CB2 IC50 **>1000 nM** (LoVerme Table 1 footnote). |
| **4.** | CB1 **inverse antagonist**; CB2 inactive/weak. |
| **6. JANUS** | **D** (ANCHOR) |

---

## Discrepancy register (dataset vs primary; not silently corrected)

| # | Item | Dataset says | Primary audit |
|---|------|--------------|---------------|
| 1 | Janus ON count | 6 ON | Strict **A = 4** (URB447, Qiu-14, V-27, V-30). GW405833 & AM1710 → **B** |
| 2 | V-30 Ki | 37.2 nM | **37.3±11.8 nM** (Table 2) |
| 3 | V-27/30 CB2 AC | ~40–50% | Table 1 screen **33% / 21%**; 40–50% is **Fig 4 CRC narrative** |
| 4 | GW405833 Janus | ON | CB2 ago not demonstrated in Janus JPET; protean conflict → **B** |
| 5 | AM1710 CB2 EC50 source | bundled with JMC/JPET | EC50 **11 nM / Emax 48%** from **2016** cite inside JPET 2017 |
| 6 | Qiu-15/16/20/24 | UNKNOWN | Correct; SI pharmacology figures exist but **numbers NF OA** — do not treat as Janus |
| 7 | Computational claims | Noted | Confirm: Qiu S173/S285, MRI Trp docking/MD, Kosar Trp docking = **not** Janus evidence |

---

## Full summary table of 28

| ID | Name | Identity | CB1 (bind / func) | CB2 (bind / func) | Comp. | JANUS | Dataset status | Audit note |
|----|------|----------|-------------------|-------------------|-------|-------|----------------|------------|
| JAN-1 | URB447 | YES | IC50 313; GTPγS neut ant | IC50 41; cAMP ago | HIGH | **A** | ON | Keep A |
| JAN-2 | GW405833 | YES | Ki 4772; noncomp ant (JPET) | Ki 3.92; ago **historical/protean** | MED/LOW | **B** | ON | **Downgrade** |
| JAN-3 | AM1710 | YES | Ki 360; ant/inv + arrestin ago | Ki 6.7; cAMP part ago | MED | **B** | ON | **Downgrade** |
| JAN-4 | Qiu-14 | YES | cAMP ant (S5B); pot NF | cAMP ago (S5A); pot NF | HIGH | **A** | ON | Direction A |
| JAN-5 | V-27 | YES | Ki 15.4; neut ant + ant-of-3 | Ki 10.9; AC ago | HIGH | **A** | ON | Keep A |
| JAN-6 | V-30 | YES | Ki 37.3; neut ant | Ki 26.5; AC ago | HIGH | **A** | ON | Ki typo 37.2 |
| N-URB-5b | 5b | YES | IC50 >1000 / NF | IC50 >1000 / NF | HIGH | **D** | OFF | OK |
| N-URB-8a | 8a | YES | >1000 / NF | 498 / NF | HIGH | **D** | OFF | OK |
| N-URB-3c | 3c | YES | 70 / NF | 11 / NF | HIGH | **D** | OFF | OK |
| N-Q15 | Qiu-15 | YES | NF OA | NF OA | UNK | **D** | UNKNOWN | Not C unless author-inferred |
| N-Q16 | Qiu-16 | YES | NF OA | NF OA | UNK | **D** | UNKNOWN | same |
| N-Q20 | Qiu-20 | YES | NF OA | NF OA | UNK | **D** | UNKNOWN | same |
| N-Q24 | Qiu-24 | YES | NF OA | NF OA | UNK | **D** | UNKNOWN | same |
| N-V19 | V-19 | YES | dual ago | dual ago | HIGH | **D** | OFF | OK |
| N-V35 | V-35 | YES | AC screen only | AC screen only | HIGH screen | **B** | PARTIAL | OK |
| N-V17 | V-17 | YES | weak/null | weak ago | HIGH | **D** | OFF | OK |
| N-AM1714 | AM1714 | YES | CB1 ant NF | ago-class bind | LOW | **B** | PARTIAL | OK |
| X-MRI2687 | MRI2687 | YES | CB1 part ago | CB2 inv | HIGH | **D** | OFF | OK |
| X-MRI2594 | MRI2594 | YES | CB1 ago | CB2 ago | HIGH | **D** | OFF | OK |
| X-HU308 | HU-308 | YES | not Janus ant | ago | MED | **D** | OFF | OK |
| X-R1 | (R)-1 | YES | CB1 ant NF | CB2 inv | HIGH CB2 | **D** | OFF | OK |
| X-ago3 | ago-3 | YES | NF focus | CB2 ago | HIGH | **D** | OFF | OK |
| X-AM10257 | AM10257 | YES | CB1 ago | CB2 inv | HIGH | **D** | OFF opposite | OK |
| A-CP | CP55,940 | YES | ago | ago | HIGH | **D** | ANCHOR | OK |
| A-WIN | WIN55,212-2 | YES | ago | ago | HIGH | **D** | ANCHOR | OK |
| A-SR144 | SR144528 | YES | low CB1 | CB2 ant/inv | HIGH within paper | **D** | ANCHOR | OK |
| A-AM630 | AM630 | YES | weak part ago | CB2 inv | HIGH | **D** | ANCHOR | OK |
| A-RIM | SR141716A | YES | CB1 inv/ant | inactive | HIGH as ctrl | **D** | ANCHOR | OK |

---

## Truly Janus **A**

1. **URB447**  
2. **Qiu-14** (direction only; potencies still paywalled)  
3. **Vasiljevik-27**  
4. **Vasiljevik-30**  

**n Janus A = 4** (dataset claimed 6 ON).

---

## Which drop to B / C / D

| From dataset | Audit grade | Reason |
|--------------|-------------|--------|
| GW405833 (was ON) | **B** | CB1 ant solid; CB2 ago not closed in Janus primary + protean conflict |
| AM1710 (was ON) | **B** | Multi-paper; CB1 pathway-non-uniform |
| V-35, AM1714 (PARTIAL) | **B** | Unchanged |
| Qiu-15/16/20/24 (UNKNOWN) | **D** (not C) | Pharmacology not OA-demonstrated; author Yin-Yang = inference only if forced |
| All OFF / opposite / anchors | **D** | Unchanged |
| None promoted to A via docking/MD | — | Ban respected |

---

## Real SAR pairs (Janus-relevant)

| Pair | Real? | Notes |
|------|-------|-------|
| **V-19 ↔ V-27 / V-30** | **YES (usable)** | Same-lab dual-func: dual-ago vs Janus. Edit multi-site (not single-atom). |
| **V-35 ↔ V-27** | **PARTIAL** | Minimal CH₂ insert; 35 lacks Ki + ant panel. |
| **V-35 ↔ V-30** | **PARTIAL** | 1- vs 2-naphthyl; same missing ant on 35. |
| **5b ↔ URB447** | **PARTIAL** | Binding emergence only; 5b func NF. |
| **8a / 3c ↔ URB447** | **PARTIAL (weak)** | Binding only; 3c dual binder ≠ Janus. |
| **Qiu-14 ↔ 15/16/20/24** | **PARTIAL (blocked)** | Structures defined; comparator pharmacology OA NF. |
| MRI2687 ↔ MRI2594 | **NO for Janus** | Excellent CB2 ago↔inv; wrong phenotype. |
| ago-3 ↔ (R)-1 | **NO for Janus** | Mono-CB2 flip. |
| AM1714 ↔ AM1710 | **NO for Janus** | CB1 ant NF on 1714. |

---

## Structural mods defined enough for ON/OFF study

| Mod | Defined? | ON/OFF readiness |
|-----|----------|------------------|
| V-35 → V-27 (+CH₂ at C3-naphthyl) | **YES** | Best minimal Janus ON/OFF candidate; needs ant panel on 35 |
| V-19 → V-27/30 (ketone–aryl rewrite) | **YES** | Multi-mod; usable narrative, not atom-rule |
| URB 5b → 447 (N1-p-Cl-benzyl) | **YES** | Binding ON emergence; func OFF side missing |
| Qiu ortho vs meta/para morpholine; piperazine; CH₂-Ad | **YES** | Identity closed; OA pharmacology incomplete |
| MRI arm-1 thiazole↔benzothiazole | **YES** | Defined but **not Janus ON/OFF** |
| HU-308 ± C(2′) phenyl | **YES** | Defined but **not Janus ON/OFF** |

---

## Final verdict

### **REVISE**

The 28-compound inventory is a useful primary-anchored collection (no invented potencies; OFF/ANCHOR controls largely correct), but it **overstates Janus ON** (6 → **4 true A**), conflates **GW405833/AM1710** as clean dual Janus, and carries small numeric/citation slips (V-30 Ki 37.2 vs 37.3; CB2 AC screen vs CRC; AM1710 EC50 source year). Keep the set; revise grades/notes before using as Janus SAR truth set. **Do not REJECT** (core A compounds and SAR scaffolding are real). **Do not KEEP as-is.**

---

## Paths

| File | Path |
|------|------|
| This audit | `results/reports/qiu_0q2c_dataset_audit.md` |
| Audited dataset (unchanged this step) | `results/reports/qiu_0q2c_janus_ligand_dataset.md` |
| CSV | `results/reports/qiu_0q2c_janus_ligand_dataset.csv` |
