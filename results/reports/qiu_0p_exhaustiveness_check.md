# 0P exhaustiveness check (honesty memo)

> **Fecha:** 2026-08-13  
> **Pregunta del usuario:** «¿pero has hecho la auditoría exhaustiva?»  
> **Respuesta corta:** **No.** El 0P es una **auditoría first-pass sustancial** (útil para ahorrar: skip discovery H1-a / no 0N), **no** una recuperación exhaustiva del estado del arte. El título del informe 0P («Auditoría exhaustiva») **sobre-nombra** lo hecho.  
> **Artefacto auditado:** [`qiu_0p_state_of_art_audit.md`](qiu_0p_state_of_art_audit.md) + [`qiu_0p_compound_landscape.csv`](qiu_0p_compound_landscape.csv)

---

## Veredicto

| Pregunta | Respuesta honesta |
|----------|-------------------|
| ¿Cubrió las 10 secciones del checklist? | **Sí, estructuralmente** (hay §1–§10 + decisión). |
| ¿Fue exhaustiva en profundidad documental? | **No.** Falta el PDF Qiu principal; Ki/EC₅₀ siguen **NOT FOUND**; patentes = pasada superficial (hereda límites 0IP); citas post-2023 = índice count≈1, sin barrido citing-list completo. |
| ¿La decisión de ahorro sigue en pie? | **Sí, con cautela.** SKIP H1-a *como descubrimiento del signo* se sostiene con SI Fig. S5 cualitativa; **no** se sostiene que “ya tenemos la farmacología cuantitativa”. |

**Etiqueta correcta:** `substantial first-pass audit` — **no** `exhaustive`.

---

## Evidencia dura de acceso (repo `data/papers/`)

| Artefacto | Realidad | Implicación |
|-----------|----------|-------------|
| PDF Qiu full-text | **No recuperado** (paywall / Unpaywall 422; `am.pdf` = stub error 219 B) | Tablas Ki/EC₅₀ del artículo principal **no leídas** → TBD-18 **abierto** |
| SSRN “PDFs” | `qiu_ssrn_live.pdf` = Cloudflare HTML; `qiu_ssrn_wb*.pdf` ≈ abstract Wayback (~80 KB), no paper | No sustituyen el PDF Elsevier |
| SI `mmc1.docx` | **Sí** (~37 MB) | Existe SI local |
| `mmc1.pdf` / `mmc2.pdf` | Stubs XML “NOT FOUND” (189 B) | PDF SI no usable |
| Texto SI (`mmc1_extract.txt`) | Solo **Table S1/S2 MM-GBSA** + captions Fig. S5/S11–S13; **cero** hits `Ki`/`EC50`/`IC50`/`nM` | Farmacología SI = **curvas en figuras**, no tablas numéricas parseadas |
| OCR `si_media` / `image*_ocr.txt` | Curvas HTRF / esquemas sintéticos; **sin** Ki/EC₅₀ tabulados | No cierra TBD-18 |
| PubChem | InChIKey / CID → **NOT FOUND** (`pubchem_cid.json` PUGREST.NotFound; `pubchem_smiles.json` CID 0) | Correctamente marcado NOT FOUND en 0P |
| ChEMBL | Búsqueda keyword fuzzy (`chembl_search.json`); **no** hit estructural Qiu-14 | Correctamente NOT FOUND; profundidad de search = baja |
| ACCESS log Qiu | **Ausente** (solo existe `ge_2023_.../ACCESS_LOG.md`) | No hay auditoría de rutas de acceso Qiu comparable a Ge |
| Citas | OpenAlex `cited_by_count: 1` (péptido 2025) | Coherente con §9; **no** hay dump EuropePMC “citing articles” ni Google Scholar citing walk |

---

## Scorecard vs checklist 0P (§1–§10)

| Item | Status | Evidence in 0P report | Gap |
|------|--------|----------------------|-----|
| **1. Qiu deep dive** | **PARTIAL** | Identidad, DOI/PMID, SMILES/InChIKey, Yin-Yang cualitativo SI Fig. S5, PubChem/ChEMBL NOT FOUND | PDF principal no leído; **números Ki/IC₅₀/EC₅₀ NOT FOUND** (verdadero); selectividad numérica abierta; patente composición = “esta pasada” |
| **2. Chemotype landscape** | **PARTIAL** | Tabla familias (pirazol Yin-Yang, rimonabant, URB447, GW, AM1710, Markush fibrosis, THCV) | No es barrido sistemático de toda la literatura CB Janus; densidad = síntesis repo + hits conocidos |
| **3. Compute → wet precedents** | **DONE** (para decisión ahorro) | Ge ~62–70%, Ji/Wang R², Qiu MM-GBSA, Dhopeshwarkar | No meta-análisis exhaustivo; suficiente para “MD ≠ reemplaza H1-a” |
| **4. MD precedents** | **DONE** (para decisión ahorro) | Qiu MD, Ge, lipid entry, PNAS entropy; 0N BLOCKED | Lista corta; no revisión completa MD-CB2 |
| **5. Compound table / CSV** | **PARTIAL** | CSV ~20 filas; Qiu-14..24 + Janus refs + Ge examples; regla NOT FOUND respetada | Qiu potencies vacías; varios controles con potencies “approx / NOT FOUND this audit”; no BindingDB dump |
| **6. Patents** | **PARTIAL** | WO2022026478 / US20230234928, Sanofi, note Markush; composición Qiu-14 NOT FOUND | **Shallow:** Google Patents + reuso 0IP; **no** Espacenet family walk, **no** CNIPA deep search, **no** claim chart, **no** Derwent/SciFinder (0IP lo admite) |
| **7. Fibrosis & CB2** | **PARTIAL** | Escalera receptor→ligando→combo→clínico; Qiu-14 fibrosis NOT FOUND | Reusa auditorías previas del repo; no search exhaustivo fibrosis×Janus 2023–2026 |
| **8. Skip-map (0D…H2)** | **DONE** | Tabla clara NO GASTAR / skip discovery / 0N no justificado | Depende de gaps §1 (PDF); lógica de skip discovery es sólida |
| **9. Post-2023 citations** | **PARTIAL** | 1 citing (OpenAlex/EuropePMC count); no reuse 14/15/20/24 | Solo índice `cited_by_count`; **no** lista citing completa multi-fuente; follow-up autores = “esta pasada” |
| **10. DECISIÓN** | **DONE** | Códigos 🟢/🟡/🔴/🟠; 5 preguntas; H1-a SKIP discovery / CONDICIONAL ancla; next = TBD-18 | Correcta **como decisión de ahorro**; **no** implica que la evidencia cuantitativa esté cerrada |

---

## Inflación a evitar (lo que el 0P *no* debe vender)

1. **«Auditoría exhaustiva»** en el título → falso. Mejor: first-pass save-money audit.  
2. **«SI recuperada» ≠ «tablas Ki recuperadas».** SI docx sí; tablas de potencia **no**.  
3. **PubChem/ChEMBL NOT FOUND** es evidencia de ausencia en DB, **no** de que Qiu no publicara números (probablemente están en el PDF paywalled).  
4. **Patente Qiu-14 NOT FOUND** ≠ FTO / inexistencia (CN/PCT posible; búsqueda superficial).  
5. **citedByCount = 1** ≠ revisión exhaustiva de citas (sí es señal fuerte de baja adopción, pero método limitado).

---

## ¿Qué sí se hizo bien?

- Mentalidad ahorro (no “PASS para continuar”).  
- Epistemología NOT FOUND / no inventar potencias Qiu.  
- Decisión estratégica coherente: no pagar discovery H1-a del signo; no fundear 0N/más docking ahora.  
- CSV honesto con huecos explícitos.  
- Integración de 0D–0N / 0IP / fibrosis docs del repo.

---

## Next retrievals (2–4) para acercarse a “exhaustivo” — **sin** docking/MD

1. **TBD-18 — PDF Qiu + tablas de potencia:** obtener full-text Elsevier (o copia institucional) y extraer **literalmente** cualquier Ki/IC₅₀/EC₅₀ / selectividad de tablas principales + SI; log de ACCESS estilo Ge.  
2. **OCR dirigido de Fig. S5 / S11–S13** (y tablas del main PDF): si los números solo están en ejes/anotaciones de figura, documentarlos como *figure-estimated* vs *table-published* (nunca inventar).  
3. **Espacenet claim chart** (mínimo): familia WO2022026478 / US20230234928 + búsqueda CN/PCT por autores Qiu/Zhao/Tao + keywords pyrazole + morpholine + adamantyl + CB1/CB2; tabla claim ↔ Qiu-14 (aún **no** FTO).  
4. **EuropePMC / OpenAlex citing articles list** (export completo) + Semantic Scholar citations + búsqueda autores ShanghaiTech post-2023 por follow-up SAR — cerrar §9 más allá del count=1.

Opcional (5º si se quiere DB-clean): BindingDB structure search + ChEMBL similarity on exact InChIKey (no keyword fuzzy).

---

## Cierre

```text
0P EXHAUSTIVENESS = FAIL AS "EXHAUSTIVE"
0P AS SAVE-MONEY FIRST PASS = PASS (USEFUL)
QUANTITATIVE QIU PHARMACOLOGY = STILL OPEN (TBD-18)
DO NOT INFLATE
```
