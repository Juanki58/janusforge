# ROUND 1.4 — FINAL CONTRADICTION RESOLUTION

**Date:** 2026-08-16  
**Phase:** Final contradiction resolution (create-only)  
**Read-only inputs:** `ROUND1.3_CROSS_VALIDATION.md`, `ROUND1.3_PRIMARY_SOURCE_RECOVERY.md`, `ROUND1_RECONCILIATION_v1.0.md`, local `data/papers/` / `_recon_tmp/` OA extracts  
**Output path:** `results/reports/ROUND1.4_FINAL_CONTRADICTION_RESOLUTION.md`  
**Integrity:** NO Gold / Round1 CSV / prior-report overwrite; NO models / docking / QSAR / classification; NO git modifications. **Pipeline remains STOP.**

**Evidence tags:** **DIRECT** | **PARTIAL** | **INFERRED** | **NOT_FOUND**

**Status vocabulary used:** `CONFIRMED_SUBSET_A_cAMP` | `CONFIRMED_SUBSET_B_GTPGAMMAS` | `REVIEW_REQUIRED` | `REJECTED` | `NOT_VERIFIED`  
**Do NOT declare definitive Gold.**

---

## 0. Recovery attempts this pass (legitimate OA only)

| Target | Attempt | Outcome |
|---|---|---|
| Khanolkar *J Med Chem* 2007 DOI `10.1021/jm070441u` full PDF / Table 1–2 | ACS HTML/PDF (403); EuropePMC `HAS_FT` unavailable; Unpaywall/OpenAlex “green OA” → BindingDB DOI `10.7270/q2736qn9` (curated Ki HTML, **not** ACS PDF); Wayback CDX pdfplus snapshots = **HTTP 403 HTML only**; ACS SI `jm070441u-file002.pdf` 403 (SI text = elemental/X-ray for **4a/4b**, not pharmacology tables) | **Primary tables NOT recovered** |
| Khanolkar abstract / ACS landing abstract | PubMed efetch text; ACS landing abstract (paywalled body; abstract visible) | **Recovered** |
| Valenzano *Neuropharmacology* 2005 DOI `10.1016/j.neuropharm.2004.12.008` full PDF / Fig 1 / Table 2 | Unpaywall/OpenAlex `is_oa=false`; EuropePMC FT unavailable; Wayback CDX for ScienceDirect PII → empty 200 list; no local PDF | **Primary NOT recovered** |
| Valenzano abstract | PubMed efetch / PubMed XML | **Recovered** |
| Dhopeshwarkar & Mackie 2016 PMC4959096 | Local PMC HTML Table 2 + Methods | **Recovered** (mix-check only) |
| Sci-Hub / pirate mirrors | — | **Not used** |

**Citation correction (inherited error):** Mission brief pages **4496–4506** do **not** match PubMed/ACS pagination **6493–6500** (same DOI/PMID 18038967). Tag: **DIRECT** (PubMed/ACS masthead).

---

## 1. PRIORITY 1 — AM1710 (Khanolkar et al. 2007)

### 1.1 Resolved item: Identity — is AM1710 compound 4b or 5a?

| Field | Content |
|---|---|
| **1. Contradiction** | Gemini Round 1.3: AM1710 = compound **5a**. Cursor Round 1.3: AM1710 = **4b**; compound **5** = **AM1714**. |
| **2. Primary source** | Khanolkar AD et al., *J Med Chem* **50:6493–6500** (2007), DOI `10.1021/jm070441u`, PMID **18038967** — **abstract** as published on ACS landing page + PubMed abstract of the same article. |
| **3. Exact evidence** | ACS / PubMed abstract (verbatim core): *“Optimal receptor subtype selectivity of 490-fold and subnanomolar affinity for the CB2 receptor is exhibited by a 9-hydroxyl analog **5 (AM1714)**, while the 9-methoxy analog **4b (AM1710)** had a 54-fold CB2 selectivity.”* Location: article abstract (ACS landing + PubMed efetch). Tag: **DIRECT**. Abstract does **not** name any compound **5a** as AM1710. |
| **4. Resolution** | **4b = AM1710** is primary-abstract locked. **5 = AM1714**. Gemini **5a = AM1710** is **REJECTED**. No vote / average / chemical knowledge substitute. |
| **5. Final status** | Identity claim **4b=AM1710**: documentary lock from abstract (**not** a Subset A/B promotion). Compound-level pharmacology status remains **`REVIEW_REQUIRED`** (tables unrecovered). Gemini identity package: **`REJECTED`**. |
| **6. Confidence** | **High** (identical wording on ACS abstract + PubMed). |

### 1.2 Correspondence table (what can be documented without inventing cells)

**Rule:** No secondary common-name authority. Table cells without primary Table 1/2 page images are marked PARTIAL/NOT_FOUND.

| Compound code | Common name (primary abstract only) | Ki | Functional EC50 | Emax | Assay |
|---|---|---|---|---|---|
| **4b** | **AM1710** (**DIRECT** abstract) | CB2 **6.7 nM** / CB1 **360 nM** / selectivity **54** — **PARTIAL** (ChEMBL doc `CHEMBL1138340` / BindingDB BDBM50228073 of **same DOI**; assay text: *“Displacement of [3H]CP-55940 from CB2 receptor in **mouse spleen membranes**”*). Primary Table 1 page image: **NOT_FOUND** | **NOT_FOUND** in Khanolkar abstract / ChEMBL activities for this DOI (no EC50 **11.2**) | Curve Emax **89±3%**: **NOT_FOUND**. ChEMBL GTPγS for CHEMBL266712: **Activity = 50.0%** at **1 µM** (**PARTIAL**; not an EC50/Emax fit) | Binding: [³H]CP-55940 displacement, **mouse spleen** CB2 / **rat** brain synaptosomes CB1 (**PARTIAL** curated). Functional GTPγS: % at fixed 1 µM in mouse spleen membranes (**PARTIAL**) |
| **5** | **AM1714** (**DIRECT** abstract: “9-hydroxyl analog **5 (AM1714)**”) | CB2 **0.82 nM** / selectivity **490** — **PARTIAL** (ChEMBL CHEMBL429797 same DOI; abstract states 490-fold / subnanomolar — **DIRECT** for selectivity language, not table cell) | **NOT_FOUND** as numeric EC50 in opened sources | ChEMBL GTPγS **55%** at 1 µM (**PARTIAL**) | Same membrane systems (**PARTIAL**) |
| **5a** | **Not identified as AM1710** in primary abstract | — | — | — | Abstract numbering uses **5**, not **5a**, for AM1714. Any “5a = AM1710” mapping: **REJECTED** vs abstract |
| **4a** | Named only in ACS SI blurb (“X-ray … for **4a** and **4b**”) | SI recovered as elemental/X-ray pointer only; pharmacology **NOT_FOUND** | **NOT_FOUND** | **NOT_FOUND** | Chemistry SI, not functional table |

**Which Table 1 / Table 2 values belong to whom?**  
Primary Table 1 / Table 2 page images were **not opened** this pass → cell-by-cell ownership from Khanolkar tables = **NOT_FOUND**. Curated deposits above are labeled **PARTIAL** and are **not** accepted as Subset B confirmation.

### 1.3 Resolved item: Does `11.2 nM / 89%` belong to AM1710?

| Field | Content |
|---|---|
| **1. Contradiction** | Gemini: AM1710 GTPγS EC50 **11.2 ± 1.8 nM**, Emax **89 ± 3%**, **hCB2**. Cursor: values **NOT_FOUND** in Khanolkar; nearest ~11 nM is Dhop 2016. |
| **2. Primary source** | Khanolkar 2007 abstract + ChEMBL activities for DOI `10.1021/jm070441u` (tagged PARTIAL). Cross-check only: Dhopeshwarkar & Mackie 2016, *JPET*, PMC**4959096**, Table 2 + Methods. |
| **3. Exact evidence** | (a) Khanolkar abstract: **no** EC50 11.2, **no** Emax 89%. Tag: **NOT_FOUND**. (b) ChEMBL `CHEMBL1138340` for CHEMBL266712 (AM1710 SMILES match): Ki 6.7 / GTPγS **50% @ 1 µM** / cAMP agonist Activity blank — **no 11.2 / no 89**. Tag: **PARTIAL** (absence in curated deposit of this DOI). (c) Dhop 2016 Table 2 row **AM1710**: cyclase EC50 **11** (95% CI **5.5–15.6**), Emax **48 ± 4.3**; arrestin EC50 **4**, Emax **91 ± 3.6**. Methods: *“HEK293 cells … stably expressing **mouse** CB2”* / LANCE Ultra **cAMP** (cyclase). Tag: **DIRECT** for Dhop row — **different paper, assay, species**. Literal string **11.2** for AM1710: **NOT_FOUND** in opened literature this pass. |
| **4. Resolution** | **Cannot prove** that **11.2 nM / 89%** belongs to AM1710 from Khanolkar. Per mission rule: **`AM1710 = REVIEW_REQUIRED`** for this functional package; **do NOT use 11.2 nM by secondary association**. Nearest ~11 nM = Dhop **mCB2 cyclase EC50 11** (not 11.2; Emax **48±4.3**, not 89%) — labeled as **different assay/species**, not Khanolkar GTPγS/hCB2. |
| **5. Final status** | **`REVIEW_REQUIRED`** — **not** `CONFIRMED_SUBSET_B_GTPGAMMAS`. Functional package **11.2/89**: **`NOT_VERIFIED`** / ownership **NOT assigned** to AM1710. |
| **6. Confidence** | **High** that 11.2/89 is unproven for Khanolkar-AM1710; **High** that Dhop ~11 is a separate mCB2 cyclase datum. |

### 1.4 AM1710 parent verdict

| Question | Verdict |
|---|---|
| Which compound is **4b**? | **AM1710** (**DIRECT** abstract) |
| Which is **5a**? | **Not AM1710** in primary abstract; AM1714 is compound **5** (**DIRECT**) |
| Which is **AM1710**? | **4b** only (primary abstract) |
| Does **11.2 nM / 89%** belong to AM1710? | **Not proven** → do not assign; status **`REVIEW_REQUIRED`** |
| Subset membership | **Excluded from Subset A**; **not** promoted to Subset B |

---

## 2. PRIORITY 2 — GW405833 (Valenzano et al. 2005)

### 2.1 Resolved item: Structure from Valenzano Fig 1 + SMILES

| Field | Content |
|---|---|
| **1. Contradiction** | Gemini: structure/SMILES “resolved” (incl. morpholinoethyl etc.). Cursor: Valenzano Fig 1 unrecovered → SMILES **NOT VERIFIED**. |
| **2. Primary source** | Valenzano KJ et al., *Neuropharmacology* **48:658–672** (2005), DOI `10.1016/j.neuropharm.2004.12.008`, PMID **15814101**. Required: **Fig. 1** of this paper. |
| **3. Exact evidence** | Fig. 1 body: **NOT_FOUND** (PDF unrecovered). PubMed abstract names **GW405833** and forskolin **cAMP** partial agonism only — **no** structural drawing. Tag: **NOT_FOUND** for Fig 1. PubMed MeSH chemical string `1-(2,3-dichlorobenzoyl)-5-methoxy-2-methyl-(2-(mopholin-4-yl)ethyl)-1H-indole` and later OA IUPAC footnotes (e.g. Dhop Table 1) are **metadata / secondary** — **not** Valenzano Fig 1 inspection. Per mission: **not accepted** as primary structure proof. |
| **4. Resolution** | Structure checklist from Valenzano primary only: |

| # | Element | Status from Valenzano primary |
|---|---|---|
| 1 | Fig. 1 structure | **NOT_FOUND** |
| 2 | Exact chemical name | **NOT_FOUND** (abstract silent) |
| 3 | N1 substituent | **NOT_FOUND** |
| 4 | Indole ring substituents | **NOT_FOUND** |
| 5 | Benzoyl group | **NOT_FOUND** |
| 6 | Both chlorine positions | **NOT_FOUND** |
| 7 | Morpholinyl-ethyl/propyl/etc. chain | **NOT_FOUND** |
| 8 | SMILES from that structure | **Not generated** (structure not fixed) |

| **5. Final status** | **`GW405833 = REVIEW_REQUIRED`** (structure **`NOT_VERIFIED`**). No SMILES declared from primary. |
| **6. Confidence** | **High** that Fig 1 was not recovered; therefore structure cannot be locked. |

### 2.2 Resolved item: EC50 14±2 nM / Emax 48±4% / hCB2 CHO-K1 cAMP

| Field | Content |
|---|---|
| **1. Contradiction** | Gemini: EC50 **14 ± 2 nM**, Emax **48 ± 4%**, hCB2, CHO-K1, cAMP. Cursor: abstract has ~50% only; exact 14±2 / 48±4 **NOT_FOUND**; mix risk with Dhop AM1710 cyclase **48±4.3**. |
| **2. Primary source** | Valenzano 2005 abstract (only recovered primary fragment). |
| **3. Exact evidence** | Abstract quote (**DIRECT**): *“GW405833 selectively binds both rat and human CB2 receptors with high affinity, where it acts as a partial agonist (**approximately 50%** reduction of forskolin-mediated cAMP production compared to the full cannabinoid agonist, CP55,940).”* Exact **14 ± 2 nM**: **NOT_FOUND** in abstract; PDF tables unrecovered. Exact **48 ± 4%**: **NOT_FOUND**. **CHO-K1**: not stated in abstract (MeSH lists CHO Cells — **PARTIAL** metadata only, not methods quote). Vendor/secondary literature often cites **0.65 nM** — also **not** in Valenzano abstract; **not** used as authority here. Literal web hunt for “14±2” + GW405833 this pass: **NOT_FOUND**. |
| **4. Resolution** | Cannot lock Gemini’s **14±2 / 48±4 / CHO-K1** package to Valenzano primary. Abstract supports **partial agonist ~50%** forskolin **cAMP** vs CP55,940 and rat+human CB2 binding language only. No reconciliation by averaging with vendor 0.65 nM. |
| **5. Final status** | **`REVIEW_REQUIRED`** — **not** `CONFIRMED_SUBSET_A_cAMP`. Exact EC50/Emax package: **`NOT_VERIFIED`**. |
| **6. Confidence** | **High**. |

### 2.3 GW405833 parent verdict

| Question | Verdict |
|---|---|
| Structure from Fig 1? | **Not proven** → **`REVIEW_REQUIRED` / `NOT_VERIFIED`** |
| SMILES? | **Not generated** (forbidden without fixed primary structure) |
| EC50 14±2 / Emax 48±4 on hCB2 CHO-K1 cAMP? | **Not proven from primary** → **`NOT_VERIFIED`** |
| Abstract-only functional class | Partial forskolin cAMP ~50% vs CP55,940 (**DIRECT**) |

---

## 3. KEEP UNCHANGED — consistency check (no new primary contradiction)

Mission: change status **only** if a **new** primary contradiction appears. Brief check against Round 1.3 / Round1 reconciliation:

| Compound | Prior status | New primary contradiction this pass? | Status after Round 1.4 |
|---|---|---|---|
| **CP-55,940** | `REVIEW_REQUIRED` | **No** new primary contradiction opened | **`REVIEW_REQUIRED`** (unchanged) |
| **HU-308** | `REVIEW_REQUIRED` | **No** (Hanuš chain not re-litigated; no conflicting new primary) | **`REVIEW_REQUIRED`** (unchanged) |
| **Vicasinabin / RG7774** | `REVIEW_REQUIRED` | **No** | **`REVIEW_REQUIRED`** (unchanged) |

---

## 4. APD371 / WIN 55,212-2 — brief note only

| Compound | Note | Final status |
|---|---|---|
| **APD371 / olorinab** | Remain under review. No new-candidate search this pass. Prior: Han 2017 Table 1 Emax **106%** is **β-arrestin**, not Subset A cAMP. | **`REVIEW_REQUIRED`** |
| **WIN 55,212-2** | Remain under review. No new resources spent. Felder 1995 abstract still lacks numeric WIN EC50/Emax lock. | **`REVIEW_REQUIRED`** |

---

## 5. Final status table

| Compound | Contradiction resolved? | Primary recovered? | Final status | Confidence |
|---|---|---|---|---|
| **AM1710** | Yes: **4b≠5a**; **11.2/89 not owned** | Abstract **yes**; Tables **no** | **`REVIEW_REQUIRED`** (identity 4b locked; Subset B **not** confirmed) | **High** |
| **GW405833** | Yes: structure + 14±2/48±4 **unproven** | Abstract **yes**; Fig1/Table **no** | **`REVIEW_REQUIRED`** / structure metrics **`NOT_VERIFIED`** | **High** |
| CP-55,940 | Consistency only | — | **`REVIEW_REQUIRED`** | — |
| HU-308 | Consistency only | — | **`REVIEW_REQUIRED`** | — |
| RG7774 / Vicasinabin | Consistency only | — | **`REVIEW_REQUIRED`** | — |
| APD371 | Brief only | — | **`REVIEW_REQUIRED`** | — |
| WIN 55,212-2 | Brief only | — | **`REVIEW_REQUIRED`** | — |

**CONFIRMED_SUBSET_A_cAMP count: 0**  
**CONFIRMED_SUBSET_B_GTPGAMMAS count: 0**  
**Definitive Gold declared: No**

---

## 6. Contradiction log (Gemini vs Cursor → primary prevails)

| ID | Gemini claim | Cursor claim | Primary evidence | Resolution |
|---|---|---|---|---|
| R14-1 | AM1710 = **5a** | AM1710 = **4b** | Abstract: **4b (AM1710)**; **5 (AM1714)** (**DIRECT**) | **Gemini REJECTED**; Cursor identity **upheld** |
| R14-2 | GTPγS EC50 **11.2±1.8** / Emax **89±3%** / hCB2 | NOT_FOUND / mix risk | Khanolkar abstract + ChEMBL DOI: **NOT_FOUND**; Dhop Table 2: **11** / **48±4.3** mCB2 cyclase (**DIRECT**, different assay) | **Do not assign 11.2/89 to AM1710**; **`REVIEW_REQUIRED`** |
| R14-3 | Ki 6.7 as **human** CB2 Table 1 | Species fail vs curated mouse spleen | Primary Table 1 **NOT_FOUND**; ChEMBL/BindingDB same DOI: **mouse spleen** (**PARTIAL**) | Species = **not proven human**; Ki numeric remains **PARTIAL** only |
| R14-4 | GW405833 structure/SMILES resolved | Fig 1 unrecovered | Fig 1 **NOT_FOUND** | **`REVIEW_REQUIRED` / `NOT_VERIFIED`**; no SMILES |
| R14-5 | EC50 **14±2**, Emax **48±4**, CHO-K1 | NOT_FOUND | Abstract ~50% only (**DIRECT**); 14±2 / 48±4 **NOT_FOUND** | Gemini numeric package **not verified** |
| R14-6 | AM1710 & GW405833 “resolved” | Both REVIEW | This file | **Authority claim REJECTED**; both stay **`REVIEW_REQUIRED`** |

---

## 7. Parent return summary

| Item | Answer |
|---|---|
| **AM1710 verdict** | **4b = AM1710** (**DIRECT** ACS/PubMed abstract). **5a ≠ AM1710** (abstract: **5 = AM1714**). **11.2 nM / 89% ownership: NOT proven** → do not use; compound **`REVIEW_REQUIRED`**. Nearest ~11 nM = Dhop 2016 **mCB2 cyclase EC50 11 / Emax 48±4.3** (different assay/species). |
| **GW405833 verdict** | Valenzano PDF / Fig 1 / tables **unrecovered** → structure **`NOT_VERIFIED`**; EC50 **14±2** / Emax **48±4** **`NOT_VERIFIED`** → **`REVIEW_REQUIRED`**. Abstract-only: ~50% forskolin cAMP partial agonist vs CP55,940 (**DIRECT**). |
| **Path** | `results/reports/ROUND1.4_FINAL_CONTRADICTION_RESOLUTION.md` |
| **Integrity** | Create-only; Gold / prior reports / Round1 CSV **unchanged**; no git; **pipeline STOP**; Sci-Hub not used; no inference reconciliation |

---

*End ROUND1.4_FINAL_CONTRADICTION_RESOLUTION — create-only; STOP.*
