# Quimiotipos ricos en varinas (THCV / THCVA)

> Literatura breve + hipótesis de diseño THCV-like.  
> Castellano; tono crítico. Sin docking nuevo.  
> Fecha: 2026-08-06.  
> Complementa: [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) · hallazgo proxy: [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md).

---

## 1. Por qué este documento

La retrospectiva Vina del panel quimioma mostró que **Δ9-THCV apenas se separa de Δ9-THC** en afinidad/pose dual (gap dual THCV−THC ≈ **−0.20 kcal/mol**), mientras que el comparador URB447 sí empuja la separación grupal. Eso obliga a dos movimientos en paralelo:

1. Entender **de dónde salen las varinas en la planta** (biosíntesis C3, geografía, ratios reales vs marketing).
2. Definir **hipótesis químicas THCV-like** que puedan superar ese gap de proxy *y/o* limpiar el flip CB1 — sin pretender que Vina mida agonismo vs antagonismo.

---

## 2. Biosíntesis natural de varinas (C3 vs C5)

### 2.1. Bifurcación temprana: starter unit

Los fitocannabinoides “clásicos” (THC, CBD, CBG…) llevan cadena **pentílica (C5)**. Las **varinas** (THCV, CBDV, CBGV…) son homólogos **propílicos (C3)**. La diferencia no nace en THCAS/CBDAS: nace **antes**, en el ácido alquilresorcinólico:

| Ruta | Starter (ácido graso → CoA) | Ácido aromático | Precursor geranilado | Productos ácidos típicos |
|------|----------------------------|-----------------|----------------------|--------------------------|
| **Pentílica (C5)** | Hexanoil-CoA (C6) | Ácido olivetólico (OLA) | **CBGA** | THCA, CBDA, CBCA → THC/CBD/CBC |
| **Propílica (C3)** | Butanoil-CoA (C4) | Ácido divarinólico (DVA) | **CBGVA** | THCVA, CBDVA, CBCVA → THCV/CBDV/CBCV |

GPP (vía MEP plastidial) prenila el ácido aromático vía geraniltransferasa (GOT / CBGAS). En la rama varin, el producto es **cannabigerovarinic acid (CBGVA)**, no CBGA ([Walsh et al., 2021](#refs); [Welling et al., 2019](#refs)).

### 2.2. Oxidociclasas: mismas enzimas, sustrato distinto

THCAS, CBDAS y CBCAS actúan sobre **CBGVA** de forma análoga a CBGA:

```
butanoil-CoA → … → divarinolic acid + GPP → CBGVA
                                              ↓ THCAS
                                           THCVA  ──(calor/luz)──→  THCV
                                              ↓ CBDAS
                                           CBDVA  ──decbox──→  CBDV
```

En la planta, los cannabinoides se acumulan como **ácidos**; los neutros (THCV, THC) aparecen por **descarboxilación** no enzimática (secado, calor, UV). Por tanto, en flor fresca el marcador dominante de un quimiotipo “THCV alto” suele ser **THCVA**, no THCV neutro.

### 2.3. Genética del ratio C3:C5 (no es un solo gen “THCV”)

- El locus **B** (*B<sub>T</sub>* / *B<sub>D</sub>*) decide THCA vs CBDA sobre el precursor geranilado; **no** decide la longitud de cadena ([de Meijer et al., 2003](#refs)).
- El ratio **propílico/pentílico (PC3)** es **oligogénico/poligénico**: de Meijer & Hammond (2016) proponen loci *A¹…Aⁿ* aditivos; líneas multi-cruzamiento llegaron a PC3 hasta ~**96 %** de la fracción cannabinoide en material de mejora ([de Meijer & Hammond, 2016](#refs)).
- Welling et al. (2019) confirman herencia compleja de la cadena alquílica y el papel del starter C3 ([Welling et al., 2019](#refs)).
- Hipótesis moleculares recientes (p. ej. variantes de BKR, paralog ALT4) apuntan a la disponibilidad de butanoil-CoA / truncado de elongación; la genética aún no es un interruptor único ([trabajo transcriptómico reciente sobre segregación C3](#refs)).

**Lectura para janusforge:** un “quimiotipo varin” es un **sesgo de starter unit**, no una planta que “elige THCV en vez de THC”. Mientras haya flujo C5, coexistirán THCA/THC.

---

## 3. Geografía y landraces asociadas a THCV alto

### 3.1. Evidencia quimiotaxómica (sólida a nivel regional)

Hillig & Mahlberg (2004) analizaron accesiones y encontraron niveles elevados aparentes de **CBDV/THCV** casi solo en material tipo *C. indica* (sensu Hillig) de:

- **Asia:** Afganistán, China, India, Nepal, Tailandia  
- **África:** Gambia, Lesotho, Nigeria, **Sudáfrica**, Swazilandia (Eswatini)

En ese estudio, plantas con (CBDV+THCV)/i.s. > 0.30 eran **todas** de esas regiones; en algunos individuos **THCV podía superar a THC** ([Hillig & Mahlberg, 2004](#refs)). Baker et al. (1980) y Boucher et al. (1974) ya habían señalado productos africanos con THCV/THCVA notables.

### 3.2. Sudáfrica y nombres comerciales (matiz fuerte)

Una revisión reciente sitúa perfiles citados para landraces/cultivares sudafricanos (rangos **reportados**, no COA propios de janusforge) ([Makhaye et al., 2024 — *Plants*](#refs)):

| Nombre (comercial / landrace) | Δ9-THC (aprox.) | THCV (aprox.) | Nota crítica |
|-------------------------------|-----------------|---------------|--------------|
| **Durban Poison** | 15–25 % | **0.2–1.8 %** | THC sigue dominando; THCV es minor enriquecido, no “cepa THCV” |
| **Eswatini / Swazi Gold** (citado) | 18–27 % | **1–3 %** | Mejor señal THCV relativa en la revisión; verificar fuente primaria |
| Otras africanas (Mpondo Gold, KwaZulu, etc.) | alto THC | variable | Narrativa regional ≠ ratio analítico fijo |

### 3.3. “Durban Poison = alto THCV”: marketing vs datos

| Claim habitual en blogs/retail | Lectura crítica |
|-------------------------------|-----------------|
| “Durban Poison es la cepa de THCV” | **Parcialmente engañoso.** Hay asociación histórica sudafricana y a veces THCV medible, pero en cifras revisadas THCV queda en **décimas–pocos %** frente a THC de dos dígitos. |
| “3–5 % THCV típico” (algunos blogs) | **No aceptar sin COA.** Choca con rangos más bajos de revisiones; lotes comerciales con nombre “Durban” pueden ser híbridos sin THCV detectable. |
| Landrace africana = siempre C3 alto | **Falso.** Hillig muestra variación *dentro* de accesiones africanas; el rasgo es más frecuente, no universal. |

**Regla:** citar **regiones y accesiones analíticas** (Baker, Hillig, de Meijer), no marcas de dispensario, como evidencia de quimiotipo.

### 3.4. Rangos de proporción THCV:THC (y ácidos)

No hay un ratio “canónico”. Orden de magnitud útil:

| Contexto | PC3 / THCV:THC (orden) | Fuente / nota |
|----------|------------------------|---------------|
| Quimiotipo C5 silvestre típico | PC3 bajo (≪10 % de fracción) | Condición “wild-type” ([de Meijer & Hammond, 2016](#refs)) |
| Accesiones africanas/asiáticas “elevadas” | THCV a veces **> THC** en individuos; a menudo THCV **menor** | Hillig 2004; sin calibración absoluta de THCV en ese GC |
| Mejora dirigida (inbreeding + multi-cross) | PC3 hasta **~96 %** | de Meijer & Hammond 2016 — material de breeding, no street flower |
| “Durban Poison” citas modernas | THCV ~**0.2–1.8 %** vs THC ~**15–25 %** → ratio THCV:THC ≈ **1:10 a 1:100** | Revisión SA 2024; amplio y lote-dependiente |
| Flor fresca vs descarboxilada | Dominan **THCVA/THCA**; neutros tras calor | Biosíntesis estándar |

**Conclusión:** el rango es **amplio** (de traza a casi-puro C3 en líneas de mejora). Afirmar un ratio fijo para “África” o “Durban” es incorrecto.

---

## 4. Implicación para janusforge

1. **La planta co-produce THC (y THCA).** Incluso en quimiotipos “ricos en varinas”, el pathway C5 suele seguir activo → **contaminación agonista CB1** en extractos botánicos y **carga legal** (THC controlado).
2. **THCV natural no es un API limpio** solo por venir de una landrace africana: hay que purificar o sintetizar el análogo; el origen geográfico no limpia el flip ni el gap de docking.
3. El hallazgo retrospectivo (THCV ≈ THC en proxy Vina) refuerza: **el valor de la planta es PoC + scaffold**, no el producto final. Los **análogos limpios** (sin THC, con SAR orientado a CB1-ant/CB2-ago) son la vía operativa.
4. THCVA (ácido) ya aparece como `interesting` en el quimioma: polaridad distinta; en el panel Vina su dual (−9.18) tampoco separó de forma espectacular — útil como hipótesis de periferia, no como hit.

---

## 5. Hipótesis de optimización THCV-like (H1–H5)

Anclaje explícito al reporte: en el panel retrospectivo, **THCV dual = −9.454** vs **THC dual = −9.252** (Δ ≈ **−0.20 kcal/mol**); URB447 dual = **−10.623**. El natural C3 **no** aporta separación scaffold-scaffold fiable en el proxy. Las hipótesis buscan (i) **cerrar o superar ese gap** frente a anti-semillas en el *mismo* panel, y/o (ii) **limpiar farmacología** (flip CB1, periferia) aunque el score Vina sea solo un filtro grueso.

### H1 — Extensión controlada de cadena C3 → C4 (evitar C5–C7)

| | |
|--|--|
| **Cambio** | Homólogo **butílico (C4)** del núcleo Δ9-tetrahidrocannabinol / THCV (análogo a CBDB/THCB en espíritu, no saltar a THC C5 ni THCP C7). |
| **Racional** | La cadena lateral es la palanca SAR clásica de eficacia CB1. C3 (THCV) da el PoC Janus imperfecto; C5 (THC) es agonista; C7 (THCP) empeora agonismo. Un C4 podría **ganar contacto hidrofóbico** en el pocket (mejorar proxy vs THC) **sin** el flip completo a agonismo tipo THC — hipótesis a falsificar. |
| **Riesgo** | Deslizar hacia anti-semilla (más agonismo CB1). En Vina, un score “mejor” con farmacología peor = falso positivo (anti-criterio). |
| **Evaluación** | Similitud a THCV (Tanimoto/scaffold); docking dual en el **mismo panel retrospectivo** (debe batir gap THCV–THC); luego binding/función CB1 (antagonismo vs ago residual) y CB2 ago. |

### H2 — Derivados carboxílicos / THCVA-like (polaridad, menor CNS)

| | |
|--|--|
| **Cambio** | Ácido 2-carboxílico estable (THCVA o análogos no descarboxilables fácilmente), ésteres/prodrugs periféricos. |
| **Racional** | Sube TPSA / carga a pH fisiológico → **menor penetración SNC** hipotética; en el panel, THCVA ya mostró CB1 proxy más débil (−7.89) y CB2 razonable (−10.46). Puede **separar por ADME** aunque el dual medio no gane a URB447. |
| **Riesgo** | Descarboxilación regenera THCV (flip); ácidos mal caracterizados funcionalmente; Vina no predice periferia. |
| **Evaluación** | Estabilidad química; docking solo como ocupancia; ensayos de permeabilidad/P-gp; CB1/CB2 funcionales; no declarar éxito solo por score. |

### H3 — Bioisósteros del resorcinol / fenol

| | |
|--|--|
| **Cambio** | Sustitución o enmascaramiento de OH fenólicos (p. ej. heteroarilo, F, O-alquilo selectivo, bioisósteros de H-bond). |
| **Racional** | Los fenoles dirigen H-bonds y metabolitos; modularlos puede **alterar pose/afinidad** (cerrar gap vs THC en proxy) y **eficacia** (menos agonismo CB1 residual) sin alargar la cadena hacia THC. |
| **Riesgo** | Perder CB2 ago; crear metabolitos reactivos; SAR poco predecible in silico. |
| **Evaluación** | Panel docking + filtro de similitud; prioridad a ensayos cAMP/β-arrestin CB1 vs CB2; metabolitos in vitro. |

### H4 — Restricción conformacional / “congelar el flip”

| | |
|--|--|
| **Cambio** | Puentes, saturación/insaturación del anillo pirano/ciclohexeno, o análogos rígidos que limiten poses agonistas a alta ocupación. |
| **Racional** | El defecto de THCV es **bifásico** (ant a baja dosis / ago a alta). Una molécula más rígida podría estabilizar el modo antagonista en CB1 (bolsillo tipo 5TGZ) y mejorar discriminación vs THC en proxy **y** en función. |
| **Riesgo** | Síntesis cara; rigidez que mate CB2; overfitting a una cristalografía. |
| **Evaluación** | Docking en CB1 inactivo vs CB2 activo; MD opcional; ensayo dosis-respuesta CB1 buscando ausencia de ago a alta ocupación. |

### H5 — N-heterociclos / alejamiento controlado del scaffold (inspiración URB447, no copia)

| | |
|--|--|
| **Cambio** | Introducir N-heterociclo o fragmento polar manteniendo el farmacóforo “cannabinoide-like” (no abandonar cannabis-first: es **análogo**, no pivot total a diarylpirazol). |
| **Racional** | URB447 **sí** separó en el panel (dual −10.62). Incorporar rasgos de polaridad/heterociclo *sobre* semilla THCV podría cerrar el gap de afinidad proxy **y** sesgar a periferia, sin adoptar el norte sintético puro. |
| **Riesgo** | Salir del espacio patentable/químico deseado; perder narrativa cannabis-first; polifarmacología nueva. |
| **Evaluación** | Comparar en el mismo CSV de roles; si dual y gaps CB1/CB2 superan claramente THCV−THC **y** no hay dirección anti-semilla en función, priorizar síntesis. |

### Resumen operativo de hipótesis

| ID | Idea en una línea | Qué debe superar |
|----|-------------------|------------------|
| H1 | C4 controlado | Gap proxy THCV–THC **sin** flip a THC |
| H2 | Ácido / prodrug | CNS + legal; no solo score |
| H3 | Bioisóstero resorcinol | Eficacia CB1 limpia ± afinidad |
| H4 | Rigidez / anti-flip | Bifasicidad THCV |
| H5 | Heterociclo polar THCV-like | Separación tipo URB447 sin abandonar semilla |

Detalle breve también en [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) §3.4 (refinado). Criterio de éxito actualizado: [`criterio_exito_janus.md`](criterio_exito_janus.md).

---

## 6. Referencias {#refs}

1. Hillig K.W., Mahlberg P.G. A chemotaxonomic analysis of cannabinoid variation in *Cannabis* (Cannabaceae). *Am J Bot.* 2004;91(6):966–975. https://doi.org/10.3732/ajb.91.6.966
2. de Meijer E.P.M. et al. The inheritance of chemical phenotype in *Cannabis sativa* L. *Genetics.* 2003;163(1):335–346. https://doi.org/10.1093/genetics/163.1.335 · [PMC1462421](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1462421/)
3. de Meijer E.P.M., Hammond K.M. The inheritance of chemical phenotype in *Cannabis sativa* L. (V): regulation of the propyl-/pentyl cannabinoid ratio… *Euphytica.* 2016;210:291–307. https://doi.org/10.1007/s10681-016-1721-3
4. Welling M.T. et al. Complex patterns of cannabinoid alkyl side-chain inheritance in *Cannabis*. *Sci Rep.* 2019;9:11421. https://doi.org/10.1038/s41598-019-47812-2
5. Walsh K.B. et al. Minor cannabinoids: biosynthesis, molecular pharmacology and potential therapeutic uses. *Front Pharmacol.* 2021. https://doi.org/10.3389/fphar.2021.777804 · [PMC8669157](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8669157/)
6. Baker P.B., Gough T.A., Taylor B.J. Illicitly imported Cannabis products: some physical and chemical features indicative of their origin. *Bull Narc.* 1980;32(2):31–40. PMID: [6907024](https://pubmed.ncbi.nlm.nih.gov/6907024/)
7. Boucher F. et al. (y literatura clásica sudafricana THVA/THCA) — ver discusión en UNODC / revisiones; ratios THCA/THVA sensibles a ambiente y generación.
8. Merkus F.W. Cannabivarin and tetrahydrocannabivarin, two new constituents of hashish. *Nature.* 1971. https://doi.org/10.1038/232579a0
9. Makhaye et al. Finally Freed—Cannabis in South Africa: A Review… *Plants.* 2024;13(19):2695. https://doi.org/10.3390/plants13192695 (perfiles citados Durban Poison / Swazi Gold; tratar rangos como secundarios).
10. Pertwee R.G. The diverse CB1 and CB2 receptor pharmacology… Δ9-THCV. *Br J Pharmacol.* 2008. https://doi.org/10.1038/sj.bjp.0707442
11. Retrospectiva janusforge (proxy Vina, no función): [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md)

*Documento vivo: ampliar con COAs propios o Ki/EC50 cuando existan; no sustituir claims de retail por datos analíticos.*
