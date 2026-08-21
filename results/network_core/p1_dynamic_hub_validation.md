# P1 — Dynamic hub validation (GPCRmd/1540 WT only)

**Generated (UTC):** `2026-08-21T09:11:52Z`
**Verdict:** `P1_NOT_SUPPORTED`
**Note:** no signal above null in either channel; communication hub-rank Spearman also below pre-registered gate
**Suggested story (non-forced):** `distributed` — One of persistent / persistent+plastic / distributed / state-specific only if supported; else null. state-specific requires MSM (P2 BLOCKED).

## Scope / governance

- 5 WT GPCRmd/1540 replicas + psf/pdb; frozen six hubs.
- Channels **A** (persistence) and **B** (communication) kept **separate**.
- P2–P6 **BLOCKED**. No Dutta MSM, CB1, docking, de novo, Gαi2 reinterpretation.
- Positive P1 = reproducible signal above background — **not** proof hubs are 100% permanent.

## Inputs (SHA256 of 5 trajs)

| File | bytes | sha256 |
|------|------:|--------|
| `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/24307_trj_2126.xtc` | 77700544 | `1fe13c425c67dd1325208af71131b34fdc3407b868f8c2489930c3d81e53e134` |
| `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/24308_trj_2126.xtc` | 77697176 | `6fef31e2ae0e10eac4590be5b9e205a5b29e3b96d4ee64cc0227dd39c3628be4` |
| `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/24309_trj_2126.xtc` | 77595656 | `598ca435644396c1e2503d94d5b75e2469307effe1790a68cc490971b44eadd2` |
| `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/24310_trj_2126.xtc` | 77726792 | `fec3d8115a3a0d47bc45de20fd15baee5d21c0c46d3599e3970b9c4d08953f3d` |
| `data/external/morales_pastor_2025/trajectories/gpcrmd_dyn2126/24311_trj_2126.xtc` | 77651580 | `467c225dea6cca37e94fd7e7521d406446c32fecf34f46e7d98b303290efa99b` |

**Frames/replica:** [399, 399, 399, 399, 399] — XTC header dt may be unreliable; report uses frame counts. GPCRmd/Morales deposit ≈ 400 ns / replica with ~1 frame/ns.

## Exact definitions (frozen a priori)

### A — Contact persistence

- **Name:** `getcontacts_vdw_envelope_plus_alloviz_filters`
- **Geometry:** |AB| < Rvdw(A)+Rvdw(B)+0.5 Angstrom; A,B non-hydrogen
- **p_ij edge threshold:** `0.1` (AlloViz/Morales)
- **Exclude sequential protein contacts:** `True`
- **Limitation:** Full GetContacts chemotypes (hbond angles, pi geometry, water bridges) not reimplemented; persistence uses registered VdW distance envelope only.

### B — Dynamic communication

- **Name:** `DCC_Ca_fluctuation_correlation`
- **Formula:** `DCC_ij = <Δr_i·Δr_j> / (sqrt(<Δr_i·Δr_i>) sqrt(<Δr_j·Δr_j>))`
- **|DCC| edge threshold:** `0.3`
- **Caveat:** Correlation is not causality.

### Null

- `exact_in_out_degree_multiset_match`; n_null(real)=1000; α=0.05; primary(A)=`pct_disconn`; Spearman≥0.7

## Aggregate results

### A — Persistence

- Primary `pct_disconn`: obs=0, p=1, z=nan, null mean±sd=0±0, sig=False
- Strength: obs=39.22, p=0.1828, z=0.9023504722886597
- Betweenness (observed only): 0.2241625816993464
- Per-hub degree: `{'ALA:79': 9, 'ALA:83': 7, 'LEU:287': 8, 'ASN:291': 9, 'ASN:295': 9, 'ARG:302': 7}`
- Per-hub strength: `{'ALA:79': 7.29874686716792, 'ALA:83': 5.986466165413534, 'LEU:287': 6.388972431077694, 'ASN:291': 7.764912280701754, 'ASN:295': 6.349874686716792, 'ARG:302': 5.428070175438596}`

### B — Communication

- Primary `hub_set_strength`: obs=51.49, p=0.999, z=-2.8265715107065335, null mean±sd=56.15±1.649, sig=False
- Strength: obs=51.49, p=0.999, z=-2.8265715107065335
- Betweenness (observed only): 0.14781746031746032
- Per-hub degree: `{'ALA:79': 22, 'ALA:83': 18, 'LEU:287': 12, 'ASN:291': 22, 'ASN:295': 27, 'ARG:302': 16}`
- Per-hub strength: `{'ALA:79': 9.929361562981818, 'ALA:83': 7.965462818608408, 'LEU:287': 4.823319042268877, 'ASN:291': 9.696670723507108, 'ASN:295': 12.02295813876408, 'ARG:302': 7.05268663636081}`

### Reproducibility (hub-rank Spearman across replicas)

- A: 0.9888 (pass=True)
- B: 0.5743 (pass=False)
- Gates: A_pass=False (NULL_NOT_EXCEEDED); B_pass=False (REPRO_FAIL)

## Per-replica summary

| Rep | frames | A p(primary) | A sig | B p(primary) | B sig |
|----:|-------:|-------------:|:-----:|-------------:|:-----:|
| 1 | 399 | 1.0 | False | NA | NA |
| 2 | 399 | 1.0 | False | 0.919080919080919 | False |
| 3 | 399 | 1.0 | False | 0.987012987012987 | False |
| 4 | 399 | 1.0 | False | 0.999000999000999 | False |
| 5 | 399 | 1.0 | False | 0.999000999000999 | False |

## Robustness

### Leave-one-replica-out

| Left out | A_pass | B_pass | A_p | B_p | verdict |
|--------:|:------:|:------:|----:|----:|---------|
| 1 | False | False | 1.0 | 0.988011988011988 | `P1_NOT_SUPPORTED` |
| 2 | False | False | 1.0 | 1.0 | `P1_NOT_SUPPORTED` |
| 3 | False | False | 1.0 | 1.0 | `P1_NOT_SUPPORTED` |
| 4 | False | False | 1.0 | 1.0 | `P1_NOT_SUPPORTED` |
| 5 | False | False | 1.0 | 1.0 | `P1_NOT_SUPPORTED` |

### Traj-length sensitivity (first half frames)

- A: p=1, sig=False
- B: p=1, sig=False

### Bootstrap replicas (n=100, null=200): frac A sig=0.000; frac B sig=0.000

## P1 does NOT answer

- Gi control
- CB2-specificity
- MSM state changes
- membrane
- chemical switch

---

*End P1 report. STOP — no P2.*
