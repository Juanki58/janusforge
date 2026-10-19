# Static coordinate audit — published CB2–Gαi cross-links

**Date:** 2026-10-19  
**Type:** Retrospective, descriptive coordinate comparison; no trajectory analysis.  
**Scope authorization:** User-directed continuation of the literature review; P2, P3, and P5 flags unchanged.

## Question and method

Mnpotra et al. identified three CB2–Gαi1 cross-linked residue pairs by chemical cross-linking and LC-MS/MS. This audit measures Cα–Cα distances, the metric compared with cutoffs in the paper, and also records reactive-atom endpoint distances (SG–SG or NZ–NZ). Local chain R is CB2 (UniProt P34972); chain A is Gαi1 (P63096). Coordinates use PDB residue numbering aligned to those UniProt accessions. No structural alignment, refinement, side-chain rotamer search, linker modelling, or dynamics was performed.

Source paper: [Mnpotra et al., JBC (2014), DOI 10.1074/jbc.M113.539916](https://doi.org/10.1074/jbc.M113.539916). Local structures selected from the expanded landmark panel: 6PT0, 6KPF, 8GUQ, 8GUR, 8GUS, 8GUT, and 8X3L.

## Comparison using the paper's distance criteria

The source paper assessed Cα–Cα separations: 7–10 Å for the HgCl₂ cysteine pair and a maximum of 24.2 Å for each DSS lysine pair. The main values below are Cα–Cα distances, with these published cutoffs applied as a geometric screen. Parenthesized values are SG–SG or NZ–NZ endpoint separations (Å), included only as coordinate descriptors; they are not the paper's cutoff metric.

| PDB | Ligand / source set | Cys134–Cys351 Cα (SG–SG) | Lys245–Lys349 Cα (NZ–NZ) | Lys215–Lys317 Cα (NZ–NZ) |
|---|---|---:|---:|---:|
| 6PT0 | WIN 55,212-2 | 8.25 (4.07) | 16.26 (22.29) | 21.93 (30.42) |
| 6KPF | AM12033-class | 7.97 (3.72) | 15.73 (22.10) | 21.62 (28.77) |
| 8GUQ | Olorinab | 8.28 (3.64) | 16.17 (16.29) | 22.07 (30.29) |
| 8GUR | CP55,940 | 7.83 (3.85) | 15.51 (16.94) | 22.09 (29.95) |
| 8GUS | HU-308 | 7.85 (4.33) | 15.53 (16.31) | 21.99 (28.43) |
| 8GUT | LEI-102 | 7.80 (3.98) | 15.48 (20.78) | 21.74 (29.09) |
| 8X3L | agonist (8X3L) | 7.65 (3.91) | 15.77 (18.17) | 23.20 (31.90) |

## Interpretation

All seven snapshots fall within the source paper's Cα-distance range for Cys134–Cys351 (7–10 Å) and below its maximum Cα distance for both lysine pairs (24.2 Å). Under that source-defined geometric screen, the published cross-links are compatible with each of these static CB2–Gi structures. The parenthesized NZ endpoint distances are longer for Lys215–Lys317, which shows why the source paper's Cα-based criterion must remain distinct from reactive-atom endpoint distances.

These are single static structures with engineered constructs and ligand-specific contexts. Passing a geometric cutoff does not establish cross-link formation probability or biological occupancy; the experiment was performed in membranes without exogenous agonist, while the structures represent ligand-bound cryo-EM complexes. This audit does not establish Gi rearrangement in cells, CB2 internal allostery, or an MSM architecture. No P2 result or status is changed.

## Reproducibility

Run from the repository root: `python scripts/network_core/ext_cb2_gi_crosslink_audit.py`. The runner writes this report and `ext_cb2_gi_crosslink_audit.json` under `results/network_core/`. Input PDB SHA-256 values are stored in the JSON.

## Data and source

- Primary cross-linking experiment: [Mnpotra et al. (2014)](https://doi.org/10.1074/jbc.M113.539916).
- Cryo-EM CB2–Gi reference 6PT0: [Xing et al. (2020)](https://doi.org/10.1016/j.cell.2020.01.007).
- Cryo-EM CB2–Gi 6KPF: [Hua et al. (2020)](https://doi.org/10.1016/j.cell.2020.01.008).
- CB2–Gi panel 8GUQ/8GUR/8GUS/8GUT: [Li et al. (2023)](https://doi.org/10.1038/s41467-023-37112-9).
- CB2–Gi structure 8X3L: [Shen et al. (2024)](https://doi.org/10.1073/pnas.2401091121).
