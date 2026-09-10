# Dutta & Shukla 2023 MSM — recovery blocked

**Verdict (2026-09-10 mirror sweep):** Data **are published** (paper Data availability + live Box listing of `Final_MSM` / CB1–CB2 `*_state_prob.pkl`), but **no working download today** — every Box file GET returns HTTP **403** `error_message_bandwidth` (“The user hosting this content is out of bandwidth.”). No Zenodo/OSF/Dryad/Figshare/IDB mirror of this 2023 Commun Biol deposit. Email authors remains the path.

## Paper endpoints (locked from Nature HTML + PMC)

| Item | Value |
|------|--------|
| DOI | `10.1038/s42003-023-04868-1` |
| Data availability (exact) | Only Box: `https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4` |
| Code | `https://github.com/ShuklaGroup/Cannabinoid_activation` |
| Nature SI | MOESM1 Supporting Information PDF; MOESM2 Reporting Summary — **no MSM binaries / no extra deposit URLs** |
| Source data button | Nature page has SI/figshare container markup; **no separate MSM “Source data” archive** beyond Box |

## Box shares probed (all listings HTTP 200 on `uofi.app.box.com`; all file downloads 403 bandwidth)

| Role | Share ID | Listing | Download |
|------|----------|---------|----------|
| Official (paper) | `jzooa0o27z1w9ha0h6va3i51ir7l38j4` | 200 (`activation_paper_github` / `Final_MSM`) | 403 bandwidth (`CB2_state_prob.pkl` `f_1169830179145`; clustering `f_1169833284889`) |
| README CB2 MSM | `iw1wlcdg44gjs7ufx4rriuulindibj5t` | 200 (`CB2_state_prob.pkl` `f_1187285378640`) | 403 bandwidth (pkl **and** tiny PDB) |
| README CB1 MSM | `xoiuicdpjhrohpjputgnk5ppuwlcfp35` | 200 | (same account; not re-fetched after 403 pattern) |
| README features/bootstrap | `ix0hhvbwgwhipqrhk1oe1iwpl021vyw1` | 200 | 403 on `CB2_bt_80_0_msm.pkl` |
| README volume/docking | `vyakobq2zbk5xyoxqvccxngif6jzeo0z` | 200 | — |
| Traj CB1 apo | `p0ivhqihimh8cr3mp4tua5gd7ygsijo8` | 200 | — |
| Traj CB2 apo | `xl7tpf345rt8tikjaidfa8rm7gy2wrpj` | 200 | — |
| Traj CB1 holo act/inact | `a8dvtgmw4sjajcjbvmkbjbtfcpy9dy2i`, `9khutxgdsjc7mriqktch5ifbxcda4fs7` | 200 | — |
| Traj CB2 holo act/inact | `3ah3yftcs6e40tytnxgn8cw1g4fzrlir`, `rkflfcts7vccr4dlw325k65cxfx9fj4s` | 200 | — |

Hosts tried per ID: `uofi.box.com`, `uofi.app.box.com`, `app.box.com`. HEAD on `uofi.box.com` often 404; GET→redirect→200 SPA.

### Official `Final_MSM` inventory (priority)

| File | Box file id | Size |
|------|-------------|-----:|
| `CB2_state_prob.pkl` | `1169830179145` | 67 145 861 |
| `CB1_state_prob.pkl` | `1169830923424` | 101 054 619 |
| `CB2_msm_feature_final_clustering.pkl` | `1169833284889` | 11 429 097 |
| `CB1_msm_feature_final_clustering.pkl` | `1169835993643` | 17 205 855 |

## Other mirrors (exhaustive negative)

| Endpoint | Result |
|----------|--------|
| Wayback CDX official Box | Snapshots **2023-05-06** only as **301 redirects** — no archived file bytes |
| Wayback fetch of snapshot | SPA shell only; no recoverable binaries |
| Zenodo API `s42003-023-04868-1` / Dutta creator | **0** relevant hits |
| OSF search API | 404 / unusable |
| Figshare search | unrelated hits only |
| Dryad `Dutta Shukla cannabinoid` | **different paper** (NPS/TRAM; doi:10.5061/dryad.4f4qrfjq5) — not Commun Biol 2023 MSM |
| Illinois Data Bank search / home | HTTP **403** from this host; known **IDB-6705697** is **2026 endocannabinoid** paper — do not confuse |
| IDEALS thesis item 129420 | HTTP **403** (no data dump reachable here) |
| GitHub `ShuklaGroup/Cannabinoid_activation` | code + small figure `.pkl` (~13 KB) + PDBs; **no** `CB2_state_prob.pkl`; **no** releases |
| GitHub `Dutta_Shukla_Cannabinoid_2023a` | **different** manuscript (NPS/TRAM); other Box IDs |
| GitHub `Dutta_Shukla_EndoCannabinoid_2025` | **different** 2025/2026 endocannabinoid work |
| ResearchGate / Academic Torrents | RG 403; AT browse no matching MSM deposit |
| Nature MOESM1/2 | downloadable PDFs only (SI text + reporting summary) |

Probe artifacts: `data/external/_recovery_2026-08-21/box_list_*_2026-09-10b.html`, `box_dl_*_probe.html`, `wayback_official_cdx.json`, `zenodo_*.json`.

## Status

- Binaries under this directory: **none**
- Fallback: human email (`docs/synthesis/DATA_REQUEST_DUTTA_SHUKLA_MSM.md`) — bandwidth restore / alternate mirror / direct `Final_MSM` CB2 objects
- No MSM analysis from this attempt

## Prior

- 2026-08-21: Box shares HTTP 404  
- 2026-09-10 a.m.: listing restored; downloads 403 bandwidth  
- 2026-09-10 mirror sweep: all README Box IDs listable; same bandwidth gate; no third-party mirror
