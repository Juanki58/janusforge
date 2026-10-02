# ROUND1.6_GW405833_PRIMARY_RESOLUTION

**Mission:** Resolve exclusively GW405833 / L-768242 from Valenzano et al., *Neuropharmacology* **48** (2005) **658–672**, using that primary’s figures/tables only.  
**Date of this pass:** 2026-08-17  
**Integrity:** No Gemini / PubChem / IUPHAR / DrugBank / vendors / reviews / prior drafts used as structure or pharmacology authority. No SMILES without Fig. 1 reconstruction. No chemical-plausibility decisions. No pharmacology by secondary name association. No Git / Gold / prior Round report / Round1 CSV edits. Pipeline STOP after this file.

---

## 1. Source recovery status

| Item | Status |
| --- | --- |
| Bibliographic identity (pages/title/authors) | **DIRECT** — Valenzano KJ et al., *Neuropharmacology* **48**(5): **658–672** (Apr 2005); PMID **15814101**; Crossref/OpenAlex/EuropePMC agree |
| Correct DOI | **`10.1016/j.neuropharm.2004.12.008`** (PII `S0028-3908(05)00009-2`) |
| Mission / Round1 alternate DOI `10.1016/j.neuropharm.2005.01.010` | **WRONG PAPER** — Unpaywall resolves that DOI to Pertwee et al. 2005 (“Evidence that (−)-7-hydroxy-4′-dimethylheptyl-cannabidiol…”), **not** Valenzano/GW405833 |
| Local `data/papers/` Valenzano PDF | **NOT_FOUND** (recursive name/path scan: no `valen*` / `GW405833` / `15814101` / `L-768` PDF) |
| Unpaywall | `is_oa=false`; `best_oa_location=null`; `oa_locations=[]`; `has_repository_copy=false` |
| OpenAlex | `primary_location.is_oa=false`; `pdf_url=null` |
| EuropePMC full text | `HAS_FT:Y` → **hitCount=0**; `isOpenAccess=N`; `inEPMC=N`; `inPMC=N`; `hasPDF=N`; only DOI subscription link |
| Semantic Scholar | `isOpenAccess=false`; `openAccessPdf.status=CLOSED`; empty PDF URL |
| Wayback CDX (ScienceDirect PII / related) | Empty result sets `[]` this pass; availability API **502/503** intermittent |
| Elsevier article API (no API key) | Returned **coredata metadata only** (`openaccess=0`); **no** full-text body, figures, or tables |
| Author manuscript / PMC OA | **NOT_FOUND** (`authMan=N`, `nihAuthMan=N`) |
| Sci-Hub | **Not used** this pass (prefer legitimate OA; environment blocked untrusted mirror transfer) |
| Opened primary fragment this pass | **Abstract only** (native): PubMed XML `data/papers/_recon_tmp/valenzano_pubmed.xml`; EuropePMC abstract; prior recon dumps |

**PDF recovered: N**

**Verdict:** Valenzano full PDF / HTML with **Fig. 1** and pharmacology table(s) = **NOT_FOUND**. OCR of Fig. 1 / table images was not possible because no figure/table image was obtained.

---

## 2. Fig. 1 structural reconstruction (items 1–8)

**Status: NOT_FOUND — Fig. 1 body unrecovered**

Per hard rule: if Fig. 1 cannot be recovered with sufficient resolution → structure cannot be locked. Each required element is documented from **Valenzano primary Fig. 1 only** (not from PubMed MeSH, secondary OA captions, or chemical memory).

| # | Element | Observation from Valenzano Fig. 1 | Tag |
| --- | --- | --- | --- |
| 1 | Indole nucleus | Fig. 1 not opened | **NOT_FOUND** |
| 2 | N1 substituent | Fig. 1 not opened — **cannot** state propyl, morpholinyl-ethyl, or other | **NOT_FOUND** |
| 3 | C2 substituent | Fig. 1 not opened | **NOT_FOUND** |
| 4 | C3 substituent | Fig. 1 not opened | **NOT_FOUND** |
| 5 | Methoxy position | Fig. 1 not opened | **NOT_FOUND** |
| 6 | Benzoyl group | Fig. 1 not opened | **NOT_FOUND** |
| 7 | Exact positions of both Cl | Fig. 1 not opened | **NOT_FOUND** |
| 8 | Morpholinyl-ethyl chain presence/position | Fig. 1 not opened | **NOT_FOUND** |

**Informational only (NOT used as Fig. 1 proof):** PubMed `ChemicalList` string  
`1-(2,3-dichlorobenzoyl)-5-methoxy-2-methyl-(2-(mopholin-4-yl)ethyl)-1H-indole`  
is **NLM metadata**, not inspection of Valenzano Fig. 1. Attachment locus of the morpholinyl-ethyl chain in that string is also syntactically ambiguous. **Rejected** as primary structural evidence under mission rules.

**Abstract:** names **GW405833** only; **no** structural drawing, **no** N1 substituent description, **no** IUPAC.

---

## 3. SMILES (only if Fig. 1 fixed) or NOT_VERIFIED

**SMILES: NOT_VERIFIED**

Fig. 1 was not recovered → structure not unequivocal → **no SMILES generated** this pass.

Confidence in SMILES: **N/A** (generation forbidden without fixed primary Fig. 1).

---

## 4. Pharmacology table/figure transcription

**Status: NOT_FOUND**

No primary table or figure page containing GW405833 numeric EC50/Emax cells was recovered (no PDF pages; no OCR).

### Abstract-only primary fragment (native text; not a table)

Exact PubMed/EuropePMC abstract wording:

> “For the first time, we show that **GW405833** selectively binds both rat and human CB2 receptors with high affinity, where it acts as a **partial agonist** (**approximately 50%** reduction of **forskolin-mediated cAMP** production compared to the full cannabinoid agonist, **CP55,940**).”

| Claimed cell / attribute | In recovered primary table/figure? | In abstract? | Tag |
| --- | --- | --- | --- |
| Compound identity = GW405833 / L-768,242 | Table **NOT_FOUND**; synonym **L-768242** **not** in abstract | GW405833 **yes**; L-768,242 **no** | Partial name only |
| Receptor = hCB2 | Table **NOT_FOUND** | “human CB2” binding + cAMP partial agonism language | **PARTIAL** (abstract; not table-locked) |
| Cell system = CHO-K1 | Table/methods **NOT_FOUND** | **Not stated** (MeSH lists CHO Cells — metadata only, **not** methods quote) | **NOT_FOUND** |
| Assay = forskolin-stimulated cAMP | Table **NOT_FOUND** | Forskolin-mediated cAMP **yes** | **PARTIAL** (abstract) |
| EC50 = **14 ± 2 nM** | **NOT_FOUND** | **NOT_FOUND** | **NOT_FOUND** |
| Emax = **48 ± 4%** | **NOT_FOUND** | Exact **48 ± 4** **NOT_FOUND**; abstract has **approximately 50%** | Exact value **NOT_FOUND** |

**Round1 CSV EC50 0.65 nM:** also **NOT_FOUND** in opened Valenzano abstract; tables unrecovered. Per mission: **do not** reconcile by picking a “plausible” number; report primary silence honestly.

---

## 5. Ownership of EC50 14±2 and Emax 48±4

| Question | Answer from Valenzano primary this pass |
| --- | --- |
| Are **14 ± 2 nM** and **48 ± 4%** located in a recovered Valenzano table/figure cell labeled GW405833 (or L-768,242)? | **NO** — table/figure **NOT_FOUND** |
| Do those exact numbers appear in the opened Valenzano abstract? | **NO** |
| Can ownership be assigned unequivocally to GW405833/L-768,242 on hCB2 CHO-K1 forskolin cAMP? | **NO** |
| What does primary abstract support? | GW405833 = partial agonist ≈**50%** of CP55,940 on forskolin-mediated **cAMP**; high-affinity **rat and human CB2** binding — **without** EC50 / exact Emax / CHO-K1 |

**Ownership verdict:** EC50 **14 ± 2 nM** and Emax **48 ± 4%** are **NOT owned** by GW405833 from recovered Valenzano primary cells this pass → **`NOT_VERIFIED`**.

**Mix-risk note (documentary, not used to invent Valenzano cells):** Dhopeshwarkar 2016 reports cyclase Emax **48 ± 4.3** for **AM1710** (different paper/compound). Proximity of Gemini’s **48 ± 4** to that figure is flagged as contamination risk only; it does **not** prove or disprove Valenzano table contents that were never opened.

---

## 6. Gemini vs Fig. 1 contradiction log

| ID | Side A (Gemini claim — mission brief) | Side B (Valenzano Fig. 1 this pass) | Resolution |
| --- | --- | --- | --- |
| G16-1 | N1 substituent = **propyl** / Gemini-proposed structure “resolved” | Fig. 1 **NOT_FOUND** — N1 substituent **NOT_FOUND** | **No Fig. 1 observation** available to confirm or refute N1-propyl. Gemini structure **not accepted**. Cannot “vote,” average, or choose by chemical plausibility. |
| G16-2 | Structure/SMILES resolved from primary | Fig. 1 unrecovered → SMILES **NOT_VERIFIED** | Gemini resolve **rejected** as primary-locked |
| G16-3 | EC50 **14 ± 2 nM**, Emax **48 ± 4%**, hCB2, CHO-K1, forskolin cAMP | Numbers **NOT_FOUND** in abstract; table unrecovered; CHO-K1 **NOT_FOUND** in abstract | Gemini numeric/system package **`NOT_VERIFIED`** against primary cells |
| G16-4 | (Implicit) Round1 **0.65 nM** as competing Valenzano number | **0.65 nM** also **NOT_FOUND** in opened primary | Neither Gemini **14±2** nor Round1 **0.65** locked to Valenzano table this pass |

**Rule applied:** contradiction is resolved by **absence of primary Fig. 1 / table evidence**, not by preferring either Gemini or Round1 CSV.

---

## 7. Final status + confidence

| Endpoint | Final status | Confidence |
| --- | --- | --- |
| Structural identity from Fig. 1 (items 1–8) | **`REVIEW_REQUIRED`** / **`NOT_VERIFIED`** | **High** (Fig. 1 unrecovered) |
| SMILES from Fig. 1 reconstruction | **`NOT_VERIFIED`** (not generated) | **High** |
| Pharmacology table ownership of **14 ± 2 / 48 ± 4** | **`NOT_VERIFIED`** — values **not owned** from primary cells | **High** |
| Compound-level certification for Gold / Subset A | **`GW405833 = REVIEW_REQUIRED`** | **High** |
| Abstract-only functional class (non-table) | Partial forskolin-cAMP agonist ~50% vs CP55,940 (**DIRECT** abstract) | **High** for that sentence only |

**Hard-rule triggers fired:**

1. Fig. 1 not recovered with sufficient resolution → **GW405833 = REVIEW_REQUIRED**  
2. Pharmacology package cannot be assigned unequivocally from primary table/figure → **REVIEW_REQUIRED**

---

## 8. Documentary gaps

1. **Full Valenzano PDF/HTML** (Elsevier/ScienceDirect) — closed OA; no repository copy; no author manuscript located.  
2. **Fig. 1** image or vector — unrecovered → structure checklist 1–8 empty.  
3. **Pharmacology table/figure** with labeled GW405833/L-768,242 rows — unrecovered → cannot quote page/figure/cell for EC50/Emax.  
4. **Methods excerpt** naming **CHO-K1** for the cAMP assay — unrecovered.  
5. Explicit primary synonymy **GW405833 = L-768,242** in opened Valenzano text — **not** in abstract; table/caption unrecovered.  
6. Mission DOI typo risk: `…2005.01.010` is a **different** Neuropharmacology article (Pertwee). Always use `…2004.12.008` for this primary.  
7. Gemini full report file still **not on disk** this pass; Gemini claims treated as **mission-brief assertions** for contradiction logging only.

**Unblock path (out of scope for this STOP):** obtain legitimate Valenzano PDF (institutional access / publisher), then OCR/transcribe Fig. 1 + pharmacology table cells literally before any SMILES or ownership lock.

---

## Parent return

| Field | Value |
| --- | --- |
| PDF recovered | **N** |
| N1 substituent from Fig. 1 | **NOT_FOUND** (Fig. 1 unrecovered) |
| Do **14 ± 2 / 48 ± 4** belong to GW405833 in primary? | **NOT_VERIFIED** — **not owned** from recovered primary cells |
| Final status | **`GW405833 = REVIEW_REQUIRED`** |
| Path | `results/reports/ROUND1.6_GW405833_PRIMARY_RESOLUTION.md` |
| Integrity | Primary-only; no SMILES; no secondary structure authority; no Git/Gold/CSV/prior-report edits; pipeline STOP |
