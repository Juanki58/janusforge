#!/usr/bin/env python3
"""Qiu 0J — visual QC snapshots of best CB2 poses (MODEL 1 only).

Read-only inputs: existing docked PDBQTs + receptor.
No re-docking, no Vina, no PDBQT / receptor edits.

Writes under results/reports/qiu_0j_visual_qc/:
  - static PNG projections (xz / xy)
  - interactive 3Dmol HTML (local CDN)
  - overlay comparison PNGs
  - metrics JSON (observation coordinates only)
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_qiu_0g_poses import (  # noqa: E402
    BOX_CENTER,
    load_receptor_chain_r,
    orientation_summary,
    residue_key,
)
from compare_qiu_0g_vs_d1_cb2 import (  # noqa: E402
    ligand_heavy_centroid,
    parse_poses,
    region_occupation,
)
from compare_qiu_d1_pharmacophore_geometry import (  # noqa: E402
    d2_features,
    load_library_smiles,
    qiu_features,
    region_min_dists,
)

RECEPTOR = ROOT / "data" / "targets" / "cb2" / "6PT0_rec.pdbqt"
QIU_DIR = ROOT / "results" / "docking" / "qiu_0f"
D1_DIR = ROOT / "results" / "docking" / "option_d_batch2" / "cb2"
OUT_DIR = ROOT / "results" / "reports" / "qiu_0j_visual_qc"
OUT_JSON = OUT_DIR / "qiu_0j_visual_qc_metrics.json"

REGION = ("SER285", "TYR25", "THR114", "ILE110", "ILE186")
HIGHLIGHT_RES = ("TYR25", "SER285", "THR114", "ILE110", "ILE186", "PHE91", "PHE183", "TRP194")

QIU_IDS = (14, 15, 20, 24)
D2_IDS = ("JANUS_D2_20", "JANUS_D2_06", "JANUS_D2_22")

# Feature colors for overlays (observation markers only)
QIU_FEAT_COLORS = {
    "adamantyl": "#d97706",
    "n1_heterocycle": "#2563eb",
    "pyrazole": "#7c3aed",
    "c5_phenyl": "#059669",
    "amide": "#dc2626",
}
D2_FEAT_COLORS = {
    "benzoyl_aryl": "#d97706",
    "n1_benzyl_aryl": "#2563eb",
    "pyrrole": "#7c3aed",
    "c2_phenyl": "#059669",
    "aryl_ketone": "#dc2626",
}


def best_model(poses: list[dict]) -> dict:
    return min(poses, key=lambda p: p["vina_score"])


def atoms_to_pdb_block(atoms: list[dict], resn: str = "LIG", chain: str = "L") -> str:
    lines = []
    for i, a in enumerate(atoms, start=1):
        x, y, z = a["xyz"]
        name = (a.get("name") or a.get("atype") or "C")[:4]
        atype = (a.get("atype") or "C")[:3]
        lines.append(
            f"HETATM{i:5d} {name:<4s} {resn:3s} {chain}{1:4d}    "
            f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {atype:>2s}"
        )
    lines.append("END")
    return "\n".join(lines)


def residue_atoms(rec: list[dict], keys: set[str]) -> list[dict]:
    return [a for a in rec if residue_key(a) in keys]


def pocket_rec_atoms(rec: list[dict], lig_cent: np.ndarray, radius: float = 12.0) -> list[dict]:
    out = []
    for a in rec:
        if not a["heavy"]:
            continue
        if np.linalg.norm(a["xyz"] - lig_cent) <= radius:
            out.append(a)
    return out


def feature_centroids(pose: dict, feat_serials: dict[str, list[int]]) -> dict[str, list[float]]:
    by_serial = {a["serial"]: a for a in pose["atoms"]}
    cents = {}
    for name, serials in feat_serials.items():
        pts = [by_serial[s]["xyz"] for s in serials if s in by_serial and by_serial[s]["heavy"]]
        if pts:
            cents[name] = np.mean(np.vstack(pts), axis=0).tolist()
    return cents


def dominant_axis(core: np.ndarray, feat: np.ndarray) -> str:
    d = feat - core
    ax = int(np.argmax(np.abs(d)))
    sign = "+" if d[ax] >= 0 else "-"
    return f"{sign}{'xyz'[ax]}"


def load_entry(label: str, path: Path, series: str, cid) -> dict:
    poses = parse_poses(path)
    if not poses:
        raise RuntimeError(f"No MODEL poses in {path}")
    best = best_model(poses)
    # Prefer MODEL 1 if it is also the best score (expected for these files)
    model1 = next((p for p in poses if p["model"] == 1), None)
    pose = model1 if model1 is not None else best
    if model1 is not None and abs(model1["vina_score"] - best["vina_score"]) > 1e-6:
        # Still use MODEL 1 per 0J brief (best poses = MODEL 1); flag mismatch
        pose_note = f"MODEL 1 score {model1['vina_score']} != lowest {best['vina_score']}"
    else:
        pose_note = "MODEL 1 is lowest Vina REMARK among written models"
    return {
        "label": label,
        "series": series,
        "compound_id": cid,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "pose": pose,
        "pose_note": pose_note,
        "n_models": len(poses),
    }


def plot_projection(
    ax,
    lig_xyz: np.ndarray,
    pocket_xyz: np.ndarray,
    feat_cents: dict[str, list[float]],
    feat_colors: dict[str, str],
    region_xyz: dict[str, np.ndarray],
    dims: tuple[int, int],
    title: str,
):
    i, j = dims
    if len(pocket_xyz):
        ax.scatter(pocket_xyz[:, i], pocket_xyz[:, j], s=6, c="#94a3b8", alpha=0.35, zorder=1)
    ax.scatter(lig_xyz[:, i], lig_xyz[:, j], s=28, c="#0f172a", alpha=0.9, zorder=3, edgecolors="white", linewidths=0.3)
    for name, xyz in region_xyz.items():
        ax.scatter(xyz[i], xyz[j], s=90, marker="s", facecolors="none", edgecolors="#e11d48", linewidths=1.4, zorder=4)
        ax.annotate(name, (xyz[i], xyz[j]), textcoords="offset points", xytext=(4, 4), fontsize=7, color="#be123c")
    for fname, c in feat_cents.items():
        if fname not in feat_colors:
            continue
        col = feat_colors[fname]
        ax.scatter(c[i], c[j], s=120, c=col, marker="o", zorder=5, edgecolors="white", linewidths=0.8)
        ax.annotate(fname, (c[i], c[j]), textcoords="offset points", xytext=(5, -8), fontsize=7, color=col, fontweight="bold")
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("xyz"[i].upper() + " (Å)")
    ax.set_ylabel("xyz"[j].upper() + " (Å)")
    ax.grid(True, alpha=0.25)


def write_png_pair(entry: dict, rec: list[dict], feat_cents: dict, feat_colors: dict, out_stem: Path):
    pose = entry["pose"]
    lig_heavy = np.vstack([a["xyz"] for a in pose["atoms"] if a["heavy"]])
    cent = ligand_heavy_centroid(pose["atoms"])
    pocket = pocket_rec_atoms(rec, cent, 11.0)
    pocket_xyz = np.vstack([a["xyz"] for a in pocket]) if pocket else np.zeros((0, 3))

    # residue centroid for highlight set
    region_xyz = {}
    for rk in HIGHLIGHT_RES:
        rats = [a["xyz"] for a in rec if a["heavy"] and residue_key(a) == rk]
        if rats:
            region_xyz[rk] = np.mean(np.vstack(rats), axis=0)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.2), dpi=140)
    plot_projection(
        axes[0], lig_heavy, pocket_xyz, feat_cents, feat_colors, region_xyz, (0, 2),
        f"{entry['label']} MODEL 1 — XZ (Ad/het ±x vs ±z)",
    )
    plot_projection(
        axes[1], lig_heavy, pocket_xyz, feat_cents, feat_colors, region_xyz, (0, 1),
        f"{entry['label']} MODEL 1 — XY",
    )
    legend = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#0f172a", markersize=8, label="ligand heavy"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#94a3b8", markersize=6, label="pocket heavy ≤11 Å"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="none", markeredgecolor="#e11d48", markersize=8, label="region residue"),
    ]
    for fname, col in feat_colors.items():
        if fname in feat_cents:
            legend.append(Line2D([0], [0], marker="o", color="w", markerfacecolor=col, markersize=8, label=fname))
    fig.legend(handles=legend, loc="lower center", ncol=4, fontsize=8, frameon=False)
    fig.suptitle(
        f"0J visual QC | {entry['label']} | Vina REMARK {entry['pose']['vina_score']:.3f} (score-only)",
        fontsize=11,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0.08, 1, 0.95))
    png = out_stem.with_suffix(".png")
    fig.savefig(png, bbox_inches="tight")
    plt.close(fig)
    return png


def write_overlay(entries_feats: list[tuple[dict, dict, dict]], title: str, out_path: Path, dims=(0, 2)):
    fig, ax = plt.subplots(figsize=(7.2, 6.2), dpi=140)
    i, j = dims
    palette = ["#0f172a", "#2563eb", "#d97706", "#059669", "#dc2626", "#7c3aed", "#0891b2"]
    for idx, (entry, feat_cents, feat_colors) in enumerate(entries_feats):
        lig = np.vstack([a["xyz"] for a in entry["pose"]["atoms"] if a["heavy"]])
        col = palette[idx % len(palette)]
        ax.scatter(lig[:, i], lig[:, j], s=18, c=col, alpha=0.55, label=entry["label"], zorder=2)
        # mark primary orientation features
        for key in ("adamantyl", "benzoyl_aryl", "n1_heterocycle", "n1_benzyl_aryl"):
            if key in feat_cents:
                c = feat_cents[key]
                ax.scatter(c[i], c[j], s=140, c=feat_colors.get(key, col), marker="*", edgecolors="white", zorder=5)
                ax.annotate(f"{entry['label']}:{key}", (c[i], c[j]), fontsize=6.5, color=col, xytext=(4, 4), textcoords="offset points")
    # TYR25 marker
    # (caller may pass via first entry pocket — draw fixed from BOX if available)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("xyz"[i].upper() + " (Å)")
    ax.set_ylabel("xyz"[j].upper() + " (Å)")
    ax.set_title(title)
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


def write_html(entry: dict, rec: list[dict], feat_cents: dict, out_path: Path):
    pose = entry["pose"]
    cent = ligand_heavy_centroid(pose["atoms"])
    pocket = pocket_rec_atoms(rec, cent, 12.0)
    # include explicit region residues even if slightly farther
    keys = {residue_key(a) for a in pocket} | set(HIGHLIGHT_RES)
    pocket = residue_atoms(rec, keys)
    lig_pdb = atoms_to_pdb_block(pose["atoms"], resn="LIG", chain="L")
    rec_pdb = atoms_to_pdb_block(pocket, resn="REC", chain="R")
    # mark TYR25 atoms separately for stick highlight
    tyr = residue_atoms(rec, {"TYR25"})
    tyr_pdb = atoms_to_pdb_block(tyr, resn="TYR", chain="R") if tyr else ""

    spheres = []
    for fname, c in feat_cents.items():
        color = QIU_FEAT_COLORS.get(fname) or D2_FEAT_COLORS.get(fname) or "#111827"
        spheres.append(
            f'viewer.addSphere({{center:{{x:{c[0]:.3f},y:{c[1]:.3f},z:{c[2]:.3f}}}, radius:0.55, color:"{color}", alpha:0.85}});'
            f'viewer.addLabel("{html.escape(fname)}", {{position:{{x:{c[0]:.3f},y:{c[1]:.3f},z:{c[2]:.3f}}}, '
            f'backgroundColor:"white", fontColor:"{color}", fontSize:10, showBackground:true}});'
        )
    sphere_js = "\n".join(spheres)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>0J Visual QC — {html.escape(entry['label'])}</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"></script>
  <style>
    body {{ margin:0; font-family:Segoe UI, system-ui, sans-serif; background:#0b1018; color:#e5e7eb; }}
    #viewer {{ width:100vw; height:85vh; }}
    .meta {{ padding:10px 16px; font-size:13px; line-height:1.4; }}
    code {{ color:#93c5fd; }}
  </style>
</head>
<body>
  <div class="meta">
    <strong>{html.escape(entry['label'])}</strong> — MODEL {entry['pose']['model']} |
    Vina REMARK <code>{entry['pose']['vina_score']:.3f}</code> (score-only) |
    path <code>{html.escape(entry['path'])}</code><br/>
    Feature spheres = moiety centroids (observation). Red sticks = TYR25 if loaded. No H-bond rescue.
  </div>
  <div id="viewer"></div>
  <script id="lig" type="text/plain">{lig_pdb}</script>
  <script id="rec" type="text/plain">{rec_pdb}</script>
  <script id="tyr" type="text/plain">{tyr_pdb}</script>
  <script>
    const viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "0b1018"}});
    const lig = document.getElementById("lig").textContent;
    const rec = document.getElementById("rec").textContent;
    const tyr = document.getElementById("tyr").textContent;
    viewer.addModel(rec, "pdb");
    viewer.setStyle({{model:0}}, {{line:{{color:"#64748b", width:1.2}}}});
    viewer.addModel(lig, "pdb");
    viewer.setStyle({{model:1}}, {{stick:{{colorscheme:"cyanCarbon", radius:0.18}}, sphere:{{scale:0.22}}}});
    if (tyr.trim().length > 10) {{
      viewer.addModel(tyr, "pdb");
      viewer.setStyle({{model:2}}, {{stick:{{color:"#fb7185", radius:0.22}}}});
    }}
    {sphere_js}
    viewer.zoomTo({{model:1}});
    viewer.render();
  </script>
</body>
</html>
"""
    out_path.write_text(page, encoding="utf-8")
    return out_path


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rec = load_receptor_chain_r()
    lib_smiles = load_library_smiles()
    audit = json.loads((ROOT / "results" / "reports" / "qiu_0h_pose_audit_data.json").read_text(encoding="utf-8"))

    entries: dict[str, dict] = {}
    for cid in QIU_IDS:
        label = f"Qiu_{cid}"
        path = QIU_DIR / f"compound_{cid}_cb2_out.pdbqt"
        entries[label] = load_entry(label, path, "Qiu", cid)
    for did in D2_IDS:
        path = D1_DIR / f"{did}_docked.pdbqt"
        entries[did] = load_entry(did, path, "D2", did)

    artifacts = []
    metrics = {
        "methods": {
            "poses": "MODEL 1 from existing out/docked PDBQT only",
            "receptor": str(RECEPTOR.relative_to(ROOT)).replace("\\", "/"),
            "no_redocking": True,
            "viewer": "matplotlib PNG projections + 3Dmol.js HTML",
            "hbond_policy": "Do not reinterpret non geometry-OK H-bonds from 0H as present",
        },
        "compounds": {},
        "artifacts": [],
    }

    prepared = {}  # label -> (entry, feat_cents, feat_colors, axes)

    for label, entry in entries.items():
        pose = entry["pose"]
        if entry["series"] == "Qiu":
            cid = entry["compound_id"]
            smiles = pose.get("smiles") or ""
            feats = qiu_features(smiles, pose.get("smiles_idx") or {}, cid)
            # qiu_features returns dict name -> serials list (flat or nested?)
            # Normalize to name -> list[int]
            feat_serials = {}
            for k, v in feats.items():
                if not v:
                    continue
                if isinstance(v[0], (list, tuple)):
                    # take first match flattened unique
                    flat = []
                    for m in v:
                        flat.extend(list(m))
                    feat_serials[k] = sorted(set(flat))
                else:
                    feat_serials[k] = list(v)
            feat_colors = QIU_FEAT_COLORS
            orient = orientation_summary(pose, cid)
            axes = {}
            for k in ("adamantyl", "n1_heterocycle", "c5_phenyl", "n1_phenyl", "amide"):
                # orientation_summary stores vectors under "vectors" or similar — reuse centroids
                pass
        else:
            smiles = pose.get("smiles") or lib_smiles.get(label, "")
            feats = d2_features(smiles, pose.get("smiles_idx") or {})
            feat_serials = {}
            for k, v in feats.items():
                if not v:
                    continue
                if isinstance(v[0], (list, tuple)):
                    flat = []
                    for m in v:
                        flat.extend(list(m))
                    feat_serials[k] = sorted(set(flat))
                else:
                    feat_serials[k] = list(v)
            feat_colors = D2_FEAT_COLORS
            orient = None

        feat_cents = feature_centroids(pose, feat_serials)
        # core for axes
        core_key = "pyrazole" if entry["series"] == "Qiu" else "pyrrole"
        axes = {}
        if core_key in feat_cents:
            core = np.array(feat_cents[core_key])
            for fk, c in feat_cents.items():
                if fk == core_key:
                    continue
                axes[fk] = dominant_axis(core, np.array(c))

        cent = ligand_heavy_centroid(pose["atoms"]).tolist()
        all_serials = [a["serial"] for a in pose["atoms"] if a["heavy"]]
        region_d = region_min_dists(pose["atoms"], all_serials, rec)

        # TYR25 min heavy distance (observation)
        tyr_atoms = [a for a in rec if a["heavy"] and residue_key(a) == "TYR25"]
        lig_h = [a for a in pose["atoms"] if a["heavy"]]
        tyr_min = None
        if tyr_atoms and lig_h:
            dmat = np.linalg.norm(
                np.vstack([a["xyz"] for a in lig_h])[:, None, :]
                - np.vstack([a["xyz"] for a in tyr_atoms])[None, :, :],
                axis=2,
            )
            tyr_min = float(dmat.min())

        # Prefer 0H recorded region distances when available
        h0 = audit["compounds"].get(label, {})
        h0_region = h0.get("region_distances") or h0.get("region") or {}
        h0_hbonds = h0.get("hbond_geometry_ok")
        if h0_hbonds is None:
            h0_hbonds = h0.get("contacts", {}).get("hbonds_ok") if isinstance(h0.get("contacts"), dict) else None

        stem = OUT_DIR / f"{label.lower()}_model1"
        png = write_png_pair(entry, rec, feat_cents, feat_colors, stem)
        html_path = write_html(entry, rec, feat_cents, stem.with_suffix(".html"))
        artifacts.extend([png, html_path])
        prepared[label] = (entry, feat_cents, feat_colors, axes)

        metrics["compounds"][label] = {
            "path": entry["path"],
            "model": pose["model"],
            "vina_remark": pose["vina_score"],
            "pose_note": entry["pose_note"],
            "centroid": [round(x, 3) for x in cent],
            "feature_centroids": {k: [round(x, 3) for x in v] for k, v in feat_cents.items()},
            "dominant_axes_from_core": axes,
            "tyr25_min_heavy_A": round(tyr_min, 3) if tyr_min is not None else None,
            "tyr25_contact_le_4": bool(tyr_min is not None and tyr_min <= 4.0),
            "region_min_dists_A": {k: (round(float(v), 3) if v is not None else None) for k, v in region_d.items()}
            if isinstance(region_d, dict)
            else {},
            "h0_hbonds_geometry_ok": h0_hbonds if h0_hbonds is not None else 0,
            "png": str(png.relative_to(ROOT)).replace("\\", "/"),
            "html": str(html_path.relative_to(ROOT)).replace("\\", "/"),
        }

    # Overlay panels
    overlays = [
        (
            "overlay_qiu_14_20_xz.png",
            "Qiu 14 vs 20 — similar occupation (XZ)",
            ["Qiu_14", "Qiu_20"],
        ),
        (
            "overlay_qiu_14_15_20_24_xz.png",
            "Qiu 14/15/20 vs 24 — N1-het rotation (XZ)",
            ["Qiu_14", "Qiu_15", "Qiu_20", "Qiu_24"],
        ),
        (
            "overlay_d2_canonical_vs_qiu14_xz.png",
            "D2_20 / D2_06 vs Qiu 14 — canonical_like map (XZ)",
            ["Qiu_14", "JANUS_D2_20", "JANUS_D2_06"],
        ),
        (
            "overlay_d2_22_feature_swap_xz.png",
            "D2_22 vs Qiu 14 / D2_20 — feature_swap check (XZ)",
            ["Qiu_14", "JANUS_D2_20", "JANUS_D2_22"],
        ),
    ]
    for fname, title, labels in overlays:
        pack = [prepared[l][:3] for l in labels]
        # prepared values are (entry, feat_cents, feat_colors, axes)
        pack3 = [(prepared[l][0], prepared[l][1], prepared[l][2]) for l in labels]
        p = write_overlay(pack3, title, OUT_DIR / fname, dims=(0, 2))
        artifacts.append(p)

    # index HTML
    rows = []
    for label, m in metrics["compounds"].items():
        rows.append(
            f"<tr><td>{html.escape(label)}</td><td>{m['model']}</td>"
            f"<td>{m['vina_remark']:.3f}</td>"
            f"<td>{m.get('tyr25_min_heavy_A')}</td>"
            f"<td><code>{html.escape(str(m.get('dominant_axes_from_core')))}</code></td>"
            f"<td><a href='{Path(m['png']).name}'>png</a> · <a href='{Path(m['html']).name}'>html</a></td></tr>"
        )
    index = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/><title>Qiu 0J Visual QC index</title>
<style>body{{font-family:Segoe UI,sans-serif;margin:24px;}} td,th{{padding:6px 10px;border-bottom:1px solid #ddd;text-align:left;}}</style>
</head><body>
<h1>Qiu 0J — Visual QC artifacts</h1>
<p>MODEL 1 only. No redocking. Feature spheres/axes are geometric observations.</p>
<table>
<thead><tr><th>Compound</th><th>MODEL</th><th>Vina</th><th>TYR25 min Å</th><th>Axes</th><th>Files</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody></table>
<h2>Overlays</h2>
<ul>
<li><a href="overlay_qiu_14_20_xz.png">14 vs 20</a></li>
<li><a href="overlay_qiu_14_15_20_24_xz.png">14/15/20 vs 24</a></li>
<li><a href="overlay_d2_canonical_vs_qiu14_xz.png">D2 canonical vs Qiu 14</a></li>
<li><a href="overlay_d2_22_feature_swap_xz.png">D2_22 feature_swap</a></li>
</ul>
</body></html>
"""
    index_path = OUT_DIR / "index.html"
    index_path.write_text(index, encoding="utf-8")
    artifacts.append(index_path)

    metrics["artifacts"] = [str(p.relative_to(ROOT)).replace("\\", "/") for p in artifacts]
    OUT_JSON.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Wrote {len(artifacts)} artifacts under {OUT_DIR}")
    print(f"Metrics: {OUT_JSON}")
    for label, m in metrics["compounds"].items():
        print(f"  {label}: axes={m['dominant_axes_from_core']} TYR25={m['tyr25_min_heavy_A']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
