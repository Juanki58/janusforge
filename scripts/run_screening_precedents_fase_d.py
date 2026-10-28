#!/usr/bin/env python3
"""Phase D — Polar precedents & literature counterexamples (2×2 matrix test).

Level-0 identity verification, dual Vina docking (Exam A parity), THCV contract
v1.0 evaluation (cannabinoid scaffold where applicable), mandatory Q1–Q4 quadrant
classification. CONTRACT v1.0 READ-ONLY.
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
    evaluate_admet,
    evaluate_cb1,
    evaluate_cb2,
    load_contract,
)

from src.screening.docking import dock_ligand, resolve_vina  # noqa: E402

CHEMOME_CSV = ROOT / "data/libraries/quimioma_semillas.csv"
OUT_DIR = ROOT / "results/docking/precedents_fase_d"
REPORT_MD = ROOT / "results/docking/screening_precedents_fase_d.md"
JSON_PATH = OUT_DIR / "screening_precedents_fase_d.json"
GOLD_JSON = ROOT / "results/docking/benchmark_gold_exam_a/benchmark_gold_exam_a.json"

# Documented THCV C11-hydroxymethyl equivalent (11-OH-THCV pattern on varin scaffold).
# Source: scripts/run_thcv_analogs_series_v1.py THCV_CORE_11OH / THCV-09 (V3-C11).
THCV_C11_OH_SMILES = (
    "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)CO)C)O"
)
THCV_PARENT_CID = 93147
THCV_PARENT_IK = "ZROLHBHDLIHEMS-HUUCEWRRSA-N"

PANEL: tuple[dict, ...] = (
    {
        "id": "THCVA",
        "label": "Δ9-Tetrahydrocannabivarinic acid",
        "directive_cid": 5281856,
        "resolved_cid": 59444416,
        "chemome_key": "THCVA",
        "expected_formula": "C20H26O4",
        "source": (
            "PubChem CID 59444416 (chemome-verified); directive CID 5281856 REJECTED "
            "(C15H20N2O — not cannabinoid). quimioma_semillas.csv; "
            "https://pubchem.ncbi.nlm.nih.gov/compound/59444416"
        ),
        "scaffold": "cannabinoid",
        "class": "acidic_phytocannabinoid",
    },
    {
        "id": "CBDA",
        "label": "Cannabidiolic acid",
        "directive_cid": 160570,
        "resolved_cid": 160570,
        "chemome_key": None,
        "expected_formula": "C22H30O4",
        "source": (
            "PubChem CID 160570; phytocannabinoid precursor CBD. "
            "https://pubchem.ncbi.nlm.nih.gov/compound/160570"
        ),
        "scaffold": "cannabinoid",
        "class": "acidic_phytocannabinoid",
    },
    {
        "id": "THCV-C11-OH",
        "label": "THCV C11-hydroxymethyl (11-OH-THCV equivalent)",
        "directive_cid": None,
        "resolved_cid": THCV_PARENT_CID,
        "chemome_key": None,
        "certified_smiles": THCV_C11_OH_SMILES,
        "expected_formula": "C19H26O3",
        "parent_inchikey": THCV_PARENT_IK,
        "source": (
            "Documented C9/C11 polar metabolite mapping on Δ9-THCV parent (CID 93147); "
            "no standalone PubChem 11-OH-THCV entry (404). "
            "scripts/run_thcv_analogs_series_v1.py THCV-09 / THCV_CORE_11OH"
        ),
        "scaffold": "cannabinoid",
        "class": "hydroxylated_metabolite",
    },
    {
        "id": "JD5037",
        "label": "JD5037 (peripheral CB1 inverse agonist)",
        "directive_cid": 66553204,
        "resolved_cid": 66553204,
        "chemome_key": None,
        "expected_inchikey": "GTCSIQFTNPTSLO-RPWUZVMVSA-N",
        "expected_formula": "C27H27Cl2N5O3S",
        "source": (
            "PubChem CID 66553204; Tam 2012 DOI 10.1016/j.cmet.2012.07.002 "
            "(PMID 22841573); peripheral CB1 / CB2-negative control"
        ),
        "scaffold": None,
        "class": "synthetic_peripheral_cb1",
    },
    {
        "id": "URB447",
        "label": "URB447 (peripheral CB1-ant / CB2-ago comparator)",
        "directive_cid": 25195055,
        "resolved_cid": 25195055,
        "chemome_key": "URB447",
        "expected_inchikey": "KGXYGMKEFDUWNB-UHFFFAOYSA-N",
        "expected_formula": "C25H21ClN2O",
        "source": (
            "PubChem CID 25195055; LoVerme 2009 DOI 10.1016/j.bmcl.2008.12.059 "
            "(PMID 19128970); documented polar synthetic Janus comparator"
        ),
        "scaffold": "cannabinoid",
        "class": "synthetic_polar_cb2",
    },
    {
        "id": "LEI-101",
        "label": "LEI-101·HCl (peripheral CB2 tool)",
        "directive_cid": 127021038,
        "resolved_cid": 127021038,
        "chemome_key": None,
        "expected_inchikey": "APLLNJWPLUIBCG-UHFFFAOYSA-N",
        "expected_formula": "C23H26ClFN4O4S",
        "source": (
            "PubChem CID 127021038 (HCl salt); Mukhopadhyay 2016 DOI 10.1111/bph.13338 "
            "(PMID 26398481); imidazolidinedione peripheral CB2 agonist"
        ),
        "scaffold": None,
        "class": "synthetic_polar_cb2",
        "stereo_caveat": "HCl salt as PubChem entity; free-base identity REVIEW in Round1",
    },
)

# Identity audit rows (not docked) — documented BLOCK decisions.
BLOCKED_AUDIT: tuple[dict, ...] = (
    {
        "id": "11-OH-THCV",
        "label": "11-OH-THCV (PubChem name search)",
        "blocker": (
            "No PubChem Level-0 entity for 11-hydroxy-tetrahydrocannabivarin (404). "
            "Replaced by documented THCV-C11-OH equivalent."
        ),
        "source": "PubChem PUGREST.NotFound",
    },
    {
        "id": "THCVA-wrong-CID",
        "label": "THCVA @ directive CID 5281856",
        "blocker": (
            "CID 5281856 = C15H20N2O (InChIKey DEDKBUWNGGQJMQ-RGCMKSIDSA-N), "
            "not tetrahydrocannabivarinic acid — identity BLOCKED per PI guard."
        ),
        "source": "PubChem CID 5281856",
    },
)


def _load_chemome() -> dict[str, str]:
    out: dict[str, str] = {}
    with CHEMOME_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["name"]] = row["smiles"]
    return out


def _pubchem_props(cid: int) -> dict:
    url = (
        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/"
        "property/IsomericSMILES,InChIKey,MolecularFormula,IUPACName/JSON"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "janusforge/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        row = json.load(resp)["PropertyTable"]["Properties"][0]
    row["smiles"] = row.get("IsomericSMILES") or row.get("SMILES", "")
    return row


def _inchikey(smiles: str) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    return Chem.MolToInchiKey(mol)


def _connectivity_prefix(ik: str) -> str:
    return ik.split("-")[0] if ik else ""


def verify_identity(entry: dict, chemome: dict[str, str]) -> dict:
    ident: dict = {
        "compound_id": entry["id"],
        "label": entry["label"],
        "class": entry.get("class"),
        "directive_cid": entry.get("directive_cid"),
        "resolved_cid": entry.get("resolved_cid"),
        "source": entry.get("source"),
        "stereo_caveat": entry.get("stereo_caveat", ""),
    }

    # Reject wrong THCVA directive CID if queried
    if entry["id"] == "THCVA" and entry.get("directive_cid") == 5281856:
        try:
            bad = _pubchem_props(5281856)
            if bad.get("MolecularFormula") != "C20H26O4":
                ident["directive_cid_rejected"] = True
                ident["directive_reject_reason"] = (
                    f"CID 5281856 formula {bad.get('MolecularFormula')} != THCVA C20H26O4"
                )
        except urllib.error.HTTPError:
            ident["directive_cid_rejected"] = True
            ident["directive_reject_reason"] = "CID 5281856 fetch failed"

    cid = entry.get("resolved_cid")
    chem_smi = chemome.get(entry["chemome_key"]) if entry.get("chemome_key") else None
    cert_smi = entry.get("certified_smiles")

    smiles: str | None = None
    status = "BLOCKED"
    blocker = ""

    if cert_smi:
        mol = Chem.MolFromSmiles(cert_smi)
        if mol is None:
            blocker = "Certified SMILES invalid"
        else:
            smiles = cert_smi
            ident["resolved_inchikey"] = _inchikey(cert_smi)
            ident["pubchem_formula"] = entry.get("expected_formula")
            ident["parent_inchikey"] = entry.get("parent_inchikey")
            status = "PASS_IDENTITY"
            ident["smiles_source"] = entry.get("source", "certified SMILES")
    elif cid:
        try:
            rec = _pubchem_props(cid)
        except urllib.error.HTTPError as exc:
            ident["blocker"] = f"PubChem CID {cid} fetch failed: {exc}"
            ident["identity_status"] = "BLOCKED"
            return ident

        pub_smi = rec.get("smiles", "")
        pub_ik = rec.get("InChIKey", "")
        ident["pubchem_formula"] = rec.get("MolecularFormula")
        ident["pubchem_inchikey"] = pub_ik
        ident["pubchem_iupac"] = rec.get("IUPACName")

        exp_formula = entry.get("expected_formula")
        if exp_formula and rec.get("MolecularFormula") != exp_formula:
            blocker = (
                f"Formula mismatch: PubChem {rec.get('MolecularFormula')} "
                f"!= expected {exp_formula}"
            )
        exp_ik = entry.get("expected_inchikey")
        if not blocker and exp_ik and pub_ik and pub_ik != exp_ik:
            if _connectivity_prefix(pub_ik) != _connectivity_prefix(exp_ik):
                blocker = f"InChIKey mismatch: PubChem {pub_ik} != expected {exp_ik}"

        if not blocker and chem_smi:
            chem_ik = _inchikey(chem_smi)
            ident["chemome_smiles"] = chem_smi
            ident["chemome_inchikey"] = chem_ik
            if pub_ik and chem_ik == pub_ik:
                smiles = chem_smi
                ident["smiles_source"] = f"chemome + PubChem CID {cid} (InChIKey match)"
                status = "PASS_IDENTITY"
            elif _connectivity_prefix(chem_ik) == _connectivity_prefix(pub_ik or chem_ik):
                smiles = chem_smi
                ident["smiles_source"] = "chemome preferred; connectivity layer match"
                status = "PASS_IDENTITY"
                if pub_ik and chem_ik != pub_ik:
                    ident["stereo_caveat"] = (
                        ident.get("stereo_caveat", "")
                        + " chemome stereo vs PubChem layer"
                    ).strip()
            else:
                blocker = f"Chemome IK {chem_ik} conflicts with PubChem {pub_ik}"
        elif not blocker and pub_smi:
            smiles = pub_smi
            ident["smiles_source"] = f"PubChem CID {cid} IsomericSMILES"
            status = "PASS_IDENTITY"
            ident["resolved_inchikey"] = _inchikey(pub_smi)
        elif not blocker:
            blocker = "No SMILES from PubChem or chemome"
    else:
        blocker = "No CID or certified SMILES"

    ident["identity_status"] = status if smiles else "BLOCKED"
    ident["smiles"] = smiles
    if blocker:
        ident["blocker"] = blocker
    if smiles and "resolved_inchikey" not in ident:
        ident["resolved_inchikey"] = _inchikey(smiles)
    return ident


def _ensure_hu308_cb2(out_dir: Path, vina: Path, boxes: dict, args) -> Path | None:
    hu_work = out_dir / "reference" / "cb2"
    hu_docked = hu_work / "HU-308_docked.pdbqt"
    if GOLD_JSON.exists():
        payload = json.loads(GOLD_JSON.read_text(encoding="utf-8"))
        hu = next((l for l in payload["ligands"] if l["id"] == "HU-308"), None)
        if hu and hu.get("cb2", {}).get("docked_pdbqt"):
            ref = ROOT / Path(hu["cb2"]["docked_pdbqt"]).name
            full = Path(hu["cb2"]["docked_pdbqt"])
            if full.exists():
                return full
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


def evaluate_with_scaffold(
    compound_id: str,
    smiles: str,
    cb1_pose: Path | None,
    cb2_pose: Path | None,
    hu308_cb2: Path | None,
    contract: dict,
    scaffold: str | None,
) -> dict:
    out: dict = {"compound_id": compound_id, "smiles": smiles}
    out["admet"] = evaluate_admet(smiles, contract)

    struct_blocker: str | None = None
    if scaffold is None:
        struct_blocker = (
            "Non-cannabinoid scaffold — contract geometric proxies not mapped "
            "(JD5037 / LEI-101); STRUCTURAL INDETERMINATE"
        )
        out["cb1_filter"] = {"aggregate_pass": False, "blocker": True, "error": struct_blocker}
        out["cb2_filter"] = {"aggregate_pass": False, "blocker": True, "error": struct_blocker}
    else:
        try:
            if cb1_pose and cb1_pose.exists():
                out["cb1_filter"] = evaluate_cb1(
                    smiles,
                    cb1_pose,
                    RECEPTORS["cb1"]["receptor_pdb"],
                    contract,
                    scaffold=scaffold,
                )
            else:
                out["cb1_filter"] = {"aggregate_pass": False, "error": "missing CB1 pose"}
            if cb2_pose and cb2_pose.exists():
                out["cb2_filter"] = evaluate_cb2(
                    smiles,
                    cb2_pose,
                    RECEPTORS["cb2"]["receptor_pdb"],
                    hu308_cb2,
                    contract,
                    scaffold=scaffold,
                )
            else:
                out["cb2_filter"] = {"aggregate_pass": False, "error": "missing CB2 pose"}
        except ValueError as exc:
            struct_blocker = f"Scaffold mapping failed ({scaffold}): {exc}"
            out["cb1_filter"] = {"aggregate_pass": False, "error": struct_blocker}
            out["cb2_filter"] = {"aggregate_pass": False, "error": struct_blocker}

    if struct_blocker:
        out["structural_blocker"] = struct_blocker
        dec = {
            "structural_binding": "INDETERMINATE",
            "peripheral": "PASS" if out["admet"].get("pass") else "FAIL",
            "global_v1_0": "FAIL",
            "layer_diagnosis": f"estructural INDETERMINATE ({struct_blocker}); periférico evaluable",
        }
        out.update(dec)
        out["contract_verdict"] = "FAIL"
        return out

    out.update(decoupled_verdicts(out))
    out["contract_verdict"] = "PASS" if out.get("global_v1_0") == "PASS" else "FAIL"
    return out


def classify_quadrant(dec: dict, identity: dict) -> str:
    if identity.get("identity_status") == "BLOCKED":
        return "BLOCKED"
    struct = dec.get("structural_binding", "FAIL")
    periph = dec.get("peripheral", "FAIL")
    if struct == "INDETERMINATE":
        return "INDET."
    if struct == "PASS" and periph == "PASS":
        return "Q1"
    if struct == "PASS" and periph == "FAIL":
        return "Q2"
    if struct == "FAIL" and periph == "PASS":
        return "Q3"
    return "Q4"


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
        parts.append(f"CB2 C3 occupancy {cb2f.get('c3_tunnel_min_distance_A')} Å (>2.5)")
    if cb2f.get("ser285_pass") is False:
        parts.append(f"CB2 Ser285 {cb2f.get('ser285_distance_A')} Å (>3.5)")
    if cb2f.get("pose_persistence_pass") is False:
        parts.append(
            f"CB2 persistence {cb2f.get('hu308_centroid_separation_A')} Å (>2.0 vs HU-308)"
        )
    if ad.get("pass") is False:
        parts.append(f"TPSA {ad.get('tpsa_A2')} Å² (<70.0)")
    if cb1f.get("error"):
        parts.append(str(cb1f["error"])[:80])
    return "; ".join(parts) if parts else "all sub-checks PASS"


def write_report(payload: dict, out_md: Path) -> None:
    meta = payload["meta"]
    rows = payload["compounds"]
    blocked = payload.get("blocked_audit", [])

    lines = [
        "# Phase D — Precedents & literature counterexamples (2×2 matrix test)",
        "",
        f"Generado: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "**Control:** `CONTRACT_v1.0` FROZEN; `threshold_modification=STOP`; "
        "`de_novo_generation=STOP`.",
        "",
        "## Cuadrantes obligatorios (Contract v1.0)",
        "",
        "| Cuadrante | STRUCTURAL_BINDING | PERIPHERAL (TPSA≥70) | GLOBAL v1.0 | Interpretación |",
        "|-----------|-------------------|----------------------|-------------|----------------|",
        "| **Q1** | PASS | PASS | PASS | Contract **falsificado** — precedente polar pasa embudo |",
        "| **Q2** | PASS | FAIL | FAIL | Desacoplamiento real: geometría OK, polaridad insuficiente |",
        "| **Q3** | FAIL | PASS | FAIL | Desacoplamiento real: TPSA OK, geometría CB1/CB2 fail |",
        "| **Q4** | FAIL | FAIL | FAIL | Rechazo concomitante |",
        "",
        "## Level-0 identidad (pre-PDBQT)",
        "",
        "| Compuesto | CID / Registro | Fórmula | InChIKey resuelto | Estado | Fuente |",
        "|-----------|----------------|---------|-------------------|--------|--------|",
    ]

    for r in rows:
        ident = r.get("identity", {})
        cid = ident.get("resolved_cid") or ident.get("directive_cid") or "—"
        ik = ident.get("resolved_inchikey") or ident.get("pubchem_inchikey") or "—"
        lines.append(
            f"| {r['compound_id']} | {cid} | {ident.get('pubchem_formula', '—')} | "
            f"`{ik}` | **{ident.get('identity_status', '—')}** | "
            f"{ident.get('smiles_source') or ident.get('source', '—')[:80]} |"
        )

    if blocked:
        lines.extend(["", "### Auditoría BLOCK (no dockados)", ""])
        for b in blocked:
            lines.append(f"- **{b['id']}:** {b['blocker']}")

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
            "## Matriz principal (2×2)",
            "",
            "| Compuesto | CID / Registro | Score CB1 | Score CB2 | Delta | "
            "STRUCTURAL_BINDING | PERIPHERAL (TPSA) | Cuadrante | Desglose Sub-checks |",
            "|-----------|----------------|-----------|-----------|-------|"
            "---------------------|-------------------|-----------|---------------------|",
        ]
    )

    q_counts = {"Q1": [], "Q2": [], "Q3": [], "Q4": [], "INDET.": [], "BLOCKED": []}

    for r in rows:
        ident = r.get("identity", {})
        cid = ident.get("resolved_cid") or ident.get("directive_cid") or "—"
        dec = r.get("decoupled", {})
        quad = r.get("quadrant", "—")
        q_counts.get(quad, []).append(r["compound_id"]) if quad in q_counts else None

        if ident.get("identity_status") == "BLOCKED":
            lines.append(
                f"| {r['compound_id']} | {cid} | — | — | — | **INDET.** | **INDET.** | "
                f"**BLOCKED** | {ident.get('blocker', '—')} |"
            )
            continue

        cb1f = r.get("cb1_filter", {})
        cb2f = r.get("cb2_filter", {})
        ad = r.get("admet", {})
        delta = r.get("delta_cb2_minus_cb1")
        tpsa = ad.get("tpsa_A2")
        periph_label = f"{'PASS' if ad.get('pass') else 'FAIL'} ({tpsa} Å²)" if tpsa else "—"
        breakdown = _subcheck_lines(cb1f, cb2f, ad)

        lines.append(
            f"| {r['compound_id']} | {cid} | {_fmt(r.get('cb1_score'))} | "
            f"{_fmt(r.get('cb2_score'))} | {f'{delta:+.2f}' if delta is not None else '—'} | "
            f"**{dec.get('structural_binding', '—')}** | **{periph_label}** | "
            f"**{quad}** | {breakdown} |"
        )

    eval_rows = [
        r for r in rows if r.get("identity", {}).get("identity_status") == "PASS_IDENTITY"
    ]
    global_pass = [r["compound_id"] for r in eval_rows if r.get("quadrant") == "Q1"]

    lines.extend(
        [
            "",
            "## Diagnóstico falsificación / desacoplamiento",
            "",
            f"- **Compuestos evaluables:** {len(eval_rows)}/{len(rows)}",
            f"- **Q1 (GLOBAL PASS — falsificación):** "
            f"{', '.join(q_counts['Q1']) if q_counts['Q1'] else '**ninguno**'}",
            f"- **Q2 (STRUCTURAL PASS / PERIPHERAL FAIL):** "
            f"{', '.join(q_counts['Q2']) if q_counts['Q2'] else '**ninguno**'}",
            f"- **Q3 (STRUCTURAL FAIL / PERIPHERAL PASS):** "
            f"{', '.join(q_counts['Q3']) if q_counts['Q3'] else '**ninguno**'}",
            f"- **Q4 (concomitante):** "
            f"{', '.join(q_counts['Q4']) if q_counts['Q4'] else '—'}",
            f"- **INDETERMINATE (scaffold no mapeado):** "
            f"{', '.join(q_counts['INDET.']) if q_counts['INDET.'] else '—'}",
            "",
            "### Conclusión Phase D",
            "",
        ]
    )

    if global_pass:
        lines.append(
            f"- **Contract v1.0 falsificado:** {', '.join(global_pass)} alcanza Q1 (GLOBAL PASS)."
        )
    else:
        lines.append(
            "- **Contract v1.0 NO falsificado** en este panel polar/documentado: "
            "ningún precedente alcanza Q1 (STRUCTURAL + PERIPHERAL PASS)."
        )

    if q_counts["Q2"] or q_counts["Q3"]:
        lines.append(
            f"- **Desacoplamiento real detectado:** Q2={', '.join(q_counts['Q2']) or '—'}; "
            f"Q3={', '.join(q_counts['Q3']) or '—'}."
        )
    else:
        lines.append(
            "- **Sin desacoplamiento separable** entre capas en compuestos con scaffold "
            "mapeado (solo Q4 o INDET.)."
        )

    lines.extend(["", "## Detalle por compuesto", ""])
    for r in rows:
        lines.append(f"### {r['compound_id']}")
        ident = r.get("identity", {})
        if ident.get("identity_status") == "BLOCKED":
            lines.append(f"- **Blocker:** {ident.get('blocker')}")
            lines.append("")
            continue
        lines.extend(
            [
                f"- Clase: {ident.get('class', '—')}",
                f"- SMILES: `{ident.get('smiles')}`",
                f"- Fuente: {ident.get('source', '—')}",
                f"- CB1 score: {_fmt(r.get('cb1_score'))} kcal/mol",
                f"- CB2 score: {_fmt(r.get('cb2_score'))} kcal/mol",
                f"- Cuadrante: **{r.get('quadrant', '—')}**",
                f"- Diagnóstico: {r.get('decoupled', {}).get('layer_diagnosis', '—')}",
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
    ap.add_argument("--report-only", action="store_true")
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

    json_path = args.out_dir / "screening_precedents_fase_d.json"
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
            row["blocker"] = ident.get("blocker")
            row["decoupled"] = decoupled_verdicts({"blocker": ident.get("blocker")})
            row["quadrant"] = "BLOCKED"
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

        evaluated = evaluate_with_scaffold(
            entry["id"],
            smiles,
            cb1_pose,
            cb2_pose,
            hu308_cb2,
            contract,
            entry.get("scaffold"),
        )
        row.update(evaluated)
        row["decoupled"] = {
            "structural_binding": row.get("structural_binding"),
            "peripheral": row.get("peripheral"),
            "global_v1_0": row.get("global_v1_0"),
            "layer_diagnosis": row.get("layer_diagnosis"),
        }
        row["quadrant"] = classify_quadrant(row["decoupled"], ident)
        row["docking"] = scores
        compounds.append(row)

    meta = {
        "phase": "D",
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
    payload = {
        "meta": meta,
        "compounds": compounds,
        "blocked_audit": list(BLOCKED_AUDIT),
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(payload, REPORT_MD)
    print(f"Report: {REPORT_MD}")
    print(f"JSON: {json_path}")
    for c in compounds:
        print(
            f"  {c['compound_id']}: quadrant={c.get('quadrant')} "
            f"GLOBAL={c.get('decoupled', {}).get('global_v1_0')}"
        )
    docked_ok = sum(
        1
        for c in compounds
        if c.get("cb1_score") is not None and c.get("cb2_score") is not None
    )
    return 0 if docked_ok >= 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
