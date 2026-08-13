# ACCESS_LOG — 0P EXTERNAL primary retrieval (2026-08-13)

Rule: log every attempt; do not invent Ki/IC50/EC50.

## Local primary artifacts (read)

| Artifact | Path | Result |
|----------|------|--------|
| SI DOCX/text | `data/papers/mmc1.docx`, `mmc1_document.txt`, `mmc1_extract.txt`, `qiu_2023_bioorg/mmc1_fulltext_deep.txt` | Scheme S1, Fig S5/S11–S13 captions, HPLC labels incl. 14, MM-GBSA only — **no** nM tables |
| Scheme OCR | `data/papers/image15_ocr.txt`, `gr4_*_ocr.txt` | Compound **14/15/20/24** identities |
| Assay OCR | `image11_ocr.txt` (CB1 ant), `image12_ocr.txt` (CB2 ant), `image13_ocr.txt` (CB2 ago) | Dose–response curves; **no** annotated EC50; OCR missed explicit “Cpd 14” on S13 (S5 covers 14) |
| Graphical abstract OCR | `ga1_lrg_ocr.txt` | Qualitative Yin-Yang schematic |
| PubMed HTML dump | `data/papers/pubmed.html` | Full abstract text |
| Prior API cache (secondary to this pass) | `qiu_2023_bioorg/api/*` | Unpaywall closed; PubChem/ChEMBL empty; patent HTML for WO/US |

## Network retrievals (this pass → `api/external0p/`)

| # | Target | URL / method | HTTP / note | Saved |
|---|--------|--------------|-------------|-------|
| 1 | PDB 6PT0 entry | `https://data.rcsb.org/rest/v1/core/entry/6PT0` | 200 — WIN 55,212-2 complex, 3.2 Å, DOI 10.1016/j.cell.2020.01.007 | `pdb_6pt0.json` |
| 2 | PDB 5ZTY entry | `https://data.rcsb.org/rest/v1/core/entry/5ZTY` | 200 — 2.8 Å, DOI 10.1016/j.cell.2018.12.011 | `pdb_5zty.json` |
| 3 | PDB CNR2 search (complex JSON) | RCSB Search API | **400** | `pdb_cnr2_search.json.err.txt` |
| 4 | PDB CNR2 search (simple) | RCSB Search API | **400** | `pdb_cnr2_simple.json` fail |
| 5 | Unpaywall refresh | `api.unpaywall.org/v2/10.1016/j.bioorg.2023.106377` | 200 — `is_oa=false`, no repository copy | `unpaywall_refresh.json` |
| 6 | EuropePMC refresh | EBI search DOI | 200 — OA=N, PDF=N, citedByCount=1 | `epmc_refresh.json` |
| 7 | OpenAlex citing (DOI filter) | openalex.org/works?filter=cites:doi… | **400** | err |
| 8 | OpenAlex citing (W4317627134) | filter=cites:W4317627134 | 200 — **1** work (Chen 2025) | `openalex_citing2.json` |
| 9 | Google Patents HTML search | patents.google.com/?q=Yin-Yang… | 200 — SPA shell only | `gp_qiu_search.html` |
| 10 | Espacenet search | worldwide.espacenet.com/… | **403** | `espacenet_qiu.html.err.txt` |
| 11 | PubMed URB447 | eutils esearch | 200 — 7 hits | `pubmed_urb447.json` |
| 12 | PubMed GW405833 | eutils esearch | 200 — 43 hits | `pubmed_gw405833.json` |
| 13 | PubMed AM1710 | eutils esearch | 200 — 20 hits | `pubmed_am1710.json` |
| 14 | PubMed Janus+fibrosis | `"CB1 antagonist" AND "CB2 agonist" AND fibrosis` | 200 — **2** hits (not Qiu-14) | `pubmed_janus_fibrosis.json` + `pubmed_sum_janus.json` |
| 15 | PubMed LoVerme URB447 | esearch+esummary | 200 — PMID 19128970, DOI 10.1016/j.bmcl.2008.12.059 | `esearch_urb447_primary.json` |
| 16 | PubMed GW405833 primary | esearch+efetch | 200 — PMID 15814101, DOI 10.1016/j.neuropharm.2004.12.008 | `efetch_gw405833.xml` |
| 17 | PubMed AM1710 primary | efetch PMID 18038967 | 200 — DOI 10.1021/jm070441u | `efetch_am1710.xml` |
| 18 | PubMed Li 2019 CB2 | efetch PMID 30639103 | 200 — DOI 10.1016/j.cell.2018.12.011 | `efetch_li_5zty_mut.xml` |
| 19 | GP XHR inventor Tao | patents.google.com/xhr/query… | 200 — query syntax error | `gp_inventor_tao.json` |
| 20 | GP XHR inventor Qiu | same | 200 — query syntax error | `gp_inventor_qiu.json` |
| 21 | GP XHR “Yin-Yang” cannabinoid pyrazole | xhr/query | 200 — 3 **unrelated** patents | `gp_yinyang.json` |
| 22 | PDB 6KPC / 6KPF / 8GUR / 8GUS | REST entry | 200 | `pdb_6KPC.json` etc. |
| 23 | PDB ligands GraphQL | data.rcsb.org/graphql | 200 — 6PT0 WI5; 5ZTY 9JU; 6KPC E3R | `pdb_ligands_graphql.json` |
| 24 | WebSearch URB447 / 6PT0 / 5ZTY / patents Qiu | Cursor WebSearch | used for DOI confirmation + negative patent hit synthesis | — |
| 25 | ScienceDirect / SSRN full PDF | not re-fetched as full OA (prior: closed / 403) | Main text remains **BLOQUEADO** | — |
| 26 | Sci-Hub-style | **Not used** | — | — |

## Honest close

Public + local SI evidence supports **synthesis** and **qualitative dual cAMP pharmacology** for Qiu compound 14. **Numeric potencies** and any **fibrosis/in vivo** claim for Qiu-14 remain unavailable without the paywalled main PDF or author share.
