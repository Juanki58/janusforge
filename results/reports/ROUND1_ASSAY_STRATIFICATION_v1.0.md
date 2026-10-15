# ROUND1_ASSAY_STRATIFICATION_v1.0

**Fecha:** 2026-08-16  
**Fase:** 2A / Round 1.2 — assay-compatibility stratification (blind-validation prep)  
**Inputs (solo lectura):** `ROUND1_GOLD_AUDIT_v1.0.md`, `ROUND1_GOLD_CANDIDATES.md`, Round1 CSV, Round1.1 CERTIFICATION*, ROUND1B companions  
**Output (create-only):** este archivo  
**Prohibiciones:** sin modelado / docking / MD / ROC-AUC / descriptores / diseño molecular; sin modificar datasets originales  

**Realidad de integridad (no negociable):**  
`ROUND1_GOLD_AUDIT_v1.0` → **GOLD_CONFIRMED = 0**; las 2 filas Dataset/GOLD (`OLORINAB_func_hCB2`, `VICASINABIN_func_cAMP_hCB2`) → **REVIEW_REQUIRED**.  
La expectativa Director de “4 GOLD actuales” (HU-308, Vicasinabin, GW405833, AM1710) **no coincide** con el estado de archivos. Esta estratificación **no** promociona a subconjuntos homogéneos por etiqueta GOLD deseada.

**Regla de homogeneidad:** cAMP ≠ GTPγS ≠ β-arrestin ≠ binding; EC50 ≠ Ki; IC50 ≠ Ki; Emax no se reconstruye visualmente; preferir subconjunto vacío a homogeneidad falsa.

**Clases Emax usadas:** `EXPLICIT_NUMERIC` | `EXPLICIT_REFERENCE_NORMALIZATION` | `QUALITATIVE_ONLY` | `NOT_REPORTED`

---

## 1. cAMP HOMOGENEOUS SUBSET

**Criterio simultáneo:** hCB2 explícito + cAMP funcional + sistema celular comparable/identificado + EC50 explícito + Emax explícito y trazable (`EXPLICIT_NUMERIC` o `EXPLICIT_REFERENCE_NORMALIZATION` inequívoca) + primario verificado + `Source_Exact_Location` verificable. **Sin** GTPγS.

| Compound_ID | Assay | Species | System | EC50 / metric | Emax class | Location | Primary ref | Notes |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | **EMPTY** |

**N = 0.** Ninguna fila Round1/GOLD supera la barra Emax + trazabilidad + identidad a la vez.

**Candidatos Director / GOLD evaluados y rechazados para este subset:**

| Compound | Why not Subset A |
|---|---|
| **Vicasinabin** (`VICASINABIN_func_cAMP_hCB2`) | Primario Frontiers OK: hCB2 cAMP EC50 **2.81 ± 0.28 nM**, CHOK1hCB2_bgal, Fig 3A. Emax = **QUALITATIVE_ONLY** (“full agonist” vs CP55940 **sin %**). SMILES/InChIKey no regenerado. Audit → REVIEW; **no** homogeneidad cuantitativa Emax. |
| **HU-308** (`HU308_func_cAMP`) | Round1 = cualitativo forskolin cAMP. Round1.1 cita EC50 5.57 nM / Emax 108.6±8.4% en Hanuš 1999, pero **este pass no reabrió** PNAS (Cloudflare/PMC block) y GOLD audit no promovió ese número. Sin re-extracción limpia → **no** Subset A. |
| **GW405833** (`GW405833_func_hCB2_cAMP`) | EC50 0.65 nM Round1; PDF Valenzano **NOT VERIFIED**; sistema/Emax incompletos. |
| **Olorinab / APD371** | Valor 6.2 nM es **β-arrestin** PathHunter (Han Table 1), **no** cAMP. No entra aquí. |
| **LEI-101** (`LEI101_func_cAMP`) | pEC50 8.0±0.1 Table 1; footnote **a** → van der Stelt 2011; Methods 2016 **sin** cAMP; Emax **N.D. / NOT_REPORTED**; sal HCl vs InChIKey free-base. |
| **RNB-61** | EC50 cAMP Table 1 OK por Round1.1 hint, pero Emax **NOT_REPORTED**; InChIKey N; riesgo Fig 2. |
| **VAS27 / VAS30** | Solo inhibición AC cualitativa (~40–50%); sin EC50. |
| **URB447** | cAMP **mCB2** (no hCB2); cualitativo 1 µM. |

---

## 2. GTPγS HOMOGENEOUS SUBSET

**Criterio:** hCB2 + [³⁵S]GTPγS + prep identificada + EC50/métrica funcional explícita + Emax explícito + primario verificable. **AM1710** solo aquí *si* califica — **nunca** como equivalente cAMP.

| Compound_ID | Assay | Species | System | EC50 / metric | Emax class | Location | Primary ref | Notes |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | **EMPTY** |

**N = 0.**

**Evaluaciones clave:**

| Compound | Why not Subset B |
|---|---|
| **AM1710** | **Sin** fila hCB2 funcional GTPγS verificada. Binding Ki HOLD (Khanolkar no abierto). Claim EC50 “11 / 11.2 nM” quarantined (Q-05 / Q11-06). Solo `AM1710_Janus_CB1_inv` (CB1, P). **No** cAMP-equivalent; **no** Subset B. |
| **LEI-101** (`LEI101_func_GTP`) | Primario Mukhopadhyay 2016 Table 1: hCB2 GTPγS pEC50 **6.6 ± 0.2**, Emax **65 ± 8%** vs CP55940; membranes **CHOK1hCB2R_bgal** — farmacología OK. Bloqueo: compuesto nombrado **hydrochloride**; InChIKey Round1 `…-UHFFFAOYSA-N` sin sal/stereo → REVIEW (§16). Fidelidad > volumen: **no** promoción homogénea. |
| **LY2828360** (`LY2828360_func_GTP`) | EC50 20.1 nM secondary/vendor; primario no recuperado; Emax NOT_REPORTED; especie/sistema no verificados. |
| **URB447_func_rCB1_GTP** | GTPγS en **rat CB1** (antagonismo/neutral), no agonismo hCB2. |

---

## 3. ORTHOGONAL Gi / β-ARRESTIN SUBSET

**Criterio (Exam B futuro):** **mismo estudio** aporta hCB2 + Gi/cAMP + β-arrestin + sistema identificable + cuantificación o categorización explícita.  
**Prohibido:** inferir sesgo desde una sola vía; combinar cAMP paper A + arrestin paper B.

| Compound_ID | Assay pair (same study) | Species | System(s) | Metrics | Emax class (cAMP / β-arr) | Location | Primary ref | Notes |
|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | **EMPTY** |

**N = 0.** Preferir vacío a “ortogonal” con filas Round1 conflictivas o identidad no cerrada.

**Near-miss documentado (NO promocionado):**

| Molecule | Same-study primary fact | Why still excluded from Subset C |
|---|---|---|
| **Vicasinabin / RG7774** | Frontiers 2024 **sí** co-mide en el mismo paper: cAMP hCB2 EC50 **2.81 ± 0.28 nM** (Methods 2.2.2 CHOK1hCB2_bgal; Fig 3A) + β-arrestin hCB2 EC50 **99.69 ± 5.72 nM** (Methods 2.2.3 PathHunter hCB2_bgal CHOK1; Fig 3B). | (1) Round1 `VICASINABIN_func_barr` = **~22 nM** vs primario **99.69** → METRIC_CONFLICT; (2) cAMP Emax QUALITATIVE_ONLY; (3) β-arr Emax NOT_REPORTED en Results; (4) SMILES/InChIKey no regenerado; (5) sin factor de sesgo formal. → **REVIEW**, no Subset C. |
| **LEI-101** | Table 1 lista cAMP + β-arr + GTPγS. | cAMP = footnote **a** (van der Stelt 2011), **no** Methods 2016 → no co-campaña experimental cerrada; Emax cAMP N.D.; sal HCl / InChIKey. Autores narran “full cAMP / partial β-arr·GTPγS” **sin** análisis formal de bias → REVIEW, no Subset C. |
| **RNB-61** | Round1.1: cAMP Table 1 + β-arr Fig 2 (13.3±1.9) mismo paper. | InChIKey N; Fig 2 panel risk; β-arr no es fila Round1 limpia; sin bias formal → REVIEW. |
| **Olorinab** | Han 2017: β-arrestin cuantitativo; **sin** cAMP hCB2 cuantitativo en el mismo estudio para pairing. | No ortogonal. |

---

## 4. NON-COMPARABLE FUNCTIONAL DATA

Filas / claims con evidencia funcional que **no** pueden entrar en comparación homogénea de potencia/eficacia entre sí (métrica, especie, assay class, o ausencia de funcional hCB2).

| Compound_ID | Assay | Species | System | Metric | Emax class | Location | Primary ref | Why non-comparable |
|---|---|---|---|---|---|---|---|---|
| OLORINAB_func_hCB2 | β-arrestin PathHunter | hCB2 | PathHunter hCB2 (DiscoverX); SI cell-line catalog not re-opened | EC50=6.2 nM | EXPLICIT_REFERENCE_NORMALIZATION (106% vs CP-55,940=100) | Table 1 / Table 2 cmpd **6** | 10.1021/acsmedchemlett.7b00396 / PMC5733264 | β-arrestin ≠ cAMP ≠ GTPγS; no mezclar Emax con series cAMP. APD371=cmpd **6** (no 17). |
| OLORINAB_func_hCB1 | β-arrestin | hCB1 | PathHunter hCB1 | EC50=>10000 nM | NOT_REPORTED | Table 1/2 cmpd 6 hCB1 | same Han 2017 | Contraparte selectividad; no hCB2 agonist GOLD. |
| AM1710 (binding / EC50 claims) | binding Ki / alleged EC50 | CB2/CB1 claimed | Khanolkar not opened | Ki 6.7 / 360 HOLD; EC50 11 nM quarantined | NOT_REPORTED | pending / Q-05 | Khanolkar 2007 not opened this lineage | **No** hCB2 funcional verificado; Ki≠EC50; **no** Subset B. |
| AM1710_Janus_CB1_inv | CB1 inverse (qual) | CB1 | Dhopeshwarkar 2017 | qualitative | NOT_REPORTED | panel pending | 10.1124/jpet.116.236539 | Janus CB1 ≠ hCB2 agonist functional. |
| URB447_func_mCB2_cAMP | cAMP | **mCB2** | HEK-293 mCB2 | qualitative @ 1 µM | NOT_REPORTED | Results text | 10.1016/j.bmcl.2008.12.059 | Especie ≠ hCB2; sin EC50. |
| URB447_func_rCB1_GTP | GTPγS | rat CB1 | cerebellar membranes | EC50 4.9±0.8 µM (inhib. WIN) | NOT_REPORTED (as hCB2 Emax) | LoVerme Table/text | same | CB1 functional arm; no hCB2 GTPγS agonist. |
| URB447_bind_* | binding IC50 | rCB1 / hCB2 | membranes / CHO | IC50 | N/A | Table 1 | same | Binding IC50 ≠ Ki ≠ functional EC50. |
| VAS27_func_CB2_AC / VAS30_func_CB2_AC | AC / cAMP | hCB2 | CHO hCB2 | qualitative ~40–50% | NOT_REPORTED | Fig 4A | 10.1021/jm400268b | Sin EC50; no Emax % vs ref estándar tabulada. |
| GW405833_Janus_CB1_ant | multi-readout CB1 | hCB1 | HEK/CHO | qualitative complex | NOT_REPORTED | Dhopeshwarkar | 10.1124/jpet.116.236539 | Janus CB1; no cAMP hCB2 homogeneous. |
| JD5037_CB2_neg | binding selectivity | CB2 neg / CB1 | Tam 2012 | fold >700 CB1 vs CB2 | NOT_REPORTED | text / Fig 1 | 10.1016/j.cmet.2012.07.002 | No agonismo funcional hCB2. |
| CP55940_ref_note / WIN55212_ref_note | multi-assay refs | multi | multi | global Ki/EC50 **forbidden** | N/A | Q-12 / Q11-17 | multi | Refs globales; no fila assay-locked. |
| Qiu-14/15/16/20/24 (+ docking I) | challenge / I | — | — | qualitative / ND / I | — | SI / docking | Qiu lineage | Blinded / REJECT / no benchmark experimental phenotype. |
| Binding-only Ki/IC50 rows (JWH-133, HU-308 bind, etc.) | binding | mixed | mixed | Ki/IC50 | N/A | various | various | Binding ≠ efficacy; fuera de subsets funcionales homogéneos. |

---

## 5. REVIEW_REQUIRED

Filas con potencial farmacológico parcial pero bloqueadas por Emax, identidad, provenance, conflicto métrico, o primario no recuperado. **No** recovery por inferencia secundaria.

| Compound_ID | Assay | Species | System | Metric | Emax class | Location | Primary ref | Blocker |
|---|---|---|---|---|---|---|---|---|
| VICASINABIN_func_cAMP_hCB2 | cAMP (FSK inhib.) | hCB2 | CHOK1hCB2_bgal | EC50=2.81±0.28 nM | QUALITATIVE_ONLY (“full” vs CP55940) | Fig 3A + Results | 10.3389/fphar.2024.1426446 | Emax % ausente; SMILES/InChIKey no regenerado. **Director-named:** cAMP OK parcial; no Subset A. |
| VICASINABIN_func_barr | β-arrestin PathHunter | hCB2 | CHO PathHunter hCB2 | Round1 ~22 nM **vs** primary **99.69±5.72 nM** | NOT_REPORTED | Fig 3B + Results | same Frontiers | METRIC_CONFLICT; no corrección silenciosa Round1. Bloquea Subset C. |
| OLORINAB_func_hCB2 | β-arrestin | hCB2 | PathHunter (SI methods PDF not opened) | EC50=6.2 nM | EXPLICIT_REFERENCE_NORMALIZATION (106%) | Table 1 cmpd 6 | Han 2017 | SMILES/InChIKey no regenerado; SI cell-line incompleto. Audit demote GOLD→REVIEW. **No recovery** de “cAMP”. |
| LEI101_func_barr | β-arrestin | hCB2 | CHOK1hCB2R_bgal / 93-0706C2 | pEC50=7.0±0.3 | EXPLICIT_NUMERIC (41±6% vs CP55940) | Table 1 | 10.1111/bph.13338 / PMC4728411 | Sal **HCl** vs InChIKey free-base. |
| LEI101_func_GTP | [³⁵S]GTPγS | hCB2 | CHOK1hCB2R_bgal membranes | pEC50=6.6±0.2 | EXPLICIT_NUMERIC (65±8%) | Table 1 | same | Misma ambigüedad sal/identidad → no Subset B. |
| LEI101_func_cAMP | cAMP inhib. | hCB2 claimed | system via van der Stelt 2011 footnote a | pEC50=8.0±0.1 | NOT_REPORTED (N.D.) | Table 1 + footnote a | same / van der Stelt 2011 not re-opened | Provenance cross-paper; no Emax; no inventar. |
| HU308_func_cAMP | cAMP (FSK) | hCB2 (CHO lineage claimed) | Round1 qualitative; Round1.1 Methods CHO | qualitative Round1; Round1.1 hint 5.57 nM / 108.6% **not re-extracted this pass** | Round1 NOT_REPORTED; hint would be EXPLICIT_NUMERIC if re-verified | Results cAMP § (Hanuš) | 10.1073/pnas.96.25.14228 | **Director-named:** PNAS no reabierto este pass → REVIEW. Sin β-arr → no ortogonal. |
| GW405833_func_hCB2_cAMP | cAMP | hCB2 claimed | system unverified | EC50=0.65 nM Round1 | NOT_REPORTED | NOT VERIFIED | Valenzano 2005 DOI 10.1016/j.neuropharm.2005.01.010 | **Director-named:** PDF primario no recuperado. Partial-agonist character **no** certificable sin tabla. |
| RNB61_func_cAMP | cAMP | hCB2 | CHO hCB2 | EC50=0.31±0.07 nM | NOT_REPORTED | Table 1 (Fig 2 risk) | 10.1021/acsptsci.4c00269 | InChIKey N; Emax ausente. |
| LY2828360_func_GTP | GTPγS | CB2 claimed | unverified | EC50=20.1 nM secondary | NOT_REPORTED | PRIMARY TABLE NOT RECOVERED | Lin et al. lineage | Secondary only; bias claim no primary. |
| TEDALINAB_qual | claimed functional/binding | CB2 claimed | not recovered | qualitative fold | NOT_REPORTED | not recovered | WO2006/129178 lineage | Sin tabla primaria. |
| GW405833_Janus_CB1_ant | Janus CB1 | hCB1 | HEK/CHO | qualitative | NOT_REPORTED | pending re-extract | Dhopeshwarkar 2017 | Evidence P. |
| AM1710_Janus_CB1_inv | Janus CB1 | CB1 | in vitro | qualitative | NOT_REPORTED | pending | Dhopeshwarkar 2017 | **Director-named AM1710:** no hCB2 GTPγS GOLD. |
| JD5037_CB2_neg | selectivity | CB2 neg | Tam | fold | NOT_REPORTED | text / Fig 1 | Tam 2012 | Scope CB2-neg; polish Ki absoluto opcional. |

**WIN55,212-2 / CP-55,940 / olorinab “recovery”:** **NO** elevación por inferencia ni números secundarios para inflar N. Permanecen Rejected (refs globales) o REVIEW (olorinab β-arr identity/SI) según buckets GOLD MD.

---

## 6. COUNTS

* cAMP homogeneous = **0**
* GTPγS homogeneous = **0**
* orthogonal Gi/arrestin = **0**
* non-comparable = **18** (filas/claims agrupados en §4; binding-only + Qiu + refs globales contados como clase non-comparable, no como N de filas Round1 exactas)
* review required = **16** (alineado a `ROUND1_GOLD_CANDIDATES.md` / ROUND1B REVIEW list)

**Nota de conteo non-comparable:** §4 lista clases de no-comparabilidad (incluye filas Rejected de Round1 que son binding-only / Qiu / refs). El número operativo para blind-validation prep es: **homogéneos A/B/C = 0**; todo lo demás cae en REVIEW o NON-COMPARABLE.

**Empty subsets = valid scientific outcome** (fidelidad > volumen).

---

## 7. PRIMARY SOURCES ACTUALLY INSPECTED

| # | Source | Form | What verified this pass |
|---|---|---|---|
| 1 | RG7774 / vicasinabin — DOI 10.3389/fphar.2024.1426446 | Frontiers HTML OA (re-fetched) | Methods 2.2.2 cAMP CHOK1hCB2_bgal; 2.2.3 PathHunter β-arr; Results: cAMP EC50 **2.81±0.28** (mCB2 **2.60±0.14** separate); β-arr **99.69±5.72**; “full agonist” **sin % Emax**; same-study dual pathway **sí**, Subset C **no** por conflictos Round1/Emax/identidad |
| 2 | Mukhopadhyay 2016 LEI-101 — DOI 10.1111/bph.13338 / PMC4728411 | PMC HTML (re-fetched) | Named **hydrochloride**; Table 1 β-arr 7.0±0.3 (41±6%); GTPγS 6.6±0.2 (65±8%); cAMP 8.0±0.1 footnote a van der Stelt 2011; Methods PathHunter + GTPγS membranes CHOK1hCB2R_bgal; narrative full-cAMP/partial elsewhere **≠** formal bias |
| 3 | Han 2017 APD371/olorinab — DOI 10.1021/acsmedchemlett.7b00396 | Prior GOLD audit PMC HTML (Tables 1–2); ACS/PMC re-fetch blocked (captcha) this pass | Rely on audit + GOLD MD: cmpd **6** = APD371; hCB2 β-arrestin **6.2 (106)** vs CP-55,940; **not** cAMP; SI PDF still unrecovered |
| 4 | `ROUND1_GOLD_AUDIT_v1.0.md` + `ROUND1_GOLD_CANDIDATES.md` + ROUND1B + Round1.1 CERTIFICATION/QUARANTINE | Local MD/CSV read-only | GOLD_CONFIRMED=0; Director 4-GOLD mismatch; Q11-05/06 AM1710; Q11-03 GW405833; Q11-14 HU-308; Q11-13 vicasinabin β-arr |

**Not opened / blocked this pass:** Hanuš 1999 PNAS PDF (HU-308 quantitative re-extract); Valenzano 2005 (GW405833); Khanolkar 2007 (AM1710); van der Stelt 2011 (LEI cAMP provenance); Han 2017 ACS SI; Lin primary LY2828360.

---

## 8. CRITICAL LIMITATIONS

1. **Homogeneous subsets A/B/C are all empty** under ruthless Emax + identity + same-study rules. This is intentional, not a data-entry failure.
2. **Director “4 GOLD” (HU-308, Vicasinabin, GW405833, AM1710)** map honestly to **REVIEW / NON-COMPARABLE**, not to A/B/C.
3. **Vicasinabin** is the strongest *future* Exam B near-miss (same Frontiers study: cAMP + β-arr), but Round1 β-arr METRIC_CONFLICT + missing numeric Emax + SMILES block prevent Subset C membership **now**.
4. **LEI-101** Table 1 multi-pathway looks orthogonal/GTPγS-ready pharmacologically, but HCl salt vs free-base InChIKey and cAMP footnote-a provenance force REVIEW — do not invent Subset B/C membership.
5. **Olorinab 6.2 nM = β-arrestin**, not cAMP; prior Round1 wording must not drive assay stratification.
6. **AM1710** has **zero** verified hCB2 functional GTPγS/cAMP row usable for Subset B; quarantined EC50 11 nM must not be revived.
7. **HU-308** quantitative cAMP (Round1.1 hint) was **not** re-verified in primary this pass → cannot seed Subset A.
8. **No formal pathway bias** (ΔΔlog / operational framework) established for any molecule → Exam B YES estricto permanece 0; CONDITIONAL near-misses only.
9. Integrity: Round1 CSV, GOLD MD, GOLD AUDIT, CERTIFICATION*, QUARANTINE_LOG **no modificados**. Solo se creó este archivo.

---

*End ROUND1_ASSAY_STRATIFICATION_v1.0 — create-only; empty homogeneous subsets accepted.*
