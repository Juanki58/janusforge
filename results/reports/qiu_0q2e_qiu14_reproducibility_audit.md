# 0Q.2E-FINAL — Qiu-14 post-publication reproducibility audit (R0–R4)

**Date:** 2026-08-15  
**Anchor:** Qiu et al., *Bioorg. Chem.* 2023, **DOI [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377)** (PMID 36731294; OpenAlex `W4317627134`)  
**Molecule:** Qiu-14 = N1-*o*-morpholinophenyl, C3-CONH-1-adamantyl pyrazole-3-carboxamide  
**0D identity:** SMILES `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` · InChIKey `QQXQVTJJXRACOB-UHFFFAOYSA-N` (`qiu_0d_structure_verification.md`)  
**Scope:** later appearances of **Qiu-14 / compound 14** only — not a broad cannabinoid SAR review.  
**Bans respected:** no docking, MD, NCE, or invented papers.

---

## Rank definitions

| Rank | Meaning |
|------|---------|
| **R0** | Citation of Qiu 2023 only (no Qiu-14 molecule use) |
| **R1** | Mentions Qiu-14 / compound 14 identity |
| **R2** | Uses the molecule but does not measure function |
| **R3** | Measures function (any arm) |
| **R4** | Independent reproduction CB1 **and** CB2 |

---

## Methods (verify + extend prior 0P)

| Source | Query / artifact | Result (2026-08-15) |
|--------|------------------|---------------------|
| **OpenAlex** | work DOI → `cited_by_count=1`; `filter=cites:W4317627134` | **1** citer: Chen 2025 |
| **EuropePMC** | `/MED/36731294/citations` | **1** citer: PMID 40714479 (Chen 2025) |
| **Crossref** | work `is-referenced-by-count` | **1** |
| **NIH iCite** | PMID 36731294 | `citation_count=1`; `cited_by=[40714479]` |
| **Scite** | tallies DOI | `citingPublications=1` (supporting/contradicting tallies 0) |
| **Semantic Scholar** | paper + citations | `citationCount=0` / empty list (**index lag** vs OpenAlex/Crossref/iCite) |
| **Google Scholar** | DOI exact-phrase fetch | HTML shell retrieved; no additional citer beyond the indexed n=1 consensus |
| **WebSearch** | Yin-Yang / ortho-morpholine / InChIKey / compound 14 | Hits resolve to Qiu 2023 itself or unrelated scaffolds; no third-lab Qiu-14 assay |
| **PubChem** | InChIKey / SMILES PUG | InChIKey **404**; SMILES → **CID 0** (not deposited) |
| **ChEMBL** | `molecule_structures__standard_inchi_key=` | **0** molecules |
| **Prior 0P** | `qiu_0p_external_evidence_table.md`; ACCESS_LOGs | Same sole citer (Chen); chem DBs empty — **confirmed** |
| **Author follow-up check** | Qiu/Tao 2026 Azo23 DOI 10.1016/j.ejmech.2026.118883 | Same author cluster; **Crossref refs do not include** 106377; abstract = **Azo23** (not Qiu-14) |
| **False-positive check** | Bo/Zhao/Li *Clin. Sci.* 10.1042/cs20231156 | Crossref references: **no** Qiu 2023 DOI |

API dumps for this pass: `data/papers/qiu_2023_bioorg/api/0q2e/`.

---

## Source datum (not a “later appearance”)

| Field | Status |
|-------|--------|
| Synthesis + SI characterization of compound **14** | Original lab (Qiu/Tao et al. 2023 + SI mmc1) |
| Functional CB2 agonist + CB1 antagonist (cAMP / HTRF; SI Fig. S5) | **Same single lab** |
| Numeric Ki/IC50/EC50 in open sources | **NOT FOUND** (paywalled main text; SI lacks tabulated potencies) |
| Independent wet replica | **NOT FOUND** (this audit) |

---

## Post-publication appearances of Qiu-14

| Appearance | Year | DOI | What they did with Qiu-14 | Rank | Evidence |
|------------|------|-----|---------------------------|------|----------|
| Chen et al., *Bioorg. Chem.* — “A novel CB2 agonist peptide with bone-promoting activity” | 2025 | [10.1016/j.bioorg.2025.108770](https://doi.org/10.1016/j.bioorg.2025.108770) (PMID 40714479) | **Nothing.** Paper screens/validates **peptides** as CB2 agonists (cAMP in HEK293-CB2; osteoblast readouts). Qiu 2023 appears only in the reference list. | **R0** | Sole OpenAlex/EuropePMC/Crossref/iCite/Scite citer; EPMC abstract names peptides APOCB2R3/4/7 only; Crossref ref key `…_bb0145` = DOI 10.1016/j.bioorg.2023.106377; chemotype ≠ Qiu pyrazole |

**n appearances (post-publication) = 1**  
**Max rank found = R0**

### Checked related items (not Qiu-14 appearances)

| Item | Year | DOI | Why excluded |
|------|------|-----|--------------|
| Qiu/Zhao/Hu/Tao et al. photoswitch **Azo23** | 2026 | [10.1016/j.ejmech.2026.118883](https://doi.org/10.1016/j.ejmech.2026.118883) | Same lab/theme (bifunctional CB1/CB2), **different molecule** (azo photoswitch; cis = CB1 ago + CB2 ant). Does **not** cite Qiu 2023 in Crossref metadata; abstract never names compound 14. |
| Structure DBs (PubChem / ChEMBL / prior BindingDB) | — | — | Exact SMILES/InChIKey **not deposited**; no third-party bioactivity rows. |
| Lab publication lists / SSRN preprint of Qiu 2023 | — | — | Self-listing of the source paper, not external reuse. |

---

## Max rank & conclusion

**Maximum rank found: R0**

No R1–R4 hit was located. No independent lab has been shown to (i) name Qiu-14, (ii) procure/synthesize it, or (iii) measure CB1 and/or CB2 function on that exact structure after Qiu et al. 2023.

**Bridge RFQ framing:** the only known functional data on Qiu-14 remain those of the **original Qiu/Tao laboratory** (SI cAMP directions; potencies still largely paywalled). A third-party CRO bridge assay on Qiu-14 is therefore a **well-defined independent reproduction** of a published validation vehicle — **not** open exploration of an uncharacterized chemotype.

**Recommendation — treat bridge assay as independent reproduction: YES**

---

## Limitations (honest)

- Qiu 2023 main PDF remains closed OA; this audit does not invent potencies.
- Chen 2025 full text is subscription; classification uses abstract + Crossref reference list (sufficient for **R0** vs R1+).
- Semantic Scholar and Google Scholar UIs lag or are JS-gated; multi-source citation APIs agree on **n = 1**.
- Index lag could add future citers; none currently elevate above R0 for Qiu-14.
