# CB2_APO trajectory ingest — PARTIAL (1 file via browser)

**Date:** 2026-09-11  
**Status:** `PARTIAL_BROWSER_OK` — **1** Amber NetCDF on disk; scripted Box GET still **403 bandwidth**  
**PI auth:** explicit (“te doy permiso para hacerlo tu”); automated downloads blocked by **host account bandwidth**; **manual browser download succeeded** for at least one file.

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

## Download probe (scripted FAILED — stop thrash)

Tried scripted GET via prior Box pattern  
`…/index.php?rm=box_download_shared_file&shared_name=…&file_id=f_…`  
on the **two smallest** files only:

| File | Box file id | Expected | Result |
|------|-------------|----------:|--------|
| `mv_short_file` | `1046788274875` | 121 B | **HTTP 403** `error_message_bandwidth` |
| `list` | `1046785195564` | 201 B | **HTTP 403** `error_message_bandwidth` |

Box body: *“The user hosting this content is out of bandwidth.”*  
Evidence: `_probe/probe_results.json` (+ HTML error stubs under `_probe/`).

**No scripted pilot set. No batch download started.**

## Browser recovery (WORKED — 2026-09-11)

Same pattern as Final_MSM: **listing / scripted GET 403**, but **PI browser download** delivered a usable file.

| Item | Value |
|------|--------|
| Temp source | `c:\Users\juanc\AppData\Local\Temp\CB2-APO_inactive_pr_9_frame_99-strip.nc` |
| Landed path | `CB2-APO_inactive_pr_9_frame_99-strip.nc` (copied, not moved) |
| Size | **32 907 228** bytes (~31.4 MiB) |
| mtime (Temp) | 2026-09-11 15:48:18 (local) |
| git | `*.nc` is gitignored — binary **not** committed |

### Filename pattern (hypothesis)

Pattern observed: `CB2-APO_{state}_pr_{N}_frame_{F}-strip.nc`

| Token | Hypothesis |
|-------|------------|
| `CB2-APO` | System: CB2 apo |
| `inactive` | Conformational / MSM **state label** in the filename (not a guarantee of MSM microstate id) |
| `pr_9` | Likely **production run / replica index** 9 (Amber-style `pr` naming); not verified against paper SI |
| `frame_99` | Likely **seed / start / reference frame index** used when cutting this chunk — **not** “this file has 1 frame” |
| `strip` | Solvent/ions stripped (protein-only coords) — consistent with atom count |

**Smoke-open contradicts a single-frame file:** NetCDF has **600 frames**.

### Smoke-open (`janus_p1`: netCDF4 / mdtraj / MDAnalysis available)

| Field | Value |
|-------|--------|
| Format | NetCDF3 64-bit offset, Conventions **AMBER** 1.0 |
| Writer | cpptraj V18.01 (`Cpptraj Generated trajectory`) |
| `coordinates` | `(600, 4566, 3)` float32 |
| **n_frames** | **600** |
| **n_atoms** | **4566** |
| Other vars | `time`, `cell_lengths`, `cell_angles` |
| Topology | **missing locally** — coords-only `.nc`; analysis that needs bonds/residues needs matching `prmtop` / PDB from the deposit or paper SI |

## Local inventory

| Path | Content |
|------|---------|
| `INGEST_README.md` | this note |
| `CB2-APO_inactive_pr_9_frame_99-strip.nc` | 1 Amber traj chunk (gitignored) |
| `_probe_dl.py` | one-shot tiny-file probe script |
| `_probe/probe_results.json` | machine-readable 403 results |

## Next steps (human / PI)

1. **Continue browser downloads** (or Box “Download” / multi-select / zip if the UI allows) into this folder — one file is **not** enough for MSM/frame-level reanalysis (~thousands of `*.nc` in the share).
2. Prefer batching by state prefix if browsing: `inactive_*`, then other state labels once naming is confirmed from more filenames.
3. Also grab any **topology** (`*.prmtop`, `*.parm7`, stripped PDB) if present in the share.
4. After a useful subset lands: open with mdtraj/MDAnalysis **+ topology**, optionally align to MSM labels in `data/external/dutta_shukla_2023/msm/`.
5. Email authors / wait for bandwidth restore remains fallback for full ~153 GB (see `docs/synthesis/DATA_REQUEST_DUTTA_SHUKLA_MSM.md`).

## Epistemology

- EXTERNAL ingest only; **P2 not reopened as CONVERGENT**.
- **No contact-probability claims** from this single chunk.
- Final_MSM pickles remain available under `../msm/` for optional comparison when PI authorizes.
