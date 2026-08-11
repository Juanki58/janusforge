# AUDITORÍA 0E — Verificación bruta PDBQT (Qiu 14/15/20/24)

> Read-only. Sin docking, sin receptor prep, sin modificar/sobrescribir/generar PDBQT.
> Fecha: 2026-08-11.
> Fuentes brutas: `results/docking/qiu_0e/compound_{14,15,20,24}_lig.pdbqt`
> Referencia (no verdad sobre el archivo): `qiu_0e_pdbqt_preparation.md`, `qiu_0d_structure_verification.md`, `scripts/prepare_qiu_0e_pdbqt.py`
> Herramientas: lectura directa de líneas + RDKit 2025.09.6 + Meeko 0.7.1 (`PDBQTMolecule` → `RDKitMolCreate`). Open Babel no instalado.

## D) Veredicto final

**0E = PASS 4/4**

---

## A) QC table (14 / 15 / 20 / 24)

| Cpd | n_atoms | Elements (counts) | AD types | Σ q (partial) | TORSDOF | ROOT/BRANCH | SMILES exact vs 0D | Heavy atoms vs 0D | Formula 0D | Meeko connectivity InChIKey | Chemotype | Coords | QC |
|-----|---------|-------------------|----------|---------------|---------|-------------|--------------------|-------------------|------------|------------------------------|-----------|--------|-----|
| 14 | 38 | C31 H1 N4 O2 | A15 C16 HD1 N3 NA1 OA2 | +0.002 | 5 | YES (3 BRANCH) | EXACT | 37 = 37 | C31H36N4O2 | QQXQVTJJXRACOB (match; stereo layer differs) | PASS o-morph + CONH-Ad | OK | **PASS** |
| 15 | 38 | C31 H1 N4 O2 | A15 C16 HD1 N3 NA1 OA2 | +0.002 | 5 | YES (3 BRANCH) | EXACT | 37 = 37 | C31H36N4O2 | ZVVBFOFPAAUAGH (match; stereo layer differs) | PASS m-morph + CONH-Ad | OK | **PASS** |
| 20 | 39 | C32 H1 N5 O1 | A15 C17 HD1 N3 NA2 OA1 | +0.002 | 5 | YES (3 BRANCH) | EXACT | 38 = 38 | C32H39N5O | ZWCGYXUFIUXGBQ (match; stereo layer differs) | PASS o-Me-pip + CONH-Ad | OK | **PASS** |
| 24 | 39 | C32 H1 N4 O2 | A15 C17 HD1 N3 NA1 OA2 | 0.000 | 6 | YES (4 BRANCH) | EXACT | 38 = 38 | C32H38N4O2 | RAQAMHLYXWAFRF (match; stereo layer differs) | PASS o-morph + CONH-CH2-Ad | OK | **PASS** |

### QC notes (all four)

- **Partial charges:** all finite; no missing charge/type; \|q\| ≤ 0.378; Σq ≈ 0 (neutral Meeko Gasteiger). No suspicious charges/types.
- **Connectivity in PDBQT:** Meeko torsion tree only (`ROOT`/`ENDROOT`/`BRANCH`/`ENDBRANCH`); no `CONECT` records.
- **H content:** PDBQT stores **heavy atoms + polar H only** (1× `HD` amide). Nonpolar H absent — expected for Meeko PDBQT. Element tally therefore shows H1, not full molecular H.
- **Coordinates (fixed PDB columns 31–54):** finite; no NaN/Inf; no exact duplicate XYZ; \|coord\|max ≈ 6.3–6.7 Å (reasonable ligand embedding).
- **SMILES:** `REMARK SMILES` in each file == script `COMPOUNDS[].smiles` == exact 0D SMILES (character-identical).
- **Identity method:** (1) exact REMARK SMILES vs 0D; (2) Meeko PDBQT→RDKit → heavy-atom InChI. Full InChIKey differs only in stereo block (`UHFFFAOYSA-N` in 0D vs absolute stereo assigned from 3D coords, e.g. `HTTPIDPASA-N` / `SQHSIVEPSA-N`). **Connectivity layer (first InChIKey block) matches 0D.** Meeko also regenerates the same canonical SMILES as 0D. PDBQT→mol is partially lossy on bond-order inference and H; connectivity + formula verified.

### Chemotype checks (PASS/FAIL)

| Cpd | Required | Result | Evidence |
|-----|----------|--------|----------|
| 14 | o-morpholine + CONH-adamantane (no CH2) | **PASS** | SMARTS `n-c1ccccc1-N1CCOCC1` True; `C(=O)NC12CC3CC(CC(C3)C1)C2` True; `C(=O)NCC12…` False; meta-morph False; Me-piperazine False |
| 15 | m-morpholine + CONH-adamantane | **PASS** | SMARTS `n-c1cccc(N2CCOCC2)c1` True; ortho-morph False; CONH-Ad True; CONH-CH2-Ad False |
| 20 | o-(4-methylpiperazinyl) + CONH-adamantane | **PASS** | SMARTS `n-c1ccccc1-N1CCN(C)CC1` True; morpholine False; CONH-Ad True; CONH-CH2-Ad False |
| 24 | o-morpholine + CONH-CH2-adamantane | **PASS** | ortho-morph True; `C(=O)NCC12CC3CC(CC(C3)C1)C2` True; direct CONH-Ad False |

---

## B) Raw PDBQT data (full ATOM/HETATM + tree headers)

### Compound 14 — `results/docking/qiu_0e/compound_14_lig.pdbqt`

**REMARK SMILES (exact):** `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1`

**Summary:** n=38; elements C31/H1/N4/O2; AD A15/C16/HD1/N3/NA1/OA2; Σq=+0.002; TORSDOF=5; XYZ ranges x∈[-5.558,6.681], y∈[-3.664,2.633], z∈[-3.932,2.499]

```
ROOT
ATOM      1  C   UNL     1      -0.190  -2.706   2.055  1.00  0.00     0.049 C 
ATOM      2  C   UNL     1      -0.481  -1.765   0.940  1.00  0.00     0.009 A 
ATOM      3  C   UNL     1       0.463  -0.926   0.285  1.00  0.00     0.154 A 
ATOM      4  N   UNL     1      -0.096  -0.276  -0.750  1.00  0.00    -0.162 NA
ATOM      5  N   UNL     1      -1.423  -0.571  -0.680  1.00  0.00    -0.230 N 
ATOM      6  C   UNL     1      -1.687  -1.549   0.279  1.00  0.00     0.078 A 
ENDROOT
BRANCH   3   7
ATOM      7  C   UNL     1       1.897  -0.748   0.595  1.00  0.00     0.272 C 
ATOM      8  O   UNL     1       2.459  -1.325   1.519  1.00  0.00    -0.267 OA
ATOM      9  N   UNL     1       2.514   0.140  -0.260  1.00  0.00    -0.345 N 
ATOM     10  H   UNL     1       1.897   0.509  -0.980  1.00  0.00     0.164 HD
BRANCH   9  11
ATOM     11  C   UNL     1       3.922   0.521  -0.242  1.00  0.00     0.041 C 
ATOM     12  C   UNL     1       4.319   1.185   1.100  1.00  0.00     0.032 C 
ATOM     13  C   UNL     1       4.167   1.553  -1.375  1.00  0.00     0.032 C 
ATOM     14  C   UNL     1       4.844  -0.696  -0.496  1.00  0.00     0.032 C 
ATOM     15  C   UNL     1       5.795   1.619   1.074  1.00  0.00    -0.008 C 
ATOM     16  C   UNL     1       5.639   1.994  -1.410  1.00  0.00    -0.008 C 
ATOM     17  C   UNL     1       6.320  -0.262  -0.523  1.00  0.00    -0.008 C 
ATOM     18  C   UNL     1       6.681   0.386   0.825  1.00  0.00     0.007 C 
ATOM     19  C   UNL     1       6.006   2.633  -0.062  1.00  0.00     0.007 C 
ATOM     20  C   UNL     1       6.528   0.763  -1.650  1.00  0.00     0.007 C 
ENDBRANCH   9  11
ENDBRANCH   3   7
BRANCH   6  21
ATOM     21  C   UNL     1      -2.964  -2.258   0.444  1.00  0.00     0.001 A 
ATOM     22  C   UNL     1      -3.565  -2.354   1.706  1.00  0.00     0.010 A 
ATOM     23  C   UNL     1      -3.581  -2.890  -0.644  1.00  0.00     0.010 A 
ATOM     24  C   UNL     1      -4.764  -3.052   1.876  1.00  0.00     0.001 A 
ATOM     25  C   UNL     1      -4.783  -3.584  -0.476  1.00  0.00     0.001 A 
ATOM     26  C   UNL     1      -5.373  -3.664   0.783  1.00  0.00     0.000 A 
ENDBRANCH   6  21
BRANCH   5  27
ATOM     27  C   UNL     1      -2.303   0.072  -1.597  1.00  0.00     0.089 A 
ATOM     28  C   UNL     1      -1.851   0.162  -2.932  1.00  0.00     0.030 A 
ATOM     29  C   UNL     1      -3.579   0.554  -1.223  1.00  0.00     0.063 A 
ATOM     30  C   UNL     1      -2.692   0.635  -3.932  1.00  0.00     0.002 A 
ATOM     31  C   UNL     1      -4.413   0.988  -2.273  1.00  0.00     0.028 A 
ATOM     32  C   UNL     1      -3.981   1.027  -3.605  1.00  0.00     0.002 A 
BRANCH  29  33
ATOM     33  N   UNL     1      -3.978   0.697   0.109  1.00  0.00    -0.365 N 
ATOM     34  C   UNL     1      -3.107   1.524   0.978  1.00  0.00     0.145 C 
ATOM     35  C   UNL     1      -5.408   0.734   0.467  1.00  0.00     0.145 C 
ATOM     36  C   UNL     1      -3.925   2.617   1.687  1.00  0.00     0.181 C 
ATOM     37  C   UNL     1      -5.558   0.886   1.989  1.00  0.00     0.181 C 
ATOM     38  O   UNL     1      -4.994   2.107   2.499  1.00  0.00    -0.378 OA
ENDBRANCH  29  33
ENDBRANCH   5  27
TORSDOF 5
```

**Partial charges (atom serial → q):** 1:0.049, 2:0.009, 3:0.154, 4:-0.162, 5:-0.230, 6:0.078, 7:0.272, 8:-0.267, 9:-0.345, 10:0.164, 11:0.041, 12:0.032, 13:0.032, 14:0.032, 15:-0.008, 16:-0.008, 17:-0.008, 18:0.007, 19:0.007, 20:0.007, 21:0.001, 22:0.010, 23:0.010, 24:0.001, 25:0.001, 26:0.000, 27:0.089, 28:0.030, 29:0.063, 30:0.002, 31:0.028, 32:0.002, 33:-0.365, 34:0.145, 35:0.145, 36:0.181, 37:0.181, 38:-0.378

**Meeko→RDKit:** SMILES = 0D; formula C31H36N4O2; formal charge 0; InChI connectivity = 0D; stereo layer `/t22-,23+,24-,31-` added from coords.

---

### Compound 15 — `results/docking/qiu_0e/compound_15_lig.pdbqt`

**REMARK SMILES (exact):** `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2cccc(N3CCOCC3)c2)c1-c1ccccc1`

**Summary:** n=38; elements C31/H1/N4/O2; AD A15/C16/HD1/N3/NA1/OA2; Σq=+0.002; TORSDOF=5; XYZ ranges x∈[-5.062,6.334], y∈[-6.196,5.003], z∈[-3.030,2.504]

```
ROOT
ATOM      1  C   UNL     1       1.165  -4.046  -1.754  1.00  0.00     0.049 C 
ATOM      2  C   UNL     1       0.311  -2.983  -1.157  1.00  0.00     0.009 A 
ATOM      3  C   UNL     1       0.756  -1.731  -0.662  1.00  0.00     0.154 A 
ATOM      4  N   UNL     1      -0.276  -0.977  -0.247  1.00  0.00    -0.162 NA
ATOM      5  N   UNL     1      -1.386  -1.754  -0.391  1.00  0.00    -0.232 N 
ATOM      6  C   UNL     1      -1.071  -2.972  -0.998  1.00  0.00     0.078 A 
ENDROOT
BRANCH   3   7
ATOM      7  C   UNL     1       2.140  -1.218  -0.594  1.00  0.00     0.272 C 
ATOM      8  O   UNL     1       3.106  -1.848  -1.009  1.00  0.00    -0.267 OA
ATOM      9  N   UNL     1       2.213   0.032  -0.018  1.00  0.00    -0.345 N 
ATOM     10  H   UNL     1       1.308   0.412   0.252  1.00  0.00     0.164 HD
BRANCH   9  11
ATOM     11  C   UNL     1       3.422   0.826   0.168  1.00  0.00     0.041 C 
ATOM     12  C   UNL     1       4.456   0.096   1.062  1.00  0.00     0.032 C 
ATOM     13  C   UNL     1       3.038   2.155   0.872  1.00  0.00     0.032 C 
ATOM     14  C   UNL     1       4.083   1.178  -1.188  1.00  0.00     0.032 C 
ATOM     15  C   UNL     1       5.702   0.974   1.276  1.00  0.00    -0.008 C 
ATOM     16  C   UNL     1       4.276   3.040   1.092  1.00  0.00    -0.008 C 
ATOM     17  C   UNL     1       5.329   2.055  -0.972  1.00  0.00    -0.008 C 
ATOM     18  C   UNL     1       6.334   1.297  -0.088  1.00  0.00     0.007 C 
ATOM     19  C   UNL     1       5.288   2.283   1.967  1.00  0.00     0.007 C 
ATOM     20  C   UNL     1       4.917   3.358  -0.267  1.00  0.00     0.007 C 
ENDBRANCH   9  11
ENDBRANCH   3   7
BRANCH   6  21
ATOM     21  C   UNL     1      -2.019  -3.983  -1.463  1.00  0.00     0.001 A 
ATOM     22  C   UNL     1      -2.097  -5.226  -0.824  1.00  0.00     0.010 A 
ATOM     23  C   UNL     1      -2.830  -3.730  -2.577  1.00  0.00     0.010 A 
ATOM     24  C   UNL     1      -2.993  -6.196  -1.278  1.00  0.00     0.001 A 
ATOM     25  C   UNL     1      -3.724  -4.702  -3.030  1.00  0.00     0.001 A 
ATOM     26  C   UNL     1      -3.807  -5.932  -2.379  1.00  0.00     0.000 A 
ENDBRANCH   6  21
BRANCH   5  27
ATOM     27  C   UNL     1      -2.637  -1.239   0.082  1.00  0.00     0.067 A 
ATOM     28  C   UNL     1      -3.751  -2.049   0.299  1.00  0.00     0.028 A 
ATOM     29  C   UNL     1      -2.739   0.142   0.366  1.00  0.00     0.054 A 
ATOM     30  C   UNL     1      -4.936  -1.486   0.768  1.00  0.00     0.004 A 
ATOM     31  C   UNL     1      -3.924   0.741   0.829  1.00  0.00     0.039 A 
ATOM     32  C   UNL     1      -5.017  -0.114   1.025  1.00  0.00     0.026 A 
BRANCH  31  33
ATOM     33  N   UNL     1      -4.003   2.099   1.078  1.00  0.00    -0.367 N 
ATOM     34  C   UNL     1      -5.062   2.684   1.917  1.00  0.00     0.145 C 
ATOM     35  C   UNL     1      -3.081   3.061   0.451  1.00  0.00     0.145 C 
ATOM     36  C   UNL     1      -4.586   4.024   2.504  1.00  0.00     0.181 C 
ATOM     37  C   UNL     1      -3.770   4.427   0.288  1.00  0.00     0.181 C 
ATOM     38  O   UNL     1      -4.229   5.003   1.518  1.00  0.00    -0.378 OA
ENDBRANCH  31  33
ENDBRANCH   5  27
TORSDOF 5
```

**Partial charges (atom serial → q):** 1:0.049, 2:0.009, 3:0.154, 4:-0.162, 5:-0.232, 6:0.078, 7:0.272, 8:-0.267, 9:-0.345, 10:0.164, 11:0.041, 12:0.032, 13:0.032, 14:0.032, 15:-0.008, 16:-0.008, 17:-0.008, 18:0.007, 19:0.007, 20:0.007, 21:0.001, 22:0.010, 23:0.010, 24:0.001, 25:0.001, 26:0.000, 27:0.067, 28:0.028, 29:0.054, 30:0.004, 31:0.039, 32:0.026, 33:-0.367, 34:0.145, 35:0.145, 36:0.181, 37:0.181, 38:-0.378

**Meeko→RDKit:** SMILES = 0D; formula C31H36N4O2; formal charge 0; connectivity InChIKey ZVVBFOFPAAUAGH matches 0D.

---

### Compound 20 — `results/docking/qiu_0e/compound_20_lig.pdbqt`

**REMARK SMILES (exact):** `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCN(C)CC2)c1-c1ccccc1`

**Summary:** n=39; elements C32/H1/N5/O1; AD A15/C17/HD1/N3/NA2/OA1; Σq=+0.002; TORSDOF=5; XYZ ranges x∈[-6.494,4.620], y∈[-4.185,3.419], z∈[-3.371,4.418]

```
ROOT
ATOM      1  C   UNL     1       2.803  -2.061  -0.570  1.00  0.00     0.089 A 
ATOM      2  C   UNL     1       2.971  -3.445  -0.351  1.00  0.00     0.030 A 
ATOM      3  C   UNL     1       3.879  -4.185  -1.107  1.00  0.00     0.002 A 
ATOM      4  C   UNL     1       4.620  -3.557  -2.097  1.00  0.00     0.002 A 
ATOM      5  C   UNL     1       4.465  -2.187  -2.312  1.00  0.00     0.028 A 
ATOM      6  C   UNL     1       3.577  -1.401  -1.549  1.00  0.00     0.063 A 
ENDROOT
BRANCH   1   7
ATOM      7  N   UNL     1       1.772  -1.399   0.159  1.00  0.00    -0.230 N 
ATOM      8  C   UNL     1       0.245  -0.816   1.673  1.00  0.00     0.009 A 
ATOM      9  C   UNL     1      -0.036  -0.251   0.394  1.00  0.00     0.154 A 
ATOM     10  C   UNL     1       1.400  -1.572   1.494  1.00  0.00     0.078 A 
ATOM     11  N   UNL     1       0.907  -0.588  -0.492  1.00  0.00    -0.162 NA
ATOM     12  C   UNL     1      -0.498  -0.595   2.943  1.00  0.00     0.049 C 
BRANCH   9  13
ATOM     13  C   UNL     1      -1.170   0.607  -0.015  1.00  0.00     0.272 C 
ATOM     14  O   UNL     1      -1.055   1.516  -0.830  1.00  0.00    -0.267 OA
ATOM     15  N   UNL     1      -2.377   0.258   0.571  1.00  0.00    -0.345 N 
ATOM     16  H   UNL     1      -2.404  -0.666   0.978  1.00  0.00     0.164 HD
BRANCH  15  17
ATOM     17  C   UNL     1      -3.666   0.870   0.237  1.00  0.00     0.041 C 
ATOM     18  C   UNL     1      -3.673   2.399   0.493  1.00  0.00     0.032 C 
ATOM     19  C   UNL     1      -4.061   0.598  -1.235  1.00  0.00     0.032 C 
ATOM     20  C   UNL     1      -4.752   0.236   1.150  1.00  0.00     0.032 C 
ATOM     21  C   UNL     1      -5.058   2.994   0.182  1.00  0.00    -0.008 C 
ATOM     22  C   UNL     1      -5.445   1.195  -1.543  1.00  0.00    -0.008 C 
ATOM     23  C   UNL     1      -6.140   0.823   0.848  1.00  0.00    -0.008 C 
ATOM     24  C   UNL     1      -6.109   2.340   1.092  1.00  0.00     0.007 C 
ATOM     25  C   UNL     1      -5.412   2.712  -1.288  1.00  0.00     0.007 C 
ATOM     26  C   UNL     1      -6.494   0.550  -0.622  1.00  0.00     0.007 C 
ENDBRANCH  15  17
ENDBRANCH   9  13
BRANCH  10  27
ATOM     27  C   UNL     1       2.174  -2.309   2.497  1.00  0.00     0.001 A 
ATOM     28  C   UNL     1       3.511  -1.980   2.755  1.00  0.00     0.010 A 
ATOM     29  C   UNL     1       1.577  -3.349   3.223  1.00  0.00     0.010 A 
ATOM     30  C   UNL     1       4.243  -2.690   3.709  1.00  0.00     0.001 A 
ATOM     31  C   UNL     1       2.310  -4.058   4.178  1.00  0.00     0.001 A 
ATOM     32  C   UNL     1       3.643  -3.729   4.418  1.00  0.00     0.000 A 
ENDBRANCH  10  27
ENDBRANCH   1   7
BRANCH   6  33
ATOM     33  N   UNL     1       3.634  -0.031  -1.796  1.00  0.00    -0.367 N 
ATOM     34  C   UNL     1       3.886   0.891  -0.682  1.00  0.00     0.132 C 
ATOM     35  C   UNL     1       2.722   0.471  -2.845  1.00  0.00     0.132 C 
ATOM     36  C   UNL     1       4.300   2.266  -1.262  1.00  0.00     0.105 C 
ATOM     37  C   UNL     1       2.256   1.922  -2.563  1.00  0.00     0.105 C 
ATOM     38  N   UNL     1       3.321   2.884  -2.189  1.00  0.00    -0.303 NA
ATOM     39  C   UNL     1       3.991   3.419  -3.371  1.00  0.00     0.105 C 
ENDBRANCH   6  33
TORSDOF 5
```

**Partial charges (atom serial → q):** 1:0.089, 2:0.030, 3:0.002, 4:0.002, 5:0.028, 6:0.063, 7:-0.230, 8:0.009, 9:0.154, 10:0.078, 11:-0.162, 12:0.049, 13:0.272, 14:-0.267, 15:-0.345, 16:0.164, 17:0.041, 18:0.032, 19:0.032, 20:0.032, 21:-0.008, 22:-0.008, 23:-0.008, 24:0.007, 25:0.007, 26:0.007, 27:0.001, 28:0.010, 29:0.010, 30:0.001, 31:0.001, 32:0.000, 33:-0.367, 34:0.132, 35:0.132, 36:0.105, 37:0.105, 38:-0.303, 39:0.105

**Meeko→RDKit:** SMILES = 0D; formula C32H39N5O; formal charge 0; connectivity InChIKey ZWCGYXUFIUXGBQ matches 0D. Extra N vs 14/15 (piperazine N-Me); one OA (amide carbonyl only).

---

### Compound 24 — `results/docking/qiu_0e/compound_24_lig.pdbqt`

**REMARK SMILES (exact):** `Cc1c(C(=O)NCC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1`

**Summary:** n=39; elements C32/H1/N4/O2; AD A15/C17/HD1/N3/NA1/OA2; Σq=0.000; TORSDOF=6; XYZ ranges x∈[-5.207,6.657], y∈[-4.846,4.201], z∈[-2.816,2.849]

```
ROOT
ATOM      1  C   UNL     1      -0.242  -3.231   1.253  1.00  0.00     0.049 C 
ATOM      2  C   UNL     1      -0.830  -1.958   0.755  1.00  0.00     0.009 A 
ATOM      3  C   UNL     1      -0.329  -0.634   0.936  1.00  0.00     0.154 A 
ATOM      4  N   UNL     1      -1.178   0.267   0.430  1.00  0.00    -0.162 NA
ATOM      5  N   UNL     1      -2.215  -0.429  -0.093  1.00  0.00    -0.230 N 
ATOM      6  C   UNL     1      -2.024  -1.805   0.055  1.00  0.00     0.078 A 
ENDROOT
BRANCH   3   7
ATOM      7  C   UNL     1       0.930  -0.186   1.566  1.00  0.00     0.272 C 
ATOM      8  O   UNL     1       1.033   0.864   2.196  1.00  0.00    -0.267 OA
ATOM      9  N   UNL     1       2.010  -1.024   1.342  1.00  0.00    -0.350 N 
ATOM     10  H   UNL     1       1.893  -1.785   0.689  1.00  0.00     0.163 HD
BRANCH   9  11
ATOM     11  C   UNL     1       3.356  -0.681   1.752  1.00  0.00     0.123 C 
BRANCH  11  12
ATOM     12  C   UNL     1       4.221  -0.084   0.619  1.00  0.00    -0.012 C 
ATOM     13  C   UNL     1       3.639   1.249   0.083  1.00  0.00     0.012 C 
ATOM     14  C   UNL     1       5.643   0.200   1.174  1.00  0.00     0.012 C 
ATOM     15  C   UNL     1       4.356  -1.072  -0.569  1.00  0.00     0.012 C 
ATOM     16  C   UNL     1       4.544   1.840  -1.012  1.00  0.00    -0.010 C 
ATOM     17  C   UNL     1       6.553   0.787   0.082  1.00  0.00    -0.010 C 
ATOM     18  C   UNL     1       5.263  -0.486  -1.666  1.00  0.00    -0.010 C 
ATOM     19  C   UNL     1       4.656   0.834  -2.170  1.00  0.00     0.007 C 
ATOM     20  C   UNL     1       5.943   2.101  -0.431  1.00  0.00     0.007 C 
ATOM     21  C   UNL     1       6.657  -0.213  -1.080  1.00  0.00     0.007 C 
ENDBRANCH  11  12
ENDBRANCH   9  11
ENDBRANCH   3   7
BRANCH   6  22
ATOM     22  C   UNL     1      -2.983  -2.841  -0.337  1.00  0.00     0.001 A 
ATOM     23  C   UNL     1      -4.285  -2.845   0.179  1.00  0.00     0.010 A 
ATOM     24  C   UNL     1      -2.598  -3.854  -1.225  1.00  0.00     0.010 A 
ATOM     25  C   UNL     1      -5.191  -3.837  -0.200  1.00  0.00     0.001 A 
ATOM     26  C   UNL     1      -3.504  -4.846  -1.602  1.00  0.00     0.001 A 
ATOM     27  C   UNL     1      -4.801  -4.836  -1.091  1.00  0.00     0.000 A 
ENDBRANCH   6  22
BRANCH   5  28
ATOM     28  C   UNL     1      -3.237   0.252  -0.822  1.00  0.00     0.089 A 
ATOM     29  C   UNL     1      -3.651  -0.282  -2.058  1.00  0.00     0.030 A 
ATOM     30  C   UNL     1      -3.824   1.442  -0.331  1.00  0.00     0.063 A 
ATOM     31  C   UNL     1      -4.632   0.356  -2.816  1.00  0.00     0.002 A 
ATOM     32  C   UNL     1      -4.805   2.067  -1.126  1.00  0.00     0.028 A 
ATOM     33  C   UNL     1      -5.207   1.532  -2.350  1.00  0.00     0.002 A 
BRANCH  30  34
ATOM     34  N   UNL     1      -3.506   1.962   0.929  1.00  0.00    -0.365 N 
ATOM     35  C   UNL     1      -4.607   2.117   1.901  1.00  0.00     0.145 C 
ATOM     36  C   UNL     1      -2.575   3.112   0.876  1.00  0.00     0.145 C 
ATOM     37  C   UNL     1      -4.802   3.588   2.300  1.00  0.00     0.181 C 
ATOM     38  C   UNL     1      -2.401   3.681   2.292  1.00  0.00     0.181 C 
ATOM     39  O   UNL     1      -3.624   4.201   2.849  1.00  0.00    -0.378 OA
ENDBRANCH  30  34
ENDBRANCH   5  28
TORSDOF 6
```

**Partial charges (atom serial → q):** 1:0.049, 2:0.009, 3:0.154, 4:-0.162, 5:-0.230, 6:0.078, 7:0.272, 8:-0.267, 9:-0.350, 10:0.163, 11:0.123, 12:-0.012, 13:0.012, 14:0.012, 15:0.012, 16:-0.010, 17:-0.010, 18:-0.010, 19:0.007, 20:0.007, 21:0.007, 22:0.001, 23:0.010, 24:0.010, 25:0.001, 26:0.001, 27:0.000, 28:0.089, 29:0.030, 30:0.063, 31:0.002, 32:0.028, 33:0.002, 34:-0.365, 35:0.145, 36:0.145, 37:0.181, 38:0.181, 39:-0.378

**Meeko→RDKit:** SMILES = 0D; formula C32H38N4O2; formal charge 0; connectivity InChIKey RAQAMHLYXWAFRF matches 0D. Extra methylene (atom 11, BRANCH 9→11→12) vs compound 14; TORSDOF 6 = one extra rotatable bond.

---

## C) Discrepancies

**None that fail QC.** Documented non-failures:

1. **Stereo InChIKey layer:** Meeko round-trip assigns absolute stereo on adamantane bridgeheads from 3D coords (`/t…` layer). 0D SMILES/InChI are stereo-omitted (`UHFFFAOYSA-N`). Connectivity (first InChIKey block) and canonical SMILES match exactly — expected for 3D PDBQT, not a connectivity error.
2. **H-count in raw PDBQT element tally:** only polar `HD` present (Meeko convention). Full molecular formula recovered via Meeko→RDKit (implicit H) matches 0D (`C31H36N4O2` / `C32H39N5O` / `C32H38N4O2`).
3. **Σq ≈ +0.002** (14/15/20) vs exact 0: typical Gasteiger rounding; within ±0.05; formal charge 0.
4. Open Babel not available; identity used Meeko + REMARK SMILES + RDKit SMARTS instead.

No SMILES mismatch. No wrong regioisomer. No missing CH2 linker on 24 / no spurious CH2 on 14/15/20. No charge/type anomalies. PDBQT files were not modified.

---

## Method appendix

| Step | Method |
|------|--------|
| Atom dump | Direct file read of all `ATOM`/`HETATM`/`ROOT`/`BRANCH`/`TORSDOF` lines |
| Charges / AD types | Trailing two whitespace fields of each ATOM line |
| Coordinates | PDB fixed columns 31–38 / 39–46 / 47–54 |
| Input SMILES recovery | `REMARK SMILES` + `scripts/prepare_qiu_0e_pdbqt.py` `COMPOUNDS` |
| Exact match | Python string equality vs 0D SMILES |
| PDBQT→mol | Meeko `PDBQTMolecule(..., skip_typing=True)` + `RDKitMolCreate.from_pdbqt_mol` |
| Chemotype | RDKit SMARTS on REMARK/0D SMILES (and Meeko-regenerated SMILES identical) |

---

## Artefact

- Report only: `results/reports/qiu_0e_raw_pdbqt_audit.md`
- PDBQT untouched under `results/docking/qiu_0e/`
