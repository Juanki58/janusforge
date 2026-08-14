"""
Janusforge Visor Molecular — servidor local FastAPI.

Sirve una UI 3Dmol.js y descubre estructuras bajo el repo
(results/docking, results/md, data/targets) sin subir datos sensibles.
"""

from __future__ import annotations

import json
import os
import re
import traceback
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent
SCAN_ROOTS = (
    REPO_ROOT / "results" / "docking",
    REPO_ROOT / "results" / "md",
    REPO_ROOT / "data" / "targets",
)
STRUCTURE_EXTS = {".pdb", ".pdbqt", ".sdf", ".mol2", ".cif", ".mmcif"}
METRICS_EXTS = {".csv", ".json"}
OPTIONAL_TRAJ_EXTS = {".dcd", ".xtc"}
MAX_STRUCTURE_BYTES = 80 * 1024 * 1024  # 80 MB

app = FastAPI(title="Janusforge Visor Molecular", version="1.0.0")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))

static_dir = APP_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

def _is_under_repo(path: Path) -> bool:
    try:
        path.resolve().relative_to(REPO_ROOT.resolve())
        return True
    except (ValueError, OSError):
        return False


def resolve_safe_path(raw: str) -> Path:
    """Resuelve un path relativo o absoluto y bloquea path traversal."""
    if not raw or not str(raw).strip():
        raise HTTPException(status_code=400, detail="Parámetro 'path' vacío.")

    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate

    try:
        resolved = candidate.resolve(strict=False)
    except OSError as exc:
        raise HTTPException(status_code=400, detail=f"Path inválido: {exc}") from exc

    if not _is_under_repo(resolved):
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: el path debe estar dentro del repositorio Janusforge.",
        )
    return resolved


# ---------------------------------------------------------------------------
# Heuristic classifier
# ---------------------------------------------------------------------------

ROLE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("receptor", re.compile(r"(receptor|_rec\b|_rec\.|nofusion|protonated|clean)", re.I)),
    ("ligando", re.compile(r"(ligand|_lig\b|_lig\.|pose|_pose)", re.I)),
    ("complejo", re.compile(r"(complex|system_ready|membrane_system|minimized|packed)", re.I)),
    ("caja", re.compile(r"(\.box\.|_box\b|grid)", re.I)),
    ("metricas", re.compile(r"(metrics|frame_metrics|summary|score|docking)", re.I)),
    ("trayectoria", re.compile(r"(\.dcd$|\.xtc$|trajectory|production)", re.I)),
]

LEAD_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("H1_02c", re.compile(r"(h1[_\-]?02c|janus_h1_02c)", re.I)),
    ("D2_22", re.compile(r"(janus_d2_22|d2[_\-]?22)", re.I)),
    ("Option_D", re.compile(r"(option_d|janus_d2_)", re.I)),
    ("THCV", re.compile(r"(thcv|delta9-thcv|δ9-thcv)", re.I)),
    ("THC", re.compile(r"(delta9-thc|δ9-thc|\bthc\b)", re.I)),
    ("CB1", re.compile(r"(cb1|5tgz)", re.I)),
    ("CB2", re.compile(r"(cb2|6pt0)", re.I)),
]


def classify_file(path: Path) -> dict[str, Any]:
    name = path.name
    stem = path.stem
    ext = path.suffix.lower()
    rel = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    parent = path.parent.name

    file_type = "otro"
    if ext in STRUCTURE_EXTS:
        file_type = ext.lstrip(".")
        if file_type == "mmcif":
            file_type = "cif"
    elif ext in METRICS_EXTS:
        file_type = ext.lstrip(".")
    elif ext in OPTIONAL_TRAJ_EXTS:
        file_type = ext.lstrip(".")

    role = "desconocido"
    haystack = f"{rel} {name} {parent}"
    # Poses Vina *_docked.pdbqt viven bajo results/docking/ — no son "metricas"
    if "_docked" in stem.lower() and ext == ".pdbqt":
        role = "ligando"
    else:
        for label, pat in ROLE_PATTERNS:
            if pat.search(haystack):
                role = label
                break

    if role == "desconocido":
        if ext in METRICS_EXTS:
            role = "metricas"
        elif ext in OPTIONAL_TRAJ_EXTS:
            role = "trayectoria"
        elif ext in {".pdb", ".pdbqt", ".cif"} and "rec" in stem.lower():
            role = "receptor"
        elif ext in {".sdf", ".mol2"} or "_lig" in stem.lower():
            role = "ligando"

    tags: list[str] = []
    for label, pat in LEAD_PATTERNS:
        if pat.search(haystack):
            tags.append(label)

    # Preferencia visual: poses SDF y complejos listos primero
    priority = 50
    if "D2_22" in tags and role == "ligando":
        priority = 8  # Lead Option D
    elif role == "ligando" and ext == ".sdf":
        priority = 10
    elif role == "complejo" and "system_ready" in name.lower():
        priority = 15
    elif role == "complejo" and "minimized" in name.lower():
        priority = 18
    elif role == "receptor":
        priority = 25
    elif role == "ligando":
        priority = 20
    elif role == "metricas":
        priority = 40
    elif role == "trayectoria":
        priority = 90

    size = 0
    try:
        size = path.stat().st_size
    except OSError:
        pass

    return {
        "path": rel,
        "name": name,
        "ext": ext,
        "type": file_type,
        "role": role,
        "tags": tags,
        "size_bytes": size,
        "priority": priority,
        "viewable": ext in STRUCTURE_EXTS and size <= MAX_STRUCTURE_BYTES,
        "parent": parent,
    }


def scan_project() -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    roots_status: list[dict[str, Any]] = []
    allowed_exts = STRUCTURE_EXTS | METRICS_EXTS | OPTIONAL_TRAJ_EXTS

    for root in SCAN_ROOTS:
        exists = root.is_dir()
        count = 0
        if exists:
            for p in root.rglob("*"):
                if not p.is_file():
                    continue
                if p.suffix.lower() not in allowed_exts:
                    continue
                # Evitar basura enorme / logs disfrazados
                if p.name.lower().endswith(".log"):
                    continue
                try:
                    item = classify_file(p)
                except Exception:
                    continue
                files.append(item)
                count += 1
        roots_status.append(
            {
                "path": str(root.relative_to(REPO_ROOT)).replace("\\", "/"),
                "exists": exists,
                "count": count,
            }
        )

    files.sort(key=lambda x: (x["priority"], x["path"]))

    suggestions = _build_suggestions(files)
    return {
        "repo_root": str(REPO_ROOT),
        "roots": roots_status,
        "count": len(files),
        "files": files,
        "suggestions": suggestions,
        "empty": len(files) == 0,
        "help_empty": (
            "No se encontraron estructuras. Genera docking (results/docking) o MD "
            "(results/md), o coloca PDB/PDBQT/SDF en data/targets. "
            "Luego pulsa «Re-escanear»."
        ),
    }


def _build_suggestions(files: list[dict[str, Any]]) -> dict[str, Any]:
    receptors = [f for f in files if f["role"] == "receptor" and f["viewable"]]
    ligands = [f for f in files if f["role"] == "ligando" and f["viewable"]]
    complexes = [f for f in files if f["role"] == "complejo" and f["viewable"]]

    by_tag: dict[str, list[dict[str, Any]]] = {}
    for f in files:
        if not f["viewable"]:
            continue
        for t in f["tags"]:
            by_tag.setdefault(t, []).append(f)

    compare_leads = []
    for lead in ("H1_02c", "THCV", "THC"):
        candidates = [
            f
            for f in by_tag.get(lead, [])
            if f["role"] in ("ligando", "complejo") and f["ext"] in (".sdf", ".pdb")
        ]
        if candidates:
            compare_leads.append(candidates[0])

    # Lead Option D (JANUS_D2_22): prefer CB1 docked pose
    d2_candidates = [
        f
        for f in by_tag.get("D2_22", [])
        if f["role"] == "ligando"
        and f["viewable"]
        and ("_docked" in f["name"].lower() or f["ext"] in (".sdf", ".pdbqt"))
    ]
    d2_cb1 = [f for f in d2_candidates if "CB1" in f["tags"] and "_docked" in f["name"].lower()]
    option_d_pose = (d2_cb1 or d2_candidates or [None])[0]
    option_d_receptor = next(
        (f for f in receptors if "5TGZ" in f["name"].upper() or "CB1" in f["tags"]),
        receptors[0] if receptors else None,
    )

    return {
        "best_receptor": receptors[0] if receptors else None,
        "best_pose": (ligands + complexes)[0] if (ligands or complexes) else None,
        "compare_three": compare_leads if len(compare_leads) >= 2 else compare_leads,
        "leads_found": sorted(
            {
                t
                for f in files
                for t in f["tags"]
                if t in ("H1_02c", "THCV", "THC", "D2_22", "Option_D")
            }
        ),
        "option_d_pose": option_d_pose,
        "option_d_receptor": option_d_receptor,
    }


# ---------------------------------------------------------------------------
# Contextual help (rule-based) + optional LLM
# ---------------------------------------------------------------------------

def rule_assistant(question: str, scan: dict[str, Any]) -> str:
    q = (question or "").strip().lower()
    n = scan.get("count", 0)
    leads = scan.get("suggestions", {}).get("leads_found", [])
    roots = ", ".join(
        f"{r['path']} ({r['count']} archivos)" if r["exists"] else f"{r['path']} (ausente)"
        for r in scan.get("roots", [])
    )

    if n == 0 or "vacío" in q or "no hay" in q or "dónde" in q or "donde" in q:
        return (
            "No hay (o hay pocas) estructuras visibles. Coloca archivos en:\n"
            "• data/targets/ — receptores PDB/PDBQT\n"
            "• results/docking/ — poses SDF/PDBQT\n"
            "• results/md/ — complejos y poses de MD\n"
            f"Estado actual: {roots}\n"
            "Luego pulsa «Re-escanear»."
        )

    if "compar" in q or "tres" in q or "3 ligand" in q:
        if len(leads) >= 2:
            return (
                f"Detecté leads: {', '.join(leads)}. "
                "Elige el modo «Comparar 3 ligandos» en el asistente: cargará las mejores "
                "poses/complejos etiquetados H1_02c, THCV y THC (si existen)."
            )
        return (
            "Para comparar, necesito al menos 2 poses con nombres que incluyan "
            "H1_02c, THCV o THC. Revisa results/md/membrane/ o results/docking/."
        )

    if "receptor" in q:
        best = scan.get("suggestions", {}).get("best_receptor")
        if best:
            return (
                f"Receptor sugerido: {best['path']} (rol={best['role']}). "
                "Usa el modo «Receptor solo» o carga ese archivo desde la lista."
            )
        return "No encontré un receptor claro (*_rec.pdbqt, *clean.pdb, receptor*)."

    if "dock" in q or "pose" in q:
        best = scan.get("suggestions", {}).get("best_pose")
        if best:
            return (
                f"Pose/complejo sugerido: {best['path']}. "
                "Modo «Pose docking»: carga el receptor + la pose del ligando."
            )
        return "No hay poses SDF/PDB detectadas. Ejecuta docking o revisa results/."

    if "dcd" in q or "trayector" in q or "md" in q:
        return (
            "Las trayectorias DCD se listan si existen, pero el visor 3D aún no las "
            "reproduce frame a frame. Por ahora abre minimized.pdb / system_ready.pdb "
            "o la pose SDF del ligando. Soporte DCD: pendiente."
        )

    if "ayuda" in q or "cómo" in q or "como" in q or not q:
        return (
            f"Escaneo: {n} archivos. Leads: {', '.join(leads) or 'ninguno'}.\n"
            "Pasos: 1) Elige un modo en el asistente. 2) Revisa la lista. "
            "3) Clic en un archivo viewable para cargarlo en 3Dmol. "
            "4) Usa estilos (cartoon/sticks/surface) en la barra inferior.\n"
            f"Carpetas: {roots}"
        )

    return (
        f"Tengo {n} archivos indexados. Leads: {', '.join(leads) or 'ninguno'}. "
        "Prueba preguntar: «comparar», «receptor», «pose», «dónde poner archivos» o «md»."
    )


async def maybe_llm_answer(question: str, scan: dict[str, Any]) -> str | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        return None

    # Resumen corto (sin SMILES ni contenido molecular)
    summary_files = [
        {
            "path": f["path"],
            "role": f["role"],
            "type": f["type"],
            "tags": f["tags"],
        }
        for f in scan.get("files", [])[:40]
    ]
    system = (
        "Eres un asistente del Visor Molecular Janusforge (español, breve). "
        "Ayudas a elegir archivos locales ya detectados. No pidas ni inventes SMILES. "
        "No inventes paths que no estén en la lista. Máx 120 palabras."
    )
    user = (
        f"Pregunta: {question}\n"
        f"Archivos detectados (muestra): {json.dumps(summary_files, ensure_ascii=False)}\n"
        f"Sugerencias: {json.dumps(scan.get('suggestions', {}), ensure_ascii=False)}"
    )

    try:
        import httpx

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                f"{base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                    "temperature": 0.2,
                    "max_tokens": 300,
                },
            )
            if resp.status_code >= 400:
                return None
            data = resp.json()
            text = data["choices"][0]["message"]["content"].strip()
            return text or None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    accept = request.headers.get("accept", "")
    payload = {"ok": False, "error": exc.detail, "status": exc.status_code}
    if "text/html" in accept and not request.url.path.startswith("/api/"):
        return HTMLResponse(
            f"<h1>Error {exc.status_code}</h1><p>{exc.detail}</p>"
            f"<p><a href='/'>Volver al visor</a></p>",
            status_code=exc.status_code,
        )
    return JSONResponse(payload, status_code=exc.status_code)


@app.exception_handler(Exception)
async def unhandled_exc_handler(request: Request, exc: Exception):
    tb = traceback.format_exc(limit=8)
    payload = {
        "ok": False,
        "error": str(exc) or exc.__class__.__name__,
        "hint": "Revisa la consola del servidor o reinicia con lanzar_visor.bat",
        "traceback": tb if os.environ.get("VISOR_DEBUG") else None,
    }
    return JSONResponse(payload, status_code=500)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        # Starlette reciente: TemplateResponse(request, name, context)
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "repo_root": str(REPO_ROOT),
                "has_openai": bool(os.environ.get("OPENAI_API_KEY")),
            },
        )
    except Exception as exc:
        return HTMLResponse(
            f"<h1>Error al cargar la plantilla</h1><pre>{exc}</pre>"
            f"<p>¿Existe app/templates/index.html?</p>",
            status_code=500,
        )


@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "repo_root": str(REPO_ROOT),
        "app_dir": str(APP_DIR),
        "openai_configured": bool(os.environ.get("OPENAI_API_KEY")),
    }


@app.get("/api/scan")
async def api_scan():
    try:
        data = scan_project()
        data["ok"] = True
        return data
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Fallo en scan: {exc}") from exc


@app.get("/api/structure")
async def api_structure(path: str = Query(..., description="Path relativo al repo")):
    resolved = resolve_safe_path(path)
    if not resolved.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Archivo no encontrado: {path}. ¿Está generado o gitignored en otro PC?",
        )

    ext = resolved.suffix.lower()
    if ext not in STRUCTURE_EXTS:
        raise HTTPException(
            status_code=415,
            detail=f"Extensión no servible como estructura: {ext}. Usa PDB/PDBQT/SDF/CIF/MOL2.",
        )

    try:
        size = resolved.stat().st_size
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo leer el archivo: {exc}") from exc

    if size > MAX_STRUCTURE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Archivo demasiado grande ({size} bytes). Límite {MAX_STRUCTURE_BYTES}.",
        )

    try:
        text = resolved.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"Error leyendo archivo: {exc}") from exc

    media = "chemical/x-pdb"
    if ext == ".sdf":
        media = "chemical/x-mdl-sdfile"
    elif ext == ".mol2":
        media = "chemical/x-mol2"
    elif ext in {".cif", ".mmcif"}:
        media = "chemical/x-mmcif"
    elif ext == ".pdbqt":
        media = "text/plain"

    return PlainTextResponse(text, media_type=media)


@app.get("/api/metrics")
async def api_metrics(path: str = Query(...)):
    resolved = resolve_safe_path(path)
    if not resolved.is_file():
        raise HTTPException(status_code=404, detail=f"No encontrado: {path}")
    if resolved.suffix.lower() not in METRICS_EXTS:
        raise HTTPException(status_code=415, detail="Solo CSV/JSON de métricas.")
    try:
        if resolved.suffix.lower() == ".json":
            return JSONResponse(json.loads(resolved.read_text(encoding="utf-8", errors="replace")))
        # CSV: primeras líneas como texto
        lines = resolved.read_text(encoding="utf-8", errors="replace").splitlines()
        return {
            "ok": True,
            "path": str(resolved.relative_to(REPO_ROOT)).replace("\\", "/"),
            "preview_lines": lines[:40],
            "total_lines": len(lines),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/ask")
async def api_ask(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    question = str(body.get("question") or body.get("q") or "").strip()
    scan = scan_project()
    llm = await maybe_llm_answer(question, scan)
    if llm:
        return {"ok": True, "source": "llm", "answer": llm}
    return {"ok": True, "source": "rules", "answer": rule_assistant(question, scan)}


@app.get("/api/ask")
async def api_ask_get(q: str = Query("", alias="q")):
    scan = scan_project()
    llm = await maybe_llm_answer(q, scan)
    if llm:
        return {"ok": True, "source": "llm", "answer": llm}
    return {"ok": True, "source": "rules", "answer": rule_assistant(q, scan)}
