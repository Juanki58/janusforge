"""Minimal PDB parsing / geometry helpers (numpy-only, no BioPython)."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

AtomRec = tuple[str, str, int, str, np.ndarray]  # resname, chain, resseq, atom, xyz


def read_atoms(pdb_path: Path, chains: set[str] | None = None) -> list[AtomRec]:
    atoms: list[AtomRec] = []
    for line in pdb_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("ATOM"):
            continue
        alt = line[16]
        if alt not in (" ", "A"):
            continue
        resname = line[17:20].strip()
        chain = line[21].strip() or "_"
        if chains and chain not in chains:
            continue
        try:
            resseq = int(line[22:26])
        except ValueError:
            continue
        atom = line[12:16].strip()
        xyz = np.array(
            [float(line[30:38]), float(line[38:46]), float(line[46:54])],
            dtype=float,
        )
        atoms.append((resname, chain, resseq, atom, xyz))
    return atoms


def atom_xyz(
    atoms: list[AtomRec],
    resseq: int,
    resname: str,
    atom_name: str,
) -> np.ndarray | None:
    want = resname.upper()
    for rn, _ch, rs, an, xyz in atoms:
        if rs == resseq and rn.upper() == want and an == atom_name:
            return xyz.copy()
    return None


def residue_atoms(
    atoms: list[AtomRec],
    resseq: int,
    resname: str | None = None,
) -> list[AtomRec]:
    out: list[AtomRec] = []
    for rec in atoms:
        rn, _ch, rs, _an, _xyz = rec
        if rs != resseq:
            continue
        if resname and rn.upper() != resname.upper():
            continue
        out.append(rec)
    return out


def ca_coords_by_resseq(
    atoms: list[AtomRec],
    resseqs: set[int] | tuple[int, ...],
) -> dict[int, np.ndarray]:
    want = set(resseqs)
    out: dict[int, np.ndarray] = {}
    for rn, _ch, rs, an, xyz in atoms:
        if rs in want and an == "CA":
            out[rs] = xyz.copy()
    return out


def dihedral(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
    """Return dihedral angle in degrees."""
    b0 = p1 - p0
    b1 = p2 - p1
    b2 = p3 - p2
    b1n = b1 / (np.linalg.norm(b1) + 1e-12)
    v = b0 - np.dot(b0, b1n) * b1n
    w = b2 - np.dot(b2, b1n) * b1n
    x = np.dot(v, w)
    y = np.linalg.norm(np.cross(b1n, v)) * np.sign(np.dot(np.cross(b1n, v), w))
    return math.degrees(math.atan2(y, x))


def kabsch_align(mobile: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return (R, t) mapping mobile -> target (row vectors)."""
    if mobile.shape != target.shape or mobile.shape[0] < 3:
        raise ValueError("Need >=3 matched points with identical shape")
    mob_c = mobile.mean(axis=0)
    tgt_c = target.mean(axis=0)
    mob0 = mobile - mob_c
    tgt0 = target - tgt_c
    h = mob0.T @ tgt0
    u, _s, vt = np.linalg.svd(h)
    r = vt.T @ u.T
    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T
    t = tgt_c - mob_c @ r
    return r, t


def apply_transform(xyz: np.ndarray, rot: np.ndarray, trans: np.ndarray) -> np.ndarray:
    return xyz @ rot + trans


def write_aligned_pdb(
    source_path: Path,
    out_path: Path,
    rot: np.ndarray,
    trans: np.ndarray,
    chains: set[str] | None = None,
) -> None:
    lines: list[str] = []
    for line in source_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        chain = line[21].strip() or "_"
        if chains and chain not in chains:
            continue
        try:
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
        except ValueError:
            continue
        xyz = apply_transform(np.array([x, y, z]), rot, trans)
        new_line = (
            f"{line[:30]}{xyz[0]:8.3f}{xyz[1]:8.3f}{xyz[2]:8.3f}{line[54:]}"
        )
        lines.append(new_line)
    lines.append("END")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
