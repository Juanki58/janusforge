# ROUND1_GOLD_AUDIT_v1.0

**Audit date:** 2026-08-16  
**Input (read-only):** `results/reports/ROUND1_GOLD_CANDIDATES.md` (Dataset/GOLD = **2** rows)  
**Do not modify:** `CB2_Experimental_Master_Dataset_v1.0_Round1.csv`, `ROUND1_GOLD_CANDIDATES.md`  
**Rule applied:** prefer **REVIEW_REQUIRED** over **GOLD_CONFIRMED** on any unresolved check (§15–17, SMILES, SI).

---

## 0. SCOPE MISMATCH

Director expected a **7-compound GOLD set**. Current `ROUND1_GOLD_CANDIDATES.md` Dataset/GOLD has **2 rows** only (OLORINAB_func_hCB2; VICASINABIN_func_cAMP_hCB2). This audit does **not** promote any of the other five.

| Expected compound | Current status in ROUND1_GOLD_CANDIDATES | Would fail GOLD under this audit? |
|---|---|---|
| **HU-308** | **REVIEW** — `HU308_func_cAMP` (qualitative forskolin cAMP only; Round1.1 quantitative EC50/Emax not promoted) | **YES** — no clean quantitative EC50/Emax row locked to a reproducible primary table location in the GOLD file; species/system caveats on binding; SMILES/stereo not re-proven here |
| **Vicasinabin** | **GOLD** for `VICASINABIN_func_cAMP_hCB2` only; **REVIEW** for `VICASINABIN_func_barr` (Round1 ~22 nM vs primary 99.69±5.72 nM) | cAMP row: audited below (not auto-confirmed). β-arr row: **YES fail** — METRIC_CONFLICT |
| **GW405833** | **REVIEW** — `GW405833_func_hCB2_cAMP` (Valenzano PDF NOT VERIFIED); Janus arm also REVIEW | **YES** — primary PDF unrecovered; Source_Location NOT VERIFIED; Emax/system incomplete |
| **AM1710** | **No hCB2 functional GOLD row.** Binding rows treated as **Rejected** (binding-only Ki). `AM1710_Janus_CB1_inv` = **REVIEW** (P). Quarantine Q-05: EC50 “11 nM” / “11.2” claims not primary-verified | **YES** — no verified hCB2 functional EC50; EC50 11 nM quarantined; Khanolkar primary not opened; Janus ≠ hCB2 GOLD |
| **APD371 / olorinab** | **GOLD** as `OLORINAB_func_hCB2` | Audited below (Director “compound 17” is **wrong**; primary = compound **6**) |
| **CP-55,940** | **Rejected** — global ref note only (`CP55940_ref_note`); Q-12 / Q11-17 | **YES** — no single assay-locked EC50/Ki/Emax; multi-assay reference; cannot invent global number |
| **WIN55,212-2** | **Rejected** — global ref note only (`WIN55212_ref_note`); Q-12 / Q11-17 | **YES** — no single assay-locked functional datum; identity/form/assay-dependence unresolved; Soethoudt-type caveats not a GOLD row |

**Net:** expected 7 ≠ current GOLD 2. Of the five non-current-GOLD names, **all five would fail GOLD** under this audit’s bar. Do not promote.

---

## 1. AUDIT TABLE

| Compound_ID | Original_Status | Final_Status | EC50/Metric_Verified | Emax_Verified | hCB2_Verified | Cellular_System_Verified | SMILES_Verified | Source_Location_Verified | Evidence | Audit_Decision |
|---|---|---|---|---|---|---|---|---|---|---|
| OLORINAB_func_hCB2 | GOLD | REVIEW_REQUIRED | YES (EC50=6.2 nM) | YES (106% vs CP-55,940=100) | YES | PARTIAL (PathHunter named; SI methods PDF not opened) | NO | YES (Table 1 / Table 2 cmpd 6) | PMC5733264 HTML Table 1 row 6: hCB2 β-arrestin 6.2 (106); footnote b; APD371=cmpd **6** not 17; Round1 “typically cAMP” contradicts primary β-arrestin; InChIKey not regenerated from SI/structure | Demote confidence: pharmacological D-checks mostly pass; **SMILES/SI cell-line** block GOLD_CONFIRMED |
| VICASINABIN_func_cAMP_hCB2 | GOLD | REVIEW_REQUIRED | YES (EC50=2.81±0.28 nM) | N/A → treated as FAIL for GOLD_CONFIRMED (no numeric Emax; “full agonist” narrative only) | YES | YES (CHOK1hCB2_bgal, Methods 2.2.2) | NO | YES (Fig 3A + Results) | Frontiers 10.3389/fphar.2024.1426446 HTML: Results + Fig 3A; mCB2 2.60±0.14 separate; β-arr 99.69±5.72 is other row; InChIKey not regenerated from IUPAC/X-ray | Demote confidence: EC50/hCB2/system/location pass; **Emax numeric absent + SMILES** block GOLD_CONFIRMED |

Statuses used: **GOLD_CONFIRMED** | **REVIEW_REQUIRED** | **REJECTED**

---

## 2. ROW-BY-ROW FINDINGS

### 2.1 OLORINAB_func_hCB2

| # | Check | Result |
|---|---|---|
| 1 | Primary reference retrieved | **YES** — Han et al. 2017, DOI 10.1021/acsmedchemlett.7b00396, PMID 29259753, PMC5733264 |
| 2 | PDF/SI primary opened | **PARTIAL** — PMC full-text HTML + Table 1/2 inspected. ACS SI PDF (`ml7b00396_si_001.pdf`) **not** retrieved this pass (ACS 503 / EuropePMC 500). PMC PDF download page did not yield extractable body |
| 3 | Quantitative datum literal | **YES** — Table 1, compound **6**, column hCB2 (Emax): **6.2 (106)** |
| 4 | Same Compound_ID as table compound | **YES** — Abstract/conclusion: **6 (APD371)** = olorinab. **Director “compound 17” REJECTED:** Table 2 compound **17** is a different CF3 analog (hCB2 EC50 **2.3 (108)**), not APD371 |
| 5 | Unequivocal hCB2 | **YES** — Table header **hCB2** (distinct from hCB1, rCB2, rCB1) |
| 6 | Cellular system | **PARTIAL** — Main text: DiscoverX PathHunter β-arrestin assay. Catalog cell line / CHO PathHunter ID not re-read from SI Methods this pass → not full cellular-system proof |
| 7 | Assay format | **YES** — **β-arrestin recruitment** (PathHunter); explicitly **not** cAMP for the 6.2 nM table value. Text notes cAMP is less discerning and EC50s in β-arrestin are right-shifted |
| 8 | Metric | **YES** — **EC50** (nM) + parenthetical **Emax**; no Ki↔EC50 equivalence |
| 9 | Unit | **YES** — nM; Emax % |
| 10 | Emax normalization | **YES** — Footnote b: Emax relative to **CP-55,940 (100)** |
| 11 | Exact location | **YES** — **Table 1**, compound 6, hCB2 β-arrestin EC50 (Emax); echoed **Table 2** row 6 |
| 12 | SMILES / identity | **NO / NOT VERIFIED** — Stored value is InChIKey `ACSQLTBPYZSGBA-GMXVVIOVSA-N` (not a SMILES string). Stereo in Table 1 = **(S,S)** + **(S)-t-butyl**; X-ray absolute stereo cited (Fig S4) but **InChIKey not regenerated** from primary scheme/SI this audit. Secondary DBs (PubChem/GtoPdb) concord — **not** used as §16 proof |

**Round1 conflict (documented, not silent-fixed):** Round1 CSV notes “typically cAMP/functional”; primary Table 1 header = **β-arrestin EC50**. Number 6.2 nM + Emax 106% match β-arrestin, not a cAMP table.

**Audit_Decision:** **REVIEW_REQUIRED** (SMILES not primary-proven; SI cellular methods not opened). Do not overwrite GOLD MD.

---

### 2.2 VICASINABIN_func_cAMP_hCB2

| # | Check | Result |
|---|---|---|
| 1 | Primary reference retrieved | **YES** — Frontiers Pharmacol. 2024, DOI 10.3389/fphar.2024.1426446 (HTML OA; PMC11272598) |
| 2 | PDF/SI primary opened | **YES (HTML)** — Methods 2.2.2 + Results §3 functional paragraph + Fig 3A callout. PMC PDF download page did not yield separate extractable PDF body; HTML sufficient for cited numbers |
| 3 | Quantitative datum literal | **YES** — Results: human CB2R **EC50: 2.81 ± 0.28 nM** (with mouse CB2R **2.60 ± 0.14 nM** in same sentence); Abstract rounds to **2.8 nM** |
| 4 | Same Compound_ID | **YES** — RG7774 / vicasinabin; IUPAC **(S)-1-(5-tert-butyl-3-[(1-methyl-1H-tetrazol-5-yl)methyl]-3H-[1,2,3]triazolo[4,5-d]pyrimidin-7-yl)pyrrolidin-3-ol**; CAS **1433361-02-4**; compound 9 in synthesis section |
| 5 | Unequivocal hCB2 | **YES** — “recombinant **human** … CB2R”; cell line **CHOK1hCB2_bgal**; mCB2 reported separately (no pooling) |
| 6 | Cellular system | **YES** — Methods 2.2.2: **CHOK1hCB2_bgal** (DiscoveRx), forskolin-stimulated cAMP, Nano-TRF kit |
| 7 | Assay format | **YES** — forskolin-stimulated **cAMP** inhibition (not β-arrestin) |
| 8 | Metric | **YES** — **EC50**; no conversion from Ki (Ki 51.3±16.2 nM is binding, separate) |
| 9 | Unit | **YES** — nM |
| 10 | Emax normalization | **FAIL for GOLD_CONFIRMED** — Text: “potent, **full agonist** … compared to the maximum efficacy of the reference agonist (**CP55940**)” **without** a numeric % Emax in table/figure. GOLD correctly stores **NOT REPORTED**. Under ruthless Emax rules, absence of verifiable numeric Emax + standard → **Emax NOT VERIFIED** → cannot **GOLD_CONFIRMED** |
| 11 | Exact location | **YES** — **Figure 3A** + Results text (hCB2 EC50 2.81 ± 0.28 nM) |
| 12 | SMILES / identity | **NO / NOT VERIFIED** — Stored InChIKey `MAYZWDRUFKUGGP-VIFPVBQESA-N`. Primary proves **(S)** via IUPAC + **X-ray** (CCDC **22814444**). InChIKey **not regenerated** from primary structure this audit; secondary concordance ignored for §16 |

**Sibling contradiction (other row, not this GOLD row):** `VICASINABIN_func_barr` Round1 `~22 nM` vs primary Fig 3B / Results **99.69 ± 5.72 nM** — keeps that row REVIEW; does not alter the cAMP EC50 literal.

**Audit_Decision:** **REVIEW_REQUIRED** (numeric Emax absent; SMILES not primary-regenerated). Do not overwrite GOLD MD.

---

## 3. CONTRADICTIONS

1. **OLORINAB assay type vs Round1 note:** Round1 “typically cAMP/functional” vs Han 2017 Table 1 **β-arrestin**. Literal 6.2 nM / 106% belong to β-arrestin. → ASSAY_CONFLICT; GOLD MD already corrected format; CSV not modified.
2. **APD371 compound number:** Director “compound 17” vs primary **compound 6 (APD371)**. Compound 17 ≠ olorinab.
3. **VICASINABIN β-arrestin (sibling):** Round1 ~22 nM vs primary **99.69 ± 5.72 nM** (Fig 3B). METRIC_CONFLICT on REVIEW row; cAMP 2.81±0.28 unchanged.
4. **VICASINABIN Emax language:** “full agonist” vs CP55940 **without %** → Efficacy_Metric NOT REPORTED is correct; inventing 100% would violate §17.
5. **VICASINABIN species:** hCB2 2.81±0.28 vs mCB2 2.60±0.14 — not a conflict; must not pool.
6. **AM1710 EC50 11 / 11.2 nM claims:** Quarantined (Q-05 / Q11-06); not in current GOLD; must not be conflated with Ki 6.7.
7. **CP-55,940 / WIN55,212-2:** No single verified functional GOLD datum; global Ki/EC50 invention forbidden (Q-12).
8. **SMILES column naming:** GOLD “SMILES_Canonical” holds **InChIKeys** for both rows — identity proof incomplete until structure→InChIKey regeneration from primary/SI.

No silent correction of GOLD MD or Round1 CSV performed.

---

## 4. FINAL COUNTS

| Bucket (this audit of current GOLD rows) | N |
|---|---|
| **GOLD_CONFIRMED** | **0** |
| **REVIEW_REQUIRED** | **2** |
| **REJECTED** | **0** |

| Scope note | N |
|---|---|
| Rows listed under Dataset/GOLD in `ROUND1_GOLD_CANDIDATES.md` | 2 |
| Director expected GOLD compounds | 7 |
| Of the 5 non-current-GOLD expected names that would fail this audit’s GOLD bar | 5 / 5 |

**Parent report:** Current GOLD list remains 2 rows in the source MD (untouched). Independent re-audit confirms **0 / 2 GOLD_CONFIRMED**; both → **REVIEW_REQUIRED** on SMILES and (olorinab) SI cell-line / (vicasinabin) numeric Emax gaps. Scope mismatch: expected 7-compound GOLD is obsolete relative to §15–23 GOLD MD.

---

## 5. PRIMARY SOURCES ACTUALLY INSPECTED

| # | Source | Form inspected | What was verified |
|---|---|---|---|
| 1 | Han et al. 2017 APD371 — DOI 10.1021/acsmedchemlett.7b00396 / PMC5733264 | PMC HTML full text (Tables 1–2, footnotes, Methods narrative) | Cmpd **6** = APD371; hCB2 β-arrestin EC50 **6.2** (Emax **106**); CP-55,940=100; PathHunter named; cmpd **17** ≠ APD371 |
| 2 | Han 2017 ACS SI PDF | **NOT retrieved** (ACS 503; EuropePMC SI 500) | In vitro Methods / InChI / cell-line catalog **not** re-opened |
| 3 | RG7774/vicasinabin — DOI 10.3389/fphar.2024.1426446 / PMC11272598 | Frontiers HTML OA (Methods 2.2.2–2.2.3; Results functional; Fig 3 callouts) | hCB2 cAMP EC50 **2.81±0.28 nM**; mCB2 **2.60±0.14**; β-arr **99.69±5.72**; CHOK1hCB2_bgal; (S) IUPAC + CCDC 22814444; no numeric Emax % |
| 4 | `ROUND1_GOLD_CANDIDATES.md` + Round1 CSV (read-only) | Local MD/CSV | Scope of GOLD=2; REVIEW/Rejected placement of HU-308, GW405833, AM1710 Janus, CP/WIN refs; Round1 olorinab cAMP note |

**Not opened this pass (relevant to scope-mismatch only):** Valenzano 2005 (GW405833); Khanolkar 2007 (AM1710); Hanuš 1999 PNAS quantitative re-extract (HU-308); Soethoudt/primary panels for CP/WIN single-number claims.

---

*End ROUND1_GOLD_AUDIT_v1.0 — create-only; no dataset expansion; no docking/MD/ROC.*
