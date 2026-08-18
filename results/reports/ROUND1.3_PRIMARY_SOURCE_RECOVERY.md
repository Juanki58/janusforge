# ROUND1.3 — PRIMARY DOCUMENTARY RECOVERY

**Date:** 2026-08-16  
**Phase:** Round 1.3 — primary documentary recovery (create-only)  
**Start from (read-only):** `ROUND1_RECONCILIATION_v1.0.md` (+ related Round1 reports / CSV as context)  
**Output path:** `results/reports/ROUND1.3_PRIMARY_SOURCE_RECOVERY.md`  
**Integrity:** NO dataset expansion; NO models/docking/MD/ROC/design; NO Gold modify; NO Round1 CSV / prior-report overwrite; NO git commit/PR.  
**Rule:** Prefer **REVIEW_REQUIRED** / **NOT_VERIFIED** over false CONFIRMED. Do **not** declare definitive Gold in Round 1.3.

**Statuses used:** `CONFIRMED` | `REVIEW_REQUIRED` | `REJECTED` | `NOT_VERIFIED`

---

## 1. AM1710 forensic reconciliation

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | Adversarial / inherited: `AM1710 = compound 5a = EC50 11.2 nM = [³⁵S]GTPγS` (Emax ~89±3% vs CP). Round1 also carries binding Ki 6.7 / 360 (Khanolkar lineage) and functional “11 nM” (quarantine Q-05). Citation often given as Khanolkar *J Med Chem* **50:4496–4506** — **wrong page range**. |
| 2 | Primary source found | **Khanolkar et al. 2007** full PDF / tables: **NOT recovered** (ACS paywalled; EuropePMC `HAS_FT=0`; ACS SI HTTP 403). PubMed/EuropePMC **abstract** recovered (DIRECT for compound numbering only). **Dhopeshwarkar & Mackie 2016** PMC4959096 Table 2 + Methods recovered (DIRECT for ~11 nM cyclase). Unpaywall “OA” DOI `10.7270/q2736qn9` resolves to **BindingDB curated Ki**, not Khanolkar PDF → **secondary; not accepted as primary**. |
| 3 | DOI/identifier | Khanolkar: **10.1021/jm070441u**, PMID **18038967**, *J Med Chem* **50:6493–6500** (not 4496–4506). Dhop: **10.1124/jpet.116.232561**, PMC**4959096**. |
| 4 | Page + table/figure + row | Khanolkar GTPγS / Table 2 / compound 5a: **NOT_FOUND** in opened primaries. Abstract identity: AM1710 = **4b**; compound **5** = **AM1714**. Dhop Table 2 row **AM1710**, cyclase columns (PMC HTML `#T2`). |
| 5 | EC50/other metric exactly as appears | **Abstract:** no numeric GTPγS EC50. **Dhop Table 2 cyclase:** EC50 **11** nM (95% CI **5.5–15.6**) — **not** 11.2. Arrestin (separate): EC50 **4** (CI 1.6–7.1). BindingDB secondary Ki **6.7 nM** (mouse spleen) — **INFERRED/secondary only**. |
| 6 | Emax exactly as appears | Dhop cyclase Emax **48 ± 4.3**; arrestin Emax **91 ± 3.6**. Adversarial **89±3%** **NOT_FOUND**. |
| 7 | Species | Dhop Methods: **mouse** CB2 (mCB2). Abstract Khanolkar: agonists claimed; mesh lists mouse spleen / rat synaptosomes for binding context — **hCB2 GTPγS not proven**. |
| 8 | Experimental system | Dhop: **HEK293 stably expressing mouse CB2** (intact-cell LANCE Ultra cAMP / cyclase). **Not** hCB2 CHO membranes. |
| 9 | Assay type | Dhop verified row = **adenylyl cyclase / forskolin cAMP**, **not** [³⁵S]GTPγS. |
| 10 | Chemical identity | Abstract + MEDLINE chemicals: AM1710 = **9-methoxy** analog **4b** = `3-(1,1-dimethyl-heptyl)-1-hydroxy-9-methoxy-benzo(c)chromen-6-one`; AM1714 = **9-hydroxy** analog **5**. Compound **5a** as AM1710: **refuted by abstract numbering**. Neighbors: **4b ≠ 5 ≠ 5a**. |
| 11 | SMILES verified/not verified | **NOT VERIFIED** atom-by-atom from Khanolkar structure drawing (PDF unrecovered). |
| 12 | Contradictions found | See §8 C2/C3. |
| 13 | Recovery result | **NOT_VERIFIED** for adversarial `5a / 11.2 / GTPγS / 89%`. **REVIEW_REQUIRED** overall (cannot CONFIRMED). Dhop ~11 nM = **PARTIAL/DIRECT** mCB2 cyclase only. |
| 14 | Brief auditable explanation | Prove/refute: **`AM1710 = 5a = EC50 11.2 nM = GTPγS` is REFUTED / NOT_VERIFIED.** Abstract makes AM1710 = **4b** (not 5a; **5 = AM1714**). **11.2** nowhere in opened primaries. Nearest **11 nM** is Dhop 2016 **mCB2 cyclase** Emax **48±4.3**, not GTPγS, not hCB2 membranes, not 11.2, not 89%. Khanolkar functional table unrecovered → no CONFIRMED GTPγS. |

**Evidence tags (AM1710):**

| Claim | Tag | Quote / location | Interpretation |
|---|---|---|---|
| AM1710 = 4b; 5 = AM1714 | **DIRECT** | Abstract: “9-methoxy analog **4b (AM1710)**”; “9-hydroxyl analog **5 (AM1714)**” | Adversarial **5a = AM1710** fails |
| Pages 4496–4506 | **NOT_FOUND** | PubMed pagination **6493–6500** | Inherited citation error |
| GTPγS EC50 11.2±1.8 / Emax 89±3% | **NOT_FOUND** | Not in abstract; Khanolkar PDF not opened | Do not inherit |
| EC50 ~11 nM functional | **DIRECT** (Dhop) | Table 2 AM1710 cyclase EC50 **11** (5.5–15.6), Emax **48±4.3** | **mCB2** HEK cyclase ≠ GTPγS ≠ hCB2 |
| Ki 6.7 / 360 from Khanolkar table | **NOT_VERIFIED** | BindingDB curated only this pass | Secondary DB ≠ primary table |

---

## 2. GW405833 forensic reconciliation

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | Round1 `GW405833_func_hCB2_cAMP`: EC50 **0.65 nM**; binding Ki **3.92 / 4772**; SMILES/InChIKey stored; Valenzano 2005 primary. ROUND1B lists wrong DOI `…2005.01.010` (correct below). |
| 2 | Primary source found | **Valenzano et al. 2005 full PDF / Fig 1 / Table 2: NOT recovered.** EuropePMC `EXT_ID:15814101 AND HAS_FT:y` → hitCount **0**. Unpaywall `is_oa=false`. Local `data/papers/` has no Valenzano PDF. PubMed **abstract only**. |
| 3 | DOI/identifier | **10.1016/j.neuropharm.2004.12.008**, PMID **15814101**, *Neuropharmacology* **48:658–672**. |
| 4 | Page + table/figure + row | Fig 1 structure / Table 2 pharmacology for 0.65 nM: **NOT_FOUND**. |
| 5 | EC50/other metric exactly as appears | Abstract: **no EC50 0.65**. States high-affinity binding to rat + human CB2; partial agonist **~50%** reduction of forskolin-mediated cAMP vs CP55,940. |
| 6 | Emax exactly as appears | Abstract: “approximately **50%** reduction …” vs full agonist CP55,940 — qualitative/% narrative only; **no separate numeric Emax table cell recovered**. |
| 7 | Species | Abstract: **rat and human** CB2 (binding); functional cAMP species/system **not located** without PDF. |
| 8 | Experimental system | **NOT VERIFIED** (CHO etc. claimed elsewhere; not in abstract). |
| 9 | Assay type | Abstract functional claim = forskolin **cAMP** (partial agonism). |
| 10 | Chemical identity | From Valenzano primary figure: **NOT VERIFIED**. PubMed chemical list names `1-(2,3-dichlorobenzoyl)-5-methoxy-2-methyl-(2-(mopholin-4-yl)ethyl)-1H-indole` (typo “mopholin”) — **metadata only, not Fig 1 inspection**. Secondary OA pointers (Dhop Table 1 footnote; JPET 2017 intro) give morpholinoethyl IUPAC — **INFERRED/informational**, **not** Valenzano-proof. Salt: **NOT VERIFIED**. |
| 11 | SMILES verified/not verified | **SMILES NOT VERIFIED.** Forbidden to rebuild from memory/DB without primary structure. |
| 12 | Contradictions found | See §8 C8 / DOI typo. Dhop mCB2 cyclase Emax **0** for GW405833 — different experiment; do not use to REJECT Valenzano abstract. |
| 13 | Recovery result | **NOT_VERIFIED** (primary unrecovered) → provisional **REVIEW_REQUIRED**. |
| 14 | Brief auditable explanation | Paywalled Valenzano PDF unrecovered honestly. Cannot lock EC50 0.65, Fig 1→SMILES, salt, or N-substituent from primary. Abstract supports partial cAMP agonism ~50% vs CP55,940 only. |

**Evidence tags (GW405833):**

| Claim | Tag | Quote / location | Interpretation |
|---|---|---|---|
| Partial agonist ~50% vs CP55,940 forskolin cAMP | **PARTIAL** | PubMed abstract | Functional class only; no EC50 |
| EC50 0.65 nM | **NOT_FOUND** | Not in abstract; tables unrecovered | Round1 value stays unverified |
| Structure → SMILES | **NOT_FOUND** | Fig 1 unrecovered | SMILES NOT VERIFIED |
| IUPAC morpholinoethyl (secondary) | **INFERRED** | Dhop footnote / JPET naming | Pointer only |

---

## 3. CP-55,940 verification

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | Round1 `CP55940_ref_note` only (global reference). Adversarial “CONFIRMED homogeneous hCB2 cAMP” was rejected in Round1.2. |
| 2 | Primary source found | **No single Round1-locked primary.** Consistency: **Soethoudt et al. 2017** *Nat Commun* **8:13958** main PDF + SI MOESM657 recovered. Felder 1995 abstract: binding Kd only. Dhop 2016 Table 2: **mCB2** cyclase. |
| 3 | DOI/identifier | Soethoudt: **10.1038/ncomms13958**, PMID **28045021**, PMC**5216056**. Felder: PMID **7565624**. Dhop: PMC**4959096**. |
| 4 | Page + table/figure + row | Soethoudt SI **Supplementary Table 4** row **CP55940**, columns **hCB2R** (Roche human cAMP). Also Suppl Table 3 GTPγS hCB2R. |
| 5 | EC50/other metric exactly as appears | Soethoudt SI Table 4 hCB2 cAMP: **pEC50 10.33 ± 0.09** (implies ~0.047 nM; report **pEC50 as published**). Felder abstract: [³H]CP Kd **2.6 / 3.7 nM** CB1/CB2 — **binding**, not functional EC50. Dhop mCB2 cyclase EC50 **3** nM. |
| 6 | Emax exactly as appears | Soethoudt SI Table 4 hCB2: **Emax 98 ± 1**; footnote: normalized to **10 µM CP55940**. (Self-reference normalization — explicit numeric but tautological as absolute “CP Emax=100” row.) |
| 7 | Species | Soethoudt human cAMP: **human CB2**. |
| 8 | Experimental system | Methods “Human cAMP assay”: **CHO cells stably expressing human CB2** (DiscoveRx), intact cells, cAMP-Nano-TRF (Roche). |
| 9 | Assay type | **forskolin-related cAMP** (Nano-TRF kit; IBMX buffer). Separate GTPγS on **CHOK1 membranes** (Suppl Table 3: pEC50 **8.43 ± 0.25**, Emax **95 ± 4**). |
| 10 | Chemical identity | Used as named reference ligand CP55940; structure regeneration **not** performed this pass. |
| 11 | SMILES verified/not verified | **NOT VERIFIED** from primary structure drawing. |
| 12 | Contradictions found | Multi-assay / multi-species numbers (Felder Kd vs Soethoudt pEC50 vs Dhop mCB2) — do not invent one global Ki/EC50 (Q-12). |
| 13 | Recovery result | **REVIEW_REQUIRED** (Soethoudt SI newly supplies hCB2 cAMP numbers; SMILES + Round1 “no locked row” + Gold ban → no CONFIRMED promotion). |
| 14 | Brief auditable explanation | Soethoudt **is** a usable pharmacological primary for CP hCB2 cAMP **if** a future row is curated from Suppl Table 4 — but Round 1.3 does not promote Gold/CONFIRMED. Prior CONFIRMED claim still fails Round1 gate (ref_note only + SMILES). |

**Evidence tags:** Soethoudt SI Table 4 CP55940 hCB2 = **DIRECT**; Felder functional WIN/CP EC50 = **NOT_FOUND**; Dhop CP = **DIRECT** for **mCB2** only.

---

## 4. HU-308 verification

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | Round1 qualitative `HU308_func_cAMP`; Round1.1/1.2 near-miss: Hanuš EC50 **5.57 nM**, Emax **108.6±8.4%**; adversarial CONFIRMED demoted for SMILES + Emax-reference atomicity. |
| 2 | Primary source found | **Hanuš et al. 1999** PNAS EuropePMC PDF extract **re-opened** (claimed primary). **Soethoudt 2017** SI Tables 3–4 recovered as consistency check (not Round1 claimed primary). |
| 3 | DOI/identifier | Hanuš: **10.1073/pnas.96.25.14228**, PMID **10588688**, PMC**24419**. Soethoudt: **10.1038/ncomms13958**. |
| 4 | Page + table/figure + row | Hanuš Results cAMP paragraph (PMC/EuropePMC extract). Soethoudt SI Table 4 row **HU308** hCB2R; Table 3 GTPγS row HU308. |
| 5 | EC50/other metric exactly as appears | Hanuš: EC50 **5.57 nM** (95% CL **1.68 and 18.5 nM**; n=5). Soethoudt SI Table 4 hCB2 cAMP: **pEC50 8.53 ± 0.06**. |
| 6 | Emax exactly as appears | Hanuš: **108.6 ± 8.4%** (n=5). Soethoudt SI Table 4: **98 ± 1** (vs 10 µM CP55940). β-AR Suppl Table 5: HU308 Emax **57 ± 10** (partial recruitment) — **different assay**. |
| 7 | Species | Hanuš: **human CB2**. Soethoudt hCB2 columns: human. |
| 8 | Experimental system | Hanuš Methods: **CHO stably transfected with human CB1 or CB2**. Soethoudt human cAMP: CHO DiscoveRx hCB2, Nano-TRF. |
| 9 | Assay type | Hanuš: forskolin-stimulated **cAMP** inhibition (method cites Ross [19]). |
| 10 | Chemical identity | Named HU-308; Scheme 1 / Structure V described in paper — **atom-by-atom SMILES regeneration not completed this pass**. |
| 11 | SMILES verified/not verified | **NOT VERIFIED** (InChIKey `CFMRIVODIXTERW-BDTNDASRSA-N` not regenerated from Structure V). |
| 12 | Contradictions found | Hanuš EC50 5.57 vs Soethoudt pEC50 8.53 (~3 nM) — different labs/kits; do not pool. Emax 108.6% vs CP=100 atomicity still not explicit in Hanuš Results. |
| 13 | Recovery result | **REVIEW_REQUIRED** (pharmacology DIRECT/PARTIAL; SMILES block + Gold ban). |
| 14 | Brief auditable explanation | Strongest pharmacologic near-miss remains Hanuš hCB2 forskolin cAMP. Soethoudt SI corroborates high-efficacy hCB2 cAMP agonist numerically under CP55940=100 normalization, but Round 1.3 does not promote CONFIRMED/Gold. |

---

## 5. RG7774 verification

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | `VICASINABIN_func_cAMP_hCB2` EC50 **2.81 ± 0.28 nM**; Emax “full agonist”; β-arr Round1 ~22 nM conflict. |
| 2 | Primary source found | Grether / Ullmer et al. 2024 Frontiers OA PDF + extract **re-opened**. |
| 3 | DOI/identifier | **10.3389/fphar.2024.1426446**, PMC**11272598**. |
| 4 | Page + table/figure + row | Methods **2.2.2** cAMP; Results §3.3; **Figure 3A** (cAMP), **Figure 3B** (β-arrestin). |
| 5 | EC50/other metric exactly as appears | hCB2 cAMP **2.81 ± 0.28 nM**; mCB2 **2.60 ± 0.14 nM** (separate); β-arr **99.69 ± 5.72 nM**. |
| 6 | Emax exactly as appears | “**full agonist** … compared to the maximum efficacy of the reference agonist (**CP55940**)” — **no numeric %**. Do **not** convert to 100%. |
| 7 | Species | Recombinant **human** CB2R (and mouse separately). |
| 8 | Experimental system | **CHOK1hCB2_bgal** (DiscoveRx) — **CHO, not HEK293**. |
| 9 | Assay type | Forskolin-stimulated **cAMP** (cAMP-Nano-TRF). β-arrestin = separate PathHunter. |
| 10 | Chemical identity | IUPAC **(S)-1-(5-tert-butyl-3-[(1-methyl-1H-tetrazol-5-yl)methyl]-3H-[1,2,3]triazolo[4,5-d]pyrimidin-7-yl)pyrrolidin-3-ol**; CAS **1433361-02-4**; synthesis compound **9**; X-ray CCDC **22814444**. |
| 11 | SMILES verified/not verified | **NOT VERIFIED** atom-by-atom / InChIKey not regenerated from X-ray coordinates this pass. |
| 12 | Contradictions found | β-arr ~22 vs **99.69±5.72** (METRIC_CONFLICT). HEK293 claim unsupported. |
| 13 | Recovery result | **REVIEW_REQUIRED**. |
| 14 | Brief auditable explanation | EC50/system/assay chain for hCB2 cAMP reconfirmed DIRECT; numeric Emax % and SMILES still block CONFIRMED. |

---

## 6. APD371 Emax investigation

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | Missing quantitative Emax; sometimes “typically cAMP”; Director “compound 17”. |
| 2 | Primary source found | Han et al. 2017 ACS Med Chem Lett / PMC5733264 EuropePMC PDF extract. **ACS SI HTTP 403** — Figure S6 / cell-line catalog **not opened**. |
| 3 | DOI/identifier | **10.1021/acsmedchemlett.7b00396**, PMID **29259753**, PMC**5733264**. |
| 4 | Page + table/figure + row | **Table 1** compound **6**; also Table 2 row **6**; text cites Figure S6 for ~106%. |
| 5 | EC50/other metric exactly as appears | hCB2 **6.2** (nM); hCB1 **>10,000**; rCB2 **7.6**. |
| 6 | Emax exactly as appears | Table 1: **(106)** with footnote b: “Intrinsic activity (Emax) was determined relative to **CP-55,940 (100)**.” Assay header: **β-arrestin, EC50 (nM)**. **No quantitative cAMP Emax for compound 6 in main tables.** Do not invent cAMP Emax. |
| 7 | Species | **hCB2** (and rCB2) PathHunter. |
| 8 | Experimental system | DiscoverX **PathHunter** β-arrestin; SI cell-line catalog unrecovered. |
| 9 | Assay type | **β-arrestin recruitment** — **not cAMP**. Text mentions HTRF cyclase for **other** SAR compounds; APD371 Table 1 format = β-arrestin. |
| 10 | Chemical identity | Compound **6** = **APD371** / olorinab; stereo **(S,S)**; compound **17** = different CF3 analog ≠ APD371. |
| 11 | SMILES verified/not verified | **NOT VERIFIED** from SI/scheme atom-by-atom. |
| 12 | Contradictions found | ASSAY_CONFLICT if labeled cAMP; compound 17 identity error. |
| 13 | Recovery result | **REVIEW_REQUIRED** (β-arrestin Emax **is** explicit; cAMP Emax **NOT_VERIFIED**; not CAMP_HOMOGENEOUS). |
| 14 | Brief auditable explanation | Quantitative Emax **106% vs CP-55,940=100** is **β-arrestin Table 1 compound 6**. SI unrecovered → cannot add cAMP Emax. |

---

## 7. WIN 55,212-2 primary-source investigation

### Required fields

| # | Field | Finding |
|---|---|---|
| 1 | Original claim | Round1 `WIN55212_ref_note`; need Felder/Showalter historical quantitative primary; Hua 2020 Cryo-EM not substitute. |
| 2 | Primary source found | **Felder 1995** PubMed abstract only (full PDF OA not recovered). **Showalter 1996** PMID 8831752 = different chemistry paper → **not** WIN characterization primary. **Soethoudt 2017 SI Tables 3–4** recovered as later profiling primary (not historical original). Dhop 2016 Table 2 WIN row = **mCB2**. |
| 3 | DOI/identifier | Felder: *Mol Pharmacol* **48:443–450**, PMID **7565624**. Soethoudt: **10.1038/ncomms13958**. |
| 4 | Page + table/figure + row | Felder: abstract only — **no table EC50/Emax**. Soethoudt SI Table 4 row **WIN55212-2** hCB2R; Table 3 GTPγS. |
| 5 | EC50/other metric exactly as appears | Felder abstract: WIN higher affinity CB2 vs CB1; cAMP rank-order narrative — **no numeric WIN EC50**. Soethoudt SI Table 4 hCB2 cAMP: **pEC50 9.50 ± 0.09**. Table 3 GTPγS hCB2: **pEC50 7.96 ± 0.04**. Dhop mCB2 cyclase: EC50 **16** (10.5–21.7). |
| 6 | Emax exactly as appears | Soethoudt SI Table 4 hCB2 cAMP: **98 ± 1**; GTPγS: **49 ± 7** (partial). Dhop cyclase: **40 ± 1.2**. |
| 7 | Species | Soethoudt: **human** CB2 (Roche cAMP; Leiden GTPγS membranes). Felder: human CB1/CB2 in CHO/AtT-20 (abstract). |
| 8 | Experimental system | Soethoudt GTPγS: **CHOK1CB_bgal membranes**; cAMP: **CHO DiscoveRx** intact cells Nano-TRF. |
| 9 | Assay type | Soethoudt: cAMP and [³⁵S]GTPγS **separate**. |
| 10 | Chemical identity | Named WIN55,212-2; salt/form not re-proven. |
| 11 | SMILES verified/not verified | **NOT VERIFIED**. |
| 12 | Contradictions found | Partial (GTPγS/β-arr) vs near-full (cAMP) — assay-dependent; do not pool. Hua Cryo-EM rejected as screening primary. |
| 13 | Recovery result | **REVIEW_REQUIRED** (historical Felder numbers **NOT_VERIFIED**; Soethoudt SI supplies later DIRECT numbers but Round 1.3 no Gold/CONFIRMED promote). |
| 14 | Brief auditable explanation | Original Felder full-text tables still missing. Soethoudt SI is a valid modern primary for WIN hCB2 cAMP/GTPγS metrics if curated later as a **separate** Source_Exact_Location row. |

---

## 8. Contradiction log

| ID | Claim A | Claim B | Resolution |
|---|---|---|---|
| C1 | AM1710 = compound **5a** GTPγS 11.2 / 89% | Khanolkar abstract: AM1710 = **4b**; **5 = AM1714**; no 11.2/89% in abstract; PDF unrecovered | **A NOT_VERIFIED / refuted on ID.** Keep REVIEW |
| C2 | ~11 nM = Khanolkar GTPγS hCB2 | Dhop 2016 Table 2: cyclase EC50 **11**, Emax **48±4.3**, **HEK-mCB2** | **B DIRECT.** Nearest 11 nM is mCB2 cyclase |
| C3 | JPET 2017: AM1710 EC50 11 nM “human CB2” | Dhop 2016 Methods: **mouse** CB2 | **2016 Methods control.** Cross-paper species error |
| C4 | Khanolkar pages 4496–4506 | PubMed **6493–6500** | Citation error logged |
| C5 | Unpaywall “OA” Khanolkar | Resolves to BindingDB curated Ki page | **Not primary PDF** |
| C6 | GW Round1 EC50 0.65 + SMILES | Valenzano PDF unrecovered; abstract lacks 0.65 | **NOT_VERIFIED** |
| C7 | ROUND1B Valenzano DOI `…2005.01.010` | Correct DOI `…2004.12.008` | Typo logged; do not overwrite Round1 files |
| C8 | Valenzano ~50% partial agonist | Dhop GW405833 mCB2 cyclase Emax **0** | Do not pool; different species/assay |
| C9 | Olorinab missing Emax / cAMP | Han Table 1 β-arrestin **106%** vs CP=100 | Emax found for **β-arrestin**; cAMP Emax still absent |
| C10 | APD371 = compound 17 | Han: APD371 = compound **6** | **17 rejected** |
| C11 | Vicasinabin β-arr ~22 nM | Frontiers **99.69±5.72 nM** | METRIC_CONFLICT |
| C12 | Vicasinabin HEK293? | Methods CHOK1hCB2_bgal | **CHO** |
| C13 | CP/HU/WIN “CONFIRMED” without SI | Soethoudt SI Tables 3–4 now recover numeric pEC50/Emax | Improves evidence; **still no Round1.3 Gold/CONFIRMED promote** (SMILES + directive) |
| C14 | Local `soethoudt_pmc.html` | Wrong cardiology article (prior recon temp) | Superseded by Nat Commun PDF/SI |
| C15 | Hua 2020 as WIN screening primary | Directive | **Rejected** |

---

## 9. Exact source locations

| Compound | Source | Exact location | What locked |
|---|---|---|---|
| AM1710 | Khanolkar 2007 abstract (PMID 18038967) | Abstract compound sentences | **4b = AM1710**; **5 = AM1714** |
| AM1710 | Dhopeshwarkar & Mackie 2016 PMC4959096 | Methods HEK-mCB2 cyclase; **Table 2** row AM1710 | Cyclase EC50 **11** (5.5–15.6), Emax **48±4.3**; arrestin 4 / 91±3.6 |
| AM1710 | Khanolkar full PDF / GTPγS table | — | **NOT RECOVERED** |
| GW405833 | Valenzano 2005 abstract (PMID 15814101) | Abstract only | Partial ~50% cAMP vs CP55,940; rat+human CB2 binding claim |
| GW405833 | Valenzano Fig 1 / Table 2 / 0.65 nM | — | **NOT RECOVERED** |
| CP-55,940 | Soethoudt 2017 SI MOESM657 | **Suppl Table 4** row CP55940 hCB2R | pEC50 **10.33±0.09**, Emax **98±1** (vs 10 µM CP55940); Roche CHO hCB2 Nano-TRF Methods |
| CP-55,940 | Soethoudt SI | **Suppl Table 3** row CP55940 hCB2R | GTPγS pEC50 **8.43±0.25**, Emax **95±4**; CHO membranes |
| HU-308 | Hanuš 1999 EuropePMC PDF extract | Results cAMP paragraph; Methods CHO hCB1/hCB2 | EC50 **5.57 nM**; Emax **108.6±8.4%** |
| HU-308 | Soethoudt SI Suppl Table 4 | Row HU308 hCB2R | pEC50 **8.53±0.06**, Emax **98±1** |
| RG7774 | Frontiers 2024 | Methods 2.2.2; Results §3.3; Fig 3A/3B | EC50 2.81±0.28; “full” sans %; β-arr 99.69±5.72; CHO |
| APD371 | Han 2017 PMC5733264 | Table 1 / Table 2 compound **6**; footnote b | β-arrestin EC50 **6.2**, Emax **106** vs CP=100 |
| APD371 | Han ACS SI / Fig S6 | — | **HTTP 403 / NOT OPENED** |
| WIN | Felder 1995 abstract | Abstract | Affinity preference narrative; **no numeric WIN EC50/Emax** |
| WIN | Soethoudt SI Tables 3–4 | Rows WIN55212-2 | cAMP pEC50 **9.50±0.09**, Emax **98±1**; GTPγS pEC50 **7.96±0.04**, Emax **49±7** |

**Attempted / blocked:** Valenzano PDF (paywall); Khanolkar PDF + ACS SI (paywall/403); Han ACS SI (403); Felder full PDF OA (unavailable this pass); Sci-Hub **not used**.

---

## 10. Provisional final classification

| Compound | Provisional Final_Status | Notes |
|---|---|---|
| AM1710 | **REVIEW_REQUIRED** (+ adversarial GTPγS claim **NOT_VERIFIED**) | 4b≠5a; 11 nM = mCB2 cyclase |
| GW405833 | **NOT_VERIFIED** / **REVIEW_REQUIRED** | Primary PDF unrecovered; SMILES NOT VERIFIED |
| CP-55,940 | **REVIEW_REQUIRED** | Soethoudt SI numbers recovered; SMILES + no Gold promote |
| HU-308 | **REVIEW_REQUIRED** | Hanuš pharmacology strong; SMILES not regenerated |
| RG7774 / Vicasinabin | **REVIEW_REQUIRED** | EC50 OK; Emax% + SMILES fail |
| APD371 / Olorinab | **REVIEW_REQUIRED** | β-arrestin Emax OK; not cAMP |
| WIN 55,212-2 | **REVIEW_REQUIRED** | Felder numbers missing; Soethoudt SI later primary exists |

**Do NOT declare definitive Gold in Round 1.3.**

---

## Closing summary table

| Compound | Primary source recovered | EC50 verified | Emax verified | Species/system verified | SMILES verified | Final status |
|---|---|---|---|---|---|---|
| AM1710 | Partial (abstract + Dhop 2016; **not** Khanolkar PDF) | Partial (Dhop **11** nM mCB2 cyclase; **not** 11.2 GTPγS) | Partial (Dhop 48±4.3 cyclase; **not** 89%) | Yes for Dhop mCB2 HEK; **no** for claimed hCB2 GTPγS | **No** | **REVIEW_REQUIRED** / GTPγS claim **NOT_VERIFIED** |
| GW405833 | **No** (abstract only) | **No** (0.65 not found) | Partial (~50% abstract only) | **No** (system unrecovered) | **No** | **NOT_VERIFIED** → **REVIEW_REQUIRED** |
| CP-55,940 | Yes (Soethoudt SI T4; Felder abstract binding only) | Yes as **pEC50 10.33±0.09** (Soethoudt hCB2 cAMP) | Yes **98±1** (vs 10 µM CP55940) | Yes CHO hCB2 Nano-TRF | **No** | **REVIEW_REQUIRED** |
| HU-308 | Yes (Hanuš 1999 + Soethoudt SI) | Yes Hanuš **5.57 nM**; Soethoudt pEC50 **8.53±0.06** (separate) | Yes Hanuš **108.6±8.4%**; Soethoudt **98±1** | Yes CHO hCB2 (both) | **No** | **REVIEW_REQUIRED** |
| RG7774 | Yes (Frontiers 2024) | Yes **2.81±0.28 nM** | **No** numeric % (“full” only) | Yes CHOK1hCB2_bgal | **No** | **REVIEW_REQUIRED** |
| APD371 | Yes (Han 2017 main text; SI no) | Yes **6.2 nM** (β-arrestin) | Yes **106%** (β-arrestin vs CP=100); **cAMP Emax no** | Partial (PathHunter; SI catalog no) | **No** | **REVIEW_REQUIRED** |
| WIN 55,212-2 | Partial (Felder abstract no; Soethoudt SI yes) | Yes Soethoudt cAMP pEC50 **9.50±0.09** / GTPγS **7.96±0.04**; Felder **no** | Yes Soethoudt cAMP **98±1** / GTPγS **49±7** | Yes Soethoudt CHO systems | **No** | **REVIEW_REQUIRED** |

### Counts (provisional Round 1.3)

| Bucket | N |
|---|---|
| **CONFIRMED** | **0** |
| **REVIEW_REQUIRED** | **7** |
| **REJECTED** | **0** |
| **NOT_VERIFIED** (compound-level primary failure / adversarial GTPγS) | **GW405833 primary**; **AM1710 GTPγS 11.2/5a claim** |

### One-line verdicts (parent)

- **AM1710:** Adversarial `5a / 11.2 nM / GTPγS` **refuted/not verified**; AM1710=**4b**; ~11 nM = Dhop **mCB2 cyclase** (Emax 48±4.3), not Khanolkar GTPγS.  
- **GW405833:** Valenzano **PDF unrecovered** → EC50 0.65 + SMILES **NOT VERIFIED** → **REVIEW_REQUIRED**.

### Integrity

- Written only: `results/reports/ROUND1.3_PRIMARY_SOURCE_RECOVERY.md`  
- No git commit/PR; no Gold / Round1 CSV / prior report modification.

---

*End ROUND1.3_PRIMARY_SOURCE_RECOVERY — create-only; stop.*
