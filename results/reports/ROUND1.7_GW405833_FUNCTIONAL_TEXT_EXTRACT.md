# ROUND1.7_GW405833_FUNCTIONAL_TEXT_EXTRACT

**Mission:** Recover **primary text only** of Valenzano et al. 2005 (*Neuropharmacology* **48**:658–672, DOI `10.1016/j.neuropharm.2004.12.008` — **not** Pertwee `…2005.01.010`) and determine whether EC50 **14 ± 2 nM** and Emax **48 ± 4%** for **GW405833** in **CHO-K1 hCB2** forskolin-cAMP appear **literally**.  
**Date of this pass:** 2026-08-17  
**Prior status (ROUND1.6):** PDF/tables/Fig. 1 unrecovered; abstract-only; `GW405833 = REVIEW_REQUIRED`.  
**Integrity:** No Gemini / PubChem / Tocris / reviews / secondary papers as primary evidence. No models. No git / Round1 CSV / Gold / prior-report overwrites (this file is a **new** deliverable only). Pipeline **STOP** after this file.

---

## 1. Source recovery (what text was opened)

| Source | Opened? | Content recovered |
| --- | --- | --- |
| ROUND1.6 report | Yes (read-only) | Confirmed abstract-only; PDF N; wrong DOI flagged |
| Local `data/papers/**` Valenzano PDF / OCR | Scanned | **No** Valenzano PDF / figure OCR / table image under that name/DOI/PMID |
| PubMed abstract (efetch text + XML) | Yes | Full native abstract (PMID **15814101**) |
| EuropePMC core / HAS_FT / AUTH_MAN | Yes (live re-query) | Same abstract; `HAS_FT` hitCount=0; `authMan=N`; `isOpenAccess=N`; `hasPDF=N` |
| Unpaywall | Yes (live) | `is_oa=false`; `best_oa_location=null`; no repository copy |
| OpenAlex | Yes (live) | Non-OA; no PDF URL; no reconstructable abstract body |
| Semantic Scholar | Yes (live) | `isOpenAccess=false`; abstract elided/`null`; OA PDF closed |
| Crossref | Yes (live) | Bibliographic identity + TDM link metadata only (no body) |
| Elsevier article API (no key) | Yes (live) | **coredata metadata only** (`openaccess=0`); no full-text / tables |
| Elsevier text/plain TDM URL | Yes (live) | **400** `INVALID_INPUT` / no body |
| ScienceDirect abs HTML (`S0028390805000092`) | Yes (live, ~833 KB) | JS shell only — **no** readable abstract/body after strip; false-positive “Emax”/“0.65” hits inside obfuscated JS/SVG, **not** article text |
| Wayback / CDX | Attempted | Availability/CDX **502/503**; no archived full text obtained |
| Author manuscript / PMC OA | Queried | **NOT_FOUND** |

**Recovered primary text body:** **Y** — **abstract only** (PubMed / EuropePMC native wording).  
**Full PDF / HTML with tables-figures / methods pages:** **N**.

---

## 2. Literal extracts (quotes)

### 2.1 Functional cAMP sentence (only recoverable functional efficacy language)

**Location:** PubMed / EuropePMC **Abstract** (not a numbered Results table; page/section of PDF unknown because PDF unrecovered).  
**Local copies:** `data/papers/_recon_tmp/valenzano_pubmed.xml` (`AbstractText`); `data/papers/_recon_tmp/r17_pubmed_abs.txt`; EuropePMC `abstractText`.

> “For the first time, we show that **GW405833** selectively binds both **rat and human CB2** receptors with high affinity, where it acts as a **partial agonist** (**approximately 50%** reduction of **forskolin-mediated cAMP** production compared to the full cannabinoid agonist, **CP55,940**).”

### 2.2 Related abstract numerics (not EC50/Emax)

Same Abstract:

> “…intraperitoneal administration of GW405833 (**0.3-100 mg/kg**) to rats…”  
> “…GW405833 (**up to 30 mg/kg**) elicits potent and efficacious antihyperalgesic effects…”  
> “…not observed in this dose range, but were apparent at **100 mg/kg**.”

These are **in vivo dose** figures, not CHO-K1 hCB2 EC50/Emax.

### 2.3 Not primary article body (documentary only)

- PubMed MeSH includes **CHO Cells** — NLM indexing metadata, **not** a Methods quote naming **CHO-K1**.  
- PubMed ChemicalList string for the ligand is NLM metadata — not used here for functional values.

**No table/figure/section** with labeled GW405833 / L-768242 EC50 or Emax cells was opened.

---

## 3. All GW405833 functional numbers found

Scope = **recovered Valenzano primary text only** (abstract). Synonym **L-768242 / L-768,242** does **not** appear in the abstract.

| Value in recovered primary text | Type | Assigned to GW405833? | Assay / system stated in that text |
| --- | --- | --- | --- |
| **approximately 50%** reduction of forskolin-mediated cAMP vs CP55,940 | Qualitative / approximate **efficacy** (not “Emax = 48 ± 4%”) | **Yes** (GW405833) | Forskolin-mediated cAMP; human (and rat) CB2 binding context; **CHO-K1 not stated** |
| **0.3–100 mg/kg** | In vivo i.p. dose range | Yes | Rat PK / systemic, **not** cAMP EC50 |
| **up to 30 mg/kg** | In vivo efficacy dose | Yes | Pain models, **not** cAMP EC50 |
| **100 mg/kg** | In vivo side-effect dose | Yes | Analgesia/sedation/catalepsy, **not** cAMP EC50 |
| EC50 numeric (any) | — | **None found** | — |
| Emax as **48 ± 4%** (or any ± SEM Emax) | — | **None found** | — |
| **14 ± 2 nM** | — | **None found** | — |
| **0.65 nM** (Round1 CSV legacy) | — | **None found** in opened primary | — |
| % inhibition numeric other than “approximately 50%” | — | **None found** | — |

---

## 4. Literal match check: 14±2 nM / 48±4%

| Question | Answer |
| --- | --- |
| Does **“14 ± 2 nM”** (or equivalent literal `14±2 nM` / `14 +/- 2 nM`) appear in recovered Valenzano primary text? | **NO** |
| Does **“48 ± 4%”** (or equivalent literal `48±4%` / `48 +/- 4%`) appear in recovered Valenzano primary text? | **NO** |
| Are either value assigned to **GW405833** in **CHO-K1 hCB2 forskolin-cAMP** in a recovered table/figure/section? | **NO** — system **CHO-K1** not in abstract; table/figure unrecovered |
| Is abstract **“approximately 50%”** accepted as literal equivalent of **48 ± 4%**? | **NO** (hard rule: do not invent / equate paraphrase) |

---

## 5. Final status

| Endpoint | Status |
| --- | --- |
| Recovered Valenzano primary functional **table/figure** | **NOT_FOUND** |
| Literal EC50 **14 ± 2 nM** | **NOT_FOUND** |
| Literal Emax **48 ± 4%** | **NOT_FOUND** |
| Abstract-only partial-agonist language (~50% forskolin cAMP vs CP55,940) | **DIRECT** (abstract only; non-table) |
| Compound certification for functional Subset A / Gold | **`GW405833 = REVIEW_REQUIRED`** |

**CONFIRMED_FUNCTIONAL_TEXT:** **not** reached (requires both numbers literal **and** assigned to GW405833 CHO-K1 hCB2 forskolin-cAMP).

**Final status: `GW405833 = REVIEW_REQUIRED`**

---

## 6. Gaps

1. Full Valenzano PDF / ScienceDirect HTML body with Results tables (and Methods naming cell system) still closed / unrecovered.  
2. No OCR path: no local Valenzano page images.  
3. **CHO-K1** not present in recoverable primary prose (MeSH only).  
4. Synonym **L-768242** not in abstract.  
5. Cannot inventory every EC50/Emax/% inhibition cell for GW405833 until PDF/HTML tables are obtained.  
6. Elsevier TDM full-text requires valid authorized access (API key / institutional); unauthenticated calls return metadata or errors only.  
7. Internet Archive CDX/availability intermittent (**502/503**) this pass — no archived full text captured.

**Unblock (out of scope for STOP):** legitimate full-text access → transcribe functional table/figure cells literally → re-run literal match for **14 ± 2 nM** / **48 ± 4%**.

---

## Parent return

| Field | Value |
| --- | --- |
| Recovered text | **Y** (abstract only) |
| Literal **14 ± 2** | **N** |
| Literal **48 ± 4** | **N** |
| Final status | **`GW405833 = REVIEW_REQUIRED`** |
| Path | `results/reports/ROUND1.7_GW405833_FUNCTIONAL_TEXT_EXTRACT.md` |
| Integrity | Primary-only abstract; no secondary as evidence; no CSV/Gold/prior overwrite; pipeline STOP |
