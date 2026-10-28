# Paso 0E — Preparación PDBQT Qiu 2023 (compuestos 14, 15, 20, 24)

> Estricto: **solo** PDBQT / 3D prep. Sin Vina, sin receptor, sin grids, sin docking.
> Conectividad = 0D PASS (`results/reports/qiu_0d_structure_verification.md`).
> Fecha: 2026-08-11.

## Estado global

**0E = PASS 4/4**

## Método

1. Import SMILES exactos 0D (RDKit `MolFromSmiles`).
2. Verify: canonical SMILES self-consistent + InChI match to 0D table.
3. Embed 3D: ETKDGv3 + MMFF (fallback UFF) — coordenadas only; sin cambiar conectividad/tautómero.
4. Protonación: ruta janusforge `prepare_ligands.smiles_to_pdbqt` / Meeko `MoleculePreparation` + `PDBQTWriterLegacy`. Sin ácido carboxílico → **sin dimorphite**; aminas terciarias (morfolina / N-metilpiperazina) **neutras como dibujadas** a pH 7.4 (carga formal total 0).
5. PDBQT independientes bajo `results/docking/qiu_0e/`.
6. QC: reload PDBQT, contar ATOM/HETATM, residue names, basename → compound ID.

Script: `scripts/prepare_qiu_0e_pdbqt.py`

## Tabla 0E

| Compound | input SMILES | protonation | total charge | n_atoms | pdbqt path | QC OK |
|----------|--------------|-------------|--------------|---------|------------|-------|
| 14 | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` | neutral as drawn (no dimorphite; tertiary amines) | 0 | 38 | `results/docking/qiu_0e/compound_14_lig.pdbqt` | **YES** |
| 15 | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2cccc(N3CCOCC3)c2)c1-c1ccccc1` | neutral as drawn (no dimorphite; tertiary amines) | 0 | 38 | `results/docking/qiu_0e/compound_15_lig.pdbqt` | **YES** |
| 20 | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCN(C)CC2)c1-c1ccccc1` | neutral as drawn (no dimorphite; tertiary amines) | 0 | 39 | `results/docking/qiu_0e/compound_20_lig.pdbqt` | **YES** |
| 24 | `Cc1c(C(=O)NCC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` | neutral as drawn (no dimorphite; tertiary amines) | 0 | 39 | `results/docking/qiu_0e/compound_24_lig.pdbqt` | **YES** |

## Detalle QC / protonación

### Compound 14 (`compound_14`)

- 0D InChI match: YES
- Protonation tag: `rdkit_neutral_phenol_ok_ph7.4`
- Note: rdkit_neutral_phenol_ok_ph7.4; keep as drawn (neutral tertiary amines); o-morpholine tertiary amine; neutral as drawn (pKa conj. acid ~8); dimorphite=N/A (no COOH)
- Formal charge (post-prep SMILES): 0
- Meeko partial-charge sum: 0.002
- n_heavy (2D): 37; n_atoms PDBQT (H included): 38
- Residue names in PDBQT: UNL
- SDF intermediate: `results/docking/qiu_0e/compound_14_lig.sdf`
- QC OK: YES

### Compound 15 (`compound_15`)

- 0D InChI match: YES
- Protonation tag: `rdkit_neutral_phenol_ok_ph7.4`
- Note: rdkit_neutral_phenol_ok_ph7.4; keep as drawn (neutral tertiary amines); m-morpholine tertiary amine; neutral as drawn; dimorphite=N/A (no COOH)
- Formal charge (post-prep SMILES): 0
- Meeko partial-charge sum: 0.002
- n_heavy (2D): 37; n_atoms PDBQT (H included): 38
- Residue names in PDBQT: UNL
- SDF intermediate: `results/docking/qiu_0e/compound_15_lig.sdf`
- QC OK: YES

### Compound 20 (`compound_20`)

- 0D InChI match: YES
- Protonation tag: `rdkit_neutral_phenol_ok_ph7.4`
- Note: rdkit_neutral_phenol_ok_ph7.4; keep as drawn (neutral tertiary amines); o-(4-methylpiperazine); N-Me + aniline-N kept neutral as drawn; dimorphite=N/A (no COOH)
- Formal charge (post-prep SMILES): 0
- Meeko partial-charge sum: 0.002
- n_heavy (2D): 38; n_atoms PDBQT (H included): 39
- Residue names in PDBQT: UNL
- SDF intermediate: `results/docking/qiu_0e/compound_20_lig.sdf`
- QC OK: YES

### Compound 24 (`compound_24`)

- 0D InChI match: YES
- Protonation tag: `rdkit_neutral_phenol_ok_ph7.4`
- Note: rdkit_neutral_phenol_ok_ph7.4; keep as drawn (neutral tertiary amines); o-morpholine + adamantylmethyl amide; neutral as drawn; dimorphite=N/A (no COOH)
- Formal charge (post-prep SMILES): 0
- Meeko partial-charge sum: -0.0
- n_heavy (2D): 38; n_atoms PDBQT (H included): 39
- Residue names in PDBQT: UNL
- SDF intermediate: `results/docking/qiu_0e/compound_24_lig.sdf`
- QC OK: YES

## Artefactos

- PDBQT / SDF: `results/docking/qiu_0e/` (gitignored `*.pdbqt`; SDF local).
- Meta JSON: `results/docking/qiu_0e/qiu_0e_meta.json` (local).
- Report (público): este archivo.

## Notas

- SMILES públicos (publicados Qiu 2023 / verificados en 0D).
- Piperazina/morfolina: a pH fisiológico una fracción puede estar protonada; aquí se conserva la forma **neutra dibujada** (consistente con 0D y con `prepare_ligands` sin COOH → sin dimorphite).
- Sin docking en este paso.
