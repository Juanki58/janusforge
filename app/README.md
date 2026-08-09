# Visor Molecular Janusforge (local)

UI local en español con **FastAPI + 3Dmol.js** para inspeccionar estructuras del proyecto sin subir datos sensibles.

## Cómo abrir

1. **Doble clic** en el acceso directo del Escritorio: `Janusforge Visor`
2. O doble clic en `lanzar_visor.bat` (raíz del repo)
3. Se abre el navegador en [http://127.0.0.1:8765](http://127.0.0.1:8765)

Crear / recrear el acceso directo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\crear_acceso_directo_visor.ps1
```

## Qué hace

- Escanea `results/docking`, `results/md`, `data/targets`
- Clasifica por extensión y nombre (receptor, ligando, complejo, H1_02c, THCV, THC…)
- Asistente inicial: pose docking / comparar 3 ligandos / receptor / ayuda
- Sirve PDB/PDBQT/SDF solo bajo el repo (bloquea path traversal)
- `/api/ask`: reglas locales; si hay `OPENAI_API_KEY` (u `OPENAI_BASE_URL` local), usa LLM con metadatos de paths (sin SMILES)

## Requisitos

- Windows + Python 3.10+ en PATH (no hace falta conda)
- El BAT crea `.venv_visor` e instala `requirements-visor.txt`

## API

| Ruta | Descripción |
|------|-------------|
| `GET /` | UI |
| `GET /api/scan` | Archivos descubiertos |
| `GET /api/structure?path=...` | Contenido de estructura |
| `GET/POST /api/ask` | Asistente |
| `GET /api/health` | Healthcheck |

## Limitaciones

- Trayectorias **DCD** se listan pero no se animan aún
- Archivos muy grandes (>80 MB) no se sirven al canvas
- Datos en `results/` / PDB locales suelen estar gitignored: existen en tu PC, no en el remoto

## Detener

Cierra la ventana de consola del BAT (detiene uvicorn).
