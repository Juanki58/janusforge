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

Convenciones de la columna **Diagnóstico**:

- **semilla** — PoC natural o análogo cercano del perfil Janus deseado; punto de partida de optimización.
- **secundaria** — interés químico o periférico, pero no prototipo Janus claro.
- **interesante** — señal parcial o hipótesis abierta; evidencia incompleta.
- **control** — referencia conocida (agonista, polifarmacológico, etc.) para contrastar ensayos.
- **anti-semilla** — perfil incompatible con el norte (p. ej. agonismo CB1 fuerte); no optimizar hacia aquí.
- **ambiguo / poco caracterizado** — datos insuficientes o contradictorios; no asignar afinidades firmes.

Los perfiles CB1/CB2 se redactan en lenguaje funcional (antagonista, agonista parcial, baja afinidad, etc.). Donde no hay consenso firme se marca **evidencia limitada** o **poco caracterizado**. No se inventan Ki/IC50; cuando se citan órdenes de magnitud, vienen de revisiones o papers primarios referenciados abajo.

| Categoria | Candidato | Perfil CB1 | Perfil CB2 | Fibrosis/FPI / notas | Diagnóstico |
|-----------|-----------|------------|------------|----------------------|-------------|
| Propílico neutro (varin) | **Δ9-THCV** | Antagonista / modulador negativo en muchos ensayos *in vitro* y a dosis bajas *in vivo*; a dosis altas puede comportarse como **agonista** (flip bifásico). Perfil tejido- y ligando-dependiente (Pertwee). | Agonista parcial en varios ensayos *in vitro* (revisiones Pertwee / McPartland). Algunos reportes conflictivos (agonismo vs antagonismo según ensayo). | Sin datos robustos en FPI/bleomicina como Janus limpio. PoC natural del perfil *deseado a baja dosis*, pero el flip CB1 impide tratarlo como fármaco listo. | **semilla** (prototipo Janus *imperfecto*) |
| Propílico neutro (varin) | **CBDV** | Baja afinidad ortostérica típica; no es antagonista CB1 “limpio” tipo THCV. Efectos a menudo independientes de CB1 (TRP, GPR55, etc.). | Afinidad baja–moderada según fuente; en algunos ensayos más actividad relativa en CB2 que en CB1, pero **no** un agonista CB2 canónico potente. Evidencia limitada para perfil Janus. | Interés antiinflamatorio / neuroinflamatorio en literatura, mecanismos no CB1/CB2-dominantes. No hay ancla FPI sólida vía Janus. | **secundaria** / interesante (scaffold varin, no PoC Janus) |
| Ácido propílico | **THCVA** (ácido) | Poco caracterizado en ensayos funcionales CB1 modernos frente a THCV neutro. El carboxilo aumenta polaridad → hipótesis de **menor penetración SNC** / mayor sesgo periférico tras (o sin) decarboxilación controlada. | Poco caracterizado. | Interés principal: **periferia / polaridad / prodrug** del scaffold THCV, no potencia demostrada en fibrosis. Decarboxilación → THCV (y su flip). | **secundaria** (interés periferia) |
| Mayores / controles | **CBD** | Baja afinidad; antagonismo funcional / modulación negativa de agonistas en algunos tejidos; polifarmacología alta (no Janus limpio). | No es agonista CB2 canónico “puro”; interacciones complejas. | Efectos antifibróticos reportados en ciertos modelos; atribución mecanística ambigua (no prueba el perfil Janus). | **control** (región química útil; no dogma) |
| Mayores / controles | **Δ9-THC** | Agonista parcial CB1 (psicoactivo). | Agonista parcial CB2. | Irrelevante como candidato Janus; útil como control positivo de agonismo CB1. | **anti-semilla** / control |
| Menor | **CBG** | Afinidad baja–micromolar; efectos parciales / inciertos en CB1. | Agonista parcial débil en varios ensayos; sesgo CB2>CB1 en parte de la literatura. | Antiinflamatorio en modelos diversos; no perfil Janus limpio. Evidencia FPI vía CB1-ant/CB2-ago: limitada. | **interesante** (control de parcial agonismo CB2 débil) |
| Menor | **CBC** | Actividad CB1 débil / parcial en algunos ensayos; a menudo efectos vía TRP. | Agonista parcial con cierto sesgo CB2 en literatura reciente; evidencia heterogénea. | Poco anclado a FPI Janus. | **interesante** / poco caracterizado como Janus |
| Menor (oxidado) | **CBN** | Agonista parcial débil CB1 (menos potente que THC). | Agonista parcial débil CB2. | No Janus; control de agonismo débil dual. | **control** / anti-semilla suave |
| Menor cadena larga | **THCP** (Δ9-THC heptílico) | Agonista CB1 de alta afinidad reportada (cadena C7); dirección **opuesta** al norte Janus. | Agonismo CB2 también reportado; no limpia el problema CB1. | No priorizar. Sirve de control estructural: alargar cadena hacia “más THC” empeora el perfil deseado. | **anti-semilla** / ambiguo para CB2 pero **malo para CB1** |
| Menor cadena C4 | **CBD-C4** / nor-CBD / análogos butílicos | Poco caracterizado de forma sistemática vs CBD/CBDV. | Poco caracterizado. | Placeholder de SAR de cadena (C3–C5); no asignar perfil Janus sin datos. | **ambiguo / poco caracterizado** |
| Otros minors | CBGV, CBCV, CBDA, CBGA, etc. | En general **poco caracterizados** de forma funcional dual CB1-ant/CB2-ago. | Idem. | Mantener en radar de inventario; no priorizar sin binding/función. | **ambiguo / poco caracterizado** |
| Análogo de diseño (no cannabis) | **URB447** | Antagonista CB1 periférico (literatura LoVerme 2009). | Agonista CB2. | No es hit de FPI; **comparador de diseño** del perfil Janus limpio + periferia. | **control de diseño** (no norte cannabis) |
| Análogo de diseño (opcional) | Series tipo AM1710 / ligandos duales citados en config | Variable; verificar paper a paper. | Variable. | Anclas sintéticas para SAR, no semilla vegetal. | **control de diseño** |

### Lectura rápida de la matriz

1. **Solo THCV** se acerca al arquetipo natural “CB1↓ / CB2↑”, y lo hace de forma **imperfecta** (flip).
2. El resto del quimioma aporta **controles**, **scaffolds parciales** o **hipótesis de polaridad** (ácidos), no un segundo PoC Janus tan claro.
3. Si tras inventariar y caracterizar no aparece nada más limpio que THCV flip-prone, el proyecto **debe salir del naturalismo estricto** hacia análogos THCV-like (decisión 1), o declarar fracaso temprano del brazo “solo planta” (sección 7).

---

## 4. Limitaciones de THCV (prototipo Janus imperfecto)

### 4.1. El flip CB1 y la ventana bifásica

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
| **TGF-β1** | Motor central de fibrogénesis y transición a miofibroblasto | Modular TGF-β vía ECS es plausible; no implica que cualquier cannabinoide sea antifibrótico |
| **EMT / pérdida de fenotipo epitelial** | Reparación aberrante del alvéolo | Extrapolación fuerte; no todos los modelos ECS lo capturan |
| **Fibroblastos → miofibroblastos** (α-SMA, contractilidad) | Productores de MEC | CB2 ago y CB1 ant tienen apoyo preclínico *por separado*; el dual falta |
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
4. Modelos celulares de fibrogénesis (TGF-β, miofibroblasto, colágeno).
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

*Fin de la versión actual del quimioma. Ampliar en prosa y tablas, no solo en listas de deseos.*
