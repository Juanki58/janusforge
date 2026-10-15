# ROUND1_LEVEL0_CERTIFICATION_v1.0

**Certification date:** 2026-08-16  
**Phase:** Round 1.2 / cierre de integridad Nivel 0  
**Inputs (read-only):** `ROUND1_GOLD_CANDIDATES.md`, `ROUND1_GOLD_AUDIT_v1.0.md`, `ROUND1_ASSAY_STRATIFICATION_v1.0.md`  
**Do not modify:** Round1 CSV, GOLD MD, GOLD AUDIT, stratification, quarantine logs  
**Rule:** prefer **LEVEL0_CONFIRMED = 0** over false certification. Prior GOLD / D / CERTIFIED / VERIFIED ≠ proof. Physical primary location required.

**Reality check:** `ROUND1_GOLD_AUDIT_v1.0` has **GOLD_CONFIRMED = 0**. Stratification subsets A/B/C = empty; REVIEW = 16. Director-named “4 GOLD” (HU-308, Vicasinabin, GW405833, AM1710) are **not** GOLD_CONFIRMED in files. This certificate does **not** invent GOLD_CONFIRMED = 4.

**Scope:** re-audit of 7 focus compounds only (no dataset expansion; no docking/MD/ROC/descriptors/design).

Statuses used: **LEVEL0_CONFIRMED** | **REVIEW_REQUIRED** | **REJECTED**

---

## 1. CERTIFICATION TABLE

| Compound_ID | Final_Status | Assay_Target | Cellular_System | Assay_Format | Concentration_Metric | Efficacy_Metric | Emax_Status | SMILES_Status | Source_Location_Status | Evidence | Certification_Decision |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HU308_func_cAMP | REVIEW_REQUIRED | hCB2 (CHO stably transfected) | CHO hCB2 (Methods Cyclic AMP Assay) | forskolin-stimulated cAMP inhibition | EC50=5.57 nM (95% CL 1.68–18.5; n=5) — Round1 row still qualitative | Emax=108.6±8.4% (n=5) numeric in Results | FAIL — numeric present but reference-agonist normalization not explicit in Hanuš Results (method cites Ross [19]; not atomic “vs CP=100” in-paper) | FAIL — InChIKey `CFMRIVODIXTERW-BDTNDASRSA-N` not regenerated from primary structure V / NMR this pass | PASS (atomic) — Results cAMP paragraph, Hanuš 1999 PMC24419 | PMC24419 re-opened this pass: literal EC50/Emax recovered; Round1 qualitative preserved (no silent promote). Binding Ki 22.7±3.9 separate. SMILES + Emax-ref block Level-0 | Do not certify; prior Round1.1 CERTIFIED_WITH_SCOPE ≠ Level-0 |
| VICASINABIN_func_cAMP_hCB2 | REVIEW_REQUIRED | hCB2 | CHOK1hCB2_bgal (Methods 2.2.2) | forskolin-stimulated cAMP (Nano-TRF) | EC50=2.81±0.28 nM | NOT REPORTED (“full agonist” vs CP55940 narrative only) | FAIL — no numeric % Emax | FAIL — InChIKey `MAYZWDRUFKUGGP-VIFPVBQESA-N` not regenerated from IUPAC/X-ray this pass | PASS — Fig 3A + Results text | Frontiers HTML re-confirmed. mCB2 2.60±0.14 kept separate. Sibling β-arr Round1 ~22 vs primary 99.69±5.72 = METRIC_CONFLICT (other row) | Do not certify |
| GW405833_func_hCB2_cAMP | REVIEW_REQUIRED | hCB2 claimed (Valenzano) | human CB2 (system detail not table-verified) | cAMP (forskolin) | EC50=0.65 nM (Round1) — **not** re-found in OA abstract/table this pass | ~50% vs CP55,940 cited in abstract only | FAIL — Emax not table-locked | FAIL — InChIKey not primary-regenerated | FAIL — Valenzano 2005 full PDF/table NOT recovered; Source_Exact_Location NOT VERIFIED for 0.65 nM | EuropePMC abstract only: partial agonist ~50% vs CP55,940; Ki/EC50 table numbers pending PDF. Dhopeshwarkar 2016 mCB2 cyclase lists GW405833 inactive (Emax 0) — do not pool assays | Do not certify; PRIMARY_SOURCE_UNAVAILABLE for Round1 0.65 |
| AM1710_func_cAMP_claim | REVIEW_REQUIRED | **mCB2** (not hCB2) in Dhopeshwarkar & Mackie 2016 | HEK293 HA-mCB2 (cyclase Methods) | adenylyl cyclase / forskolin cAMP | EC50=**11** nM (95% CI 5.5–15.6) Table 2 cyclase — **not** 11.2 | Emax=48±4.3 (% forskolin inhibition; compared to CP55940 at 1 µM) | PARTIAL — numeric + CP55940 comparison present; cyclase Emax scale ≠ arrestin 100-normalized scale | FAIL — InChIKey not regenerated; Khanolkar structure not re-proven | PASS for functional EC50 location — Table 2 row AM1710, cyclase columns (PMC4959096) | Binding Ki 6.7 (Khanolkar 2007) **not** opened this pass → separate HOLD. Functional EC50 is real EC50 but **mouse CB2**. JPET 2017 intro mis-cites as “human CB2”. 11.2 nM not in primary. Arrestin EC50 4 / Emax 91% = other assay — no pooling | Do not certify as hCB2 Level-0 |
| OLORINAB_func_hCB2 | REVIEW_REQUIRED | hCB2 | PathHunter hCB2 (DiscoverX); SI catalog cell-line not re-opened | β-arrestin recruitment (NOT cAMP) | EC50=6.2 nM | Emax=106% vs CP-55,940=100 (Table 1 footnote b) | PASS — explicit numeric + same assay + ref control | FAIL — InChIKey `ACSQLTBPYZSGBA-GMXVVIOVSA-N` not regenerated from SI/scheme; ACS SI PDF unrecovered | PASS — Table 1 / Table 2 compound **6** (APD371); compound **17** ≠ APD371 | PMC5733264 re-confirmed. Round1 “typically cAMP” note = ASSAY_CONFLICT (documented). Quantitative Emax located; do not convert “full agonist” narrative → 100% | Do not certify (SMILES + SI cell-line) |
| WIN55212_ref_note | REVIEW_REQUIRED | mixed CB1/CB2 (no single assay lock) | multi | multi / reference_agonist note | no assay-locked EC50/Ki for Level-0 | N/A | FAIL | FAIL — stored InChIKey/CID not primary-regenerated for a locked assay row | FAIL — no Felder / Showalter screening primary in Round1 trail; Hua Cryo-EM = material validation only, not screening primary | Q-12 / Q11-17: forbid inventing global Ki/EC50. Directive: look Felder/Showalter only if already mentioned — **not mentioned** → REVIEW. Not REJECTED merely for missing info | Do not certify; no Level-0 functional row |
| CP55940_ref_note | REVIEW_REQUIRED | mixed CB1/CB2 (no single assay lock) | multi | multi / reference_agonist note | no assay-locked global EC50/Ki | N/A as absolute pharmacology | FAIL as compound Emax claim — appears as **assay normalization reference** (e.g. Han Table 1 footnote CP-55,940=100) | FAIL for a locked Level-0 identity row | FAIL — multi-assay literature; GtoPdb ≠ primary substitute | Distinguish pharmacological Emax 100% vs assay-normalization reference (Critical Distinctions §5). Q-12 forbids global number | Do not certify; no Level-0 functional row |

---

## 2. CERTIFIED LEVEL-0 ROWS

**None.**

LEVEL0_CONFIRMED = **0**.

No row simultaneously clears: hCB2-only identity, assay exactness, numeric concentration metric without transform, Emax rules (or documented assay-design reference exception), SMILES/InChIKey regeneration from primary (no secondary DB), and atomic Source_Exact_Location.

---

## 3. REVIEW_REQUIRED

All **7** re-audit focus compounds:

1. **HU-308 (`HU308_func_cAMP`)** — Primary Hanuš 1999 (PMC24419) **re-opened this pass**. Results literal: EC50 **5.57 nM**, Emax **108.6±8.4%**, CHO cells stably transfected with **human CB2**, forskolin cAMP. Round1 CSV remains qualitative (no silent overwrite). Blocks: (i) SMILES/InChIKey not regenerated from structure V; (ii) Emax reference-agonist normalization not atomic in-paper (cites method [19]); (iii) prefer REVIEW over promoting Round1.1 CERTIFIED_WITH_SCOPE as Level-0.

2. **Vicasinabin / RG7774 (`VICASINABIN_func_cAMP_hCB2`)** — Frontiers 2024 primary re-confirmed: hCB2 cAMP EC50 **2.81±0.28 nM**, CHOK1hCB2_bgal, Fig 3A. Blocks: numeric Emax absent (“full agonist” only); SMILES/InChIKey not regenerated. Sibling `VICASINABIN_func_barr` METRIC_CONFLICT (~22 vs 99.69±5.72) remains out of scope for this cAMP row but prevents orthogonal pairing.

3. **GW405833 (`GW405833_func_hCB2_cAMP`)** — Valenzano 2005 full PDF/table **not recovered**. Round1 EC50 0.65 nM Source_Location NOT VERIFIED. Abstract-only partial-agonist language (~50% vs CP55,940) insufficient for atomic Level-0. Do not use Dhopeshwarkar 2016 mCB2 inactivity to REJECT Valenzano hCB2 claim — different experiment; keep REVIEW.

4. **AM1710 (functional EC50 claim + binding separation)** — Binding Ki **6.7 / 360** (Khanolkar 2007): primary table **not opened** → REVIEW (not Level-0). Functional: Dhopeshwarkar & Mackie 2016 (PMC4959096) Table 2 proves EC50 **11 nM** (CI 5.5–15.6), Emax **48±4.3** for **cyclase** — metric is truly EC50, **not** Ki. Critical failure for Level-0 hCB2: Methods = HEK **mouse** CB2 (mCB2), not human. “11.2 nM” **not found** in primary (maps/internal only). JPET 2017 cites 11 nM as hCB2 — **species attribution error** relative to 2016 Methods. Arrestin values (EC50 4; Emax 91±3.6) are a separate PathHunter assay — no pooling. Distinct binding vs functional experiments are correctly separable in principle, but binding primary unopened + functional species ≠ hCB2 → **REVIEW**, not LEVEL0_CONFIRMED.

5. **APD371 / olorinab (`OLORINAB_func_hCB2`)** — Han 2017 PMC5733264 re-confirmed: compound **6** = APD371; Table 1 hCB2 β-arrestin EC50 **6.2 (106)**; footnote b Emax vs **CP-55,940 (100)**. Quantitative Emax **located** (do not invent 100% from “full agonist” prose). Blocks: SMILES/InChIKey not regenerated; SI Methods cell-line catalog not opened; Round1 assay-type note conflict documented. Compound **17** rejected as APD371 identity.

6. **WIN55,212-2 (`WIN55212_ref_note`)** — No Felder / Showalter primary in Round1 trail. Hua Cryo-EM (if cited elsewhere) validates complexed material, **not** a screening primary for Round1 Level-0. Global ref note cannot become a single certified EC50/Ki. → REVIEW_REQUIRED (missing assay-locked primary; not REJECTED solely for absence).

7. **CP-55,940 (`CP55940_ref_note`)** — Same global-ref prohibition (Q-12). Where CP appears as **100** in other papers (e.g. Han Table 1), that is **assay normalization reference**, not a certified absolute pharmacological Emax row for CP itself. → REVIEW_REQUIRED.

---

## 4. REJECTED

**None** among the 7 re-audit focus compounds.

REJECTED reserved for cases with enough evidence that a datum **must not** be used (e.g. proven wrong identity, invented transform, or binding sold as functional under false attribution). Missing primary / incomplete SMILES / wrong-species attribution → **REVIEW_REQUIRED**, not REJECTED.

---

## 5. CRITICAL DISTINCTIONS

1. **Prior labels ≠ Level-0:** Round1 Evidence_Tag D, Round1.1 CERTIFIED / CERTIFIED_WITH_SCOPE, and Dataset/GOLD placement do **not** equal LEVEL0_CONFIRMED. Stratification empty subsets stand.

2. **Director “4 GOLD” vs files:** HU-308, Vicasinabin, GW405833, AM1710 are **not** GOLD_CONFIRMED in `ROUND1_GOLD_AUDIT_v1.0` (GOLD_CONFIRMED=0). This certificate keeps all four at REVIEW_REQUIRED.

3. **AM1710 binding vs functional:** Ki 6.7 nM (Khanolkar lineage) ≠ EC50 11 nM (Dhopeshwarkar & Mackie 2016 Table 2 cyclase). Do not conflate. EC50 is genuinely an EC50, but in **mCB2** HEK cyclase — fails hCB2-only Level-0 gate. “11.2 nM” is unverified.

4. **Emax rules:** Never promote from “full agonist” prose (vicasinabin). Olorinab Emax 106% is explicit vs CP-55,940=100 in the **same** β-arrestin table — still blocked by SMILES/SI. HU-308 Emax 108.6% is numeric but normalization reference not atomic in Hanuš Results → Emax_Status FAIL for Level-0.

5. **CP-55,940 Emax 100% vs assay reference:** Footnote “CP-55,940 (100)” in Han Table 1 is **normalization of test-compound Emax**, not a Level-0 certified absolute Emax claim for CP as a standalone row.

6. **No pathway pooling:** cAMP ≠ GTPγS ≠ β-arrestin ≠ Ca2+/ERK. Olorinab 6.2 nM is β-arrestin only. Vicasinabin cAMP and β-arr are separate. AM1710 cyclase vs arrestin are separate (and cyclase is mCB2).

7. **WIN material vs screening:** Structural/cryo-EM presence of WIN does not certify a Round1 screening potency row. Felder/Showalter not in current Round1 primary trail → REVIEW.

8. **GW405833 cross-paper conflict risk:** Valenzano (hCB2 partial agonist narrative) vs Dhopeshwarkar 2016 (mCB2 cyclase inactive) must not be pooled; insufficient Valenzano table recovery → REVIEW both for Level-0 use of Round1 0.65 nM.

---

## 6. PRIMARY SOURCES

| # | Source | Form inspected this pass | What was verified / not verified |
|---|---|---|---|
| 1 | Hanuš et al. 1999 HU-308 — DOI 10.1073/pnas.96.25.14228 / PMC24419 | PMC HTML full text | Ki 22.7±3.9; CB1 >10 µM; cAMP EC50 **5.57 nM**; Emax **108.6±8.4%**; CHO hCB1/hCB2 Methods. SMILES not regenerated |
| 2 | Han et al. 2017 APD371 — DOI 10.1021/acsmedchemlett.7b00396 / PMC5733264 | PMC HTML Tables 1–2 + footnotes | Cmpd **6**=APD371; hCB2 β-arr EC50 **6.2 (106)**; CP-55,940=100; PathHunter. SI PDF not opened; InChIKey not regenerated |
| 3 | RG7774/vicasinabin — DOI 10.3389/fphar.2024.1426446 | Frontiers HTML OA | hCB2 cAMP **2.81±0.28**; mCB2 **2.60±0.14**; β-arr **99.69±5.72**; CHOK1hCB2_bgal; no numeric cAMP Emax % |
| 4 | Dhopeshwarkar & Mackie 2016 — DOI 10.1124/jpet.116.232561 / PMC4959096 | PMC HTML Methods + Table 2 | AM1710 cyclase EC50 **11** (5.5–15.6), Emax **48±4.3** on **HEK-mCB2**; arrestin separate; CP55940 reference; GW405833 cyclase Emax 0 (mCB2) |
| 5 | Dhopeshwarkar et al. 2017 Janus — DOI 10.1124/jpet.116.236539 | Publisher HTML (intro + CB1 panels) | Cites AM1710 EC50 11 nM / Emax 48% to 2016 paper but states “human CB2” — **conflicts with 2016 Methods (mCB2)**. CB1 Janus panels ≠ hCB2 Level-0 agonist row |
| 6 | Valenzano et al. 2005 GW405833 — PMID 15814101 | EuropePMC **abstract only** | Partial agonist ~50% vs CP55,940 in abstract; full PDF/table for Ki 3.92 / EC50 0.65 **not recovered** |
| 7 | Khanolkar et al. 2007 AM1710 — DOI 10.1021/jm070441u | **Not opened** (binding table pending) | Ki 6.7 / 360 remain unverified at primary table for Level-0 |
| 8 | Felder / Showalter WIN primaries | **Not in Round1 trail; not opened** | WIN stays REVIEW |
| 9 | `ROUND1_GOLD_CANDIDATES.md` + `ROUND1_GOLD_AUDIT_v1.0.md` + stratification (read-only) | Local MD | GOLD_CONFIRMED=0; GOLD rows=2 both previously demoted to REVIEW; homogeneous subsets empty |

---

## 7. FINAL COUNTS

| Bucket | N |
|---|---|
| **LEVEL0_CONFIRMED** | **0** |
| **REVIEW_REQUIRED** | **7** |
| **REJECTED** | **0** |

| Context | N |
|---|---|
| Focus compounds re-audited | 7 |
| Stratification homogeneous subsets A/B/C (unchanged) | 0 / 0 / 0 |
| Invented GOLD_CONFIRMED = 4 | **NO** |

**Parent summary line:** LEVEL0_CONFIRMED=0 / REVIEW_REQUIRED=7 / REJECTED=0. None confirmed because every focus compound fails at least one hard gate (SMILES regeneration, Emax atomic rules, hCB2-only, or unrecovered primary table). Integrity preserved: no silent metric transforms, no pathway pooling, no promotion of Director’s four names to certified Level-0.

---

## 8. AUDIT LIMITATIONS

1. ACS SI PDF for Han 2017 (olorinab cell-line catalog / structure → InChIKey) unrecovered this pass.  
2. Valenzano 2005 full PDF paywalled / not on disk — Round1 GW405833 0.65 nM remains location-unverified.  
3. Khanolkar 2007 AM1710 binding table not opened — binding Ki cannot be Level-0 confirmed even separately from functional.  
4. SMILES/InChIKey regeneration from primary structures deliberately **not** performed via secondary databases (§16). Fail → REVIEW.  
5. Round1 CSV / GOLD MD / GOLD AUDIT / quarantine logs **not modified**. No new molecules added except reading Dhopeshwarkar 2016 as the concrete primary for the AM1710 EC50 11/11.2 discrepancy.  
6. No docking, MD, descriptors, ROC, classification models, or molecular design performed.  
7. Homogeneous assay subsets remain empty; this certificate does not reopen stratification promotion.

---

*End ROUND1_LEVEL0_CERTIFICATION_v1.0 — create-only; stop.*
