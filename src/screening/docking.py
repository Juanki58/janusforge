"""AutoDock Vina docking helpers (CLI binary + Meeko), adapted from molforge patterns."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from src.chemistry.prepare_ligands import smiles_to_pdbqt

_AFFINITY_RE = re.compile(
    r"REMARK VINA RESULT:\s+(-?\d+\.\d+)",
    re.IGNORECASE,
)


def resolve_vina(explicit: str | None = None, root: Path | None = None) -> Path:
    """Locate vina.exe / vina. Prefer explicit path, then local tools/, then sibling molforge."""
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if root is None:
        root = Path.cwd()
    candidates.extend(
        [
            root / "tools" / "vina.exe",
            root / "tools" / "vina",
            Path("tools/vina.exe"),
            Path("tools/vina"),
            Path("vina.exe"),
            Path("vina"),
            root.parent / "molforge" / "tools" / "vina.exe",
            root.parent / "molforge" / "tools" / "vina",
        ]
    )
    for path in candidates:
        if path.exists():
            return path.resolve()
    raise FileNotFoundError(
        "Binario Vina no encontrado. Coloca tools/vina.exe (Windows) desde "
        "https://github.com/ccsb-scripps/AutoDock-Vina/releases "
        "o configura docking.vina_binary en configs/cb1_cb2.yaml "
        "(también se busca en ../molforge/tools/vina.exe)."
    )


def parse_best_affinity(pdbqt_text: str) -> float | None:
    match = _AFFINITY_RE.search(pdbqt_text)
    return float(match.group(1)) if match else None


def dock_ligand(
    smiles: str,
    name: str,
    receptor: Path,
    box: dict,
    work_dir: Path,
    vina_path: Path,
    exhaustiveness: int = 8,
    num_modes: int = 9,
    seed: int = 42,
    ph: float = 7.4,
    reuse_ligand_pdbqt: Path | None = None,
) -> dict:
    """Dock one ligand; affinity in kcal/mol (more negative = better)."""
    work_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:80]
    lig_pdbqt = work_dir / f"{safe}_lig.pdbqt"
    out_pdbqt = work_dir / f"{safe}_docked.pdbqt"
    log_path = work_dir / f"{safe}_vina.log"
    sdf_path = work_dir / f"{safe}_lig.sdf"

    if out_pdbqt.exists():
        affinity = parse_best_affinity(
            out_pdbqt.read_text(encoding="utf-8", errors="replace")
        )
        if affinity is not None:
            return {
                "name": name,
                "smiles": smiles,
                "vina_affinity": affinity,
                "dock_error": None,
                "docked_pdbqt": str(out_pdbqt),
                "ligand_pdbqt": str(lig_pdbqt) if lig_pdbqt.exists() else None,
            }

    try:
        if reuse_ligand_pdbqt and Path(reuse_ligand_pdbqt).exists():
            lig_pdbqt.write_text(
                Path(reuse_ligand_pdbqt).read_text(encoding="utf-8"), encoding="utf-8"
            )
        else:
            smiles_to_pdbqt(
                smiles,
                lig_pdbqt,
                name=name,
                seed=seed,
                ph=ph,
                sdf_path=sdf_path,
            )
    except Exception as exc:  # noqa: BLE001
        log_path.write_text(f"ligand prep failed: {exc}\n", encoding="utf-8")
        return {
            "name": name,
            "smiles": smiles,
            "vina_affinity": None,
            "dock_error": f"prep: {exc}"[:300],
            "docked_pdbqt": None,
            "ligand_pdbqt": None,
        }

    cmd = [
        str(vina_path),
        "--receptor",
        str(receptor),
        "--ligand",
        str(lig_pdbqt),
        "--out",
        str(out_pdbqt),
        "--center_x",
        str(box["center_x"]),
        "--center_y",
        str(box["center_y"]),
        "--center_z",
        str(box["center_z"]),
        "--size_x",
        str(box["size_x"]),
        "--size_y",
        str(box["size_y"]),
        "--size_z",
        str(box["size_z"]),
        "--exhaustiveness",
        str(exhaustiveness),
        "--num_modes",
        str(num_modes),
        "--seed",
        str(seed),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    log_path.write_text(
        (proc.stdout or "") + "\n" + (proc.stderr or ""),
        encoding="utf-8",
    )
    if proc.returncode != 0 or not out_pdbqt.exists():
        return {
            "name": name,
            "smiles": smiles,
            "vina_affinity": None,
            "dock_error": (proc.stderr or proc.stdout or "vina failed")[:300],
            "docked_pdbqt": None,
            "ligand_pdbqt": str(lig_pdbqt),
        }

    affinity = parse_best_affinity(out_pdbqt.read_text(encoding="utf-8"))
    return {
        "name": name,
        "smiles": smiles,
        "vina_affinity": affinity,
        "dock_error": None,
        "docked_pdbqt": str(out_pdbqt),
        "ligand_pdbqt": str(lig_pdbqt),
    }
