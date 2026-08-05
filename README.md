# Janusforge

Descubrimiento computacional de **Janus cannabinoids**: ligandos duales con perfil

- **CB1** — antagonista (bloqueo)
- **CB2** — agonista (activación)

Perfil relacionado con el espacio químico de cannabinoides tipo CBD (sin replicar CBD como único objetivo), orientado a cribado virtual, priorización y docking dual.

## Objetivo

Encontrar y priorizar compuestos candidatos que antagonicen CB1 y activen CB2 (ligandos “Yin-Yang” / Janus), útiles como leads para inflamación, dolor y trastornos del uso de sustancias, según literatura de dual CB1 antagonist / CB2 agonist.

## Targets

| Receptor | Rol deseado | UniProt (humano) | Notas estructurales |
|----------|-------------|------------------|---------------------|
| CB1 (CNR1) | Antagonista | P21554 | Preferir estructuras con antagonista/inversor conocido |
| CB2 (CNR2) | Agonista | P34972 | Preferir estructuras con agonista ortostérico |

## Pipeline previsto

1. Semillas = duales conocidos (p. ej. URB447, AM12435, GW405833/AM1710 como referencias Janus) + análogos CBD-like
2. Librería candidata (ChEMBL / generativa)
3. Filtros drug-likeness + PAINS
4. Similitud / farmacóforo dual
5. Docking / scoring en CB1 (modo antagonista) y CB2 (modo agonista)
6. Rankeo por score combinado CB1↓ + CB2↑ + ADME

## Estructura

```
janusforge/
├── configs/           # parámetros de runs (CB1/CB2)
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

Ver `configs/cb1_cb2.yaml`.

## Relación con otros repos

Proyecto **independiente** de [molforge](https://github.com/Juanki58/molforge). No es un branch ni subcarpeta de molforge.
