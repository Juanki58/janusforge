# CB2 Experimental Master Dataset — v1.0 Round 1.1 CERTIFICATION

**Fecha:** 2026-08-16  
**Fase:** 2A — Round 1.1 Certification (LEVEL 0)  
**Inputs inmutables (solo lectura):**
- `results/reports/CB2_Experimental_Master_Dataset_v1.0_Round1.csv`
- `results/reports/QUARANTINE_LOG.md`
- contexto: `results/reports/CB2_Experimental_Master_Dataset_v1.0_Round1.md`

**Outputs Round 1.1:**
- `results/reports/CB2_Experimental_Master_Dataset_v1.0_Round1.1_CERTIFICATION.csv`
- `results/reports/CB2_Experimental_Master_Dataset_v1.0_Round1.1_CERTIFICATION.md` (este archivo)
- `results/reports/ROUND1.1_CERTIFICATION_QUARANTINE.md`

**Prohibiciones respetadas:** sin búsqueda de moléculas nuevas; sin docking/MD/scoring; sin commits git; sin sobreescritura de Round 1 CSV ni `QUARANTINE_LOG.md`.

---

## 1. Método

1. Enumeración completa de **55** filas de datos Round 1 (CSV header + 55 records).
2. Verificación preferente contra fuentes primarias en disco (`data/papers/`: Vasiljevik PMC HTML/PDF, Qiu SI `mmc1_document.txt`, etc.).
3. Recuperación abierta vía red **solo para verificación** (PMC / Frontiers / PNAS mirrors / escholarship): URB447 (LoVerme), LEI-101 (Mukhopadhyay), olorinab/APD371 (Han), RG7774/vicasinabin (Frontiers), HU-308 (Hanuš), RNB-61 (Chicca), JD5037 (Tam).
4. Si PDF primario no recuperable → **HOLD** + `PRIMARY_SOURCE_UNAVAILABLE` (no inventar; secondary/vendor/GtoPdb ≠ sustituto).
5. Discrepancias: **no** se corrige Round 1; se registran en CSV de certificación + cuarentena Round 1.1.
6. Métricas: no intercambiar IC50/Ki/Kd/EC50/Emax; no convertir pKi/pEC50 a nM; no mezclar especies/sistemas; no inferir sesgo Gi ni cinética desde estructura/docking.

### Estados de certificación (solo estos)

| Status | Uso |
|--------|-----|
| **CERTIFIED** | Valor + ensayo + sistema + localización exacta inequívocos en primario |
| **CERTIFIED_WITH_SCOPE** | Primario OK pero con caveat material (IC50≠Ki, cualitativo, especie, assay mal etiquetado en Round1, etc.) |
| **HOLD** | Primario no disponible / outcome no determinable / challenge blinded / refs globales |
| **REJECT** | Inferencia (I) o no usable como evidencia experimental de fenotipo |

---

## 2. Criterios Exam A / B / C (Round 1.1)

### Exam A — Estado funcional (hCB2)
**YES** solo si: receptor **hCB2** + ensayo **funcional** identificado + sistema celular identificado + EC50 / IC50 funcional / Emax inequívoco + localización exacta en primario.  
**NO** binding Ki como sustituto funcional. **NO** docking/MM-GBSA.

### Exam B — Señalización / sesgo
**STRICT:** se requiere evidencia primaria de vía tipo Gi/cAMP (o equiv.) **y** β-arrestin, con receptor/especie/sistemas identificables y proveniencia primaria.  
**No** auto-etiquetar “Gi-biased”. Si ambas vías existen sin análisis formal de sesgo → `Exam_B_Eligible = CONDITIONAL` + `BIAS_NOT_ESTABLISHED`.  
Ninguna fila Round 1.1 alcanza **YES** estricto de sesgo formal (factor/ΔΔlog o equivalente).

### Exam C — Fenotipo farmacológico (conservador)
**YES** solo si:
1. dual CB1/CB2 funcional verificado en primario (Janus / Yin-Yang experimental), **o**
2. rol de control negativo CB2 / comparador CB1-selectivo verificado en primario,  
con localización exacta.  
En caso contrario **NO**. Qiu challenge set: **NO** para Exam C (blindado).

---

## 3. Auditorías especiales (resumen)

| Caso | Hallazgo Round 1.1 |
|------|-------------------|
| **HU-308** | Ki 22.7±3.9 / CB1 >10 µM CERTIFIED(+scope especies). cAMP: Round1 cualitativo; primario también da EC50 5.57 nM, Emax 108.6% → CERTIFIED_WITH_SCOPE. Sin β-arr → no Gi-bias. |
| **RG7774 / vicasinabin** | Ki 51.3±16.2; cAMP EC50 2.81±0.28 CERTIFIED. β-arr **99.69±5.72 nM** (Fig 3B) — Round1 ~22 **incorrecto**. Exam B = CONDITIONAL. |
| **AM1710** | Ki 6.7 / 360 HOLD (PDF Khanolkar no abierto). EC50 11 nM sigue Q-05; no confligir métricas. |
| **APD371 / olorinab** | EC50 6.2 nM es **β-arrestin PathHunter** (Table 1), **no** cAMP. CERTIFIED_WITH_SCOPE. |
| **URB447** | Binding = IC50 (CERTIFIED_WITH_SCOPE). GTPγS CB1 CERTIFIED. cAMP mCB2 cualitativo CERTIFIED_WITH_SCOPE. |
| **LEI-101** | pKi/pEC50 Table 1 CERTIFIED; diferencias de vía sin label Gi-biased; Exam B CONDITIONAL. |
| **Kinetic-Gold** | 0 filas kon/koff/residence en Round 1 / primarios auditados. |
| **Qiu challenge** | 14 cualitativo S5 = CERTIFIED_WITH_SCOPE; S173/S285 = REJECT (I); resto HOLD + QIU_BLINDED. |
| **GW405833 / Valenzano** | HOLD — PDF primario no recuperado. |
| **JWH-133** | Valores alineados Huffman 1999; venue correcta = **Bioorg Med Chem** (no J Med Chem) → WITH_SCOPE. |
| **RNB-61** | Table 1 OK; Fig 2 riesgo swap paneles → WITH_SCOPE en cAMP; Exam B CONDITIONAL. |
| **CP/WIN** | HOLD — prohibido Ki global único. |

---

## 4. Discrepancias materiales (no se corrigió Round 1)

1. **Olorinab EC50 6.2 nM** = β-arrestin, no cAMP (Han 2017 Table 1).
2. **Vicasinabin β-arr** Round1 ~22 nM vs primario **99.69 ± 5.72 nM**.
3. **HU-308** Round1 omitió EC50/Emax cuantitativos presentes en Hanuš 1999.
4. **JWH-133** venue Round1 “J Med Chem” → Bioorg Med Chem 1999.
5. **VAS30 mCB1 Ki** Round1 37.2 vs Table 2 **37.3 ± 11.8**.
6. **RNB-61 Fig 2** prosa/caption pueden intercambiar EC50 cAMP vs GTPγS — anclar Table 1.
7. Filas GW405833 / AM1710 binding: cifras Round1 no re-verificadas en PDF primario este round → HOLD.

---

## 5. Integridad

- Round 1 CSV: **no modificado**.
- `QUARANTINE_LOG.md` Round 1: **no modificado**.
- Git: **sin commits / sin cambios de rama**.
- Filas examinadas: **55 / 55**.
- Fidelidad > volumen: se prefiere HOLD a CERTIFIED falso.

---

## 6. Tabla de métricas (EXACTA)

| Métrica | Resultado |
|---------|-----------|
| Filas Round 1 examinadas | 55 |
| CERTIFIED | 14 |
| CERTIFIED_WITH_SCOPE | 20 |
| HOLD | 20 |
| REJECT | 1 |
| Exam A eligible | 8 |
| Exam B eligible | 6 |
| Exam C eligible | 8 |
| hCB2 humano verificado | 17 |
| Filas con bias formalmente demostrable | 0 |
| Filas con datos cinéticos | 0 |
| Qiu challenge blindado | YES |

**Nota Exam B:** las 6 filas elegibles son todas `CONDITIONAL` (vías duales presentes sin análisis formal de sesgo): LEI-101 cAMP/β-arr/GTPγS; vicasinabin cAMP/β-arr; RNB-61 cAMP. Exam B **YES** estricto = 0.

---

## LEVEL 0 STATUS = CONDITIONAL

**Rationale:** hay un núcleo usable de filas CERTIFIED / CERTIFIED_WITH_SCOPE con localización primaria, pero (i) 20 HOLD por primario no recuperado o challenge/refs, (ii) discrepancias materiales Round1 vs primario (olorinab assay type; vicasinabin β-arr value), (iii) 0 bias formal y 0 cinética, (iv) Qiu permanece blindado. No se infla PASS.
