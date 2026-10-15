# CB2 Experimental Master Dataset — v1.0 Round 1 (RAW)

**Estado:** curación cruda Round 1 — NO pulido.  
**Fecha:** 2026-08-16  
**Alcance:** solo extracción / curación experimental. **Prohibido:** docking, MD, diseño NCE, inventar números, convertir I→D, git commit/push.  
**CSV:** `results/reports/CB2_Experimental_Master_Dataset_v1.0_Round1.csv`  
**Nota gitignore:** `*.csv` está en `.gitignore` del repo; el CSV se escribe igual y puede no versionarse.  
**Quarentena:** `results/reports/QUARANTINE_LOG.md`

---

## 1. Método (Round 1)

### Fuentes locales
- `data/papers/mmc1_document.txt` / `mmc1_extract.txt` / `mmc1.docx` (SI Qiu 2023)
- `results/reports/qiu_0d_structure_verification.md` (SMILES/InChIKey 14/15/20/24)
- `results/reports/qiu_0q2f_regioisomer_14_15_16_audit.md` (matriz experimental SI)
- `docs/mapa_ligandos_janus_cb1_cb2.md` (mapa literario; no sustituye primary)
- `data/papers/vasiljevik_2013/` (PMC HTML / extractos)
- **`qiu_0p`:** no hallado como artefacto nombrado en repo Round 1

### Fuentes externas (WebSearch / PMC / GtoPdb / PubChem)
Solo para semillas no-Qiu y DOIs/PMID. Números solo si aparecen en primary o extracto primary-equivalente (PMC full text).

### Reglas de evidencia
| Tag | Significado |
|-----|------------|
| **D** | Demostrado directamente en fuente primaria (tabla/caption/texto inequívoco) |
| **P** | Parcialmente demostrado / relectura / secondary-confirmed pending |
| **I** | Inferido (docking/MD/hipótesis) — **nunca** tratar como D |
| **N** | No disponible / outcome no legible |

### Qiu — reglas especiales (obligatorias)
1. **NO** asumir 14=ago, 15=ant, 20/24=inactive.
2. Qiu-14 Yin-Yang: **D** solo cualitativo cAMP CB2-ago + CB1-ant si SI/caption lo soporta (Fig. S5).
3. **S173 / S285 = I** (mecanismo docking/MD) → `include_in_benchmark=NO`.
4. Qiu-15/16/20/24: **HOLD** o **N** salvo tabla/figura primaria clara; citar figura/tabla exacta.
5. Sin IC50/EC50/Emax en texto SI para 14/15/16 (auditoría 0Q.2F).

### Integridad NIVEL 0
Cada fila debe tener: identidad química (nombre + InChIKey/SMILES si conocido), ensayo, sistema, ref primaria, tag D/P/I/N.  
Si falta → `include_in_benchmark=NO` o `HOLD`.

---

## 2. Partición propuesta de familias / scaffolds (solo diseño; NO modelos)

| Familia | Ejemplos seed | Rol propuesto Round1 |
|---------|---------------|----------------------|
| F1 Pirrol Janus | URB447 | TRAIN candidate (ancla conceptual) |
| F2 Indol aminoalquilo / N-acil | GW405833; Vasiljevik 27/30 | TRAIN candidate (Janus-like / dual) |
| F3 Cannabilactona | AM1710 | TRAIN candidate (afinidad CB2) |
| F4 Pirazol Yin-Yang Qiu | Qiu-14/15/16/20/24 | **CHALLENGE SET** — no training |
| F5 Imidazolidinediona periférica | LEI-101 | HOLD-OUT / peripheral tool |
| F6 Clínico/pipeline CB2-selectivo | olorinab, vicasinabin, LY2828360, tedalinab, RNB-61 | HOLD-OUT clínico / chemotype diverso |
| F7 Clásico CB2-selectivo | HU-308, JWH-133 | TRAIN refs de selectividad |
| F8 Refs no selectivas | CP55,940; WIN55,212-2 | calibración ensayo (no labels Janus) |
| F9 Control negativo CB2 | JD5037 | CB1-only / CB2-neg control |

**Propuesta TRAIN vs HOLD-OUT (solo propuesta):**
- **TRAIN (candidato):** F1, F2 (parcial), F3, F7 + refs F8 para normalización de ensayo.
- **HOLD-OUT (candidato):** F5, F6 (olorinab/vicasinabin/RNB-61/LY/tedalinab).
- **CHALLENGE (fijo):** serie Qiu completa (F4) — evaluación ciega posterior; **no** entrenar fenotipos.

---

## 3. Definiciones Examen A/B/C (diseño solo; no ejecutar)

| Examen | Pregunta | Etiqueta objetivo (futuro) | No confundir con |
|--------|----------|----------------------------|------------------|
| **A — Estado funcional** | ¿Agonista / antagonista / inverso / neutro / inactivo en un readout dado? | `func_state` | Afinidad sola (Ki) |
| **B — Tipo de señalización** | ¿cAMP vs GTPγS vs β-arr vs binding vs internalización? | `signal_type` + sesgo relativo | Un solo EC50 “global” |
| **C — Fenotipo farmacológico** | ¿CB2-ago selectivo / Janus Yin-Yang / CB1-ant limpio / control neg? | `pharm_phenotype` | Pose docking o contacto S173/S285 |

Round 1 solo documenta candidatos de etiqueta en columna `phenotype_label_candidate`; no cierra A/B/C.

---

## 4. Tabla markdown — filas clave (subset)

| molecule_id | molecule_name | value_type | value | units | evidence | include |
|-------------|---------------|------------|-------|-------|----------|---------|
| URB447_bind_hCB2 | URB447 | IC50 | 41 ± 23 | nM | D | YES |
| URB447_bind_rCB1 | URB447 | IC50 | 313 ± 72 | nM | D | YES |
| GW405833_bind_hCB2 | GW405833 | Ki | 3.92 | nM | D | YES |
| AM1710_bind_CB2 | AM1710 | Ki | 6.7 | nM | D | YES |
| VAS27_bind_hCB2 | Vasiljevik 27 | Ki | 10.9 | nM | D | YES |
| VAS30_bind_hCB2 | Vasiljevik 30 | Ki | 26.5 | nM | D | YES |
| QIU14_func_CB2_ago_cAMP | Qiu-14 | qualitative | CB2 ago (S5A) | — | D | HOLD |
| QIU14_func_CB1_ant_cAMP | Qiu-14 | qualitative | CB1 ant (S5B) | — | D | HOLD |
| QIU14_mech_S173_S285 | Qiu-14 | qualitative | S173/S285 hyp. | — | I | NO |
| QIU15_func_panels | Qiu-15 | qualitative | N | — | N | HOLD |
| QIU20_func / QIU24_func | Qiu-20/24 | qualitative | N | — | N | HOLD |
| LEI101_func_cAMP | LEI-101 | pEC50 | 8.0 ± 0.1 | pEC50 | D | YES |
| OLORINAB_func_hCB2 | olorinab | EC50 | 6.2 | nM | D | YES |
| VICASINABIN_func_cAMP_hCB2 | vicasinabin | EC50 | 2.81 ± 0.28 | nM | D | YES |
| HU308_bind_CB2 | HU-308 | Ki | 22.7 ± 3.9 | nM | D | YES |
| JWH133_bind_CB2 | JWH-133 | Ki | 3.4 | nM | D | YES |
| RNB61_bind_hCB2 | RNB-61 | Ki | 0.57 ± 0.03 | nM | D | YES |
| TEDALINAB_qual | tedalinab | qualitative | N numbers | — | N | HOLD |
| JD5037_bind_CB1 | JD5037 | Ki | 0.35 | nM | D | YES |
| LY2828360_* | LY2828360 | Ki/EC50 | secondary | nM | P | HOLD |

Ver CSV completo para todas las filas.

---

## 5. Caveats Round 1 (WARNINGS)

### Estructura
- Qiu-14/15/20/24: InChIKey de 0D (PASS). Qiu-16: identidad o/m/p D; SMILES/InChIKey **pending**.
- Vasiljevik 27/30: SMILES derivados de IUPAC local; **InChIKey = N** hasta RDKit/PubChem.
- RNB-61: Ki/EC50 D desde Table 1 paper; **InChIKey N** Round1.
- Tedalinab: posible discrepancia estereo InChIKey Wikipedia vs PubChem CID.
- Sales (LEI-101·HCl): InChIKey de sal HCl vs free base — documentar en Round2.

### Ensayos / unidades
- **IC50 ≠ Ki ≠ EC50.** URB447 Table 1 = IC50 binding.
- LEI-101 reportado como **pKi/pEC50** (no convertir a nM en benchmarks sin flag).
- Especies mezcladas: rat CB1 (URB), mouse CB1 (Vasiljevik), hCB2 frecuente — **no pool** ciego.
- GW405833 / AM1710 “Janus”: **P** vía Dhopeshwarkar 2017; no igualar a URB447 D.

### Figuras Qiu
- Fig **S5**: única ancla D cualitativa Yin-Yang de **14**.
- Fig **S6**: docking regioisómeros — **computacional**, no fenotipo.
- Fig **S11–S13**: presencia de paneles ≠ desenlace; OCR sin `Cpd 14` en S11–S13; 15 ausente en S13 OCR.
- Tables **S1/S2**: MM-GBSA — **no** farmacología experimental.

---

## 6. Discrepancias abiertas (segundo curator)

1. Recuperar **tabla farmacológica principal** Qiu 2023 (PDF) — potencias 14/15/16/20/24.
2. Alta resolución paneles S11–S13: ¿15/16 activos o planos?
3. AM1710: Ki 6.7 vs pantallas Rahn (mCB2 17 / rCB1 282) — ¿qué fila es canónica TRAIN?
4. GW405833: rango Ki 4–12 nM en mapas internos vs 3.92 Valenzano — reconciliar.
5. LY2828360: confirmar Table primary (Ki 40.3 / EC50 20.1) — ahora P/HOLD.
6. Tedalinab: localizar Ki/EC50 primary o mantener N/HOLD.
7. JWH-133: verificar DOI Huffman exacto + tabla Ki 3.4 / 677.
8. Vasiljevik: EC50 AC numéricos si existen fuera del texto extractado.
9. RNB-61 Fig2: posible confusión de paneles GTP vs cAMP en prosa — usar **Table 1**.
10. CP55,940 / WIN: no fijar un solo Ki global Round1.

---

## 7. Referencias primarias (lista corta)

1. LoVerme et al. URB447 — DOI 10.1016/j.bmcl.2008.12.059  
2. Valenzano et al. GW405833 — DOI 10.1016/j.neuropharm.2005.01.010  
3. Khanolkar et al. cannabilactonas / AM1710 — DOI 10.1021/jm070441u  
4. Dhopeshwarkar et al. Janus GW/AM1710 — DOI 10.1124/jpet.116.236539  
5. Vasiljevik et al. — DOI 10.1021/jm400268b  
6. Qiu et al. — DOI 10.1016/j.bioorg.2023.106377 (+ SI mmc1)  
7. Mukhopadhyay et al. LEI-101 — DOI 10.1111/bph.13338  
8. Han et al. APD371/olorinab — DOI 10.1021/acsmedchemlett.7b00396  
9. RG7774/vicasinabin — DOI 10.3389/fphar.2024.1426446  
10. Hanus et al. HU-308 — DOI 10.1073/pnas.96.25.14228  
11. Huffman et al. JWH-133 lineage — J Med Chem 1999 (confirmar DOI Round2)  
12. RNB-61 — DOI 10.1021/acsptsci.4c00269  
13. Tam et al. JD5037 — DOI 10.1016/j.cmet.2012.07.002  
14. Soethoudt et al. CB2 ligand profiling — DOI 10.1038/ncomms13958 (contexto selectividad; no sustituye primary por ligando)

---

## 8. Explicit non-claims

- No novelty claim.
- No docking/MD como evidencia funcional.
- No conversión I→D.
- No fenotipos inventados para Qiu-15/16/20/24.
- Round 1 = curación; benchmarks A/B/C = diseño futuro.
