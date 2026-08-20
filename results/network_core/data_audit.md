# Data audit — CB2 minimal Gi-core reanalysis

**Access date (UTC):** 2026-08-20T12:15:33Z  
**Branch:** `feat/cb2-minimal-gi-core-reanalysis`  
**Mode:** READ_ONLY / PUBLIC_DATA_REANALYSIS

## Governance

```yaml
DE_NOVO_GENERATION: STOP
THRESHOLD_MODIFICATION: STOP
ORTHOSTERIC_DESIGN: PAUSED
CONTRACT_v1.0: ARCHIVED_HISTORICAL
NEW_DOCKING: STOP
NEW_CHEMISTRY: STOP
MODO: READ_ONLY / PUBLIC_DATA_REANALYSIS
```

## 1. Primary sources (identity)

### A — Morales-Pastor et al. 2025
- DOI `10.1038/s41467-025-60003-0` | PMID `40500255` | PMC `PMC12159191`
- GPCRmd `https://gpcrmd.org/dynadb/publications/1540/`
- GitHub `https://github.com/GPCRmd/prefcoup_cb2r` | Zenodo `10.5281/zenodo.15270434`
- System: CB2R + HU-210; **14 PrefCoup / 20 Coup** + WT; PDB 6KPC / 5ZTY / 6KPF
- Article match: **confirmed** via PMC MOESM↔Supplementary Data mapping

### B — Dutta & Shukla 2023 (MSM/VAMPnets; NOT Li 2023)
- DOI `10.1038/s42003-023-04868-1` | PMC `PMC10163236`
- GitHub `https://github.com/ShuklaGroup/Cannabinoid_activation`
- Li et al. 2023 = cryo-EM only — excluded as MSM source

## 2. Recovered datasets (checksums)

- `41467_2025_60003_MOESM1_ESM.pdf` — 4670882 bytes — sha256 `4ec13634862838f8f1c10431f67f904350844e266715f16dc546db3ef22060b7` — SI PDF (figures/notes). Springer ESM MOESM1; article-matched SI PDF.
- `41467_2025_60003_MOESM3_ESM.xlsx` — 56748 bytes — sha256 `f296cb131c22d32de9985fe54fb17422f72385aed2b0596e8ed180f07b7e2a7a` — Supplementary Data 1 (PMC #MOESM3). 360-mutant expression/Emax/coupling profile table.
- `41467_2025_60003_MOESM4_ESM.xlsx` — 5133984 bytes — sha256 `04a7d0c084e97bf40fa2637e996258e527d4b422b257a172623c13f289ad929c` — Supplementary Data 2 (contacts; LigACN contact tables). Inactive/Active structure contacts; 36 mutant_id x replicas; edge-like contact columns.
- `41467_2025_60003_MOESM5_ESM.xlsx` — 970304 bytes — sha256 `ff53ec7bf227e0d2c3e5ced9fb81e2e56e61fb5d6ec373c1e3f2c574e77c09b9` — Supplementary Data 3 (degeneracy / information transmission). 36 *_degeneracy sheets including WT_degeneracy (100x100).
- `prefcoup_cb2r-v.1.0.0.zip` — 4513 bytes — sha256 `e1c6d0308aeef7bd52cd986a8fb7bca940162d895c0e0857dfbde55b6682e061` — Zenodo code release v.1.0.0. 4.5 kB zip — release metadata/stub; full notebooks fetched separately from GitHub raw.
- `prepare_suplementary_data.ipynb` — 27184 bytes — sha256 `9763016011790b57ee677bebe8fbaeb975bfe64ceb9a853613f1071e5149e16e` — GitHub analysis notebook. Documents how Supp Data 1/2 were assembled; paths point to authors' private project_root.
- `download_simualtions.ipynb` — 15271 bytes — sha256 `a28b08fbb1db3eed2c0ca16cd804bed9936c4fc7e2c540cb995d7522c61ee604` — GitHub GPCRmd download notebook. Documents GPCRmd download procedure; does not embed trajectories.
- `preprocess_contacts.ipynb` — 3811 bytes — sha256 `3a9af8d7a7aea9108a29ceb79ece4dc5981b3653799f5021fad0310d2414e49e` — GitHub contact preprocess notebook. Requires local MD contact TSVs — not present in repo release.
- `interaction_coupling.ipynb` — 257658 bytes — sha256 `12c7afca12bdb987c340bffc1311dc073d5abd3f34a5e31d1a0fd22bb0807bfb` — GitHub interaction notebook. Author analysis notebook; not a standalone edge-list dump.
- `pmc_article.html` — 276789 bytes — sha256 `46934505a7da2615d0a6fa1deee0a9e8066bf2316294eab462f6995c0505bf97` — PMC full text snapshot. Used to map MOESM# <-> Supplementary Data #.
- `gpcrmd_1540.html` — 147468 bytes — sha256 `e3866ff8cc5233390d98a8d319884df7d82bb31bbda022d7cf9b9684db8113cc` — GPCRmd publication landing. Landing page recovered; trajectory binaries not downloaded in this run.
- `github_contents.json` — 19617 bytes — sha256 `f2c62d1f92e8e9374bf3769b1b3836d15ca9c2907b0571f80946f89387d35c8f` — GitHub API listing GPCRmd/prefcoup_cb2r. Confirms notebooks-only public tree (no trajectory blobs).
- `shukla_tree.json` — 30585 bytes — sha256 `2e9e80e48c758a814432c0c47ccf6c1c983c7794aa95f32443c6b99d62e1d822` — GitHub tree ShuklaGroup/Cannabinoid_activation. Figure/code + Initial_Coordinates PDBs listed; MSM feature objects/traj deposit not fully local.

## 3. Not recovered / blocked

- **41467_2025_60003_MOESM2_ESM.xlsx**: Springer ESM returned HTTP 403 Forbidden in this environment.
- **41467_2025_60003_MOESM6_ESM.xlsx**: Required for full mutant-response audit; blocked.
- **GPCRmd trajectories (dynadb/publications/1540)**: Landing HTML present; xtc/dcd/topology binaries not fetched. Notebooks require local simulations/.
- **Dutta & Shukla Box MSM/trajectory deposit**: Box URL cited in paper Data availability; not downloaded. GitHub has figure scripts/coords, not full MSM objects for ACN-comparable graph.
- **Exact intracellular sink residue list for LigACN path termini**: Not extractable from recovered SI PDF binary text hunt; not present as a dedicated table in recovered xlsx. Blocks pre-registered S↔T core search.

## 4. What could vs could not be reproduced

**Could (partial):** load published Supp Data 1–3 tables; build descriptive graph stats from WT degeneracy (Supp Data 3); confirm PrefCoup/Coup counts and ligand node `8D0:1`.

**Could not:** recompute ACN from trajectories; recover Supp Data 4; recover exact intracellular sink list T; obtain CB1 LigACN-equivalent; download Box MSM deposit.

## 5. Software

- Python 3.14.6
- pandas 3.0.5
- networkx 3.6.1
- platform Windows-11-10.0.26200-SP0

## 6. Audit conclusion

Recovery is **incomplete** relative to the pre-registered minimal-core procedure. Downstream core verdict must remain **INDETERMINATE** unless blockers are cleared without post-hoc rule changes.
