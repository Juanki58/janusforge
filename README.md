# Janusforge

Descubrimiento computacional de **Janus cannabinoids** (ligandos *Yin-Yang*): compuestos con perfil dual

- **CB1 (CNR1)** — antagonista (bloqueo)
- **CB2 (CNR2)** — agonista (activación)

No es un cribado genérico de “cannabinoides”. El objetivo es priorizar ligandos que empujen el sistema endocannabinoide en dirección **antifibrótica**, con brújula **cannabis-first + análogos** y prioridad absoluta de **receptor limpio** (CB1 ant / CB2 ago) antes del filtro de indicación.

## Qué se busca, para qué y por qué

| | |
|---|---|
| **Qué** | Ligandos duales CB1-antagonista + CB2-agonista (perfil Janus / Yin-Yang), partiendo del **quimioma cannábico** (prototipo natural imperfecto: **THCV**) y análogos cercanos THCV-like; CBD-like como región/control, **sin** exigir CBD como hit. |
| **Para qué** | Aliados terapéuticos frente a **fibrosis**, con prioridad en **fibrosis pulmonar idiopática (IPF)** *después* de tener perfil de receptor aceptable; el mismo eje es relevante en fibrosis hepática, renal, cardíaca y cutánea. |
| **Por qué** | En IPF y otros órganos fibróticos, la **sobreactividad de CB1** es profibrótica/proinflamatoria; el **agonismo de CB2** tiende a ser antiinflamatorio/antifibrótico. Un ligando dual —idealmente de acción periférica— podría modular ambos brazos sin repetir la toxicidad de SNC de antagonistas CB1 centrados (p. ej. rimonabant). |

**Brújula química** (mapa vivo del quimioma CB1/CB2):  
→ [`docs/quimioma_cannabico_cb1_cb2.md`](docs/quimioma_cannabico_cb1_cb2.md)

Memoria biológica / fibrosis (castellano, prosa científica):  
→ [`docs/literatura_fibrosis_cb1_cb2.md`](docs/literatura_fibrosis_cb1_cb2.md)

## Problema clínico

La **fibrosis** (depósito patológico de matriz extracelular mediado por fibroblastos/miofibroblastos) es un rasgo transversal del **envejecimiento** y de enfermedades crónicas. La **IPF** es una enfermedad pulmonar progresiva con necesidad médica alta; la evidencia preclínica y traslacional vincula el eje endocannabinoide/CB1 a su patogenia, y el agonismo CB2 a protección antifibrótica en pulmón y otros órganos. Janusforge ancla el cribado a esa hipótesis, no a inflamación o dolor de forma genérica.

## Targets

| Receptor | Rol deseado | UniProt (humano) | Estructura preferida (ejemplo) |
|----------|-------------|------------------|--------------------------------|
| CB1 (CNR1) | Antagonista | [P21554](https://www.uniprot.org/uniprotkb/P21554) | [5TGZ](https://www.rcsb.org/structure/5TGZ) (antagonista AM6538) |
| CB2 (CNR2) | Agonista | [P34972](https://www.uniprot.org/uniprotkb/P34972) | [6PT0](https://www.rcsb.org/structure/6PT0) (agonista WIN 55,212-2 + Gi) |

## Pipeline previsto

1. Mapa del quimioma cannábico (THCV = semilla imperfecta; análogos cercanos permitidos; URB447 = comparador de diseño)
2. Filtro receptor-first: CB1 ant / CB2 ago limpio (fibrosis = gate de indicación después)
3. Librería candidata (ChEMBL / generativa) cuando el mapa lo justifique
4. Filtros drug-likeness + PAINS (sesgo hacia propiedades compatibles con periferia)
5. Similitud / farmacóforo dual
6. Docking / scoring en CB1 (modo antagonista) y CB2 (modo agonista) — no es el entregable inmediato
7. Rankeo por score combinado CB1↓ + CB2↑ + ADME

## Estructura

```
janusforge/
├── configs/           # parámetros de runs (CB1/CB2, focus fibrosis/IPF)
├── docs/              # memoria literaria y documentación
├── data/
│   ├── raw/
│   ├── processed/
│   ├── libraries/
│   └── targets/       # cb1/, cb2/
├── models/
├── notebooks/
├── results/
│   ├── hits/
│   ├── docking/
│   └── reports/
├── scripts/
├── src/
│   ├── targets/
│   ├── screening/
│   ├── generative/
│   ├── adme/
│   ├── chemistry/
│   └── pipeline/
├── tests/
└── tools/             # vina, etc. (local, no en git)
```

## Setup

```bash
pip install -r requirements.txt
# Colocar binario Vina en tools/vina.exe (Windows)
```

## Config

Ver [`configs/cb1_cb2.yaml`](configs/cb1_cb2.yaml) (cannabis-first + semilla THCV; fibrosis/IPF como filtro segundo; targets CB1+CB2).

## Documentación

- [`docs/README.md`](docs/README.md) — índice
- [`docs/quimioma_cannabico_cb1_cb2.md`](docs/quimioma_cannabico_cb1_cb2.md) — brújula química / quimioma CB1–CB2
- [`docs/literatura_fibrosis_cb1_cb2.md`](docs/literatura_fibrosis_cb1_cb2.md) — memoria biológica fibrosis / ECS

## Relación con otros repos

Proyecto **independiente** de [molforge](https://github.com/Juanki58/molforge). No es un branch ni subcarpeta de molforge.
