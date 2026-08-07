# MD plan — Lead #1 JANUS_H1_02c vs Δ9-THCV on CB1 inactive (5TGZ)

> **No SMILES / no coordinates.** Poses and trajectories stay local (`results/docking/…`, `results/md/…`).  
> Script: [`scripts/run_md_openmm_lead.py`](../../scripts/run_md_openmm_lead.py) · deps: [`requirements-md.txt`](../../requirements-md.txt)

## Pregunta

En el receptor **CB1 inactivo** (PDB **5TGZ**), ¿el lead Batch 3 **JANUS_H1_02c** (1′-metilo + bioisóstero de cadena) se comporta como un **trinquete geométrico** frente a **Δ9-THCV**? Métricas de estabilidad del estado inactivo — **no** prueba de agonismo ni de Janus α.

## Inputs (gitignored)

| Rol | Path local típico |
|-----|-------------------|
| Receptor | `data/targets/cb1/5TGZ_clean.pdb` |
| Pose lead | `results/docking/h1_h5_batch3/cb1/JANUS_H1_02c_docked.pdbqt` (Vina MODEL 1) |
| Pose THCV | `results/docking/h1_h5_batch3/cb1/delta9-THCV_docked.pdbqt` |
| Overrides | YAML opcional vía `--config` (paths locales; no commitear poses) |

## Protocolo (OpenMM)

| Elemento | Elección |
|----------|----------|
| Proteína | `amber14-all.xml` |
| Ligando | **GAFF2** (`gaff-2.11`) vía OpenFF Toolkit + `openmmforcefields.GAFFTemplateGenerator` |
| Solvente | caja cúbica **TIP3P** explícita, padding ~1 nm |
| Iones | neutralizar + **NaCl 0.15 M** |
| Minimización | 5000 steps |
| Equilibrio | NVT + NPT cortos ~**100 ps**, 300 K, 1 atm |
| Producción | NPT **2–5 ns** (`--ns`; default **2** en CPU) |
| Seed | 42 (fijo; override `--seed`) |

### Residuos TM (5TGZ / UniProt P21554; GPCRdb CNR1_HUMAN)

Parametrizables en YAML / defaults del script:

- **TM3:** 185–220 (S3.21–R3.56)
- **TM6:** 332–369 (P6.24–G6.61)

5TGZ es quimera CB1–flavodoxina (insert ~1002–1148). El script **elimina el insert** por defecto y conserva tramos UniProt 99–306 y 332–414. ICL3 queda como gap peptídico — aceptable para un primer escalón de coste cero, no para publicar dinámica de bucle.

### Métricas

1. **RMSD Cα TM6** vs frame minimizado  
2. **Distancia COM** de Cα **TM3–TM6**  
3. **Persistencia H-bond fenólico** (% frames; OH ligando → aceptores proteína, corte distancia 3.5 Å)

Salida agregada (gitignored): `results/md/janus_h1_02c_vs_thcv_5tgz.csv`  
Trayectorias / logs: `results/md/<ligand_id>/`

## Cómo lanzar

```bash
# Validar poses + deps (sin MD)
python scripts/run_md_openmm_lead.py --dry-run

# Producción corta (requiere OpenFF+GAFF2 instalables)
python scripts/run_md_openmm_lead.py --ns 2

# Un solo ligando / smoke
python scripts/run_md_openmm_lead.py --ligand JANUS_H1_02c --ns 0.05 --platform CPU
```

### Install (Windows / GAFF2)

OpenFF **no** está usable desde el wheel PyPI yankado `openff-toolkit==0.18.0`. Usar **conda-forge** (ver `requirements-md.txt`):

```bash
conda create -n janus-md -c conda-forge python=3.12 \
  openmm openmmforcefields openff-toolkit ambertools mdtraj pdbfixer rdkit
conda activate janus-md
```

Si OpenFF/GAFF2 faltan, el script hace **dry-run** de inputs y sale con mensaje claro (exit 3 en modo MD).

## Limitaciones (críticas)

1. **Sin membrana explícita** — solo proteína+ligando en agua TIP3P. Helices TM pueden deformarse; no es MD embebida en bilipido.  
2. **MD corta (ns)** mide estabilidad geométrica del complejo en el pozo inactivo — **no** demuestra agonismo, flip bifásico, ni Janus α.  
3. **Vina ≠ α** — las poses de partida son proxy de ocupación; el gap Batch 3 (0.856 kcal/mol vs THC) sigue siendo proxy de docking.  
4. Quimera 5TGZ (mutaciones + flavodoxina) ≠ CB1 nativo completo.  
5. H-bond fenólico: detección flexible (OH–C ligando); no fija un residuo a priori (p.ej. S7.39) para no sesgar si la pose difiere.

## Lectura de resultado (cuando corra)

Comparar lado a lado lead vs THCV: ¿TM6 más quieta / COM TM3–TM6 más estable / fenol más persistente en el lead? Eso **sugiere** trinquete en el estado inactivo; no sustituye ensayo funcional.

## Siguiente = membrane MD (A1+A3)

Resultado 2 ns en agua: mixto / débil ([`md_lead_2ns_summary.md`](md_lead_2ns_summary.md)). **Siguiente paso:** MD en **POPC explícita** 20 ns, panel triplete H1_02c vs THCV vs THC (agonista control), con criterio go/no-go hacia ensayo in vitro u Opción D.

- Plan: [`md_membrane_20ns_plan.md`](md_membrane_20ns_plan.md)  
- Script: `scripts/run_md_openmm_membrane_lead.py`  
- Env: `environments/environment-md-membrane.yml`
