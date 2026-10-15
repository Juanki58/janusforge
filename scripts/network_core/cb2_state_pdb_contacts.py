#!/usr/bin/env python3
"""EXTERNAL — Dutta & Shukla 2023 CB2 state-representative PDB contact maps.

Governance: docs/synthesis/EXPERIMENT_CB2_STATE_PDB_CONTACTS.md (pre-registered).
  - Snapshot-only soft A/B/C at contact-map level.
  - Does NOT reopen P2 as CONVERGENT; does NOT resurrect P1 hub hunt.
  - One PDB per state ≠ ensemble.

Outputs:
  results/network_core/cb2_state_pdb_contacts.{md,json}
  results/network_core/cb2_state_pdb_contacts_overlap.png
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "network_core"))

from dynamic_pipeline import HUBS, HUB_LABELS  # noqa: E402
from p1_dynamic_hub_validation import (  # noqa: E402
    CONTACT_DEF,
    _MAX_CUT,
    _SLACK,
    _VDW,
    res_label,
)

try:
    import MDAnalysis as mda
    from MDAnalysis.lib.distances import capped_distance
except ImportError as e:  # pragma: no cover
    raise SystemExit(f"MDAnalysis required: {e}") from e

# ---------------------------------------------------------------------------
# Locked a priori (see EXPERIMENT_CB2_STATE_PDB_CONTACTS.md)
# ---------------------------------------------------------------------------

PDB_DIR = ROOT / "data" / "external" / "dutta_shukla_2023" / "main_figure_6"
MANIFEST = PDB_DIR / "MANIFEST.json"
UNIPROT_P34972 = (
    "MEECWVTEIANGSKDGLDSNPMKDYMILSGPQKTAVAVLCTLLGLLSALENVAVLYLILSSHQLRRKPSYLFIGSLAGADFLASVVFACSFVNFHVFHGVDSKAVFLLKIGSVTMTFTAS"
    "VGSLLLTAIDRYLCLRYPPSYKALLTRGRALVTLGIMWVLSALVSYLPLMGWTCCPRPCSELFPLIPNDYLLSWLLFIAFLFSGIIYTYGHVLWKAHQHVASLSGHQDRQVPGMARMRLD"
    "VRLAKTLGLVLAVLLICWFPVLALMAHSLATTLSDQVKKAFAFCSMLCLINSMVNPVIYALRSGEIRSSAHHCLAHWKKCVRGLGSEAKEEAPRSSVTETEADGKITPWPDSRDLDLSDC"
)

# Path order from filenames / Fig. 6 (NOT MSM pickle order I1,I2,I3,Inactive,I4,Active)
STATE_ORDER = ["inactive", "I1", "I2", "I3", "I4", "active"]
STATE_FILES = {
    "inactive": "CB2_ref_inactive_3_b.pdb",
    "I1": "CB2_ref_inactive_I1_b.pdb",
    "I2": "CB2_ref_inactive_I2_b.pdb",
    "I3": "CB2_ref_inactive_I3_b.pdb",
    "I4": "CB2_ref_inactive_I4_b.pdb",
    "active": "CB2_ref_inactive_active_b.pdb",
}

THR_MEAN_J_STABLE = 0.80
THR_FRAC_CORE_STABLE = 0.60
THR_FRAC_SPECIFIC_B = 0.15
THR_PATH_TURNOVER_B = 0.20
THR_MEAN_J_DIFFUSE = 0.55
THR_SUBSTANTIAL = 0.80  # mean_jaccard below → DIFFERS_SUBSTANTIALLY (or turnover)

CA_CUTOFF_A = 8.0
CA_MIN_SEP = 2

AA3_TO_1 = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "CYX": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIE": "H",
    "HID": "H",
    "HIP": "H",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}

OUT_DIR = ROOT / "results" / "network_core"
OUT_JSON = OUT_DIR / "cb2_state_pdb_contacts.json"
OUT_MD = OUT_DIR / "cb2_state_pdb_contacts.md"
OUT_PNG = OUT_DIR / "cb2_state_pdb_contacts_overlap.png"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def jaccard(a: set[tuple[str, str]], b: set[tuple[str, str]]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return float(inter) / float(union) if union else 0.0


def edge_key(u: str, v: str) -> tuple[str, str]:
    return (u, v) if u <= v else (v, u)


def nw_align(a: str, b: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> tuple[str, str]:
    """Needleman–Wunsch global alignment (compact)."""
    n, m = len(a), len(b)
    score = np.zeros((n + 1, m + 1), dtype=np.int32)
    ptr = np.zeros((n + 1, m + 1), dtype=np.uint8)  # 0=diag, 1=up, 2=left
    for i in range(1, n + 1):
        score[i, 0] = i * gap
        ptr[i, 0] = 1
    for j in range(1, m + 1):
        score[0, j] = j * gap
        ptr[0, j] = 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            s = match if ai == b[j - 1] else mismatch
            diag = score[i - 1, j - 1] + s
            up = score[i - 1, j] + gap
            left = score[i, j - 1] + gap
            best = diag
            p = 0
            if up > best:
                best = up
                p = 1
            if left > best:
                best = left
                p = 2
            score[i, j] = best
            ptr[i, j] = p
    # traceback
    i, j = n, m
    ra: list[str] = []
    rb: list[str] = []
    while i > 0 or j > 0:
        p = ptr[i, j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if i > 0 and j > 0 and p == 0:
            ra.append(a[i - 1])
            rb.append(b[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or p == 1):
            ra.append(a[i - 1])
            rb.append("-")
            i -= 1
        else:
            ra.append("-")
            rb.append(b[j - 1])
            j -= 1
    return "".join(reversed(ra)), "".join(reversed(rb))


def map_hubs_to_pdb(u: mda.Universe) -> dict[str, Any]:
    """Align PDB protein seq to UniProt; map hub UniProt indices."""
    residues = [r for r in u.residues if r.resname not in ("ACE", "NME")]
    pdb_resids: list[int] = []
    pdb_aas: list[str] = []
    for r in residues:
        aa = AA3_TO_1.get(r.resname)
        if aa is None:
            continue
        pdb_resids.append(int(r.resid))
        pdb_aas.append(aa)
    pdb_seq = "".join(pdb_aas)
    up_aln, pdb_aln = nw_align(UNIPROT_P34972, pdb_seq)
    up_i = 0
    pdb_i = 0
    up_to_pdb: dict[int, tuple[int, str]] = {}
    n_match = 0
    n_aligned = 0
    for ua, pa in zip(up_aln, pdb_aln):
        if ua != "-":
            up_i += 1
        if pa != "-":
            resid = pdb_resids[pdb_i]
            pdb_i += 1
            if ua != "-":
                up_to_pdb[up_i] = (resid, pa)
                n_aligned += 1
                if ua == pa:
                    n_match += 1
    identity = float(n_match) / float(n_aligned) if n_aligned else 0.0

    mapped: dict[str, Any] = {}
    for hub in HUBS:
        up_num = int(hub["label"].split(":")[1])
        expect_aa = hub["label"].split(":")[0]
        expect_1 = AA3_TO_1[expect_aa]
        hit = up_to_pdb.get(up_num)
        if hit is None:
            mapped[hub["label"]] = {
                "status": "HUB_MAP_FAIL",
                "reason": "uniprot_index_not_in_alignment",
                "uniprot": up_num,
                "expected_aa": expect_aa,
            }
            continue
        resid, aa1 = hit
        # recover 3-letter from residue
        sel = u.select_atoms(f"resid {resid}")
        resname = str(sel.residues.resnames[0]) if len(sel) else "?"
        label = res_label(resname, resid)
        ok = aa1 == expect_1 and resname.upper()[:3] == expect_aa
        # CYX/HIE etc.: compare 1-letter
        ok = aa1 == expect_1
        mapped[hub["label"]] = {
            "status": "OK" if ok else "HUB_MAP_FAIL",
            "reason": None if ok else f"aa_mismatch_expected_{expect_aa}_got_{resname}",
            "uniprot": up_num,
            "expected_aa": expect_aa,
            "pdb_resid": resid,
            "pdb_resname": resname,
            "pdb_label": label,
            "aligned_aa1": aa1,
        }
    return {
        "alignment_identity": identity,
        "n_pdb_residues": len(pdb_resids),
        "hubs": mapped,
    }


def contacts_vdw(u: mda.Universe) -> tuple[set[tuple[str, str]], list[str]]:
    """Binary residue-pair contacts under P1 VdW envelope (single frame)."""
    sel = u.select_atoms("protein")
    heavy = sel.select_atoms("not name H*")
    if len(heavy) == 0:
        return set(), []

    elements: list[str] = []
    for atom in heavy:
        el = (atom.element if hasattr(atom, "element") else "").upper()
        if not el or el == "DUMMY":
            el = "".join(c for c in atom.name if c.isalpha())[:2].upper()
            if el.startswith("CL"):
                el = "CL"
            elif el.startswith("BR"):
                el = "BR"
            else:
                el = el[:1] if el else "C"
        if el not in _VDW:
            el = "C"
        elements.append(el)

    labels = [res_label(rn, int(ri)) for rn, ri in zip(heavy.resnames, heavy.resids)]
    unique_labels = sorted(set(labels), key=lambda x: (x.split(":")[0], int(x.split(":")[1])))
    label_index = {lab: i for i, lab in enumerate(unique_labels)}
    atom_lab_idx = np.asarray([label_index[lab] for lab in labels], dtype=np.int32)
    radii = np.asarray([_VDW[e] for e in elements], dtype=np.float64)
    resnums = np.asarray([int(lab.split(":")[1]) for lab in unique_labels], dtype=np.int32)

    pos = heavy.positions
    pairs = capped_distance(pos, pos, max_cutoff=_MAX_CUT, return_distances=True)
    edges: set[tuple[str, str]] = set()
    if pairs[0].size == 0:
        return edges, unique_labels

    idx, dist = pairs
    mask = idx[:, 0] < idx[:, 1]
    idx = idx[mask]
    dist = dist[mask]
    lim = radii[idx[:, 0]] + radii[idx[:, 1]] + _SLACK
    hit = dist < lim
    idx = idx[hit]
    if idx.size == 0:
        return edges, unique_labels

    li = atom_lab_idx[idx[:, 0]]
    lj = atom_lab_idx[idx[:, 1]]
    same = li != lj
    li, lj = li[same], lj[same]
    exclude_seq = bool(CONTACT_DEF["exclude_sequential_protein"])
    seen: set[tuple[int, int]] = set()
    for a, b in zip(li.tolist(), lj.tolist()):
        if a > b:
            a, b = b, a
        if (a, b) in seen:
            continue
        seen.add((a, b))
        if exclude_seq and abs(int(resnums[a]) - int(resnums[b])) == 1:
            continue
        edges.add(edge_key(unique_labels[a], unique_labels[b]))
    return edges, unique_labels


def contacts_ca(u: mda.Universe) -> set[tuple[str, str]]:
    """Secondary Cα–Cα contacts within 8 Å, |Δresid| >= 2."""
    cas = u.select_atoms("protein and name CA")
    if len(cas) < 2:
        return set()
    labels = [res_label(rn, int(ri)) for rn, ri in zip(cas.resnames, cas.resids)]
    resnums = cas.resids.astype(int)
    # self_distance_array returns condensed; use capped_distance
    pos = cas.positions
    pairs = capped_distance(pos, pos, max_cutoff=CA_CUTOFF_A, return_distances=False)
    edges: set[tuple[str, str]] = set()
    if pairs.size == 0:
        return edges
    mask = pairs[:, 0] < pairs[:, 1]
    pairs = pairs[mask]
    for i, j in pairs:
        if abs(int(resnums[i]) - int(resnums[j])) < CA_MIN_SEP:
            continue
        edges.add(edge_key(labels[i], labels[j]))
    return edges


def hub_participation(
    edges: set[tuple[str, str]],
    hub_map: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for hub_lab, info in hub_map["hubs"].items():
        if info.get("status") != "OK":
            out[hub_lab] = {"status": info.get("status"), "degree": None, "neighbors": []}
            continue
        node = info["pdb_label"]
        nbrs = sorted({v if u == node else u for u, v in edges if u == node or v == node})
        out[hub_lab] = {
            "status": "OK",
            "pdb_label": node,
            "degree": len(nbrs),
            "neighbors": nbrs,
        }
    return out


def assign_verdicts(
    mean_j: float,
    frac_core: float,
    frac_spec: float,
    path_turnover: float,
) -> dict[str, str]:
    if mean_j >= THR_MEAN_J_STABLE and frac_core >= THR_FRAC_CORE_STABLE:
        primary = "EXT_PDB_CONTACTS_STABLE"
        snap = "EXT_STRUCTURAL_ABC_SNAPSHOT_A"
    elif (frac_spec >= THR_FRAC_SPECIFIC_B) or (path_turnover >= THR_PATH_TURNOVER_B):
        primary = "EXT_PDB_CONTACTS_STATE_DEPENDENT"
        snap = "EXT_STRUCTURAL_ABC_SNAPSHOT_B"
    elif mean_j < THR_MEAN_J_DIFFUSE and frac_spec < THR_FRAC_SPECIFIC_B:
        primary = "EXT_PDB_CONTACTS_DIFFUSE"
        snap = "EXT_STRUCTURAL_ABC_SNAPSHOT_C"
    else:
        primary = "EXT_PDB_CONTACTS_INDETERMINATE"
        snap = "EXT_STRUCTURAL_ABC_SNAPSHOT_INDETERMINATE"

    q1 = (
        "DIFFERS_SUBSTANTIALLY"
        if (mean_j < THR_SUBSTANTIAL or path_turnover >= THR_PATH_TURNOVER_B)
        else "SIMILAR_OVERALL"
    )
    return {
        "EXT_PDB_CONTACTS": primary,
        "EXT_STRUCTURAL_ABC": snap,
        "Q1_MAPS": q1,
    }


def write_overlap_plot(matrix: np.ndarray, labels: list[str], path: Path) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(matrix, vmin=0.0, vmax=1.0, cmap="viridis")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    ax.set_title("Pairwise contact Jaccard (VdW+0.5Å)")
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", fontsize=8, color="w")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)


def render_md(payload: dict[str, Any]) -> str:
    v = payload["verdicts"]
    m = payload["metrics_primary"]
    lines = [
        "# EXTERNAL — CB2 state PDB contact maps (Dutta & Shukla 2023)",
        "",
        f"**Generated (UTC):** `{payload['generated_utc']}`",
        f"**Branch:** `{payload['branch']}`",
        f"**Pre-reg:** `docs/synthesis/EXPERIMENT_CB2_STATE_PDB_CONTACTS.md`",
        "",
        "## Epistemology",
        "",
        "- EXTERNAL structural **snapshot** comparison of published state PDBs.",
        "- **One PDB ≠ ensemble.** Not P2 CONVERGENT; not Gi mechanism; not P1 hub hunt.",
        "",
        "## Verdicts",
        "",
        f"- **`{v['EXT_PDB_CONTACTS']}`**",
        f"- **`{v['EXT_STRUCTURAL_ABC']}`** (snapshot-only soft A/B/C)",
        f"- Q1 maps: `{v['Q1_MAPS']}`",
        "",
        "## Contact definition",
        "",
        f"- Primary: `{payload['contact_def']['name']}` — {payload['contact_def']['geometry']}",
        f"- Exclude sequential `|Δresid|==1`: `{payload['contact_def']['exclude_sequential_protein']}`",
        f"- Secondary (sensitivity): Cα < {CA_CUTOFF_A} Å, `|Δresid|>={CA_MIN_SEP}`",
        "",
        "## Data / integrity",
        "",
    ]
    for st in STATE_ORDER:
        rec = payload["states"][st]
        lines.append(
            f"- `{st}`: `{rec['file']}` sha256=`{rec['sha256'][:12]}…` "
            f"n_edges_vdw={rec['n_edges_vdw']} n_edges_ca={rec['n_edges_ca']}"
        )
    lines += [
        "",
        f"- Manifest verified: `{payload['manifest_ok']}`",
        f"- Hub alignment identity (inactive ref): `{payload['hub_mapping']['alignment_identity']:.4f}`",
        "",
        "## Pairwise Jaccard (primary VdW)",
        "",
        f"- mean={m['mean_jaccard']:.4f}  min={m['min_jaccard']:.4f}  max={m['max_jaccard']:.4f}",
        f"- frac_core={m['frac_core']:.4f}  frac_state_specific={m['frac_state_specific']:.4f}",
        f"- path_turnover_frac={m['path_turnover_frac']:.4f}",
        "",
        "### Matrix",
        "",
        "| | " + " | ".join(STATE_ORDER) + " |",
        "|" + "|".join(["---"] * (len(STATE_ORDER) + 1)) + "|",
    ]
    mat = m["jaccard_matrix"]
    for i, s in enumerate(STATE_ORDER):
        row = " | ".join(f"{mat[i][j]:.3f}" for j in range(len(STATE_ORDER)))
        lines.append(f"| **{s}** | {row} |")

    lines += ["", "## Path turnover (inactive→…→active)", ""]
    for step in payload["path_steps"]:
        lines.append(
            f"- `{step['from']}→{step['to']}`: appear={step['n_appear']} "
            f"disappear={step['n_disappear']} turnover={step['turnover_frac']:.3f}"
        )
        if step["appear_top"]:
            lines.append(f"  - appear sample: {', '.join(step['appear_top'][:8])}")
        if step["disappear_top"]:
            lines.append(f"  - disappear sample: {', '.join(step['disappear_top'][:8])}")

    lines += ["", "## LigACN hubs (descriptive)", ""]
    for hub in HUB_LABELS:
        info = payload["hub_mapping"]["hubs"][hub]
        lines.append(
            f"- `{hub}`: status=`{info['status']}` "
            f"pdb=`{info.get('pdb_label')}` resid=`{info.get('pdb_resid')}` "
            f"aa=`{info.get('pdb_resname')}`"
            + (f" ({info.get('reason')})" if info.get("reason") else "")
        )
    lines += ["", "### Per-state hub degrees", ""]
    lines.append("| hub | " + " | ".join(STATE_ORDER) + " |")
    lines.append("|" + "|".join(["---"] * (len(STATE_ORDER) + 1)) + "|")
    for hub in HUB_LABELS:
        deg = []
        for st in STATE_ORDER:
            hp = payload["states"][st]["hub_participation"].get(hub, {})
            d = hp.get("degree")
            deg.append("—" if d is None else str(d))
        lines.append(f"| `{hub}` | " + " | ".join(deg) + " |")

    ca = payload["metrics_secondary_ca"]
    lines += [
        "",
        "## Secondary Cα 8Å (sensitivity)",
        "",
        f"- mean_jaccard_ca={ca['mean_jaccard']:.4f} (not used for verdicts)",
        "",
        "## Forbidden claims (reminder)",
        "",
        "- No Gi mechanism; no docking/de novo; no P2 CONVERGENT; snapshot ≠ ensemble.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Verify manifest hashes
    manifest_ok = True
    manifest_detail: dict[str, Any] = {}
    if MANIFEST.is_file():
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        by_name = {f["name"]: f for f in man.get("files", [])}
        for st, fname in STATE_FILES.items():
            path = PDB_DIR / fname
            got = sha256_file(path)
            exp = by_name.get(fname, {}).get("sha256")
            ok = (exp is None) or (got == exp)
            if not ok:
                manifest_ok = False
            manifest_detail[fname] = {"sha256": got, "expected": exp, "ok": ok}
    else:
        manifest_ok = False

    # Load states
    state_edges: dict[str, set[tuple[str, str]]] = {}
    state_edges_ca: dict[str, set[tuple[str, str]]] = {}
    state_payload: dict[str, Any] = {}
    hub_mapping_ref: dict[str, Any] | None = None

    for st in STATE_ORDER:
        path = PDB_DIR / STATE_FILES[st]
        if not path.is_file():
            raise SystemExit(f"Missing PDB: {path}")
        u = mda.Universe(str(path))
        if hub_mapping_ref is None:
            hub_mapping_ref = map_hubs_to_pdb(u)
        edges, _labels = contacts_vdw(u)
        edges_ca = contacts_ca(u)
        # Remap hubs on each structure (resid numbering should be identical across refs)
        hub_map_st = map_hubs_to_pdb(u)
        hp = hub_participation(edges, hub_map_st)
        state_edges[st] = edges
        state_edges_ca[st] = edges_ca
        state_payload[st] = {
            "file": STATE_FILES[st],
            "sha256": sha256_file(path),
            "n_atoms": int(u.atoms.n_atoms),
            "n_residues": int(u.residues.n_residues),
            "n_edges_vdw": len(edges),
            "n_edges_ca": len(edges_ca),
            "hub_participation": hp,
            "hub_mapping_status": {
                k: v.get("status") for k, v in hub_map_st["hubs"].items()
            },
        }

    assert hub_mapping_ref is not None

    # Pairwise Jaccard
    n = len(STATE_ORDER)
    mat = np.zeros((n, n), dtype=float)
    for i, s in enumerate(STATE_ORDER):
        for j, t in enumerate(STATE_ORDER):
            mat[i, j] = jaccard(state_edges[s], state_edges[t])
    pairs = [mat[i, j] for i in range(n) for j in range(i + 1, n)]
    mean_j = float(np.mean(pairs)) if pairs else 0.0
    min_j = float(np.min(pairs)) if pairs else 0.0
    max_j = float(np.max(pairs)) if pairs else 0.0

    core = set.intersection(*(state_edges[s] for s in STATE_ORDER))
    union = set.union(*(state_edges[s] for s in STATE_ORDER))
    frac_core = float(len(core) / len(union)) if union else 0.0

    spec_fracs: list[float] = []
    n_specific: dict[str, int] = {}
    for s in STATE_ORDER:
        others = set.union(*(state_edges[t] for t in STATE_ORDER if t != s))
        only = state_edges[s] - others
        n_specific[s] = len(only)
        spec_fracs.append(len(only) / max(len(state_edges[s]), 1))
    frac_spec = float(np.mean(spec_fracs)) if spec_fracs else 0.0

    # Path turnover
    path_steps: list[dict[str, Any]] = []
    turnovers: list[float] = []
    for a, b in zip(STATE_ORDER, STATE_ORDER[1:]):
        ea, eb = state_edges[a], state_edges[b]
        appear = eb - ea
        disappear = ea - eb
        uab = ea | eb
        tf = float((len(appear) + len(disappear)) / len(uab)) if uab else 0.0
        turnovers.append(tf)

        def fmt_edge(e: tuple[str, str]) -> str:
            return f"{e[0]}–{e[1]}"

        path_steps.append(
            {
                "from": a,
                "to": b,
                "n_appear": len(appear),
                "n_disappear": len(disappear),
                "turnover_frac": tf,
                "appear_top": sorted(fmt_edge(e) for e in appear)[:25],
                "disappear_top": sorted(fmt_edge(e) for e in disappear)[:25],
            }
        )
    path_turnover = float(np.mean(turnovers)) if turnovers else 0.0

    # Secondary CA metrics
    mat_ca = np.zeros((n, n), dtype=float)
    for i, s in enumerate(STATE_ORDER):
        for j, t in enumerate(STATE_ORDER):
            mat_ca[i, j] = jaccard(state_edges_ca[s], state_edges_ca[t])
    pairs_ca = [mat_ca[i, j] for i in range(n) for j in range(i + 1, n)]
    mean_j_ca = float(np.mean(pairs_ca)) if pairs_ca else 0.0

    # Hub neighborhood Jaccard across states (descriptive)
    hub_edge_jaccard: dict[str, float] = {}
    for hub in HUB_LABELS:
        sets: list[set[tuple[str, str]]] = []
        for st in STATE_ORDER:
            hp = state_payload[st]["hub_participation"].get(hub, {})
            node = hp.get("pdb_label")
            if not node or hp.get("degree") is None:
                sets = []
                break
            he = {edge_key(u, v) for u, v in state_edges[st] if u == node or v == node}
            sets.append(he)
        if len(sets) == 6:
            pj = [
                jaccard(sets[i], sets[j])
                for i in range(6)
                for j in range(i + 1, 6)
            ]
            hub_edge_jaccard[hub] = float(np.mean(pj))
        else:
            hub_edge_jaccard[hub] = float("nan")

    verdicts = assign_verdicts(mean_j, frac_core, frac_spec, path_turnover)

    write_overlap_plot(mat, STATE_ORDER, OUT_PNG)

    payload: dict[str, Any] = {
        "generated_utc": generated,
        "branch": "feat/cb2-hubs-functional-topology-test",
        "experiment": "EXPERIMENT_CB2_STATE_PDB_CONTACTS",
        "epistemology": {
            "scope": "EXTERNAL_STRUCTURAL_SNAPSHOT",
            "one_pdb_neq_ensemble": True,
            "p2_unchanged": True,
            "no_gi_claim": True,
            "no_docking": True,
            "no_p1_hub_hunt": True,
        },
        "contact_def": {
            "name": CONTACT_DEF["name"],
            "geometry": CONTACT_DEF["geometry"],
            "slack_A": CONTACT_DEF["slack_A"],
            "exclude_sequential_protein": CONTACT_DEF["exclude_sequential_protein"],
            "selection": "protein",
            "limitation": CONTACT_DEF["limitation"],
        },
        "secondary_ca_def": {
            "cutoff_A": CA_CUTOFF_A,
            "min_sep": CA_MIN_SEP,
            "drives_verdict": False,
        },
        "thresholds": {
            "mean_jaccard_stable": THR_MEAN_J_STABLE,
            "frac_core_stable": THR_FRAC_CORE_STABLE,
            "frac_state_specific_B": THR_FRAC_SPECIFIC_B,
            "path_turnover_B": THR_PATH_TURNOVER_B,
            "mean_jaccard_diffuse": THR_MEAN_J_DIFFUSE,
        },
        "state_order": STATE_ORDER,
        "manifest_ok": manifest_ok,
        "manifest_detail": manifest_detail,
        "hub_mapping": hub_mapping_ref,
        "hub_incident_mean_jaccard": hub_edge_jaccard,
        "states": state_payload,
        "metrics_primary": {
            "mean_jaccard": mean_j,
            "min_jaccard": min_j,
            "max_jaccard": max_j,
            "frac_core": frac_core,
            "n_core_edges": len(core),
            "n_union_edges": len(union),
            "frac_state_specific": frac_spec,
            "n_state_specific": n_specific,
            "path_turnover_frac": path_turnover,
            "jaccard_matrix": mat.tolist(),
        },
        "metrics_secondary_ca": {
            "mean_jaccard": mean_j_ca,
            "jaccard_matrix": mat_ca.tolist(),
        },
        "path_steps": path_steps,
        "verdicts": verdicts,
        "outputs": {
            "json": str(OUT_JSON.relative_to(ROOT)),
            "md": str(OUT_MD.relative_to(ROOT)),
            "png": str(OUT_PNG.relative_to(ROOT)),
        },
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")

    print(f"[cb2_state_pdb_contacts] {verdicts['EXT_PDB_CONTACTS']}")
    print(f"[cb2_state_pdb_contacts] {verdicts['EXT_STRUCTURAL_ABC']}")
    print(f"[cb2_state_pdb_contacts] Q1={verdicts['Q1_MAPS']}")
    print(f"[cb2_state_pdb_contacts] mean_jaccard={mean_j:.4f} frac_core={frac_core:.4f}")
    print(f"[cb2_state_pdb_contacts] wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
