#!/usr/bin/env python3
"""Directed Vina docking — HU-308 / HU-433 on CB2 6PT0 and 6KPF (micronetwork test).

Engine: AutoDock Vina exhaustiveness=16, num_modes=9, seed=42.
Ligands: Meeko pH 7.4 Gasteiger (Exam A parity).
Poses: data/docking_poses/micronetwork_test/{pdb_id}/{ligand_id}/
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import inchi

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.screening.docking import dock_ligand, resolve_vina  # noqa: E402

LIGANDS: tuple[dict, ...] = (
    {
        "id": "HU-308",
        "pubchem_cid": 11553430,
        "expected_inchikey": "CFMRIVODIXTERW-BDTNDASRSA-N",
        "smiles": (
            "CCCCCCC(C)(C)C1=CC(=C(C(=C1)OC)[C@H]2C=C([C@H]3C[C@@H]2C3(C)C)CO)OC"
        ),
    },
    {
        "id": "HU-433",
        "pubchem_cid": 59386636,
        "expected_inchikey": "CFMRIVODIXTERW-JTGIGXABSA-N",
        "smiles": (
            "CCCCCCC(C)(C)C1=CC(=C(C(=C1)OC)C2C=C([C@@H]3C[C@H]2C3(C)C)CO)OC"
        ),
    },
)

STATES: tuple[dict, ...] = (
    {
        "pdb_id": "6PT0",
        "receptor_pdbqt": ROOT / "data/targets/cb2_multistate/cb2_6pt0_clean.pdbqt",
        "grid_config": ROOT / "configs/grid_cb2_multistate_6pt0.txt",
    },
    {
        "pdb_id": "6KPF",
        "receptor_pdbqt": ROOT / "data/targets/cb2_multistate/cb2_6kpf_clean.pdbqt",
        "grid_config": ROOT / "configs/grid_cb2_multistate_6kpf.txt",
    },
)

POSE_ROOT = ROOT / "data/docking_poses/micronetwork_test"
OUT_JSON = ROOT / "results/conformational/micronetwork_dock_manifest.json"

EXHAUSTIVENESS = 16
NUM_MODES = 9
SEED = 42
PH = 7.4


def _load_grid(path: Path) -> dict[str, float]:
    box: dict[str, float] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, val = line.split("=", 1)
        box[key.strip()] = float(val.strip())
    return box


def _verify_stereo(lig: dict) -> dict:
    mol = Chem.MolFromSmiles(lig["smiles"])
    if mol is None:
        return {"status": "BLOCKED", "reason": "RDKit cannot parse SMILES"}
    ik = inchi.MolToInchiKey(mol)
    ok = ik == lig["expected_inchikey"]
    return {
        "status": "PASS" if ok else "STEREO_MISMATCH",
        "computed_inchikey": ik,
        "expected_inchikey": lig["expected_inchikey"],
        "pubchem_cid": lig["pubchem_cid"],
    }


def run_dock(force: bool = False) -> dict:
    vina = resolve_vina(None, root=ROOT)
    timestamp = datetime.now(timezone.utc).isoformat()
    manifest: dict = {
        "test": "micronetwork_directed_dock",
        "timestamp_utc": timestamp,
        "engine": {
            "vina": str(vina),
            "exhaustiveness": EXHAUSTIVENESS,
            "num_modes": NUM_MODES,
            "seed": SEED,
            "ph": PH,
        },
        "ligand_identity": {},
        "runs": [],
    }

    for lig in LIGANDS:
        ident = _verify_stereo(lig)
        manifest["ligand_identity"][lig["id"]] = ident
        if ident["status"] != "PASS":
            print(f"BLOQUEO identidad {lig['id']}: {ident}", flush=True)

    for state in STATES:
        pdb_id = state["pdb_id"]
        receptor = state["receptor_pdbqt"]
        grid = _load_grid(state["grid_config"])
        if not receptor.exists():
            raise FileNotFoundError(f"Receptor missing: {receptor}")

        for lig in LIGANDS:
            ident = manifest["ligand_identity"][lig["id"]]
            if ident["status"] != "PASS":
                manifest["runs"].append(
                    {
                        "pdb_id": pdb_id,
                        "ligand_id": lig["id"],
                        "status": "SKIPPED_IDENTITY",
                        "identity": ident,
                    }
                )
                continue

            work = POSE_ROOT / pdb_id / lig["id"]
            out_pdbqt = work / f"{lig['id']}_docked.pdbqt"
            if out_pdbqt.exists() and not force:
                from src.screening.docking import parse_best_affinity

                aff = parse_best_affinity(
                    out_pdbqt.read_text(encoding="utf-8", errors="replace")
                )
                manifest["runs"].append(
                    {
                        "pdb_id": pdb_id,
                        "ligand_id": lig["id"],
                        "status": "CACHED",
                        "vina_affinity_kcal_mol": aff,
                        "docked_pdbqt": str(out_pdbqt),
                        "work_dir": str(work),
                    }
                )
                print(f"[cached] {pdb_id} {lig['id']} aff={aff}", flush=True)
                continue

            print(f"[dock] {pdb_id} {lig['id']} ...", flush=True)
            res = dock_ligand(
                smiles=lig["smiles"],
                name=lig["id"],
                receptor=receptor,
                box=grid,
                work_dir=work,
                vina_path=vina,
                exhaustiveness=EXHAUSTIVENESS,
                num_modes=NUM_MODES,
                seed=SEED,
                ph=PH,
            )
            entry = {
                "pdb_id": pdb_id,
                "ligand_id": lig["id"],
                "status": "OK" if res.get("dock_error") is None else "DOCK_FAILED",
                "vina_affinity_kcal_mol": res.get("vina_affinity"),
                "dock_error": res.get("dock_error"),
                "docked_pdbqt": res.get("docked_pdbqt"),
                "ligand_pdbqt": res.get("ligand_pdbqt"),
                "work_dir": str(work),
            }
            manifest["runs"].append(entry)
            print(
                f"  aff={entry['vina_affinity_kcal_mol']} err={entry['dock_error']}",
                flush=True,
            )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="Re-dock even if poses exist")
    args = ap.parse_args()
    manifest = run_dock(force=args.force)
    n_ok = sum(1 for r in manifest["runs"] if r["status"] in ("OK", "CACHED"))
    print(f"Manifest: {OUT_JSON} ({n_ok}/{len(manifest['runs'])} poses ready)")
    return 0 if n_ok == len(manifest["runs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
