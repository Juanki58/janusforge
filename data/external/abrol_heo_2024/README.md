# Abrol / Heo 2024 — local EXTERNAL landing (gitignored binaries)

**Zenodo concept:** [10.5281/zenodo.14227795](https://doi.org/10.5281/zenodo.14227795)  
**Paper:** [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100)  
**Analysis:** `scripts/network_core/ext_abrol_ic_contacts.py` → `results/network_core/ext_abrol_ic_contacts.*`

## Local files (NOT committed — `*.zip` / large PDB gitignored)

| File | Role | Notes |
|------|------|-------|
| `PDB_avg_structures.zip` | Avg + start PDBs | sha256 `1bbace2586c238f2c003b00854271456a8612e882823ecacd616758e8db4df2c` (~97 MB) |
| `Zenodo_Readme.txt` | Deposit readme | committed if small; else regenerable from Zenodo |
| `avg_pdbs/CB2R-WT-*_avgframe*.pdb` | Extracted WT avg frames | local only |

**Not downloaded this turn:** `MD trajectories.zip` (~375 MB) — avg frames sufficient for EXTERNAL IC inventory.

**Governance:** EXTERNAL toward P3; `P3_PROJECT_GATE = BLOCKED`; no Gi functional claim; P2 unchanged.
