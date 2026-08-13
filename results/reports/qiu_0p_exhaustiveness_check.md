# 0P exhaustiveness check — post deep retrieval (2026-08-13)

> **Pregunta:** «¿pero has hecho la auditoría exhaustiva?»  
> **Respuesta tras esta pasada:** **Sí, como auditoría documental exhaustiva de vías públicas/locales razonables.**  
> **No** significa que se hayan recuperado las tablas Ki/EC₅₀ del PDF Elsevier (siguen **bloqueadas**).  
> **Etiqueta correcta ahora:** `exhaustive public/local retrieval audit` — pharmacology tables still **OPEN/BLOCKED**.

**Artefactos:** [`qiu_0p_state_of_art_audit.md`](qiu_0p_state_of_art_audit.md) · [`qiu_0p_compound_landscape.csv`](qiu_0p_compound_landscape.csv) · [`data/papers/qiu_2023_bioorg/ACCESS_LOG.md`](../../data/papers/qiu_2023_bioorg/ACCESS_LOG.md)

---

## Veredicto

| Pregunta | Respuesta |
|----------|-----------|
| ¿Se intentaron todas las vías públicas/locales razonables? | **Sí** (Unpaywall, EuropePMC, CORE, OpenAlex, S2, SSRN, Wayback, SciDirect dump, SI docx+OCR, ResearchGate search, chem DBs exactas, patents Google Patents HTML, citas multi-fuente, follow-up autores). Sci-Hub **no** (sin precedente legal en repo). |
| ¿Se recuperaron Ki/IC₅₀/EC₅₀ de Qiu-14/15/20/24? | **No** — confirmado ausentes en SI texto/OCR y DBs; PDF principal sigue cerrado. |
| ¿Cambia la recomendación H1-a skip discovery? | **No.** El signo Yin-Yang sigue PUBLICADO cualitativamente; números siguen NOT FOUND. |

---

## Scorecard actualizado (§1–§10)

| Item | Status | Cambio vs first-pass |
|------|--------|----------------------|
| **1. Qiu deep dive** | **PARTIAL → DONE (retrieval) / BLOCKED (numbers)** | ACCESS_LOG completo; SI Scheme S1 + HTRF OCR + MM-GBSA; PDF tables still blocked |
| **2. Chemotype landscape** | **DONE** (for save-money) | Sin cambio material; densidad suficiente |
| **3. Compute → wet precedents** | **DONE** | Sin cambio |
| **4. MD precedents** | **DONE** | Sin cambio; 0N sigue no justificado |
| **5. Compound CSV** | **DONE (honest gaps)** | Potencies Qiu aún NOT FOUND; MM-GBSA anotado como compute; Azo23 fila nueva |
| **6. Patents** | **DONE (inventory)** | WO/US HTML parse; Compound 1 Ki 1 / >1000 nM VERIFIED; claim themes fibrosis; Qiu composition patent NOT FOUND; no FTO |
| **7. Fibrosis & CB2** | **DONE** (for decision) | Sin cambio: Qiu-14 fibrosis NOT FOUND |
| **8. Skip-map** | **DONE** | Sin cambio de códigos |
| **9. Post-2023 citations** | **DONE** | Lista citing completa (n=1); autor follow-up Azo23 2026 documentado (no reuse 14) |
| **10. DECISIÓN** | **DONE** | H1-a discovery **SKIP** reafirmado; ancla CONDICIONAL |

---

## Evidencia dura nueva (esta pasada)

| Hallazgo | Valor |
|----------|-------|
| Unpaywall | closed; zero OA locations |
| CORE | 0 hits |
| Citing OpenAlex + EuropePMC | **Chen et al. 2025** DOI 10.1016/j.bioorg.2025.108770 — **cite only** |
| Semantic Scholar citations | empty / count 0 (lag) |
| Author follow-up | Qiu/Tao **2026** DOI 10.1016/j.ejmech.2026.118883 — **Azo23** photoswitch; opposite CB1/CB2 control; **≠** Qiu-14 |
| PubChem/ChEMBL exact InChIKey 14/15/20/24 | **CONFIRMED NOT FOUND** |
| BindingDB SMILES | endpoint 404 / no hit |
| Makriyannis Compound 1 | CB1 Ki **1 nM**; CB2 Ki **>1000 nM** (patent text) |
| SI MM-GBSA (compute) | 14/15/20/24 scores recovered — **not** wet potencies |
| Main PDF tables | still **BLOCKED** |

---

## Cierre

```text
0P EXHAUSTIVE RETRIEVAL = DONE (PUBLIC/LOCAL)
QUANTITATIVE QIU PHARMACOLOGY = STILL BLOCKED (TBD-18 INSTITUTIONAL PDF)
H1-a DISCOVERY SKIP = UNCHANGED
DO NOT INVENT NUMBERS
```
