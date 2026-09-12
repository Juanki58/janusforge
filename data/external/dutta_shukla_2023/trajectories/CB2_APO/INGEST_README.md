# CB2_APO trajectory ingest — ZIP LOCAL + TOPOLOGY

**Date:** 2026-09-12 (update); pilots 2026-09-11  
**Status:** `ZIP_LOCAL_TOPOLOGY_OK` — full **CB2_APO.zip** on disk under `trajectories/`; **prmtop extracted**; 2 Amber NetCDF pilots still present. Do **not** clean Temp for this zip (already moved out).

## Source

| Item | Value |
|------|--------|
| Share | https://uofi.box.com/s/xl7tpf345rt8tikjaidfa8rm7gy2wrpj |
| Shared name | `xl7tpf345rt8tikjaidfa8rm7gy2wrpj` |
| Folder | `CB2_APO` (Box folder id `178517467499`) |
| Parent deposit | official paper Box `jzooa0o27z1w9ha0h6va3i51ir7l38j4` |
| Landing path | `data/external/dutta_shukla_2023/trajectories/CB2_APO/` |

## Full zip (MOVED 2026-09-12) — confirmed

| Item | Value |
|------|--------|
| Previous Temp path | `C:\Users\juanc\AppData\Local\Temp\CB2_APO.zip` (**gone** — moved, not copied) |
| **Current zip path** | `data/external/dutta_shukla_2023/trajectories/CB2_APO.zip` |
| Absolute | `C:\Users\juanc\projects\janusforge\data\external\dutta_shukla_2023\trajectories\CB2_APO.zip` |
| Size | **152 769 973 351** bytes (~**142.28 GB**) |
| Zip entries | **4974** (1× `prmtop` + **4971**× `.nc` + helpers) |
| `.nc` by state label | inactive **2598**; active **2373** |
| Move method | `Move-Item` same volume (instant rename); Temp no longer holds the zip |
| Free disk after move (C:) | ~**1375 GB** |
| git | `*.zip` gitignored — **do not commit** |

**Temp cleanup:** zip already removed from Temp by the move. Do not delete the destination zip until analysis / backup policy is decided.

## Topology (EXTRACTED — priority)

| Item | Value |
|------|--------|
| Path inside zip | `CB2_APO/CB2-APO_inactive_pr_1-strip.prmtop` |
| Landed | `CB2-APO_inactive_pr_1-strip.prmtop` (flat under this folder) |
| Size | **1 989 174** bytes (~1.9 MiB) |
| Extract scope | **prmtop only** — full 142 GB of `.nc` **not** bulk-extracted |
| Optional stratified `.nc` sample | **skipped** (optional; pilots already on disk) |
| git | `*.prmtop` / `*.parm7` gitignored — **do not commit** |

## Disk / listing (historical Box listing OK)

| Check | Result |
|-------|--------|
| Listing HTTP | **200** (live 2026-09-11) |
| Pages | **249** (~20 items/page → ~**4975** files; zip confirms **4974** entries) |
| Page-1 types | mostly Amber NetCDF `*.nc` (~22–33 MB each); tiny helpers `list`, `mv_short_file` |
| Example traj names | `CB2-APO_inactive_pr_9_frame_99-strip.nc`; `CB2-APO_active_pr_10_frame_28-strip.nc` |
| State map (spot-check) | Early pages mostly `inactive`; mix from ~p.50; late pages mostly `active` |

## Download probe (scripted FAILED — historical)

Scripted Box GET → **HTTP 403** `error_message_bandwidth`. Evidence under `_probe/`. **No longer blocking** for full archive: zip is local.

## Browser recovery pilots (2026-09-11) — still on disk

| Item | inactive pilot | active pilot |
|------|----------------|--------------|
| Landed path | `CB2-APO_inactive_pr_9_frame_99-strip.nc` | `CB2-APO_active_pr_10_frame_28-strip.nc` |
| Size | **32 907 228** bytes (~31.4 MiB) | **32 907 228** bytes (~31.4 MiB) |
| git | `*.nc` gitignored | same |

### Filename pattern

`CB2-APO_{state}_pr_{N}_frame_{F}-strip.nc` — both pilots smoke-open as Amber NetCDF, **600 frames**, **4566 atoms**.

### Smoke-open (pilots)

| Field | Value |
|-------|--------|
| Format | NetCDF3 64-bit offset, Conventions **AMBER** 1.0 |
| `coordinates` | `(600, 4566, 3)` float32 |
| Topology | **now available locally** — `CB2-APO_inactive_pr_1-strip.prmtop` |

## Local inventory

| Path | Content |
|------|---------|
| `../CB2_APO.zip` | full share archive (~142 GB; gitignored) |
| `INGEST_README.md` | this note |
| `CB2-APO_inactive_pr_1-strip.prmtop` | stripped Amber topology (gitignored) |
| `CB2-APO_inactive_pr_9_frame_99-strip.nc` | inactive pilot |
| `CB2-APO_active_pr_10_frame_28-strip.nc` | active pilot |
| `_probe_dl.py` / `_probe/` | historical 403 probe artifacts |

## Next steps (analysis now unblocked)

1. **Open pilots + prmtop** with mdtraj / MDAnalysis (`janus_p1`) — topology was the blocker; atom count should match **4566**.
2. Optionally extract more `.nc` **on demand** from the local zip (do not unpack all 142 GB).
3. Align frames to MSM labels in `data/external/dutta_shukla_2023/msm/` when PI authorizes.
4. Keep zip under `trajectories/`; extract subsets only.

## Epistemology

- EXTERNAL ingest only; **P2 not reopened as CONVERGENT**.
- **No contact-probability claims** from two chunks alone.
- Final_MSM pickles remain under `../msm/` for optional comparison when PI authorizes.
