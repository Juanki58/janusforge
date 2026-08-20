#!/usr/bin/env python3
"""Phase C — Canonical natural phytocannabinoid retrospective panel (Exam A parity).

Level-0 identity verification, dual Vina docking, THCV contract v1.0 evaluation
(cannabinoid scaffold mapping), decoupled layer verdicts.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from rdkit import Chem

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark_gold_exam_a import (  # noqa: E402
    GOLD_LIGANDS,
    RECEPTORS,
    _load_grid,
)
from src.analysis.contract_evaluation import (  # noqa: E402
    decoupled_verdicts,
    evaluate_compound,
    load_contract,
)
from src.screening.docking import dock_ligand, resolve_vina  # noqa: E402

CHEMOME_CSV = ROOT / "data/libraries/quimioma_semillas.csv"
OUT_DIR = ROOT / "results/docking/screening_natural_cannabinoids_fase_c"
REPORT_MD = ROOT / "results/docking/screening_natural_cannabinoids_fase_c.md"
JSON_PATH = OUT_DIR / "screening_natural_fase_c.json"
GOLD_JSON = ROOT / "results/docking/benchmark_gold_exam_a/benchmark_gold_exam_a.json"

PANEL: tuple[dict, ...] = (
    {
        "id": "CBD",
        "label": "(-)-Cannabidiol",
        "cid": 644019,
        "chemome_key": "CBD",
        "expected_ik": "QGZKDVFQNNGYKY-UHFFFAOYSA-N",
        "stereo_note": "(1'R,2'R); chemome @@H on cyclohexene",
        "scaffold_class": "monocyclic / open chain",
    },
    {
        "id": "CBN",
        "label": "Cannabinol",
        "cid": 2543,
        "chemome_key": "CBN",
        "expected_ik": "VBGLYOIFKLUMDO-UHFFFAOYSA-N",
        "stereo_note": "planar aromatic tricyclic",
        "scaffold_class": "flat aromatic tricyclic",
    },
    {
        "id": "CBG",
        "label": "Cannabigerol",
        "cid": 5315659,
        "chemome_key": "CBG",
        "expected_ik": "QXACEHWTBCFNSA-UHFFFAOYSA-N",
        "stereo_note": "trans/E farnesyl side chain",
        "scaffold_class": "acyclic / farnesyl",
    },
    {
        "id": "CBC",
        "label": "(±)-Cannabichromene",
        "cid": 5281827,
        "chemome_key": "CBC",
        "expected_ik": "UVLZLKCGGIKUBK-UHFFFAOYSA-N",
        "fallback_cid": 30219,
        "stereo_note": "racemic / ± chromene",
        "scaffold_class": "bicyclic chromene",
    },
    {
        "id": "Delta-8-THC",
        "label": "(-)-Δ8-THC",
        "cid": 2977,
        "chemome_key": None,
        "expected_ik": "HAEBWWCHOUPTDF-UHFFFAOYSA-N",
        "stereo_note": "(6aR,10aR) rigid tricyclic",
        "scaffold_class": "rigid tricyclic analog",
        # PubChem CID 2977 connectivity (stereo undefined at PubChem; PI expected
        # HAEBWWCHOUPTDF not found in PubChem InChIKey registry)
        "fallback_smiles": "CCCCCC1=CC(=C2C3CC(=CCC3C(OC2=C1)(C)C)C)O",
    },
)


def _load_chemome() -> dict[str, str]:
    out: dict[str, str] = {}
    with CHEMOME_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["name"]] = row["smiles"]
    return out


def _pubchem_record(cid: int) -> dict:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON"
    req = urllib.request.Request(url, headers={"User-Agent": "janusforge/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def _extract_pubchem_props(record: dict) -> dict:
    out: dict = {}
    for prop in record["PC_Compounds"][0]["props"]:
        urn = prop.get("urn", {})
        label = urn.get("label", "")
        name = urn.get("name", "")
        sval = prop.get("value", {}).get("sval")
        if label == "InChIKey" and name == "Standard":
            out["inchikey"] = sval
        elif label == "IUPAC Name" and name == "Preferred":
            out["iupac"] = sval
        elif label == "Molecular Formula":
            out["formula"] = sval
        elif label in ("SMILES", "Isomeric SMILES", "Canonical SMILES") and sval:
            out.setdefault("smiles", sval)
        elif label == "Connectivity SMILES" and sval:
            out.setdefault("smiles", sval)
    return out


def _inchikey(smiles: str) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    return Chem.MolToInchiKey(mol)


def _connectivity_key(smiles: str) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return ""
    try:
        flat = Chem.RemoveStereochemistry(mol)
        return Chem.MolToInchiKey(flat) if flat is not None else ""
    except Exception:  # noqa: BLE001
        return Chem.MolToInchiKey(mol).split("-")[0]


def _chiral_summary(smiles: str) -> list:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return []
    return Chem.FindMolChiralCenters(mol, includeUnassigned=True)


def verify_identity(entry: dict, chemome: dict[str, str]) -> dict:
    """Level-0 identity gate before PDBQT."""
    cid = entry["cid"]
    rec = _extract_pubchem_props(_pubchem_record(cid))
    chem_smi = chemome.get(entry["chemome_key"]) if entry.get("chemome_key") else None
    pub_smi = rec.get("smiles", "")
    pub_ik = rec.get("inchikey", "")
    expected_ik = entry["expected_ik"]
    identity: dict = {
        "compound_id": entry["id"],
        "label": entry["label"],
        "directive_cid": cid,
        "pubchem_formula": rec.get("formula"),
        "pubchem_iupac": rec.get("iupac"),
        "pubchem_inchikey": pub_ik,
        "expected_inchikey": expected_ik,
        "stereo_note": entry["stereo_note"],
        "scaffold_class": entry["scaffold_class"],
    }

    # CBC directive CID mismatch guard (5281827 ≠ cannabichromene)
    if entry["id"] == "CBC" and rec.get("formula") not in (None, "C21H30O2"):
        fb_cid = entry.get("fallback_cid")
        if fb_cid:
            fb = _extract_pubchem_props(_pubchem_record(fb_cid))
            identity["directive_cid_rejected"] = True
            identity["directive_reject_reason"] = (
                f"CID {cid} formula {rec.get('formula')} != cannabichromene C21H30O2; "
                f"using chemome / CID {fb_cid}."
            )
            rec = fb
            pub_smi = rec.get("smiles", "")
            pub_ik = rec.get("inchikey", "")
            identity["pubchem_formula"] = rec.get("formula")
            identity["pubchem_inchikey"] = pub_ik
            identity["resolved_cid"] = fb_cid

    smiles: str | None = None
    source = ""
    status = "BLOCKED"
    caveat = ""

    if chem_smi:
        chem_ik = _inchikey(chem_smi)
        identity["chemome_smiles"] = chem_smi
        identity["chemome_inchikey"] = chem_ik
        identity["chemome_chiral"] = _chiral_summary(chem_smi)
        if pub_ik and chem_ik == pub_ik:
            smiles = chem_smi
            source = f"chemome + PubChem CID {identity.get('resolved_cid', cid)} (InChIKey match)"
            status = "PASS_IDENTITY"
        elif pub_smi and _connectivity_key(chem_smi) == _connectivity_key(pub_smi):
            smiles = chem_smi
            source = (
                f"chemome certified SMILES (stereo explicit); PubChem connectivity match "
                f"(PubChem IK {pub_ik or '—'} vs chemome {chem_ik})"
            )
            status = "PASS_IDENTITY"
            caveat = "stereo: chemome explicit; PubChem may use undefined-stereo layer"
        elif pub_ik and pub_ik.split("-")[0] == expected_ik.split("-")[0]:
            smiles = chem_smi
            source = f"chemome preferred; connectivity layer matches expected InChIKey prefix"
            status = "PASS_IDENTITY"
            caveat = "InChIKey stereo layer differs; chemome stereo retained"
        elif _connectivity_key(chem_smi) == expected_ik.split("-")[0] or chem_ik.startswith(
            expected_ik.split("-")[0]
        ):
            smiles = chem_smi
            source = "chemome preferred (expected connectivity layer)"
            status = "PASS_IDENTITY"
            caveat = "stereo caveat documented"
        else:
            identity["blocker"] = (
                f"Chemome InChIKey {chem_ik} conflicts with PubChem {pub_ik} "
                f"and expected {expected_ik}"
            )
    elif entry.get("fallback_smiles"):
        fb = entry["fallback_smiles"]
        fb_ik = _inchikey(fb)
        identity["fallback_smiles"] = fb
        identity["fallback_inchikey"] = fb_ik
        if pub_ik and fb_ik == pub_ik:
            smiles = fb
            source = f"PubChem CID {cid} connectivity SMILES (InChIKey match)"
            status = "PASS_IDENTITY"
            if fb_ik.split("-")[0] != expected_ik.split("-")[0]:
                caveat = (
                    f"PI expected IK {expected_ik} not in PubChem; "
                    f"resolved {fb_ik}; stereo undefined (UHFFFAOYSA layer)"
                )
        elif fb_ik.split("-")[0] == expected_ik.split("-")[0]:
            smiles = fb
            source = (
                f"fallback certified SMILES; expected connectivity layer "
                f"{expected_ik.split('-')[0]}"
            )
            status = "PASS_IDENTITY"
            caveat = entry["stereo_note"]
        elif pub_ik and fb_ik.split("-")[0] == pub_ik.split("-")[0]:
            smiles = fb
            source = f"fallback SMILES; connectivity layer match PubChem {pub_ik}"
            status = "PASS_IDENTITY"
            caveat = "stereo resolved from certified fallback, not chemome"
        elif pub_smi and _connectivity_key(fb) and _connectivity_key(fb) == _connectivity_key(pub_smi):
            smiles = fb
            source = "fallback SMILES stereo-resolved; PubChem connectivity match"
            status = "PASS_IDENTITY"
            caveat = entry["stereo_note"]
        else:
            identity["blocker"] = (
                f"No chemome entry; fallback IK {fb_ik} ≠ PubChem {pub_ik} "
                f"(expected {expected_ik})"
            )
    elif pub_smi:
        pub_ik_from_smi = _inchikey(pub_smi)
        if pub_ik_from_smi.split("-")[0] == expected_ik.split("-")[0]:
            smiles = pub_smi
            source = f"PubChem CID {cid} SMILES"
            status = "PASS_IDENTITY"
            caveat = "PubChem SMILES; verify absolute stereo manually"
        else:
            identity["blocker"] = (
                f"PubChem SMILES IK {pub_ik_from_smi} ≠ expected {expected_ik}"
            )
    else:
        identity["blocker"] = "No resolvable SMILES from chemome or PubChem"

    identity["identity_status"] = status
    identity["smiles"] = smiles
    identity["smiles_source"] = source
    identity["stereo_caveat"] = caveat
    if smiles:
        identity["resolved_inchikey"] = _inchikey(smiles)
        identity["resolved_chiral"] = _chiral_summary(smiles)
        if identity["resolved_inchikey"] != expected_ik:
            identity["inchikey_caveat"] = (
                f"PI expected {expected_ik}; resolved {identity['resolved_inchikey']}"
            )
    return identity


def _ensure_hu308_cb2(out_dir: Path, vina: Path, boxes: dict, args) -> Path | None:
    hu_work = out_dir / "reference" / "cb2"
    hu_docked = hu_work / "HU-308_docked.pdbqt"
    if GOLD_JSON.exists():
        payload = json.loads(GOLD_JSON.read_text(encoding="utf-8"))
        hu = next((l for l in payload["ligands"] if l["id"] == "HU-308"), None)
        if hu and hu.get("cb2", {}).get("docked_pdbqt"):
            ref = ROOT / hu["cb2"]["docked_pdbqt"]
            if ref.exists():
                return ref
    if hu_docked.exists() and not args.force:
        return hu_docked
    hu_lig = next(l for l in GOLD_LIGANDS if l["id"] == "HU-308")
    print("[reference] Docking HU-308 CB2 for persistence proxy ...", flush=True)
    res = dock_ligand(
        smiles=hu_lig["smiles"],
        name="HU-308",
        receptor=RECEPTORS["cb2"]["receptor_pdbqt"],
        box=boxes["cb2"],
        work_dir=hu_work,
        vina_path=vina,
        exhaustiveness=args.exhaustiveness,
        num_modes=args.num_modes,
        seed=args.seed,
        ph=args.ph,
    )
    p = Path(res["docked_pdbqt"]) if res.get("docked_pdbqt") else None
    return p if p and p.exists() else None


def _fmt(v: float | None, places: int = 2) -> str:
    return f"{v:.{places}f}" if v is not None else "—"


def _subcheck_lines(cb1f: dict, cb2f: dict, ad: dict) -> str:
    parts: list[str] = []
    if cb1f.get("c3_clearance_pass") is False:
        parts.append(f"CB1 C3 clearance {cb1f.get('c3_clearance_A')} Å (<0.8)")
    if cb1f.get("c9_c11_volume_delta_pass") is False:
        parts.append(f"CB1 C9/C11 Δvol {cb1f.get('c9_c11_volume_delta_A')} Å (>1.0)")
    if cb1f.get("clash_pass") is False:
        parts.append(f"CB1 clash TM {cb1f.get('min_tm_shell_distance_A')} Å (<2.5)")
    if cb2f.get("c3_occupancy_pass") is False:
        parts.append(f"CB2 C3 occupancy {cb2f.get('c3_tunnel_min_distance_A')} Å (>2.5 env)")
    if cb2f.get("ser285_pass") is False:
        parts.append(f"CB2 Ser285 {cb2f.get('ser285_distance_A')} Å (>3.5)")
    if cb2f.get("pose_persistence_pass") is False:
        parts.append(
            f"CB2 persistence {cb2f.get('hu308_centroid_separation_A')} Å (>2.0 vs HU-308)"
        )
    if ad.get("pass") is False:
        parts.append(f"TPSA {ad.get('tpsa_A2')} Å² (<70.0)")
    return "; ".join(parts) if parts else "all sub-checks PASS"


def write_report(payload: dict, out_md: Path) -> None:
    meta = payload["meta"]
    rows = payload["compounds"]
    lines = [
        "# Phase C — Canonical natural phytocannabinoid retrospective panel",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "**Control:** `de_novo_generation=STOP`; `threshold_modification=STOP`; "
        "Contract v1.0 READ-ONLY.",
        "",
        "## Level-0 identidad (pre-PDBQT)",
        "",
        "| Compuesto | CID | Fórmula | InChIKey resuelto | Estado | Fuente / caveat |",
        "|-----------|-----|---------|-------------------|--------|-----------------|",
    ]
    for r in rows:
        ident = r.get("identity", {})
        lines.append(
            f"| {r['compound_id']} | {ident.get('resolved_cid') or ident.get('directive_cid')} | "
            f"{ident.get('pubchem_formula', '—')} | "
            f"`{ident.get('resolved_inchikey', ident.get('pubchem_inchikey', '—'))}` | "
            f"**{ident.get('identity_status', '—')}** | "
            f"{ident.get('smiles_source') or ident.get('blocker', '—')}"
            f"{(' — ' + ident['stereo_caveat']) if ident.get('stereo_caveat') else ''} |"
        )

    lines.extend(
        [
            "",
            "## Protocolo (Exam A parity)",
            "",
            "| Parámetro | Valor |",
            "|-----------|-------|",
            f"| Receptor CB1 | `{meta['receptors']['cb1']}` |",
            f"| Receptor CB2 | `{meta['receptors']['cb2']}` |",
            f"| Grid CB1 | `{meta['grids']['cb1']}` |",
            f"| Grid CB2 | `{meta['grids']['cb2']}` |",
            f"| Vina exhaustiveness | {meta['exhaustiveness']} |",
            f"| num_modes | {meta['num_modes']} |",
            f"| seed | {meta['seed']} |",
            f"| pH (Meeko) | {meta['ph']} |",
            f"| Contrato | `{meta['contract_yaml']}` (READ-ONLY) |",
            "",
            "## Matriz principal",
            "",
            "| Compuesto | Identidad / InChIKey | Score CB1 | Score CB2 | Delta | "
            "STRUCTURAL_BINDING | PERIPHERAL | GLOBAL_V1_0 | Causas / Desglose de Capas |",
            "|-----------|---------------------|-----------|-----------|-------|"
            "---------------------|------------|-------------|----------------------------|",
        ]
    )
    for r in rows:
        ident = r.get("identity", {})
        ik = ident.get("resolved_inchikey") or ident.get("pubchem_inchikey") or "—"
        cid = ident.get("resolved_cid") or ident.get("directive_cid")
        cb1 = r.get("cb1_score")
        cb2 = r.get("cb2_score")
        delta = r.get("delta_cb2_minus_cb1")
        dec = r.get("decoupled", {})
        cb1f = r.get("cb1_filter", {})
        cb2f = r.get("cb2_filter", {})
        ad = r.get("admet", {})
        if ident.get("identity_status") == "BLOCKED":
            layer = ident.get("blocker", "BLOCKED identity")
            lines.append(
                f"| {r['compound_id']} | CID {cid} / `{ik}` | — | — | — | "
                f"**INDET.** | **INDET.** | **BLOCKED** | {layer} |"
            )
            continue
        breakdown = _subcheck_lines(cb1f, cb2f, ad)
        lines.append(
            f"| {r['compound_id']} | CID {cid} / `{ik}` | {_fmt(cb1)} | {_fmt(cb2)} | "
            f"{f'{delta:+.2f}' if delta is not None else '—'} | "
            f"**{dec.get('structural_binding', '—')}** | "
            f"**{dec.get('peripheral', '—')}** | "
            f"**{dec.get('global_v1_0', '—')}** | {dec.get('layer_diagnosis', breakdown)} |"
        )

    # Population decoupling diagnosis
    eval_rows = [
        r for r in rows if r.get("identity", {}).get("identity_status") == "PASS_IDENTITY"
    ]
    structural_pass = [r for r in eval_rows if r.get("decoupled", {}).get("structural_binding") == "PASS"]
    peripheral_pass = [r for r in eval_rows if r.get("decoupled", {}).get("peripheral") == "PASS"]
    sp_pf = [
        r["compound_id"]
        for r in eval_rows
        if r.get("decoupled", {}).get("layer_diagnosis", "").startswith("desacoplamiento REAL: STRUCTURAL PASS")
    ]
    sf_pp = [
        r["compound_id"]
        for r in eval_rows
        if "STRUCTURAL FAIL / PERIPHERAL PASS" in r.get("decoupled", {}).get("layer_diagnosis", "")
    ]
    concomitant = [
        r["compound_id"]
        for r in eval_rows
        if "concomitante" in r.get("decoupled", {}).get("layer_diagnosis", "")
    ]
    global_pass = [r["compound_id"] for r in eval_rows if r.get("decoupled", {}).get("global_v1_0") == "PASS"]

    lines.extend(
        [
            "",
            "## Diagnóstico poblacional — desacoplamiento de capas",
            "",
            f"- **Compuestos evaluables:** {len(eval_rows)}/{len(rows)}",
            f"- **STRUCTURAL PASS:** {len(structural_pass)} ({', '.join(r['compound_id'] for r in structural_pass) or '—'})",
            f"- **PERIPHERAL PASS:** {len(peripheral_pass)} ({', '.join(r['compound_id'] for r in peripheral_pass) or '—'})",
            f"- **GLOBAL_V1_0 PASS:** {len(global_pass)} ({', '.join(global_pass) or '—'})",
            "",
            "### Modos de rechazo / desacoplamiento",
            "",
            f"- **Desacoplamiento REAL (STRUCTURAL PASS / PERIPHERAL FAIL):** "
            f"{', '.join(sp_pf) if sp_pf else '**ninguno**'}",
            f"- **Desacoplamiento REAL (STRUCTURAL FAIL / PERIPHERAL PASS):** "
            f"{', '.join(sf_pp) if sf_pp else '**ninguno**'}",
            f"- **Rechazo concomitante (ambas capas FAIL):** "
            f"{', '.join(concomitant) if concomitant else '—'}",
            "",
            "### Sub-checks geométricos (referencia v1.0 congelado)",
            "",
            "**CB1:** C3 clearance ≥0.8 Å; C9/C11 Δvol ≤1.0 Å; clash TM shell ≥2.5 Å  ",
            "**CB2:** C3 occupancy envelope 2.5 Å; Ser285 ≤3.5 Å; persistence vs HU-308 ≤2.0 Å  ",
            "**Peripheral:** TPSA ≥70.0 Å²",
            "",
            "## Detalle por compuesto",
            "",
        ]
    )
    for r in rows:
        lines.append(f"### {r['compound_id']}")
        ident = r.get("identity", {})
        if ident.get("identity_status") == "BLOCKED":
            lines.append(f"- **Blocker:** {ident.get('blocker')}")
            lines.append("")
            continue
        cb1f = r.get("cb1_filter", {})
        cb2f = r.get("cb2_filter", {})
        ad = r.get("admet", {})
        lines.extend(
            [
                f"- SMILES: `{ident.get('smiles')}`",
                f"- CB1 score: {_fmt(r.get('cb1_score'))} kcal/mol",
                f"- CB2 score: {_fmt(r.get('cb2_score'))} kcal/mol",
                f"- C3 clearance: {cb1f.get('c3_clearance_A', '—')} Å (pass={cb1f.get('c3_clearance_pass')})",
                f"- C9/C11 Δvol: {cb1f.get('c9_c11_volume_delta_A', '—')} Å (pass={cb1f.get('c9_c11_volume_delta_pass')})",
                f"- CB1 clash TM: {cb1f.get('min_tm_shell_distance_A', '—')} Å",
                f"- CB2 C3 occupancy: {cb2f.get('c3_tunnel_min_distance_A', '—')} Å",
                f"- CB2 Ser285: {cb2f.get('ser285_distance_A', '—')} Å",
                f"- HU-308 centroid Δ: {cb2f.get('hu308_centroid_separation_A', '—')} Å",
                f"- TPSA: {ad.get('tpsa_A2', '—')} Å²",
                f"- **Diagnóstico capas:** {r.get('decoupled', {}).get('layer_diagnosis', '—')}",
                "",
            ]
        )

    lines.extend(
        [
            f"JSON: `{JSON_PATH.relative_to(ROOT)}`",
            f"Poses CB1: `{OUT_DIR.relative_to(ROOT)}/cb1/`",
            f"Poses CB2: `{OUT_DIR.relative_to(ROOT)}/cb2/`",
            "",
        ]
    )
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    ap.add_argument("--exhaustiveness", type=int, default=16)
    ap.add_argument("--num-modes", type=int, default=9)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ph", type=float, default=7.4)
    ap.add_argument("--force", action="store_true")
    ap.add_argument(
        "--report-only",
        action="store_true",
        help="Rebuild report/JSON from existing poses",
    )
    args = ap.parse_args()

    chemome = _load_chemome()
    contract = load_contract()
    identities = [verify_identity(e, chemome) for e in PANEL]

    print("=== Level-0 identity ===")
    for ident in identities:
        print(
            f"  {ident['compound_id']}: {ident['identity_status']} "
            f"IK={ident.get('resolved_inchikey', ident.get('pubchem_inchikey', '—'))}"
        )
        if ident.get("directive_cid_rejected"):
            print(f"    REJECT: {ident.get('directive_reject_reason')}")
        if ident.get("blocker"):
            print(f"    blocker: {ident['blocker']}")

    json_path = args.out_dir / "screening_natural_fase_c.json"
    if args.report_only:
        if not json_path.exists():
            print(f"BLOQUEO: --report-only pero falta {json_path}")
            return 2
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        write_report(payload, REPORT_MD)
        print(f"Report: {REPORT_MD}")
        return 0

    for tk, v in RECEPTORS.items():
        if not v["receptor_pdbqt"].exists():
            print(f"BLOQUEO: receptor ausente {v['receptor_pdbqt']}")
            return 2

    try:
        vina = resolve_vina(root=ROOT)
    except FileNotFoundError as exc:
        print(f"BLOQUEO: {exc}")
        return 2

    boxes = {k: _load_grid(v["grid_config"]) for k, v in RECEPTORS.items()}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    hu308_cb2 = _ensure_hu308_cb2(args.out_dir, vina, boxes, args)
    print(f"Vina: {vina}")
    print(f"HU-308 CB2 reference: {hu308_cb2}")

    compounds: list[dict] = []
    for entry, ident in zip(PANEL, identities):
        row: dict = {
            "compound_id": entry["id"],
            "label": entry["label"],
            "identity": ident,
        }
        if ident["identity_status"] == "BLOCKED" or not ident.get("smiles"):
            evaluated = evaluate_compound(
                entry["id"],
                None,
                None,
                None,
                RECEPTORS["cb1"]["receptor_pdb"],
                RECEPTORS["cb2"]["receptor_pdb"],
                hu308_cb2,
                contract,
                scaffold="cannabinoid",
            )
            row.update(evaluated)
            row["decoupled"] = decoupled_verdicts(row)
            row["blocker"] = ident.get("blocker")
            compounds.append(row)
            continue

        smiles = ident["smiles"]
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in entry["id"])[:80]
        scores: dict = {}
        for tk, tmeta in RECEPTORS.items():
            work = args.out_dir / tk
            docked = work / f"{safe}_docked.pdbqt"
            if args.force and docked.exists():
                docked.unlink()
            print(f"[{entry['id']}] docking {tk} ...", flush=True)
            res = dock_ligand(
                smiles=smiles,
                name=entry["id"],
                receptor=tmeta["receptor_pdbqt"],
                box=boxes[tk],
                work_dir=work,
                vina_path=vina,
                exhaustiveness=args.exhaustiveness,
                num_modes=args.num_modes,
                seed=args.seed,
                ph=args.ph,
            )
            scores[tk] = res
            print(f"  {tk} affinity={res.get('vina_affinity')} err={res.get('dock_error')}")

        cb1_a = scores["cb1"].get("vina_affinity")
        cb2_a = scores["cb2"].get("vina_affinity")
        row["cb1_score"] = cb1_a
        row["cb2_score"] = cb2_a
        row["delta_cb2_minus_cb1"] = (
            cb2_a - cb1_a if cb1_a is not None and cb2_a is not None else None
        )
        cb1_pose = Path(scores["cb1"]["docked_pdbqt"]) if scores["cb1"].get("docked_pdbqt") else None
        cb2_pose = Path(scores["cb2"]["docked_pdbqt"]) if scores["cb2"].get("docked_pdbqt") else None
        evaluated = evaluate_compound(
            entry["id"],
            smiles,
            cb1_pose,
            cb2_pose,
            RECEPTORS["cb1"]["receptor_pdb"],
            RECEPTORS["cb2"]["receptor_pdb"],
            hu308_cb2,
            contract,
            scaffold="cannabinoid",
        )
        row.update(evaluated)
        row["decoupled"] = {
            "structural_binding": row.get("structural_binding"),
            "peripheral": row.get("peripheral"),
            "global_v1_0": row.get("global_v1_0"),
            "layer_diagnosis": row.get("layer_diagnosis"),
        }
        row["docking"] = scores
        compounds.append(row)

    meta = {
        "phase": "C",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "exhaustiveness": args.exhaustiveness,
        "num_modes": args.num_modes,
        "seed": args.seed,
        "ph": args.ph,
        "vina": str(vina),
        "receptors": {k: str(v["receptor_pdbqt"]) for k, v in RECEPTORS.items()},
        "grids": {k: str(v["grid_config"]) for k, v in RECEPTORS.items()},
        "contract_yaml": str((ROOT / "configs/thcv_design_constraints.yaml").relative_to(ROOT)),
        "contract_frozen": True,
        "de_novo_generation": "STOP",
        "threshold_modification": "STOP",
        "hu308_cb2_reference": str(hu308_cb2.relative_to(ROOT)) if hu308_cb2 else None,
    }
    payload = {"meta": meta, "compounds": compounds}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(payload, REPORT_MD)
    print(f"Report: {REPORT_MD}")
    print(f"JSON: {json_path}")
    for c in compounds:
        dec = c.get("decoupled", {})
        print(
            f"  {c['compound_id']}: GLOBAL={dec.get('global_v1_0')} "
            f"STRUCT={dec.get('structural_binding')} PERIPH={dec.get('peripheral')}"
        )
    docked_ok = sum(
        1
        for c in compounds
        if c.get("cb1_score") is not None and c.get("cb2_score") is not None
    )
    return 0 if docked_ok >= 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
