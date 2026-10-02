# Target prep + redocking QC

Generado: 2026-08-18 09:07 UTC

## Receptores y ligandos de referencia

### cb1_5tgz (5TGZ)
- Receptor: `C:\Users\juanc\projects\janusforge\data\targets\cb1\cb1_5tgz_clean.pdbqt`
- Cadenas: ['A']
- Ligando caja: ZDG (33 át.)
- Grid: `configs/grid_cb1_5tgz.txt`
- Centro (Å): (43.638, 27.47, 318.531)
- Tamaño (Å): 20.0 × 20.0 × 20.0

### cb2_6pt0 (6PT0)
- Receptor: `C:\Users\juanc\projects\janusforge\data\targets\cb2\cb2_6pt0_clean.pdbqt`
- Cadenas: ['R']
- Ligando caja: WI5 (32 át.)
- Grid: `configs/grid_cb2_6pt0.txt`
- Centro (Å): (98.379, 109.559, 123.801)
- Tamaño (Å): 20.0 × 20.0 × 20.0

### cb2_6kpc (6KPC)
- Receptor: `C:\Users\juanc\projects\janusforge\data\targets\cb2\cb2_6kpc_clean.pdbqt`
- Cadenas: ['A']
- Ligando caja: E3R (29 át.)
- Grid: `configs/grid_cb2_6kpc.txt`
- Centro (Å): (10.524, 1.258, -45.17)
- Tamaño (Å): 20.0 × 20.0 × 20.0

## Ligandos de referencia (PDBQT)

- **apd371** (8GUQ): `C:\Users\juanc\projects\janusforge\data\targets\cb2\apd371_ref.pdbqt`
  - Nota: APD371/Olorinab extraído de 8GUQ (6KPC contiene agonista E3R, no APD371)

## Notas estructurales

- **6KPC_ligand**: E3R (agonista cristal); APD371 proviene de 8GUQ (KNF)
- **6PT0_chains**: Solo cadena R (CNR2); Gi/Nb35 excluidos
- **5TGZ_chains**: Cadena A (CNR1 chimera)

## Redocking QC (criterio RMSD < 2.0 Å)

- Vina: `C:\Users\juanc\projects\molforge\tools\vina.exe`
- exhaustiveness=8 seed=42

| Sistema | RMSD (Å) | Affinity (kcal/mol) | PASS (<2Å) |
|---------|----------|---------------------|------------|
| AM6538_5TGZ | 0.429 | -11.307 | PASS |
| WIN55212_6PT0 | 0.468 | -12.007 | PASS |

**Resultado global**: PASS
