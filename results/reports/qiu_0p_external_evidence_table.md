# 0P EXTERNAL — Primary-evidence table (user-led)

**Authority note:** This file replaces Cursor-internal 0P reports (`qiu_0p_state_of_art_audit.md`, `qiu_0p_exhaustiveness_check.md`, and similar) as the decision authority until the user decides otherwise. Prior Cursor reports may be consulted only as secondary notes after primary sources.

**Scope bans respected:** no docking/MD/NCE/wet/PDBQT work in this pass.

**Date:** 2026-08-13  
**Anchor paper:** Qiu et al., *Bioorg. Chem.* 2023, **DOI 10.1016/j.bioorg.2023.106377** (PMID 36731294)  
**Local SI:** `data/papers/mmc1.docx` / `mmc1_document.txt` / `qiu_2023_bioorg/mmc1_fulltext_deep.txt`  
**Retrieval log:** `data/papers/qiu_2023_bioorg/api/external0p/ACCESS_LOG.md` (+ CSV companion)

---

## Evidence table (primary sources only)

| Pregunta | Evidencia | Fuente primaria (DOI/PDB/patente) | Estado |
|----------|-----------|-----------------------------------|--------|
| ¿Qiu-14 está realmente sintetizado? | **Sí.** Compound **14** = N1-phenyl **ortho-morpholinyl**, C3-amide **1-adamantyl** on the pyrazole core (Scheme S1 map). Included in synthetic Scheme S1 (HATU coupling route); SI lists **HPLC** trace label `14:` and a global **“NMR Spectra of Final Ligands”** section. No small-molecule crystal structure of 14 in Fig. S2 (crystals shown for 5/6/8/9/12/13 only). Exact ¹H/¹³C shift tables for 14 are image-spectra in SI, not recoverable as numeric text here. | DOI 10.1016/j.bioorg.2023.106377 SI (mmc1 Scheme S1; HPLC/NMR final-ligand sections); OCR map `data/papers/image15_ocr.txt` | **VERIFICADO** (synthesis claimed + SI characterization present); numeric NMR tables **PARCIAL** (image-only) |
| ¿Tiene actividad CB2 experimental? | **Sí (cualitativa), numeric NOT FOUND in open sources.** Fig. **S5A**: compound 14 evaluated as **CB2 agonist** by **cAMP assay** (control CP55,940); mean±SEM, n=3 indep. × triplicate. Series CB2-agonist HTRF/cAMP curves also in Fig. S13 (OCR incomplete for “Cpd 14” panel). **No Ki / EC50 / %Emax numbers** in SI prose or OCR axes. PubChem/ChEMBL exact lookups for 14: empty. Main-text SAR tables paywalled. | DOI 10.1016/j.bioorg.2023.106377 SI Fig. S5 caption (`mmc1_document.txt`); abstract (EuropePMC/PubMed) claims Yin-Yang CB2 agonism for ortho-morpholine series | **PARCIAL** (assay + direction VERIFICADO; potency numbers **BLOQUEADO**/NOT FOUND publicly) |
| ¿Tiene actividad CB1 experimental? | **Sí (cualitativa), numeric NOT FOUND in open sources.** Fig. **S5B**: compound 14 as **CB1 antagonist** by **cAMP assay** (control rimonabant); same stats. Series CB1-antagonist curves Fig. S11. No tabulated IC50/Ki in SI. | DOI 10.1016/j.bioorg.2023.106377 SI Fig. S5 / S11 | **PARCIAL** (assay + direction VERIFICADO; potency numbers **BLOQUEADO**/NOT FOUND publicly) |
| ¿Es realmente Janus CB1/CB2? | **Sí, as published Yin-Yang claim for the ortho-morpholine pyrazole (compound 14 highlighted).** Abstract: antagonist at CB1 and concurrently agonist at CB2; ortho-morpholine is the bifunctional switch. SI Fig. S5 shows **both** arms for compound 14 in the same figure. This is functional dual pharmacology in recombinant cAMP assays — **not** in vivo Janus proof, **not** fibrosis efficacy. | DOI 10.1016/j.bioorg.2023.106377 abstract (EuropePMC JSON) + SI Fig. S5 | **VERIFICADO** (paper’s own functional claim); in vivo/fibrosis **NOT FOUND** for Qiu-14 |
| ¿Qué otros ligandos CB2 se parecen estructuralmente? | Neighbors **named by Qiu SI** for pose comparison (same chemotype family / dual-profile exemplars, not Tanimoto calc here): **AM1710**, **URB447**, **GW405833** (Fig. S8). Primary pharmacology identities: **URB447** = first mixed **CB1 antagonist / CB2 agonist** (pyrrole; DOI 10.1016/j.bmcl.2008.12.059, PMID 19128970). **GW405833** = CB2-selective agonist (DOI 10.1016/j.neuropharm.2004.12.008, PMID 15814101). **AM1710** = CB2-selective cannabilactone agonist (DOI 10.1021/jm070441u, PMID 18038967). Qiu-14 itself is a **1-adamantyl pyrazole-3-carboxamide** with o-morpholino-phenyl — closer in scaffold class to rimonabant/AM-style pyrazoles than to cannabilactones. | Qiu SI Fig. S8 captions; DOIs above | **VERIFICADO** (identity + primary refs); quantitative similarity metrics **NOT FOUND** (not computed; banned docking) |
| ¿Hay complejos CB2–ligando experimentales? | **Sí.** Key entries (RCSB REST/GraphQL 2026-08-13): **5ZTY** — X-ray **2.8 Å**, ligand **AM10257** (chem_comp **9JU**), DOI **10.1016/j.cell.2018.12.011** (PMID 30639103). **6PT0** — cryo-EM **3.2 Å**, agonist **WIN 55,212-2** (**WI5**)+Gi, DOI **10.1016/j.cell.2020.01.007** (PMID 32004460). **6KPC** — X-ray **3.2 Å**, agonist **AM12033**-class ligand (**E3R**), DOI **10.1016/j.cell.2020.01.008** (PMID 32004463). **8GUR** / **8GUS** — cryo-EM CP55,940- and HU-308-bound CB2–G (~2.8–3.0 Å), DOI **10.1038/s41467-023-37112-9** (PMID 36922494). **No experimental CB2–Qiu-14 complex.** | PDB 5ZTY, 6PT0, 6KPC, 8GUR, 8GUS + DOIs | **VERIFICADO** |
| ¿Qué interacciones están demostradas experimentalmente? | **For Qiu-14: NOT FOUND experimentally.** Abstract proposes H-bonds to **S173 (CB1)** and **S285 (CB2)** from **docking + MD only** — not mutagenesis/crystal for 14. Broader CB2 structure papers (e.g. Li et al. 2019, PDB 5ZTY) report mutagenesis supporting ligand recognition for **their** ligands (AM10257 etc.), not Qiu-14. Ballesteros–Weinstein mapping of S173/S285 for Qiu-14 remains a **hypothesis**, not an experimental fact in open primary text. | Qiu abstract DOI 10.1016/j.bioorg.2023.106377; contrast Li et al. DOI 10.1016/j.cell.2018.12.011 | **NOT FOUND** (experimental for Qiu-14); structure-paper mutagenesis for other ligands **VERIFICADO** separately |
| ¿Nuestra hipótesis Janus ya está publicada? | **Split answer.** (A) Monomolecular **CB1-ant / CB2-ago** (“Yin-Yang”): **Sí** — Qiu 2023; earlier precedent URB447 2009. (B) Same dual profile **specifically as a fibrosis therapy with Qiu-14 / Qiu chemotype**: **NOT FOUND** in PubMed (`"CB1 antagonist" AND "CB2 agonist" AND fibrosis` → 2 hits, neither Janus–Qiu–fibrosis: PMID 27028843 MSC homing; PMID 17412522 ECS/fibrosis review). (C) **Concept** of mixed CB1-ant/CB2-ago compounds for **liver/lung/kidney fibrosis**: claimed in Makriyannis family **WO2022026478** / **US20230234928** (different scaffolds; inventory only, not FTO). | Qiu DOI 10.1016/j.bioorg.2023.106377; URB447 DOI 10.1016/j.bmcl.2008.12.059; WO2022026478; PubMed esearch 2026-08-13 | **PARCIAL** — pharmacology Yin-Yang **VERIFICADO**; Qiu-14-for-fibrosis **NOT FOUND**; fibrosis dual-ligand **concept in patent** |
| ¿Está protegida por patente (Qiu-14 / familia)? | **NOT FOUND** for Qiu-14 / Qiu–Tao Yin-Yang pyrazole composition in Google Patents inventor/keyword probes (Yanli Qiu / Houchao Tao cannabinoid; “Yin-Yang” cannabinoid pyrazole → unrelated hits). Espacenet scraper **403**. Local full-text of WO2022026478 / US20230234928: **no** Qiu/Tao/ortho-morpholine-adamantyl match. Related **inventory** (not claiming Qiu-14): Makriyannis fibrosis mixed CB1/CB2 family WO2022026478. | Google Patents XHR 2026-08-13; WO2022026478; US20230234928 | **NOT FOUND** (Qiu-14 composition); related family inventory **VERIFICADO** |
| ¿Qué queda sin responder? | (1) **Numeric** CB1/CB2 potencies (Ki/IC50/EC50/%Emax) for **14/15/20/24** — locked in paywalled main tables. (2) Experimental proof of **S173/S285** contacts for Qiu-14. (3) Any **in vivo / fibrosis** primary data for Qiu-14. (4) Definitive **CN/WO composition filing** by authors (may exist offline / CNIPA not scraped). (5) Independent replication outside Qiu lab. | — | **hueco real** (see below) |

---

## Post-2023 citing Qiu (primary list)

| Year | DOI | Title | Notes |
|------|-----|-------|-------|
| 2025 | 10.1016/j.bioorg.2025.108770 | A novel CB2 agonist peptide with bone-promoting activity | Sole OpenAlex/EuropePMC citer located (Chen et al.); peptide CB2 agonist — not Qiu-14 reuse |
| 2026 | 10.1016/j.ejmech.2026.118883 | A photoswitchable ligand for opposite control over cannabinoid receptors CB1 and CB2 | Same first/senior authors (Qiu/Tao); **photoswitch Azo** series — related Yin-Yang theme, **not** a citation dump of compound 14 identity in Crossref metadata alone |

---

## Compound identity quick map (from SI Scheme S1 OCR)

| Cpd | R1 (N1-phenyl) | R3 (amide) |
|-----|----------------|------------|
| **14** | Morpholinyl, **ortho** | 1-adamantyl |
| 15 | Morpholinyl, meta | 1-adamantyl |
| 20 | 4-Methylpiperazinyl, ortho | (Group I adamantyl series) |
| 24 | Morpholinyl, ortho | CH₂-1-adamantyl |

---

## HUECO REAL → siguiente movimiento

**Gap that blocks a money-smart decision:** published **numbers** (and any fibrosis/in vivo claim) for Qiu-14 sit behind the Elsevier paywall; SI only proves synthesis + cAMP **direction**, not potency or disease relevance.

**Next move (prefer saving money):** obtain the Qiu 2023 main PDF once — cheapest path first: **email corresponding authors** (Houchao Tao / Xiaodi Yang / Suwen Zhao per PubMed affiliations) requesting the published potency table for compounds **14/15/20/24** (or a sharing-compliant PDF). If no reply in a short window, buy/access the single article (~institutional or publisher pay-per-view). **Do not** spend on docking, MD, resynthesis, or wet assays until those numbers are in hand and show the dual profile is potent enough to matter.

---

## Optional machine-readable table

See `qiu_0p_external_evidence_table.csv` in this folder.
