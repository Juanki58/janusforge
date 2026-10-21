# Repriorización tras contraste de datos humanos: CB1 primero en IPF

**Fecha:** 2026-10-21  
**Decisión de programa:** priorizar la hipótesis de antagonismo CB1 periférico/en pulmón para IPF. Mantener agonismo CB2 como brazo opcional secundario; exigir evidencia de beneficio incremental antes de que determine la selección de compuestos. No se declara eficacia ni potencia farmacológica.

## Por qué cambia la prioridad

La primera pantalla de célula única (GSE128033) encontró que los marcadores profibróticos de macrófago SPP1/MERTK aumentan fuertemente en IPF. En esos macrófagos, CNR1 detectable pasó de 0,25 % en controles a 0,49 % en IPF; CNR2 quedó muy bajo, 0,08 % frente a 0,07 %. La señal de CNR1 fue escasa en términos absolutos, acorde con el *dropout* de genes de baja abundancia en célula única.

Una cohorte independiente de tejido pulmonar completo (GSE110147; 22 IPF, 11 controles) dio una diferencia de expresión más clara para CNR1: mediana de RMA log2 6,83 frente a 6,26; diferencia 0,57; Mann–Whitney no ajustado p=0,008. Para CNR2, la mediana fue 6,63 frente a 6,55; diferencia 0,08; p=0,058. Es evidencia asociativa de tejido, no localizada a célula ni causal.

Una segunda colección de célula única (GSE122960) aportó un resultado discordante. Con clasificación heurística de macrófagos por marcadores (8 bibliotecas de donantes control y 4 IPF), CNR1 detectable bajó de 3,96 % a 1,19 %, mientras CNR2 subió de 0,08 % a 0,50 %. Dentro de macrófagos SPP1+, CNR1 fue 2,29 % vs 1,73 % y CNR2 0 % vs 0,64 %. La cohorte IPF es pequeña y esta etiqueta de macrófago no reproduce la anotación publicada; los valores por biblioteca son exploratorios y los p no ajustados no son prueba confirmatoria.

En cambio, la evidencia humana más específica y funcional favorece a CB1: el estudio espacial JCI Insight 2025 localizó aumento de CNR1 en nichos FABP4+/SPP1+ profibróticos y probó en tejido pulmonar humano ex vivo un inhibidor CB1/iNOS. Ese experimento no valida CB2 ni prueba eficacia clínica.

## Decisión

**CB1 pasa a ser el objetivo primario de validación y diseño para IPF.** La prioridad se basa en evidencia humana espacial y ex vivo, además de una asociación bulk independiente. No significa que CNR1 aumente en todos los tipos de macrófago, que bloquearlo vaya a beneficiar pacientes o que el inhibidor sea más potente como molécula.

**CB2 no se descarta.** GSE122960 deja una señal exploratoria de CNR2 en macrófagos SPP1+ de IPF, aunque la señal sigue siendo rara y no está confirmada funcionalmente. En adelante, CB2 debe demostrar que añade actividad antifibrótica por encima del brazo CB1; no debe ser requisito de entrada para priorizar candidatos.

## Qué significa “más prometedor” y qué no sabemos

Las cohortes públicas miden expresión de CNR1/CNR2, no la potencia de ligandos. Potencia farmacológica requiere curvas concentración-respuesta y valores como IC50/EC50 en ensayos comparables; afinidad de unión tampoco basta para distinguir antagonismo, agonismo parcial o sesgo funcional. En el proyecto, llamar a CB1 “más prometedor” describe hoy la prioridad biológica para IPF, no un compuesto que haya demostrado mayor potencia ni un beneficio humano.

## Siguiente criterio de decisión

1. Mantener CB1 periférico/dirigido al pulmón como eje de la próxima hipótesis.
2. Comparar candidatos por función CB1 antagonista y seguridad periférica; registrar CB2 como dato secundario.
3. Reabrir una molécula Janus como prioridad solo si un ensayo funcional muestra una ganancia adicional mediada por CB2 (o una validación de tejido humano equivalente).
4. No convertir transcriptómica ni docking en una afirmación de eficacia clínica.

## Datos y fuentes

- GSE128033: [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE128033); [Morse et al., ERJ 2019](https://doi.org/10.1183/13993003.02441-2018).
- GSE110147: [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110147), matriz de microarray RMA; [Cecchini et al., 2018](https://pubmed.ncbi.nlm.nih.gov/30111332/).
- GSE122960: [GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE122960); [Reyfman et al., AJRCCM 2019](https://doi.org/10.1164/rccm.201712-2410OC).
- [JCI Insight 2025: targeting CB1 in profibrotic alveolar macrophages](https://doi.org/10.1172/jci.insight.187967).
- Reanálisis inicial reproducible: [`ipf_cb1_cb2_cribado_humano.md`](ipf_cb1_cb2_cribado_humano.md).
