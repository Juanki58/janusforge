# Guía Maestra: Fundamentación Biotecnológica y Hoja de Ruta de Quimiotipos (janusforge)

| | |
|---|---|
| **Estatus del Documento** | Guía Primaria de Referencia (**Nivel 0 / Norma Fuente**) |
| **Última revisión** | 2026-08-06 |

---

## Propósito

Servir de ancla científica e histórica cuando el proyecto requiera evaluar **retroactivamente** la viabilidad de extracción, edición genética, síntesis o escalado biotecnológico de los candidatos Janus.

Documentos subordinados (Nivel ≥1):

- [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md) — biosíntesis C3/varinas, landraces, hipótesis H1–H5
- [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) — brújula química del quimioma CB1/CB2
- [`criterio_exito_janus.md`](criterio_exito_janus.md) — gates de éxito pre-ensayo
- [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md) — separación proxy del panel retrospectivo

---

## 1. El Dilema del Quimiotipo Natural: Por qué la planta no da el fármaco directo

El cribado in silico y la literatura cromatográfica confirman que variedades emblemáticas ricas en Δ⁹-THCV (como la landrace sudafricana *Durban Poison* o líneas genéticas asociadas):

| Rol | Compuesto | Acumulación típica (orden de magnitud) |
|-----|-----------|----------------------------------------|
| **Semilla** | Δ⁹-THCV | 1 % – 5 % |
| **Anti-semilla** | Δ⁹-THC | 15 % – 24 % (inevitable en el mismo tejido) |

> **Nota de coherencia.** En [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md) §3.2–3.3, revisiones recientes sitúan THCV de “Durban Poison” a menudo en **0.2–1.8 %** frente a THC de dos dígitos: el claim retail de “cepa THCV” es marketing; el dilema (THC domina) se mantiene.

### Conclusión farmacológica obligada

Dado que el Δ⁹-THC es un **agonista de CB₁** que desencadena cascadas profibróticas en los macrófagos alveolares y psicoactividad central, un **extracto crudo de planta viva no es clínicamente viable** para fibrosis pulmonar (IPF).

La planta aporta la **prueba de concepto moleculocéntrica**, pero **no** el producto final sin intervención química o biotecnológica.

---

## 2. Hoja de Ruta Biotecnológica: 3 Vías Reales para Obtener el Quimiotipo Janus Limpio

Cuando el programa in silico identifique y valide los hits moleculares (sean la THCVA natural pura o análogos THCV-like), la producción física del compuesto se articulará mediante tres vías tecnológicas fundamentadas:

```
                               ┌───► 1. Edición Genética CRISPR/Cas9 (Knockout de Olivetol Sintasa)
                               │
[ CANDIDATO JANUS VALIDADO ] ──┼───► 2. Biología Sintética / Fermentación en Levaduras (S. cerevisiae)
                               │
                               └───► 3. Síntesis Orgánica / Derivación Semi-sintética (Hipótesis H1–H5)
```

### Vía A: Edición Genética por CRISPR/Cas9 (Knockout enzimático)

| | |
|---|---|
| **Mecanismo** | Silenciamiento o inactivación selectiva del gen de la **olivetol sintasa** (vía del ácido olivetólico / serie C₅). |
| **Resultado** | La planta anula la biosíntesis de THC y CBD, canalizando el 100 % del sustrato (geranil pirofosfato + ácido divarinólico) hacia la THC-sintasa, produciendo **THCVA / THCV pura libre de THC**. |
| **Estatus científico** | Viable y validado por la industria biotecnológica (mutagénesis dirigida en cannabinoides minoritarios). |

### Vía B: Biología Sintética y Fermentación (Biorreactores)

| | |
|---|---|
| **Mecanismo** | Inserción de la ruta metabólica de la serie propílica (C₃) en microorganismos chasis (*Saccharomyces cerevisiae* o *E. coli*). |
| **Resultado** | Producción fermentativa escalable de Δ⁹-THCV o THCVA pura, **0.0 % THC**, sin necesidad de suelo, cultivo vegetal ni procesos complejos de separación cromatográfica. |

### Vía C: Optimización Química y Análogos Semi-sintéticos (Hipótesis H1–H5)

| | |
|---|---|
| **Mecanismo** | Modificación dirigida del andamiaje de la THCV (extensión de cadena C₃ → C₄, bioisósteros del resorcinol, funcionalización carboxílica/periférica). Detalle operativo: [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md) §5. |
| **Resultado** | Moléculas sintéticas que corrigen el flip agonista de la THCV natural y fijan la restricción periférica (PSA/LogP). |

---

## 3. Matriz de Consulta Retroactiva para Fases Futuras

Este documento debe ser consultado en los siguientes hitos del desarrollo:

| Hito del Proyecto | Pregunta a responder mediante esta Guía |
|-------------------|-----------------------------------------|
| **Fase In Silico (Actual)** | ¿Por qué no usamos mezclas complejas ni docking de aceites completos? *(Ver Sección 1)* |
| **Fase de In Vitro / Ensayos** | ¿Compramos estándar puro de THCV o mandamos a sintetizar el análogo H1–H5? |
| **Fase de Propiedad Intelectual** | ¿Protegemos el análogo sintético (Vía C) o la línea vegetal knockout (Vía A)? |
| **Fase de Escalado Preclínico** | ¿Qué vía de producción (Fermentación Vía B vs Síntesis Vía C) ofrece mejor coste/pureza sin THC? |

---

## Nota de jerarquía (Nivel 0)

**Jerarquía:** este documento queda fijado como el **ancla conceptual Nivel 0**. Si en el futuro dudamos de por qué no compramos semillas de *Durban Poison* para extraer aceite, volvemos a la Sección 1 de esta guía y recordamos que del orden del **~80 %** del perfil cannabinoide dominante sería THC profibrótico (THC 15–24 % frente a THCV 1–5 % en el mismo tejido).

**Visión completa:** janusforge abarca desde el byte de docking hasta la levadura en el biorreactor.
