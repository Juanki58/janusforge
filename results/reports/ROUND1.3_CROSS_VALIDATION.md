# ROUND 1.3 — CROSS-VALIDATION OF GEMINI ADVERSARIAL COUNTER-AUDIT

**Date:** 2026-08-16  
**Rule:** Do **not** accept Gemini conclusions by authority. Every numeric / identity / assay claim tested against primary sources (or documented as unrecovered).  
**Create-only deliverable.** Gold dataset / Round1 CSV **not modified**. No docking / QSAR / structural inference / commits.  
**Pipeline status after this file:** **STOP**.

---

## 0. Gemini report recovery

| Search | Result |
|---|---|
| `results/reports/*ADVERSARIAL*`, `*COUNTER-AUDIT*`, `*Gemini*`, `*ROUND1.3*` | **NOT FOUND** |
| `ROUND1.3_PRIMARY_SOURCE_RECOVERY.md` | **NOT FOUND** |
| Workspace / agent-transcripts string hunt for `ADVERSARIAL COUNTER-AUDIT REPORT (ROUND 1.3)` | **NOT FOUND** as a standalone artifact |

**Working assumption:** Gemini claims validated below are those stated in the Round 1.3 mission brief (AM1710 / GW405833 “resolved”; APD371 / WIN still under review; specific numeric/structural assertions listed per compound). Citation of “Gemini claim” = that brief, not a recovered Gemini PDF/MD.

**Read-only inputs used:** `ROUND1_RECONCILIATION_v1.0.md`, Round1 CSV, local OA extracts under `data/papers/_recon_tmp/`, PubMed abstracts, EuropePMC/Unpaywall metadata, ChEMBL document activities for DOI `10.1021/jm070441u` (tagged **PARTIAL** — curated deposit, not primary page image).

---

## 1. Evidence tags

| Tag | Meaning |
|---|---|
| **DIRECT** | Quote / number / identity read from primary full text, table, figure, or PubMed/EuropePMC abstract of the cited primary |
| **PARTIAL** | Corroborating curated deposit (ChEMBL/BindingDB) of the same DOI, or abstract-only fragment insufficient for full chain |
| **INFERRED** | Cross-paper pointer only (never final authority for CONFIRMED_*) |
| **NOT_FOUND** | Claimed datum not located in opened sources |

---

## 2. PRIORITY 1 — AM1710 (Khanolkar et al. 2007)

**Cited primary:** Khanolkar AD et al., *J Med Chem* **50:6493–6500** (2007), DOI `10.1021/jm070441u`, PMID 18038967.  
**Note:** Mission brief pages “4496–4506” do **not** match PubMed/ChEMBL pagination (**6493–6500**). Same DOI/PMID.

**Primary PDF / Table 1 / Table 2:** Unpaywall marks green OA via BindingDB DOI `10.7270/q2736qn9`, but that resolves to BindingDB entry HTML — **not** the ACS article PDF. ACS SI fetch → 403. EuropePMC `HAS_FT` unavailable. → Primary tables **not opened** this pass.

### Checklist vs Gemini claims

| Gemini claim | Independent check | Evidence | Verdict |
|---|---|---|---|
| AM1710 = compound **5a** | PubMed/EuropePMC/ChEMBL abstract: *“9-methoxy analog **4b (AM1710)**”*; *“9-hydroxyl analog **5 (AM1714)**”* | **DIRECT** (abstract) | **FAIL** — conflicts prior Cursor recon (4b) and primary abstract. **5a ≠ AM1710** |
| Table 1 Ki = **6.7 nM** | Numeric **6.7** widely attributed to this paper; ChEMBL doc `CHEMBL1138340` deposits Ki **6.7 nM** for CHEMBL266712 (AM1710 SMILES match) as *“Displacement of [3H]CP-55940 from CB2 receptor in **mouse spleen membranes**”* | **PARTIAL** (ChEMBL of this DOI); primary Table 1 page **NOT_FOUND** | Numeric **plausible**; species in curated deposit = **mouse**, **not** human |
| Table 2 for **5a**: EC50 = **11.2 ± 1.8 nM** | No EC50 **11.2** in ChEMBL activities for this document; abstract has no EC50. Nearest OA functional “11 nM” = Dhopeshwarkar & Mackie 2016 Table 2 cyclase (below) | **NOT_FOUND** in Khanolkar primary/abstract/ChEMBL | **FAIL** |
| Emax = **89 ± 3%** | ChEMBL for AM1710 from this DOI: GTPγS **Activity 50.0%** at **1 µM** (not Emax curve). No 89±3. (Later Molecules 2019 cites **E(max)=89%** for **AM4346**, not AM1710 — informational only.) | **NOT_FOUND** for AM1710/Khanolkar | **FAIL** |
| Assay = **[³⁵S]GTPγS** | ChEMBL deposits GTPγS **and** forskolin-cAMP agonist activity for this DOI on **mouse spleen membranes**; GTPγS values are **% at 1 µM**, not EC50/Emax | **PARTIAL** | Paper class includes GTPγS; Gemini’s **EC50/Emax GTPγS** package **not** recovered |
| Receptor = **human hCB2** | Abstract does not state human recombinant CB2 for the Ki. ChEMBL/BindingDB for this DOI: **Mus musculus** spleen CB2 | **PARTIAL** (curated) + abstract silent on hCB2 | **FAIL** vs Gemini hCB2 claim |
| **5b** has distinct Gemini-cited value | Without Gemini report text + without primary Table 2, cannot map “5b” | **NOT_FOUND** | Unverified |
| No mix with mCB2 / other compound / other table | **Mix risk HIGH:** Dhop 2016 Table 2 AM1710 cyclase EC50 **11** (CI 5.5–15.6), Emax **48 ± 4.3** on **HEK-mCB2**; arrestin Emax **91 ± 3.6**. Gemini **11.2 / 89** resembles a composite of nearby numbers, not a located Khanolkar cell | **DIRECT** (Dhop PMC4959096 Table 2) | Contamination risk documented |

**DIRECT abstract quotes (identity):**

> “Optimal receptor subtype selectivity of 490-fold and subnanomolar affinity for the CB2 receptor is exhibited by a 9-hydroxyl analog **5 (AM1714)**, while the 9-methoxy analog **4b (AM1710)** had a 54-fold CB2 selectivity.”

**ChEMBL quote (AM1710 Ki system — PARTIAL, same DOI):**

> “Displacement of [3H]CP-55940 from CB2 receptor in mouse spleen membranes” — Ki **6.7 nM** (CHEMBL266712 / document CHEMBL1138340).

**Dhop 2016 Table 2 quote (do not substitute for Khanolkar):**

> AM1710 | cyclase EC50 **11** | Emax **48 ± 4.3** | arrestin EC50 **4** | Emax **91 ± 3.6** — Methods: HEK cells stably expressing **mouse** CB2.

### AM1710 Final status

**`REVIEW_REQUIRED` / NOT `CONFIRMED_SUBSET_B_GTPGAMMAS`**

Hard fails for Subset B gate: (i) identity **5a** false vs abstract **4b**; (ii) EC50 **11.2±1.8** and Emax **89±3%** **NOT_FOUND** in Khanolkar; (iii) curated Ki system is **mCB2 spleen membranes**, not proven **hCB2**; (iv) primary Table 1/2 PDF unrecovered.

**Integrity rule:** Even if a future Khanolkar GTPγS table is recovered, **never** merge AM1710 into Master **cAMP** Subset A.

---

## 3. PRIORITY 2 — GW405833 (Valenzano et al. 2005)

**Cited primary:** Valenzano KJ et al., *Neuropharmacology* 48:658–672 (2005), DOI `10.1016/j.neuropharm.2004.12.008`, PMID 15814101.

**Primary PDF / Fig 1 / Table 2:** Unpaywall `is_oa=false`; EuropePMC full text unavailable; no local Valenzano PDF. → **NOT recovered**.

### Checklist vs Gemini claims

| Gemini claim | Independent check | Evidence | Verdict |
|---|---|---|---|
| Identity GW405833 / **L-768,242** | Valenzano PubMed abstract names **GW405833** only. Synonym **L768242 / L-768,242** appears in later OA (e.g. Li et al. 2017 PMC5502377 Fig 1 caption citing Gallant/Valenzano) | **DIRECT** (name GW405833 in abstract); synonym **INFERRED** (secondary) | Name continuity only — not Valenzano Fig 1 proof |
| Fig 1 structure / N1 substituent / chemical name | Fig 1 body unavailable without PDF | **NOT_FOUND** | Cannot lock N1 (morpholinoethyl vs other) from Valenzano primary |
| Table 2 | Not recovered | **NOT_FOUND** | — |
| EC50 = **14 ± 2 nM** | Not in Valenzano abstract. Vendor/secondary literature commonly cites **0.65 nM** (also **not** in abstract). No OA primary table with **14±2** located | **NOT_FOUND** in primary | **FAIL** as Valenzano-locked value |
| Emax = **48 ± 4%** | Abstract: *“partial agonist (**approximately 50%** reduction of forskolin-mediated cAMP production compared to … CP55,940)”*. Exact **48±4** **not** in abstract. Note: **48±4.3** is Dhop AM1710 cyclase Emax — mix risk | **PARTIAL** (~50% abstract); **48±4** **NOT_FOUND** | Exact Gemini Emax **not** primary-verified |
| hCB2, CHO-K1, cAMP | Abstract: binds **rat and human CB2**; forskolin **cAMP** partial agonism vs CP55,940. **CHO-K1** not stated in abstract | **PARTIAL** | System cell line not abstract-locked |
| Proposed SMILES matches Fig 1 | Round1 stores `CC1=C(C2=C(N1C(=O)C3=C(C(=CC=C3)Cl)Cl)C=CC(=C2)OC)CCN4CCOCC4` / InChIKey `FSFZRNZSZYDVLI-UHFFFAOYSA-N`. **Cannot** accept as chemically plausible; Valenzano Fig 1 not inspected | **NOT_FOUND** (primary figure) | **SMILES NOT VERIFIED** from Valenzano |

**DIRECT abstract quote:**

> “For the first time, we show that GW405833 selectively binds both rat and human CB2 receptors with high affinity, where it acts as a partial agonist (**approximately 50%** reduction of forskolin-mediated cAMP production compared to the full cannabinoid agonist, CP55,940).”

### GW405833 Final status

**`REVIEW_REQUIRED` / NOT `CONFIRMED_SUBSET_A_cAMP`**

Structure **not** unequivocally proven from Valenzano Fig 1. EC50 **14±2** **not** recovered. Exact Emax **48±4** **not** recovered. No secondary DB as final SMILES authority.

---

## 4. PRIORITY 3 — Revalidation of previously “CONFIRMED” trio

Mission: re-check CP-55,940, HU-308, RG7774 only against primaries (Soethoudt 2017 / Ullmer-Frontiers 2024 preferred where claimed).

### 4.1 CP-55,940

| Chain element | Finding | Evidence |
|---|---|---|
| Compound | Reference agonist in Round1 (`CP55940_ref_note`) — not a locked Level-0 agonist row | Round1 CSV |
| Receptor / species / system | Soethoudt 2017 (*Nat Commun*): multi-assay panel on **hCB2** and mouse CBRs; CP55940 used as full-agonist normalizer (10 µM) across pathways | **DIRECT** (Soethoudt extract) |
| Assay | GTPγS, cAMP, β-arrestin, pERK, GIRK — **not** a single Subset A row | **DIRECT** |
| EC50 / Emax | No single global hCB2 cAMP EC50/Emax certified as Gold row this pass; Round1 forbids inventing one number | **NOT_FOUND** as locked Level-0 row |
| Structure | Not regenerated for a CONFIRMED_* row | — |

**New contradiction vs Gemini “resolved homogeneous” framing:** Soethoudt itself notes CP55940 may be **biased toward cAMP** vs other pathways — reinforces **not** treating CP as a trivial absolute Emax=100 compound row.

**Final:** **`REVIEW_REQUIRED`** (reference / multi-assay — not Subset A Gold row).

### 4.2 HU-308

| Chain element | Finding | Evidence |
|---|---|---|
| Compound | HU-308, Hanuš et al. 1999 PNAS; Scheme 1 / Structure named | **DIRECT** (`hanus_epmc_extract.txt`) |
| Receptor / species / system | CHO cells stably transfected with **human CB2** (and CB1 for contrast) | **DIRECT** |
| Assay | Forskolin-stimulated **cAMP** | **DIRECT** |
| EC50 | **5.57 nM** (95% CL 1.68–18.5; n=5) | **DIRECT** |
| Emax | **108.6 ± 8.4%** (n=5); CP=100 normalization **not** atomic in Results paragraph | **DIRECT** (numeric); reference atomicity **PARTIAL** |
| Structure → SMILES | Scheme 1 / Structure V described; InChIKey **not** regenerated this pass | **PARTIAL** pharmacology / **NOT_FOUND** SMILES regen |
| Soethoudt 2017 | Consensus tool agonist; full agonist language in GTPγS/cAMP panels — complementary profiling, not a replacement primary for Hanuš EC50 | **DIRECT** (profiling) |

**Quote (Hanuš Results):**

> “In CB2-transfected cells, HU-308 inhibited forskolin-stimulated cAMP … EC50 value of **5.57 nM** … mean Emax value of **108.6 ± 8.4%**.”

**Final:** **`REVIEW_REQUIRED`** (near-miss Subset A; blocked by SMILES regen + Emax-reference atomicity under CONFIRMED_* rules). **No new numeric contradiction** vs Round1 reconciliation.

### 4.3 RG7774 / Vicasinabin (Ullmer / Frontiers 2024)

| Chain element | Finding | Evidence |
|---|---|---|
| Compound | (S)-RG7774 / vicasinabin; X-ray CCDC cited | **DIRECT** (Frontiers extract) |
| Receptor / species / system | **CHOK1hCB2_bgal** (DiscoveRx) — **CHO**, not HEK293 | **DIRECT** Methods 2.2.2 |
| Assay | Forskolin **cAMP** Nano-TRF | **DIRECT** |
| EC50 | hCB2 **2.81 ± 0.28 nM**; mCB2 **2.60 ± 0.14 nM** (keep separate) | **DIRECT** |
| Emax | Narrative **“full agonist”** vs CP55940 — **no numeric % Emax** | **DIRECT** (absence of %) |
| Structure → SMILES | IUPAC + X-ray; InChIKey not regenerated | **PARTIAL** / **NOT_FOUND** regen |

**Final:** **`REVIEW_REQUIRED`** for Subset A (missing numeric Emax % + SMILES regen). β-arrestin sibling EC50 **99.69 ± 5.72 nM** remains a separate assay (Round1 ~22 nM = prior METRIC_CONFLICT on barr row only).

---

## 5. PRIORITY 4 — APD371 / olorinab (Han 2017)

**Primary:** Han S et al., *ACS Med Chem Lett* 2017, DOI `10.1021/acsmedchemlett.7b00396`, PMC5733264. SI PDF fetch failed (placeholder/403).

| Check | Result | Evidence |
|---|---|---|
| Identity | Compound **6** = APD371; compound **17** ≠ APD371 | **DIRECT** Table 1/2 + text |
| Explicit numeric Emax | **Yes** — Table 1: hCB2 **6.2 (106)**; footnote: Emax relative to **CP-55,940 (100)** | **DIRECT** |
| Assay class | Header: **β-arrestin** EC50 — **not cAMP** | **DIRECT** |
| Exact reference | CP-55,940 = 100 in same table footnote | **DIRECT** |
| Convert “full agonist” → 100% for missing cAMP Emax? | **Forbidden** — not done | — |
| cAMP Emax in main text? | Mentions pathway differences historically for other series; **no** Subset A cAMP EC50/Emax row certified for APD371 this pass | **NOT_FOUND** for Subset A |

**Quote:**

> Table 1 header: “β-arrestin, EC50 (nM)” … “**6 (S,S)- … 6.2 (106)**” … “Intrinsic activity (Emax) was determined relative to CP-55,940 (100).”

**Final:** **`REVIEW_REQUIRED`**. Emax **106%** is real for **β-arrestin PathHunter** — document as **non–Subset A**. Do **not** place in Subset A cAMP Gold.

---

## 6. PRIORITY 5 — WIN 55,212-2

| Source | What was recovered | Sufficiency for CONFIRMED_* |
|---|---|---|
| **Felder et al. 1995** PMID 7565624 | Abstract: CHO / AtT-20 transfected CB1/CB2; WIN higher affinity CB2 vs CB1; rank-order mirrored in **cAMP** inhibition; **no numeric WIN EC50/Emax** | **Insufficient** — **DIRECT** abstract, metrics **NOT_FOUND** |
| **Showalter et al. 1996** PMID 8831752 | Title: synthesis of a phenolic-OH-lacking cannabinoid with high CB2 affinity — **not** a WIN 55,212-2 characterization primary | **Reject as WIN primary** |
| Hua 2020 Cryo-EM | Structural complex — **not** screening EC50/Emax primary | **Rejected** (per mission) |
| Dhop 2016 Table 2 | WIN cyclase EC50 **16** / Emax **40±1.2** on **mCB2** | Different species — not substitute |

**Felder abstract excerpt:**

> “The rank order of potency and efficacy for binding … was mimicked in functional inhibition of cAMP accumulation experiments for all compounds tested.” — **no WIN EC50/Emax numbers**.

**Final:** **`REVIEW_REQUIRED`** (primary insufficiently located for numeric chain).

---

## 7. LEI-101 / URB447 — provenance (not assumed original-7)

| Compound | Why it appears | In Round1 CSV? | Action |
|---|---|---|---|
| **URB447** | Seed / Janus map precedent; LoVerme 2009 rows | **YES** (`URB447_bind_*`, `URB447_func_*`) | Already in Round1 universe — **not** a Gemini-only add. **No new Gold promotion** this pass |
| **LEI-101** | Mukhopadhyay 2016 BJP functional/binding rows | **YES** (`LEI101_*`) | Same — documentary traceability via Round1 CSV. **Out of Round 1.3 focus-7 CONFIRMED promotion** unless separately re-audited end-to-end |

If Gemini listed them as “extras” without Round1 rows, they would stay out of Gold. Here they **pre-exist** in Round1 with Source DOIs — still **not** auto-promoted by this cross-validation.

---

## 8. Mandatory assay separation

### Subset A — hCB2 / intact cells / cAMP

| Compound | Membership after Round 1.3 | Notes |
|---|---|---|
| CP-55,940 | **EMPTY / not promoted** | Reference only |
| HU-308 | **Near-miss; not CONFIRMED** | EC50/Emax DIRECT; SMILES/Emax-ref blocks |
| RG7774 | **Near-miss; not CONFIRMED** | EC50/system DIRECT; numeric Emax % missing |
| GW405833 | **Not CONFIRMED** | Valenzano PDF unrecovered; Gemini 14±2 / 48±4 failed |
| APD371 | **Excluded (wrong assay class)** | β-arrestin 106% only |
| AM1710 | **Excluded from A** | Never mix GTPγS / mCB2 cyclase into A |
| WIN | **Not CONFIRMED** | No numeric primary lock |

**CONFIRMED_SUBSET_A_cAMP count: 0**

### Subset B — hCB2 / isolated membranes / [³⁵S]GTPγS

| Compound | Membership after Round 1.3 | Notes |
|---|---|---|
| AM1710 | **Not CONFIRMED** | 5a identity fail; 11.2/89 NOT_FOUND; curated Ki/GTP system = **mouse spleen**, not proven hCB2 |

**CONFIRMED_SUBSET_B_GTPGAMMAS count: 0**

Do **not** merge Subset A and Subset B into one homogeneous Gold.

---

## 9. Final status table

| Compound | Gemini claim (brief) | Primary source | Independently verified | Assay subset | Final status | Confidence |
|---|---|---|---|---|---|---|
| AM1710 | Resolved as Subset B: **5a**, Ki 6.7, GTPγS EC50 **11.2±1.8**, Emax **89±3%**, **hCB2** | Khanolkar 2007 abstract + ChEMBL doc activities; Dhop 2016 as mix-check | Identity **4b** DIRECT; Ki 6.7 PARTIAL (**m** spleen); 11.2/89 **NOT_FOUND**; hCB2 **FAIL** | Would be B **if** proven — **not** proven | **REVIEW_REQUIRED** | **High** (rejects Gemini resolve) |
| GW405833 | Resolved as Subset A: EC50 **14±2**, Emax **48±4%**, structure/SMILES | Valenzano 2005 abstract only (PDF N) | ~50% partial agonist DIRECT; 14±2 / 48±4 / Fig1 SMILES **NOT_FOUND** | A (cAMP claim) | **REVIEW_REQUIRED** | **High** |
| CP-55,940 | (Prior adversarial CONFIRMED homogeneous) | Soethoudt 2017; Round1 ref note | Multi-assay reference; no locked absolute Gold row | A candidate only as ref | **REVIEW_REQUIRED** | **High** |
| HU-308 | (Prior adversarial CONFIRMED) | Hanuš 1999 PMC/EuropePMC | Chain mostly DIRECT; SMILES regen fail | A near-miss | **REVIEW_REQUIRED** | **High** |
| RG7774 | (Prior adversarial CONFIRMED) | Frontiers 2024 OA | EC50/system DIRECT; Emax% missing | A near-miss | **REVIEW_REQUIRED** | **High** |
| APD371 | Still under review; Emax issues | Han 2017 PMC5733264 | Emax **106%** DIRECT for **β-arrestin**; not cAMP | **β-arrestin (not A/B)** | **REVIEW_REQUIRED** | **High** |
| WIN 55,212-2 | Still under review | Felder 1995 abstract; Showalter ≠ WIN primary | No numeric EC50/Emax | Unlocked | **REVIEW_REQUIRED** | **High** |
| LEI-101 | Appear in R1.3 context | Round1 CSV / Mukhopadhyay 2016 | Provenance = pre-existing Round1 rows | Mixed (cAMP/GTP/β-arr in Round1) | **Out of promotion** (trace only) | **Med** |
| URB447 | Appear in R1.3 context | Round1 CSV / LoVerme 2009 | Provenance = pre-existing Round1 rows | Mixed | **Out of promotion** (trace only) | **Med** |

---

## 10. Contradiction log vs Gemini claims (DIRECT quotes)

| ID | Gemini claim | Primary / curated counter-evidence | Resolution |
|---|---|---|---|
| G1 | AM1710 = **5a** | Abstract: “**4b (AM1710)** … **5 (AM1714)**” | **Gemini rejected** |
| G2 | AM1710 GTPγS EC50 **11.2±1.8** / Emax **89±3%** on **hCB2** | Values **NOT_FOUND** in Khanolkar abstract/ChEMBL; ChEMBL GTPγS = **50% at 1 µM**, **mouse** spleen | **Gemini rejected** / **REVIEW** |
| G3 | Ki 6.7 = **human** CB2 Table 1 | ChEMBL (same DOI): Ki 6.7 from **mouse spleen** CB2 membranes | Species claim **fails** curated deposit; primary table still unrecovered |
| G4 | GW405833 EC50 **14±2 nM** | Not in Valenzano abstract; PDF unrecovered | **NOT_FOUND** — cannot CONFIRMED_A |
| G5 | GW405833 Emax **48±4%** | Abstract “**approximately 50%**”; exact 48±4 absent; **48±4.3** = Dhop AM1710 cyclase | Exact Gemini Emax **not** verified; mix risk flagged |
| G6 | GW405833 SMILES proven from Fig 1 | Fig 1 **not** recovered | **SMILES NOT VERIFIED** |
| G7 | AM1710 & GW405833 “resolved” | This audit: both **REVIEW_REQUIRED** | **Authority claim rejected** |
| G8 | APD371 / WIN still under review | Independent: both **REVIEW_REQUIRED** | **Survives** (agree under-review) |
| G9 | APD371 missing quantitative Emax (if still claimed) | Han Table 1: **106** vs CP-55,940=100 (**β-arrestin**) | Emax exists for β-arrestin; still not Subset A |

---

## 11. Sources inspected this pass

| # | Source | Form | Outcome |
|---|---|---|---|
| 1 | Khanolkar 2007 | PubMed/EuropePMC/ChEMBL abstract + ChEMBL activities `CHEMBL1138340` | Identity 4b/5 DIRECT; Ki/GTP systems PARTIAL (mouse); 11.2/89 NOT_FOUND; PDF N |
| 2 | BindingDB DOI 10.7270/q2736qn9 | HTML entry (not ACS PDF) | Ki 6.7 / 360 pointers; **not** primary tables |
| 3 | Valenzano 2005 | PubMed abstract; Unpaywall closed | ~50% cAMP partial; PDF/Fig1/Table2 N |
| 4 | Dhopeshwarkar & Mackie 2016 PMC4959096 | Local HTML Table 2 + Methods | AM1710 mCB2 cyclase 11 / 48±4.3; mix check |
| 5 | Hanuš 1999 | EuropePMC PDF extract | HU-308 hCB2 CHO cAMP 5.57 / 108.6±8.4 |
| 6 | Han 2017 | EuropePMC PDF extract | APD371=6; β-arr 6.2 (106); SI N |
| 7 | RG7774 Frontiers 2024 | Local PDF extract | CHO hCB2 cAMP 2.81±0.28; full agonist sans % |
| 8 | Soethoudt 2017 | Local EuropePMC PDF extract | CP/HU/WIN multi-pathway consensus; not Level-0 single-row lock |
| 9 | Felder 1995 / Showalter 1996 | PubMed XML | WIN narrative only; Showalter ≠ WIN primary |
| 10 | Li 2017 PMC5502377 | HTML Fig 1 caption | GW405833=L768242 naming — **INFERRED** only |
| 11 | Round1 CSV + ROUND1_RECONCILIATION_v1.0.md | Local | Baseline statuses; URB447/LEI-101 provenance |

**Not used as final authority:** PubChem/GtoPdb SMILES, vendor datasheets (0.65 nM), Wikipedia, Sci-Hub.

---

## 12. Parent summary (integrity)

| Question | Answer |
|---|---|
| Which Gemini claims **survived**? | Only the **under-review** stance on **APD371** and **WIN**. Numeric “resolve” packages for **AM1710** and **GW405833** **did not** survive. |
| Subset A membership | **Empty (0 CONFIRMED)**. HU-308 / RG7774 remain near-misses. GW405833 not confirmed. |
| Subset B membership | **Empty (0 CONFIRMED)**. AM1710 **not** `CONFIRMED_SUBSET_B_GTPGAMMAS`. |
| Path written | `results/reports/ROUND1.3_CROSS_VALIDATION.md` |
| Gold / Round1 CSV modified? | **No** |
| Pipeline | **STOP** after this validation |

**Bottom line:** Gemini’s Round 1.3 claim that AM1710 and GW405833 are resolved is **independently rejected**. Prefer **REVIEW_REQUIRED** over false CONFIRMED_* while primary PDFs for Khanolkar Tables and Valenzano Fig 1/Table 2 remain unrecovered and key Gemini numbers remain **NOT_FOUND** or species-mismatched.

---

*End ROUND1.3_CROSS_VALIDATION — create-only; STOP.*
