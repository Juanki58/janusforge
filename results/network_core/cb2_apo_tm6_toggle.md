# EXTERNAL fallback — CB2_APO TM6/toggle (filename inactive vs active)

**Generated (UTC):** `2026-09-12T12:00:34.071697+00:00`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs\synthesis\EXPERIMENT_CB2_ESMDYNAMIC.md`
**Run mode:** `sample5`

## Epistemology

- Filename `inactive`/`active` = **start-label proxy only** — **≠** MSM macrostate.
- Fallback after `EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE`.
- Does **not** reopen P2 CONVERGENT; no Gi; no fake filelist alignment.

## Verdicts

- **`EXT_APO_TM6_TOGGLE_INDETERMINATE`**
- Soft vs PDB state-dependence narrative: `EXT_APO_TM6_SOFT_NOT_CLEAR_STATE_DEPENDENT`
- Filename ≠ MSM: `True`
- P2 unchanged: `CLOSED_INSUFFICIENT_SAMPLING`

## Mapping

- Alignment identity: `1.0000`
- Median topo−UniProt offset: `-20`
- Note: UniProt P34972 → topo resid; expect ~-20 on Dutta construct

## Primary toggle summary

- |d|≥0.8 among primary 6: **3**/6
- IC opening (active>inactive & |d|≥0.8): **1**/3
- Frames pooled inactive/active: `1000` / `1000`

## Primary features

| role | UniProt | topo | mean_in | mean_act | Δ | d |
|---|---|---|---:|---:|---:|---:|
| Arg3.50-Lys6.35 | [131, 245] | [111, 213] | 10.37 | 15.12 | 4.75 | 6.24 |
| Arg3.50-Asp6.30 | [131, 240] | [111, 208] | 13.73 | 12.69 | -1.04 | -0.49 |
| Arg3.50-Trp6.48 | [131, 258] | [111, 226] | 22.10 | 20.87 | -1.23 | -1.53 |
| Pro5.50-Trp6.48 | [211, 258] | [191, 226] | 23.12 | 20.97 | -2.16 | -2.65 |
| Trp6.48-Asn7.45 | [258, 291] | [226, 259] | 7.23 | 7.10 | -0.13 | -0.13 |
| Trp6.48-Asn7.49 | [258, 295] | [226, 263] | 12.00 | 11.74 | -0.26 | -0.26 |

## Hub-adjacent distances (descriptive)

- `Trp6.48-Asn7.45` UniProt=[258, 291] d=-0.13 Δ=-0.13 Å
- `Trp6.48-Asn7.49` UniProt=[258, 295] d=-0.26 Δ=-0.26 Å
- `Lys6.35-Asn7.45` UniProt=[245, 291] d=0.63 Δ=0.67 Å
- `Asp6.30-Asn7.49` UniProt=[240, 295] d=0.97 Δ=1.64 Å
- `TM6Cterm-Asn7.49` UniProt=[264, 295] d=-0.16 Δ=-0.13 Å
- `Arg3.50-Asn7.49` UniProt=[131, 295] d=-1.83 Δ=-1.89 Å
- `Arg3.50-Asn7.45` UniProt=[131, 291] d=-1.66 Δ=-1.65 Å
- `Ala2.53-Asn7.45` UniProt=[83, 291] d=-0.37 Δ=-0.22 Å
- `Ala2.49-Asn7.45` UniProt=[79, 291] d=-0.35 Δ=-0.16 Å
- `Leu7.41-Asn7.49` UniProt=[287, 295] d=-0.64 Δ=-0.48 Å
- `Arg8.46-Asn7.49` UniProt=[302, 295] d=-1.71 Δ=-1.25 Å

## PI summary (ES)

Fallback TM6/toggle (filename inactive vs active, N_traj=5+5): **EXT_APO_TM6_TOGGLE_INDETERMINATE** — primary pairs |d|≥0.8: 3/6; apertura IC (active>inactive y |d|≥0.8): 1/3. Etiqueta de arranque ≠ macroestado MSM; no reabre P2; no sustituye ESMDynamic ni contactos MSM.

## Forbidden claims

- No MSM substitute; no P2 CONVERGENT; no Gi; filename ≠ metastable state.

## Artifact SHA256

- `cb2_apo_tm6_toggle.json`: `99fdd09f1519532bda2d10e3403b717a479939530fe9ecff808ce202c47f6f04`
- prereg `EXPERIMENT_CB2_ESMDYNAMIC.md` (fallback section): `3b48e7290dcb0fe2af3c57f26731b8a11edff6b28b6f85c03a614eedfc236ffe`
- script `cb2_apo_tm6_toggle.py`: `1ed9e1636a4cca303ab066c0c22c942fc215414a34b5d519a98fe87fc1bdd1a7`
