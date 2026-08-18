# QUARANTINE_LOG — CB2 Master Dataset Round 1

**Fecha:** 2026-08-16  
**Relacionado:** `CB2_Experimental_Master_Dataset_v1.0_Round1.csv` / `.md`  
**Regla:** ítems aquí = no usar como D en benchmark hasta reconciliación.

---

## Q-01 — Qiu potencias cuantitativas (14/15/16/20/24)

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED |
| Motivo | PDF principal / tabla farmacológica no recuperada; SI sin IC50/EC50/Emax en texto |
| Evidencia local | mmc1 Fig S5 cualitativa (solo 14); 0Q.2F INSUFFICIENT |
| Acción Round2 | Extraer tabla principal Elsevier/SSRN; no inventar |

## Q-02 — Qiu-15 / 16 fenotipo funcional

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED |
| Motivo | Paneles S11–S13 presentes (OCR) pero desenlace activo/inactivo NOT DETERMINABLE |
| Prohibido | Asumir pérdida de Yin-Yang por meta/para; Fig S6 es docking |
| Tag | N / HOLD |

## Q-03 — Qiu-20 / 24 “inactivos”

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED |
| Motivo | Sin caption/tabla que declare inactividad; identidad 0D OK |
| Tag | N / HOLD |

## Q-04 — Qiu S173 / S285

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED AS INFERENCE |
| Motivo | Hipótesis docking/MD del paper |
| Tag | **I** obligatorio |
| include_in_benchmark | **NO** |

## Q-05 — AM1710 EC50 “11 nM”

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED |
| Motivo | Aparece en mapa interno repo; primary Round1 ancla Ki 6.7 nM (Khanolkar); EC50 11 nM no verificada aquí |
| Acción | No promover a D sin primary |

## Q-06 — GW405833 / AM1710 como “Janus limpio”

| Campo | Valor |
|-------|-------|
| Status | PARTIAL / HOLD |
| Motivo | Dhopeshwarkar 2017 = P; mecanismo CB1 complejo / no competitivo ≠ URB447 |
| Tag | P |

## Q-07 — LY2828360 números

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED |
| Motivo | Ki 40.3 / EC50 20.1 circulan en secondary/vendor; primary table no extraída Round1 |
| Tag | P → HOLD |

## Q-08 — Tedalinab potencias

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED |
| Motivo | Selectividad >4700× citada en secondary; sin Ki/EC50 primary verificado |
| Tag | N / HOLD |

## Q-09 — Vasiljevik 27/30 InChIKey

| Campo | Valor |
|-------|-------|
| Status | IDENTITY PARTIAL |
| Motivo | SMILES desde IUPAC local; InChIKey no PubChem-confirmado |
| Acción | RDKit + deposit search Round2 |

## Q-10 — RNB-61 InChIKey + Fig2 panel swap risk

| Campo | Valor |
|-------|-------|
| Status | STRUCTURE ID PENDING / ASSAY READ CAVEAT |
| Motivo | Table 1 números usados (D); InChIKey ausente; prosa Fig2 puede intercambiar paneles |
| Acción | Anclar solo Table 1 hasta re-lectura Fig2 |

## Q-11 — JWH-133 DOI exacto

| Campo | Valor |
|-------|-------|
| Status | REF POLISH PENDING |
| Motivo | Ki 3.4 / 677 ampliamente citados Huffman 1999; DOI exacto a fijar Round2 |
| Tag | D provisional con caveat |

## Q-12 — CP55,940 / WIN55,212-2 Ki únicos

| Campo | Valor |
|-------|-------|
| Status | QUARANTINED AS SINGLE GLOBAL NUMBER |
| Motivo | Refs multi-ensayo; un solo Ki inventado = violación integridad |
| Acción | Filas por ensayo cuando se curen; Round1 = note only HOLD |

## Q-13 — vicasinabin β-arr EC50 exacto

| Campo | Valor |
|-------|-------|
| Status | HOLD |
| Motivo | Texto Frontiers indica menos potencia que cAMP (±5.72); valor puntual a confirmar Fig 3B |
| Tag | P |

## Q-14 — Artefacto `qiu_0p`

| Campo | Valor |
|-------|-------|
| Status | MISSING |
| Motivo | No encontrado en repo bajo ese nombre Round1 |
| Acción | Localizar o declarar N/A |

## Q-15 — CSV gitignore

| Campo | Valor |
|-------|-------|
| Status | INFO |
| Motivo | `*.csv` en `.gitignore`; archivo escrito pero puede no trackearse |
| Acción | Excepción git o export MD-only si hace falta versionar |

---

## Resumen operativo

| Acción | Conteos approx Round1 |
|--------|------------------------|
| Filas YES (benchmark-usable D) | ver CSV `include_in_benchmark=YES` |
| Filas HOLD | toda serie Qiu funcional cuantitativa; LY; tedalinab; refs globales CP/WIN; Janus P |
| Filas NO | S173/S285 (I) |

**Criterio de salida de cuarentena:** primary table/figura citada + segundo curator OK + tag D o P explícito sin inventar.
