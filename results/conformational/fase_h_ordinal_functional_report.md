# Phase H — Auditoría funcional (H0) y separación ordinal (H1)

**Generado:** 2026-08-19T10:22:01.666297+00:00  
**Rama:** `feat/fase-h-conformational-functional-correlation`

## Gobernanza

```yaml
PHASE_H: ORDINAL_FUNCTIONAL_SEPARATION
CONTRACT_v1.0: FROZEN
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ALLOSTERIC_FRAMEWORK: HYPOTHESIS_PENDING_CALIBRATION
H0_BEFORE_H1: mandatory
FORBIDDEN_PATHWAYS: beta_arrestin, ERK_phosphorylation
```

## H0 — ¿Tenemos datos Gi comparables?

**Respuesta:** **Sí** (parcial)

Soethoudt et al. 2017 (Nat Commun; DOI 10.1038/ncomms13958) provides a unified hCB2 CHO panel with explicit CP55940 normalization in both cAMP (Suppl. Table 4) and GTPgammaS (Suppl. Table 3). Hanus 1999 adds independent HU-308 cAMP on hCB2 CHO. Ordinal tiers are assay-dependent: cAMP lacks a clean PARTIAL tier; GTPgammaS supports TOTAL / PARTIAL / INVERSE separation among five compounds. HU-433 lacks comparable hCB2 Gi row with CP55940 reference in recovered primaries.

- Mejor ensayo para ordinal: **GTPgammaS**
- Compuestos elegibles ordinal: CP-55,940, HU-308, WIN55,212-2, JWH-133, SR144528

### Tabla H0 (filas auditadas)

| Compuesto | Ensayo | Ref. | Emax % | Clase | Comparabilidad | DOI/PMID |
|-----------|--------|------|--------|-------|----------------|----------|
| CP-55,940 | cAMP_inhibition | CP55,940 | 98 | TOTAL | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| CP-55,940 | GTPgammaS | CP55,940 | 95 | TOTAL | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| WIN55,212-2 | cAMP_inhibition | CP55,940 | 98 | PROTEAN_OR_SYSTEM_DEPENDENT | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| WIN55,212-2 | GTPgammaS | CP55,940 | 49 | PARTIAL | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| JWH-133 | cAMP_inhibition | CP55,940 | 98 | PROTEAN_OR_SYSTEM_DEPENDENT | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| JWH-133 | GTPgammaS | CP55,940 | 61 | PARTIAL | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| HU-308 | cAMP_inhibition | CP55,940 | 98 | TOTAL | LEVEL_0_MODERATE | 10.1038/ncomms13958 |
| HU-308 | cAMP_inhibition | CP55,940 | 108.6 | TOTAL | LEVEL_0_MODERATE | 10.1073/pnas.96.25.14228 |
| HU-308 | GTPgammaS | CP55,940 | 97 | TOTAL | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| HU-433 | cAMP_inhibition | CP55,940 | null | INDETERMINATE | INDETERMINATE | 10.1073/pnas.1503395112 |
| Delta9-THCV | GTPgammaS | CP55,940 | null | INDETERMINATE | INDETERMINATE | 10.1038/sj.bjp.0707442 |
| SR144528 | cAMP_inhibition | CP55,940 | -151 | INVERSE | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| SR144528 | GTPgammaS | CP55,940 | -29 | INVERSE | LEVEL_0_HIGH | 10.1038/ncomms13958 |
| AM630 | cAMP_inhibition | CP55,940 | -152 | PROTEAN_OR_SYSTEM_DEPENDENT | LEVEL_0_MODERATE | 10.1038/ncomms13958 |
| AM630 | GTPgammaS | CP55,940 | -22 | PROTEAN_OR_SYSTEM_DEPENDENT | LEVEL_0_MODERATE | 10.1038/ncomms13958 |

**Cautelas PI:** AM630 → PROTEAN (no INVERSE automático). THCV → INDETERMINATE (no intermediario ordinal forzado). HU-308/HU-433 → caso pareado, no misma clase.

## H1 — Proyección conformacional

Receptor-state fingerprint distance to active centroid (6PT0+6KPF). Ligand projection = distance of multistate-docking preferred receptor state to that centroid — NOT ligand pose fingerprint, NOT Vina score as Gi Emax.

- Centroide activo: **6PT0 + 6KPF**
- SHA256 Phase F matrix: `29d516e521f9f5f0ac39865c83449228d8a33114a1a29de464136c6618c61e4a`
- SHA256 Phase G report: `36c493ea5ea903d2fe39c1b6254f6d546e8ea823e32614711947e85ee07b6efd`

### Distancias por compuesto (Phase F normalizado)

| Compuesto | Estado preferido | Distancia | Proyección definida |
|-----------|------------------|-----------|---------------------|
| AM630 | — | — | no |
| CP-55,940 | — | — | no |
| Delta9-THCV | 6PT0 | 1.7646 | sí |
| HU-308 | 6PT0 | 1.7646 | sí |
| HU-433 | 6PT0 | 1.7646 | sí |
| JWH-133 | — | — | no |
| SR144528 | — | — | no |
| WIN55,212-2 | — | — | no |

## Caso prioritario — par HU-308 ↔ HU-433

- Relación: C3/C1 stereoisomers (enantiomeric pair)
- Ki literatura: HU-308 22.7±3.9 (Hanus 1999); HU-433 12.2 (patent US20110269842A1; higher affinity)
- Docking 6PT0 Δscore: -0.4 kcal/mol; ΔTrp258: 1.32 Å
- Identical receptor-state centroid distance for both ligands (pose selects same PDB state), yet pose-conditioned microswitch contacts differ (Trp258 5.15 vs 6.47 Å) and literature reports affinity vs Gi efficacy dissociation. Supports orientation/conformation mechanism over simple 'distance = Emax' ordinal.

## Veredicto H1

### ⚪ INDETERMINATE (Blanco)

Insufficient ligands with both comparable Gi tier and defined conformational projection (1 projections across 1 tiers; need ≥3 projections spanning TOTAL/PARTIAL/INVERSE).

### Limitaciones explícitas

- Proyección = estado receptor preferido por docking multistate; **no** equivalencia Vina ↔ Gi Emax.
- Ensayo funcional y expresión celular no entran en la coordenada estructural.
- β-arrestin / ERK **prohibidos** como proxy de clase Gi.

## Integridad (SHA256)

| Artefacto | SHA256 |
|-----------|--------|
| H0 JSON | `05f215e243dca61bfb46ea2338eddacce8ca1d939da6c6e34814e42526ffce27` |
| Phase F matrix | `29d516e521f9f5f0ac39865c83449228d8a33114a1a29de464136c6618c61e4a` |
| Phase G report | `36c493ea5ea903d2fe39c1b6254f6d546e8ea823e32614711947e85ee07b6efd` |
| Este reporte JSON | `f414257c326f6b19b592df42607fbac9681181e579e6fa0dc071e06cb6929616` |
