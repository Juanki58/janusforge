# Quimioma cannábico CB1/CB2 — brújula química de janusforge

> Documento maestro vivo (castellano).  
> Última redacción: 2026-08-06.  
> Complementa la memoria biológica: [`literatura_fibrosis_cb1_cb2.md`](literatura_fibrosis_cb1_cb2.md).

---

## 1. Título y propósito

Este documento fija la **brújula química** del proyecto: un mapa vivo del **quimioma cannábico** (fitocannabinoides naturales y análogos cercanos) evaluado por su perfil en **CB1** y **CB2**, con la fibrosis/FPI como filtro de indicación *después*, no como criterio que justifique farmacología sucia.

**Norte operativo.** Janusforge es *cannabis-first*: la planta aporta el **scaffold** y la **prueba de concepto** del perfil Janus imperfecto (prototipo natural: Δ9-THCV). Se aceptan **análogos cercanos / semi-sintéticos THCV-like** (modulación de cadena alquílica, esterificación, bioisósteros del resorcinol) cuando sirvan para limpiar el flip CB1, mejorar ADME o sesgar a periferia. Los sintéticos Janus (p. ej. URB447) son **comparadores de diseño**, no el norte químico.

**Qué no es este documento.** No es un protocolo de docking, ni un inventario de potencias inventadas, ni un plan de cribado masivo. Es la tabla viva + el razonamiento que decide qué merece seguimiento y qué es control o anti-semilla.

---

## 2. Tres decisiones fijadas (resumen)

| # | Decisión | Contenido operativo |
|---|----------|---------------------|
| 1 | **Semilla amplia** | Fitocannabinoides naturales = template / PoC. Análogos cercanos y semi-sintéticos THCV-like permitidos para limpiar flip CB1, ADME y periferia. La planta no es dogma de pureza natural: es scaffold + prueba de concepto. |
| 2 | **Prioridad absoluta: receptor limpio** | Perfil **CB1 antagonista / CB2 agonista** limpio primero. Fibrosis/FPI = filtro de indicación *después*. Farmacología sucia en CB1 (agonismo residual, flip dosis-dependiente no controlado) = bomba de tiempo aunque “funcione” en un modelo de fibrosis. |
| 3 | **Entregable vivo** | Esta tabla del quimioma + análisis THCV + criterios de fibrosis + reglas de pipeline. Sin código masivo ni docking como entrega inmediata. |

---

## 3. Matriz del Quimioma Cannábico

**Tabla operativa (trackeable):** [`../data/libraries/quimioma_semillas.csv`](../data/libraries/quimioma_semillas.csv)  
Columnas: `name`, `common_name`, `category`, `smiles`, `role`, perfiles CB1/CB2, notas fibrosis, refs, `confidence`, `notes`.  
SMILES curados desde PubChem (CID en `notes`); no inventados. Si faltara confianza en una estructura futura, `smiles` vacío + `confidence=low`.

### 3.1. Cómo leer el `role`

| `role` | Significado operativo |
|--------|------------------------|
| **seed** | PoC / punto de partida de optimización del perfil Janus (hoy: Δ9-THCV imperfecto). |
| **secondary** | Scaffold o región útil, pero no prototipo Janus claro (p. ej. CBDV). |
| **interesting** | Hipótesis abierta o periferia/SAR (ácidos, C4); evidencia incompleta — radar, no hit. |
| **control** | Referencia para contrastar ensayos (polifarmacología, agonismo débil, etc.). |
| **anti_seed** | Perfil incompatible con el norte (agonismo CB1 fuerte / SAR “más THC”); no optimizar hacia aquí. |
| **design_comparator** | Ancla sintética del perfil Janus limpio + periferia (URB447); **no** es el norte cannabis. |

Los perfiles CB1/CB2 se redactan en lenguaje funcional. Donde no hay consenso firme: **evidencia limitada** / **poco caracterizado**. No se inventan Ki/IC50 en esta fase de mapa.

### 3.2. Matriz curada (resumen)

| Categoria | Candidato | `role` | Perfil CB1 (resumen) | Perfil CB2 (resumen) | Fibrosis / notas | Conf. | PubChem |
|-----------|-----------|--------|----------------------|----------------------|------------------|-------|---------|
| Propílico neutro | **Δ9-THCV** | seed | Antagonista / modulador negativo *in vitro* y a dosis bajas *in vivo*; **flip** a agonista a dosis altas | Agonista parcial (ensayos heterogéneos) | PoC natural imperfecto; sin ancla FPI Janus limpia | high | [93147](https://pubchem.ncbi.nlm.nih.gov/compound/93147) |
| Ácido propílico | **THCVA** | interesting | Poco caracterizado vs THCV neutro | Poco caracterizado | Polaridad / hipótesis periferia; decarboxilación → THCV | medium | [59444416](https://pubchem.ncbi.nlm.nih.gov/compound/59444416) |
| Propílico neutro | **CBDV** | secondary | Baja afinidad; no CB1-ant limpio tipo THCV | No CB2 ago canónico potente | Mecanismos a menudo no CB1/CB2-dominantes | high | [11601669](https://pubchem.ncbi.nlm.nih.gov/compound/11601669) |
| Mayor | **CBD** | control | Baja afinidad; polifarmacología | No CB2 ago “puro” | Antifibrótico en algunos modelos ≠ prueba Janus | high | [644019](https://pubchem.ncbi.nlm.nih.gov/compound/644019) |
| Mayor | **Δ9-THC** | anti_seed | Agonista parcial CB1 | Agonista parcial CB2 | Control positivo de agonismo CB1 | high | [16078](https://pubchem.ncbi.nlm.nih.gov/compound/16078) |
| Menor | **CBG** | control | Baja / incierta | Ago parcial débil; a veces CB2>CB1 | No Janus limpio | high | [5315659](https://pubchem.ncbi.nlm.nih.gov/compound/5315659) |
| Menor oxidado | **CBN** | control | Ago parcial débil CB1 | Ago parcial débil CB2 | Control dual débil | high | [2543](https://pubchem.ncbi.nlm.nih.gov/compound/2543) |
| Menor | **CBC** | control | Débil / TRP | Ago parcial CB2 (heterogéneo) | Poco anclado a FPI Janus | medium | [30219](https://pubchem.ncbi.nlm.nih.gov/compound/30219) |
| Menor C7 | **Δ9-THCP** | anti_seed | Ago CB1 alta afinidad (cadena larga) | También ago CB2 reportado | Control SAR: alargar cadena empeora el norte | high | [6453074](https://pubchem.ncbi.nlm.nih.gov/compound/6453074) |
| Menor C4 | **CBD-C4** (CBDB) | interesting | Poco caracterizado vs CBD/CBDV | Poco caracterizado | Placeholder SAR C3–C5 | medium | [59444413](https://pubchem.ncbi.nlm.nih.gov/compound/59444413) |
| Diseño (no cannabis) | **URB447** | design_comparator | Antagonista CB1 periférico | Agonista CB2 | Comparador de diseño; no hit FPI ni norte planta | high | [25195055](https://pubchem.ncbi.nlm.nih.gov/compound/25195055) |

Otros minors (CBGV, CBCV, CBDA, CBGA, etc.): radar de inventario; **poco caracterizados** como dual CB1-ant/CB2-ago — no priorizar sin binding/función.

### 3.3. Lectura rápida de la matriz

1. **Solo THCV** se acerca al arquetipo natural “CB1 ant / CB2 ago”, y lo hace de forma **imperfecta** (flip).
2. El resto del quimioma aporta **controles**, **scaffolds parciales** o **hipótesis de polaridad** (ácidos), no un segundo PoC Janus tan claro.
3. Si tras inventariar y caracterizar no aparece nada más limpio que THCV flip-prone, el proyecto **debe salir del naturalismo estricto** hacia análogos THCV-like (decisión 1), o declarar fracaso temprano del brazo “solo planta” (sección 7).
4. Criterio de éxito pre-Vina: [`criterio_exito_janus.md`](criterio_exito_janus.md).

### 3.4. Hipótesis THCV-like (refinadas tras gap Vina THCV≈THC)

**Anclaje.** En la retrospectiva del panel, THCV apenas se separa de THC (gap dual ≈ **−0.20 kcal/mol**); URB447 sí. El natural C3 no basta como discriminador de afinidad proxy. Origen vegetal de varinas y prosa completa de H1–H5: [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md). Informe: [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md).

| Hipótesis | Idea química | Racional post-retrospectiva | Riesgo principal |
|-----------|--------------|----------------------------|------------------|
| **H1 — C3→C4 controlada** | Homólogo butílico (no C5–C7) | Ganar contacto hidrofóbico / cerrar gap proxy vs THC **sin** flip a agonismo tipo THC | Deslizar a anti-semilla |
| **H2 — Ácido / THCVA-like** | Carboxilo o prodrug periférico | Polaridad / menor CNS; THCVA ya dio CB1 proxy más débil en el panel | Descarboxilación → flip |
| **H3 — Bioisóstero resorcinol** | Modular fenoles / H-bond | Alterar pose y eficacia CB1 sin alargar cadena a THC | Perder CB2 ago |
| **H4 — Congelar el flip** | Restricción conformacional | Atacar la bifasicidad (defecto funcional de THCV), no solo el score | Síntesis / overfitting cristal |
| **H5 — N-heterociclo polar** | Rasgos tipo URB447 *sobre* scaffold THCV | URB447 separó en Vina; importar polaridad sin abandonar cannabis-first | Salir del espacio semilla |

**Regla:** priorizar **limpiar el flip** + superar separación THCV–THC en el mismo panel ([`criterio_exito_janus.md`](criterio_exito_janus.md)); no “más fibrosis” con CB1 sucio. Palancas amplias: §4.3.

---

## 4. Limitaciones de THCV (prototipo Janus imperfecto)

### 4.1. El flip CB1 y la ventana bifásica

Marco ampliado (R ⇌ R\*, C3 vs C5 / toggle TM6, tabla de eficacia esquemática, H1–H5 y matices Vina ≠ α): [`mecanismo_flip_thcv_cb1.md`](mecanismo_flip_thcv_cb1.md).

La revisión clásica de Pertwee (2008) resume el núcleo del problema: Δ9-THCV **antagoniza** agonistas en tejidos que expresan CB1 con potencia relativamente alta y de modo tejido-/ligando-dependiente, y a la vez es **agonista parcial de CB2** en varios ensayos *in vitro*. *In vivo*, sin embargo, puede comportarse como **antagonista CB1 a dosis bajas** y como **agonista CB1 a dosis altas** (antinocicepción, hipotermia, inmovilidad en anillo, sustitución parcial de THC en discriminación de drogas). Esa bifasicidad no es un detalle cosmético: es el defecto que impide llamar a THCV un Janus “limpio”.

Revisiones posteriores (p. ej. McPartland et al., 2015) enfatizan que THCV **no es rimonabant**: alta afinidad y antagonismo *in vitro* no se traducen siempre en un fenotipo de antagonismo CB1 central robusto y estable *in vivo*. Eso es bueno para seguridad psiquiátrica relativa, pero malo para la **predicibilidad** del perfil terapéutico.

### 4.2. Sin datos FPI como Janus

No hay, a fecha de esta redacción, un cuerpo de evidencia que demuestre THCV como antagonista CB1 periférico + agonista CB2 eficaz en modelos de **fibrosis pulmonar idiopática** o bleomicina con atribución causal limpia a ese perfil dual. Cualquier extrapolación desde metabolismo, inflamación o epilepsia es **hipótesis**, no ancla.

### 4.3. Vías de optimización estructural (THCV-like)

Direcciones químicas coherentes con la semilla amplia (sin exigir que ya existan hits publicados):

| Palanca | Idea | Para qué |
|---------|------|----------|
| Cadena alquílica C3 → C4 (y vecindad) | Explorar butílicos / homologación corta sin ir a C5–C7 tipo THC/THCP | Ajustar eficacia CB1 (reducir agonismo residual) manteniendo engagement CB2 |
| Propílicos “congelados” | Restricciones conformacionales, saturación/insaturación del anillo | Separar antagonismo CB1 de agonismo a alta ocupación |
| Ácidos / ésteres (THCVA, profármacos) | Aumentar polaridad o liberar el neutro en periferia | Sesgo periférico, ADME, menor carga SNC |
| Bioisósteros del resorcinol / fenol | Sustituciones que modulen H-bond y lipofilia | Limpiar flip, metabolitos, formulabilidad |
| Periferia por diseño | TPSA, carga, sustratos de eflujo; entrega pulmonar | Evitar repetición rimonabant aunque el perfil receptor mejore |

**Regla:** optimizar para **eliminar el flip** y estabilizar CB1-ant + CB2-ago; no optimizar para “más efecto en un modelo de fibrosis” con CB1 sucio.

---

## 5. Criterios de evaluación para fibrosis (filtro de indicación)

Estos criterios se aplican **después** de tener (o priorizar) un perfil de receptor aceptable. Son mecánicos y de literatura; la extrapolación de CB1/CB2 a FPI humana sigue siendo incompleta (véase memoria de fibrosis).

### 5.1. Eje celular y molecular (qué medir conceptualmente)

| Eje | Por qué importa | Nota crítica |
|-----|-----------------|--------------|
| **TGF-beta1** | Motor central de fibrogénesis y transición a miofibroblasto | Modular TGF-beta vía ECS es plausible; no implica que cualquier cannabinoide sea antifibrótico |
| **EMT / pérdida de fenotipo epitelial** | Reparación aberrante del alvéolo | Extrapolación fuerte; no todos los modelos ECS lo capturan |
| **Fibroblastos -> miofibroblastos** (alpha-SMA, contractilidad) | Productores de MEC | CB2 ago y CB1 ant tienen apoyo preclínico *por separado*; el dual falta |
| **AEC2** (células epiteliales alveolares tipo II) | Nicho de lesión/reparación en IPF | Datos ECS directos aún limitados |
| **Colágeno I/III** y matriz | Readout clásico de fibrosis | Necesario pero no específico de mecanismo Janus |
| **Inflamación** (macrófagos alveolares, citocinas) | CB1 en macrófagos profibróticos (Cinar et al.); CB2 en inmunomodulación | Buen puente mecanístico; no sustituye histología fibrótica |

### 5.2. Lectura CB1 vs CB2 en fibrosis (tono crítico)

- **CB1 pro-fibrótico (cuando hiperactivo):** apoyo sólido en IPF humana y bleomicina (Cinar 2017 y trabajos de macrófagos alveolares). Eso justifica *antagonismo CB1 periférico* como modalidad, no cualquier ligando que “toque” CB1.
- **CB2 protector:** revisiones y agonistas selectivos (p. ej. JWH133 en fibrosis pulmonar experimental) apuntan a antiinflamación y menor depósito de matriz. Extrapolación a un fitocannabinoide parcial y polifarmacológico = **paso largo**.
- **El salto Janus:** combinar ambos en una sola molécula es la hipótesis del proyecto; **aún no está validado en FPI**. Por tanto, un hit de fibrosis con perfil CB1 ambiguo no “gana” frente a un hit de receptor limpio pendiente de ensayo antifibrótico.

### 5.3. Orden de gates

1. Binding / función: CB1 antagonismo (sin agonismo residual problemático en la ventana dosis).
2. Binding / función: CB2 agonismo (parcial aceptable si estable y periférico).
3. ADME / periferia (SNC bajo o entrega pulmonar).
4. Modelos celulares de fibrogénesis (TGF-beta, miofibroblasto, colágeno).
5. Modelos *in vivo* de fibrosis pulmonar (y solo entonces claims de FPI).

---

## 6. Reglas del pipeline de investigación

1. **Receptor limpio → luego indicación.** Ningún score de fibrosis, similitud a CBD, ni narrativa de “cannabinoide antifibrótico” puede saltarse el filtro CB1-ant / CB2-ago.
2. **Cannabis-first, no cannabis-only.** Inventariar y entender el quimioma; optimizar con análogos THCV-like cuando el natural falle en limpieza de perfil.
3. **THCV es semilla, no producto.** Todo plan que asuma THCV como fármaco FPI sin resolver el flip está fuera de brújula.
4. **Controles obligatorios.** THC (anti-semilla), CBD (polifarmacología), URB447 (Janus sintético periférico) como referencias de contraste.
5. **Minors ambiguos ≠ hits.** THCP, CBD-C4, ácidos poco leídos: radar, no priorización ciega.
6. **Periferia es parte del perfil**, no un nice-to-have, para antagonismo CB1 crónico.
7. **Documentar descartes.** Si un candidato falla por flip CB1, se registra como aprendizaje de SAR, no como “casi funcionó en fibrosis”.
8. **Sin docking como entrega de esta fase.** El mapa químico y los criterios mandan ahora; el in silico vendrá anclado a esta brújula (`configs/cb1_cb2.yaml`, memoria de fibrosis).

---

## 7. Criterios de fracaso temprano (brazo “solo planta / solo THCV”)

Declarar **fracaso temprano del brazo natural estricto** (no necesariamente del proyecto entero) si se cumplen de forma acumulativa:

1. **THCV permanece flip-prone** en la ventana dosis relevante (antagonismo a baja dosis + agonismo CB1 a alta dosis) sin margen terapéutico usable.
2. **Ningún otro fitocannabinoide natural** del inventario muestra perfil CB1-ant / CB2-ago más limpio tras revisión de literatura y, cuando existan, ensayos de binding/función.
3. **Los ácidos / minors** (THCVA, varins, C4, etc.) no aportan evidencia funcional que mejore el perfil Janus; solo hipótesis de polaridad sin datos.
4. No hay ruta clara de **análogo cercano** (cadena, éster, bioisóstero) con hipótesis SAR testeable — o esa ruta se rechaza explícitamente por recursos/alcance.

**Qué implica el fracaso temprano:** no abandonar fibrosis ni el perfil Janus; **abandonar la idea de que el fármaco ya está en la planta**. El norte pasa a análogos THCV-like + comparadores sintéticos, con la planta como scaffold histórico y de PoC.

**Qué no es fracaso temprano:** falta de datos FPI para THCV (esperado); falta de docking; polifarmacología de CBD (ya clasificada como control).

---

## 8. Relación con el resto del repo

| Recurso | Rol |
|---------|-----|
| [`literatura_fibrosis_cb1_cb2.md`](literatura_fibrosis_cb1_cb2.md) | Memoria biológica: por qué CB1-ant / CB2-ago importa en fibrosis/IPF |
| Este documento | Brújula química: qué del cannabis (y análogos) merece el perfil |
| [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md) | Biosíntesis C3/varinas, landraces, ratios; H1–H5 THCV-like vs gap Vina |
| [`../data/libraries/quimioma_semillas.csv`](../data/libraries/quimioma_semillas.csv) | Tabla operativa de semillas / controles / SMILES (mapa, no hit table masiva) |
| [`criterio_exito_janus.md`](criterio_exito_janus.md) | Umbral: “más limpio que THCV” + superar separación THCV–THC en panel |
| [`configs/cb1_cb2.yaml`](../configs/cb1_cb2.yaml) | Configuración de foco: cannabis-first, semilla THCV, análogos permitidos, fibrosis como filtro segundo |
| [`README.md`](../README.md) / [`docs/README.md`](README.md) | Entrada al mapa |

---

## 9. Referencias (selección)

1. Pertwee R.G. The diverse CB1 and CB2 receptor pharmacology of three plant cannabinoids: Δ9-THC, CBD and Δ9-THCV. *Br J Pharmacol.* 2008. https://doi.org/10.1038/sj.bjp.0707442 · [PMC2219532](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2219532/)
2. Pertwee R.G. et al. The psychoactive plant cannabinoid Δ9-THC is antagonized by Δ8- and Δ9-THCV in mice in vivo. *Br J Pharmacol.* 2007. https://doi.org/10.1038/sj.bjp.0707134 · [PubMed 17245367](https://pubmed.ncbi.nlm.nih.gov/17245367/)
3. McPartland J.M. et al. Are CBD and Δ9-THCV negative modulators of the endocannabinoid system? A systematic review. *Br J Pharmacol.* 2015. https://doi.org/10.1111/bph.12944 · [PMC4301686](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4301686/)
4. Walsh K.B. et al. Minor cannabinoids: biosynthesis, molecular pharmacology and potential therapeutic uses. *Front Pharmacol.* 2021. https://doi.org/10.3389/fphar.2021.777804
5. Rosenthaler S. et al. Differences in receptor binding affinity of several phytocannabinoids… *Neurochem Int.* / PubMed [25311884](https://pubmed.ncbi.nlm.nih.gov/25311884/) (Ki relativos CBDV, CBC, CBG, CBN, etc.; no explica por sí solo efectos celulares).
6. Zagzoog A. et al. In vitro and in vivo pharmacological activity of minor cannabinoids… *Sci Rep.* 2020. https://doi.org/10.1038/s41598-020-77175-y
7. Navarro G. et al. Cannabigerol action at CB1 and CB2… *Front Pharmacol.* 2018. https://doi.org/10.3389/fphar.2018.00632
8. Cinar R. et al. Cannabinoid CB1 receptor overactivity contributes to the pathogenesis of idiopathic pulmonary fibrosis. *JCI Insight.* 2017. https://doi.org/10.1172/jci.insight.92281
9. Targeting CB1 in pro-fibrotic alveolar macrophages… *JCI Insight.* https://doi.org/10.1172/jci.insight.187967
10. Therapeutic potential of agents targeting CB2 in organ fibrosis. *Pharmacol Res Perspect.* https://doi.org/10.1002/prp2.1219
11. JWH133 and experimental pulmonary fibrosis. *BMC Pulm Med.* 2023. https://doi.org/10.1186/s12890-023-02747-3
12. LoVerme J. et al. URB447, peripherally restricted CB1 antagonist / CB2 agonist. *Bioorg Med Chem Lett.* 2009. https://doi.org/10.1016/j.bmcl.2008.12.059
13. Citti C. et al. / literatura sobre THCP (agonismo CB1 potenciado por cadena heptílica) — tratar como **anti-semilla** estructural frente al norte Janus; verificar paper primario antes de citar potencias numéricas en tablas de hits.

---

## 10. Notas para mantener vivo este mapa

- Actualizar filas cuando haya Ki/EC50/IC50 curados (ChEMBL + paper primario), sin mezclar ensayos no comparables en una sola celda numérica.
- Registrar cada análogo THCV-like sintetizado o comprado con el mismo esquema de columnas.
- Si un minor pasa de “poco caracterizado” a perfil Janus limpio, promoverlo a **semilla** y bajar THCV a “semilla histórica / control de flip”.
- Enlazar resultados futuros de binding (no solo docking) en `results/reports/`.

### Nota (2026-08-06) — retrospectiva Vina del panel de 11

Se lanzó una validación retrospectiva pequeña (preparación 3D pH 7.4 + docking dual Vina en CB1 **5TGZ** / CB2 **6PT0**) sobre `data/libraries/quimioma_semillas.csv`, para comprobar si THCV/URB447 se separan de anti-semillas por **afinidad/pose proxy** (no por función). Informe: [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md). Lectura química: THCV≈THC en dual → hipótesis y literatura de varinas en [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md).

*Fin de la versión actual del quimioma. Ampliar en prosa y tablas, no solo en listas de deseos.*
