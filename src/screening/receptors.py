"""Download / clean CB1–CB2 PDB structures and prepare Vina PDBQT receptors."""

from __future__ import annotations

import json
import shutil
import subprocess
import urllib.request
from pathlib import Path

# Common crystallographic junk / lipids to ignore when picking the co-ligand
_SKIP_RESNAMES = {
    "HOH",
    "WAT",
    "SOL",
    "NA",
    "CL",
    "K",
    "MG",
    "CA",
    "ZN",
    "SO4",
    "PO4",
    "GOL",
    "EDO",
    "PEG",
    "PG4",
    "DMS",
    "ACT",
    "ACE",
    "NAG",
    "OLA",
    "OLC",
    "OLE",
    "PLM",
    "STE",
    "CLR",
    "CHL",
    "P6G",
    "1PE",
    "PGE",
    "BOG",
    "LMT",
    "D10",
    "HEX",
    "UND",
    "FMN",  # flavin in 5TGZ chimera
}


def download_pdb(pdb_id: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and out_path.stat().st_size > 1000:
        return out_path
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    urllib.request.urlretrieve(url, out_path)
    return out_path


def _parse_hetatm_coords(pdb_text: str) -> dict[tuple[str, str, int], list[tuple[float, float, float]]]:
    """Map (resname, chain, resseq) -> list of xyz."""
    groups: dict[tuple[str, str, int], list[tuple[float, float, float]]] = {}
    for line in pdb_text.splitlines():
        if not line.startswith("HETATM"):
            continue
        resname = line[17:20].strip().upper()
        chain = line[21].strip() or "_"
        try:
            resseq = int(line[22:26])
        except ValueError:
            continue
        try:
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
        except ValueError:
            continue
        key = (resname, chain, resseq)
        groups.setdefault(key, []).append((x, y, z))
    return groups


def find_ligand_group(
    pdb_text: str,
    preferred_resname: str | None = None,
) -> tuple[str, str, int, list[tuple[float, float, float]]]:
    """Pick co-crystallized ligand group for box center."""
    groups = _parse_hetatm_coords(pdb_text)
    if preferred_resname:
        pref = preferred_resname.upper()
        matches = [(k, v) for k, v in groups.items() if k[0] == pref]
        if matches:
            # largest atom count among preferred
            (resname, chain, resseq), coords = max(matches, key=lambda kv: len(kv[1]))
            return resname, chain, resseq, coords

    organic = [
        (k, v)
        for k, v in groups.items()
        if k[0] not in _SKIP_RESNAMES and len(v) >= 8
    ]
    if not organic:
        raise RuntimeError(
            "No se encontró ligando co-cristalizado usable para centrar la caja. "
            "Define box.center_* manualmente en configs/cb1_cb2.yaml."
        )
    (resname, chain, resseq), coords = max(organic, key=lambda kv: len(kv[1]))
    return resname, chain, resseq, coords


def centroid(coords: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    n = len(coords)
    return (
        sum(c[0] for c in coords) / n,
        sum(c[1] for c in coords) / n,
        sum(c[2] for c in coords) / n,
    )


def write_ligand_pdb(
    pdb_text: str,
    resname: str,
    chain: str,
    resseq: int,
    out_path: Path,
) -> Path:
    lines = []
    for line in pdb_text.splitlines():
        if not line.startswith("HETATM"):
            continue
        rn = line[17:20].strip().upper()
        ch = line[21].strip() or "_"
        try:
            rs = int(line[22:26])
        except ValueError:
            continue
        if rn == resname.upper() and ch == chain and rs == resseq:
            lines.append(line)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def clean_protein_pdb(
    pdb_text: str,
    out_path: Path,
    chains: list[str] | None = None,
) -> Path:
    """Keep protein ATOM records (optional chain filter); drop HETATM/water."""
    keep = []
    for line in pdb_text.splitlines():
        if line.startswith("ATOM"):
            ch = line[21].strip() or "_"
            if chains and ch not in chains:
                continue
            # drop alternate locations other than A / blank
            alt = line[16]
            if alt not in (" ", "A"):
                continue
            keep.append(line)
        elif line.startswith(("TER", "END")):
            keep.append(line)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(keep) + "\n", encoding="utf-8")
    return out_path


def resolve_mk_prepare_receptor() -> Path:
    scripts = Path(__import__("sys").executable).resolve().parent / "Scripts"
    for name in ("mk_prepare_receptor.exe", "mk_prepare_receptor"):
        p = scripts / name
        if p.exists():
            return p
    found = shutil.which("mk_prepare_receptor")
    if found:
        return Path(found)
    raise FileNotFoundError(
        "mk_prepare_receptor no encontrado (paquete meeko). "
        "pip install meeko>=0.7.1"
    )


def prepare_receptor_pdbqt(
    clean_pdb: Path,
    out_basename: Path,
    box_center: tuple[float, float, float],
    box_size: tuple[float, float, float],
    allow_bad_res: bool = True,
) -> Path:
    """Run Meeko mk_prepare_receptor; return rigid PDBQT path."""
    out_basename.parent.mkdir(parents=True, exist_ok=True)
    # Meeko may write out_basename.pdbqt or out_basename_rigid.pdbqt
    candidates = [
        Path(str(out_basename) + ".pdbqt"),
        Path(str(out_basename) + "_rigid.pdbqt"),
        out_basename.with_suffix(".pdbqt"),
    ]
    existing = next((c for c in candidates if c.exists()), None)
    if existing:
        return existing

    mk = resolve_mk_prepare_receptor()
    cmd = [
        str(mk),
        "--read_pdb",
        str(clean_pdb),
        "-o",
        str(out_basename),
        "-p",
        "-v",
        "--default_altloc",
        "A",
        "--box_center",
        str(box_center[0]),
        str(box_center[1]),
        str(box_center[2]),
        "--box_size",
        str(box_size[0]),
        str(box_size[1]),
        str(box_size[2]),
    ]
    if allow_bad_res:
        cmd.append("-a")
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    log = out_basename.parent / f"{out_basename.name}_mk_prepare.log"
    log.write_text((proc.stdout or "") + "\n" + (proc.stderr or ""), encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(
            f"mk_prepare_receptor failed for {clean_pdb} (rc={proc.returncode}). "
            f"Ver {log}"
        )
    existing = next((c for c in candidates if c.exists()), None)
    if existing is None:
        # also search directory
        found = list(out_basename.parent.glob(f"{out_basename.name}*.pdbqt"))
        if found:
            return found[0]
        raise RuntimeError(f"PDBQT no generado para {out_basename}; ver {log}")
    return existing


def prepare_target(
    pdb_id: str,
    out_dir: Path,
    ligand_resname: str | None,
    box_size: tuple[float, float, float] = (22.0, 22.0, 22.0),
    chains: list[str] | None = None,
) -> dict:
    """Full receptor prep: download → ligand box → clean → PDBQT → box.json."""
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = download_pdb(pdb_id, out_dir / f"{pdb_id.upper()}.pdb")
    text = raw.read_text(encoding="utf-8", errors="replace")

    resname, chain, resseq, coords = find_ligand_group(text, ligand_resname)
    cx, cy, cz = centroid(coords)
    lig_pdb = write_ligand_pdb(
        text, resname, chain, resseq, out_dir / f"{pdb_id.upper()}_ligand.pdb"
    )
    clean = clean_protein_pdb(
        text, out_dir / f"{pdb_id.upper()}_clean.pdb", chains=chains
    )
    rec = prepare_receptor_pdbqt(
        clean,
        out_dir / f"{pdb_id.upper()}_rec",
        box_center=(cx, cy, cz),
        box_size=box_size,
    )
    box = {
        "center_x": round(cx, 3),
        "center_y": round(cy, 3),
        "center_z": round(cz, 3),
        "size_x": float(box_size[0]),
        "size_y": float(box_size[1]),
        "size_z": float(box_size[2]),
        "source": "co-crystallized_ligand_centroid",
        "ligand_resname": resname,
        "ligand_chain": chain,
        "ligand_resseq": resseq,
        "ligand_natoms": len(coords),
        "ligand_pdb": str(lig_pdb),
        "receptor_pdbqt": str(rec),
        "pdb_id": pdb_id.upper(),
    }
    box_path = out_dir / "box.json"
    box_path.write_text(json.dumps(box, indent=2), encoding="utf-8")
    return box
