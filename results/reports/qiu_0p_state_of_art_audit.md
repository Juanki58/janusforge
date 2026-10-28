# Qiu 0P — Auditoría del estado del arte (pasada exhaustiva documental)

> **Fecha:** 2026-08-13 (deep retrieval pass)  
> **Modo:** investigación + auditoría **solo**. **Prohibido:** docking nuevo, MD, NCE, síntesis, PDBQT, ensayos, campañas SAR.  
> **Mentalidad:** ahorrar gasto; no inventar potencias.  
> **CSV:** [`qiu_0p_compound_landscape.csv`](qiu_0p_compound_landscape.csv)  
> **Exhaustiveness:** [`qiu_0p_exhaustiveness_check.md`](qiu_0p_exhaustiveness_check.md)  
> **ACCESS:** [`data/papers/qiu_2023_bioorg/ACCESS_LOG.md`](../../data/papers/qiu_2023_bioorg/ACCESS_LOG.md)

**Capas:** PUBLICADO · REPO · INFERENCIA · NOT FOUND · **BLOCKED** (vía intentada, recurso inaccesible)

| Sección | Status |
|---------|--------|
| §1 Qiu deep dive (identidad + SI + DBs + ACCESS) | **DONE** retrieval / **BLOCKED** numeric tables |
| §2 Chemotype landscape | **DONE** |
| §3 Compute → wet | **DONE** |
| §4 MD precedents | **DONE** |
| §5 Compound table/CSV | **DONE** (gaps honestos) |
| §6 Patents inventory | **DONE** (≠ FTO) |
| §7 Fibrosis ladder | **DONE** |
| §8 Skip-map | **DONE** |
| §9 Post-2023 citations + author follow-up | **DONE** |
| §10 DECISIÓN + 5 preguntas | **DONE** (re-answered) |

---

## Resumen ejecutivo (ahorro) — post exhaustivo

1. **PDF Qiu principal sigue BLOCKED** tras Unpaywall (closed), EuropePMC (no PDF), CORE (0), SSRN (403), Wayback (sin fulltext), SciDirect shell, ResearchGate sin PDF usable. Sci-Hub **no** usado (sin precedente en repo).  
2. **SI local sí se parseó por completo:** Fig. S5 Yin-Yang cualitativo de **14**; Fig. S11–S13 curvas HTRF de la serie; Scheme S1 identidades; Tables S1–S2 = **solo MM-GBSA** (cómputo). **Cero** Ki/IC₅₀/EC₅₀/nM en texto SI.  
3. **PubChem / ChEMBL / BindingDB:** exact InChIKey/SMILES de **14/15/20/24** → **CONFIRMED NOT FOUND**.  
4. **Citas:** exactamente **1** (Chen 2025 péptido) — cite only. **Follow-up autores 2026:** Azo23 photoswitch — chemotipo distinto; **no** reutiliza 14/15/20/24.  
5. **Patentes:** WO2022026478 / US20230234928 claim themes verificados en HTML Google Patents; Compound 1 Ki CB1 **1 nM** / CB2 **>1000 nM**; patente composición Qiu-14 **NOT FOUND**.  
6. **H1-a discovery SKIP se mantiene** — la farmacología cuantitativa **no** se recuperó; el signo cualitativo **sí** basta para no pagar “descubrimiento”. Ancla operativa sigue **CONDICIONAL**.

---

## 1. Qiu-14 — deep dive

### 1.1 Identidad / nombres / estructuras — **DONE**

| Campo | Valor | Estado |
|-------|-------|--------|
| Paper | Qiu et al., *Bioorg. Chem.* **133**, 106377 (2023) | PUBLICADO |
| DOI / PMID | https://doi.org/10.1016/j.bioorg.2023.106377 · PMID 36731294 | PUBLICADO |
| Preprint SSRN | abstract_id=4276225 (2022-11) — full PDF **BLOCKED** (403/Cloudflare) | PUBLICADO abstract |
| Autores | Yanli Qiu et al.; corr. Yang / Zhao / Tao (ShanghaiTech / SHUTCM) | PUBLICADO |
| Chemotype 14 | N1=2-morpholinophenyl; C3=CONH-1-Ad; C4=Me; C5=Ph | PUBLICADO + Scheme S1 OCR |
| SMILES / InChIKey | `QQXQVTJJXRACOB-UHFFFAOYSA-N` | REPO 0D YES |
| PubChem CID | **CONFIRMED NOT FOUND** (PUGREST.NotFound) | NOT FOUND |
| ChEMBL | `total_count: 0` exact InChIKey | NOT FOUND |
| BindingDB | SMILES search endpoints 404 / no hit | NOT FOUND |
| Vecinos 15 / 20 / 24 | meta-morph; o-Me-piperazine; CH₂-Ad | Scheme S1 OCR YES |

### 1.2 Binding / funcional — **PARTIAL / BLOCKED numbers**

| Endpoint | Hallazgo | Estado |
|----------|----------|--------|
| Ki / IC₅₀ / EC₅₀ tabulados (main PDF) | Tablas t1–t4 = stubs 189 B; Unpaywall closed | **BLOCKED** |
| Ki / IC₅₀ / EC₅₀ en SI texto | 0 hits en mmc1 deep extract | **NOT FOUND** (ausentes en SI prose) |
| EC₅₀ figure-estimated desde OCR HTRF | Ejes log[Cpd] sin anotaciones nM | **NOT FOUND** (no inventar) |
| Funcional CB2 ago / CB1 ant de **14** | SI Fig. S5 cAMP/HTRF; controles CP55940 / rimonabant; 3×triplicado | PUBLICADO cualitativo |
| SAR neighbors en paneles | 15/20/24 aparecen en Fig. S11–S13 OCR (curvas) | PUBLICADO cualitativo |
| MM-GBSA (compute) | 14 CB2(6PT0) **−95.436**; 15 CB1 **−63.823** / CB2(5ZTY) **−104.222**; 20 CB1 **−77.848**; 24 CB1 **−57.177** | PUBLICADO compute ≠ wet |
| Cellular fibrosis / in vivo Qiu-14 | — | **NOT FOUND** |

**Assay conditions (from SI captions only):** cAMP assay; HTRF ratio 665/620 in SI figures; mean ± SEM; three independent experiments in triplicate. Radioligand Ki method details remain in **BLOCKED** main text.

### 1.3 Patentes / citas / follow-up — **DONE** (esta pasada)

| Tema | Hallazgo |
|------|----------|
| Patente composición Qiu-14 | **NOT FOUND** (Google Patents / author name search) — ≠ inexistencia CN |
| Citing post-2023 | **1:** Chen et al. *Bioorg. Chem.* 2025 DOI https://doi.org/10.1016/j.bioorg.2025.108770 — péptido CB2 óseo; **cite only** |
| Author follow-up | Qiu/Zhao/Tao et al. 2026 *Eur. J. Med. Chem.* DOI https://doi.org/10.1016/j.ejmech.2026.118883 — **Azo23** photoswitch (CB1 ago / CB2 ant cis); **≠** compounds 14/15/20/24 |
| Réplica independiente de Qiu-14 | **NOT FOUND** |

### 1.4 ¿H1-a reproducción o incertidumbre? — **DONE**

| Pregunta | Respuesta |
|----------|-----------|
| ¿Evidencia publicada CB2-ago / CB1-ant para **14**? | **Sí** (un lab; cAMP/HTRF; SI) |
| ¿Números en DBs / open text? | **No** — exhaustive confirms |
| ¿Réplica independiente? | **No** |
| ¿H1-a “descubrir signo” aporta conocimiento nuevo? | **Poco** — reproducción cualitativa |
| ¿Ancla panel janusforge? | Solo si PI exige Yin-Yang monomolecular; si no → controles comerciales |

**Veredicto §1:** retrieval exhaustivo **cerró** la duda de “¿acaso los números están abiertos en SI/DBs?” → **No están.** La duda restante es solo **PDF institucional**.

---

## 2. Paisaje de quimiotipos — **DONE**

| Familia | Ejemplos | Relación Janus | Saturación |
|---------|----------|----------------|------------|
| Pirazol Yin-Yang Qiu | 14/15/20/24 | Switch o-morpholine | Una campaña 2023; 1 cita; follow-up photoswitch distinto |
| Pirazol CB1 clásico | Rimonabant / AM6538 | Template Qiu | Muy saturado |
| Pirazol CB2 ant | AM10257 | Control Qiu | Cristal CB2 |
| Pirrol Janus | URB447 | Precedente conceptual D2 | Pequeña clase |
| Indol / oxazinoindol | GW405833 | Janus-like | Conocida |
| Cannabilactona | AM1710 | Janus-like | Conocida |
| Markush fibrosis | WO2022026478 | Claims mixtos + fibrosis | Presión IP |
| Photoswitch opposite CB | Azo23 (2026) | Concepto opposite-control | Nueva línea autores Qiu/Tao |
| Fitocannabinoide | THCV | Janus imperfecto | Prior art |

**Hueco:** NCE + datos fibrosis — no “inventar Yin-Yang”.

---

## 3. Precedentes compute → experimento — **DONE**

| Estudio | Método | Ensayo | Tasa / límite |
|---------|--------|--------|---------------|
| Ge 2023 | LRIP + docking + MD | Ca²⁺ CHO | ~62–70% success function |
| Ji/Wang 2020 | Docking + MD + MM-PBSA | Correlación literatura | R² ~0.60 |
| Qiu 2023 | Docking + MD + MM-GBSA | cAMP serie | Función ensayada; MM-GBSA correlación aproximada (Fig. S14) |
| Dhopeshwarkar 2017 | Experimental | Binding + función | Gold-standard Janus relectura |

**Límite:** ~30–40% error funcional tipico → **MD no reemplaza H1-a**.

---

## 4. MD / HPC — **DONE**

Qiu ya hizo MD ~100 ns (H-bond Ser occupancy). Ge LRIP **NOT READY** en repo; 0N **BLOCKED**. Más simulación **no** cierra potencia ni fibrosis → **NO JUSTIFICADO** ahora.

---

## 5. Tabla de ligandos — **DONE**

Ver CSV. Regla: potencias Qiu = **NOT FOUND**; MM-GBSA etiquetado como compute; Azo23 añadido.

---

## 6. Patentes (inventario; **no FTO**) — **DONE**

| Familia / doc | Hallazgo verificado esta pasada | Links |
|---------------|----------------------------------|-------|
| **WO2022026478A1** | Title: novel compounds for fibrosis/inflammatory conditions; inventors Makriyannis / Vemuri; scaffolds incl. **pyrazoles**; language for **CB1 ant / CB2 ago mixed properties**; fibrosis liver/**lung**/kidney/prostate; morpholine/thiomorpholine/adamantyl in definition language | https://patents.google.com/patent/WO2022026478A1 |
| **US20230234928A1** | Counterpart; Compound 1: CB1 Ki **1 nM**, CB2 Ki **>1000 nM**; CB1 Kis “0.1 nM to <100 nM” range language; lung fibrosis / NASH figures; COVID ARDS claim language | https://patents.google.com/patent/US20230234928A1 |
| Sanofi US5624941 | Rimonabant-class diarylpyrazole | https://patents.google.com/patent/US5624941 |
| Makriyannis earlier pyrazole families | US7393842, US7119108, US8084467, US8410097 (UConn) — CB pyrazole space | FreePatentsOnline / Google Patents |
| Pyrazole + adamantyl carboxamide + morpholinophenyl CB overlapping Qiu-14 | **NOT FOUND** as dedicated composition matching Qiu-14 | searches this pass |
| Patent citing Qiu 2023 / composition Qiu-14 | **NOT FOUND** | this pass |
| Espacenet family walk | **BLOCKED** (HTTP 403 scraper) | — |

**Separación:** ciencia Qiu ≠ patente Makriyannis ≠ FTO. Counsel para claim chart.

---

## 7. Fibrosis & CB2 — **DONE**

Escalera receptor → ligando → combo → clínico **soporta hipótesis de programa**; **ningún** nivel valida Qiu-14 en fibrosis (**NOT FOUND**).

---

## 8. Skip-map (0D…H2) — **DONE**

| Ítem | ¿Más inversión? |
|------|-----------------|
| 0D–0J compute chain | **NO GASTAR** |
| 0N MD/LRIP | **NO JUSTIFICADO** |
| H1-a discovery signo Qiu-14 | **SKIP** |
| H1-a ancla Yin-Yang operativa | **CONDICIONAL** (PI) |
| H2 D2_20/06 | **NO** ahora |
| TBD-18 institutional PDF | **BARATO Y ÚTIL** (única vía restante para números) |
| Controles comerciales CB2/CB1 | **BARATO Y ÚTIL** si se abre panel |

---

## 9. Evidencia post-Qiu 2023 — **DONE**

| Fuente | Citing / follow-up | ¿Usa 14/15/20/24? |
|--------|--------------------|-------------------|
| OpenAlex `cites:W4317627134` | Chen et al. 2025 DOI 10.1016/j.bioorg.2025.108770 | **No** (péptido) |
| EuropePMC citations PMID 36731294 | mismo Chen 2025 | **No** |
| Semantic Scholar | citations empty / count 0 (lag) | — |
| Crossref filter `references:` | API 400 this pass | — |
| Author works Tao/Zhao 2023–2026 | **Azo23** DOI 10.1016/j.ejmech.2026.118883 | **No** (azo photoswitch) |

**Explícito:** campo **no** adoptó Qiu-14 experimentalmente; follow-up de autores pivota a photopharmacology, no a SAR del 14.

---

## 10. DECISIÓN 0P (re-answered con evidencia nueva)

### Tabla de clasificación

| Paso / gasto | Código | Justificación |
|--------------|--------|---------------|
| 0D–0J | 🟢 NO GASTAR | Hecho |
| Recuperar PDF institucional Qiu (TBD-18) | 🟢 BARATO Y ÚTIL | **Única** vía restante para Ki/EC₅₀ |
| Controles comerciales | 🟢 BARATO Y ÚTIL | Sustituyen discovery del 14 |
| H1-a discovery CB2-ago Qiu-14 | 🔴 NO JUSTIFICADO | Signo PUBLICADO; números no cambian eso |
| H1-a ancla Yin-Yang CRO | 🟡 CONDICIONAL | Sin números, ancla cuantitativa débil; solo si PI insiste |
| H1-b / H2 / 0N | 🔴 / 🟡 | Sin cambio: no primero |
| Fibrosis Qiu-14 / FTO formal | 🟠 INSUFICIENTE | Counsel / decisión de indicación |

### Cinco preguntas (NEW evidence)

1. **¿Qué sabemos de verdad de Qiu-14?**  
   Identidad 2D YES; Yin-Yang **cualitativo** cAMP/HTRF YES (SI Fig. S5); MM-GBSA compute YES; **Ki/IC₅₀/EC₅₀ STILL NOT FOUND** tras exhaustive public retrieval; sin réplica; sin fibrosis; sin CID/ChEMBL.

2. **¿Qué hay de CB2/CB1 para este chemotipo?**  
   Solo la campaña Qiu 2023 (+ curvas SI de vecinos). DBs públicas vacías. Follow-up 2026 de autores es **otro** chemotipo (Azo23).

3. **¿Qué demostraron otros?**  
   Janus refs (URB447/GW/AM1710); fibrosis CB2 (JWH133 etc.); combo AM6545+AM1241; Ge compute→wet ~62–70%. **Nadie** wet-reprodujo Qiu-14 ni lo usó en fibrosis. Una sola cita (péptido).

4. **¿Qué trabajo se elimina por ya publicado?**  
   Redescubrir signo CB2-ago/CB1-ant; rehacer docking/MD S173/S285; más QC poses; 0N como sustituto de ensayo.

5. **¿Menor coste que más reduce incertidumbre?**  
   **(1)** Acceso institucional al PDF Qiu + extracto literal de tablas. **(2)** Si el norte es el *panel*, no el 14: ensayo con agonista CB2 + antagonista CB1 **comerciales**. **(3)** H1-a Qiu-14 solo si ancla Yin-Yang monomolecular es requisito de programa. **No** docking. **No** 0N primero.

### Recomendación H1-a (¿cambia con números?)

| Rol | Recomendación | ¿Cambió tras exhaustivo? |
|-----|---------------|--------------------------|
| Discovery “¿activa CB2?” | **SKIP** | **No** — números siguen ausentes; signo cualitativo intacto |
| Ancla operativa Janus | **CONDICIONAL / prefer SKIP** si no hay exigencia PI | **Ligeramente más fuerte el skip ancla** — sin potencias no hay guía de dosis/concentración CRO |
| Next | Institutional PDF (TBD-18) o panel con refs comerciales | PDF sigue siendo el único documental pendiente |

**Preferencia 0P:** SKIP H1-a discovery; **no** 0N; **no** H2 aún; sí PDF institucional si se quiere calibrar; wet barato = controles comerciales.

---

## Fuentes ancla

1. Qiu 2023 — DOI 10.1016/j.bioorg.2023.106377 · SI mmc1 · ACCESS_LOG  
2. Chen 2025 citing — DOI 10.1016/j.bioorg.2025.108770  
3. Qiu/Tao 2026 Azo23 — DOI 10.1016/j.ejmech.2026.118883  
4. WO2022026478A1 / US20230234928A1 (Google Patents extracts)  
5. Ge 2023 — DOI 10.1021/acschemneuro.3c00580  
6. URB447 / Dhopeshwarkar / Cinar / JWH133 fibrosis (ver first-pass sources)  
7. Repo 0D–0N, 0IP, fibrosis docs  

---

## Cierre

```text
0P EXHAUSTIVE PUBLIC/LOCAL RETRIEVAL = COMPLETE
MAIN PDF TABLES = STILL BLOCKED
NUMERIC Ki/IC50/EC50 QIU-14/15/20/24 = NOT FOUND (CONFIRMED)
H1-a DISCOVERY = SKIP (UNCHANGED)
H1-a ANCHOR = CONDITIONAL / PREFER SKIP WITHOUT POTENCIES
0N / MORE DOCKING = DO NOT FUND
NEXT CHEAPEST DOCUMENTARY = INSTITUTIONAL PDF (TBD-18)
```
