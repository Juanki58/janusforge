# Dutta & Shukla 2023 MSM — Final_MSM recovered (trajectories still open)

**Status (2026-09-10):** `FINAL_MSM_COMPLETE` — full Box `Final_MSM` quartet ingested via **user browser download**. Scripted Box GETs may still hit HTTP **403** `error_message_bandwidth`. **Trajectory** shares were **not** downloaded. Optional external comparison is **READY when PI authorizes** — no P2 A/B/C reopen from this ingest alone.

## Local inventory (this directory)

| File | Bytes | SHA256 |
|------|------:|--------|
| `CB2_state_prob.pkl` | 67 145 861 | `0F273641DC3BD26CEDF38B0F98B3E4B8AFD0E3EADC5F10E38F22AAD16370C079` |
| `CB2_msm_feature_final_clustering.pkl` | 11 429 097 | `E4DB17C8E30DE41C0829BDF0F10C00643171CBDD5438E894E1C3F0A99E6C20E8` |
| `CB1_state_prob.pkl` | 101 054 619 | `14D51227A1D6B51C8C32216C5E514864427DBE26E6B102554D095D8090E7C60C` |
| `CB1_msm_feature_final_clustering.pkl` | 17 205 855 | `5851CA89D92B3863F9099538110E264D6B4E207AF27FEBC3794F0BDC80E1BE56` |

See also `MANIFEST.json`.

### Safe inspect (pickle.load only; no analysis)

| File | Type | High-level structure |
|------|------|----------------------|
| `CB2_state_prob.pkl` | `list` len **4972** | each `ndarray` `(T, 6)` `float32`; mode `T=600` (range 250–600); rows ≈ probability simplex over **6** metastable states |
| `CB2_msm_feature_final_clustering.pkl` | `list` len **4972** | each `ndarray` `(T,)` `int32` discrete cluster labels; same `T` per traj as state_prob |
| `CB1_state_prob.pkl` | `list` len **7582** | each `ndarray` `(T, 6)` `float32`; mode `T=600` (range 250–1000); **6** states |
| `CB1_msm_feature_final_clustering.pkl` | `list` len **7582** | each `ndarray` `(T,)` `int32` cluster labels; same `T` per traj as CB1 state_prob |

## Paper endpoints (locked from Nature HTML + PMC)

| Item | Value |
|------|--------|
| DOI | `10.1038/s42003-023-04868-1` |
| Data availability (exact) | Only Box: `https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4` |
| Code | `https://github.com/ShuklaGroup/Cannabinoid_activation` |
| Nature SI | MOESM1 Supporting Information PDF; MOESM2 Reporting Summary — **no MSM binaries / no extra deposit URLs** |

## Box shares (pre-recovery probe)

| Role | Share ID | Listing | Scripted download |
|------|----------|---------|-------------------|
| Official (paper) | `jzooa0o27z1w9ha0h6va3i51ir7l38j4` | 200 (`Final_MSM`) | 403 bandwidth (user browser later succeeded for Final_MSM) |
| README CB2/CB1 MSM + features | `iw1wlcdg…`, `xoiuicdp…`, `ix0hhvbw…`, `vyakobq2…` | 200 | 403 bandwidth |
| Traj shares (6) | see prior probe table | 200 | **not downloaded** |

### Official `Final_MSM` inventory (Box sizes matched local)

| File | Box file id | Size |
|------|-------------|-----:|
| `CB2_state_prob.pkl` | `1169830179145` | 67 145 861 |
| `CB1_state_prob.pkl` | `1169830923424` | 101 054 619 |
| `CB2_msm_feature_final_clustering.pkl` | `1169833284889` | 11 429 097 |
| `CB1_msm_feature_final_clustering.pkl` | `1169835993643` | 17 205 855 |

## Still missing (optional)

- Full **trajectory** dumps from Box traj shares (apo/holo CB1/CB2)
- Other README folders (bootstrap MSMs, volume/docking) — not required for Final_MSM external comparison

## Prior

- 2026-08-21: Box shares HTTP 404  
- 2026-09-10 a.m.: listing restored; downloads 403 bandwidth; mirror sweep negative  
- 2026-09-10 p.m.: user browser recovered all four `Final_MSM` pickles → this directory
