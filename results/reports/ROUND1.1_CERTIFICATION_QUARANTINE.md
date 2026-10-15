# ROUND 1.1 CERTIFICATION QUARANTINE

**Fecha:** 2026-08-16  
**Relacionado:** `CB2_Experimental_Master_Dataset_v1.0_Round1.1_CERTIFICATION.csv`  
**Regla:** Round 1 CSV / `QUARANTINE_LOG.md` inmutables. Aquí solo hallazgos Round 1.1.  
**Conflict types permitidos:** METRIC_CONFLICT | SPECIES_CONFLICT | ASSAY_CONFLICT | UNIT_CONVERSION | SOURCE_LOCATION_MISSING | STRUCTURE_IDENTITY | BIAS_NOT_ESTABLISHED | PRIMARY_SOURCE_UNAVAILABLE | FUNCTIONAL_ACTIVITY_UNCLEAR | KINETIC_DATA_UNCLEAR | QIU_BLINDED

---

## Q11-01 — URB447_bind_rCB1 / URB447_bind_hCB2 (scope IC50)

```
Compound: URB447
Original row: 1–2 (URB447_bind_rCB1; URB447_bind_hCB2)
Problem: Binding reported as IC50; must not be treated as Ki or functional EC50
Original value: 313 ± 72 nM (rCB1); 41 ± 23 nM (hCB2)
Primary-source value: same IC50s in Table 1 LoVerme 2009
Primary-source location: Table 1 (compound 8b)
Conflict type: METRIC_CONFLICT
Decision: CERTIFIED_WITH_SCOPE
Reason: Primario confirma números; métrica = IC50 binding only
Required follow-up: Mantener flag IC50≠Ki en cualquier benchmark de afinidad
```

## Q11-02 — URB447_func_mCB2_cAMP (species + qualitative)

```
Compound: URB447
Original row: 4
Problem: Functional CB2 evidence is mouse HEK, single concentration, no EC50
Original value: inhibits isoproterenol-stimulated cAMP at 1 µM (qualitative)
Primary-source value: same qualitative + pmol/well numbers in text
Primary-source location: Main text Results (HEK-293 mCB2 cAMP)
Conflict type: SPECIES_CONFLICT
Decision: CERTIFIED_WITH_SCOPE
Reason: Agonismo CB2 soportado; no hCB2; no potencia tabulada
Required follow-up: No pool con ensayos hCB2 cuantitativos
```

## Q11-03 — GW405833 binding + cAMP (Valenzano PDF missing)

```
Compound: GW405833 / L-768242
Original row: 5–7
Problem: Round1 D values (Ki 3.92 / 4772; EC50 0.65) not re-verified in primary PDF
Original value: 3.92; 4772; 0.65 nM
Primary-source value: NOT RETRIEVED Round1.1
Primary-source location: Valenzano 2005 DOI cited; PDF paywalled / not on disk
Conflict type: PRIMARY_SOURCE_UNAVAILABLE
Decision: HOLD
Reason: Secondary/vendor ≠ primary verification
Required follow-up: Obtener PDF Valenzano Table/figure exactos
```

## Q11-04 — GW405833_Janus_CB1_ant

```
Compound: GW405833
Original row: 8
Problem: Janus CB1 arm is P (Dhopeshwarkar); not clean URB447-like Yin-Yang
Original value: noncompetitive CB1 antagonism / complex
Primary-source value: complex multi-assay claim (not re-certified as D)
Primary-source location: Dhopeshwarkar JPET 2017
Conflict type: FUNCTIONAL_ACTIVITY_UNCLEAR
Decision: HOLD
Reason: Evidence_tag P; mechanism ≠ URB447
Required follow-up: Relectura primaria completa antes de Exam C
```

## Q11-05 — AM1710 binding (Khanolkar PDF missing)

```
Compound: AM1710
Original row: 9–10
Problem: Ki 6.7 / 360 attributed to Khanolkar 2007 but primary table not opened
Original value: Ki 6.7 nM (CB2); 360 nM (CB1)
Primary-source value: NOT RETRIEVED Round1.1 (cited via Rahn secondary)
Primary-source location: Khanolkar J Med Chem 2007 Table (PDF pending)
Conflict type: PRIMARY_SOURCE_UNAVAILABLE
Decision: HOLD
Reason: Prefer HOLD over secondary citation chain
Required follow-up: Abrir Table Khanolkar; separar filas Rahn si se usan variantes de especie
```

## Q11-06 — AM1710 EC50 11 nM (legacy Q-05) + Janus P

```
Compound: AM1710
Original row: 11 (Janus); Q-05 legacy for EC50 11 nM (not a Round1 CSV functional EC50 row)
Problem: Unverified EC50 11 nM must not be conflated with Ki 6.7; Janus CB1 inverse = P
Original value: qualitative low-potency CB1 inverse agonist
Primary-source value: not certified as D this round
Primary-source location: Dhopeshwarkar 2017 / Q-05 note
Conflict type: METRIC_CONFLICT
Decision: HOLD
Reason: Keep Ki vs EC50 as separate metrics; do not treat missing EC50 as error-vs-Ki
Required follow-up: Localizar primary para cualquier EC50 numérico
```

## Q11-07 — Vasiljevik InChIKey + VAS30 Ki rounding

```
Compound: Vasiljevik 27 / 30
Original row: 12–19
Problem: InChIKey = N (SMILES IUPAC-derived); VAS30 mCB1 Round1 37.2 vs Table 2 37.3±11.8
Original value: Ki / qualitative AC as Round1
Primary-source value: Table 2 / Fig 3–4 confirmed (PMC3904296)
Primary-source location: Table 2; Figures 3–4
Conflict type: STRUCTURE_IDENTITY
Decision: CERTIFIED or CERTIFIED_WITH_SCOPE (see CSV); quarantine for identity polish
Reason: Pharmacology OK; structure keys pending RDKit/PubChem
Required follow-up: RDKit InChIKey + deposit search
```

## Q11-08 — Qiu-14 qualitative only (S5)

```
Compound: Qiu-14
Original row: 20–21
Problem: Caption-only Yin-Yang; no EC50/IC50/Emax; cell system unnamed in SI caption
Original value: CB2 agonist / CB1 antagonist (caption)
Primary-source value: same qualitative captions
Primary-source location: SI mmc1 Figure S5A / S5B
Conflict type: QIU_BLINDED
Decision: CERTIFIED_WITH_SCOPE (qualitative only); Exam A/B/C = NO
Reason: Challenge set; no quantitative functional labels by inference
Required follow-up: Main pharmacology table Elsevier/SSRN if ever recovered — still blinded for training
```

## Q11-09 — Qiu-14 S173/S285

```
Compound: Qiu-14
Original row: 22
Problem: Docking/MD contact hypothesis tagged I
Original value: morpholine–S173/S285 hypothesis
Primary-source value: computational narrative / SI Fig S6 docking regioisomers
Primary-source location: paper docking narrative; SI Fig S6
Conflict type: QIU_BLINDED
Decision: REJECT
Reason: Must not enter experimental phenotype benchmarks; include_in_benchmark=NO
Required follow-up: None for LEVEL 0 experimental certification
```

## Q11-10 — Qiu-15/16/20/24 identity + func

```
Compound: Qiu-15 / 16 / 20 / 24
Original row: 23–30
Problem: Structure 0D OK where stated; functional outcomes NOT DETERMINABLE / table missing
Original value: structure_only or N
Primary-source value: Scheme S1 / Fig S6 structure; S11–S13 unread
Primary-source location: SI Scheme S1; Figs S6, S11–S13
Conflict type: QIU_BLINDED
Decision: HOLD
Reason: No new functional labels by inference; challenge blinded
Required follow-up: High-res panels + main table (still non-training)
```

## Q11-11 — LEI-101 pathway differences (no formal bias)

```
Compound: LEI-101
Original row: 33–35 (func cAMP / β-arr / GTPγS)
Problem: Full in cAMP vs partial in β-arr/GTPγS without formal bias analysis
Original value: pEC50 8.0 / 7.0 (Emax 41%) / 6.6 (Emax 65%)
Primary-source value: same Table 1 Mukhopadhyay 2016
Primary-source location: Table 1
Conflict type: BIAS_NOT_ESTABLISHED
Decision: CERTIFIED values; Exam_B_Eligible = CONDITIONAL
Reason: Do not auto-label Gi-biased
Required follow-up: Optional formal bias calculation only if using same systems/criteria
```

## Q11-12 — Olorinab / APD371 assay type

```
Compound: olorinab / APD371
Original row: 36–37
Problem: Round1 implied cAMP/functional; primary Table 1 is β-arrestin PathHunter
Original value: EC50 6.2 nM (hCB2); >10000 nM (hCB1)
Primary-source value: 6.2 (Emax 106) β-arrestin; hCB1 >10000 same platform
Primary-source location: Han 2017 Table 1 / Table 2 compound 6
Conflict type: ASSAY_CONFLICT
Decision: CERTIFIED_WITH_SCOPE
Reason: Numbers OK; assay class must be β-arrestin not cAMP
Required follow-up: Do not pool with cAMP EC50 series without assay tag
```

## Q11-13 — Vicasinabin β-arrestin value

```
Compound: vicasinabin / RG7774
Original row: 40
Problem: Round1 ~22 nM incorrect; ±5.72 belongs to 99.69
Original value: ~22 nM
Primary-source value: 99.69 ± 5.72 nM
Primary-source location: Frontiers 2024 Figure 3B / Results text
Conflict type: METRIC_CONFLICT
Decision: CERTIFIED_WITH_SCOPE (Verified_Value corrected; Original_Value preserved)
Reason: Primary unequivocal; Round1 not overwritten
Required follow-up: Exam B CONDITIONAL only (cAMP+β-arr present, no formal bias factor)
```

## Q11-14 — HU-308 incomplete Round1 functional + no bias

```
Compound: HU-308
Original row: 43
Problem: Round1 qualitative only; primary has EC50/Emax; no β-arrestin → no Gi-bias claim
Original value: inhibits forskolin-stimulated cAMP (qualitative)
Primary-source value: EC50 5.57 nM; Emax 108.6 ± 8.4%
Primary-source location: Hanuš 1999 Results cAMP paragraph; Methods
Conflict type: BIAS_NOT_ESTABLISHED
Decision: CERTIFIED_WITH_SCOPE
Reason: Quantitative functional recoverable from primary; bias not established
Required follow-up: Optional separate row for EC50 if dataset expanded (without editing Round1)
```

## Q11-15 — HU-308 species mix binding

```
Compound: HU-308
Original row: 41–42
Problem: CB2 transfected COS-7 vs CB1 rat synaptosomes
Original value: Ki 22.7±3.9; >10000 nM
Primary-source value: same
Primary-source location: Fig 1 / Results; Methods binding
Conflict type: SPECIES_CONFLICT
Decision: CERTIFIED / CERTIFIED_WITH_SCOPE
Reason: Values OK if species/system kept explicit
Required follow-up: Never pool CB1/CB2 Ki as same-species selectivity without note
```

## Q11-16 — JWH-133 venue / PDF

```
Compound: JWH-133
Original row: 44–45
Problem: Round1 said J Med Chem; correct primary is Bioorg Med Chem 1999; full PDF not opened
Original value: Ki 3.4 / 677 nM
Primary-source value: 3.4±1.0 / 677±132 (Huffman lineage)
Primary-source location: Huffman Bioorg Med Chem 1999 DOI 10.1016/S0968-0896(99)00219-9
Conflict type: SOURCE_LOCATION_MISSING
Decision: CERTIFIED_WITH_SCOPE
Reason: Venue discrepancy + PDF not fully opened this round
Required follow-up: Extract exact Table from Huffman PDF
```

## Q11-17 — CP55,940 / WIN55,212-2 global Ki

```
Compound: CP55,940; WIN55,212-2
Original row: 46–47
Problem: Single global Ki/EC50 would violate integrity
Original value: reference standard (qualitative)
Primary-source value: assay-dependent (many)
Primary-source location: multi-assay literature
Conflict type: PRIMARY_SOURCE_UNAVAILABLE
Decision: HOLD
Reason: Ref notes only; no invented global number
Required follow-up: Curate per-assay rows when needed
```

## Q11-18 — LY2828360 secondary numbers + bias claim

```
Compound: LY2828360
Original row: 48–49
Problem: Ki 40.3 / EC50 20.1 from secondary/vendor; G-bias not primary-verified
Original value: 40.3; 20.1 (CB2) / >100000 (CB1)
Primary-source value: NOT RETRIEVED
Primary-source location: secondary lineage; Lin et al. often cited
Conflict type: PRIMARY_SOURCE_UNAVAILABLE
Decision: HOLD
Reason: Also BIAS_NOT_ESTABLISHED until primary bias methods extracted
Required follow-up: Primary PDF table + bias methods
```

## Q11-19 — RNB-61 structure + Fig2 panel risk

```
Compound: RNB-61
Original row: 50–52
Problem: InChIKey N; Fig 2 caption/body may swap cAMP vs GTPγS EC50
Original value: Ki 0.57±0.03; 3882±73.4; cAMP EC50 0.31±0.07
Primary-source value: Table 1 confirms; Fig 2 also reports β-arr EC50 13.3±1.9 without formal bias
Primary-source location: Table 1; Figure 2
Conflict type: STRUCTURE_IDENTITY
Decision: CERTIFIED / CERTIFIED_WITH_SCOPE
Reason: Anchor Table 1 only for cAMP EC50; Exam B CONDITIONAL
Required follow-up: Confirm InChIKey; re-read Fig 2 carefully
```

## Q11-20 — Tedalinab

```
Compound: tedalinab / GRC-10693
Original row: 53
Problem: >4700-fold selectivity secondary; no Ki/EC50 primary
Original value: qualitative fold claim
Primary-source value: NOT RETRIEVED
Primary-source location: WO2006/129178 / secondary
Conflict type: PRIMARY_SOURCE_UNAVAILABLE
Decision: HOLD
Reason: No PASS numbers
Required follow-up: Locate primary pharmacology table or keep N
```

## Q11-21 — JD5037 CB2-neg (P tag / CB2 Ki detail)

```
Compound: JD5037
Original row: 54–55
Problem: >700-fold stated in Tam; CB2 Ki not in main-text excerpt; Round1 row 55 tagged P
Original value: Ki 0.35 nM CB1; >700-fold vs CB2
Primary-source value: Ki 0.35 nM; >700-fold CB1/CB2 (Tam 2012)
Primary-source location: Tam Cell Metab 2012 text / Fig 1
Conflict type: SOURCE_LOCATION_MISSING
Decision: CERTIFIED (CB1 Ki); CERTIFIED_WITH_SCOPE (CB2-neg)
Reason: Selectivity claim primary-stated; exact CB2 Ki table optional polish
Required follow-up: Chorvat BMCL 2012 Table if absolute CB2 Ki needed
```

## Q11-22 — Kinetic-Gold (global)

```
Compound: (dataset-wide)
Original row: all 55
Problem: No kon/koff/residence time rows in Round 1; none verified in audited primaries for these seeds
Original value: N/A
Primary-source value: none for this seed set Round1.1
Primary-source location: N/A
Conflict type: KINETIC_DATA_UNCLEAR
Decision: Report 0 kinetic rows (do not invent)
Reason: Kinetic-Gold empty at LEVEL 0
Required follow-up: Only add kinetic rows from primary kinetic assays
```

## Q11-23 — Vicasinabin / LEI / RNB bias formal

```
Compound: vicasinabin; LEI-101; RNB-61
Original row: 33–35, 39–40, 52
Problem: Dual pathways exist without formal bias factor / operational bias framework in primary
Original value: pathway EC50/pEC50 as Round1
Primary-source value: same + (RNB) β-arr 13.3±1.9 nM in Fig 2 not as Round1 row
Primary-source location: LEI Table 1; Frontiers Fig 3; RNB Table 1 / Fig 2
Conflict type: BIAS_NOT_ESTABLISHED
Decision: Exam_B_Eligible = CONDITIONAL (not YES)
Reason: Preserve pathway facts; forbid Gi-biased auto-label
Required follow-up: Formal bias only if primary methods support or new primary analysis documented
```

---

## Resumen operativo Round 1.1

| Status | N |
|--------|---|
| CERTIFIED | 14 |
| CERTIFIED_WITH_SCOPE | 20 |
| HOLD | 20 |
| REJECT | 1 |

**Salida de cuarentena LEVEL 0:** requiere primario con tabla/figura exacta + métrica no intercambiada + (para Exam B) framework de sesgo formal si se pretende YES.
