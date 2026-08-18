# ROUND1_ORDEN12 — GW405833 PRIMARY FORENSIC AUDIT

**Primary cited:** Valenzano KJ et al., *Neuropharmacology* **48**:658–672 (2005), DOI `10.1016/j.neuropharm.2004.12.008`, PMID 15814101  
**Date:** 2026-08-17  
**Role:** Cursor Pro forensic audit (Blocks A–D)  
**Integrity:** No docking / models / QSAR / git / silent dataset fix. No secondary as primary. No invented Table 2 cells. Pipeline **STOP** after this file.

---

## Activation condition

**Rule:** Fully execute Blocks A–D only if Gemini (or workspace) has recovered a **verifiable** Valenzano et al. 2005 primary document (PDF/HTML with **Fig. 1** and/or **Table 2** visible).

| Activation probe | Result |
| --- | --- |
| Gemini-deposited Valenzano PDF / HTML body with Fig. 1 or Table 2 | **NOT_FOUND** |
| Gemini / ADVERSARIAL / ORDEN quote-deposit of Table 2 cells or Fig. 1 OCR/screenshots | **NOT_FOUND** |
| Local `data/papers/**` Valenzano PDF (`valen*`, `15814101`, `GW405833`, `L-768`) | **NOT_FOUND** |
| Local figure/table image or OCR for Valenzano Fig. 1 / Table 2 | **NOT_FOUND** |
| Prior Cursor reports (R1.6–1.8, ORDEN4) on primary recovery | PDF / Fig. 1 / Table 2 = **NOT_FOUND**; abstract-only |
| `results/reports/*GEMINI*`, `*ADVERSARIAL*` Valenzano primary | **NOT_FOUND** as Valenzano table/figure deposit (`qiu_0q1_final_cursor_vs_gemini.md` is unrelated Qiu audit) |

**Activation met: N**

**Consequence:** Blocks A–D are recorded as **NOT_VERIFIED** (not executed against a recovered primary figure/table). Mandatory overall status = **REVIEW_REQUIRED** (cannot **GOLD_CONFIRMED**). No table cells invented from secondary sources.

---

## Searched locations (this pass)

| Path / pattern | Finding |
| --- | --- |
| `results/reports/*` (incl. `ROUND1.6`–`1.9`, `ROUND1_ORDEN4_GW405833_FALSIFICATION.md`, GOLD / CERTIFICATION) | Abstract-only Valenzano state reconfirmed; no new Gemini primary deposit |
| `data/papers/**` name/path hunt (`valen*`, `GW405833`, `15814101`, `L-768`) | API/metadata/abstract HTML dumps only; **no** article PDF |
| `data/papers/_recon_tmp/*valenzano*` | Abstract / Unpaywall / EuropePMC / PubMed / S2 JSON/HTML — **not** Fig. 1 or Table 2 |
| `data/papers/_recon_tmp/r14_ia_valenzano.html` | Wayback Machine shell page — **not** article body/tables |
| `data/papers/_recon_tmp/orden4_*` | Recovery probes documenting OA closed; no PDF |
| Workspace globs `*GEMINI*`, `*ADVERSARIAL*`, `*ORDEN12*`, `*Table2*` + Valenzano PDF | No verifiable Valenzano primary Fig. 1 / Table 2 artifact |
| Strings: Valenzano, GW405833, Table 2, OCR, ADVERSARIAL, GEMINI, ORDEN | Prior audits only; **no** new primary transcription |

**Recovered Valenzano primary fragment available on disk:** abstract text only (e.g. `orden4_pubmed_abs.txt`, `r14_pubmed_valenzano.txt`, prior PubMed/EuropePMC dumps). Abstract is **not** Fig. 1 or Table 2 and does **not** satisfy activation.

---

## Block A — Identity (Fig. 1)

**Status:** activation not met → Fig. 1 **not opened**. PubChem / ChemicalList / memory **forbidden** as Fig. 1 substitute.

| Item | Verdict |
| --- | --- |
| GW405833 (labeled on Fig. 1) | **NOT_VERIFIED** |
| L-768,242 if present | **NOT_VERIFIED** |
| Full connectivity | **NOT_VERIFIED** |
| N1 substituent | **NOT_VERIFIED** |
| C3 substituent | **NOT_VERIFIED** |
| 2,3-dichlorobenzoyl | **NOT_VERIFIED** |
| 5-methoxy | **NOT_VERIFIED** |
| 2-methyl | **NOT_VERIFIED** |

---

## Block B — Table 2 (GW405833 row)

**Status:** Table 2 **not recovered** → complete row **not transcribed**. No normalization/correction applied because **no cells** were read from primary.

| Column | Transcribed value |
| --- | --- |
| Human CB1 EC50 | **NOT_VERIFIED** (table unrecovered) |
| Human CB1 Emax | **NOT_VERIFIED** |
| Human CB2 EC50 | **NOT_VERIFIED** |
| Human CB2 Emax | **NOT_VERIFIED** |
| Rat CB1 EC50 | **NOT_VERIFIED** |
| Rat CB1 Emax | **NOT_VERIFIED** |
| Rat CB2 EC50 | **NOT_VERIFIED** |
| Rat CB2 Emax | **NOT_VERIFIED** |

### Targeted check: `14 ± 2 nM` and `48 ± 4 %` at GW405833 × Human CB2

| Check | Verdict |
| --- | --- |
| Literal `14 ± 2` / `14±2` in recovered Table 2 | **NOT_VERIFIED** (table unrecovered) |
| Literal `48 ± 4` / `48±4` in recovered Table 2 | **NOT_VERIFIED** |
| Visual ownership: GW405833 row × Human CB2 column | **NOT_VERIFIED** |
| Numbers found but **not** owned by that intersection | **NOT_VERIFIED** (numbers not found in any opened Valenzano table) |

**Hard rule honored:** abstract “approximately 50%” is **not** accepted as `48 ± 4%`. Secondary / historical Round1 `0.65 nM` is **not** used as Table 2.

---

## Block C — Methods

**Status:** Methods section **not recovered** in full text. Forbidden to infer from MeSH, vendors, or other papers.

| Element | Verdict |
| --- | --- |
| Cell type (literal) | **NOT_VERIFIED** |
| CHO-K1 | **NOT_VERIFIED** |
| hCB2 expression | **NOT_VERIFIED** |
| Forskolin | **NOT_VERIFIED** (Methods unrecovered; abstract mentions forskolin-mediated cAMP — **not** Methods lock) |
| cAMP | **NOT_VERIFIED** (same: abstract ≠ Methods) |
| Relevant assay conditions | **NOT_VERIFIED** |
| Emax normalization | **NOT_VERIFIED** |
| CP55940 control | **NOT_VERIFIED** (abstract names CP55,940 — **not** Methods) |
| Number of determinations | **NOT_VERIFIED** |

---

## Block D — Falsification (deliberate refutation attempts)

Each check requires recovered primary table/figure/text. Without Table 2 / Fig. 1 / Methods body, none can be confirmed or contradicted inside Valenzano.

| Falsification probe | Verdict |
| --- | --- |
| Do `14±2` belong to another row? | **NOT_VERIFIED** |
| Do `48±4` belong to another column? | **NOT_VERIFIED** |
| Human/Rat swapped? | **NOT_VERIFIED** |
| CB1/CB2 swapped? | **NOT_VERIFIED** |
| EC50/Emax swapped? | **NOT_VERIFIED** |
| Other Emax normalization? | **NOT_VERIFIED** |
| Fig. 1 contradicts currently stored structure? | **NOT_VERIFIED** (Fig. 1 unrecovered) |
| Text/table/figure discrepancy? | **NOT_VERIFIED** |
| Erratum? | **NOT_VERIFIED** (no erratum primary inspected this pass; prior ORDEN4 probes did not surface a Valenzano erratum unlocking Table 2) |

---

## SPECIAL STRUCTURE RULE

**Priority rule:** Previous structure starting `CCCn1...` is **INVALIDATED** and must **not** reappear in any Gold file. Compare primary Fig. 1 against structure currently attributed to GW405833 in Round1 CSV / GOLD candidates / reports. If discrepancy: report **STRUCTURE_CONFLICT**, do **not** auto-correct dataset, **STOP** further promotion in this report.

### Stored attribution (documentary — not Fig. 1 proof)

| Source | Stored structure / key |
| --- | --- |
| Round1 lineage / `_tmp_literal_dump.txt` / GOLD candidates | InChIKey **`FSFZRNZSZYDVLI-UHFFFAOYSA-N`** |
| Same lineage SMILES | `CC1=C(C2=C(N1C(=O)C3=C(C(=CC=C3)Cl)Cl)C=CC(=C2)OC)CCN4CCOCC4` (morpholinoethyl / aminoalkylindole encoding — **not** a `CCCn1...` string) |
| Workspace grep for `CCCn1` in Round1 CSV / GOLD / reports | **No `CCCn1...` SMILES found** on disk this pass |
| Valenzano Fig. 1 | **NOT recovered** → cannot compare connectivity, N1, or substituents to stored SMILES |

### Structure conflict decision

| Question | Answer |
| --- | --- |
| Fig. 1 vs stored SMILES discrepancy demonstrated? | **NO** — Fig. 1 absent |
| **STRUCTURE_CONFLICT** declared this pass? | **N** |
| Dataset auto-corrected? | **NO** (forbidden) |
| Promotion work continued? | **NO** — STOP; status remains REVIEW_REQUIRED |

Note: invalidation of any historical `CCCn1...` Gold encoding is acknowledged as a standing rule; absence of Fig. 1 prevents both **confirmation** of the stored morpholinoethyl SMILES and a Fig.1-based **STRUCTURE_CONFLICT**.

---

## FINAL

| Field | Value |
| --- | --- |
| Activation met | **N** |
| Overall status | **REVIEW_REQUIRED** |
| STRUCTURE_CONFLICT | **N** |
| GOLD_CONFIRMED | **Forbidden** (activation failed; primary Fig. 1 / Table 2 unrecovered) |
| CONTRADICTED | **Not selected** (no recovered Valenzano cells prove misassignment) |
| Path | `results/reports/ROUND1_ORDEN12_GW405833_PRIMARY_AUDIT.md` |

**Parent return:** activation met **N**; overall status **REVIEW_REQUIRED**; STRUCTURE_CONFLICT **N**; path `results/reports/ROUND1_ORDEN12_GW405833_PRIMARY_AUDIT.md`.

**PIPELINE = STOP.**
