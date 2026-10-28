#!/usr/bin/env python3
"""Phase E — Documented THCV/CBD / CB2 patent-literature derivatives vs Contract v1.0.

Level-0 identity verification, dual Vina docking (Exam A parity), THCV contract
v1.0 evaluation, mandatory Q1–Q4 quadrant classification. CONTRACT v1.0 READ-ONLY.
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
OUT_DIR = ROOT / "results/docking/screening_patents_thcv_fase_e"
REPORT_MD = ROOT / "results/docking/screening_patents_thcv_fase_e.md"
JSON_PATH = OUT_DIR / "screening_patents_fase_e.json"
GOLD_JSON = ROOT / "results/docking/benchmark_gold_exam_a/benchmark_gold_exam_a.json"

# THCV-10 / 11-carboxylate on varin scaffold (metabolite pattern mapped to gem-dimethyl bridge).
THCV_11_COOH_SMILES = (
    "CCCC1=CC(=C2[C@@H]3C=C(CC[C@H]3C(OC2=C1)(C)C(=O)O)C)O"
)
THCV_PARENT_CID = 93147
THCV_PARENT_IK = "ZROLHBHDLIHEMS-HUUCEWRRSA-N"

PANEL: tuple[dict, ...] = (
    {
        "id": "AM1710",
        "label": "AM1710 (9-methoxy cannabilactone)",
        "resolved_cid": 11268660,
        "chemome_key": None,
        "expected_inchikey": "ZAIKPEWFCSQNQB-UHFFFAOYSA-N",
        "expected_formula": "C23H28O4",
        "source": (
            "PubChem CID 11268660; ChEMBL266712; Khanolkar 2007 DOI 10.1021/jm070441u; "
            "Janus reanalysis Dhopeshwarkar 2017 DOI 10.1124/jpet.116.236539"
        ),
        "scaffold": None,
        "class": "cannabilactone_janus_literature",
        "lit_data": {
            "cb2_ki_nM": 6.7,
            "cb1_ki_nM": 360.0,
            "selectivity_fold": 54,
            "cb2_function": "agonist (GTPγS, mouse spleen)",
            "cb1_function": "low-potency inverse agonist/antagonist (Dhop 2017 reanalysis)",
            "primary_ref": "Khanolkar et al. J Med Chem 2007; PMID 18038967",
        },
    },
    {
        "id": "GW405833",
        "label": "GW405833 / L-768,242 (CB2-selective indole)",
        "resolved_cid": 9911463,
        "chemome_key": None,
        "expected_inchikey": "FSFZRNZSZYDVLI-UHFFFAOYSA-N",
        "expected_formula": "C23H24Cl2N2O3",
        "source": (
            "PubChem CID 9911463; Valenzano 2005 DOI 10.1016/j.neuropharm.2004.12.008; "
            "Janus reanalysis Dhopeshwarkar 2017 DOI 10.1124/jpet.116.236539"
        ),
        "scaffold": None,
        "class": "indole_cb2_janus_literature",
        "lit_data": {
            "cb2_ki_nM": "4–12 (human, literature range)",
            "cb1_ki_nM": "1900–4800 (human, literature range)",
            "cb2_function": "partial agonist ~50% cAMP vs CP55,940 (Valenzano abstract)",
            "cb1_function": "functional antagonism / noncompetitive CB1 (Dhop 2017)",
            "primary_ref": "Valenzano et al. Neuropharmacology 2005; PMID 15814101",
        },
    },
    {
        "id": "CBDV",
        "label": "Cannabidivarin (CBDV)",
        "resolved_cid": 11601669,
        "chemome_key": "CBDV",
        "expected_inchikey": "REOZWEGFPHTFEI-JKSUJKDBSA-N",
        "expected_formula": "C19H26O2",
        "source": (
            "PubChem CID 11601669; quimioma_semillas.csv; "
            "Walsh 2021 DOI 10.3389/fphar.2021.777804"
        ),
        "scaffold": "cannabinoid",
        "class": "propyl_varin_phytocannabinoid",
        "lit_data": {
            "cb1_profile": "low orthosteric affinity; not clean CB1-ant like THCV",
            "cb2_profile": "low–moderate; not potent canonical CB2 agonist",
            "primary_ref": "Walsh et al. Front Pharmacol 2021",
        },
    },
    {
        "id": "THCV-11-COOH",
        "label": "Δ9-THCV 11-carboxylate (C11-COOH metabolite mapping)",
        "resolved_cid": THCV_PARENT_CID,
        "chemome_key": None,
        "certified_smiles": THCV_11_COOH_SMILES,
        "expected_formula": "C19H24O4",
        "parent_inchikey": THCV_PARENT_IK,
        "source": (
            "Documented C11-carboxylate on Δ9-THCV scaffold (THCV-10); "
            "11-COOH-THCV PubChem name search 404; "
            "scripts/run_thcv_analogs_series_v1.py THCV-10; parent CID 93147"
        ),
        "scaffold": "cannabinoid",
        "class": "oxygenated_thcv_metabolite",
        "lit_data": {
            "note": "Metabolite analog per THC 11-COOH pattern on varin core; "
            "no standalone PubChem entity; direct Ki/EC50 N/A",
            "primary_ref": "Internal mapping + THCV parent literature (Pertwee 2008)",
        },
    },
    {
        "id": "HU-433",
        "label": "HU-433 (HU-308 enantiomer, CB2 agonist)",
        "resolved_cid": 59386636,
        "chemome_key": None,
        "expected_inchikey": "CFMRIVODIXTERW-JTGIGXABSA-N",
        "expected_formula": "C27H42O3",
        "source": (
            "PubChem CID 59386636; Hanus 2015 DOI 10.1073/pnas.1503395112 (PMID 26124120); "
            "patent US20110269842A1 (Yissum)"
        ),
        "scaffold": "cannabinoid",
        "class": "bicyclic_cb2_patent_literature",
        "lit_data": {
            "cb2_ki_nM": "12.2 (patent US20110269842 vs HU-308 22.7 nM); "
            "lower CP55,940 displacement vs HU-308 but higher functional potency (Hanus 2015)",
            "cb1_ki_nM": "no appreciable CB1 binding (Hanus 2015)",
            "cb2_function": "CB2-selective agonist",
            "primary_ref": "Hanus et al. PNAS 2015; US20110269842A1",
        },
    },
    {
        "id": "O-1966",
        "label": "O-1966 (cyclohexanol-fused resorcinol CB2 agonist)",
        "resolved_cid": 21087750,
        "chemome_key": None,
        "expected_inchikey": "QRVATYZBDQGJCP-UHFFFAOYSA-N",
        "expected_formula": "C24H40O3",
        "source": (
            "PubChem CID 21087750; US6166066 (Makriyannis/Khanolkar CB2-selective cannabinoids); "
            "Wiley et al. 2002; Zhang 2007 GTPγS (cited Front Pharmacol 2021)"
        ),
        "scaffold": "cannabinoid",
        "class": "polar_aliphatic_tricyclic_patent",
        "lit_data": {
            "cb2_ki_nM": "23 ± 2.1",
            "cb1_ki_nM": "5055 ± 984",
            "cb2_ec50_nM": "70 ± 14 (GTPγS)",
            "cb2_emax_pct": "74 ± 5 vs CP55,940",
            "cb2_function": "CB2-selective partial agonist",
            "primary_ref": "Wiley et al. 2002; Zhang et al. 2007 (via Front Pharmacol 2021)",
        },
    },
)

BLOCKED_AUDIT: tuple[dict, ...] = (
    {
        "id": "7-OH-THCV",
        "label": "7-hydroxy-tetrahydrocannabivarin",
        "blocker": "PubChem name search 404 — no Level-0 entity",
        "source": "PubChem PUGREST.NotFound",
    },
    {
        "id": "11-OH-THCV",
        "label": "11-hydroxy-tetrahydrocannabivarin",
        "blocker": "PubChem name search 404 — covered in Phase D as THCV-C11-OH equivalent",
        "source": "PubChem PUGREST.NotFound; Phase D precedent",
    },
    {
        "id": "AM7438",
        "label": "AM7438 (Nikas 2015 controlled-deactivation lead)",
        "blocker": "No PubChem CID; SMILES not independently cross-verified to registry",
        "source": "Nikas 2015 DOI 10.1021/jm501165d; PubChem 404",
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
    if not row.get("IsomericSMILES"):
        full_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON"
        req2 = urllib.request.Request(full_url, headers={"User-Agent": "janusforge/1.0"})
        with urllib.request.urlopen(req2, timeout=60) as resp2:
            rec = json.load(resp2)
        for prop in rec["PC_Compounds"][0]["props"]:
            urn = prop.get("urn", {})
            if urn.get("label") in ("SMILES", "Isomeric SMILES", "Canonical SMILES"):
                sval = prop.get("value", {}).get("sval")
                if sval:
                    row["IsomericSMILES"] = sval
                    break
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
        "resolved_cid": entry.get("resolved_cid"),
        "source": entry.get("source"),
        "lit_data": entry.get("lit_data"),
    }

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
            ident["smiles_source"] = "certified SMILES (documented metabolite mapping)"
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
            f"Non-cannabinoid scaffold ({compound_id}) — contract geometric proxies "
            "not mapped; STRUCTURAL INDETERMINATE"
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
            "layer_diagnosis": (
                f"estructural INDETERMINATE ({struct_blocker}); periférico evaluable"
            ),
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


def _lit_summary(lit: dict | None) -> str:
    if not lit:
        return "N/A"
    parts = []
    for k in (
        "cb2_ki_nM",
        "cb1_ki_nM",
        "cb2_ec50_nM",
        "cb2_emax_pct",
        "selectivity_fold",
        "cb2_function",
        "cb1_function",
        "cb1_profile",
        "cb2_profile",
        "note",
    ):
        if k in lit and lit[k]:
            parts.append(f"{k}: {lit[k]}")
    if not parts and lit.get("primary_ref"):
        parts.append(f"ref: {lit['primary_ref']}")
    return "; ".join(parts) if parts else "N/A"


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
        "# Phase E — Documented THCV/CBD / CB2 patent-literature derivatives vs Contract v1.0",
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
        "| **Q1** | PASS | PASS | PASS | Contract **falsificado** — precedente documentado pasa embudo |",
        "| **Q2** | PASS | FAIL | FAIL | Desacoplamiento: geometría OK, polaridad insuficiente |",
        "| **Q3** | FAIL | PASS | FAIL | Desacoplamiento: TPSA OK, geometría CB1/CB2 fail |",
        "| **Q4** | FAIL | FAIL | FAIL | Rechazo concomitante |",
        "",
        "## Level-0 identidad (pre-PDBQT)",
        "",
        "| Compuesto | CID / Registro | Fórmula | InChIKey resuelto | Estado | Fuente |",
        "|-----------|----------------|---------|-------------------|--------|--------|",
    ]

    for r in rows:
        ident = r.get("identity", {})
        cid = ident.get("resolved_cid") or "—"
        ik = ident.get("resolved_inchikey") or ident.get("pubchem_inchikey") or "—"
        lines.append(
            f"| {r['compound_id']} | {cid} | {ident.get('pubchem_formula', '—')} | "
            f"`{ik}` | **{ident.get('identity_status', '—')}** | "
            f"{(ident.get('smiles_source') or ident.get('source', '—'))[:90]} |"
        )

    if blocked:
        lines.extend(["", "### Auditoría BLOCK (no incluidos en panel dockado)", ""])
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
            "## Matriz principal — lit vs simulación separados",
            "",
            "| Compuesto | **Experimental (lit)** | Score CB1 | Score CB2 | STRUCTURAL | "
            "PERIPHERAL | Cuadrante | GLOBAL | Sub-checks simulación |",
            "|-----------|------------------------|-----------|-----------|------------|"
            "-----------|-----------|--------|----------------------|",
        ]
    )

    q_counts = {"Q1": [], "Q2": [], "Q3": [], "Q4": [], "INDET.": [], "BLOCKED": []}
    lit_active_contract_fail: list[str] = []

    for r in rows:
        ident = r.get("identity", {})
        dec = r.get("decoupled", {})
        quad = r.get("quadrant", "—")
        if quad in q_counts:
            q_counts[quad].append(r["compound_id"])

        lit = _lit_summary(ident.get("lit_data"))

        if ident.get("identity_status") == "BLOCKED":
            lines.append(
                f"| {r['compound_id']} | {lit[:60]} | — | — | **INDET.** | **INDET.** | "
                f"**BLOCKED** | BLOCKED | {ident.get('blocker', '—')} |"
            )
            continue

        cb1f = r.get("cb1_filter", {})
        cb2f = r.get("cb2_filter", {})
        ad = r.get("admet", {})
        tpsa = ad.get("tpsa_A2")
        periph = dec.get("peripheral", "—")
        periph_label = f"{'PASS' if ad.get('pass') else 'FAIL'} ({tpsa} Å²)" if tpsa else "—"
        breakdown = _subcheck_lines(cb1f, cb2f, ad)
        global_v = dec.get("global_v1_0", "—")

        if lit != "N/A" and global_v == "FAIL" and dec.get("structural_binding") != "INDETERMINATE":
            lit_active_contract_fail.append(r["compound_id"])

        lines.append(
            f"| {r['compound_id']} | {lit[:100]} | {_fmt(r.get('cb1_score'))} | "
            f"{_fmt(r.get('cb2_score'))} | **{dec.get('structural_binding', '—')}** | "
            f"**{periph_label}** | **{quad}** | **{global_v}** | {breakdown} |"
        )

    eval_rows = [
        r for r in rows if r.get("identity", {}).get("identity_status") == "PASS_IDENTITY"
    ]

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
            "### Discrepancias lit-activo vs contract FAIL",
            "",
        ]
    )

    if lit_active_contract_fail:
        lines.append(
            f"- **Metodológicas (lit activo, contract FAIL sin retune):** "
            f"{', '.join(lit_active_contract_fail)}"
        )
    else:
        lines.append(
            "- Ninguna discrepancia lit-vs-contract evaluable en compuestos con scaffold "
            "mapeado y datos experimentales cuantitativos."
        )

    lines.extend(["", "### Conclusión Phase E", ""])

    if q_counts["Q1"]:
        lines.append(
            f"- **Contract v1.0 falsificado:** {', '.join(q_counts['Q1'])} alcanza Q1."
        )
    else:
        lines.append(
            "- **Contract v1.0 NO falsificado** en panel patent/literatura documentado: "
            "ningún derivado alcanza Q1."
        )

    if q_counts["Q2"] or q_counts["Q3"]:
        lines.append(
            f"- **Desacoplamiento real:** Q2={', '.join(q_counts['Q2']) or '—'}; "
            f"Q3={', '.join(q_counts['Q3']) or '—'}."
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
                "#### 1. Level-0 identidad",
                f"- Clase: {ident.get('class', '—')}",
                f"- SMILES: `{ident.get('smiles')}`",
                f"- Fuente: {ident.get('source', '—')}",
                "",
                "#### 2. Experimental (literatura) — NO mezclar con docking",
                f"- {_lit_summary(ident.get('lit_data'))}",
                f"- Ref: {(ident.get('lit_data') or {}).get('primary_ref', '—')}",
                "",
                "#### 3. Simulación Contract v1.0",
                f"- CB1 score: {_fmt(r.get('cb1_score'))} kcal/mol",
                f"- CB2 score: {_fmt(r.get('cb2_score'))} kcal/mol",
                f"- STRUCTURAL_BINDING: **{r.get('decoupled', {}).get('structural_binding', '—')}**",
                f"- PERIPHERAL: **{r.get('decoupled', {}).get('peripheral', '—')}** "
                f"(TPSA {r.get('admet', {}).get('tpsa_A2')} Å²)",
                f"- Cuadrante: **{r.get('quadrant', '—')}**",
                f"- GLOBAL v1.0: **{r.get('decoupled', {}).get('global_v1_0', '—')}**",
                f"- Diagnóstico capas: {r.get('decoupled', {}).get('layer_diagnosis', '—')}",
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
        if ident.get("blocker"):
            print(f"    blocker: {ident['blocker']}")

    json_path = args.out_dir / "screening_patents_fase_e.json"
    if args.report_only:
        if not json_path.exists():
            print(f"BLOQUEO: --report-only pero falta {json_path}")
            return 2
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        write_report(payload, REPORT_MD)
        print(f"Report: {REPORT_MD}")
        return 0

    for v in RECEPTORS.values():
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
        "phase": "E",
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
