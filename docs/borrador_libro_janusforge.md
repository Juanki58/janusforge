# Janusforge: del mapa cannabinoide a la decisión experimental

## Borrador de libro del proyecto

**Versión:** 0.1  
**Fecha:** 13 de agosto de 2026  
**Naturaleza:** memoria narrativa interna; no es consejo médico, regulatorio ni legal.  
**Confidencialidad:** no incluye SMILES, coordenadas ni estructuras de NCE no publicadas.

---

## Nota al lector

Este texto cuenta lo que Janusforge ha hecho y, con la misma importancia, lo que **no** ha demostrado. El proyecto persigue un perfil farmacológico denominado *Janus* o *Yin–Yang*: evitar agonismo CB1 y sostener agonismo CB2. La motivación terapéutica es la fibrosis, con IPF como caso prioritario; no es una afirmación de eficacia clínica ni la descripción de un fármaco existente.

La idea rectora es sencilla: el éxito no es obtener un score de docking atractivo. Es identificar, validar y eventualmente proteger una familia molecular cuyo comportamiento funcional sea compatible con CB1 antagonista/no agonista y CB2 agonista, con evidencia experimental reproducible.

---

## 1. El problema que define Janusforge

La fibrosis es una respuesta patológica caracterizada por acumulación de matriz extracelular. Janusforge parte de una lectura de la literatura: la señalización CB1 se asocia en distintos contextos con mecanismos profibróticos o proinflamatorios, mientras que CB2 puede ofrecer una dirección antiinflamatoria/antifibrótica. De ahí nace una hipótesis, no un resultado: un único ligando que combine ambos brazos podría ser más interesante que intervenir uno solo.

El proyecto no busca “otro cannabinoide”. Busca una señal de receptor concreta: CB1 bloqueado o no activado de forma limpia, y CB2 activado. La fibrosis es el propósito clínico; el perfil de receptor es el primer criterio de selección.

## 2. Una regla de diseño: separar descubrimiento y suministro

La documentación normativa separó dos tracks:

- **Track 1 — descubrimiento:** encontrar y validar un ligando Janus.
- **Track 2 — suministro:** estándares, biomasa, breeding o manufactura si resultan pertinentes.

Esta separación fue una buena decisión. Evita que la disponibilidad de material vegetal o una narrativa de cannabis reemplacen la pregunta farmacológica central. El Track 1 es la prioridad y el Track 2 permanece como soporte, no como sustituto de la validación.

## 3. THCV: un punto de partida, no una respuesta

THCV se usó como prototipo natural de un perfil Janus imperfecto. Su valor fue conceptual y metodológico: permitió formular una pregunta más útil que “¿qué molécula dokea mejor?”. La pregunta pasó a ser “¿qué candidato se separa de THC, evita el *flip* funcional de CB1 y mantiene una dirección CB2 deseable?”.

El programa construyó un mapa del quimioma cannabinoide, de varinas y de precedentes CB1/CB2. También fijó anti-criterios: similitud superficial con CBD, un buen score aislado o una historia genérica de antifibrosis no cuentan como éxito.

## 4. La primera campaña: análogos THCV-like H1–H5

La primera campaña generó y evaluó varias hipótesis estructurales alrededor del espacio THCV-like. Los Batches 1 y 2 fueron amplios y enseñaron una lección clara: introducir acidez o determinados ésteres perjudicó el comportamiento proxy en CB1; pequeños cambios de volumen en la región 1′ parecían más prometedores.

En Batch 3, JANUS_H1_02c fue el mejor resultado computacional de esta línea y superó el gate proxy frente a THCV y THC. No obstante, el proyecto no confundió ese resultado con farmacología: la dinámica molecular en membrana POPC de 20 ns no mostró una mejora convincente respecto a THCV en el mecanismo geométrico escogido. La línea THCV-like recibió un **NO-GO como eje principal**.

Este fue un resultado valioso. Cerró una vía sin maquillar el dato y evitó prolongar una optimización basada solo en Vina.

## 5. El pivot: de fitocannabinoides a scaffolds sintéticos

Tras ese NO-GO, Janusforge pivotó hacia precedentes sintéticos de perfil Yin–Yang, especialmente la región conceptual URB447 y compuestos publicados relacionados. El objetivo no era copiar un compuesto ni reclamar invención sobre el arte previo: era utilizar precedentes como mapa para formular hipótesis más rígidas y testeables.

Se prepararon receptores CB1 (5TGZ) y CB2 (6PT0), se documentaron cajas y se ejecutó un panel dual de docking con protocolo reproducible. El gate de Vina comparaba los candidatos con THCV y THC en el mismo marco; era un filtro de ocupación/pose, nunca una medida de afinidad, eficacia o selectividad funcional.

## 6. JANUS_D2_22: el mejor score no fue el mejor lead

En el Batch D1/Option D, JANUS_D2_22 fue el ex-lead de docking: mostró el mejor valor dual observado del panel (–11,277 kcal/mol como salida Vina) y sus poses para CB1 y CB2 están disponibles localmente para inspección. Ese dato justificó, en su momento, una comprobación dinámica adicional.

La simulación de membrana POPC de 20 ns en CB1 5TGZ terminó correctamente y produjo métricas trazables. Sin embargo, su lectura no apoyó el mecanismo de “trinquete” inactivo que se pretendía priorizar: la geometría TM3–TM6 se solapó más con el régimen de THC que con el patrón de referencia THCV. Una hélice TM6 estable no equivalía a una contención funcional deseada.

La decisión registrada es inequívoca: **JANUS_D2_22 está descartado como lead funcional (NO-GO de trinquete CB1)**. Debe conservarse como caso de estudio, control histórico y objeto de visualización, pero no comunicarse como el lead activo del programa. Es quizá la lección metodológica más importante del repositorio: Vina puede ordenar poses; no puede validar la función Janus.

## 7. La línea Qiu: un vehículo de validación, no una invención

El programa examinó de forma trazable los compuestos publicados de Qiu et al. (2023), en particular Qiu-14, dentro de una serie de etapas 0D–0J: verificación 2D, preparación PDBQT, docking CB2, análisis geométrico, matriz de evidencia y control visual. La identidad y el flujo computacional están auditados; la interpretación farmacológica no se ha extrapolado más allá de esos datos.

Qiu-14 tiene un único papel operativo actual: **vehículo publicado de validación** para una hipótesis H1-a de agonismo funcional hCB2. No es una molécula propia de Janusforge, ni un candidato patentable del proyecto, ni una prueba de eficacia en fibrosis.

## 8. La madurez del programa: de computación a ensayo

La parte más madura de Janusforge ya no es generar más docking. Es el paso de validación experimental. Se cerró una especificación H1-a CB2-first para Qiu-14, con controles, material, pureza, formato de ensayo y umbrales de PASS/KILL marcados como TBD cuando aún no están definidos. Esta forma de documentar los TBD es una fortaleza: impide inventar números para aparentar madurez.

También se produjo un paquete CRO con RFQs comparables, lista de envío, borradores de comunicación y scorecard interno. La ruta crítica actual es enviar el mismo paquete a dos o tres CROs, comparar presupuesto, plazo y capacidad, y cerrar los campos pendientes con el proveedor elegido antes de iniciar trabajo húmedo.

## 9. Lo que el proyecto demuestra, infiere y desconoce

| Capa | Estado actual |
|---|---|
| Literatura | Existe racional para estudiar CB1/CB2 en fibrosis y precedentes Yin–Yang. |
| Computación | Receptores, preparación, docking, QC de poses y algunas MD están ejecutados y documentados. |
| Observación negativa útil | H1_02c y D2_22 no sostuvieron el gate geométrico/mecanicista elegido en MD de una réplica. |
| Hipótesis | Qiu-14 puede actuar como agonista hCB2 en el ensayo seleccionado; futuros NCE podrían mejorar el perfil. |
| No demostrado | Afinidad, potencia, eficacia CB1/CB2, perfil Janus de los compuestos propios, actividad antifibrótica, seguridad o beneficio clínico. |

Esta tabla es el contrato epistemológico del proyecto. Mantenerla visible será decisivo cuando aumente la presión por presentar resultados a colaboradores, financiadores o proveedores.

## 10. Propiedad intelectual: oportunidad con puertas, no un atajo

Janusforge creó un landscape de novelty/prior art y una puerta IP operativa. El análisis reconoce zonas ocupadas: el espacio de pirazoles tipo rimonabant, compuestos Qiu publicados y familias con reclamaciones relacionadas con CB1/CB2 y fibrosis. También plantea hipótesis de “blue ocean”, pero las marca correctamente como exploratorias.

La secuencia prudente es: validar con un compuesto publicado, generar evidencia experimental, decidir una familia propia bajo confidencialidad y solicitar revisión de counsel antes de divulgar estructuras, sintetizar una campaña propietaria o hacer afirmaciones de libertad de operación. El landscape no es una opinión FTO ni una garantía de patentabilidad.

## 11. Qué se aprendió del cómputo

1. Un score dual mejor que THCV/THC sirve como filtro comparativo, no como lectura funcional.
2. La separación entre docking, geometría de MD, hipótesis y ensayo húmedo debe permanecer explícita.
3. Un NO-GO temprano puede aumentar la calidad del programa: H1_02c y D2_22 evitaron inversión posterior sobre una inferencia frágil.
4. La reproducción computacional de alta fidelidad tipo Ge/LRIP no es actualmente ruta crítica. Está documentada, pero bloqueada por parámetros y materiales suplementarios pendientes; no debe ejecutarse por inercia.
5. El mayor retorno próximo está en una decisión experimental bien especificada, no en más docking o más generación masiva de compuestos.

## 12. El visor molecular: valor y corrección de lenguaje

El visor local FastAPI + 3Dmol.js es una aportación práctica: permite inspeccionar receptores y poses sin sacar datos sensibles del entorno. Puede cargar CB1/CB2, ligandos y resultados locales, y es una herramienta útil para QC, conversación con un químico medicinal o revisión de CRO.

Su interfaz debe alinear sus etiquetas con el estado científico. JANUS_D2_22 puede aparecer como **“ex‑lead de docking / NO‑GO funcional”**, no como “Lead Option D”. Esta pequeña corrección evita que una conveniencia de navegación cambie accidentalmente la narrativa científica del proyecto.

## 13. Opinión sobre Janusforge

Janusforge destaca por una cualidad que muchas iniciativas tempranas no tienen: la voluntad de registrar los límites de la evidencia y de matar hipótesis cuando no pasan el gate. La documentación, los informes sin SMILES, la trazabilidad de protocolos y el paquete CRO convierten una exploración computacional en un programa de investigación que ya puede sostener una conversación seria con colaboradores.

El riesgo principal no es técnico; es de foco y comunicación. Hay mucha documentación de alta calidad, pero la historia está repartida entre informes y con terminología histórica que puede confundir qué está activo, qué está cerrado y qué solo es un control. También hay artefactos de codificación de caracteres en varios Markdown que restan legibilidad. El siguiente salto de calidad consiste en consolidar un estado único del programa y en llevar la validación H1-a a una decisión real.

En síntesis: la ciencia aún no ha encontrado un lead Janus validado, pero el proyecto sí ha construido un buen sistema para no engañarse sobre ello y para descubrirlo de forma defendible.

## 14. Ruta crítica propuesta

1. Revisar la interfaz y los documentos de estado para que D2_22 figure como ex‑lead/NO‑GO, no como lead.
2. Enviar el paquete H1-a idéntico a 2–3 CROs; recoger cotizaciones comparables.
3. Seleccionar proveedor y cerrar todos los TBD del ensayo, incluidos criterios predefinidos de PASS/KILL.
4. Ejecutar H1-a con Qiu-14 como control publicado; si pasa, planificar H1-b para CB1 como ensayo separado.
5. Solo tras señal experimental y revisión IP: elegir una hipótesis NCE, trabajar bajo confidencialidad y solicitar counsel antes de revelar o sintetizar estructuras propietarias.

No se recomienda, en esta fase, reactivar MD pesada, nuevo docking masivo ni una campaña NCE pública. Son actividades que pueden ser útiles después, pero no sustituyen la evidencia experimental de la ruta crítica.

## 15. Epílogo: la forma correcta de contar el proyecto

La historia de Janusforge no es “hemos descubierto un fármaco antifibrótico”. Es más interesante y más cierta: se formuló una hipótesis farmacológica dual, se construyó una infraestructura de comparación y QC, se descartaron dos señales computacionales que no resistieron un gate más exigente, se delimitó el espacio de propiedad intelectual y se preparó el primer experimento que puede decidir si la hipótesis merece crecer.

El próximo capítulo no se escribirá con un score de docking. Se escribirá con un ensayo CB2 bien controlado, una decisión transparente y, si hay señal, un programa de química medicinal propio y protegido.

---

## Fuentes internas principales

- `README.md` y `docs/README.md`
- `docs/criterio_exito_janus.md`
- `docs/lecciones_aprendidas_track1.md`
- `docs/ip_gate_janusforge.md`
- `results/reports/janusforge_dossier_estado_programa.md`
- `results/reports/h1_h5_design_history.md`
- `results/reports/option_d_batch_d1_gate_summary.md`
- `results/reports/md_d2_22_20ns_summary.md`
- `results/reports/qiu_0l_h1a_experimental_spec.md`
- `results/reports/qiu_0n_status.md`
- `results/reports/qiu_0ip_novelty_landscape.md`
- `results/reports/cro_package_h1a/00_index.md`
