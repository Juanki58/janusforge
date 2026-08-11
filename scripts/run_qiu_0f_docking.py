#!/usr/bin/env python3
"""Execute Qiu 0F CB2 docking for compounds 14/15/20/24 (protocol-locked params)."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "results" / "docking" / "qiu_0f"
VINA = (ROOT / ".." / "molforge" / "tools" / "vina.exe").resolve()
RECEPTOR = ROOT / "data" / "targets" / "cb2" / "6PT0_rec.pdbqt"
LIG_DIR = ROOT / "results" / "docking" / "qiu_0e"

COMPOUNDS = [14, 15, 20, 24]

PARAMS = {
    "center_x": 98.379,
    "center_y": 109.559,
    "center_z": 123.801,
    "size_x": 22.0,
    "size_y": 22.0,
    "size_z": 22.0,
    "exhaustiveness": 8,
    "num_modes": 9,
    "seed": 42,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_cmd(compound: int) -> list[str]:
    lig = LIG_DIR / f"compound_{compound}_lig.pdbqt"
    out = OUT_DIR / f"compound_{compound}_cb2_out.pdbqt"
    return [
        str(VINA),
        "--receptor",
        str(RECEPTOR),
        "--ligand",
        str(lig),
        "--out",
        str(out),
        "--center_x",
        str(PARAMS["center_x"]),
        "--center_y",
        str(PARAMS["center_y"]),
        "--center_z",
        str(PARAMS["center_z"]),
        "--size_x",
        str(PARAMS["size_x"]),
        "--size_y",
        str(PARAMS["size_y"]),
        "--size_z",
        str(PARAMS["size_z"]),
        "--exhaustiveness",
        str(PARAMS["exhaustiveness"]),
        "--num_modes",
        str(PARAMS["num_modes"]),
        "--seed",
        str(PARAMS["seed"]),
    ]


def cmd_display(cmd: list[str]) -> str:
    """Bat-style relative command matching protocol section E."""
    compound = None
    for i, part in enumerate(cmd):
        if part.endswith("_lig.pdbqt"):
            m = re.search(r"compound_(\d+)_lig", part)
            if m:
                compound = m.group(1)
            break
    assert compound is not None
    return (
        f"..\\molforge\\tools\\vina.exe "
        f"--receptor data\\targets\\cb2\\6PT0_rec.pdbqt "
        f"--ligand results\\docking\\qiu_0e\\compound_{compound}_lig.pdbqt "
        f"--out results\\docking\\qiu_0f\\compound_{compound}_cb2_out.pdbqt "
        f"--center_x 98.379 --center_y 109.559 --center_z 123.801 "
        f"--size_x 22.0 --size_y 22.0 --size_z 22.0 "
        f"--exhaustiveness 8 --num_modes 9 --seed 42"
    )


def parse_mode_table(log_text: str) -> list[dict]:
    modes: list[dict] = []
    in_table = False
    for line in log_text.splitlines():
        if "mode |" in line or "-----+" in line:
            in_table = True
            continue
        if not in_table:
            continue
        m = re.match(
            r"^\s*(\d+)\s+(-?\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*$",
            line,
        )
        if m:
            modes.append(
                {
                    "mode": int(m.group(1)),
                    "affinity_kcal_mol": float(m.group(2)),
                    "rmsd_lb": float(m.group(3)),
                    "rmsd_ub": float(m.group(4)),
                }
            )
        elif modes and line.strip() == "":
            break
        elif modes and not line.strip().startswith(("Writing", "WARNING", "NOTE")):
            # stop if non-table content after modes started
            if not re.match(r"^\s*\d+", line):
                break
    return modes


def count_models(pdbqt: Path) -> int:
    if not pdbqt.exists():
        return 0
    text = pdbqt.read_text(encoding="utf-8", errors="replace")
    return text.count("MODEL")


def count_atoms_pdbqt(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    return sum(1 for line in text.splitlines() if line.startswith(("ATOM", "HETATM")))


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()

    ligand_hashes = {}
    for c in COMPOUNDS:
        lig = LIG_DIR / f"compound_{c}_lig.pdbqt"
        ligand_hashes[str(c)] = {
            "path": str(lig.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(lig),
            "atom_lines": count_atoms_pdbqt(lig),
            "mtime_utc": datetime.fromtimestamp(lig.stat().st_mtime, timezone.utc).isoformat(),
        }

    results = []
    for c in COMPOUNDS:
        cmd = build_cmd(c)
        display = cmd_display(cmd)
        log_path = OUT_DIR / f"compound_{c}_cb2.log"
        cmd_path = OUT_DIR / f"compound_{c}_cb2.cmd.txt"
        out_path = OUT_DIR / f"compound_{c}_cb2_out.pdbqt"
        params_path = OUT_DIR / f"compound_{c}_cb2_params.json"

        cmd_path.write_text(display + "\n", encoding="utf-8")
        params_path.write_text(
            json.dumps(
                {
                    "compound": c,
                    "receptor": "data/targets/cb2/6PT0_rec.pdbqt",
                    "ligand": f"results/docking/qiu_0e/compound_{c}_lig.pdbqt",
                    "out": f"results/docking/qiu_0f/compound_{c}_cb2_out.pdbqt",
                    "vina_binary": str(VINA),
                    "engine": "AutoDock Vina",
                    "version_expected": "1.2.7",
                    "parameters": PARAMS,
                    "energy_range": "omit (engine default)",
                    "command": display,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        print(f"[0F] Docking compound {c} ...", flush=True)
        print(f"  CMD: {display}", flush=True)
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        combined = (proc.stdout or "") + (proc.stderr or "")
        log_path.write_text(combined, encoding="utf-8")

        modes = parse_mode_table(combined)
        n_models = count_models(out_path)
        warnings = [
            line.strip()
            for line in combined.splitlines()
            if re.search(r"warn|error|fail|exception", line, re.I)
        ]
        finished_ok = (
            proc.returncode == 0
            and out_path.exists()
            and out_path.stat().st_size > 0
            and n_models > 0
            and "mode |" in combined
        )

        entry = {
            "compound": c,
            "returncode": proc.returncode,
            "finished_ok": finished_ok,
            "out_pdbqt": str(out_path.relative_to(ROOT)).replace("\\", "/"),
            "log": str(log_path.relative_to(ROOT)).replace("\\", "/"),
            "cmd_file": str(cmd_path.relative_to(ROOT)).replace("\\", "/"),
            "params_file": str(params_path.relative_to(ROOT)).replace("\\", "/"),
            "n_poses_log": len(modes),
            "n_models_pdbqt": n_models,
            "modes": modes,
            "warnings_or_errors": warnings,
            "command": display,
            "out_readable": out_path.exists() and out_path.stat().st_size > 0,
            "ligand_sha256": ligand_hashes[str(c)]["sha256"],
            "ligand_atom_lines": ligand_hashes[str(c)]["atom_lines"],
        }
        results.append(entry)
        print(
            f"  rc={proc.returncode} poses_log={len(modes)} models={n_models} ok={finished_ok}",
            flush=True,
        )

    summary = {
        "protocol": "results/reports/qiu_0f_docking_protocol.md",
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "working_directory": str(ROOT),
        "vina_binary": str(VINA),
        "receptor": "data/targets/cb2/6PT0_rec.pdbqt",
        "parameters": PARAMS,
        "energy_range": "omit (engine default)",
        "ligand_integrity": ligand_hashes,
        "results": results,
        "n_finished_ok": sum(1 for r in results if r["finished_ok"]),
        "n_total": len(results),
    }

    (OUT_DIR / "qiu_0f_scores.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )

    csv_path = OUT_DIR / "qiu_0f_scores.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "compound",
                "mode",
                "affinity_kcal_mol",
                "rmsd_lb",
                "rmsd_ub",
                "returncode",
                "finished_ok",
                "n_models_pdbqt",
            ]
        )
        for r in results:
            if r["modes"]:
                for m in r["modes"]:
                    w.writerow(
                        [
                            r["compound"],
                            m["mode"],
                            m["affinity_kcal_mol"],
                            m["rmsd_lb"],
                            m["rmsd_ub"],
                            r["returncode"],
                            r["finished_ok"],
                            r["n_models_pdbqt"],
                        ]
                    )
            else:
                w.writerow(
                    [
                        r["compound"],
                        "",
                        "",
                        "",
                        "",
                        r["returncode"],
                        r["finished_ok"],
                        r["n_models_pdbqt"],
                    ]
                )

    print(
        f"[0F] Done: {summary['n_finished_ok']}/{summary['n_total']} finished_ok",
        flush=True,
    )
    return 0 if summary["n_finished_ok"] == summary["n_total"] else 1


if __name__ == "__main__":
    sys.exit(main())
