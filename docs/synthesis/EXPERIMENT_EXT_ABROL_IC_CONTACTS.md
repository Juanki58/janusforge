# Experiment — EXTERNAL: Abrol Zenodo IC contact inventory (Gi vs βarr2 avg frames)

**Fecha pre-registro:** 2026-09-22  
**Rama:** `feat/cb2-hubs-functional-topology-test`  
**Modo:** `DATA_BLIND_PREREGISTRATION`  
**Scope:** **`EXTERNAL_ABROL_IC_CONTACTS`** — inventario de contactos en la cara **intracelular** CB2↔efector desde **average PDB frames** Zenodo (Heo & Abrol). Puente descriptivo **hacia P3**, **sin** declarar P3 hecho ni eficacia Gi.  
**PI authorization:** YES ([`PUBLIC_DATA_LEADS_CB2.md`](PUBLIC_DATA_LEADS_CB2.md) §3 Abrol / §4 opcional).

---

## Epistemology (HARD)

| Allowed | Forbidden |
|---------|-----------|
| Descargar **solo** zip de PDBs avg/start (~97 MB) | Descargar traj zip ~375 MB salvo fallo de avg-only |
| Contactos VdW+0.5 (o Cα≤8 Å fallback) CB2-IC ↔ efector | Claim “Gi coupling mechanism resolved” |
| Comparar sets Gi-Empty / Gi-GDP vs BARR2 (WT) | Reabrir P3 = DONE; reabrir P2; hub hunt |
| Veredicto `EXT_ABROL_IC_*` | Preferencias funcionales / bias scores |

```text
P3_EFFECTOR                     = BLOCKED                      # unchanged as project gate
P2_MSM_TRANSITIONS              = CLOSED (INSUFFICIENT_SAMPLING)
EXT_ABROL_IC_*                  = NEW (EXTERNAL inventory toward P3)
Gi_FUNCTIONAL_CLAIM             = FORBIDDEN
AVG_FRAME ≠ ENSEMBLE_MSM        = TRUE
```

**Explicit non-claim:**

> Average frames de complejo efector **≠** MSM de activación apo.  
> Diferencias de contacto IC Gi vs βarr2 son **inventario estructural EXTERNAL**, no veredicto de sesgo funcional ni cierre de P3.

**Pregunta discriminante:**

> En avg frames WT publicados, ¿el conjunto de contactos CB2-IC↔efector **difiere** entre Gi (Empty/GDP) y βarr2 (± fosfo-C), y esos contactos intersectan hubs/TM3–TM6 IC del repo — sin afirmar función?

---

## Data (locked)

| Item | Value |
|------|--------|
| Zenodo concept | [10.5281/zenodo.14227795](https://doi.org/10.5281/zenodo.14227795) |
| Preferred record | latest `14232007` (same PDB zip as `14227796`) |
| File used | `PDB files for signaling complex starting and average structures.zip` |
| Local | `data/external/abrol_heo_2024/` (zip **gitignored**) |
| Paper | Heo & Abrol *BBRC* [10.1016/j.bbrc.2024.151100](https://doi.org/10.1016/j.bbrc.2024.151100) |

### Systems (primary WT set)

| Label | Avg PDB (basename pattern) |
|-------|----------------------------|
| WT_Gi_Empty | `CB2R-WT-NoPhosphoC_Gi-Empty_avgframe*` |
| WT_Gi_GDP | `CB2R-WT-NoPhosphoC_Gi-GDP_avgframe*` |
| WT_BARR2_NoP | `CB2R-WT-NoPhosphoC_BARR2_avgframe*` |
| WT_BARR2_P | `CB2R-WT-PhosphoC_BARR2_avgframe*` |

Mutants Q63R / L133I = **optional appendix**; not required for primary call.

### IC residue window (CB2, UniProt P34972 — locked)

Intracellular face approximation for contact endpoints on receptor:

- ICL1 / TM2 IC: residues **60–80**  
- ICL2 / DRY region: **130–150**  
- ICL3 / TM5–TM6 IC: **215–250**  
- TM7 IC / H8: **290–320**

Effector atoms: any protein residue **not** in CB2 chain (Gi or βarr2). Chain IDs discovered from PDB (fail-closed if ambiguous).

### Contact definition

Primary: heavy-atom pair within `r_vdw(i)+r_vdw(j)+0.5` Å (same spirit as network_core contacts).  
Fallback if VdW tables awkward: Cα–Cα ≤ 8 Å between CB2-IC window and effector.

---

## Metrics (locked)

For each system report:

1. `n_contacts` CB2-IC↔effector  
2. `n_CB2_residues_in_contact`  
3. Intersection with six hubs / hub 1-hop if any  
4. Pairwise Jaccard of contact residue-sets: Gi_Empty vs BARR2_P; Gi_Empty vs Gi_GDP; BARR2_NoP vs BARR2_P  

Aggregates:

- `jaccard_GiEmpty_vs_BARR2P`  
- `frac_hub_residues_touching_effector` (hubs that appear in any contact)

---

## Verdict rules

| Call | Criterio |
|------|----------|
| **`EXT_ABROL_IC_EFFECTOR_DISTINCT`** | Jaccard(Gi_Empty, BARR2_P) **< 0.50** on CB2 contact-residue sets **and** both systems have ≥20 contacts |
| **`EXT_ABROL_IC_EFFECTOR_SIMILAR`** | Jaccard ≥ 0.70 |
| **`EXT_ABROL_IC_EFFECTOR_PARTIAL`** | 0.50 ≤ Jaccard < 0.70 **or** mixed Gi-GDP |
| **`EXT_ABROL_IC_INDETERMINATE_MISSING_DATA`** | Download/extract/chain ID fails |
| **`EXT_ABROL_IC_INDETERMINATE_NUMBERING`** | CB2 residue numbering vs UniProt cannot be validated (≥50 matched IC residues required) |

**P3 status annotation (mandatory):** `P3_PROJECT_GATE = BLOCKED` — this EXTERNAL inventory does **not** complete P3.

---

## Outputs

| Artefacto | Path |
|-----------|------|
| Pre-reg | `docs/synthesis/EXPERIMENT_EXT_ABROL_IC_CONTACTS.md` |
| Script | `scripts/network_core/ext_abrol_ic_contacts.py` |
| Report | `results/network_core/ext_abrol_ic_contacts.md` |
| JSON | `results/network_core/ext_abrol_ic_contacts.json` |

---

## Fail-closed

- If zip download fails → `INDETERMINATE_MISSING_DATA` (no fake contacts).  
- Never claim Gi signaling efficacy from avg-frame contacts.  
- Do not unpack MD trajectories.zip unless avg PDB path blocked.

---

*Fin pre-registro. EXTERNAL toward P3; P3 not done; no Gi claim.*
