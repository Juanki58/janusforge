# Batch 3 — plan de refino JANUS_H1_02 (público)

> **No SMILES.** Solo IDs conceptuales y dirección de diseño.  
> Vina = afinidad/pose proxy — no éxito Janus funcional ([`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).  
> Historial: [`h1_h5_design_history.md`](h1_h5_design_history.md).

- Estado: **planificado, no ejecutado**
- Scaffold base: **JANUS_H1_02** (1′-metilo; único PASS proxy marginal de Batch 1–2)
- Objetivo proxy (aspiracional): amplificar gap vs THC hacia **>0.80** kcal/mol si es posible, sin reintroducir polaridad que hunda CB1

## Lecciones que anclan el plan

- Ácidos / ésteres aromáticos (COOH/COOMe) hunden CB1 en Vina estático → **prohibido** -COOH libre en Batch 3.
- Volumen 1′ Et/cPr no ayudó → **mantener 1′-Me**; no escalar más volumen en 1′.
- H1×H2 falló por polaridad en anillo A → periferia vía motivos **menos ácidos** (éteres, F, bioisósteros de fenol).

## Estrategia

1. **Cadena lipofílica / bioisósteros no polares** con 1′-Me fijo — extremos ω-modificados sin ácido libre.
2. **Periferia / TPSA** — éteres pequeños, F estratégico, o bioisósteros de fenol; **sin** ácidos libres que penalicen el bolsillo CB1.

## Placeholders de diseño (IDs conceptuales; sin estructuras)

| ID conceptual | Dirección (sin SMILES) |
|---------------|------------------------|
| JANUS_H1_02a | Cadena ω-F (extremo lipofílico fluorado) |
| JANUS_H1_02b | Éter pequeño en periferia (TPSA suave) |
| JANUS_H1_02c | Bioisóstero no polar de extremo de cadena |
| JANUS_H1_02d | F estratégico (anillo o cadena; no ácido) |
| JANUS_H1_02e | Bioisóstero de fenol (evitar -COOH) |

IDs finales y panel local se fijarán al generar el CSV gitignored; este documento no contiene estructuras.

## Fuera de alcance (este plan)

- No reabrir híbridos H1×H2 con COOH/COOMe aromático.
- No escalar 1′ a Et/cPr u homólogos mayores como eje principal.
- No docking Batch 3 hasta que el usuario lo pida explícitamente.

## IP

- CSV/SDF/PDBQT de candidatos: gitignored (`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- Informes públicos: IDs + scores + lecciones — **sin SMILES**.
