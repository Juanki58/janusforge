# Batch 3 — plan de refino JANUS_H1_02 (público)

> **No SMILES.** Solo IDs conceptuales y dirección de diseño.  
> Vina = afinidad/pose proxy — no éxito Janus funcional ([`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md)).  
> Historial: [`h1_h5_design_history.md`](h1_h5_design_history.md).  
> Gate ejecutado: [`h1_h5_batch3_gate_summary.md`](h1_h5_batch3_gate_summary.md).

- Estado: **ejecutado** (exh=12, seed=42; 5/7 PASS proxy)
- Scaffold base: **JANUS_H1_02** (1′-metilo; control del batch + único PASS Batch 1)
- Objetivo proxy (aspiracional): amplificar gap vs THC hacia **>0.80** kcal/mol — **alcanzado en JANUS_H1_02c** (0.856) en este run

## Lecciones que anclan el plan

- Ácidos / ésteres aromáticos (COOH/COOMe) hunden CB1 en Vina estático → **prohibido** -COOH libre en Batch 3.
- Volumen 1′ Et/cPr no ayudó → **mantener 1′-Me**; no escalar más volumen en 1′.
- H1×H2 falló por polaridad en anillo A → periferia vía motivos **menos ácidos** (éteres, F, bioisósteros de fenol).

## Estrategia

1. **Cadena lipofílica / bioisósteros no polares** con 1′-Me fijo — extremos ω-modificados sin ácido libre.
2. **Periferia / TPSA** — éteres pequeños, F estratégico, o bioisósteros de fenol; **sin** ácidos libres que penalicen el bolsillo CB1.

## Placeholders → IDs del panel local

| ID | Dirección (sin SMILES) | Gate |
|----|------------------------|------|
| JANUS_H1_02 | Control 1′-Me (Batch 1) | PASS |
| JANUS_H1_02a | Cadena ω-F | PASS |
| JANUS_H1_02b | Éter pequeño (fenol→OMe) | fail |
| JANUS_H1_02c | Bioisóstero no polar de extremo de cadena | PASS (+aspiración >0.80) |
| JANUS_H1_02d | F estratégico en rama 1′ | PASS |
| JANUS_H1_02e | Bioisóstero de fenol (OEt) | fail |
| JANUS_H1_02f | Homólogo corto con 1′-Me | PASS |

## Fuera de alcance (este plan)

- No reabrir híbridos H1×H2 con COOH/COOMe aromático.
- No escalar 1′ a Et/cPr u homólogos mayores como eje principal.

## IP

- CSV/SDF/PDBQT de candidatos: gitignored (`data/libraries/h1_h5*`, `results/docking/h1_h5*`, `results/hits/h1_h5*`).
- Informes públicos: IDs + scores + lecciones — **sin SMILES**.
