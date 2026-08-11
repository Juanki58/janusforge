# MD 20 ns — Membrane POPC: JANUS_D2_22 on CB1 inactive (5TGZ)

> **Public report:** no SMILES, no coordinates. Trajectories / CSV / DCD / PDB stay local under `results/md/membrane/` (gitignored).  
> Script: [`scripts/run_md_openmm_membrane_lead.py`](../../scripts/run_md_openmm_membrane_lead.py) · prior membrane panel: [`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md) · docking lead: [`option_d_batch_d1_gate_summary.md`](option_d_batch_d1_gate_summary.md) · precedentes: [`docs/mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md)

## Run status

| Item | Value |
|------|--------|
| Ligand | **JANUS_D2_22** (Opción D / Batch D1 lead; Bz_pCF3; dual Vina = −11.277) |
| Receptor | 5TGZ CB1 chimera (same strip as prior membrane MD) |
| Membrane | POPC bilayer (`amber14/lipid17`) + TIP3P + NaCl 0.15 M |
| FF | Protein `amber14-all`; ligand **GAFF2** (`gaff-2.11` via OpenFF) |
| Protocol | Min → NVT + NPT membrane equil ~1 ns → **NPT production 20.0 ns**, 300 K, seed 42 |
| Platform | OpenMM **CUDA** (Docker `janus_md_memb20_d2_22`) |
| Frames | 2000 |
| Container | Exited (0) |
| Log | `results/md/membrane/run_20ns_d2_22_docker.log` → **`EXIT_CODE=0`** |
| Wall clock | ~2026-08-10T14:24Z → 2026-08-11T02:34Z |
| Status | **OK — production + metrics complete** |

TM ranges (UniProt): TM3 185–220; TM6 332–369. RMSD vs minimized frame of this trajectory. H-bond proxy = % frames with ligand OH (C–O–H style O) → protein O/N within 3.5 Å (same flexible criterion as prior membrane batch; **not** a classic phytocannabinoid phenol for this scaffold).

## Hard metrics (production 20 ns)

| Metric | JANUS_D2_22 |
|--------|------------:|
| TM6 Cα RMSD mean ± sd (Å) | **1.03 ± 0.33** |
| TM6 Cα RMSD final (Å) | 1.77 |
| TM3–TM6 COM mean ± sd (Å) | **12.35 ± 0.28** |
| TM3–TM6 COM final (Å) | 12.26 |
| TM3–TM6 axis angle mean ± sd (°) | 10.26 ± 2.14 |
| OH→protein H-bond persistence (%) | **67.4** |

Sources: `results/md/membrane/JANUS_D2_22/metrics_summary.json`, `frame_metrics.csv`, `production.dcd` (~1.70 GB; gitignored). Aggregate CSV: `results/md/membrane/d2_22_5tgz_popc.csv`.

## Comparison vs prior membrane panel (THCV / H1_02c / THC)

Numbers from [`md_membrane_20ns_summary.md`](md_membrane_20ns_summary.md) (same protocol, 1 replica × 20 ns each):

| Metric | JANUS_D2_22 | JANUS_H1_02c | delta9-THCV | delta9-THC |
|--------|------------:|-------------:|------------:|-----------:|
| TM6 Cα RMSD mean ± sd (Å) | **1.03 ± 0.33** | 1.31 ± 0.22 | 1.20 ± 0.22 | 1.22 ± 0.21 |
| TM6 Cα RMSD final (Å) | 1.77 | 1.46 | 1.48 | 1.73 |
| TM3–TM6 COM mean ± sd (Å) | 12.35 ± 0.28 | **11.93 ± 0.30** | 13.07 ± 0.26 | 12.06 ± 0.26 |
| TM3–TM6 axis angle mean ± sd (°) | 10.26 ± 2.14 | 12.98 ± 1.23 | 13.78 ± 1.10 | **10.04 ± 1.11** |
| H-bond persistence (%) | 67.4 | 84.6 | **89.1** | 33.5 |

Reading (geométrico, no funcional):

1. **TM6:** D2_22 tiene la **media más baja** del cuarteto (≈0.2 Å bajo THCV), compatible con TM6 más “fría” vs el panel fitocannabinoide — pero la **sd es mayor** (0.33 vs ~0.22) y el **final** (1.77 Å) se parece a THC, no a un congelamiento monótono.
2. **COM TM3–TM6:** 12.35 Å — más cerrado que THCV (13.07), casi en la banda H1_02c/THC (~11.9–12.1). No hay separación clara tipo “antagonista abre menos / agonista abre más”.
3. **Ángulo de ejes:** solapa con THC (~10°), no con THCV/H1 (~13–14°).
4. **H-bond proxy:** 67.4% queda entre THC (33.5) y el panel fenólico Track 1 (85–89). En andamiaje Opción D esto es **persistencia OH genérica del pipeline**, no el fenol de THCV; no rankear como “peor fenol que H1”.

## Veredicto frío — ¿trinquete? ¿go / no-go vs mapa Janus?

**NO-GO de trinquete CB1. D2_22 descartado como lead funcional** (ex-lead docking únicamente). El “go exploratorio débil” previo queda **superseded** por el análisis de falla abajo.

| Pregunta | Respuesta fría |
|----------|----------------|
| ¿MD terminó OK? | **Sí** (`EXIT_CODE=0`, `status: ok`, 2000 frames) |
| ¿Hay blow-up / inestabilidad catastrófica de TM6? | **No** a esta escala (RMSD media ~1 Å) |
| ¿Evidencia de trinquete térmico CB1 inactivo superior a THCV? | **Parcial / no concluyente:** media TM6 mejor que THCV; patrón COM/ángulo **solapa con THC**; 1 réplica |
| ¿Prueba de perfil Janus (CB1-ant / CB2-ago) o antifibrosis? | **No** — esto es solo geometría CB1 5TGZ en POPC |
| ¿Supera precedentes del mapa (URB447, GW405833, AM1710, Qiu-14)? | **No evaluable aquí** — el mapa es farmacología experimental; este run no mide Ki/IC₅₀ ni bifuncionalidad |

Contexto mapa ([`mapa_ligandos_janus_cb1_cb2.md`](../../docs/mapa_ligandos_janus_cb1_cb2.md)): D2_22 fue el top dual Vina Opción D (−11.277) y queda como *ex-lead docking*. Los precedentes documentan bifuncionalidad **experimental** en otras familias; **ninguno** de esos cuatro tiene métricas MD comparables en este repo. Este 20 ns **no** autoriza claim de “mejor que URB447/Qiu-14”; sí basta, con el matiz de 1 réplica, para **cerrar** D2_22 como eje de trinquete.

**Gate operativo (superseded 2026-08-11):** el análisis de falla abajo **descarta D2_22 como lead funcional** (NO-GO trinquete). Ya no se mantiene como eje prioritario de cómputo.

## Análisis de la falla biofísica

Decisión de usuario tras auditoría de métricas (2026-08-11). Matiz obligatorio: **1 réplica × 20 ns** — priorización / evidencia en contra del trinquete, no prueba de agonismo ni de farmacología Janus.

1. **Descarte D2_22 como lead funcional** — **NO-GO trinquete CB1.** El andamiaje Opción D / Bz_pCF3 no pasa el gate geométrico de contención del estado inactivo frente al panel de referencia. D2_22 queda como *ex-lead de docking* (histórico Batch D1), no como candidato a escalar.
2. **COM TM3–TM6 12.35 Å ≈ régimen THC (12.06 Å), no contención THCV (13.07 Å).** El overlap con THC es **evidencia en contra** de un trinquete tipo contención inactiva más abierta (lectura THCV en este panel), **no** prueba de agonismo. Con una sola réplica no se clasifica eficacia; sí se niega el claim de “congela mejor que THCV / abre menos que el agonista de referencia”.
3. **TM6 RMSD bajo = hélice estable pero “atrapada” en estado más abierto.** Media TM6 fría (1.03 Å) indica que la hélice no explota; la hipótesis operativa es que la **torsión carboxamida / Bz_pCF3 no bloquea TM6** en la geometría deseada — estabilidad ≠ contención funcional del trinquete.
4. **Vina −11.277 no predice restricción funcional** — segunda vez tras Serie H1 (H1_02c: PASS docking → NO-GO membrana). Score dual alto ≠ trinquete CB1.
5. **GPU liberada → pausa de cómputo pesado.** No más MD / docking masivo hasta autorización explícita de la siguiente iteración.
6. **Siguiente eje metodológico (solo plan):** andamiaje **pirazol rígido** tipo Compuesto 14 (Qiu 2023; S173/TM6), sin margen de rotación de la carboxamida flexible. Documentado en [`next_iter_pyrazole_qiu_plan.md`](next_iter_pyrazole_qiu_plan.md) — **sin** lanzar docking ni MD ahora.

## Limitations (must read)

1. **1 réplica / 20 ns** — ruido térmico y sesgo de pose Vina inicial; priorización, no prueba funcional.
2. **Solo CB1 inactivo (5TGZ)** — no hay MD CB2 activo (6PT0) en este informe; Janus requiere ambos brazos.
3. **Quimera 5TGZ** (flavodoxina strip; ICL3 gap) ≠ CB1 nativo completo.
4. H-bond = proxy flexible OH→proteína del script; en D2_22 **no** equivale al fenol fitocannabinoide ni a un contacto fijado (p. ej. S7.39 / morfolina–S173).
5. Sin controles de integridad de membrana reportados aquí (área/lípido, thickness).
6. Comparación vs THCV/H1/THC es **cross-run** del mismo protocolo, no co-simulada en un único sistema.

## Local artifacts (gitignored)

- Log: `results/md/membrane/run_20ns_d2_22_docker.log` (`EXIT_CODE=0`; container end 2026-08-11T02:34:43Z)
- Aggregate CSV: `results/md/membrane/d2_22_5tgz_popc.csv`
- Per ligand: `results/md/membrane/JANUS_D2_22/{production.dcd,metrics_summary.json,frame_metrics.csv,minimized.pdb,…}`
- **Gráficas locales (ver PNG locales; no en git):**
  - `results/md/membrane/JANUS_D2_22/tm6_ca_rmsd_vs_time.png`
  - `results/md/membrane/JANUS_D2_22/tm3_tm6_com_vs_time.png`
  - `results/md/membrane/JANUS_D2_22/tm3_tm6_angle_vs_time.png`
  - `results/md/membrane/JANUS_D2_22/hbond_vs_time.png`

## Status

**2026-08-11:** membrane MD 20 ns **completo** (`EXIT_CODE=0`). Métricas duras arriba. PNG locales generados desde `frame_metrics.csv`.  
**Decisión funcional:** **D2_22 descartado** como lead (NO-GO trinquete CB1). GPU en pausa. Próximo eje = plan pirazol Qiu-like ([`next_iter_pyrazole_qiu_plan.md`](next_iter_pyrazole_qiu_plan.md)), sin ejecución.
