# 0Q.2F — Auditoría documental regioisómeros Qiu-14 / 15 / 16

**Fecha:** 2026-08-15  
**Alcance:** SOLO SI local `data/papers/mmc1.docx` y artefactos derivados del mismo SI.  
**Prohibido en este entregable:** docking/MD/MM-GBSA como evidencia funcional; potencias inventadas; conocimiento externo; curva→fenotipo si el panel no es inequívoco.

---

## Método / fuentes usadas

| Archivo | Uso |
|---------|-----|
| `data/papers/mmc1.docx` | Fuente primaria; mapeo caption↔embed (`image5.png`→S5 … `image13.emf`→S13) |
| `data/papers/mmc1_document.txt` | Texto/captions + Tables S1/S2 |
| `data/papers/mmc1_extract.txt` | Cruz-chequeo de captions |
| `data/papers/qiu_2023_bioorg/mmc1_fulltext_deep.txt` | Cruz-chequeo de captions / tablas |
| `data/papers/si_media/image5.png` | Figura S5 |
| `data/papers/si_media/image6.png` | Figura S6 |
| `data/papers/si_media/image11.png` (+ `.emf` en docx) | Figura S11 |
| `data/papers/si_media/image12.png` (+ `.emf`) | Figura S12 |
| `data/papers/si_media/image13.png` (+ `.emf`) | Figura S13 |
| `data/papers/image11_ocr.txt` | Etiquetas de paneles S11 |
| `data/papers/image12_ocr.txt` | Etiquetas de paneles S12 |
| `data/papers/image13_ocr.txt` | Etiquetas de paneles S13 |
| `data/papers/si_media/image15.png` + `image15_ocr.txt` / `image15_hq_ocr.txt` | Scheme S1 (identidades o/m/p) |
| `data/papers/image3_ocr.txt`, `image4_ocr.txt` | Inspeccionados; corresponden a energías conformacionales (S3/S4), no a 14/15/16 funcionales |

**No usados como evidencia:** texto principal del paper, PubChem/ChEMBL, conocimiento externo, re-interpretación de forma de curva sin etiqueta inequívoca.

---

## 1. Localización exacta en mmc1

| Ítem | ¿Encontrado? | Ubicación documental |
|------|--------------|----------------------|
| **Figure S5 — compound 14** | **SÍ** | TOC `mmc1_document.txt` L12–15; caption L60; embed `media/image5.png` inmediatamente antes del caption en `document.xml`; archivo local `si_media/image5.png` |
| **Figure S6 — 14/15/16** | **SÍ** | TOC L15–17; caption L63; embed `media/image6.png`; local `si_media/image6.png` |
| **Figure S11 — CB1 antagonist, all compounds** | **SÍ** | TOC L26–27; caption L76; embed `media/image11.emf`; local `si_media/image11.png` + `image11_ocr.txt` |
| **Figure S12 — CB2 antagonist, all compounds** | **SÍ** | TOC L28–29; caption L78; embed `media/image12.emf`; local `si_media/image12.png` + `image12_ocr.txt` |
| **Figure S13 — CB2 agonist, all compounds** | **SÍ** | TOC L30–31; caption L80; embed `media/image13.emf`; local `si_media/image13.png` + `image13_ocr.txt` |
| **Table S1 — MM-GBSA CB1** | **SÍ** | Caption L83–84 (`Table S1. MM-GBSA computation for tested compounds to CB1 (PDB: 5TGZ)`); filas L95–234 |
| **Table S2 — MM-GBSA CB2** | **SÍ** | Bloques CB2 `(5ZTY)` / `(6PT0)` L248–359; caption literal L360 (`Table S2. MM-GBSA computation for tested compounds to CB2`) |

### Captions literales (extracto)

**Fig. S5** (`mmc1_document.txt` L60):  
> Pharmacological evaluation of the compound 14 as agonist for CB2 (A) and as antagonist for CB1 (B) as determined by the cAMP assay. CP55940 and Rimonabant were served as controls for CB2 agonist and CB1 antagonist, respectively. Data are presented as mean ± SEM of three independent experiments performed in triplicate.

**Fig. S6** (L63):  
> The docking studies of the ortho/meta/para-substituents of morpholine (compound 14, 15, 16) within inactiv CB1 (PDB: 5TGZ). the ortho-substituents (14), meta-substituents (15) and para-substituents (16) were colored in white, cyan and pink, respectively. The meta/para-substituents may be at the inappropriate positions that resulted in collisions with residues at pockets, as showed in red dashed.

**Fig. S11–S13** (L76–80): ensayos cAMP “all compound” con controles Rimonabant / AM10257 / CP55940 respectivamente.

**Scheme S1** (OCR `image15_hq_ocr.txt` L74–76):  
> `14: R1=Morpholinyl, R3=1-adamantyl, ortho`  
> `15: R1=Morpholinyl, R3=1-adamantyl, meta`  
> `16: R1=Morpholinyl, R3=1-adamantyl, para`

---

## 2. Matriz experimental — compuestos 14, 15, 16

Criterio de celda: **REPORTED** / **NOT REPORTED** / **UNCERTAIN** únicamente.  
No se lee fenotipo activo/inactivo desde la forma de la curva si la etiqueta del panel no es inequívoca en OCR + caption.

| Compuesto | Posición morfolina | CB1 antagonismo experimental | CB2 antagonismo experimental | CB2 agonismo experimental | Potencia cuantitativa reportada | Tipo de dato |
|-----------|--------------------|------------------------------|------------------------------|---------------------------|---------------------------------|--------------|
| **14** | **ortho** (REPORTED; Fig. S6 + Scheme S1) | **REPORTED** (Fig. S5 panel B caption: “antagonist for CB1”) | **NOT REPORTED** (S5 no es ese ensayo; OCR S12 sin `Cpd 14`) | **REPORTED** (Fig. S5 panel A caption: “agonist for CB2”) | **NOT REPORTED** | Experimental cualitativo (caption S5 + curvas cAMP); sin IC50/EC50/Emax tabulados en SI |
| **15** | **meta** (REPORTED; Fig. S6 + Scheme S1) | **REPORTED** (panel etiquetado `Cpd 15` en OCR Fig. S11) | **REPORTED** (panel etiquetado `Cpd 15` en OCR Fig. S12) | **NOT REPORTED** (OCR Fig. S13 sin `Cpd 15`) | **NOT REPORTED** | Experimental: presencia de curva HTRF en S11/S12; **fenotipo activo/inactivo = no afirmado** (sin número ni caption por compuesto) |
| **16** | **para** (REPORTED; Fig. S6 + Scheme S1) | **REPORTED** (panel `Cpd 16` OCR Fig. S11) | **REPORTED** (panel `Cpd 16` OCR Fig. S12) | **REPORTED** (panel `Cpd 16` OCR Fig. S13) | **NOT REPORTED** | Idem: curvas presentes; fenotipo no cuantificado ni captionado por compuesto |

### Notas de identificación de paneles (regla crítica)

- En OCR de Fig. S11 la secuencia de etiquetas pasa de `Cpd 13` → `Cpd 15` → `Cpd 16` (**sin `Cpd 14`**). Fig. S12: `Cpd 13` → `Cpd 15` → `Cpd 16` (**sin `Cpd 14`**). Fig. S13: aparece `Cpd 16`; **no** `Cpd 14` ni `Cpd 15`.
- Por tanto: **no se asume** que 14 esté en S11–S13; su evidencia funcional SI se ancla en **Fig. S5** (caption inequívoco).
- Si se necesitara leer el desenlace (activo vs plano) de 15/16 en S11–S13, haría falta **mayor resolución / paneles recortados con etiqueta legible al 100%**; con el OCR actual **no** se declara pérdida o conservación de fenotipo.

CSV: `results/reports/qiu_0q2f_regioisomer_14_15_16_matrix.csv`

---

## 3. Extracción de números (SI texto)

Búsqueda en `mmc1_document.txt` / `mmc1_extract.txt` / `mmc1_fulltext_deep.txt` de IC50, EC50, Emax, nM, µM, Ki, valores cAMP tabulados: **ningún número farmacológico explícito** para 14/15/16.

| Valor | Unidad | Ensayo | Compuesto | Ubicación |
|-------|--------|--------|-----------|-----------|
| — | — | — | 14 / 15 / 16 | **NOT REPORTED** en texto SI |

Únicos números tabulados asociados a estos IDs en SI = **MM-GBSA** (cómputo; §4), no potencias.

Fig. S5 indica “mean ± SEM of three independent experiments performed in triplicate” pero **sin** EC50/IC50/Emax numéricos en el caption.

---

## 4. Experimental vs computacional

| Compuesto | CB1 experimental | CB2 experimental | MM-GBSA CB1 (Table S1, 5TGZ) | MM-GBSA CB2 | Docking | Fuente |
|-----------|------------------|------------------|-----------------------------|-------------|---------|--------|
| **14** | Fig. S5B (CB1 ant, caption) | Fig. S5A (CB2 ago, caption); CB2 ant **NOT REPORTED** | **NOT REPORTED** (ID 14 ausente en filas S1) | **REPORTED** dG Bind **−95.436** en bloque CB2 **(6PT0)** (`mmc1_document.txt` L339–348) | Fig. S6 (14 = white / ortho) | S5 experimental; S6/Tablas cómputo |
| **15** | Panel `Cpd 15` Fig. S11 | Paneles `Cpd 15` Fig. S12; CB2 ago **NOT REPORTED** en S13 OCR | **REPORTED** dG Bind **−63.823** (`mmc1_document.txt` L145–154) | **REPORTED** dG Bind **−104.222** en bloque CB2 **(5ZTY)** (L316–325); **ausente** en (6PT0) | Fig. S6 (15 = cyan / meta) | S11/S12 experimental presencia; S6/Tablas cómputo |
| **16** | Panel `Cpd 16` Fig. S11 | Paneles `Cpd 16` Fig. S12 y S13 | **NOT REPORTED** (ID 16 ausente en S1) | **NOT REPORTED** (ID 16 ausente en bloques S2) | Fig. S6 (16 = pink / para) | S11–S13 experimental presencia; S6 docking |

**Regla aplicada:** MM-GBSA y docking **no** cuentan como evidencia de agonismo, antagonismo ni Janus.

Fig. S6 caption (cómputo) afirma que meta/para “may be at the inappropriate positions that resulted in collisions…” — narrativa de docking, **no** resultado experimental.

---

## 5. Preguntas SAR (solo YES / NO / PARTIAL / NOT DETERMINABLE)

### A. ¿Se compararon experimentalmente 14, 15 y 16 en CB1 y CB2 bajo condiciones comparables?

**PARTIAL**  
S11–S13 presentan el mismo formato cAMP/HTRF “all compound” con el mismo tipo de control por figura; OCR confirma paneles de **15** y **16** en S11/S12 y de **16** en S13. El compuesto **14** está documentado en **Fig. S5** (CB1 ant + CB2 ago) pero **no** aparece como `Cpd 14` en OCR de S11–S13; **15** no aparece en OCR de S13. No hay tabla farmacológica única que alinee los tres bajo los tres ensayos.

### B. ¿Hay evidencia experimental de que 14 es CB1-antagonista + CB2-agonista?

**YES**  
Caption literal de Fig. S5: compound 14 “as agonist for CB2 (A) and as antagonist for CB1 (B)” por ensayo cAMP, con controles CP55940 y Rimonabant (`mmc1_document.txt` L60; `si_media/image5.png`).

### C. ¿Hay evidencia experimental de que 15 pierde uno de esos dos fenotipos?

**NOT DETERMINABLE**  
Hay paneles etiquetados `Cpd 15` en Fig. S11 (CB1 ant) y Fig. S12 (CB2 ant), pero el SI **no** tabula ni captiona el desenlace (activo/inactivo/pérdida). OCR Fig. S13 **no** muestra `Cpd 15` (CB2 ago). Inferir “pérdida” desde forma de curva o desde docking Fig. S6 está **prohibido** aquí.

### D. ¿Hay evidencia experimental de que 16 pierde uno de esos dos fenotipos?

**NOT DETERMINABLE**  
Misma lógica: paneles `Cpd 16` en S11–S13 confirman que se midió, no el resultado cualitativo/cuantitativo. Sin números ni caption por compuesto que declare pérdida de CB1-ant o CB2-ago.

### E. ¿Se puede atribuir experimentalmente el cambio a la posición ortho/meta/para?

**NOT DETERMINABLE**  
La asignación o/m/p **sí** está en el SI (Fig. S6 + Scheme S1 OCR). La **causalidad experimental** del cambio de fenotipo por posición **no** está demostrada en tablas/captions: la única explicación explícita de “meta/para inappropriate / collisions” es el **caption de docking** Fig. S6.

---

## 6. Veredicto final

### 🔴 INSUFFICIENT

**Motivo (único, experimental):** el SI documenta de forma explícita el Yin-Yang cualitativo de **14** (Fig. S5), y las identidades regioisoméricas **14/15/16 = o/m/p** (Fig. S6 + Scheme S1), pero **no** aporta potencias ni una comparación experimental captionada/tabulada que demuestre que **15** o **16** pierden CB1-antagonismo y/o CB2-agonismo. El relato de pérdida por posición en Fig. S6 es **computacional** y no eleva la clasificación.

---

## 7. Limitaciones explícitas

1. Sin IC50/EC50/Emax/Emax%/nM en texto SI para 14/15/16.  
2. OCR S11–S13: ausencia de etiqueta `Cpd 14`; no se rellena con la Fig. S5.  
3. Desenlace de curvas 15/16 = **UNCERTAIN** sin panel de alta resolución inequívoco.  
4. Tables S1/S2 incompletas respecto a {14,15,16}×{CB1,CB2}: solo se copian valores que aparecen.  
5. No se usó el PDF principal del artículo ni fuentes externas.
