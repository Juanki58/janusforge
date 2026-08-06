# Memoria literaria: fibrosis, envejecimiento y el eje endocannabinoide CB1/CB2

> Documento vivo de investigación para **janusforge**.  
> Idioma: castellano. Formato: prosa científica accesible.  
> Última ampliación: 2026-08-06.  
> Propósito: anclar *qué* se busca, *para qué* y *por qué*, más allá de un cribado genérico de cannabinoides.  
> Brújula química (quimioma cannábico + THCV): [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md).

---

## 0. Norte del proyecto (brújula fijada)

Tres decisiones operativas condicionan cómo leer el resto de esta memoria:

1. **Cannabis-first + análogos.** Los fitocannabinoides naturales son *template* y prueba de concepto; se aceptan análogos cercanos / semi-sintéticos THCV-like (cadena alquílica, esterificación, bioisósteros del resorcinol) para limpiar el flip CB1, ADME y periferia. La planta aporta scaffold, no un dogma de pureza.
2. **Receptor-first.** La prioridad absoluta es un perfil **CB1 antagonista / CB2 agonista limpio**. La fibrosis/FPI es el *para qué* —filtro de indicación **después**—, no una excusa para tolerar farmacología sucia en CB1.
3. **Mapa vivo antes que docking masivo.** El inventario y el juicio químico viven en [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md); esta memoria ancla la biología de fibrosis y el eje ECS.

**Puente químico.** El prototipo natural imperfecto del perfil Janus es **Δ9-THCV** (antagonismo CB1 en muchos ensayos / dosis bajas + agonismo parcial CB2, con flip agonista CB1 a dosis altas). URB447 y otros duales sintéticos siguen siendo *comparadores de diseño*, no el norte cannabis. Detalle, matriz y criterios de fracaso temprano: documento del quimioma. Origen vegetal de las varinas (biosíntesis C3, landraces, por qué la planta co-produce THC) e hipótesis THCV-like: [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md).

---

## 1. Qué se busca, para qué y por qué

**Qué.** Janusforge busca ligandos de perfil dual —denominados en la literatura *Janus cannabinoids* o ligandos *Yin-Yang*— capaces de **antagonizar el receptor cannabinoide tipo 1 (CB1 / CNR1)** y, a la vez, **agonizar el receptor cannabinoide tipo 2 (CB2 / CNR2)**. No se trata de replicar el cannabidiol (CBD) como único objetivo, ni de maximizar afinidad indiferenciada por “cualquier” receptor cannabinoide. El producto deseado es un compuesto (o una familia priorizada de compuestos) con un perfil farmacológico *opuesto* en ambos receptores: bloqueo de CB1 y activación de CB2. La búsqueda química parte del **quimioma cannábico** (con THCV como semilla imperfecta) y se abre a análogos cercanos cuando el natural no limpia el perfil.

**Para qué.** El uso terapéutico que motiva el proyecto es la **fibrosis orgánica**, con prioridad en la **fibrosis pulmonar idiopática (IPF)** cuando la evidencia lo soporta, y con proyección razonable hacia fibrosis en hígado, riñón, corazón y piel, donde el sistema endocannabinoide (ECS) también participa de forma profibrótica o antifibrótica según el receptor. En un horizonte más amplio, la fibrosis es un rasgo transversal del **envejecimiento** y de muchas enfermedades crónicas: el mismo eje molecular puede, por tanto, interesar a patologías distintas que convergen en depósito excesivo de matriz extracelular (MEC) y pérdida de función orgánica. Insistencia de brújula: la indicación **no** precede al perfil de receptor; un compuesto que “mejore” fibrosis con CB1 sucio no cumple el norte.

**Por qué.** La hipótesis central es que, en el microambiente fibrótico, la **sobreactividad de CB1** es en buena medida **profibrótica y proinflamatoria**, mientras que la **activación de CB2** tiende a ser **antiinflamatoria y antifibrótica**. Un único ligando que combine antagonismo CB1 y agonismo CB2 podría, en teoría, empujar el ECS en la dirección terapéuticamente deseable sin depender de dos fármacos separados, y —si se restringe la penetración al sistema nervioso central (SNC)— sin repetir el fracaso clínico de antagonistas CB1 centrados en el cerebro (p. ej. rimonabant). Janusforge traduce esa hipótesis en un programa de descubrimiento anclado primero en el **mapa del quimioma y el perfil funcional**, y más adelante en priorización / cribado in silico (docking dual sobre estructuras de CB1 en modo antagonista y CB2 en modo agonista) cuando la brújula química lo justifique.

---

## 2. El problema clínico y biológico: envejecimiento y fibrosis

### 2.1. Fibrosis como rasgo del envejecimiento

La fibrosis es la acumulación patológica de colágeno y otros componentes de la MEC, mediada sobre todo por la activación de fibroblastos y su transición a **miofibroblastos** (células alpha-SMA+, productoras intensas de colágeno). Este proceso no es exclusivo de una enfermedad concreta: aparece en cicatrización aberrante, en órganos sometidos a lesión crónica y, de forma creciente con la edad, como parte del deterioro tisular asociado al envejecimiento. Inflamación de bajo grado, senescencia celular, disfunción mitocondrial y remodelado de la MEC convergen en un terreno fértil para la fibrogénesis.

Desde el punto de vista del descubrimiento de fármacos, atacar “la fibrosis” exige elegir un contexto clínico donde (i) la necesidad médica sea alta, (ii) existan modelos experimentales y biomarcadores, y (iii) haya anclaje molecular creíble para la hipótesis terapéutica. En janusforge, ese contexto prioritario es la **IPF**, sin renunciar a la relevancia del mismo eje en otros órganos.

### 2.2. Fibrosis pulmonar idiopática (IPF)

La IPF es una enfermedad intersticial pulmonar progresiva, de causa desconocida, caracterizada por cicatrización irreversible del parénquima pulmonar, deterioro de la capacidad de difusión y, en última instancia, insuficiencia respiratoria. El pronóstico sigue siendo grave pese a tratamientos antifibróticos aprobados (p. ej. pirfenidona, nintedanib), que ralentizan pero no detienen la enfermedad ni revierten el daño establecido. La patogenia es multifactorial: lesión epitelial alveolar, activación de macrófagos, señales de TGF-beta y PDGF, transición fibroblasto–miofibroblasto y depósito de colágeno.

Esa complejidad sugiere que estrategias de **un solo blanco** pueden ser insuficientes, y que enfoques que modulen varios nodos del microambiente fibrótico —incluyendo mediadores lipídicos como los endocannabinoides— merecen exploración sistemática.

### 2.3. Fibrosis en otros órganos y el ECS

Más allá del pulmón, la activación de CB1 se ha asociado a progresión fibrótica en **hígado**, **riñón**, **corazón** y **piel**, mientras que agonistas de CB2 han mostrado efectos antifibróticos o antiinflamatorios en varios de esos mismos tejidos (véase sección 4). Esto no implica que un único fármaco Janus cure “toda” fibrosis, pero sí que el **eje CB1 up / CB2 down** (o, más precisamente, señalización CB1 excesiva frente a señalización CB2 insuficiente o poco explotada) es un patrón recurrente en fibrogénesis orgánica. La IPF es, por tanto, el *caso de uso prioritario*; la fibrosis multiórgano es el *contexto biológico* que da sentido a la hipótesis.

---

## 3. El sistema endocannabinoide en fibrosis

El ECS comprende, de forma simplificada, los ligandos endógenos (anandamida / AEA, 2-araquidonilglicerol / 2-AG), las enzimas de síntesis y degradación (p. ej. FAAH, MAGL) y los receptores CB1 y CB2, ambos receptores acoplados a proteína G de clase A. CB1 se expresa de forma abundante en el SNC, pero también en tejidos periféricos (incluido el pulmón). CB2 se asocia clásicamente al sistema inmune y a órganos periféricos, con menor carga psicoactiva cuando se activa de forma selectiva.

En fibrosis, el ECS no es un espectador:

- Los niveles de **anandamida** pueden elevarse en fluidos y tejidos fibróticos.
- La expresión o la señalización de **CB1** puede aumentarse en paralelo a la progresión de la enfermedad.
- La señalización vía **CB2** modula inflamación, activación de fibroblastos y depósito de MEC, a menudo en sentido opuesto al de CB1.

La imagen resultante —y la que motiva el perfil Janus— es la de un sistema con **dos caras funcionales** en el tejido enfermo: CB1 como brazo frecuentemente profibrótico; CB2 como brazo potencialmente protector.

---

## 4. CB1 en fibrosis pulmonar e IPF: evidencia que soporta el antagonismo

### 4.1. Sobreactividad de CB1 en IPF humana y en modelos murinos

Un trabajo clave de Cinar y colaboradores (*JCI Insight*, 2017) demostró que la sobreactividad del eje endocannabinoide/CB1 contribuye a la patogenia de la IPF. En tejido pulmonar y lavado broncoalveolar (BALF) de pacientes con IPF, y en el modelo murino de fibrosis inducida por bleomicina, se observaron elevaciones de anandamida y evidencia de hiperactividad CB1 asociada a progresión de la enfermedad. La deleción genética de *Cnr1* atenuó la fibrosis inducida por bleomicina y mejoró la supervivencia en ratones. Además, un inhibidor híbrido oral y **restringido a periferia** de CB1 e iNOS mostró eficacia antifibrótica superior a la inhibición de cada diana por separado, e incluso detuvo la progresión de fibrosis ya establecida en el modelo animal.

Fuente primaria:  
Cinar R. et al. Cannabinoid CB1 receptor overactivity contributes to the pathogenesis of idiopathic pulmonary fibrosis. *JCI Insight*. 2017.  
https://doi.org/10.1172/jci.insight.92281 · [PMC5396529](https://pmc.ncbi.nlm.nih.gov/articles/PMC5396529/) · [JCI Insight](https://insight.jci.org/articles/view/92281)

### 4.2. Macrófagos alveolares profibróticos y antagonismo CB1 local

Trabajos posteriores han precisado el papel celular de CB1 en el pulmón fibrótico. En particular, se ha propuesto que la sobreactividad de CB1 en **macrófagos alveolares** favorece un microambiente profibrótico, y que el antagonismo de CB1 —incluso con administración pulmonar de antagonistas de acción periférica— mitiga la fibrosis en modelos preclínicos. Esto refuerza dos ideas operativas para el diseño de fármacos:

1. El blanco relevante puede estar **fuera del cerebro**.
2. La estrategia de **restricción periférica** (o de entrega pulmonar) no es un detalle ADME menor: es parte del *rationale* de seguridad, a la luz del fracaso de rimonabant.

Fuente:  
Cinar R. et al. / trabajos relacionados sobre antagonismo CB1 en macrófagos alveolares profibróticos.  
https://doi.org/10.1172/jci.insight.187967 · [PMC12333952](https://pmc.ncbi.nlm.nih.gov/articles/PMC12333952/)

### 4.3. Lectura para janusforge

Para este proyecto, la conclusión operativa no es “CB1 es malo en absoluto”, sino: **en el pulmón fibrótico (y en varios órganos fibróticos), la señalización excesiva de CB1 favorece inflamación y fibrogénesis; antagonizar CB1 en periferia es una modalidad terapéutica con apoyo preclínico sólido en IPF.** El perfil Janus añade una segunda pata —agonismo CB2— en lugar de limitarse a un antagonista CB1 monofuncional.

---

## 5. CB2 en fibrosis: por qué el agonismo es la cara protectora

### 5.1. Patrón general en fibrosis orgánica

Revisiones recientes sintetizan el potencial terapéutico de agentes que activan CB2 en fibrosis de órganos (cardíaca, hepática, renal, pulmonar y cutánea). Mecanísticamente, el agonismo CB2 se asocia con:

- reducción de citocinas proinflamatorias;
- inhibición o atenuación de la transformación fibroblasto → miofibroblasto;
- menor acumulación de MEC / colágeno;
- modulación de vías como TGF-beta, ERK y otras cascadas fibrogénicas.

Fuente de revisión:  
Therapeutic potential of agents targeting cannabinoid type 2 receptors in organ fibrosis. *Pharmacol Res Perspect.*  
https://doi.org/10.1002/prp2.1219 · [PMC11489134](https://pmc.ncbi.nlm.nih.gov/articles/PMC11489134/)

### 5.2. Pulmón: agonistas CB2 en fibrosis experimental

En fibrosis pulmonar experimental, agonistas selectivos de CB2 como **JWH133** han reducido inflamación, cambios histopatológicos y acumulación de matriz en el modelo de bleomicina, con implicación de vías FAK/ERK/S100A4. Otros trabajos han relacionado efectos antifibróticos de compuestos (incluido CBD en ciertos contextos) con dependencia parcial de CB2, aunque el CBD no es un agonista CB2 “limpio” (véase sección 7).

Fuente:  
A selective CB2R agonist (JWH133) protects against pulmonary fibrosis… *BMC Pulm Med.* 2023.  
https://doi.org/10.1186/s12890-023-02747-3

### 5.3. Conexión con fármacos antifibróticos existentes

De forma sugerente, se ha propuesto que parte de los efectos antiinflamatorios/antifibróticos de la **pirfenidona** en modelos de IPF podrían implicar CB2: el co-tratamiento con un antagonista CB2 (SR144528) abolió efectos protectores en ciertos ensayos, lo que apunta a un solapamiento funcional entre vías ya explotadas clínicamente y el ECS. Esto no convierte a CB2 en el único mecanismo de pirfenidona, pero sí refuerza la idea de que **activar CB2 es coherente con estrategias antifibróticas ya validadas en clínica**.

---

## 6. Hipótesis terapéutica Janus / Yin-Yang

### 6.1. Enunciado

**Hipótesis:** un compuesto que **antagonice CB1 y agonice CB2** (perfil Janus / Yin-Yang), preferiblemente con **acción predominante en periferia** (baja penetración al SNC o administración dirigida al pulmón), puede actuar como aliado frente a la fibrosis —en particular frente a la IPF— al:

1. cortar la señalización profibrótica/proinflamatoria mediada por CB1 en el microambiente pulmonar (macrófagos, fibroblastos/miofibroblastos, y posiblemente otras células del nicho alveolar);
2. potenciar la señalización antiinflamatoria/antifibrótica mediada por CB2;
3. evitar, en la medida de lo posible, los efectos adversos psiquiátricos asociados al antagonismo CB1 central.

### 6.2. Por qué un solo ligando dual y no dos fármacos

Un ligando dual no es automáticamente superior a una combinación. Las razones para buscarlo incluyen: farmacocinética unificada, posible ocupación simultánea de ambos receptores en el mismo microambiente, simplificación del desarrollo preclínico temprano, y el hecho de que **ya existen precedentes químicos** de moléculas con ese perfil opuesto (URB447 y otros ligandos Janus). El riesgo es obvio: optimizar dos actividades a la vez es más difícil que optimizar una. Por eso janusforge trata el problema como un **rankeo multiobjetivo** (CB1-ant + CB2-ago + filtros ADME/drug-likeness), no como un docking trivial a un único bolsillo.

### 6.3. Yin-Yang estructural

La metáfora Yin-Yang no es solo retórica. Las estructuras cristalográficas y de criomicroscopía de CB1 y CB2 han mostrado que ligandos muy relacionados pueden adoptar poses y perfiles funcionales **opuestos** en un receptor frente al otro: un mismo quimotipo puede comportarse como antagonista en CB2 y agonista en CB1, o viceversa, según el encaje en el bolsillo y el estado conformacional del receptor. Eso implica que el diseño (o el cribado) de un Janus auténtico exige **modelos estructurales distintos** para cada brazo del perfil: estructura de CB1 compatible con antagonismo, y estructura de CB2 compatible con agonismo.

---

## 7. Precedentes farmacológicos y químicos

### 7.1. Rimonabant y la lección del SNC

Rimonabant (antagonista/agonista inverso de CB1, penetrante al cerebro) demostró eficacia metabólica en humanos, pero fue retirado por efectos adversos psiquiátricos mediables por CB1 central. Esa historia condiciona todo el campo: **antagonizar CB1 sigue siendo atractivo en periferia; hacerlo en el cerebro es, en general, indeseable** para indicaciones crónicas como la fibrosis. Los antagonistas CB1 restringidos a periferia (p. ej. programas tipo monlunabant / MRI-1891) revitalizan la modalidad, con énfasis en el margen de seguridad respecto al SNC.

### 7.2. Δ9-THCV: prototipo natural Janus imperfecto

Dentro del quimioma cannábico, **Δ9-tetrahidrocannabivarina (THCV)** es el fitocannabinoide que más se acerca al arquetipo deseado: en muchos ensayos *in vitro* antagoniza CB1 (de forma tejido- y ligando-dependiente) y se comporta como **agonista parcial de CB2**; *in vivo*, sin embargo, muestra una **ventana bifásica** (antagonismo CB1 a dosis bajas; agonismo CB1 a dosis altas). Esa bifasicidad es exactamente el tipo de “farmacología sucia” que la brújula prohíbe tolerar solo porque el scaffold sea natural o porque un modelo de fibrosis pudiera responder.

THCV es, por tanto, **semilla / PoC**, no candidato listo. No hay cuerpo sólido de datos FPI que lo validen como Janus periférico. Las vías de optimización (cadena C3→C4, ácidos tipo THCVA, ésteres, bioisósteros, periferia) y la matriz completa del quimioma están en [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md).

Fuentes ancla:  
Pertwee R.G. *Br J Pharmacol.* 2008. https://doi.org/10.1038/sj.bjp.0707442 · McPartland J.M. et al. *Br J Pharmacol.* 2015. https://doi.org/10.1111/bph.12944

### 7.3. URB447: comparador sintético CB1 ant / CB2 ago periférico

URB447 ([4-amino-1-(4-chlorobenzyl)-2-methyl-5-phenyl-1H-pyrrol-3-yl](phenyl)methanone) se describió como el primer ligando mixto **antagonista CB1 / agonista CB2** con acción restringida a periferia: reduce la ingesta y la ganancia de peso en ratones sin entrar de forma apreciable en el cerebro ni antagonizar respuestas CB1 centrales. Valores de referencia frecuentemente citados sitúan potencias en el rango nanomolar (IC50 del orden de ~313 nM en CB1 y ~41 nM en CB2, según fichas y literatura secundaria; conviene verificar en el paper primario y en ensayos propios).

Fuente primaria:  
LoVerme J. et al. Synthesis and characterization of a peripherally restricted CB1 cannabinoid antagonist, URB447… *Bioorg Med Chem Lett.* 2009;19:639–643.  
https://doi.org/10.1016/j.bmcl.2008.12.059 · [PubMed 19128970](https://pubmed.ncbi.nlm.nih.gov/19128970/)

URB447 no es un fármaco de IPF ni el norte cannabis del proyecto; es un **comparador de diseño** del perfil Janus limpio + periferia. Trabajos posteriores lo han explorado en otros contextos (p. ej. metástasis hepática en modelos tumorales), lo que confirma interés biológico pero no sustituye la validación antifibrótica específica ni desplaza a THCV/análogos como semilla química prioritaria.

### 7.4. Otros ligandos Janus / duales de referencia

En el espacio de cribado de janusforge figuran, como semillas o anclas de literatura (a completar con SMILES y datos de actividad), compuestos o series asociadas a perfiles duales o parcialmente Janus, entre ellos referencias citadas en la configuración del proyecto (p. ej. AM12435, GW405833, AM1710). Su papel aquí es de **ancla química sintética**: definen regiones del espacio molecular donde el perfil CB1-ant / CB2-ago es plausible, no necesariamente el hit clínico final ni el reemplazo del quimioma cannábico.

### 7.5. CBD como referencia imperfecta

El cannabidiol ocupa un lugar ambivalente. Es un andamiaje natural ampliamente estudiado, con efectos antiinflamatorios reportados y, en algunos modelos, antifibróticos. Sin embargo:

- no es un agonista CB2 canónico ni un antagonista CB1 “puro”;
- su polifarmacología (canales, GPR55, PPAR, etc.) complica la atribución mecanística;
- usarlo como *único* objetivo de optimización convertiría el proyecto en “mejora de CBD”, no en descubrimiento de un perfil Janus definido.

Por ello, janusforge trata el espacio CBD-like como **región química útil** (lipofilia, andamiajes, filtros de similitud) y como **control** en la matriz del quimioma, no como dogma: el criterio de éxito es el **perfil funcional dual**, no la semejanza máxima al CBD. El prototipo natural imperfecto del norte Janus es THCV, no CBD.

### 7.6. Inhibidores híbridos CB1/iNOS y entrega pulmonar

Los híbridos CB1/iNOS (p. ej. MRI-1867 / zevaquenabant en literatura de fibrosis pulmonar) y las estrategias de antagonismo CB1 restringido o inhalado muestran que el campo se mueve hacia **periferia + multi-target**. Janusforge no replica necesariamente el brazo iNOS; propone un multi-target distinto y complementario: **CB1-ant + CB2-ago**. Ambas líneas comparten el diagnóstico de que la IPF exige más que un único interruptor molecular.

---

## 8. Fibroblastos, miofibroblastos e inflamación: el eje celular

Para conectar la hipótesis con biología celular operable:

1. **Macrófagos / inmunidad innata.** CB1 en macrófagos alveolares se asocia a estados proinflamatorios y profibróticos (p. ej. vía IRF5 en trabajos de IPF). CB2, expresado en células inmunes, modula la intensidad de la respuesta inflamatoria.
2. **Fibroblastos y miofibroblastos.** La activación de CB2 puede reducir señales fibrogénicas (TGF-beta, colágeno, alpha-SMA) y limitar la transformación a miofibroblasto; la señalización CB1 excesiva favorece el entorno que sostiene esa transformación.
3. **Epitelio y microambiente.** La lesión epitelial inicia y mantiene el ciclo de reparación aberrante; el ECS actúa como modulador lipídico de ese microambiente (AEA elevada, FAAH disminuida en algunos contextos de IPF).

El ligando Janus ideal debería, en ensayos futuros (fuera del alcance in silico inmediato), atenuar marcadores de activación miofibroblástica y de inflamación pulmonar sin señales de antagonismo CB1 central.

---

## 9. Anclas estructurales para descubrimiento in silico

El docking dual exige estructuras representativas del **estado funcional** deseado en cada receptor.

| Receptor | Actividad deseada | Estructura de referencia (ejemplo) | Ligando en estructura | Notas |
|----------|-------------------|------------------------------------|------------------------|-------|
| CB1 (CNR1) | Antagonista | [PDB 5TGZ](https://www.rcsb.org/structure/5TGZ) | AM6538 (antagonista estabilizante) | Útil para pose de bloqueo / bolsillo antagonista |
| CB1 | (contraste agonista) | [PDB 5XRA](https://www.rcsb.org/structure/5XRA) / [5XR8](https://www.rcsb.org/structure/5XR8) | Agonistas AM11542 / AM841 | Referencia negativa: evitar optimizar hacia estado activo de CB1 |
| CB2 (CNR2) | Agonista | [PDB 6PT0](https://www.rcsb.org/structure/6PT0) | WIN 55,212-2 + complejo Gi | Estado activo / señalización |
| CB2 | Agonista (alternativa) | [PDB 6KPF](https://www.rcsb.org/structure/6KPF) | Agonista sintético en complejo Gi | Complementaria para pose agonista |
| CB2 | (contraste antagonista) | [PDB 5ZTY](https://www.rcsb.org/structure/5ZTY) | AM10257 | Útil para contraste Yin-Yang / selectividad |

UniProt: CB1 = [P21554](https://www.uniprot.org/uniprotkb/P21554); CB2 = [P34972](https://www.uniprot.org/uniprotkb/P34972).

Estas entradas se reflejan en `configs/cb1_cb2.yaml` y podrán refinarse cuando el pipeline de preparación de receptores esté operativo (limpieza de fusión/quimeras, definición de grid, protonación, etc.).

---

## 10. Gaps (huecos de conocimiento y de traslación)

> **Novelty check (2026-08-06).** Una auditoría explícita de solapamiento con literatura y patentes visibles —incluyendo la duda de si el *rationale* Janus×IPF es “demasiado obvio”— está en [`literatura_prioridad_y_novelty.md`](literatura_prioridad_y_novelty.md). Resumen: el perfil Janus, la farmacología de THCV y la biología CB1/CB2 en fibrosis **sí** están muy publicados; el cruce experimental **THCV (o Janus limpio) × IPF/bleomicina** no apareció en esa búsqueda (ausencia ≠ inexistencia). Leer ese documento antes de reivindicar prioridad o IP.

1. **Falta de un Janus clínico validado en IPF.** Existe apoyo fuerte para antagonismo CB1 en fibrosis pulmonar y para agonismo CB2 en fibrosis orgánica, pero un ligando dual CB1-ant/CB2-ago **demostrado en IPF** sigue siendo, en esencia, una hipótesis a validar.
2. **Polifarmacología y sesgo de señalización.** CB1 y CB2 no son interruptores binarios; agonismo sesgado, ocupación parcial y off-targets pueden alterar el beneficio.
3. **Seguridad a largo plazo.** La IPF exige tratamientos crónicos; el margen SNC de cualquier antagonismo CB1 debe caracterizarse con rigor.
4. **Traducción de docking a función.** Un buen score de docking en CB1-ant y CB2-ago no garantiza el perfil funcional; hacen falta ensayos de binding y de actividad celular.
5. **Heterogeneidad de la fibrosis.** Un hit antifibrótico pulmonar no tiene por qué ser óptimo en hígado o riñón, aunque el eje ECS sea compartido.
6. **CBD y ruido del espacio cannabinoide.** La abundancia de literatura sobre cannabis/CBD puede sesgar la priorización química hacia andamiajes populares en lugar de hacia el perfil funcional.

Estos gaps no invalidan el proyecto: delimitan lo que el cribado in silico puede y no puede afirmar.

---

## 11. Cómo aborda janusforge el descubrimiento (orden receptor → indicación)

Janusforge es un repositorio **independiente** (no un branch de molforge) orientado a convertir la hipótesis anterior en un programa reproducible. El orden de trabajo, fijado por brújula, es:

1. **Mapa del quimioma cannábico** ([`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md)): inventariar fitocannabinoides y análogos cercanos; clasificar semilla / control / anti-semilla; anclar THCV como PoC imperfecto.
2. **Definición explícita del perfil** en configuración (`configs/cb1_cb2.yaml`): CB1 antagonista, CB2 agonista, cannabis-first + análogos THCV-like permitidos, fibrosis/IPF como filtro de indicación *segundo*.
3. **Semillas químicas**: THCV (+ ácidos/análogos cercanos) como norte cannabis; URB447 y otras referencias Janus como **comparadores de diseño**; espacio CBD-like como región/control *sin* exigir CBD como hit.
4. **Solo después**, cuando el mapa lo justifique: librería candidata, filtros drug-likeness/PAINS (sesgo periférico), priorización por similitud/farmacóforo dual, docking/scoring dual (`score_mode: dual_janus`) y rankeo CB1-ant + CB2-ago + ADME.

El presente documento es la **memoria biológica** (fibrosis / ECS). La **brújula química** vive en el quimioma. Ambos deben ampliarse con papers, ensayos y descartes —no solo con scores de docking.

---

## 12. Definición operativa del problema (versión corta)

> Buscamos compuestos de perfil **Janus (CB1 antagonista + CB2 agonista) limpio**, preferiblemente de acción periférica, partiendo del **quimioma cannábico** (prototipo natural imperfecto: **THCV**) y aceptando **análogos cercanos** para limpiar flip CB1 / ADME / periferia. La **fibrosis / IPF** es el *para qué* (filtro de indicación después del receptor), porque la evidencia preclínica indica que la **sobreactividad de CB1** favorece la fibrosis pulmonar y que el **agonismo de CB2** contrarresta inflamación y fibrogénesis. URB447 y PDBs de CB1 antagonizado / CB2 agonizado son anclas de diseño y estructurales; no desplazan el norte cannabis-first.

---

## 13. Bibliografía seleccionada (para ampliar)

1. Cinar R. et al. Cannabinoid CB1 receptor overactivity contributes to the pathogenesis of idiopathic pulmonary fibrosis. *JCI Insight.* 2017. https://doi.org/10.1172/jci.insight.92281  
2. Targeting cannabinoid receptor 1 for antagonism in pro-fibrotic alveolar macrophages mitigates pulmonary fibrosis. *JCI Insight.* https://doi.org/10.1172/jci.insight.187967 · https://pmc.ncbi.nlm.nih.gov/articles/PMC12333952/  
3. Therapeutic potential of agents targeting cannabinoid type 2 receptors in organ fibrosis. *Pharmacol Res Perspect.* https://doi.org/10.1002/prp2.1219  
4. JWH133 y fibrosis pulmonar experimental. *BMC Pulm Med.* 2023. https://doi.org/10.1186/s12890-023-02747-3  
5. Pertwee R.G. The diverse CB1 and CB2 receptor pharmacology of Δ9-THC, CBD and Δ9-THCV. *Br J Pharmacol.* 2008. https://doi.org/10.1038/sj.bjp.0707442  
6. McPartland J.M. et al. Are CBD and Δ9-THCV negative modulators of the endocannabinoid system? *Br J Pharmacol.* 2015. https://doi.org/10.1111/bph.12944  
7. LoVerme J. et al. URB447, peripherally restricted CB1 antagonist / CB2 agonist. *Bioorg Med Chem Lett.* 2009. https://doi.org/10.1016/j.bmcl.2008.12.059  
8. Hua T. et al. Crystal structure of human CB1 with antagonist AM6538. PDB [5TGZ](https://www.rcsb.org/structure/5TGZ).  
9. Xing C. et al. Cryo-EM structure of CB2–Gi with WIN 55,212-2. PDB [6PT0](https://www.rcsb.org/structure/6PT0).  
10. Li X. et al. Crystal structure of human CB2 (antagonist AM10257) — contraste Yin-Yang. PDB [5ZTY](https://www.rcsb.org/structure/5ZTY); discusión estructural en *Cell* / GEN News sobre perfiles opuestos CB1/CB2.

Más referencias de quimioma / minors: ver bibliografía en [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md).

---

## 14. Notas para futuras ampliaciones

- Mantener sincronía con la **matriz del quimioma** (promociones/descartes de candidatos).
- Añadir tabla de potencias (Ki/IC50/EC50) de semillas Janus y fitocannabinoides cuando se curaten SMILES y ChEMBL IDs.
- Incorporar sección específica de **envejecimiento pulmonar** (senescencia de fibroblastos, SASP) y su solapamiento con ECS.
- Documentar resultados de docking y falsos positivos recurrentes *cuando* el pipeline in silico se active bajo la brújula receptor-first.
- Expandir fibrosis hepática/renal con el mismo rigor que IPF si el programa se generaliza.
- Registrar decisiones negativas (compuestos descartados y por qué), incluido fracaso temprano del brazo “solo planta” si THCV sigue flip-prone y no hay natural más limpio.

*Fin de la versión actual de la memoria. Ampliar en prosa, no solo en listas.*
