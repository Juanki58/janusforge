# ROUND1_ORDEN4_GW405833_FALSIFICATION

**Mission:** Attempt to refute assignment  
`GW405833 → hCB2 → intact CHO-K1 → forskolin-stimulated cAMP → EC50 14 ± 2 nM → Emax 48 ± 4%`  
using **Valenzano et al., Neuropharmacology 48:658–672, DOI `10.1016/j.neuropharm.2004.12.008`** as sole primary.  
**Date:** 2026-08-17  
**Prior status read:** `ROUND1.6_GW405833_PRIMARY_RESOLUTION.md`, `ROUND1.7_GW405833_FUNCTIONAL_TEXT_EXTRACT.md`, `ROUND1.8_GW405833_CONSOLIDATION.md`, `ROUND1.9_MASTER_EVIDENCE_STATE.md`  
**Integrity:** No Gemini / PubChem / Tocris / reviews as primary. No docking / models / git. Pipeline STOP after this file.

---

## 1. Table 2 recovery status

| Probe | Result (this pass) |
| --- | --- |
| Local `data/papers/**` Valenzano PDF / Table 2 image / OCR | **NOT_FOUND** (no `valen*` / `15814101` / `GW405833` / `L-768` PDF) |
| Unpaywall `10.1016/j.neuropharm.2004.12.008` | `is_oa=false`; `best_oa_location=null`; `oa_locations=[]`; `has_repository_copy=false` |
| OpenAlex | `primary_location.is_oa=false`; `pdf_url=null`; `any_repository_has_fulltext=false` |
| EuropePMC | `isOpenAccess=N`; `hasPDF=N`; `inEPMC=N`; `HAS_FT:Y` → **hitCount=0** |
| Semantic Scholar | `isOpenAccess=false`; `openAccessPdf.status=CLOSED`; empty PDF URL |
| Wayback CDX (doi.org) | Redirects/HTML only — **no PDF snapshot** of article body/tables |
| ScienceDirect PDF CDX | Gateway **504** this pass; prior R1.6 empty PDF sets |
| Author manuscript / PMC OA | **NOT_FOUND** |
| Gemini-deposited Valenzano extracts (candidate primary quotes) | **NOT_FOUND** on disk (no Gemini Valenzano table/text deposit to verify) |
| Recovered Valenzano primary text this path | **Abstract only** (PubMed eFetch / EuropePMC / local `orden4_pubmed_abs.txt`, `r14_pubmed_valenzano.txt`) |

**Table 2 recovered: N**

**Verdict:** Pharmacology **Table 2** (and any labeled functional table/figure with EC50/Emax cells) remains **unrecovered**. Per ORDEN rule: if Table 2 still unrecovered → **cannot** issue `GOLD_CONFIRMED`.

---

## 2. Claim under test

Exact package under falsification:

| Element | Claimed value |
| --- | --- |
| Compound | **GW405833** |
| Receptor | **hCB2** |
| System | **intact CHO-K1** |
| Assay | **forskolin-stimulated cAMP** |
| Potency | **EC50 14 ± 2 nM** |
| Efficacy | **Emax 48 ± 4%** |

**Historical competitors (not used to “pick” a winner):** Round1 CSV EC50 **0.65 nM**; abstract qualitative **approximately 50%** vs CP55,940. Neither substitutes for a recovered Table 2 cell.

---

## 3. Falsification attempts (each check)

Each check was attempted against **recovered Valenzano primary only** (abstract) + recovery probes for Table 2/Fig./Methods. Secondary papers (e.g. Dhopeshwarkar 2016) are noted only as **mix-risk documentation**, not as Valenzano primary.

### 3.1 Another row with those numbers

| Status | Finding |
| --- | --- |
| **INCONCLUSIVE — table unrecovered** | No Valenzano table rows opened. Literal strings **`14 ± 2`**, **`14±2`**, **`48 ± 4`**, **`48±4`** do **not** appear in the recovered abstract. Cannot show the numbers belong to a different compound row **inside Valenzano**. |

### 3.2 Another species

| Status | Finding |
| --- | --- |
| **PARTIAL abstract / table unrecovered** | Abstract assigns high-affinity binding to **both rat and human CB2**, and places partial agonism in that same sentence (forskolin cAMP vs CP55,940). Without Table 2 / Methods, cannot prove whether claimed **14 ± 2 / 48 ± 4** (if they exist in the paper) are **human-only**, **rat-only**, or dual. Species misassignment **not proven**. |

### 3.3 Another receptor

| Status | Finding |
| --- | --- |
| **INCONCLUSIVE — table unrecovered** | Abstract language is **CB2**-selective for the partial-agonist statement. No recovered table cells for CB1 functional EC50/Emax for GW405833. Cannot prove the numeric package belongs to CB1 (or other) **from Valenzano primary**. |

### 3.4 Another assay

| Status | Finding |
| --- | --- |
| **INCONCLUSIVE — table unrecovered** | Abstract functional readout named: **forskolin-mediated cAMP**. Binding is also claimed (affinity), but **no EC50** for binding or function appears in abstract. Cannot show **14 ± 2 nM** is Ki / GTPγS / other assay from Valenzano cells. Competing historical Round1 **0.65 nM** also **NOT_FOUND** in abstract. |

### 3.5 Another normalization

| Status | Finding |
| --- | --- |
| **PARTIAL abstract tension / not CONTRADICTED** | Abstract efficacy is **“approximately 50%”** reduction of forskolin-mediated cAMP **compared to CP55,940**. Claimed **Emax 48 ± 4%** is **not** a literal abstract string and **must not** be equated to “approximately 50%”. Without Table 2 footnotes, cannot prove alternate normalization (e.g. % forskolin absolute vs % of CP55,940). Abstract vs claimed exact Emax is a **verification gap**, not a demonstrated row/column mis-read. |

### 3.6 Erratum

| Status | Finding |
| --- | --- |
| **NOT_FOUND** | PubMed: `"Valenzano KJ"[Author] AND GW405833 AND "published erratum"[Publication Type]` → **0 hits**. Crossref work record: `update-to` / `updated-by` **null**; `relation` **empty**. No Valenzano/GW405833 corrigendum recovered that retracts or reassigns the claimed numbers. |

### 3.7 Discrepancy among text, figure, and table

| Status | Finding |
| --- | --- |
| **CANNOT COMPLETE — figure/table unrecovered** | Recovered **text** (abstract): partial agonist; ~50% vs CP55,940; forskolin cAMP; rat+human CB2; **no** EC50; **no** 48±4; **no** CHO-K1. **Fig. 1** / **Table 2**: unrecovered → no text↔figure↔table conflict can be demonstrated for the numeric package. |

### 3.8 Cross-paper mix-risk (NOT Valenzano primary; not used to CONTRADICT)

Documentary only (from prior ROUND1.3 / R1.6; not primary authority here):

- Dhopeshwarkar & Mackie 2016 Table 2: **AM1710** mCB2 cyclase Emax **48 ± 4.3** (different compound/species/paper).
- Same Dhop table: **GW405833** mCB2 cyclase Emax **0** (different experiment — do **not** pool to reject Valenzano abstract partial agonism).

These raise **contamination risk** for historical Gemini **48 ± 4**, but **do not** constitute Valenzano-primary proof that Valenzano’s (unseen) Table 2 misassigns the claim.

---

## 4. Evidence log (quotes + locations)

### 4.1 Primary abstract (PubMed eFetch PMID 15814101; also `data/papers/_recon_tmp/orden4_pubmed_abs.txt`)

> “For the first time, we show that **GW405833** selectively binds both **rat and human CB2** receptors with high affinity, where it acts as a **partial agonist** (**approximately 50%** reduction of **forskolin-mediated cAMP** production compared to the full cannabinoid agonist, **CP55,940**).”

**Supports (abstract-only):** compound name GW405833; human (and rat) CB2; forskolin cAMP partial agonism; ~50% vs CP55,940.  
**Does not support:** EC50 **14 ± 2 nM**; Emax **48 ± 4%**; intact **CHO-K1**; unequivocal table-row ownership.

### 4.2 Absences in recovered primary text

| Literal / element | In Valenzano abstract? | In recovered Table 2? |
| --- | --- | --- |
| `14 ± 2` / `14±2` nM | **NO** | Table **NOT_FOUND** |
| `48 ± 4` / `48±4` % | **NO** | Table **NOT_FOUND** |
| `0.65` nM | **NO** | Table **NOT_FOUND** |
| `CHO-K1` | **NO** (MeSH “CHO Cells” = indexing metadata only — **not** Methods quote) | Methods **NOT_FOUND** |
| `L-768242` / `L-768,242` | **NO** | Table **NOT_FOUND** |

### 4.3 OA / repository status (this pass dumps)

- `data/papers/_recon_tmp/orden4_up_valenzano.json` — closed OA  
- `data/papers/_recon_tmp/orden4_epmc_valenzano.json` / `orden4_epmc_ft.json` — no full text  
- `data/papers/_recon_tmp/orden4_s2.json` — CLOSED PDF  
- `data/papers/_recon_tmp/orden4_crossref.json` — no update/erratum relation  
- `data/papers/_recon_tmp/orden4_erratum_tight.json` — 0 published errata  

### 4.4 Continuity with ROUND1.6–1.8

| Prior report | Locked finding preserved |
| --- | --- |
| R1.6 | PDF/Fig.1/tables **NOT_FOUND**; ownership of 14±2 / 48±4 = **NOT_VERIFIED** |
| R1.7 | Literal 14±2 = **N**; literal 48±4 = **N**; CHO-K1 not in abstract |
| R1.8 | Status **`GW405833 = REVIEW_REQUIRED`**; do not transform ~50% → 48±4 |

This ORDEN4 pass **reconfirmed** those gaps; Table 2 still not recovered.

---

## 5. Mandatory result

# **REVIEW_REQUIRED**

| Allowed outcome | Why selected / rejected |
| --- | --- |
| **GOLD_CONFIRMED** | **Forbidden.** Table 2 unrecovered; numbers not literal in primary abstract; CHO-K1 not Methods-locked; falsification incomplete by absence of table — not by successful primary confirmation. Secondary/historical numbers do not unlock GOLD. |
| **CONTRADICTED** | **Not selected.** No recovered Valenzano table/figure/text proves the claimed numbers belong to another row, species, receptor, assay, or normalization **inside Valenzano**. Abstract ~50% ≠ 48±4 is a **non-identity / unverified** gap, not a demonstrated misassignment of a recovered cell. Cross-paper Dhop mix-risk is not Valenzano primary contradiction. |
| **REVIEW_REQUIRED** | **Selected.** Per hard rule: Table 2 still unrecovered → **REVIEW_REQUIRED** (not GOLD). Claim package remains **unfalsified and unconfirmed**. |

---

## 6. Confidence + blocking reason

| Item | Value |
| --- | --- |
| **Mandatory result** | **`REVIEW_REQUIRED`** |
| **Confidence** | **High** |
| **Blocking reason** | Valenzano full PDF / HTML / **Table 2** (and Methods naming intact CHO-K1) remain **unrecovered** (Elsevier closed OA; no repository/PMC/author manuscript; no Gemini quote deposit). Without primary table cells, the package `14 ± 2 nM / 48 ± 4% / hCB2 / CHO-K1 / forskolin cAMP` cannot be **confirmed** or **contradicted** under ORDEN rules. |
| **Unblock (out of scope)** | Obtain legitimate Valenzano PDF → literal Table 2 + Methods transcription → re-run falsification checks 3.1–3.7. |
| **Pipeline** | **STOP** (no docking / models / git / Gold promotion). |

---

## Parent handoff

| Field | Value |
| --- | --- |
| Table 2 recovery | **N** |
| Result | **REVIEW_REQUIRED** |
| Path | `results/reports/ROUND1_ORDEN4_GW405833_FALSIFICATION.md` |
