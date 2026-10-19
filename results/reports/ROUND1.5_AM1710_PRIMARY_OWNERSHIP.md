# ROUND1.5_AM1710_PRIMARY_OWNERSHIP

**Mission:** Resolve AM1710 ownership exclusively from Khanolkar et al., *J. Med. Chem.* 2007 (primary tables).  
**Date of this pass:** 2026-08-17  
**Integrity:** No Gemini / PubChem / IUPHAR / Wikipedia / reviews / commercial DBs used as primary evidence for Ki/EC50/Emax ownership. No voting. No numerical inference. No secondary name→value association beyond what the opened primary text literally states. No Gold/prior-report edits.

---

## 1. Source recovery status (PDF recovered? pages?)

| Item | Status |
| --- | --- |
| Correct bibliographic identity | **DIRECT** — Khanolkar AD et al., *J. Med. Chem.* **2007**, **50**, **6493–6500** (issue 26); DOI **10.1021/jm070441u**; PMID **18038967**. Note: mission brief page range **4496–4506** does **not** match Crossref/PubMed/ACS for this DOI (wrong pages). |
| ACS full HTML (`/doi/full/…`) | **NOT_FOUND** (paywall / “Access is not provided”; programmatic fetch **403**) |
| ACS PDF (`/doi/pdf/…`, `/doi/pdfplus/…`) | **NOT_FOUND** (**403**) |
| ACS Supporting Information PDF | **NOT_FOUND** as PDF this pass (local `data/papers/_recon_tmp/khanolkar_si.pdf` is Cloudflare HTML “Just a moment…”, size 5652 B, not `%PDF-`). SI description on ACS landing is elemental/X-ray for **4a**/**4b** only — not Tables 1–2 pharmacology. |
| EuropePMC full text | **NOT_FOUND** (`isOpenAccess=N`, `inEPMC=N`, no PMCID; `fullTextXML` **404**; publisher link = subscription) |
| Unpaywall / OpenAlex / Semantic Scholar “OA” | Resolves to `https://doi.org/10.7270/q2736qn9` → **BindingDB curated Ki landing**, **not** the Khanolkar article PDF. **Rejected as primary** under mission rules. |
| Local `data/papers/` scan | **No** PDF containing `jm070441u` / `Cannabilactones` / article page string recovered with size >20 KB |
| Wayback Machine CDX / availability | **Unavailable this pass** (HTTP **503** / hung availability API) |
| Opened primary text this pass | **Abstract only** (native text): PubMed abstract dump `data/papers/_recon_tmp/r14_pubmed_khanolkar.txt`; ACS DOI landing abstract (WebFetch); EuropePMC abstract page |

**Verdict:** Full article PDF/HTML with **Table 1** and **Table 2** = **NOT_FOUND**. Pipeline cannot OCR table images that were never obtained.

---

## 2. Table 1 complete transcription

**Status: NOT_FOUND**

No Table 1 page, caption, column headers, footnotes, or compound rows were recovered from the primary PDF/HTML.

Abstract alone does **not** contain tabular Ki cells and is insufficient to reconstruct Table 1.

---

## 3. Table 2 complete transcription

**Status: NOT_FOUND**

No Table 2 page, caption, column headers (EC50 / Emax / assay type), Methods excerpt for the functional assay (species; membrane vs cell; GTPγS vs cyclase), footnotes, or compound rows were recovered from the primary PDF/HTML.

Abstract alone states only that “in vitro testing revealed that the novel compounds are CB2 agonists” — **no** EC50/Emax numbers.

---

## 4. Identity map (4b / 5a / AM1710 / neighbors)

### Evidence opened (native abstract text)

Exact PubMed/ACS/EuropePMC abstract wording (native text):

> “… Optimal receptor subtype selectivity of 490-fold and subnanomolar affinity for the CB2 receptor is exhibited by a 9-hydroxyl analog **5 (AM1714)**, while the 9-methoxy analog **4b (AM1710)** had a 54-fold CB2 selectivity. … in vivo testing of cannabilactones **4b** and **5** found them to possess potent peripheral analgesic activity.”

| Code / name | Documentary status from opened primary | Tag |
| --- | --- | --- |
| **4b** | Explicitly equated to **AM1710** (9-methoxy analog) in abstract | **DIRECT** |
| **AM1710** | Explicitly equated to **4b** in abstract | **DIRECT** |
| **5** | Explicitly equated to **AM1714** (9-hydroxyl analog) in abstract | **DIRECT** |
| **AM1714** | Explicitly equated to **5** in abstract | **DIRECT** |
| **5a** | **Not named** in opened abstract; no table row recovered linking **5a** to any AM code or value | **NOT_FOUND** (in opened primary) |
| Neighbors (other numbered analogs) | Not recoverable without Scheme/Table cells | **NOT_FOUND** |

**Documentary map (abstract-only):**

- **4b = AM1710** — DIRECT  
- **5 = AM1714** — DIRECT  
- **5a = ?** — cannot be established from recovered primary text  
- **AM1710 = 4b** — DIRECT for **identity only**; **not** a license to attach Table 1/2 numbers that were not read  

**Hard rule compliance:** Abstract identity **must not** be used to assign unrecovered Ki/EC50/Emax cells to AM1710.

---

## 5. Ownership of 11.2 ± 1.8 nM

| Question | Answer |
| --- | --- |
| Located in recovered Khanolkar Table 1 or Table 2 cell? | **NO** |
| Located in opened abstract? | **NO** |
| Compound code that owns **11.2 ± 1.8 nM** in primary tables | **NOT_FOUND** — tables unrecovered |
| Can AM1710 be assigned this value from primary tables? | **NO** |

**Tag: NOT_FOUND**

---

## 6. Ownership of Emax 89 ± 3%

| Question | Answer |
| --- | --- |
| Located in recovered Khanolkar Table 2 cell? | **NO** |
| Located in opened abstract? | **NO** |
| Compound code that owns **Emax 89 ± 3%** in primary tables | **NOT_FOUND** — tables unrecovered |
| Can AM1710 be assigned this value from primary tables? | **NO** |

**Tag: NOT_FOUND**

---

## 7. Final status for AM1710

### AM1710 = **REVIEW_REQUIRED**

Primary tables **cannot** prove `AM1710 = 11.2 ± 1.8 nM` and/or `AM1710 = Emax 89 ± 3%`.

| Claim | Status |
| --- | --- |
| AM1710 identity = compound **4b** (9-methoxy) | **DIRECT** (abstract) |
| AM1710 = compound **5a** | **NOT proven** (5a absent from opened primary; abstract assigns AM1710 to **4b**, and **5** to AM1714) |
| AM1710 owns Table Ki / EC50 / Emax cells including **11.2 ± 1.8** and **89 ± 3%** | **REVIEW_REQUIRED** — full Table 1/2 cells missing |

---

## 8. Documentary gaps (if any)

Exact missing pieces required to close ownership under mission rules:

1. **Khanolkar 2007 full PDF or unlocked full HTML** for pages covering **Table 1** and **Table 2** (within **6493–6500**).  
2. **Complete literal transcription** of Table 1 (binding): compound code column, any AM common-name column if present, Ki ± SEM, receptor/assay footnotes.  
3. **Complete literal transcription** of Table 2 (functional): compound code, EC50, Emax, assay definition.  
4. **Methods text** for Table 2 assay: species (human/mouse/rat), membrane vs intact cell, **[³⁵S]GTPγS** vs cyclase/cAMP or other.  
5. **Row-level location** of the literal string **`11.2 ± 1.8`** (or equivalent typesetting) and of **`89 ± 3`** / **`89 ± 3%`**, with the compound-code cell in the **same row**.  
6. Clarification whether any table uses code **5a** at all (abstract never mentions **5a**).

Until (1)–(5) are satisfied from the primary article itself, **AM1710 remains REVIEW_REQUIRED** for the 11.2 / 89 ownership package.

**Explicitly not used to fill gaps:** BindingDB (`10.7270/q2736qn9`), ChEMBL deposits, IUPHAR, PubChem, Gemini claims, later papers (e.g. Rahn 2011, Dhopeshwarkar 2016), or chemical memory.

---

## 9. Evidence tag summary (DIRECT/PARTIAL/NOT_FOUND)

| Item | Tag |
| --- | --- |
| DOI / correct pages 6493–6500 | **DIRECT** |
| Abstract: **4b (AM1710)**; **5 (AM1714)** | **DIRECT** |
| Abstract: compounds are CB2 agonists (qualitative) | **DIRECT** |
| Full PDF/HTML recovery | **NOT_FOUND** |
| Table 1 complete transcription | **NOT_FOUND** |
| Table 2 complete transcription | **NOT_FOUND** |
| Identity **5a = ?** | **NOT_FOUND** (opened primary) |
| Ownership of **11.2 ± 1.8 nM** | **NOT_FOUND** |
| Ownership of **Emax 89 ± 3%** | **NOT_FOUND** |
| Proof AM1710 = 11.2 / 89 from primary tables | **NOT_FOUND** → final **REVIEW_REQUIRED** |
| False OA BindingDB DOI as article substitute | **Rejected** (not primary article) |

---

## Parent return (compact)

| Field | Value |
| --- | --- |
| Tables recovered? | **No** (Table 1 & Table 2 **NOT_FOUND**) |
| Who owns **11.2 ± 1.8 nM**? | **Unknown / NOT_FOUND** (no primary table cell) |
| Who owns **Emax 89 ± 3%**? | **Unknown / NOT_FOUND** (no primary table cell) |
| AM1710 final status | **REVIEW_REQUIRED** (identity **4b** DIRECT from abstract only; 11.2/89 unproven) |
| Report path | `results/reports/ROUND1.5_AM1710_PRIMARY_OWNERSHIP.md` |
| Integrity | Primary tables unrecovered; abstract-only for identity; no secondary DB fill; Gold/prior reports untouched |

**PIPELINE STOP** after this deliverable.
