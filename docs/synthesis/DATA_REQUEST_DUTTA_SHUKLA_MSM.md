# Data request — Dutta & Shukla 2023 MSM (DRAFT)

**Status:** `FINAL_MSM_RECOVERED` — CB2_APO traj ingest **PARTIAL** 2026-09-11 (scripted GET **403 bandwidth**; **1** `.nc` recovered via PI browser → `trajectories/CB2_APO/`); email draft still relevant for full traj set / bandwidth restore  

**Action:** draft only — **do NOT email** from automation  
**Date:** 2026-08-21 (updated 2026-09-11)  
**Branch:** `feat/cb2-hubs-functional-topology-test`  
**P2 role (reformulated):** Dutta & Shukla is **NOT** required to run P2. Real P2 uses **own MSM** on 5 WT GPCRmd Morales-Pastor trajs. Final_MSM pickles are **READY for optional external comparison when PI authorizes** (never a fitting template; different K is allowed).

---

## Citation / endpoints (locked)

| Item | Value |
|------|--------|
| Paper | Dutta, S. & Shukla, D. *Commun Biol* **6**, 485 (2023) |
| DOI | [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1) |
| PMC | [PMC10163236](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10163236/) |
| Code | [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) |
| Box (Data availability) | `https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4` (ID `jzooa0o27z1w9ha0h6va3i51ir7l38j4`) |
| Prior recovery | One-shot 2026-08-21 — all Box host/README mirrors **404**; see `results/network_core/traj_recovery_attempt.md` |
| Reprobe 2026-09-10 | Listing **HTTP 200** (`Final_MSM`: `CB2_state_prob.pkl` ~64 MB, `CB2_msm_feature_final_clustering.pkl` ~11 MB, CB1 twins). File download **HTTP 403** — Box body: *“The user hosting this content is out of bandwidth.”* (`error_message_bandwidth`). cursor-ide-browser MCP could not keep a tab for UI download. Manual browser likely same gate. Email remains fallback. Details: `data/external/dutta_shukla_2023/msm/BLOCKED_README.md` |
| Mirror sweep 2026-09-10 | All README Box IDs (`iw1wlcdg…`, `xoiuicdp…`, `ix0hhvbw…`, `vyakobq2…`, 6 traj shares) list **200**, downloads **403 bandwidth** (even tiny PDBs). Nature/PMC Data availability = **only** official Box; SI MOESM1/2 = PDFs only. Wayback = 301s only. Zenodo/OSF/Figshare/IDB/IDEALS/RG: no 2023 MSM mirror (Dryad hit = other NPS paper; IDB-6705697 = 2026 endo). GitHub code-only. |
| User browser recovery 2026-09-10 | Full `Final_MSM` quartet copied to `data/external/dutta_shukla_2023/msm/` (sizes match Box listing). Scripted downloads may still 403. **Trajectories not downloaded.** Provenance: `msm/BLOCKED_README.md`, `msm/MANIFEST.json`. |
| CB2_APO ingest attempt 2026-09-11 | PI authorized scripted download. Disk ~1518 GB free. Listing **200** (`CB2_APO`, ~249 pages, mostly `*.nc`). Tiny-file GETs → **403 bandwidth**. Later: **browser download worked** for `CB2-APO_inactive_pr_9_frame_99-strip.nc` (32.9 MB; smoke-open **600 frames × 4566 atoms**, Amber/cpptraj; topology still missing). Note: `trajectories/CB2_APO/INGEST_README.md`. |

**Need (remaining):** optional **trajectories** only if frame-level reanalysis of authors’ MD is required; Final_MSM state/clustering objects are already local. Full CB2_APO set still needs **browser batch** (or bandwidth restore / mirror / author copy) — one file is not enough.

**Local landing path:** `data/external/dutta_shukla_2023/msm/` + `MANIFEST.json` · traj: `trajectories/CB2_APO/` (1 gitignored `.nc` + README)

---

## Email template (copy for human send)

**To:** corresponding author(s) as listed on the paper  
**Subject:** Request for MSM / trajectory deposit — Commun Biol 2023 cannabinoid activation (DOI 10.1038/s42003-023-04868-1)

Dear Dr. Dutta and Dr. Shukla,

We are independently reanalyzing published CB1/CB2 conformational dynamics and would like to reproduce the metastable-state (MSM) analysis reported in your *Communications Biology* paper (DOI [10.1038/s42003-023-04868-1](https://doi.org/10.1038/s42003-023-04868-1)).

The GitHub repository [ShuklaGroup/Cannabinoid_activation](https://github.com/ShuklaGroup/Cannabinoid_activation) is available. The Box deposit cited in the Data availability statement (`https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4`) is listable, and we already hold the `Final_MSM` pickles locally. Trajectory share `CB2_APO` (`https://uofi.box.com/s/xl7tpf345rt8tikjaidfa8rm7gy2wrpj`) also lists successfully, but downloads still return HTTP 403 with Box’s message that the hosting account is **out of bandwidth** (confirmed 2026-09-11 even for ~100-byte helper files). We are therefore writing to request a bandwidth restore, an alternate mirror, or a direct copy of the **CB2 apo trajectories** (Amber NetCDF `*.nc` strips under `CB2_APO`) for frame-level reanalysis aligned to your published MSM labels.

We would use these materials only for academic reanalysis of state-dependent communication routes (no redistribution beyond our research group without your permission). Happy to cite the paper and acknowledge any guidance on preferred file formats.

Thank you very much for your time and for making the analysis reproducible.

Best regards,  
[NAME]  
[AFFILIATION]  
[EMAIL]

---

## Governance

```
STATUS: FINAL_MSM_RECOVERED
AUTO_EMAIL: FORBIDDEN
INFINITE_PUBLIC_SEARCH: STOP
EXTERNAL_COMPARISON: READY_WHEN_PI_AUTHORIZES
P2_REAL_MSM_COMPUTE: NOT_GATED_BY_DUTTA (own Morales-Pastor MSM)
P5_EXECUTION: NOT_OPENED_BY_THIS_REQUEST
TRAJECTORIES: BLOCKED_403_BANDWIDTH (CB2_APO probe 2026-09-11; 0 bytes)
```

*Fin — Final_MSM on disk; trajs still need bandwidth restore / author mirror / email.*
