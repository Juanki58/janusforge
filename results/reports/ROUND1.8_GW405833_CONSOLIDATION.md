# ROUND1.8_GW405833_CONSOLIDATION

**Mission:** Consolidate exclusively recovered primary evidence from Valenzano et al. (2005) and close GW405833 documentary status.  
**Date of this pass:** 2026-08-17  
**Primary source (exclusive):** Valenzano et al., *Neuropharmacology* **48**(5):658–672. DOI `10.1016/j.neuropharm.2004.12.008`  
**Cross-reference (read-only; not overwritten):** `ROUND1.6_GW405833_PRIMARY_RESOLUTION.md`, `ROUND1.7_GW405833_FUNCTIONAL_TEXT_EXTRACT.md`  
**Integrity:** No infer / reconcile / vote / fill. No Gemini / PubChem / Tocris / reviews / secondary chemistry as primary substitute. No models / docking / QSAR / classification / git. No other compound touched. No promotion to CONFIRMED / Gold. Pipeline **STOP** after this file.

---

## A. IDENTITY

| Field | Value |
| --- | --- |
| Name | **GW405833** |
| Source | Valenzano et al. 2005, *Neuropharmacology* **48**(5):658–672 |
| Exact DOI | **`10.1016/j.neuropharm.2004.12.008`** (PMID **15814101**; PII `S0028-3908(05)00009-2`) |
| Wrong DOI (do not use) | `10.1016/j.neuropharm.2005.01.010` = Pertwee et al. 2005 (different paper) |
| Recovered primary evidence | **Abstract only** (PubMed / EuropePMC native text). Full PDF / HTML body / Fig. 1 / pharmacology tables = **NOT_FOUND** (ROUND1.6–1.7). |

### Abstract quote (functional identity; quote fidelity re-checked)

> “For the first time, we show that **GW405833** selectively binds both **rat and human CB2** receptors with high affinity, where it acts as a **partial agonist** (**approximately 50%** reduction of **forskolin-mediated cAMP** production compared to the full cannabinoid agonist, **CP55,940**).”

Also from abstract (identity / class language):

> “**GW405833**, a **selective CB2 agonist**…”

**Recovered primary claims (abstract):**

- Compound name **GW405833** stated.
- Selective **CB2** agonist / selective high-affinity binding at **rat and human CB2**.
- Functional nature: **partial agonist** on forskolin-mediated **cAMP** vs full agonist **CP55,940**, with qualitative efficacy **approximately 50%**.

**Not in recovered abstract (do not invent):** synonym **L-768242 / L-768,242**; explicit CB1 numeric binding cells; methods cell-line string **CHO-K1**; Fig. 1 structure; any EC50; exact Emax **48 ± 4%**.

---

## B. FUNCTIONAL ASSAY

Documented from recoverable Valenzano **abstract** only. Historical system labels retained with status tags — **not** elevated to primary-locked.

| Attribute | Documented value | Primary status (this path) |
| --- | --- | --- |
| Receptor | **human CB2** (abstract: “human CB2”; binding also “rat and human CB2”) | **VERIFIED** (abstract language) as hCB2 context for the cAMP partial-agonist sentence |
| System | **CHO-K1** (historical claim / MeSH “CHO Cells”) | **NOT_RECOVERED** from accessible primary abstract prose; MeSH/indexing is **not** a Methods quote → keep as **REVIEW_REQUIRED** for future full-text recovery |
| Readout | Inhibition of **forskolin-mediated / forskolin-stimulated cAMP** production | **VERIFIED** (abstract) |
| Pharmacological nature | **Partial agonist** | **VERIFIED** (abstract) |
| Qualitative response | **Approximately 50%** reduction vs full agonist **CP55,940** | **VERIFIED** (abstract) — qualitative / approximate only |

**Hard rule:** do **not** transform “approximately 50%” into “48 ± 4%”.

---

## C. NUMERIC OWNERSHIP

Historical numeric claims are **retained for traceability** and marked unverified. They are **not** deleted and are **not** introduced into Gold.

| Claim (historical) | Ownership from recoverable Valenzano primary this path | Status |
| --- | --- | --- |
| EC50 = **14 ± 2 nM** | Literal string **not** in abstract; pharmacology table/figure **not** recovered | **NOT_VERIFIED** / **NOT_RECOVERED** → **UNVERIFIED** / **REVIEW_REQUIRED** (keep historical record) |
| Emax = **48 ± 4%** | Literal string **not** in abstract; abstract has only **approximately 50%**; table/figure **not** recovered | **NOT_VERIFIED** / **NOT_RECOVERED** → **UNVERIFIED** / **REVIEW_REQUIRED** (keep historical record) |

**Traceability (do not delete):**

| Historical record | Content | Disposition |
| --- | --- | --- |
| ROUND1.6 §4–5, §7 | Ownership of **14 ± 2 / 48 ± 4** = **NOT_VERIFIED** | Preserved; cross-ref only |
| ROUND1.7 §3–5 | Literal **14 ± 2** = **N**; literal **48 ± 4** = **N** | Preserved; cross-ref only |
| Round1 CSV EC50 **0.65 nM** | Historically recorded for GW405833 functional row | Remains historically recorded; **also not verified** from recoverable abstract text this path (optional note; no invention; no reconciliation with 14 ± 2) |

No averaging, voting, or substitution between **14 ± 2**, **48 ± 4**, **approximately 50%**, or **0.65 nM**.

---

## D. STRUCTURE

| Endpoint | Status |
| --- | --- |
| Fig. 1 | Still **inaccessible** / **NOT_FOUND** (ROUND1.6) |
| Structure | **REVIEW_REQUIRED** |
| SMILES | **REVIEW_REQUIRED** |

No structure or SMILES asserted as primary without Fig. 1. PubMed ChemicalList / MeSH strings are **not** accepted as Fig. 1 substitutes.

---

## E. RESOLUTION

**Final status: `GW405833 = REVIEW_REQUIRED`**

**Exact reason:**

> Primary functional identity and qualitative partial-agonist activity are verified from the recoverable Valenzano 2005 abstract, but exact numerical ownership of EC50 = 14 ± 2 nM and Emax = 48 ± 4% is not recovered from accessible primary text.

**Not promoted:** CONFIRMED / Gold / Subset A lock.

**Confirmed from recoverable abstract (this closure):**

- Name **GW405833**; DOI `10.1016/j.neuropharm.2004.12.008`
- Selective CB2 agonist; high-affinity binding language at rat and human CB2
- Partial agonist on forskolin-mediated cAMP vs CP55,940
- Qualitative efficacy **approximately 50%**

**Undemonstrated / not recovered from accessible primary text:**

- EC50 = **14 ± 2 nM** (historical → **UNVERIFIED** / **REVIEW_REQUIRED**; retained)
- Emax = **48 ± 4%** (historical → **UNVERIFIED** / **REVIEW_REQUIRED**; retained; ≠ “approximately 50%”)
- Round1 CSV EC50 **0.65 nM** (historical; not in abstract)
- Structure / SMILES (Fig. 1 unrecovered → **REVIEW_REQUIRED**)
- Cell system **CHO-K1** as Methods-locked primary prose (abstract silent; MeSH only)

**Pipeline:** **STOP**

---

## Parent return

| Field | Value |
| --- | --- |
| File created | `results/reports/ROUND1.8_GW405833_CONSOLIDATION.md` |
| Final status | **`GW405833 = REVIEW_REQUIRED`** |
| Claims confirmed | Identity GW405833 + Valenzano DOI; selective CB2 / rat+human CB2 binding language; partial agonist; forskolin cAMP; ~50% vs CP55,940 |
| Claims undemonstrated | EC50 14±2 nM; Emax 48±4%; structure/SMILES; CHO-K1 Methods lock; Round1 CSV 0.65 nM |
| Pipeline | **STOP** |
| Integrity | This file only; no other compound; no Gold promotion; historical 14±2 / 48±4 retained as UNVERIFIED/REVIEW_REQUIRED |
