# ROUND1_RECONCILIATION_v1.0

**Date:** 2026-08-16  
**Phase:** Round 1.2 / cierre de contradicciones adversariales  
**Scope:** Primary-evidence reconciliation of adversarial claims for 7 focus compounds only.  
**Rule:** Prefer **REVIEW_REQUIRED** over false **CONFIRMED_***. Critical fields for CONFIRMED_* require Evidence_Tag **D** with atomic primary location. No dataset expansion; no docking/MD/ROC/descriptors/design.  
**Inputs (read-only):** `ROUND1_GOLD_CANDIDATES.md`, `ROUND1_GOLD_AUDIT_v1.0.md`, `ROUND1_LEVEL0_CERTIFICATION_v1.0.md`, `ROUND1_ASSAY_STRATIFICATION_v1.0.md`, Round1 CSV, OA primaries under `data/papers/` + fetches listed in §8.

**Statuses used (only):** `CONFIRMED_CAMP` | `CONFIRMED_GTPS` | `REVIEW_REQUIRED` | `REJECTED`

---

## 1. FINAL CLASSIFICATION

| Compound | Adversarial claim (to test) | Final_Status | Assay locked | Species / system | Metric / Emax | SMILES / identity | Evidence | Decision rationale |
|---|---|---|---|---|---|---|---|---|
| CP-55,940 | CONFIRMED homogeneous hCB2 / cAMP / intact cells | **REVIEW_REQUIRED** | No Round1 assay-locked row (`CP55940_ref_note` only) | Mixed / multi; Dhop 2016 cyclase = **mCB2** HEK | No single hCB2 cAMP EC50/Emax certified for Level-0 | Not primary-regenerated for a locked row | N/P | Global reference ≠ CONFIRMED_CAMP; Felder 1995 abstract lacks WIN/CP numeric EC50/Emax lock for this gate |
| HU-308 | CONFIRMED homogeneous hCB2 / cAMP / intact cells | **REVIEW_REQUIRED** | forskolin cAMP (Hanuš 1999) | **hCB2** CHO stably transfected (Methods) | EC50 **5.57 nM** (95% CL 1.68–18.5); Emax **108.6±8.4%** — numeric yes; **CP=100 normalization not atomic** in Results | InChIKey `CFMRIVODIXTERW-BDTNDASRSA-N` **not** regenerated from Structure V / Scheme 1 this pass | D (pharmacology) / N (SMILES) | Hard fails: SMILES + Emax-reference atomicity → prefer REVIEW over false CONFIRMED_CAMP |
| Vicasinabin / RG7774 | CONFIRMED homogeneous hCB2 / cAMP / intact cells | **REVIEW_REQUIRED** | forskolin cAMP Nano-TRF | **hCB2** **CHOK1hCB2_bgal** (DiscoveRx) — **CHO, not HEK293** | EC50 **2.81±0.28 nM** (Fig 3A + Results); mCB2 **2.60±0.14** separate; Emax = “full agonist” vs CP55940 **without numeric %** | InChIKey `MAYZWDRUFKUGGP-VIFPVBQESA-N` not regenerated from IUPAC/X-ray (CCDC 22814444) | D (EC50/system) / N (Emax%/SMILES) | Numeric Emax absent + SMILES → no CONFIRMED_CAMP |
| GW405833 | REVIEW_REQUIRED (chem ID / SMILES PRIORITY #1) | **REVIEW_REQUIRED** | cAMP claim Round1 EC50 0.65 nM | Abstract: rat + human CB2 binding; system/table for 0.65 **not** recovered | Abstract: partial agonist **~50%** vs CP55,940 forskolin cAMP; **EC50 0.65 not in abstract** | **SMILES NOT VERIFIED** from Valenzano Fig 1 / Table 2 | N (primary PDF) | Valenzano 2005 full PDF/tables **not recovered** (EuropePMC HAS_FT=0). No secondary DB as final SMILES authority |
| AM1710 | REVIEW_REQUIRED (GTPγS vs cAMP) | **REVIEW_REQUIRED** (not CONFIRMED_GTPS) | Khanolkar GTPγS claim **not** primary-verified; Dhop 2016 Table 2 = **cyclase** | Dhop cyclase: **HEK-mCB2** (mouse), not hCB2 CHO membranes | Dhop Table 2: cyclase EC50 **11** nM (CI 5.5–15.6), Emax **48±4.3**; arrestin EC50 **4**, Emax **91±3.6**. **11.2 not found**. Khanolkar abstract: AM1710 = **4b** (not 5a); **5 = AM1714** | Binding SMILES Round1 not re-proven from Khanolkar structure this pass | P/N | Adversarial “Table 2 compound 5a GTPγS 11.2±1.8 / Emax 89±3%” **not located** in opened primaries → cannot CONFIRMED_GTPS; never place in CAMP_HOMOGENEOUS |
| APD371 / olorinab | REVIEW_REQUIRED (missing quantitative Emax) | **REVIEW_REQUIRED** | **β-arrestin** PathHunter (Han 2017 Table 1) — **not cAMP** | PathHunter hCB2 (DiscoverX); SI cell-line catalog not re-opened | EC50 **6.2 nM**, Emax **106%** vs CP-55,940=100 (footnote b) — Emax **is** explicit for β-arrestin cmpd **6** | InChIKey `ACSQLTBPYZSGBA-GMXVVIOVSA-N` not regenerated from SI/scheme; stereo Table 1 **(S,S)** | D (β-arr Emax) / N (SMILES/cAMP) | Quantitative Emax located for β-arrestin; **does not qualify CAMP_HOMOGENEOUS**; do not convert “full agonist” prose → 100% for any missing cAMP Emax |
| WIN 55,212-2 | REVIEW_REQUIRED (primary insufficiently located) | **REVIEW_REQUIRED** | No Round1 assay-locked functional row (`WIN55212_ref_note`) | Felder 1995: CHO/AtT-20 hCB1/hCB2 (abstract); Dhop WIN row = **mCB2** | Felder abstract: WIN higher affinity CB2 vs CB1; cAMP rank-order narrative — **no numeric WIN EC50/Emax** located | Not primary-regenerated for locked assay row | N | Hua 2020 Cryo-EM rejected as screening primary. Felder abstract insufficient for CONFIRMED_*. Showalter 1996 PMID 8831752 is **not** a WIN characterization primary |

---

## 2. CAMP_HOMOGENEOUS

**Criterion (simultaneous):** explicit **hCB2** + forskolin **cAMP** (intact cells) + identified cellular system + explicit EC50 + explicit numeric Emax (or unequivocal same-assay reference normalization) + primary Source_Exact_Location + SMILES/identity D from primary (no secondary DB final authority). Never GTPγS / β-arrestin.

| Compound_ID | Status | Notes |
|---|---|---|
| — | **EMPTY (N = 0)** | No compound clears all gates |

**Consistency check on adversarial “CONFIRMED” trio:**

| Compound | hCB2 | System | Assay | EC50 | Emax | SMILES | Outcome |
|---|---|---|---|---|---|---|---|
| CP-55,940 | No locked hCB2 cAMP row | Fail | Fail as standalone | Fail | Fail as absolute Emax row | Fail | **Hard fail → REVIEW_REQUIRED** (not CONFIRMED_CAMP) |
| HU-308 | Pass (CHO hCB2) | Pass | Pass (forskolin cAMP) | Pass (5.57 nM) | Partial — numeric % present; **CP=100 not atomic** | Fail (not regenerated from Structure V) | **Hard fail → REVIEW_REQUIRED** |
| Vicasinabin | Pass | Pass (**CHO** CHOK1hCB2_bgal; not HEK293) | Pass | Pass (2.81±0.28) | Fail (narrative “full” only) | Fail | **Hard fail → REVIEW_REQUIRED** |

**Near-miss (documented, not promoted):** HU-308 Hanuš Results cAMP paragraph is the strongest pharmacologic near-miss; blocked by SMILES regeneration + Emax-reference atomicity under CONFIRMED_* rules.

---

## 3. GTPS_FUNCTIONAL

**Criterion:** explicit **hCB2** + **[³⁵S]GTPγS** + identified membrane prep + EC50 + explicit Emax + primary location + identity D. **Never** pool with cellular cAMP.

| Compound_ID | Status | Notes |
|---|---|---|
| — | **EMPTY (N = 0)** | No CONFIRMED_GTPS |

**AM1710 gate (adversarial path to CONFIRMED_GTPS):**

| Check | Result |
|---|---|
| Khanolkar 2007 full PDF / Table 2 opened? | **NO** (ACS paywalled this pass; EuropePMC HAS_FT=0) |
| Abstract compound ID | AM1710 = **4b** (9-methoxy); compound **5** = **AM1714** (9-hydroxy). Adversarial “compound **5a**” **conflicts** with abstract numbering |
| Abstract GTPγS EC50 11.2±1.8 / Emax 89±3% vs CP? | **Not present** in abstract |
| Nearest verified functional EC50 “11 nM” | Dhopeshwarkar & Mackie 2016 PMC4959096 **Table 2** row AM1710: cyclase EC50 **11** (CI 5.5–15.6), Emax **48±4.3** on **HEK-mCB2** — **not** GTPγS; **not** hCB2 CHO membranes; **not** 11.2; Emax **≠** 89% |
| Place in CAMP_HOMOGENEOUS? | **NEVER** (even if GTPγS later confirmed) |

→ **REVIEW_REQUIRED** (cannot CONFIRMED_GTPS without Khanolkar primary table).

---

## 4. REVIEW_REQUIRED

All **7** focus compounds:

1. **CP-55,940** — Round1 `CP55940_ref_note` only; Q-12 forbids inventing a global Ki/EC50. Appears as **assay normalization reference** (e.g. Han Table 1 CP-55,940=100; Vicasinabin “full vs CP55940”) — that is **not** a CONFIRMED_CAMP absolute pharmacology row for CP itself. Dhop 2016 Table 2 CP55940 cyclase EC50 **3** nM / Emax **57±0.5** is **mCB2**, not hCB2 homogeneous.

2. **HU-308** — Hanuš 1999 PMC24419 / EuropePMC PDF render re-opened: CHO **human CB2**, forskolin cAMP, EC50 **5.57 nM**, Emax **108.6±8.4%**. Blocks: (i) SMILES/InChIKey not regenerated from Structure V; (ii) Emax reference-agonist normalization not atomic vs CP in Results (method cites Ross [19]); (iii) Round1 CSV still stores qualitative functional row (no silent promote). Prefer REVIEW over false CONFIRMED_CAMP.

3. **Vicasinabin / RG7774** — Frontiers 2024 OA: hCB2 cAMP EC50 **2.81±0.28 nM**, CHOK1hCB2_bgal, Fig 3A; mCB2 **2.60±0.14** kept separate; β-arr sibling **99.69±5.72** (Round1 ~22 = METRIC_CONFLICT on other row). Blocks: no numeric % Emax; SMILES/InChIKey not regenerated. System is **CHO**, not HEK293.

4. **GW405833** — Valenzano 2005 Neuropharmacology full PDF/Fig 1/Table 2 **not recovered**. Abstract supports partial agonist ~50% vs CP55,940 forskolin cAMP and high-affinity rat/human CB2 binding, but **does not** locate Round1 EC50 **0.65 nM** or prove structure→SMILES. See §5. Dhop 2016 mCB2 cyclase lists GW405833 Emax **0** — different experiment; do not pool to REJECT Valenzano claim → keep REVIEW.

5. **AM1710** — Khanolkar binding Ki 6.7 / 360 lineage **not** table-verified this pass. Functional “11 nM” resolves to Dhop 2016 **mCB2 cyclase** (not Khanolkar GTPγS; not 11.2). JPET 2017 secondary attribution of 11 nM as “human CB2” **conflicts** with 2016 Methods (mCB2). Adversarial GTPγS 11.2/89% claim **unverified**. → REVIEW_REQUIRED; **not** CONFIRMED_GTPS; **not** CAMP_HOMOGENEOUS.

6. **APD371 / olorinab** — Han 2017 PMC5733264: compound **6** = APD371; Table 1 hCB2 β-arrestin **6.2 (106)**; footnote b Emax vs CP-55,940 (100). Compound **17** ≠ APD371. Assay = **β-arrestin**, not cAMP (Round1 “typically cAMP” = ASSAY_CONFLICT). Blocks for CONFIRMED_CAMP: wrong assay class + SMILES not regenerated + SI cell-line catalog unrecovered. Emax **is** verified for β-arrestin — still REVIEW for this reconciliation’s CAMP/GTPS states.

7. **WIN 55,212-2** — No Felder/Showalter full-text table with species/system/assay/conc/EC50/Emax locked for Round1. Felder 1995 PubMed abstract (PMID 7565624) confirms WIN preference for CB2 binding and cAMP coupling narrative without numeric WIN EC50/Emax. Showalter 1996 (PMID 8831752) is a different chemistry paper, not WIN screening primary. Hua Cryo-EM rejected. Dhop WIN mCB2 cyclase EC50 **16** / Emax **40±1.2** is not a substitute characterization primary for CONFIRMED_*. → REVIEW_REQUIRED (missing locked primary; not REJECTED solely for absence).

**REJECTED among focus compounds:** **0** (insufficient evidence to prove a datum must be discarded as false identity / invented transform; unresolved → REVIEW).

---

## 5. GW405833_CHEMICAL_IDENTITY_AUDIT

**Target primary:** Valenzano et al. 2005, *Neuropharmacology* 48:658–672, DOI 10.1016/j.neuropharm.2004.12.008, PMID 15814101.

### Step-by-step (no memory SMILES; no secondary DB as final authority)

| Step | Question | Finding this pass | Tag |
|---|---|---|---|
| 1 | Was Valenzano 2005 full PDF recovered? | **NO.** EuropePMC search `EXT_ID:15814101 AND HAS_FT:y` → **hitCount=0**. Publisher full text not OA. Local `data/papers/` has no Valenzano PDF. | N |
| 2 | Fig 1 structure inspected? | **NO** — figure body unavailable without PDF. | N |
| 3 | Nomenclature GW405833 = L-768242? | Abstract names **GW405833** as selective CB2 agonist; synonym L-768242 appears in later OA papers citing Valenzano/Gallant — **not** used here as Valenzano-proof of structure. | P (name continuity only) |
| 4 | Table 2 compound identity / numbers? | **NOT VERIFIED.** Round1 stores Ki 3.92 / 4772 and EC50 0.65 nM with Evidence_Tag D historically — **Source_Exact_Location not re-found** in abstract or any opened table. | N |
| 5 | N-indole substituent (propyl / ethyl / morpholinoethyl / other)? | **Cannot determine from Valenzano primary this pass.** Abstract does not describe the substituent. | N |
| 6 | Salt form? | **NOT VERIFIED** in Valenzano primary this pass. | N |
| 7 | Does Table 2 = drawn Fig 1 structure? | **NOT VERIFIED** (neither Fig 1 nor Table 2 recovered). | N |
| 8 | Round1 stored structure string | Round1 CSV row `GW405833_bind_hCB2` stores InChIKey `FSFZRNZSZYDVLI-UHFFFAOYSA-N` **and** SMILES `CC1=C(C2=C(N1C(=O)C3=C(C(=CC=C3)Cl)Cl)C=CC(=C2)OC)CCN4CCOCC4`. | Stored claim only |
| 9 | Regenerate / confirm SMILES from Valenzano Fig 1? | **Forbidden without primary figure.** No memory reconstruction. No PubChem/GtoPdb as final authority. | **SMILES NOT VERIFIED** |
| 10 | Non-authority corroboration (logged only) | Dhopeshwarkar 2016 Table 1 footnote (PMC4959096) and Li et al. 2017 Fig 1 caption (PMC5502377) **name** GW405833 as `1-(2,3-dichlorobenzoyl)-5-methoxy-2-methyl-3-[2-(4-morpholinyl)ethyl]-1H-indole` citing Gallant 1996 / Valenzano 2005. Useful as **pointer**, **not** final Valenzano chemical-identity proof. | I (informational) |
| 11 | Functional pharmacology from abstract only | Partial agonist: **~50%** reduction of forskolin-mediated cAMP vs full agonist CP55,940; binds rat and human CB2 with high affinity. | P (abstract) |
| 12 | Unequivocal resolution? | **NO.** | — |

**Outcome:** **SMILES NOT VERIFIED** + Source_Exact_Location for Round1 0.65 nM **NOT VERIFIED** → **REVIEW_REQUIRED**. No “more plausible” SMILES fix applied.

---

## 6. CONTRADICTION_LOG

| ID | Claim A | Claim B | Resolution |
|---|---|---|---|
| C1 | Adversarial: CP / HU-308 / Vicasinabin = CONFIRMED homogeneous hCB2 cAMP | LEVEL0_CERTIFICATION + this reconciliation: CONFIRMED_CAMP = 0 | **A rejected.** Hard fails (no locked row / SMILES / Emax%) → all three **REVIEW_REQUIRED** |
| C2 | Adversarial / maps: AM1710 EC50 **11.2** nM as Khanolkar Table 2 GTPγS compound **5a**, Emax **89±3%** | Khanolkar abstract: AM1710 = **4b**; **5** = AM1714. Dhop 2016 Table 2: AM1710 cyclase EC50 **11** (not 11.2), Emax **48±4.3**, **mCB2**, **not** GTPγS | **B wins where verified.** Adversarial GTPγS 11.2/89%/5a **not found** in opened primaries → REVIEW; no CONFIRMED_GTPS |
| C3 | Prior maps / JPET 2017: AM1710 EC50 11 nM as **human** CB2 | Dhopeshwarkar & Mackie 2016 Methods: HEK **mouse** CB2 cyclase | **2016 Methods control species.** 2017 intro species attribution is a **cross-paper error** relative to 2016 primary |
| C4 | Round1 / some notes: olorinab 6.2 nM “typically cAMP” | Han 2017 Table 1 header: **β-arrestin** EC50 6.2 (106) | **Primary β-arrestin.** ASSAY_CONFLICT documented; number kept under correct assay; **not** CAMP_HOMOGENEOUS |
| C5 | Director / adversarial: APD371 missing Emax | Han Table 1 compound **6**: Emax **106%** vs CP-55,940=100 | **Emax located** for β-arrestin; “missing Emax” claim is **false for β-arrestin**. Still REVIEW because assay ≠ cAMP and SMILES/SI incomplete |
| C6 | Director “compound 17” = APD371 | Han: APD371 = compound **6**; compound **17** is a different CF3 analog | **Compound 17 rejected** as APD371 identity |
| C7 | Vicasinabin Round1 β-arr `~22 nM` | Frontiers Fig 3B / Results **99.69±5.72 nM** | METRIC_CONFLICT on barr row; cAMP 2.81±0.28 unchanged; no silent overwrite |
| C8 | Valenzano narrative: GW405833 hCB2 partial agonist ~50% | Dhop 2016: GW405833 mCB2 cyclase Emax **0** | **Do not pool.** Different species/assay; insufficient Valenzano table → REVIEW both for Level-0 use of Round1 0.65 |
| C9 | Adversarial: Vicasinabin system “HEK293?” | Frontiers Methods 2.2.2: **CHOK1hCB2_bgal** | **CHO** (DiscoveRx). HEK claim unsupported for this cAMP row |
| C10 | WIN via Hua 2020 Cryo-EM as screening primary | Directive + this pass | **Rejected.** Structural complex ≠ Round1 functional EC50/Emax primary |
| C11 | CP Emax “100%” in other papers’ footnotes | Absolute CONFIRMED_CAMP row for CP | Footnote CP=100 is **normalization of test ligands**, not certified absolute Emax for CP as a compound row |

No silent correction of Round1 CSV / GOLD MD / LEVEL0 / stratification performed.

---

## 7. FINAL COUNTS

| Bucket | N |
|---|---|
| **CONFIRMED_CAMP** | **0** |
| **CONFIRMED_GTPS** | **0** |
| **REVIEW_REQUIRED** | **7** |
| **REJECTED** | **0** |

| Integrity checks | Result |
|---|---|
| Adversarial CONFIRMED trio (CP, HU-308, Vicasinabin) upheld? | **NO** — all demoted/held at REVIEW_REQUIRED |
| GW405833 SMILES unequivocal from Valenzano? | **NO** — **SMILES NOT VERIFIED** |
| AM1710 CONFIRMED_GTPS via Khanolkar Table 2? | **NO** — primary table unrecovered; 11 nM maps to mCB2 cyclase |
| Molecule universe expanded? | **NO** |
| Docking / MD / ROC / design performed? | **NO** |
| Prefer REVIEW over false CONFIRMED? | **YES** |

**Parent summary line:** CONFIRMED_CAMP=**0** / CONFIRMED_GTPS=**0** / REVIEW_REQUIRED=**7** / REJECTED=**0**. GW405833 → SMILES NOT VERIFIED + REVIEW. AM1710 → not CONFIRMED_GTPS (Khanolkar GTPγS unverified; 11 nM = mCB2 cyclase). Integrity preserved: no rubber-stamp of adversarial CONFIRMED claims.

---

## 8. SOURCES ACTUALLY INSPECTED

| # | Source | Form | What was verified / not verified |
|---|---|---|---|
| 1 | Hanuš et al. 1999 HU-308 — DOI 10.1073/pnas.96.25.14228 / PMC24419 | EuropePMC PDF render + text extract | Ki 22.7±3.9; CB1 >10 µM; CHO hCB1/hCB2 Methods; cAMP EC50 **5.57 nM**; Emax **108.6±8.4%**; Structure V named in Scheme 1 — SMILES **not** regenerated |
| 2 | Han et al. 2017 APD371 — DOI 10.1021/acsmedchemlett.7b00396 / PMC5733264 | EuropePMC PDF render | Cmpd **6**=APD371; Table 1 β-arrestin hCB2 **6.2 (106)** vs CP-55,940=100; PathHunter; cmpd **17**≠APD371; ACS SI PDF **not** retrieved (403) |
| 3 | RG7774 / vicasinabin — DOI 10.3389/fphar.2024.1426446 | Frontiers HTML OA + PDF | Methods 2.2.2 cAMP **CHOK1hCB2_bgal**; Results/Fig 3A EC50 **2.81±0.28** (mCB2 **2.60±0.14**); Fig 3B β-arr **99.69±5.72**; “full agonist” **sans %**; (S) X-ray CCDC 22814444; InChIKey not regenerated |
| 4 | Valenzano et al. 2005 GW405833 — PMID 15814101 | EuropePMC **abstract only** (HAS_FT=0); PubMed XML abstract | Partial agonist ~50% vs CP55,940 forskolin cAMP; rat+human CB2 binding claimed; **Fig 1 / Table 2 / EC50 0.65 / structure→SMILES NOT recovered** |
| 5 | Khanolkar et al. 2007 AM1710 — DOI 10.1021/jm070441u / PMID 18038967 | EuropePMC / PubMed **abstract only** (HAS_FT=0); ACS SI 403 | AM1710 = **4b**; **5**=AM1714; CB2 agonists claimed; **no GTPγS Table 2 numbers**; binding Ki table **not** opened |
| 6 | Dhopeshwarkar & Mackie 2016 — DOI 10.1124/jpet.116.232561 / PMC4959096 | PMC HTML Methods + Table 2 | HEK-**mCB2** cyclase; AM1710 EC50 **11** / Emax **48±4.3**; arrestin 4 / 91±3.6; GW405833 cyclase Emax **0**; CP55940 / WIN / HU308 rows on **mCB2**; GW405833 IUPAC in footnote (informational only) |
| 7 | Li et al. 2017 GW405833 in vivo — PMC5502377 | PMC HTML Fig 1 caption | Structure figure + naming citing Gallant/Valenzano — **not** Valenzano primary proof |
| 8 | Felder et al. 1995 — PMID 7565624 | PubMed abstract XML only | WIN higher affinity CB2 vs CB1; cAMP functional coupling narrative; **no numeric WIN EC50/Emax** for CONFIRMED_* |
| 9 | Showalter et al. 1996 — PMID 8831752 | PubMed title/metadata | **Not** a WIN 55,212-2 characterization primary (different chemistry title) |
| 10 | Round1 reports (GOLD MD, GOLD AUDIT, LEVEL0, ASSAY STRATIFICATION, Round1 CSV) | Local read-only | LEVEL0_CONFIRMED=0; stratification A/B/C empty; Round1 stored GW SMILES/InChIKey; CP/WIN ref notes |

**Attempted / blocked (logged):** ACS SI for Han 2017 and Khanolkar (403); Valenzano/Khanolkar full PDF OA (unavailable); Sci-Hub **not used**.

---

*End ROUND1_RECONCILIATION_v1.0 — create-only; stop.*
