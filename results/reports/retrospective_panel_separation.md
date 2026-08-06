# Validación retrospectiva — panel quimioma (11 compuestos)

> **Aviso científico:** AutoDock Vina reporta un **proxy de afinidad/pose** (kcal/mol; más negativo ≈ mejor ocupación del pocket). **No** demuestra agonismo vs antagonismo, ni el flip CB1 de THCV, ni eficacia antifibrótica. Ver [`docs/criterio_exito_janus.md`](../../docs/criterio_exito_janus.md) (anti-criterio: score alto sin coherencia funcional).

- Fecha análisis: 2026-08-06
- Scores: `results/docking/retrospective_panel/retrospective_scores.csv`
- Receptores: CB1 **5TGZ** (estado antagonista/inactivo); CB2 **6PT0** (agonista/activo)
- Exhaustiveness: **8**; seed: **42**; pH ligandos: **7.4**
- Cajas: centro = centroide del ligando co-cristalizado (ver `data/targets/*/box.json`)
- Protonación: fenoles neutros; dimorphite-dl solo para ácidos carboxílicos (THCVA)

## Tabla de scores

| Compuesto | role | CB1 Vina | CB2 Vina | Dual mean |
|-----------|------|----------|----------|-----------|
| URB447 (URB447) | design_comparator | -9.543 | -11.703 | -10.623 |
| THCV (delta9-THCV) | seed | -9.006 | -9.902 | -9.454 |
| CBN (CBN) | control | -8.867 | -9.855 | -9.361 |
| THC (delta9-THC) | anti_seed | -8.426 | -10.077 | -9.252 |
| THCVA (THCVA) | interesting | -7.892 | -10.460 | -9.176 |
| THCP (delta9-THCP) | anti_seed | -8.278 | -9.972 | -9.125 |
| CBC (CBC) | control | -8.967 | -9.011 | -8.989 |
| CBDV (CBDV) | secondary | -9.084 | -8.877 | -8.980 |
| CBDB / cannabidibutol (CBD-C4) | interesting | -7.769 | -9.165 | -8.467 |
| CBD (CBD) | control | -7.279 | -9.330 | -8.305 |
| CBG (CBG) | control | -8.011 | -8.282 | -8.146 |

## Foco: semillas Janus vs anti-semillas

| Grupo | n | CB1 mean | CB2 mean | Dual mean |
|-------|---|----------|----------|-----------|
| seed + design_comparator | 2 | -9.274 | -10.802 | -10.038 |
| anti_seed | 2 | -8.352 | -10.024 | -9.188 |

### Spotlight

| Ligando | role | CB1 | CB2 | Dual |
|---------|------|-----|-----|------|
| THCV | seed | -9.006 | -9.902 | -9.454 |
| URB447 | design_comparator | -9.543 | -11.703 | -10.623 |
| THC | anti_seed | -8.426 | -10.077 | -9.252 |
| THCP | anti_seed | -8.278 | -9.972 | -9.125 |

## ¿Hay separación según el criterio operativo?

- **Separación favorable seed/URB447 vs anti-semillas (dual mean):** SÍ (favorable por afinidad proxy)
- Gap dual (Janus − anti): `-0.850` kcal/mol (negativo = Janus mejor afinidad proxy)
- Gap CB1: `-0.922`; gap CB2: `-0.778`

**Lectura:** URB447/THCV muestran afinidad proxy dual media más favorable (más negativa) que las anti-semillas (Δ≥0.25 kcal/mol). Matiz: el gap grupal lo empuja sobre todo URB447; THCV vs THC en dual es solo -0.203 kcal/mol (poca separación scaffold-scaffold).

### Relación con `criterio_exito_janus.md`

- Gates 1–3 (flip CB1, CB2 ago, anti-semilla) son **funcionales / SAR**, no de Vina.
- Este panel solo pregunta si el **mapa de roles del CSV** se refleja en rankings de afinidad proxy en bolsillos antagonista (CB1) y agonista (CB2).
- Un score Vina fuerte de THC/THCP **no** las convierte en hits Janus (anti-criterio explícito del documento de éxito).

## Ranking dual (mejor → peor afinidad proxy)

1. **URB447** (`design_comparator`) dual=-10.623 (CB1=-9.543, CB2=-11.703)
2. **THCV** (`seed`) dual=-9.454 (CB1=-9.006, CB2=-9.902)
3. **CBN** (`control`) dual=-9.361 (CB1=-8.867, CB2=-9.855)
4. **THC** (`anti_seed`) dual=-9.252 (CB1=-8.426, CB2=-10.077)
5. **THCVA** (`interesting`) dual=-9.176 (CB1=-7.892, CB2=-10.460)
6. **THCP** (`anti_seed`) dual=-9.125 (CB1=-8.278, CB2=-9.972)
7. **CBC** (`control`) dual=-8.989 (CB1=-8.967, CB2=-9.011)
8. **CBDV** (`secondary`) dual=-8.980 (CB1=-9.084, CB2=-8.877)
9. **CBDB / cannabidibutol** (`interesting`) dual=-8.467 (CB1=-7.769, CB2=-9.165)
10. **CBD** (`control`) dual=-8.305 (CB1=-7.279, CB2=-9.330)
11. **CBG** (`control`) dual=-8.146 (CB1=-8.011, CB2=-8.282)

## Archivos

- Ligandos: `data/processed/panel_ligands/`
- Receptores / boxes: `data/targets/cb1/`, `data/targets/cb2/`
- Poses: `results/docking/retrospective_panel/`
- Stats JSON: `results/hits/retrospective_panel_stats.json`

