# Guía Maestra: Fundamentación del Programa y Hoja de Ruta de Suministro (`janusforge`)

| | |
|---|---|
| **Jerarquía del Documento** | Documento Normativo Nivel 0 (Norma Fuente Matrix) |
| **Versión** | 1.0 (Oficial / Congelada) |
| **Última revisión** | 2026-08-06 |
| **Propósito** | Establecer la jerarquía operativa del proyecto. Separa el desarrollo del candidato terapéutico (Track 1) de las estrategias de suministro de biomasa y controles (Track 2). |

---

## 1. Declaración de Principios y Desacoplamiento de Tracks

`janusforge` es un programa de descubrimiento de fármacos (*Drug Discovery*) enfocado en el perfil Janus (CB1-ant / CB2-ago) para la fibrosis pulmonar (IPF).

- **El Cuello de Botella es Farmacológico, no Agrícola:** La Δ9-THCV natural presenta una ventana terapéutica estrecha y un efecto bifásico (*flip* a agonista en CB1 a dosis altas) con un gap energético in silico insignificante frente al Δ9-THC (−0.20 kcal/mol). Ningún proceso de cultivo ni extracción botánica corrige las limitaciones intrínsecas de la molécula nativa.
- **El Fármaco no es la Planta:** La planta representa la prueba de concepto (PoC) inicial. La solución terapéutica requerirá análogos dirigidos (H1–H5) o derivados puros funcionalizados.

### Diagrama de tracks

```text
TRACK 1: DRUG DISCOVERY (PRIORIDAD #1)
  [ In Silico / Docking Dual ] ──► [ Análogos H1–H5 ] ──► [ Síntesis / Ensayos In Vitro ]
                                                              ▲
TRACK 2: SUPPLY CHAIN (INFRAESTRUCTURA)                       │
  [ Estándares Puros ] ──► [ Breeding / MAS THC-Zero ] ───────┘
```

| Track | Rol | Prioridad |
|-------|-----|-----------|
| **Track 1 — Drug Discovery** | Diseño de ligando / análogos H1–H5; resuelve el cuello de botella farmacológico | **#1 (núcleo prioritario)** |
| **Track 2 — Supply Chain** | Producción de biomasa, estándares puros y controles experimentales | Secundario (infraestructura) |

---

## 2. Track 1 (Prioritario): Descubrimiento y Optimización del Ligando Janus

El objetivo central del programa es la síntesis o selección de moléculas que superen el *gate* de selectividad THCV–THC mediante las 5 hipótesis de optimización (H1–H5):

1. **H1 (Extensión de Cadena C3 → C4 / CBDB-like):** Bloqueo estérico del bucle TM3–TM6 en CB1.
2. **H2 (Derivados Carboxílicos / THCVA / Ésteres):** Aumento de TPSA/LogP para restricción periférica e incapacidad de cruzar la BBB.
3. **H3 (Bioisósteros del Resorcinol):** Optimización de la red de enlaces de H en la cavidad activa de CB2.
4. **H4 (Modificación conformacional del anillo central):** Reducción de insaturación para fijar estado inactivo en CB1.
5. **H5 (Sustitución en C1′):** Ramificación en posición bencílica para maximizar el sesgo periférico.

---

## 3. Track 2 (Secundario): Matriz de Evaluación de Fuentes de Suministro (Supply)

Para la obtención de material de referencia, controles experimentales o precursores de extracción (cuando el candidato requiera andamiajes naturales), las opciones de suministro se priorizan formalmente según el siguiente veredicto técnico:

| Estrategia de Supply | Pureza / CMC | Resolución del Flip Janus | Velocidad a In Vitro | Regulación EU | Prioridad en Track 2 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Síntesis / Estándar Puro** | **Alta** | **Alta (H1–H5)** | **Rápida** | N/A (Químico) | **#1 (Inmediata)** |
| **Breeding / MAS THC-Zero (A-nat)** | Media | Baja (misma mol) | Lenta (Años) | **Fuerte (No-OGM)** | **#2 (Materia Prima)** |
| **Biología Sintética / Fermentación** | Alta | Baja (misma mol) | Media | Media (No planta) | **#3 (Escalado Limpio)** |
| **Edición Genética (CRISPR/Cas9)** | Media | Baja (misma mol) | Media | Débil / Cara (OGM/NBT) | **#4 (Reserva)** |

### Análisis de las opciones de biomasa vegetal

- **Vía A-nat (Breeding / Selección asistida MAS):** Es la primera opción de suministro de biomasa no-OGM si se requiere material vegetal de partida con THC inferior a 0.1 %. No obstante, solo suministra el precursor o estándar, no el fármaco optimizado.
- **CRISPR / NBTs:** Queda relegada a alternativa de reserva si el *breeding* tradicional no alcanza el rendimiento requerido y el marco regulatorio europeo sobre nuevas técnicas genómicas (NGT) lo permite.

---

## 4. Matriz de Auditoría Retroactiva

Consúltese esta guía en las revisiones del hito de investigación:

| Pregunta de auditoría | Respuesta normativa |
|-----------------------|---------------------|
| **¿Estamos atascados en la obtención del cultivar?** | Revisar Sección 1: el cuello de botella es la molécula (H1–H5); el cultivar es secundario. |
| **¿Qué vía de biomasa defender ante un comité para regulación en la UE?** | Revisar Sección 3: Vía A-nat (Breeding/MAS no-OGM) como opción #1 de supply vegetal. |

---

## Documentos relacionados (Nivel ≥1)

Enlaces subordinados; no alteran la norma de este documento:

- [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) — brújula química del quimioma CB1/CB2
- [`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md) — biosíntesis C3/varinas, landraces, hipótesis H1–H5
- [`criterio_exito_janus.md`](criterio_exito_janus.md) — gates de éxito pre-ensayo
- [`../results/reports/retrospective_panel_separation.md`](../results/reports/retrospective_panel_separation.md) — separación proxy del panel retrospectivo (gap dual ≈ −0.20 kcal/mol)
