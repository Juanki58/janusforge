# Qiu et al. 2023 — ACCESS LOG (exhaustive 0P pass)

> **Date:** 2026-08-13  
> **DOI:** 10.1016/j.bioorg.2023.106377 · PMID 36731294  
> **Folder:** `data/papers/qiu_2023_bioorg/` (+ legacy dumps under `data/papers/`)  
> **Rule:** document every attempt; **do not invent** Ki/IC50/EC50.

---

## Recovered (usable)

| Artifact | Path / note | Content recovered |
|----------|-------------|-------------------|
| Abstract (PubMed / EuropePMC / S2) | `api/europepmc_article.json`, `api/s2_paper.json` | Yin-Yang claim; o-morpholine switch; S173/S285 hypothesis — **no potencies** |
| SI DOCX | `../mmc1.docx` (~37 MB) | Captions Fig S1–S14, Scheme S1, Tables S1–S2 **MM-GBSA only** |
| SI text extracts | `../mmc1_document.txt`, `../mmc1_extract.txt`, `mmc1_fulltext_deep.txt` | Confirmed **zero** `Ki`/`IC50`/`EC50`/`nM` in SI prose |
| SI Scheme S1 OCR | `../image15*_ocr.txt`, `../gr4_*_ocr.txt` | Full compound map incl. **14/15/20/24** identities |
| SI HTRF OCR | `../image11_ocr.txt` (CB1 ant), `../image12_ocr.txt` (CB2 ant), `../image13_ocr.txt` (CB2 ago) | Dose–response **curves** for series; **no** tabulated EC50/IC50 labels |
| Graphical abstract OCR | `../ga1_lrg_ocr.txt` + image | Qualitative CB1-ant / CB2-ago schematic |
| Main figures (open preview images) | `../gr1_lrg.jpg`…`gr5_lrg.jpg` | Design / docking / MD / synthesis of 10 & iso-10 — **no SAR potency tables** |
| MM-GBSA (SI Tables S1/S2) | SI text | **Compute scores only** (see audit); e.g. cpd **14** CB2(6PT0) dG Bind **−95.436**; **15** CB1 **−63.823** / CB2(5ZTY) **−104.222**; **20** CB1 **−77.848**; **24** CB1 **−57.177** |
| Citing articles (multi-source) | `api/openalex_citing.json`, `api/europepmc_citations.json` | **1** citing paper (Chen 2025 peptide) |
| Author follow-up | `api/epmc_photoswitch.json`, Crossref | Qiu/Tao 2026 *Eur. J. Med. Chem.* **Azo23** photoswitch — **not** Qiu-14 reuse |
| Patents (Google Patents HTML) | `api/gp_WO2022026478.html`, `api/gp_US20230234928.html`, `*_text.txt` | Makriyannis claim themes + Compound 1 Ki |
| Chem DB exact queries | `api/pubchem_*`, `api/chembl_inchikey_*` | Confirmed **NOT FOUND** for 14/15/20/24 |

---

## Attempted — blocked / empty

| Route | Result | Evidence |
|-------|--------|----------|
| **Unpaywall** (`email=janusforge.research@gmail.com`) | `is_oa=false`, `oa_status=closed`, `oa_locations=[]`, `has_repository_copy=false` | `api/unpaywall.json` |
| **EuropePMC full text** | `isOpenAccess=N`, `inEPMC=N`, `hasPDF=N`, subscription DOI only | `api/europepmc_article.json` |
| **CORE** | `totalHits=0` | `api/core_doi.json` |
| **OpenAlex OA** | `best_oa_location=null`, `has_fulltext=false` | `api/openalex_work.json` |
| **Semantic Scholar OA PDF** | empty `openAccessPdf.url`; `citationCount=0` (index lag vs OpenAlex) | `api/s2_paper.json`, `api/s2_citations.json` |
| **SSRN** abstract_id=4276225 | HTTP **403**; local `qiu_ssrn_*.pdf` = Cloudflare / Wayback abstract shells | prior + this pass |
| **ScienceDirect HTML dump** | ~1.2 MB SPA shell; **0** pharmacology lines after script strip; “Purchase” UI | `../sciencedirect.html` |
| **Main tables t1–t4 images** | **189 B stubs** (NOT FOUND payloads) | `../t1.jpg`…`t4_lrg.jpg` |
| **Wayback DOI** | only 302 redirects to publisher; **no** archived full PDF | `api/wayback_doi_cdx.json` |
| **Wayback ScienceDirect PII** | empty CDX | `api/wayback_sd_cdx.json` |
| **ResearchGate** | no usable author PDF hit in this pass | web search |
| **Espacenet** | HTTP **403** to scraper | this pass |
| **BindingDB** REST/web SMILES | **404** / endpoint not usable | `api/bindingdb_*.json` |
| **Author manuscript / PMC** | `authMan=N`, `nihAuthMan=N` | EuropePMC |
| **Sci-Hub-style** | **Not used** — no prior legal project precedent for Qiu | repo grep |

Legacy stub: `../am.pdf` = 219 B error (prior Unpaywall/AM attempt).

---

## Quantitative pharmacology (Ki / IC50 / EC50)

| Endpoint | Status after exhaustive pass |
|----------|------------------------------|
| Main-text tables (likely Table 1–n) | **BLOCKED** — paywalled PDF; table image stubs |
| SI numeric pharmacology tables | **NOT PRESENT** in mmc1 text (only MM-GBSA + figure curves) |
| Figure-estimated EC50 from OCR | **NOT recoverable** — axes are log[Cpd] without annotated nM labels |
| PubChem / ChEMBL / BindingDB | **CONFIRMED NOT FOUND** (exact InChIKey/SMILES) |

**Honest close:** exhaustive public + local avenues **do not** yield published numeric Ki/IC50/EC50 for compounds **14/15/20/24**. Remaining path = **institutional/personal Elsevier access** (or author request), then re-parse tables.

---

## API dump index (`api/`)

`unpaywall.json`, `openalex_work.json`, `openalex_citing.json`, `openalex_tao_works.json`, `openalex_photoswitch.json`, `europepmc_article.json`, `europepmc_citations.json`, `epmc_yinyang_search.json`, `epmc_authors_post2023.json`, `epmc_photoswitch.json`, `s2_paper.json`, `s2_citations.json`, `crossref.json`, `crossref_query.json`, `crossref_photoswitch_2026.json`, `core_doi.json`, `wayback_*`, `pubchem_*`, `chembl_inchikey_*`, `bindingdb_*`, `gp_WO2022026478.html`, `gp_US20230234928.html`, `WO2022026478_text.txt`, `US20230234928_text.txt`, `US_patent_ki_hits.txt`.
