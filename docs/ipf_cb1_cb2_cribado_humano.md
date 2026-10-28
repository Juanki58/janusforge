# Cribado de CNR1 y CNR2 en pulmón humano con IPF

## Pregunta

> **Actualización importante:** este documento registra la primera cohorte (GSE128033). Después se analizaron dos conjuntos humanos independientes y surgió una señal discordante de CNR2 en una de las cohortes de célula única. Consulta el [informe actualizado](priorizacion_cb1_humano_ipf_2026-10-21.md) antes de interpretar este cribado como balance completo.


¿Aparece CB2 (CNR2) en las poblaciones humanas de macrófagos relacionadas con fibrosis pulmonar, junto al fundamento ya descrito para CB1 (CNR1)? Si CNR2 no aparece de forma detectable, eso reduce el apoyo transcriptómico a activar CB2 en ese nicho concreto, pero no demuestra que el receptor esté ausente ni inactivo.

## Datos y método

Se reanalizaron las cuentas de ARN de célula única de [GSE128033 en GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE128033), publicadas junto con el estudio de [Morse et al. (2019)](https://doi.org/10.1183/13993003.02441-2018). Se excluyeron muestras de lavado broncoalveolar y se conservaron las ocho bibliotecas de pulmón sano y ocho de IPF que aparecen en la serie. Se retuvieron columnas con 200–6.000 genes detectados. Para identificar de forma exploratoria macrófagos se exigió detección de al menos 3 de 14 marcadores inmunes/macrofágicos; para fibroblastos, 3 de 7 marcadores mesenquimales. Las subpoblaciones SPP1+ y FABP4+ se definieron por detección del marcador dentro del conjunto de macrófagos. Se contaron células en las que cada transcrito tenía al menos una cuenta.

El procesamiento reproducible está en [scripts/analyze_ipf_gse128033.py](../scripts/analyze_ipf_gse128033.py). Requiere Python, SciPy y el tar original de GEO; las matrices no se incorporaron al repositorio.

## Resultados principales

| Grupo celular | CNR1 detectable | CNR2 detectable | NOS2 detectable |
|---|---:|---:|---:|
| Macrófagos marcador+ sanos (n=17.551) | 44 (0,25 %) | 14 (0,08 %) | 1 (<0,01 %) |
| Macrófagos marcador+ IPF (n=15.420) | 75 (0,49 %) | 11 (0,07 %) | 5 (0,03 %) |
| SPP1+ macrófagos sanos (n=1.532) | 2 (0,13 %) | 4 (0,26 %) | 0 |
| SPP1+ macrófagos IPF (n=6.294) | 19 (0,30 %) | 3 (0,05 %) | 2 (0,03 %) |
| FABP4+ macrófagos sanos (n=9.754) | 24 (0,25 %) | 9 (0,09 %) | 1 (0,01 %) |
| FABP4+ macrófagos IPF (n=4.261) | 39 (0,92 %) | 7 (0,16 %) | 3 (0,07 %) |

La proporción de macrófagos marcador+ con SPP1 detectable subió del 8,7 % al 40,8 % entre las bibliotecas sanas e IPF; MERTK subió del 4,3 % al 18,1 %. Esto confirma que la señal profibrótica de macrófagos está presente en estos datos. CNR1 tuvo una detección escasa, pero aumentó en el conjunto de macrófagos IPF; el patrón es coherente con el estudio espacial humano independiente de [JCI Insight 2025](https://doi.org/10.1172/jci.insight.187967), que encontró mayor CNR1 en macrófagos FABP4+ y SPP1+ de pulmón IPF. CNR2 se detectó en menos del 0,1 % de los macrófagos marcador+ IPF y no aumentó frente a controles en este conjunto.

## Qué significa para Janusforge

Este análisis **apoya la pertinencia humana del brazo CB1** en el nicho de macrófagos profibróticos de IPF. **No aporta respaldo transcriptómico claro para activar CB2 en ese mismo nicho**. Así que la hipótesis Janus (CB1 antagonista + CB2 agonista) sigue siendo posible, pero su brazo CB2 no queda validado aquí; conviene considerarlo una incertidumbre que necesita evidencia específica, no una ventaja humana demostrada.

## Límites

- La secuenciación de célula única pierde muchos transcritos de baja abundancia. La no detección de CNR2 —o CNR1— no equivale a ausencia de proteína, receptor funcional o señalización.
- La etiqueta de macrófago es una regla reproducible de marcadores creada para este cribado; no es la anotación original de cada célula. La subpoblación SPP1+/FABP4+ no debe confundirse con los clústeres SPP1hi y FABP4hi publicados.
- Las células no son réplicas independientes. Los porcentajes agrupados describen lecturas por célula y no prueban una diferencia entre pacientes; las bibliotecas pueden incluir lóbulos de un mismo donante.
- ARN no mide proteína de CB2, ocupación, acoplamiento a Gi/cAMP ni beneficio terapéutico. Tampoco evalúa fibroblastos de forma suficientemente potente en este conjunto.

## Fuentes

- [GSE128033 — GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE128033)
- [Morse et al., European Respiratory Journal 2019](https://doi.org/10.1183/13993003.02441-2018)
- [Estudio espacial de CNR1 en macrófagos humanos con IPF, JCI Insight 2025](https://doi.org/10.1172/jci.insight.187967)
