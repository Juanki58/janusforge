# EXTERNAL — ESMDynamic soft proxy (human CB2 / P34972)

**Generated (UTC):** `2026-09-12T12:00:24.325943+00:00`
**Branch:** `feat/cb2-hubs-functional-topology-test`
**Pre-reg:** `docs\synthesis\EXPERIMENT_CB2_ESMDYNAMIC.md`

## Epistemology

- AI/sequence proxy only — **not** MSM-state contact probabilities.
- Does **not** reopen P2 as CONVERGENT; no Gi claim.
- No experimental validation of ESMDynamic on CB2 in this lab.
- Verdicts `EXT_ESMDYNAMIC_*` are provisional/soft.

## Verdicts

- **`EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE`**
- Soft compare: `EXT_ESMDYNAMIC_SOFT_COMPARE_NA`
- P2 unchanged: `CLOSED_INSUFFICIENT_SAMPLING`
- Filelist fabrication: `NOT_FABRICATED`
- Fallback: `EXTERNAL_CB2_APO_TM6_TOGGLE_FILENAME`

## Software / data pointers

- Paper DOI: `10.1038/s41467-026-76361-2`
- Code: https://github.com/ShuklaGroup/esmdynamic
- Weights / proteome DOI: `10.13012/B2IDB-3773897_V2`
- Proteome ID: `sp_P34972_CNR2_HUMAN` → archive `human_proteome_preds_04.tar.xz`

## Environment blockers

- `docker_daemon_unavailable`
- `torch_not_installed_in_runner_env`
- `esmdynamic_package_not_installed`
- `gpu_vram_likely_insufficient_for_esmdynamic`
- `proteome_shard_too_large_to_fetch_for_single_protein`
- `esmdynamic_inference_stack_incomplete`

### Notes

- gpu_vram_6144MB_below_comfortable_ESMFold_margin
- proteome_table_lists_CNR2_in_preds_04_shard
- human_proteome_preds_04.tar.xz_is_multi_GB_full_shard_not_fetched_this_session

- docker_daemon_ok=`False`
- torch_ok=`False` cuda_ok=`False` esm_ok=`False`
- GPU=`NVIDIA GeForce GTX 1060 6GB` VRAM_MB=`6144.0`

## PI summary (ES)

ESMDynamic no se pudo ejecutar en esta sesión (Docker daemon caído, sin torch/esmdynamic en el env, VRAM GTX 1060 6 GB insuficiente con margen, y el shard proteoma CNR2 ~multi-GB). Veredicto: EXT_ESMDYNAMIC_INDETERMINATE_UNAVAILABLE. No sustituye contactos MSM; no reabre P2. Se ejecuta el fallback TM6/toggle sobre CB2_APO local.

## Forbidden claims (reminder)

- No MSM substitute; no P2 CONVERGENT; no Gi; no fake filelist alignment.

## Artifact SHA256

- `cb2_esmdynamic.json`: `910ef31a2e0863417a03f4ccc5f1831aedc0ae7a7fcc3830c25ca975b3bd9460`
- prereg `EXPERIMENT_CB2_ESMDYNAMIC.md`: `3b48e7290dcb0fe2af3c57f26731b8a11edff6b28b6f85c03a614eedfc236ffe`
- script `cb2_esmdynamic.py`: `965b05b2b53b35250032f375a90a4a9e3ea3c860e1dd8bc6d3b09594fb884159`
