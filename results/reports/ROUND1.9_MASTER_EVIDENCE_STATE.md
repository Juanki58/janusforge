# ROUND 1.9 — MASTER EVIDENCE STATE

**Date:** 2026-08-17  
**Role:** Research documentalist — consolidate Round 1 documentary state only  
**Inputs (read-only, exclusive):** Round 1.x reports under `results/reports/` (listed §0)  
**Output (create-only):** this file  
**Hard prohibitions honored:** no new bibliographic search; no new candidates; no models/docking/QSAR/classification; no git modifications; no reinterpretation; no silent contradiction correction; no promotion by plausibility; **PIPELINE = STOP**

**Classification rule:** `CONFIRMED` only if identity **and** relevant quantitative datum are documentarily backed by recovered primary. Prefer `REVIEW_REQUIRED` / `NOT_VERIFIED` over false confirmation. Do **not** convert qualitative language (“full agonist”, “approximately 50%”) into numeric percentages.

**Metric separation (mandatory):** binding Ki ≠ functional EC50 ≠ measured Emax ≠ Emax-as-normalization ≠ structural identity ≠ experimental system.

---

## 0. Source inventory (reports consulted)

| Report | Role in this consolidation |
|---|---|
| `ROUND1_GOLD_CANDIDATES.md` | Initial GOLD=2 / REVIEW=16 / Rejected=37; assay locks |
| `ROUND1B_GOLD_CANDIDATES.md` | Companion counts aligned to GOLD MD |
| `ROUND1_GOLD_AUDIT_v1.0.md` | **GOLD_CONFIRMED = 0**; both Dataset/GOLD rows → REVIEW |
| `ROUND1_ASSAY_STRATIFICATION_v1.0.md` | Homogeneous subsets A/B/C = **empty** |
| `ROUND1_LEVEL0_CERTIFICATION_v1.0.md` | **LEVEL0_CONFIRMED = 0**; 7 focus compounds REVIEW |
| `ROUND1_RECONCILIATION_v1.0.md` | CONFIRMED_CAMP=0; CONFIRMED_GTPS=0; adversarial claims demoted |
| `ROUND1.3_PRIMARY_SOURCE_RECOVERY.md` | Primary recovery matrix for focus-7 |
| `ROUND1.3_CROSS_VALIDATION.md` | Gemini “resolved” packages rejected; pipeline STOP |
| `ROUND1.4_FINAL_CONTRADICTION_RESOLUTION.md` | AM1710 4b≠5a; 11.2/89 not owned; GW 14±2/48±4 not verified |
| `ROUND1.5_AM1710_PRIMARY_OWNERSHIP.md` | Khanolkar Tables 1–2 **NOT_FOUND**; abstract identity only |
| `ROUND1.6_GW405833_PRIMARY_RESOLUTION.md` | Valenzano PDF/Fig.1/tables **NOT_FOUND** |
| `ROUND1.7_GW405833_FUNCTIONAL_TEXT_EXTRACT.md` | Literal 14±2 / 48±4 **NOT_FOUND** in abstract |
| `ROUND1.8_GW405833_CONSOLIDATION.md` | Abstract-confirmed identity/partial/~50%; numbers/structure unverified |
| `ROUND1.1_CERTIFICATION_QUARANTINE.md` | Quarantine Q11-* historical holds |
| `CB2_Experimental_Master_Dataset_v1.0_Round1.1_CERTIFICATION.md` | Historical CERTIFIED/HOLD labels only — **≠** Round 1.9 Gold (ownership marked) |

Prior Round reports **not overwritten**.

---

## 1. MASTER EVIDENCE TABLE

Statuses in **Evidence status**: `CONFIRMED` | `REVIEW_REQUIRED` | `NOT_VERIFIED` (claim sought, not recovered).  
EC50 / Emax cells show **documentary values as recorded in reports**, tagged for ownership — **not** promoted to Gold.

| Compound | Identity | Primary source | Assay | Species/receptor | EC50 | Emax | Evidence status | Numerical ownership | Structure status | Confidence | Blocking reason |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **AM1710** | Abstract: **4b = AM1710** (9-methoxy); **5 = AM1714**; **5a ≠ AM1710** (DIRECT abstract). Gemini 5a = REJECTED (R1.4/R1.5) | Khanolkar 2007 DOI `10.1021/jm070441u` (pages **6493–6500**); abstract only. Tables 1–2 **NOT_FOUND** (R1.5). Dhop 2016 PMC4959096 = separate paper (mix-check only) | Claimed Khanolkar GTPγS: **NOT_VERIFIED**. Dhop: forskolin **cyclase/cAMP** (not GTPγS) | Claimed hCB2 GTPγS: **NOT_VERIFIED**. Dhop Methods: **HEK-mCB2** (mouse) | Adversarial **11.2±1.8 nM**: **NOT_FOUND** in Khanolkar. Dhop cyclase **11** nM (CI 5.5–15.6) — different assay/species; **≠ 11.2** | Adversarial **89±3%**: **NOT_FOUND**. Dhop cyclase **48±4.3**; arrestin **91±3.6** (separate assay) | **REVIEW_REQUIRED** | **11.2±1.8 / 89±3%**: ownership **NOT assigned** to AM1710 (R1.4–1.5). Binding Ki 6.7/360: PARTIAL/HOLD — primary Table 1 unrecovered. Do **not** promote to Gold | SMILES/structure from Khanolkar drawing: **NOT VERIFIED** | High (tables missing) | Khanolkar Tables 1–2 unrecovered; no literal ownership of 11.2/89; no Subset B GTPγS lock; Dhop ≠ Khanolkar |
| **GW405833** | Name **GW405833** DIRECT in Valenzano abstract. Synonym L-768242 **not** in abstract. Correct DOI **`10.1016/j.neuropharm.2004.12.008`** (wrong DOI `…2005.01.010` = Pertwee) | Valenzano 2005 *Neuropharmacology* 48:658–672; **abstract only**. PDF/Fig.1/tables **NOT_FOUND** (R1.6–1.8) | Forskolin-mediated **cAMP**; **partial agonist** (abstract) | Abstract: **rat and human CB2** binding + cAMP partial agonism. **CHO-K1** Methods: **NOT_RECOVERED** | Historical Gemini **14±2 nM**: **NOT_VERIFIED**. Round1 CSV **0.65 nM**: also **NOT_FOUND** in abstract | Abstract **approximately 50%** vs CP55,940 (**qualitative only**). Exact **48±4%**: **NOT_VERIFIED** (≠ approx. 50%) | **REVIEW_REQUIRED** | Confirmed (abstract): identity + DOI + partial agonist + forskolin cAMP + ~50% vs CP55,940. **Not owned:** 14±2, 48±4, 0.65 | Fig.1 / SMILES: **NOT_VERIFIED** / **REVIEW_REQUIRED** | High | Full PDF unrecovered; numeric EC50/Emax not literal; structure/CHO-K1 Methods unlocked |
| **CP-55,940** | Named reference agonist; Round1 `CP55940_ref_note` only | No Round1 assay-locked characterization primary. Soethoudt 2017 SI Suppl Tables 3–4 recovered as **later** profiling (R1.3) — not promoted to Gold | Multi-assay reference (cAMP / GTPγS / normalization). Footnote CP=100 elsewhere = **normalization**, not absolute Emax row for CP | Mixed / multi; Soethoudt human CHO hCB2 Nano-TRF (SI) documented but not Level-0 Gold row | Soethoudt SI T4 hCB2 cAMP **pEC50 10.33±0.09** (historical recovery; **not** Gold). Dhop mCB2 cyclase EC50 **3** nM — different species. Global single Ki/EC50 **forbidden** (Q-12) | Soethoudt SI T4 **98±1** vs 10 µM CP55940 (self-ref normalization). Do **not** invent absolute Emax=100% as Gold row | **REVIEW_REQUIRED** | No Gold-safe single assay-locked ownership. Soethoudt numbers = documentary recovery only; Round1 ref_note remains unlocked | Structure→SMILES for locked row: **NOT VERIFIED** | High | No Level-0 / Gold assay-locked row; Q-12 global-number ban; GOLD_CONFIRMED=0 lineage |
| **HU-308** | Named HU-308; Hanuš Structure V / Scheme 1 described — SMILES regen **not** completed | Hanuš 1999 DOI `10.1073/pnas.96.25.14228` / PMC24419 (Results cAMP paragraph DIRECT). Soethoudt SI = separate lab (do not pool) | Forskolin-stimulated **cAMP** inhibition | **hCB2** CHO stably transfected (Hanuš Methods) | Hanuš **5.57 nM** (95% CL 1.68–18.5; n=5) — DIRECT Results. Round1 CSV still **qualitative** (no silent promote). Soethoudt pEC50 **8.53±0.06** = different study | Hanuš **108.6±8.4%** (n=5) — numeric DIRECT; **CP=100 normalization not atomic** in Results (method cites Ross [19]). Soethoudt **98±1** vs CP — separate | **REVIEW_REQUIRED** | Hanuš EC50/Emax pharmacologically recovered but **not** Gold/Level-0 certified (SMILES + Emax-ref atomicity). Binding Ki **22.7±3.9** separate (≠ functional) | InChIKey `CFMRIVODIXTERW-BDTNDASRSA-N` **not regenerated** from Structure V | High | SMILES regen fail; Emax reference-agonist atomicity fail; GOLD_CONFIRMED=0 |
| **Vicasinabin / RG7774** | IUPAC (S)-…; CAS 1433361-02-4; X-ray CCDC 22814444 cited in Frontiers primary | Frontiers 2024 DOI `10.3389/fphar.2024.1426446` / PMC11272598 | **cAMP** forskolin Nano-TRF (Fig 3A). Sibling **β-arrestin** PathHunter (Fig 3B) = **separate assay** | **hCB2** **CHOK1hCB2_bgal** (CHO, **not** HEK293). mCB2 **2.60±0.14** kept separate | hCB2 cAMP **2.81±0.28 nM** (DIRECT). β-arr Round1 **~22 nM** vs primary **99.69±5.72 nM** — METRIC_CONFLICT on barr row | cAMP: narrative **“full agonist”** vs CP55940 — **no numeric %** → do **not** invent 100%. β-arr Emax: NOT REPORTED in Results | **REVIEW_REQUIRED** | cAMP EC50 owned to Fig 3A + Results; numeric cAMP Emax **not owned**. β-arr EC50 conflict: Round1 vs primary both recorded — no silent overwrite | InChIKey `MAYZWDRUFKUGGP-VIFPVBQESA-N` **not regenerated** from IUPAC/X-ray | High | Missing numeric Emax %; SMILES regen; β-arr METRIC_CONFLICT blocks orthogonal lock |
| **APD371 / Olorinab** | Compound **6** = APD371 (Han Table 1/2). Compound **17** ≠ APD371 (REJECTED as identity). Stereo Table 1 **(S,S)** | Han 2017 DOI `10.1021/acsmedchemlett.7b00396` / PMC5733264. ACS SI PDF **unrecovered** | **β-arrestin** PathHunter (**NOT** cAMP). Round1 “typically cAMP” = ASSAY_CONFLICT (documented) | **hCB2** PathHunter DiscoverX; SI cell-line catalog **not opened** | Table 1: **6.2 nM** (β-arrestin) | Table 1: **106%** vs CP-55,940=100 (footnote b) — **β-arrestin only**. Do **not** assign Emax=100% from “full agonist” prose for any missing cAMP Emax. **cAMP Emax: NOT_VERIFIED** | **REVIEW_REQUIRED** | β-arrestin 6.2 / 106 owned to Table 1 cmpd 6. Not Subset A cAMP. Normalization CP=100 ≠ certified CP absolute Emax | InChIKey `ACSQLTBPYZSGBA-GMXVVIOVSA-N` **not regenerated** from SI/scheme | High | SMILES/SI cell-line incomplete; wrong assay class for cAMP Gold |
| **WIN 55,212-2** | Named WIN55,212-2; Round1 `WIN55212_ref_note` | Felder 1995 PMID 7565624 — **abstract only** (numeric tables NOT_FOUND). Showalter 1996 ≠ WIN primary. **Hua 2020 Cryo-EM rejected** as screening primary. Soethoudt SI = later profiling (not historical substitute) | Multi / unlocked. Soethoudt: separate cAMP and GTPγS | Felder: CHO/AtT-20 hCB1/hCB2 (abstract narrative). Soethoudt: CHO DiscoveRx / CHOK1 membranes | Felder: **no numeric WIN EC50**. Soethoudt SI T4 cAMP pEC50 **9.50±0.09**; GTPγS **7.96±0.04**. Dhop mCB2 cyclase **16** — different species | Soethoudt cAMP **98±1**; GTPγS **49±7** (assay-dependent). Dhop **40±1.2** mCB2 | **REVIEW_REQUIRED** | Historical Felder quantitative primary **NOT_VERIFIED**. Soethoudt numbers recovered but **not** promoted as Gold substitute for historical primary | Structure→SMILES for locked row: **NOT VERIFIED** | High | Historical numeric primary missing; Hua not substitute; no assay-locked Gold row |
| **LEI-101** | Named **hydrochloride** in Mukhopadhyay 2016; stored InChIKey free-base `APLLNJWPLUIBCG-UHFFFAOYSA-N` | Mukhopadhyay 2016 DOI `10.1111/bph.13338` / PMC4728411 Table 1 + Methods | **Separate rows:** β-arrestin; [³⁵S]GTPγS; cAMP (footnote a → van der Stelt 2011 — provenance REVIEW) | hCB2 PathHunter / CHOK1hCB2R_bgal membranes (barr/GTP). cAMP system via footnote a | β-arr pEC50 **7.0±0.3**; GTPγS **6.6±0.2**; cAMP **8.0±0.1** (keep as pEC50; do not convert) | β-arr **41±6%**; GTPγS **65±8%** vs CP55940. cAMP Emax **NOT REPORTED** (“full” narrative ≠ %) | **REVIEW_REQUIRED** | Table 1 numbers D for barr/GTP; salt/identity blocks Gold. cAMP provenance cross-paper | Salt HCl vs free-base InChIKey unresolved (§16); no secondary DB fix | High | Structural salt ambiguity; cAMP footnote provenance; GOLD demotion |
| **URB447** | Diarylpyrrole URB447; LoVerme 2009 | LoVerme 2009 DOI `10.1016/j.bmcl.2008.12.059` | Binding **IC50** (≠ Ki ≠ EC50). Functional: **mCB2** cAMP qualitative @ 1 µM; rat CB1 GTPγS arm separate | Binding: rCB1 / hCB2. Functional CB2: **mCB2** HEK-293 (**not** hCB2) | Binding IC50 313±72 (rCB1) / 41±23 (hCB2). Functional: **no EC50** | Functional Emax: **NOT REPORTED** | **REVIEW_REQUIRED** | IC50 binding owned with scope; no hCB2 quantitative functional EC50/Emax for Gold | InChIKey retained; not a Gold structure lock for hCB2 agonist row | High | Species (mCB2); qualitative only; IC50≠Ki≠EC50 |
| **Qiu 14 / 15 / 16 / 20 / 24** | Challenge / blinded set | Qiu SI / docking lineage (Round1 Rejected) | Qualitative / ND / docking I — **not** calibration Gold | — | — | — | **Outside calibration / blinded challenge** (not REVIEW promotion path) | Excluded from GOLD and from REVIEW Gold path (`ROUND1_GOLD_CANDIDATES.md`) | — | — | Blinded challenge — out of Round 1 Gold calibration |

**Historical note (Round 1.1 CERTIFICATION ownership):** Round 1.1 labels such as `CERTIFIED` / `CERTIFIED_WITH_SCOPE` / `HOLD` for HU-308, RG7774, LEI-101, URB447, etc. are **historical certification-layer statuses**. They do **not** equal Round 1.9 `CONFIRMED` / Gold. Downstream audits (`GOLD_AUDIT`, `LEVEL0`, reconciliation, R1.3–1.8) set **GOLD_CONFIRMED = 0** / **LEVEL0_CONFIRMED = 0**.

---

## 2. DISCREPANCIES (no vote / no “most plausible”)

| ID | Claim A | Claim B | Documentary status | Conservative decision |
|---|---|---|---|---|
| D1 | Gemini: AM1710 = compound **5a**, GTPγS EC50 **11.2±1.8**, Emax **89±3%**, hCB2 | Cursor R1.3–1.5: AM1710 = **4b**; **5 = AM1714**; 11.2/89 **NOT_FOUND** in Khanolkar; tables unrecovered | Abstract DIRECT for 4b/5; Tables 1–2 NOT_FOUND; Dhop 11 / 48±4.3 = mCB2 cyclase (different paper) | **REVIEW_REQUIRED**. Do **not** assign 11.2/89 to AM1710. Identity 4b locked from abstract only |
| D2 | JPET 2017: AM1710 EC50 11 nM as **human** CB2 | Dhop 2016 Methods: HEK **mouse** CB2 | Both documented; 2016 Methods control species | Species attribution error in 2017 intro relative to 2016 primary; keep mCB2 for Dhop row |
| D3 | Gemini: GW405833 EC50 **14±2**, Emax **48±4**, CHO-K1, SMILES resolved | R1.6–1.8: Valenzano PDF unrecovered; abstract ~50% only; 14±2/48±4/Fig.1 **NOT_FOUND** | Abstract DIRECT for partial/~50%; numbers/structure NOT_VERIFIED | **REVIEW_REQUIRED**. Retain historical 14±2/48±4 as UNVERIFIED; do not equate ~50% → 48±4 |
| D4 | Round1 CSV GW405833 EC50 **0.65 nM** | Gemini **14±2 nM** | Neither locked to recovered Valenzano table/abstract | Both **NOT_VERIFIED**; no averaging / pick-one |
| D5 | Valenzano: GW405833 hCB2 partial ~50% | Dhop 2016: GW405833 mCB2 cyclase Emax **0** | Different species/assay | **Do not pool**; both remain out of Gold lock |
| D6 | Round1: olorinab 6.2 nM “typically cAMP” | Han Table 1: **β-arrestin** 6.2 (106) | ASSAY_CONFLICT documented | Keep number under **β-arrestin**; not Subset A cAMP |
| D7 | Director “compound 17” = APD371 | Han: APD371 = compound **6** | DIRECT Table 1/2 | Compound **17** rejected as APD371 |
| D8 | Vicasinabin β-arr Round1 **~22 nM** | Frontiers Fig 3B **99.69±5.72 nM** | METRIC_CONFLICT | Both recorded; no silent overwrite; barr row REVIEW |
| D9 | Adversarial: CP / HU-308 / Vicasinabin = CONFIRMED homogeneous hCB2 cAMP | GOLD_AUDIT / LEVEL0 / Reconciliation: CONFIRMED / GOLD = **0** | Hard fails (locked row / SMILES / Emax%) | All three **REVIEW_REQUIRED** |
| D10 | ROUND1B Valenzano DOI `…2005.01.010` | Correct `…2004.12.008` | Wrong DOI = Pertwee paper | Typo logged; use correct DOI only |
| D11 | Khanolkar pages **4496–4506** | PubMed/ACS **6493–6500** | Citation error | Use 6493–6500; same DOI |

---

## 3. END SECTIONS

### A. GOLD CONFIRMED

**N = 0**

No compound simultaneously clears: recovered primary identity **and** recovered primary quantitative datum **and** structure/assay locks required by Round 1 Gold / Level-0 / Subset A–B gates.

| Prior Dataset/GOLD row (historical) | Later audit disposition |
|---|---|
| `OLORINAB_func_hCB2` | Demoted → **REVIEW_REQUIRED** (`ROUND1_GOLD_AUDIT_v1.0`) |
| `VICASINABIN_func_cAMP_hCB2` | Demoted → **REVIEW_REQUIRED** (same) |

Honest empty set: **GOLD CONFIRMED = 0**.

---

### B. REVIEW_REQUIRED — full list with blocking reason

| # | Compound | Blocking reason (documentary) |
|---|---|---|
| 1 | **AM1710** | Khanolkar Tables 1–2 unrecovered (R1.5); 11.2±1.8 / 89±3% ownership NOT_FOUND; no hCB2 GTPγS Subset B lock; Dhop 11 nM = mCB2 cyclase only |
| 2 | **GW405833** | Valenzano PDF/Fig.1/tables unrecovered; EC50 14±2 & Emax 48±4 & Round1 0.65 NOT_VERIFIED; SMILES NOT_VERIFIED; CHO-K1 Methods not abstract-locked (R1.6–1.8) |
| 3 | **CP-55,940** | No Round1 assay-locked Level-0/Gold row; Q-12 forbids global Ki/EC50; Soethoudt SI recovery not promoted |
| 4 | **HU-308** | SMILES not regenerated from Structure V; Emax CP=100 atomicity not in Hanuš Results; Round1 qualitative preserved |
| 5 | **Vicasinabin / RG7774** | Numeric cAMP Emax % absent (“full” only); SMILES not regenerated; β-arr METRIC_CONFLICT (~22 vs 99.69±5.72) |
| 6 | **APD371 / Olorinab** | SMILES/SI cell-line incomplete; assay = β-arrestin not cAMP; cAMP Emax NOT_VERIFIED |
| 7 | **WIN 55,212-2** | Felder historical numeric tables NOT_VERIFIED; Hua Cryo-EM not screening primary; no locked Gold row |
| 8 | **LEI-101** | HCl salt vs free-base InChIKey; cAMP provenance via van der Stelt footnote a; Gold demotion |
| 9 | **URB447** | Functional CB2 = mCB2 qualitative only; binding = IC50 ≠ Ki/EC50; no hCB2 quantitative functional Gold row |

**REVIEW count (calibration focus compounds above) = 9**  
(Aligned lineage: focus-7 Level0/Reconciliation = 7 REVIEW; LEI-101 + URB447 retained REVIEW per existing reports; Qiu excluded from this count as challenge/outside calibration.)

**Qiu 14/15/16/20/24:** outside calibration / blinded challenge set — **not** listed as REVIEW for Gold promotion.

Homogeneous assay subsets (Stratification): cAMP = **0**; GTPγS = **0**; orthogonal Gi/β-arrestin = **0**.

---

### C. UNRESOLVED PRIMARY CONTRADICTIONS — still open only

| ID | Open contradiction | Why still open |
|---|---|---|
| U1 | AM1710: who owns literal **11.2±1.8 / 89±3%** in Khanolkar Table 2 (if present)? | Tables 1–2 **never recovered** (R1.5) — ownership cannot close |
| U2 | GW405833: Valenzano table cells for **14±2 / 48±4** and/or Round1 **0.65**; Fig.1 structure | PDF/Fig.1/tables **never recovered** (R1.6–1.8) |
| U3 | Vicasinabin β-arrestin: Round1 **~22 nM** vs primary **99.69±5.72 nM** | Both documented; Round1 not overwritten; no silent correction allowed |
| U4 | Olorinab Round1 assay note “cAMP” vs Han Table 1 **β-arrestin** | ASSAY_CONFLICT documented; CSV not silently fixed |
| U5 | AM1710 JPET 2017 “human CB2” vs Dhop 2016 **mCB2** Methods | Cross-paper species mismatch remains on record |
| U6 | GW405833 Valenzano partial ~50% vs Dhop mCB2 cyclase Emax **0** | Different experiments; Valenzano table still missing — cannot pool or reject |

**Closed (not open):** Gemini AM1710 = **5a** (REJECTED vs abstract **4b**); APD371 = compound **17** (REJECTED vs compound **6**); wrong Valenzano DOI `…2005.01.010`; wrong Khanolkar page range 4496–4506.

---

### D. NUMBERS NOT SAFE FOR GOLD

All of the following appear in prior Round 1 reports and **must not** be used as Gold:

| Number / claim | Why unsafe for Gold |
|---|---|
| AM1710 **11.2±1.8 nM** / **89±3%** | NOT_FOUND in Khanolkar primary tables (R1.4–1.5) |
| AM1710 Dhop cyclase **11 nM** / **48±4.3** | Real in Dhop Table 2 but **mCB2**, not hCB2 Level-0/Gold |
| AM1710 arrestin **4** / **91±3.6** | Separate assay; not Gold package |
| AM1710 binding Ki **6.7 / 360** | Primary Khanolkar Table 1 unrecovered (HOLD/PARTIAL only) |
| GW405833 **14±2 nM** / **48±4%** | NOT_VERIFIED in Valenzano recovered text (R1.6–1.8) |
| GW405833 Round1 **0.65 nM** / Ki **3.92 / 4772** | Source location NOT VERIFIED without Valenzano PDF |
| GW405833 abstract **~50%** | Qualitative only — **not** numeric Emax for Gold |
| Vicasinabin cAMP **2.81±0.28 nM** without numeric Emax | EC50 recovered but Emax % absent + SMILES block → REVIEW not Gold |
| Vicasinabin β-arr **~22 nM** | Conflicts with primary **99.69±5.72** |
| Vicasinabin “full agonist” → **100%** | Forbidden conversion (§17) |
| HU-308 **5.57 nM** / **108.6±8.4%** | Near-miss; SMILES + Emax-ref atomicity block Level-0/Gold |
| HU-308 Soethoudt pEC50 **8.53±0.06** / **98±1** | Different study — do not pool as Gold substitute |
| Olorinab **6.2 nM** / **106%** as **cAMP** Gold | Values are **β-arrestin**; SMILES/SI incomplete |
| Olorinab “full agonist” → **100%** cAMP Emax | Forbidden; cAMP Emax NOT_VERIFIED |
| CP-55,940 any **global** Ki/EC50 / absolute Emax=100 row | Q-12; footnote CP=100 is normalization only |
| WIN Felder “rank order” without numbers | No numeric EC50/Emax lock |
| WIN Soethoudt pEC50/Emax set | Later profiling — not historical primary substitute for Gold |
| WIN Hua 2020 Cryo-EM | Material/structure ≠ screening EC50/Emax primary |
| LEI-101 Table 1 pEC50/Emax set | Salt/identity + cAMP provenance block Gold |
| URB447 IC50 **313±72 / 41±23** as Ki or EC50 | Metric = IC50 binding only |
| URB447 “inhibits at 1 µM” as EC50/Emax | Qualitative mCB2 only |
| Any Round 1.1 `CERTIFIED*` label as Gold | Historical layer ≠ GOLD_CONFIRMED |
| Qiu 14/15/16/20/24 any challenge metrics | Outside calibration / blinded |

---

### E. PIPELINE STATUS

**STOP**

- No computational work authorized.  
- No new candidate search authorized.  
- No docking / QSAR / classification / modeling.  
- No Gold promotion from this consolidation.  
- Prior Round reports untouched; only this file created.

---

## 4. Parent return summary

| Field | Value |
|---|---|
| **Path** | `results/reports/ROUND1.9_MASTER_EVIDENCE_STATE.md` |
| **GOLD CONFIRMED count** | **0** |
| **REVIEW count** | **9** (AM1710, GW405833, CP-55,940, HU-308, Vicasinabin/RG7774, APD371/Olorinab, WIN 55,212-2, LEI-101, URB447) |
| **Top blocking themes** | (1) Unrecovered primary PDFs/tables (Khanolkar Tables 1–2; Valenzano Fig.1/tables); (2) Missing numeric ownership / Emax atomicity; (3) Structure/SMILES not primary-regenerated; (4) Assay/species mismatches (β-arr≠cAMP; mCB2≠hCB2; Ki≠EC50); (5) Historical METRIC/ASSAY conflicts preserved without silent fix |
| **Pipeline** | **STOP** confirmed |

---

NO COMPUTATIONAL WORK AUTHORIZED.  
NO NEW CANDIDATE SEARCH AUTHORIZED.  
PIPELINE REMAINS STOP.
