# ROUND1 ORDEN 2 — AM1710 / AM1714 Contradiction Audit

**Executor:** Cursor Pro (contradiction auditor — NOT literature-consensus seeker)  
**Date:** 2026-08-17  
**Primary target:** Khanolkar AD et al., *J. Med. Chem.* **2007**, **50**, **6493–6500**, DOI **10.1021/jm070441u**, PMID **18038967**  
**Scope:** Identity ownership of **4b** vs **5**; hunt for label inversion; 5 / 5a / 5b; binding vs functional; human vs rat/mouse.  
**Hard rules applied:** No majority vote; no PubChem/IUPHAR/Wikipedia/reviews as authority; no docking/models/QSAR/git; every matrix cell TRACEABLE to a cited primary snippet/location or marked **NOT_FOUND** / **UNRESOLVED**.

---

## 0. Recovery inventory (this pass)

| Asset | Status | Path / note |
| --- | --- | --- |
| New Gemini primary ACS PDF/HTML/OCR/screenshots of Tables 1–2 | **NOT_FOUND** | Workspace scan (`results/reports`, `data/papers/_recon_tmp`, `*GEMINI*`, `*ADVERSARIAL*`, `*AM171*`) found **no** new Gemini-deposited ACS table extracts this pass |
| ACS full PDF / full HTML | **NOT_FOUND** | Paywall / prior 403; no local `%PDF-` article body |
| ACS SI PDF | **NOT_FOUND** as PDF | Local `data/papers/_recon_tmp/khanolkar_si.pdf` begins `<!DOC…` (HTML challenge), size 5652 B — not pharmacology tables |
| EuropePMC full text | **NOT_FOUND** | `isOpenAccess=N`, `inEPMC=N`, publisher = subscription (`data/papers/_recon_tmp/epmc_khanolkar.json`) |
| Opened primary text | **Abstract only** | PubMed dump `data/papers/_recon_tmp/r14_pubmed_khanolkar.txt`; EuropePMC `abstractText` same wording; ChEMBL document abstract mirrors ACS abstract (used only to confirm abstract identity string, **not** for Ki/EC50 cells) |
| Round 1.4 / 1.5 | Contradiction **claims** only | Read for Gemini claim inventory; **not** treated as primary evidence |

**Pagination note (primary metadata):** PubMed/EuropePMC print pages = **6493–6500** (issue 26). Mission-wrong range **4496–4506** = citation error, same DOI.

---

## 1. Contradiction claims under audit (from prior Gemini / Round 1.3–1.5 — claims only)

| ID | Claim (non-primary) | What auditor must do |
| --- | --- | --- |
| C1 | AM1710 = compound **5a** | Test against ACS/PubMed abstract numbering |
| C2 | Compound **5** / **5a** / **5b** confusion; possible **4b↔5** label inversion | Separate codes; require same-source row ownership |
| C3 | Khanolkar Table 2: AM1710 (as 5a) GTPγS EC50 **11.2 ± 1.8 nM**, Emax **89 ± 3%**, **hCB2** | Require literal table cell in Khanolkar primary |
| C4 | Binding Ki package often cited as **6.7 / 360** for AM1710 as **human** | Require Table 1 + species from primary (not DB) |

---

## 2. Primary abstract evidence (DIRECT — opened)

**Source:** Khanolkar et al. 2007 abstract (PubMed efetch dump `r14_pubmed_khanolkar.txt`; EuropePMC `abstractText` for PMID 18038967).

**Verbatim core:**

> Optimal receptor subtype selectivity of **490-fold** and **subnanomolar affinity** for the CB2 receptor is exhibited by a **9-hydroxyl analog 5 (AM1714)**, while the **9-methoxy analog 4b (AM1710)** had a **54-fold** CB2 selectivity. … In vitro testing revealed that the novel compounds are **CB2 agonists**, while in vivo testing of cannabilactones **4b** and **5** found them to possess potent peripheral analgesic activity.

**MEDLINE chemical names** (EuropePMC `chemicalList`, same article record — identity language only, not Ki cells):

- `3-(1,1-dimethyl-heptyl)-1-hydroxy-9-methoxy-benzo(c)chromen-6-one` ↔ 9-methoxy (aligns with **4b / AM1710**)
- `3-(1,1-dimethyl-heptyl)-1-9-dihydroxy-benzo(c)chromen-6-one` ↔ 9-hydroxy (aligns with **5 / AM1714**)

**MeSH animals** on the same record list Mice / Rats / Animals — **does not** by itself prove recombinant **human** CB1/CB2 binding for Table 1. Species of Ki = **NOT_FOUND** without Methods/Table footnotes.

---

## 3. Matrix 4b vs 5 (primary-traceable only)

| Element | **4b** | **5** | Per-cell status | Confidence |
| --- | --- | --- | --- | --- |
| **structure** | Cannabilactone / benzo[*c*]chromen-6-one with **3-(1′,1′-dimethylheptyl)** + **6-oxo**; **9-methoxy** (abstract + MEDLINE 9-methoxy name) | Same scaffold; **9-hydroxyl** (abstract + MEDLINE dihydroxy name) | **PARTIAL** (scaffold/substituent language DIRECT in abstract; atom-by-atom drawing / SMILES from Scheme **NOT_FOUND** — PDF unrecovered) | Med (substituent); Low (full structure drawing) |
| **substituent** | **9-methoxy** | **9-hydroxyl** | **DIRECT** (abstract) | High |
| **AM-ID** | **AM1710** | **AM1714** | **DIRECT** (abstract equates **4b (AM1710)** and **5 (AM1714)**) | High |
| **Ki hCB1** | **NOT_FOUND** | **NOT_FOUND** | No numeric Ki; abstract silent on **human** CB1 | — |
| **Ki hCB2** | **NOT_FOUND** as numeric cell; abstract states **54-fold** CB2 selectivity (not Ki nM) | **NOT_FOUND** as numeric cell; abstract states **subnanomolar** CB2 affinity + **490-fold** selectivity (not Ki nM) | Selectivity language = **DIRECT** qualitative/ratio only; **h**CB2 not stated | High that numbers absent; High that “h” unproven |
| **EC50** | **NOT_FOUND** in abstract / unrecovered Table 2 | **NOT_FOUND** | Abstract: qualitative “CB2 agonists” only | High (absence) |
| **Emax** | **NOT_FOUND** | **NOT_FOUND** | No % efficacy in abstract | High (absence) |
| **exact primary evidence** | Abstract: “**9-methoxy analog 4b (AM1710)** … **54-fold** CB2 selectivity”; in vivo with **4b** | Abstract: “**9-hydroxyl analog 5 (AM1714)** … **490-fold** … **subnanomolar**”; in vivo with **5** | Location: article abstract (PubMed/EuropePMC of DOI `10.1021/jm070441u`) | High for identity; Low for any table number |

**Legend:** DIRECT = literal primary text; PARTIAL = primary language without full table/drawing; NOT_FOUND = cell empty / unrecovered; UNRESOLVED = cannot close ownership under mission rules.

---

## 4. Explicit contradiction hunts

### 4.1 Label inversion (4b ↔ 5)

| Check | Result |
| --- | --- |
| Does abstract assign AM1710 to **4b** and AM1714 to **5**? | **Yes — DIRECT** |
| Is there a second opened ACS primary (Table/Scheme) that swaps those labels? | **NOT_FOUND** (tables unrecovered) |
| Primary-vs-primary label inversion? | **Not demonstrated** (only one opened primary surface: abstract). Claim-side “5a = AM1710” is **not** ACS-table-traceable this pass → cannot score **FAIL** under “both sides primary-traceable” |

### 4.2 4b / 5 discrepancies

| Item | Finding |
| --- | --- |
| Identity ownership | Coherent in abstract: **4b = AM1710 (OMe)**; **5 = AM1714 (OH)** |
| Numeric pharmacology discrepancy between 4b and 5 | Cannot audit table cells — Tables 1–2 **NOT_FOUND** |
| Selectivity language | **5** claimed more selective (490-fold) than **4b** (54-fold) — DIRECT abstract; no contradiction within abstract |

### 4.3 Differences among **5**, **5a**, **5b**

| Code | In opened Khanolkar primary? | Status |
| --- | --- | --- |
| **5** | Yes — **AM1714**, 9-hydroxyl | **DIRECT** |
| **5a** | **Never named** in opened abstract | **NOT_FOUND** |
| **5b** | **Never named** in opened abstract | **NOT_FOUND** |

Any claim “AM1710 = **5a**” conflicts with abstract **4b = AM1710**, but the **5a** side has **no** ACS primary table citation recovered → treated as **unlocated claim**, not as a second primary.

### 4.4 Human vs rat/mouse

| Claim surface | Opened primary |
| --- | --- |
| Abstract Ki species (human vs rodent) | **NOT_FOUND** (silent) |
| Gemini claim package as **hCB2** | **NOT_FOUND** in abstract; Tables/Methods unrecovered → **UNRESOLVED** for Khanolkar species |
| MeSH Mice/Rats | Metadata hint only — **not** accepted as Table 1 species proof |

### 4.5 Binding vs functional confusion

| Layer | Opened Khanolkar primary |
| --- | --- |
| Binding (Ki) | Ratios / “subnanomolar” language only — **no** Ki nM cells |
| Functional | “CB2 agonists” qualitative — **no** EC50/Emax; assay type (GTPγS vs cyclase) **NOT_FOUND** |
| Cross-paper mix-check (NOT Khanolkar ownership) | Dhopeshwarkar & Mackie 2016 PMC4959096 Table 2 row **AM1710**: cyclase EC50 **11** nM (CI 5.5–15.6), Emax **48 ± 4.3**; arrestin EC50 **4**, Emax **91 ± 3.6**; Methods: HEK **mouse** CB2 cyclase/cAMP — **different paper, assay, species**. Literal **11.2** and **89 ± 3%** **not** in that row |

---

## 5. Ownership of **11.2** and **89**

| Value | In Khanolkar abstract? | In recovered Khanolkar Table 1/2? | Owner compound (primary) | Status |
| --- | --- | --- | --- | --- |
| **11.2** (± 1.8 nM) | **No** | Tables **NOT_FOUND** | **NOT_FOUND** | Cannot assign to 4b, 5, 5a, or AM1710 |
| **89** (± 3%) | **No** | Tables **NOT_FOUND** | **NOT_FOUND** | Cannot assign |

**Rule compliance:** Do **not** transfer Dhop **11** / **48±4.3** / arrestin **91±3.6** onto Khanolkar cells by proximity.

---

## 6. What Round 1.4 / 1.5 claimed (context only — not primary)

| Prior report | Contradiction claim used here only as hypothesis list |
| --- | --- |
| `ROUND1.4_FINAL_CONTRADICTION_RESOLUTION.md` | Gemini **5a = AM1710** vs abstract **4b**; **11.2/89** unowned |
| `ROUND1.5_AM1710_PRIMARY_OWNERSHIP.md` | Tables 1–2 **NOT_FOUND**; identity **4b** DIRECT; **11.2/89** NOT_FOUND |

This ORDEN 2 audit **re-opens** those claims against primary recovery **as of this pass** and does **not** inherit their verdicts as evidence.

---

## 7. Matrix coherence check → verdict criteria

| Criterion | Definition | This audit |
| --- | --- | --- |
| **PASS** | Matrix coherent; no unresolved primary contradictions on identity/ownership of key IDs **and numbers claimed** | **Fails criterion** — Ki/EC50/Emax ownership of claimed numbers still empty; Tables 1–2 missing |
| **FAIL** | Primary sources contradict each other on critical identity (e.g. AM1710=4b vs 5a) with **both sides primary-traceable**, OR claimed numbers cannot be assigned **without** contradiction between primaries | **Not met** — only **one** opened ACS primary surface (abstract) locks **4b=AM1710**; opposing **5a** lacks ACS table locus |
| **UNRESOLVED** | Insufficient primary table recovery to fill critical cells (typical if Tables 1–2 still missing) | **Met** |

### Overall verdict: **UNRESOLVED**

**Rationale (brief):** Abstract-only recovery locks **identity** (**4b = AM1710**, **5 = AM1714**) without a second primary that contradicts it. Critical numeric cells (**Ki hCB1/hCB2**, **EC50**, **Emax**) and ownership of **11.2 / 89** remain **NOT_FOUND** because Khanolkar Tables 1–2 were never recovered. Gemini deposits of ACS table pages were **not** located this pass. That is insufficient for **PASS** and does not meet the dual-primary bar for **FAIL**.

---

## 8. Parent return (compact)

| Field | Value |
| --- | --- |
| **Verdict** | **UNRESOLVED** |
| **AM1710 identity from ACS (opened)** | Abstract **DIRECT**: **4b (AM1710)** = 9-methoxy cannabilactone; **not** proven as **5a** (5a absent from opened primary; **5 = AM1714**) |
| **Do 11.2 / 89 appear?** | **No** in opened Khanolkar primary. Owner = **NOT_FOUND** |
| **Report path** | `results/reports/ROUND1_ORDEN2_AM1710_AM1714_CONTRADICTION_AUDIT.md` |

**PIPELINE STOP** after this deliverable.
