# MD plan — Membrane POPC 20 ns: JANUS_H1_02c vs Δ9-THCV vs Δ9-THC on CB1 inactive (5TGZ)

> **No SMILES / no coordinates.** Poses and trajectories stay local (`results/docking/…`, `results/md/membrane/…`).  
> Script: [`scripts/run_md_openmm_membrane_lead.py`](../../scripts/run_md_openmm_membrane_lead.py) · env: [`environments/environment-md-membrane.yml`](../../environments/environment-md-membrane.yml)  
> Prior soluble MD: [`md_lead_plan.md`](md_lead_plan.md) · [`md_lead_2ns_summary.md`](md_lead_2ns_summary.md)

## Pregunta

En **CB1 inactivo (5TGZ)** embebido en **bilayer POPC explícita** + agua + NaCl 0.15 M, ¿el lead **JANUS_H1_02c** congela mejor el pozo inactivo (TM6 / TM3–TM6 / H-bond fenólico) que **Δ9-THCV**, y se diferencia del agonista control **Δ9-THC** (que debería “abrir” TM3–TM6)?

Esto es el escalón **A1+A3** tras MD corta en agua (resultado mixto / débil). **No** prueba agonismo ni Janus α.

## Panel (triplete)

| Rol | ID docking | Alias CLI |
|-----|------------|-----------|
| Lead | JANUS_H1_02c | `h1_02c` |
| Referencia neutra | delta9-THCV | `thcv` |
| Agonista control | delta9-THC | `thc` |
| Los tres | — | `all` (default) |

## Protocolo

| Elemento | Elección |
|----------|----------|
| Proteína | `amber14-all.xml` |
| Lípidos | **POPC** vía `amber14/lipid17.xml` |
| Ligando | **GAFF2** (`gaff-2.11`) OpenFF + `GAFFTemplateGenerator` |
| Construcción membrana | AmberTools **`packmol-memgen -l POPC -r 1 --preoriented --keepligs`**. Script orienta TM→Z (PCA). **No** usar `--solvate` (v2025 = agua sin lípidos). MEMEMBED+ligand está roto en AmberTools 2025.1 — por eso `--preoriented`. |
| Iones | neutralizar + **NaCl 0.15 M** |
| Barostato | `MonteCarloMembraneBarostat` XY isotrópico / Z libre, 1 atm, γ=0 |
| Minimización | 5000 steps |
| Equilibrio | NVT corto + NPT membrana ~**1 ns** (default `--` via config `equil_ps`) |
| Producción | NPT **20 ns** (`--ns 20`), 300 K, seed 42 |
| TM3 / TM6 | UniProt 185–220 / 332–369 (mismo criterio que MD soluble) |

### Métricas

1. **RMSD Cα TM6** vs frame minimizado  
2. **Distancia COM** Cα **TM3–TM6**  
3. **Ángulo de ejes** TM3–TM6 (PCA de Cα; grados) — THC esperado más “abierto” vs estado inactivo  
4. **Persistencia H-bond fenólico** (% frames; OH ligando → aceptores proteína, 3.5 Å)

Salida agregada (gitignored): `results/md/membrane/h1_02c_vs_thcv_vs_thc_5tgz_popc.csv`  
Por ligando: `results/md/membrane/<ligand_id>/`

## Criterio go / no-go (Track 1)

**GO — congelar Track 1 computacional → partner ensayo in vitro** si, en membrana:

1. H1_02c **congela TM6** (menor RMSD medio) **mejor que THCV**, **y**  
2. H1_02c restringe **TM3–TM6** (distancia y/o ángulo más estables / menos abiertos) **mejor que THCV**, **y**  
3. H1_02c **recupera** persistencia H-bond fenólico **vs THCV** (en agua el lead iba peor: 55% vs 100%), **y**  
4. El patrón se **diferencia de THC** (agonista: TM3–TM6 más abierto / TM6 más móvil relativo al lead).

**NO-GO — andamiaje fitocannabinoide agotado → evaluar Opción D (URB447 / Yin-Yang)** si:

- H1_02c no mejora el panel vs THCV en membrana, **o**  
- se parece a THC (abre / no trinquete), **o**  
- H-bond fenólico sigue colapsado sin compensación clara en TM6/TM3–TM6.

### Lectura crítica (obligatoria)

**20 ns × 1 réplica no es prueba definitiva.** Un go aquí es un **gate de priorización** para ensayo, no evidencia funcional. Documentar y planificar:

- ≥3 seeds / réplicas independientes  
- ventanas ≥50–100 ns si el go es marginal  
- controles estructurales (RMSD membrana, área/lípido, thickness)  
- Vina pose ≠ ensemble unido

## Cómo lanzar

### Dry-run (valida las 3 poses)

```bash
python scripts/run_md_openmm_membrane_lead.py --dry-run --ligand all
```

### Producción 20 ns × 3 (Linux / Docker GPU)

```bash
# Env dedicado
conda env create -f environments/environment-md-membrane.yml
conda activate janus_md_membrane

python scripts/run_md_openmm_membrane_lead.py --ns 20 --ligand all --platform CUDA

# Un solo ligando / smoke / solo build
python scripts/run_md_openmm_membrane_lead.py --ligand h1_02c --ns 0.01 --platform CUDA
python scripts/run_md_openmm_membrane_lead.py --ligand thc --build-only --platform CUDA
```

### Windows host → Docker (mismo volumen `janus_md_mamba` del run 2 ns)

```powershell
# Asegurar packmol en el env janus_md (ambertools ya incluye packmol_memgen)
docker run --rm -v janus_md_mamba:/opt/conda -v "${PWD}:/work" -w /work `
  mambaorg/micromamba:2 bash -lc `
  "micromamba install -y -n janus_md -c conda-forge packmol && micromamba run -n janus_md python scripts/run_md_openmm_membrane_lead.py --dry-run --ligand all"

# Producción background
docker rm -f janus_md_memb20 2>$null
docker run -d --name janus_md_memb20 --gpus all `
  -v janus_md_mamba:/opt/conda -v "${PWD}:/work" -w /work `
  mambaorg/micromamba:2 bash -lc `
  "micromamba run -n janus_md python scripts/run_md_openmm_membrane_lead.py --ns 20 --ligand all --platform CUDA 2>&1 | tee /work/results/md/membrane/run_20ns_docker.log; echo EXIT_CODE=`$? | tee -a /work/results/md/membrane/run_20ns_docker.log"
```

## Estimación wall-time (GTX 1060 6GB)

| Sistema | Átomos (orden) | Velocidad esperada | 20 ns |
|---------|----------------|--------------------|-------|
| Soluble TIP3P (ref. 2 ns) | ~50–80k | ~57–59 ns/día | — |
| POPC + agua (este plan) | ~150–250k | **~15–30 ns/día** (estimación) | **~0.7–1.3 días / ligando** |

**Triplete 20×3 ≈ 2–4 días wall** en una sola GPU GTX 1060 (secuencial). Equilibración ~1 ns/ligando añade ~1–2 h. Build `packmol_memgen` ≈ minutos–decenas de minutos / sistema.

Si la GPU está ocupada o el build falla, el dry-run y `--build-only` siguen siendo útiles para validar inputs.

## Limitaciones

1. **1 réplica / 20 ns** — ruido térmico y sesgo de pose inicial; no cierra gates funcionales.  
2. **5TGZ quimera** (flavodoxina strip; ICL3 gap) ≠ CB1 nativo completo.  
3. **Orientación membrana** depende de `packmol_memgen` (eje z); revisar visualmente thickness / tilt.  
4. **H-bond fenólico** flexible (cualquier aceptor proteína O/N), no fijado a S7.39.  
5. AmberTools / `packmol_memgen` **no en win-64** — Docker/WSL obligatorio en Windows.  
6. Alternativa CHARMM-GUI / MemProtMD aceptable si se pasa el PDB embebido con `--prebuilt-pdb` (local, sin push).

## IP

- No push de coordenadas / SMILES / DCD / PDB de membrana.  
- Informes públicos: IDs, métricas numéricas, veredicto go/no-go — **sin estructuras**.
