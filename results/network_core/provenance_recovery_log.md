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
| GPCRmd publication/1540 (MD traj) | https://gpcrmd.org/dynadb/publications/1540/ → files via `/dynadb/files/Dynamics/dyn2417/` | see `trajectories/MANIFEST.json` | **RECUPERADO** (WT dyn2126; 2026-08-21) |
| GPCRmd/prefcoup_cb2r (code/networks) | Zenodo 15270434 + https://github.com/GPCRmd/prefcoup_cb2r | `e1c6d0308aeef7bd52cd986a8fb7bca940162d895c0e0857dfbde55b6682e061` (zip) | **RECUPERADO** (code only) |
| Box MSM/features/traj `jzooa0o27z1w9ha0h6va3i51ir7l38j4` | https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4 | n/a | **BLOQUEADO** HTTP 404 (one-shot) |
| ShuklaGroup/Cannabinoid_activation | https://github.com/ShuklaGroup/Cannabinoid_activation | n/a (remote; no MSM traj binaries) | **ENLACE_REGISTRADO** (code/figures only) |

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

---

## 2026-08-20 — Static LigACN topology (PI override)

**Branch:** `task/static-ligacn-topology`  
**Action:** Static topological reanalysis of published WT LigACN → Sink Set T using local SD1–SD3 only.  
**Did not:** claim dynamic minimal Gi core; auto-expand S with AUSENTE pocket residues; start new traj/MSM recovery cycle.

| Artifact | Path |
|----------|------|
| Report | `results/network_core/static_ligacn_topology_report.md` |
| Metrics | `results/network_core/static_ligacn_topology_metrics.json` |
| Verdict | `results/network_core/static_topological_verdict.json` |
| Script | `scripts/network/analyze_static_ligacn_topology.py` |

**S (final, verified):** `8D0:1`, `SER:285` (`285-LIG` Inactive), `PHE:87` (`87-LIG` Inactive).  
**AUSENTE (logged, not substituted):** `TRP:258`, `PHE:183` (absent from WT_degeneracy; LIG columns exist in SD2 Inactive).  
**T:** ARG:131, ASP:240, SER:303, SER:69 — 4/4 paths from ligand.  
**Verdict:** `STATIC_TOPOLOGICAL_BOTTLENECKS = TOPOLOGICAL_HUBS_IDENTIFIED`  
**Governance:** `STATIC_GRAPH_ANALYSIS=CLOSED`; `CB2_MINIMAL_GI_CORE=BLOCKED_PENDING_DYNAMIC_VALIDATION`; `CB1_COMPARISON=BLOCKED`.  
**Traj one-liner:** GPCRmd/1540 and Box deposit remain ENLACE_REGISTRADO only (no new hunt).

---

## 2026-08-21 — One-shot traj recovery (GPCRmd/1540 + Dutta–Shukla Box)

**Branch:** `feat/cb2-hubs-functional-topology-test`  
**Campaign:** directed download only (official endpoints + paper/repo mirrors once). No docking / de novo / P1.  
**Full log:** `results/network_core/traj_recovery_attempt.md`

| Recurso | Resultado | SHA256 / error |
|---------|-----------|----------------|
| GPCRmd dyn2126 WT (pdb+psf+5×xtc via `/dynadb/files/Dynamics/dyn2417/`) | **RECUPERADO** → `data/external/morales_pastor_2025/trajectories/` | see `MANIFEST.json` |
| Zenodo 15270434 `prefcoup_cb2r` zip | **RECUPERADO** (code only, 4513 B) | `e1c6d0308aeef7bd52cd986a8fb7bca940162d895c0e0857dfbde55b6682e061` |
| Box `jzooa0o27z1w9ha0h6va3i51ir7l38j4` + README CB2 Box mirrors | **BLOQUEADO** HTTP 404 | no local MSM binaries |
| GPCRmd login/API bulk zip | **BLOQUEADO** login **500**; REST api paths **404** | WT files via direct HTML links OK |
| Author-request contingency (Morales-Pastor) | **REGISTERED** — agent did **not** email | — |

**Path gate:** Morales traj `ready=true`; Dutta MSM `ready=false` → status remains **`BLOCKED_PENDING_TRAJECTORIES`**.  
**`RECOVERY_ATTEMPT = DONE`**. P1 = **no** until dual-path gate satisfied.

