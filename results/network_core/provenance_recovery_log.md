# Provenance recovery log â€” CB2 network core

**Branch:** `task/data-provenance-recovery-attempt`  
**Date (UTC):** 2026-08-20  
**Governance:** `DATA_PROVENANCE=RECOVERY_IN_PROGRESS` | `DE_NOVO=STOP` | `DOCKING=STOP` | `NEW_CHEMISTRY=STOP`  
**Base:** `feat/cb2-minimal-gi-core-reanalysis` @ `c9bc287`

## Summary

| Archivo / Recurso | Fuente oficial | Checksum (SHA256) | Estado |
|-------------------|----------------|-------------------|--------|
| `41467_2025_60003_MOESM2_ESM.pdf` | Springer ESM (Nature Comm SI); mirrors tried: PMC bin 404, Europe PMC `pdf=render` (wrong file), PMC instance interstitial, Springer ESM **OK** | `2937da830d9a7e46c1509512e54e99908f0dd60e2650ee8bfe58d6bed58f1f08` | **RECUPERADO** |
| `41467_2025_60003_MOESM2_ESM_extract.txt` | Text extract of MOESM2 (pypdf) | `b13e60dbb5b06ef409ee105321135c22b0e8828aff73ad5e719ebd880477787d` | **RECUPERADO** |
| `sink_set_T_from_methods.txt` | Morales-Pastor 2025 Methods (PMC12159191 / PMID 40500255); MOESM2 is inventory-only | `c0d5c0230911b06971ad9b0483bb1b9d45f308b4e3f8e730b5c7405444f78bfd` | **RECUPERADO** |
| `data/external/endpoints/official_endpoints.json` | Registry of confirmed official endpoints | `8a49434c4a2f4cddcdf7c27ee174d936d1216fabebf5ae384741b6745c060f54` | **RECUPERADO** |
| GPCRmd publication/1540 (MD traj) | https://gpcrmd.org/dynadb/publications/1540/ | n/a (landing; binaries deferred) | **ENLACE_REGISTRADO** |
| GPCRmd/prefcoup_cb2r (code/networks) | https://github.com/GPCRmd/prefcoup_cb2r | n/a (remote repo) | **ENLACE_REGISTRADO** |
| Box MSM/features/traj `jzooa0o27z1w9ha0h6va3i51ir7l38j4` | https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4 (Comm Biol Data availability) | n/a (full deposit deferred; HTTP 404 from this env on probe) | **ENLACE_REGISTRADO** |
| ShuklaGroup/Cannabinoid_activation | https://github.com/ShuklaGroup/Cannabinoid_activation | n/a (remote repo) | **ENLACE_REGISTRADO** |

**Stricken:** any chase of `41467_2025_60003_MOESM6_ESM.*` as a permanent blocker. Official SI inventory in MOESM2 is **SI + Supplementary Data 1â€“4 only**.

## MOESM2 download attempts

Documented in `data/external/morales_pastor_2025/moesm2_download_log.txt`.

1. PMC `/pmc/articles/PMC12159191/bin/...MOESM2...pdf` â†’ 404  
2. Europe PMC `?pdf=render` â†’ full article PDF (~2.1 MB) â€” **rejected** (not MOESM2)  
3. PMC `/articles/instance/12159191/bin/...` â†’ HTML interstitial (~1.8 KB) â€” rejected  
4. Europe PMC bin paths â†’ connection reset  
5. **Springer ESM static-content URL â†’ 200, 34257 bytes, `%PDF`** â€” saved

## Explicit Sink Set T

**MOESM2 content:** â€œDescription of Additional Supplementary Filesâ€ listing Supplementary Data 1â€“4 only â€” **no residue list**.

**Formal definition** (article Methods, Morales-Pastor 2025; Dijkstra / LigACN path termini):

> 100 shortest pathways connecting ligand CHEMBL5085420 (source) and four selected intracellular residues (sinks) per replica â†’ 2000 pathways (100 Ã— 4 sinks Ã— 5 replicas). Sinks selected by proximity to G protein in the CBâ‚‚Râ€“G protein complex (Supplementary Fig. 12).

**Sink Set T (four residues):**

| Residue | Ballesterosâ€“Weinstein (as published) |
|---------|--------------------------------------|
| Arg131 | 3Ã—50 |
| Asp240 | 6Ã—30 |
| Ser303 | 8Ã—47 |
| Ser69 | 2Ã—39 |

**SINK_SET_T status:** `EXTRACTED` (from primary Methods text; MOESM2 recovered but inventory-only).

## Corrections vs prior audit

- Prior â€œpermanent blockâ€ on GPCRmd/1540, `GPCRmd/prefcoup_cb2r`, Box `jzooa0o27z1w9ha0h6va3i51ir7l38j4`, and `ShuklaGroup/Cannabinoid_activation` **dismissed** â€” endpoints registered.  
- Prior MOESM2 treated as missing `.xlsx` (403) â€” **corrected**: official MOESM2 is PDF, recovered.  
- **MOESM6** removed from recovery target lists (not in official MOESM2 inventory).  
- Trajectories / Box binaries remain **not locally downloaded** â†’ still `ENLACE_REGISTRADO` only.

## Governance confirmations

- No docking  
- No de novo / new chemistry  
- No push  

Downstream core reanalysis remains blocked until traj/Box objects are actually fetched if required by protocol; Sink Set T is no longer the missing piece.
