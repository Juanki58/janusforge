# ROUND1_GOLD_CANDIDATES

**Fase:** 2A / Round 1B — conservative re-audit (§15–23)  
**Fecha:** 2026-08-16  
**Input (solo lectura):** `CB2_Experimental_Master_Dataset_v1.0_Round1.csv` (55 filas)  
**Reglas absolutas:** §15 Traceability · §16 Chemical identity · §17 Emax · §18 Bias · §19 Duplicate refs · §20 Anti-confirmation · §21 Benchmark independence · §22 Audit trail · §23 Conservatism ladder  
**Companions:** `ROUND1B_GOLD_CANDIDATES.csv`, `ROUND1B_REVIEW_REQUIRED.csv` (alineados a este MD = fuente de verdad).

## Dataset

| Compound_ID | SMILES_Canonical | Chemical_Scaffold | Assay_Target | Assay_Format | Cellular_System | Concentration_Metric | Efficacy_Metric | Evidence_Tag | Primary_Reference | Source_Exact_Location |
|---|---|---|---|---|---|---|---|---|---|---|
| OLORINAB_func_hCB2 | ACSQLTBPYZSGBA-GMXVVIOVSA-N | pyrazole N-1,3-carboxamide (APD371/olorinab) | hCB2 | β-arrestin recruitment (DiscoverX PathHunter; NOT cAMP) | PathHunter hCB2 (DiscoverX) | EC50=6.2 nM | Emax 106% vs CP-55,940 (explicit Table 1) | D | 10.1021/acsmedchemlett.7b00396 \| PMID:29259753 \| PMC5733264 | Table 1 compound 6 hCB2 β-arrestin EC50 (Emax); also Table 2 row 6 |
| VICASINABIN_func_cAMP_hCB2 | MAYZWDRUFKUGGP-VIFPVBQESA-N | RG7774 / vicasinabin | hCB2 | cAMP (forskolin-stimulated inhibition) | CHO hCB2 (CHOK1hCB2_bgal) | EC50=2.81 ± 0.28 nM | NOT REPORTED | D | 10.3389/fphar.2024.1426446 | Figure 3A + Results text (hCB2 EC50 2.81 ± 0.28 nM) |

### AUDIT_WARNING / Traceability (GOLD)

**OLORINAB_func_hCB2**  
Compound_ID → Han et al. 2017 (DOI 10.1021/acsmedchemlett.7b00396) → Table 1 compound **6** (also Table 2) → original EC50 **6.2 nM**, Emax **(106)** relative to CP-55,940=100 → unit nM / % → transformation=**none**.  
Assay header primario = **β-arrestin** PathHunter (texto Methods confirma DiscoverX β-arrestin; no cAMP). Stereo Table 1 = **(S,S)** + (S)-t-butyl; X-ray absolute stereo citada en paper. InChIKey Round1 `ACSQLTBPYZSGBA-GMXVVIOVSA-N` retenido (capa stereo presente); no regenerado desde esquema 2D este pass (SI ACS 503; sin DBs secundarias). Round1 anotó “typically cAMP/functional” → ASSAY_CONFLICT documentado; valor 6.2 nM preservado; Assay_Format corregido solo aquí.

**VICASINABIN_func_cAMP_hCB2**  
Compound_ID → Frontiers 2024 (DOI 10.3389/fphar.2024.1426446) → Figure 3A + Results → original EC50 **2.81 ± 0.28 nM** (hCB2) → unit nM → transformation=**none**.  
Identidad: nombre IUPAC **(S)**-… + X-ray absolute configuration **(S)** (CCDC 22814444 citada); CAS 1433361-02-4 en Methods. InChIKey Round1 `MAYZWDRUFKUGGP-VIFPVBQESA-N` retenido.  
§17: texto dice “full agonist” vs CP55940 **sin % Emax explícito** en tabla/figura numérica → Efficacy_Metric=**NOT REPORTED** (no inferir 100%).  
mCB2 EC50 **2.60 ± 0.14 nM** reportado en el mismo párrafo → **fila aparte / no pooling**. Abstract “EC50: 2.8 nM” = redondeo del mismo valor; no contradicción material cAMP.

## Review Required

| Compound_ID | SMILES_Canonical | Chemical_Scaffold | Assay_Target | Assay_Format | Cellular_System | Concentration_Metric | Efficacy_Metric | Evidence_Tag | Primary_Reference | Source_Exact_Location |
|---|---|---|---|---|---|---|---|---|---|---|
| LEI101_func_barr | APLLNJWPLUIBCG-UHFFFAOYSA-N | imidazolidinedione (LEI-101) | hCB2 | β-arrestin recruitment (PathHunter DiscoverX) | CHO-K1 PathHunter hCB2 (CNR2 93-0706C2 / CHOK1hCB2R_bgal) | pEC50=7.0 ± 0.3 | Emax 41 ± 6% vs CP55940 (explicit Table 1) | D | 10.1111/bph.13338 \| PMID:26398481 \| PMC4728411 | Table 1 row LEI-101 column β-Arrestin recruitment pEC50/Emax hCB2R |
| LEI101_func_GTP | APLLNJWPLUIBCG-UHFFFAOYSA-N | imidazolidinedione (LEI-101) | hCB2 | [35S]GTPγS binding | CHOK1hCB2R_bgal membranes | pEC50=6.6 ± 0.2 | Emax 65 ± 8% vs CP55940 (explicit Table 1) | D | 10.1111/bph.13338 \| PMID:26398481 \| PMC4728411 | Table 1 row LEI-101 column GTPγS binding pEC50/Emax hCB2R |
| LEI101_func_cAMP | APLLNJWPLUIBCG-UHFFFAOYSA-N | imidazolidinedione (LEI-101) | hCB2 | cAMP inhibition | hCB2 (system detail for this metric tied to van der Stelt 2011 / footnote a — not re-verified this pass) | pEC50=8.0 ± 0.1 (keep as pEC50; do not convert) | NOT REPORTED | D→scope REVIEW | 10.1111/bph.13338 \| PMID:26398481 \| PMC4728411 | Table 1 cAMP inhibition pEC50; footnote a → van der Stelt et al. 2011; no cAMP Methods in Mukhopadhyay 2016 |
| VICASINABIN_func_barr | MAYZWDRUFKUGGP-VIFPVBQESA-N | RG7774 / vicasinabin | hCB2 | β-arrestin recruitment (PathHunter) | CHO hCB2 PathHunter | EC50=~22 nM (Round1 original; DO NOT silently replace) | NOT REPORTED | P | 10.3389/fphar.2024.1426446 | Figure 3B + Results text (primary = 99.69 ± 5.72 nM — conflict) |
| HU308_func_cAMP | CFMRIVODIXTERW-BDTNDASRSA-N | bicyclic cannabinoid (HU-308) | hCB2 (CHO transfected per Methods lineage) | cAMP (forskolin) | CB2-transfected cells (Round1); CHO hCB2 (Round1.1 Methods) | qualitative (Round1 original value) | NOT REPORTED | D | 10.1073/pnas.96.25.14228 \| PMID:10588688 | Results cAMP paragraph (Round1 qualitative only; do not auto-promote Round1.1 EC50 5.57 nM into GOLD) |
| RNB61_func_cAMP | NOT VERIFIED | tetra-substituted pyrazole (RNB-61) | hCB2 | cAMP inhibition | CHO hCB2 | EC50=0.31 ± 0.07 nM (Table 1; Fig 2 conflict risk — preserve Round1) | NOT REPORTED | D | 10.1021/acsptsci.4c00269 \| PMC11320734 | Table 1 EC50 hCB2R cAMP; cross-check Fig 2 panels; InChIKey N |
| GW405833_func_hCB2_cAMP | FSFZRNZSZYDVLI-UHFFFAOYSA-N | indole aminoalkylindole (L-768242/GW405833) | hCB2 | cAMP (forskolin) | human CB2 (system detail unverified) | EC50=0.65 nM (Round1; primary PDF not recovered) | NOT REPORTED | D→treat as N for GOLD gate | 10.1016/j.neuropharm.2005.01.010 \| PMID:15814101 | NOT VERIFIED — Valenzano 2005 primary table/figure pending recovery |
| VAS27_func_CB2_AC | NOT VERIFIED (IUPAC-derived SMILES; InChIKey N) | aminoalkylindole (Vasiljevik 27) | hCB2 | adenylyl cyclase / cAMP | CHO hCB2 | qualitative (~40–50% AC inhibition) | NOT REPORTED | D | 10.1021/jm400268b \| PMID:23631463 \| PMC3904296 | Figure 4A + Results text (~40–50% AC inhibition); no discrete EC50 |
| VAS30_func_CB2_AC | NOT VERIFIED (IUPAC-derived SMILES; InChIKey N) | aminoalkylindole (Vasiljevik 30) | hCB2 | adenylyl cyclase / cAMP | CHO hCB2 | qualitative (~40–50% AC inhibition) | NOT REPORTED | D | 10.1021/jm400268b \| PMID:23631463 \| PMC3904296 | Figure 4A + Results text; no discrete EC50 |
| URB447_func_mCB2_cAMP | KGXYGMKEFDUWNB-UHFFFAOYSA-N | pyrrole (diarylpyrrole URB447) | mCB2 (NOT hCB2) | cAMP (isoproterenol-stimulated) | HEK-293 mouse CB2 | qualitative (inhibits at 1 µM; no EC50) | NOT REPORTED | D | 10.1016/j.bmcl.2008.12.059 \| PMID:19128970 | Main text Results HEK-293 mCB2 cAMP paragraph |
| OLORINAB_func_hCB1 | ACSQLTBPYZSGBA-GMXVVIOVSA-N | pyrazole N-1,3-carboxamide (APD371) | hCB1 (selectivity counterpart; not hCB2 GOLD) | β-arrestin (PathHunter; same platform as hCB2 row) | PathHunter hCB1 | EC50=>10000 nM | NOT REPORTED | D | 10.1021/acsmedchemlett.7b00396 \| PMID:29259753 \| PMC5733264 | Table 1 / Table 2 compound 6 hCB1 β-arrestin EC50 column |
| LY2828360_func_GTP | UCMNDPDJRSEZPL-UHFFFAOYSA-N | LY2828360 | CB2 (species/system unverified) | GTPγS | CB2 vs CB1 (secondary lineage) | EC50=20.1 nM (CB2); >100000 nM (CB1) — secondary only | NOT REPORTED | P | Lin et al. Mol Pharmacol 2018 often cited; vendor/secondary Round1 | PRIMARY TABLE NOT RECOVERED |
| TEDALINAB_qual | NOT VERIFIED (Wikipedia stereochem vs PubChem CID conflict risk) | tedalinab / GRC-10693 | CB2 claimed | functional/binding not recovered as PASS numbers | not recovered | qualitative >4700-fold CB2 vs CB1 (secondary/company) | NOT REPORTED | N | CAS 916591-01-0; WO2006/129178 lineage | PRIMARY Ki/EC50 TABLE NOT RECOVERED |
| GW405833_Janus_CB1_ant | FSFZRNZSZYDVLI-UHFFFAOYSA-N | indole aminoalkylindole | hCB1 (Janus arm) | functional multi-readout (AC/ERK/PIP2/internalization) | HEK/CHO CB1 (Dhopeshwarkar) | qualitative complex/noncompetitive CB1 antagonism | NOT REPORTED | P | 10.1124/jpet.116.236539 \| PMID:28289077 | Dhopeshwarkar JPET 2017 (exact panel location needs re-extract) |
| AM1710_Janus_CB1_inv | ZAIKPEWFCSQNQB-UHFFFAOYSA-N | cannabilactone (AM1710) | CB1 | CB1 inverse agonism (low potency) | in vitro (Dhopeshwarkar 2017) | qualitative low-potency CB1 inverse agonist | NOT REPORTED | P | 10.1124/jpet.116.236539 \| PMID:28289077 | Dhopeshwarkar JPET 2017 (exact assay panel pending) |
| JD5037_CB2_neg | GTCSIQFTNPTSLO-RPWUZVMVSA-N | ibipinabant analog (JD5037) | CB2 (negative control / selectivity) | binding selectivity fold (not functional hCB2 agonist) | as Tam 2012 | >700-fold selective for CB1 over CB2 (fold; CB2 Ki not tabulated in main-text excerpt) | NOT REPORTED | P | 10.1016/j.cmet.2012.07.002 \| PMID:22841573 (Tam 2012); Chorvat BMCL 2012 optional | Tam 2012 text / Fig 1 selectivity statement |

### AUDIT_WARNING / Traceability (Review)

**LEI101_func_barr** (DEMOTE GOLD→REVIEW §16)  
→ Mukhopadhyay 2016 Table 1 → pEC50 **7.0 ± 0.3**, Emax **41 ± 6%** → transformation=**none** (store pEC50). Methods PathHunter en CHOK1hCB2R_bgal OK.  
**Bloqueo GOLD:** primario nombra **hydrochloride**; InChIKey Round1 `…-UHFFFAOYSA-N` = sin sal / sin stereo layer; Round1.1 citó CID sal vía DB secundaria (prohibido §16 para resolver). Ambigüedad sal HCl no cerrada → REVIEW. Sin label de bias (§18).

**LEI101_func_GTP** (DEMOTE GOLD→REVIEW §16)  
→ Table 1 → pEC50 **6.6 ± 0.2**, Emax **65 ± 8%** → transformation=**none**. Methods GTPγS en membranes CHOK1hCB2R_bgal OK. Misma ambigüedad sal HCl / identidad estructural → REVIEW.

**LEI101_func_cAMP**  
→ Table 1 pEC50 **8.0 ± 0.1**; footnote **a** = van der Stelt 2011; Methods 2016 **no** detallan cAMP → provenance REVIEW. “Full in cAMP” = narrativa autores **sin %** → Efficacy_Metric=**NOT REPORTED** (§17).

**VICASINABIN_func_barr**  
→ Round1 `~22 nM` vs primario Fig 3B **99.69 ± 5.72 nM** → METRIC_CONFLICT; valor Round1 preservado; no GOLD; no digitización/corrección silenciosa (§15).

**HU308 / RNB61 / GW405833 / VAS / URB447 mCB2 / OLORINAB hCB1 / LY / TEDALINAB / Janus / JD5037:** ver Critical Warnings + secciones §22. Qiu 14/15/16/20/24 **excluidos** de GOLD y REVIEW.

## Statistics

* Gold candidates: **2**
* Review required: **16**
* Rejected: **37**

**Demotions este pass (GOLD→REVIEW):** LEI101_func_barr; LEI101_func_GTP.  
**Rejected (37 filas, sin cambio de bucket):** binding-only Ki/IC50/pKi; Qiu 14/15/16/20/24 challenge + docking I (11); refs globales CP55,940 / WIN55,212-2; VAS/URB CB1 functional arms no elegibles como hCB2 GOLD.

## Primary References

**Inspeccionados este pass (OA / EuropePMC PDF render / Frontiers HTML):**

1. Han et al. 2017 APD371/olorinab — DOI 10.1021/acsmedchemlett.7b00396 / PMC5733264 (EuropePMC PDF render) — Table 1/2 β-arrestin + stereo (S,S) + Emax 106% confirmados
2. Mukhopadhyay et al. 2016 LEI-101 — DOI 10.1111/bph.13338 / PMC4728411 (EuropePMC PDF render) — Table 1 + Methods PathHunter/GTPγS; nombre HCl; footnote a van der Stelt
3. RG7774/vicasinabin — DOI 10.3389/fphar.2024.1426446 (Frontiers HTML OA) — Fig 3A/3B + Methods cAMP / PathHunter + X-ray (S)
4. Vasiljevik 2013 — DOI 10.1021/jm400268b / PMC3904296 (local + prior) — REVIEW cualitativo
5. Round1.1 CERTIFICATION* como **hints** únicamente (no corrección silenciosa de Round1; §21 no se usa Exam A/B/C para clasificar)

## Critical Warnings

1. **Conservatism ladder (§23):** GOLD 4→**2**. LEI barr/GTP demoted por ambigüedad sal HCl / InChIKey free-base (§16); valores Table 1 siguen D pero no GOLD.
2. **Olorinab 6.2 nM = β-arrestin PathHunter**, Emax **106%** explícito Table 1; no cAMP.
3. **Vicasinabin cAMP 2.81±0.28** permanece GOLD; Efficacy “full agonist” → **NOT REPORTED** (§17). mCB2 2.60 no pooled.
4. **Vicasinabin β-arr:** Round1 ~22 vs primario 99.69±5.72 → REVIEW + EXPERIMENTAL_CONTRADICTIONS.
5. **Bias (§18):** sin etiquetas Gi-biased / arrestin-sparing / G-biased en ninguna fila GOLD/REVIEW; Evidence_Tag N/P donde corresponda (p.ej. LY2828360 P).
6. **Qiu:** fuera de GOLD (Rejected / challenge).
7. **§21:** clasificación independiente de utilidad Exam A/B/C / “training” / “like Qiu-14”.
8. **Integridad:** Round1 CSV, Round1.1 CERTIFICATION*, QUARANTINE_LOG.md **no modificados**. Sin docking/MD/modelado. Sin commits git.

---

## VERIFIED_PRIMARY_REFERENCES

| Ref | DOI / ID | Qué se verificó este pass |
|---|---|---|
| Han 2017 APD371 | 10.1021/acsmedchemlett.7b00396 / PMC5733264 | Table 1 compound 6: hCB2 β-arrestin EC50=6.2 (Emax 106); hCB1 >10,000; stereo (S,S); assay = PathHunter β-arrestin |
| Mukhopadhyay 2016 LEI-101 | 10.1111/bph.13338 / PMC4728411 | Table 1: β-arr pEC50 7.0±0.3 (Emax 41±6%); GTPγS 6.6±0.2 (Emax 65±8%); cAMP 8.0±0.1; Methods PathHunter/GTPγS; compound named as **HCl**; footnote a → van der Stelt 2011 |
| RG7774 / vicasinabin 2024 | 10.3389/fphar.2024.1426446 | Fig 3A/Results: hCB2 cAMP EC50 2.81±0.28 nM; mCB2 2.60±0.14 nM; Fig 3B β-arr EC50 **99.69±5.72 nM**; (S) X-ray absolute config; Methods CHO CHOK1hCB2_bgal cAMP + PathHunter |

## UNVERIFIED_REFERENCES

1. Valenzano 2005 GW405833 (Neuropharmacology) — PDF no recuperado → EC50 0.65 nM Round1 no re-verificado
2. Hanuš 1999 HU-308 PNAS — EC50 cuantitativo Round1.1 (5.57 nM / Emax 108.6%) **no** re-extraído limpio este pass; Round1 cualitativo preservado
3. Chicca / RNB-61 — Table 1 / Fig 2 paneles no re-abiertos limpios; InChIKey N
4. Khanolkar 2007 AM1710 — PDF no abierto (binding rejected anyway)
5. Lin / primary LY2828360 — solo secondary Round1
6. WO2006/129178 / tedalinab primary table
7. van der Stelt 2011 — provenance footnote LEI Table 1 binding (±cAMP); no re-verificado
8. Dhopeshwarkar 2017 — paneles Janus exactos pendientes de re-extract
9. Chorvat BMCL 2012 — JD5037 absolute CB2 Ki si se necesita
10. Huffman 1999 JWH-133 — binding only; venue fix pending
11. Han 2017 SI PDF (ACS) — 503 este pass; InChIKey olorinab no regenerado desde SI

## STRUCTURAL_UNCERTAINTIES

1. **LEI-101:** primario = **hydrochloride**; InChIKey almacenado `APLLNJWPLUIBCG-UHFFFAOYSA-N` sin componente sal / sin stereo layer. Round1.1 mencionó CID sal vía DB secundaria — **no usado** para resolver (§16). → GOLD bloqueado.
2. **Olorinab / APD371:** stereo **(S,S)** explícito Table 1 + X-ray citada; InChIKey Round1 con capa stereo retenido pero **no regenerado** desde esquema/SI este pass.
3. **Vicasinabin / RG7774:** (S) confirmado por X-ray primario; InChIKey Round1 retenido sin regeneración RDKit este pass.
4. **RNB-61, VAS27, VAS30, TEDALINAB:** SMILES/InChIKey **NOT VERIFIED**.
5. Columna `SMILES_Canonical` en Round1/GOLD a menudo almacena **InChIKey**, no SMILES — documentado; no se inventan SMILES.

## EXPERIMENTAL_CONTRADICTIONS

1. **VICASINABIN_func_barr — METRIC_CONFLICT (obligatorio):** Round1 Concentration_Metric `~22 nM` vs primario Frontiers Fig 3B / Results **99.69 ± 5.72 nM**. Ambos documentados; Round1 no sobrescrito; no GOLD; no “valor más plausible”.
2. **OLORINAB_func_hCB2 — ASSAY_CONFLICT vs nota Round1:** Round1 “typically cAMP/functional” vs Han 2017 Table 1 header **β-arrestin EC50**. Número 6.2 nM + Emax 106% OK bajo assay correcto.
3. **LEI-101 pathway narrative:** autores “full” en cAMP vs partial β-arr/GTPγS — **no** es contradicción numérica de Table 1; **sí** impide label de bias (§18). cAMP provenance vía footnote a vs Methods 2016 → REVIEW.
4. **HU-308:** Round1 cualitativo vs Round1.1 hint cuantitativo (5.57 nM / 108.6%) — no se elige el cuantitativo para GOLD este pass (§15/§23; primario PNAS no re-extraído limpio).
5. **Vicasinabin species:** hCB2 2.81±0.28 vs mCB2 2.60±0.14 — no contradicción; **no pooling**.
6. Ninguna contradicción residual oculta eligiendo el valor “más plausible”.
