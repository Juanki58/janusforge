# Trajectory recovery attempt (one-shot) — 2026-08-21

**Branch:** `feat/cb2-hubs-functional-topology-test`  
**Campaign:** ONE-SHOT only (official endpoints + paper/repo mirrors once each)  
**Governance:** no docking · no de novo · no P1 compute · no author email  
**Outcome:** **PARTIAL** — GPCRmd WT traj recovered; Dutta–Shukla Box MSM **blocked** (HTTP 404)  
**Status after attempt:** `DYNAMIC_REANALYSIS = BLOCKED_PENDING_TRAJECTORIES` (P1 **no**)

---

## 1. GPCRmd publication/1540 (Morales-Pastor 2025)

| Endpoint | Method | Result |
|----------|--------|--------|
| https://gpcrmd.org/dynadb/publications/1540/ | GET | **200** HTML listing dynamics (WT `2126` + mutants) |
| https://gpcrmd.org/dynadb/dynamics/id/2126/ | GET | **200** Simulation report; download buttons present |
| https://gpcrmd.org/dynadb/api/publications/1540/ | GET | **404** |
| https://gpcrmd.org/dynadb/api/dynamics/2126/ | GET | **404** |
| https://gpcrmd.org/dynadb/api/files/dynamics/2126/ | GET | **404** |
| https://gpcrmd.org/dynadb/download/dynamics/2126/ | HEAD | **404** |
| https://submission.gpcrmd.org/dynadb/files/Dynamics/dyn2126/ | HEAD | SSL trust failure |
| https://gpcrmd.org/accounts/login/ (API downloader requires login per docs) | HEAD | **500** Internal Server Error |
| Docs: https://gpcrmd-docs.readthedocs.io/en/latest/data-download.html | HEAD | **200** |
| Docs: https://gpcrmd-docs.readthedocs.io/en/latest/api.html | HEAD | **200** (bulk API needs GPCRmd account) |
| Zenodo `10.5281/zenodo.15270434` | GET API | **200** — only `prefcoup_cb2r-v.1.0.0.zip` (4513 B code, **not** traj) |

### Official file URLs (from dynamics/2126 HTML)

Paths under `/dynadb/files/Dynamics/dyn2126/*` → **404**.  
Active buttons use `/dynadb/files/Dynamics/dyn2417/*` → **200**.

| File | Bytes | SHA256 |
|------|------:|--------|
| `tmp_dyn_0_2417.pdb` | 5417685 | `a6468f3e0a93547b71a0a300b8ad1e9d664d30b62b4789dfcf53728033436350` |
| `24306_dyn_2126.psf` | 10429330 | `fce9db151fbf5f7f0ed2b235ff0fd5d962dd8da91fe97afa34f675ab8e2f02e1` |
| `24307_trj_2126.xtc` | 77700544 | `1fe13c425c67dd1325208af71131b34fdc3407b868f8c2489930c3d81e53e134` |
| `24308_trj_2126.xtc` | 77697176 | `6fef31e2ae0e10eac4590be5b9e205a5b29e3b96d4ee64cc0227dd39c3628be4` |
| `24309_trj_2126.xtc` | 77595656 | `598ca435644396c1e2503d94d5b75e2469307effe1790a68cc490971b44eadd2` |
| `24310_trj_2126.xtc` | 77726792 | `fec3d8115a3a0d47bc45de20fd15baee5d21c0c46d3599e3970b9c4d08953f3d` |
| `24311_trj_2126.xtc` | 77651580 | `467c225dea6cca37e94fd7e7521d406446c32fecf34f46e7d98b303290efa99b` |

**Local path:** `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/`  
**Manifest:** `data/external/morales_pastor_2025/trajectories/MANIFEST.json`  
**Zenodo code (non-traj):** `data/external/morales_pastor_2025/zenodo_prefcoup_cb2r/prefcoup_cb2r-v.1.0.0.zip`  
SHA256 `e1c6d0308aeef7bd52cd986a8fb7bca940162d895c0e0857dfbde55b6682e061` (4513 B)

**Scope note:** One-shot recovered **WT active** dynamic `2126` (5× ~77 MB xtc + psf + pdb). Mutant dynamics on pub/1540 were **not** bulk-downloaded (API zip requires login; login endpoint returned 500).

### Contingency (Morales-Pastor / paper Data availability)

Paper states additional data may be available on request from authors if not in public repos. **Registered as contingency only — agent did NOT email authors.**

---

## 2. Dutta & Shukla 2023 MSM deposit

| Endpoint | Method | Result |
|----------|--------|--------|
| https://uofi.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4 (paper ID) | HEAD+GET | **404** |
| https://uofi.app.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4 | HEAD+GET | **404** |
| https://app.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4 | HEAD | **404** |
| https://illinois.box.com/s/jzooa0o27z1w9ha0h6va3i51ir7l38j4 | HEAD | **404** |
| README CB2 MSM pkls `…/s/iw1wlcdg44gjs7ufx4rriuulindibj5t` | HEAD+GET | **404** |
| README CB2 apo traj `…/s/xl7tpf345rt8tikjaidfa8rm7gy2wrpj` | HEAD+GET | **404** |
| README CB2 holo active `…/s/3ah3yftcs6e40tytnxgn8cw1g4fzrlir` | HEAD+GET | **404** |
| README CB2 holo inactive `…/s/rkflfcts7vccr4dlw325k65cxfx9fj4s` | HEAD+GET | **404** |
| README features `…/s/ix0hhvbwgwhipqrhk1oe1iwpl021vyw1` | HEAD+GET | **404** |
| README volume/dock `…/s/vyakobq2zbk5xyoxqvccxngif6jzeo0z` | HEAD+GET | **404** |
| https://github.com/ShuklaGroup/Cannabinoid_activation | API tree | **200** — scripts + small figure `.pkl`/`.npy` only; **no** MSM traj deposit |

**Local:** `data/external/dutta_shukla_2023/msm/` exists with `BLOCKED_README.md` only (no binaries).

---

## 3. Path gate / P1

| Path | Ready? |
|------|--------|
| `data/external/morales_pastor_2025/trajectories` | **YES** (MANIFEST + `.xtc`) |
| `data/external/dutta_shukla_2023/msm` | **NO** (Box 404) |

→ `all_ready = false` → **`BLOCKED_PENDING_TRAJECTORIES`** → **P1 cannot start** until Dutta–Shukla MSM arrives (or PI relaxes dual-path gate).

---

## 4. Exact blocker list (remaining)

1. **Box shared link `jzooa0o27z1w9ha0h6va3i51ir7l38j4`:** HTTP **404** on all host variants tried (uofi.box.com, uofi.app.box.com, app.box.com, illinois.box.com).  
2. **All ShuklaGroup README Box mirrors for CB2 MSM/traj:** HTTP **404**.  
3. **GPCRmd bulk API downloader:** requires account; `/accounts/login/` returned **500** this session (direct WT file URLs worked without login).  
4. **Author-request contingency** for Morales-Pastor extras: registered, **not** executed.

`RECOVERY_ATTEMPT = DONE` (one-shot closed).
