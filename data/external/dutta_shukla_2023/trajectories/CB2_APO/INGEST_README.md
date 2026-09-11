# CB2_APO trajectory ingest — BLOCKED (Box bandwidth)

**Date:** 2026-09-11  
**Status:** `DOWNLOAD_BLOCKED_403_BANDWIDTH` — **0 trajectory bytes on disk**  
**PI auth:** explicit (“te doy permiso para hacerlo tu”); blocker is **host account bandwidth**, not local permission.

## Source

| Item | Value |
|------|--------|
| Share | https://uofi.box.com/s/xl7tpf345rt8tikjaidfa8rm7gy2wrpj |
| Shared name | `xl7tpf345rt8tikjaidfa8rm7gy2wrpj` |
| Folder | `CB2_APO` (Box folder id `178517467499`) |
| Parent deposit | official paper Box `jzooa0o27z1w9ha0h6va3i51ir7l38j4` |
| Landing path | `data/external/dutta_shukla_2023/trajectories/CB2_APO/` |

## Disk / listing (OK)

| Check | Result |
|-------|--------|
| Free disk (C:) | ~**1518 GB** free — enough for full ~153 GB share |
| Listing HTTP | **200** (live 2026-09-11) |
| Pages | **249** (~20 items/page → ~**4975** files, matches prior estimate) |
| Page-1 types | mostly Amber NetCDF `*.nc` (~22–33 MB each); tiny helpers `list` (201 B), `mv_short_file` (121 B) |
| Example traj name | `CB2-APO_inactive_pr_9_frame_99-strip.nc` (~32.9 MB) |

## Download probe (FAILED — stop, no thrash)

Tried scripted GET via prior Box pattern  
`…/index.php?rm=box_download_shared_file&shared_name=…&file_id=f_…`  
on the **two smallest** files only:

| File | Box file id | Expected | Result |
|------|-------------|----------:|--------|
| `mv_short_file` | `1046788274875` | 121 B | **HTTP 403** `error_message_bandwidth` |
| `list` | `1046785195564` | 201 B | **HTTP 403** `error_message_bandwidth` |

Box body: *“The user hosting this content is out of bandwidth.”*  
Evidence: `_probe/probe_results.json` (+ HTML error stubs under `_probe/`).

**No pilot set downloaded. No batch download started.**

## Local inventory after attempt

| Path | Content |
|------|---------|
| `INGEST_README.md` | this note |
| `_probe_dl.py` | one-shot tiny-file probe script |
| `_probe/probe_results.json` | machine-readable 403 results |
| `*.nc` / topologies | **none** |

## Next steps (human / PI)

1. **Email authors** or wait for UIUC Box bandwidth restore / alternate mirror (see `docs/synthesis/DATA_REQUEST_DUTTA_SHUKLA_MSM.md`).
2. Optional: manual browser download *if* host bandwidth returns (scripted GETs historically stay 403 even when listing works; Final_MSM previously needed user browser after bandwidth recovered for that folder).
3. After any bytes land: smoke-open with mdtraj/MDAnalysis + MSM labels in `data/external/dutta_shukla_2023/msm/` — **not done here**.

## Epistemology

- EXTERNAL ingest only; **P2 not reopened as CONVERGENT**.
- **No contact-probability claims** — no trajs on disk.
- Final_MSM pickles remain available under `../msm/` for optional comparison when PI authorizes.
