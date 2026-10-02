"""GPCR residue maps (UniProt / BW) for CB1 and CB2 conformational fingerprints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

# GPCRdb CNR1_HUMAN / CNR2_HUMAN TM helix spans (UniProt residue numbers).
TM_HELICES: dict[str, tuple[tuple[int, int], ...]] = {
    "cb1": (
        (90, 114),   # TM1
        (126, 149),  # TM2
        (166, 190),  # TM3
        (207, 230),  # TM4
        (252, 275),  # TM5
        (298, 322),  # TM6
        (335, 358),  # TM7
    ),
    "cb2": (
        (31, 56),    # TM1
        (67, 91),    # TM2
        (107, 132),  # TM3
        (148, 172),  # TM4
        (193, 217),  # TM5
        (239, 264),  # TM6
        (276, 300),  # TM7
    ),
}


@dataclass(frozen=True)
class MicroswitchMap:
    receptor: str
    arg350: int
    lys635: int
    trp648: int
    phe_ecl2: int
    ser739: int
    ser658: int = 0  # CB2 Ser268^6.58 (vestibular node)


MICROSWITCHS: dict[str, MicroswitchMap] = {
    "cb2": MicroswitchMap(
        receptor="cb2",
        arg350=131,
        lys635=245,
        trp648=258,
        phe_ecl2=183,
        ser739=285,
        ser658=268,
    ),
    "cb1": MicroswitchMap(
        receptor="cb1",
        arg350=214,
        lys635=343,
        trp648=356,
        phe_ecl2=268,
        ser739=383,
        ser658=0,
    ),
}


@dataclass(frozen=True)
class StructureSpec:
    pdb_id: str
    receptor: str
    chain: str | None
    source_pdb: str
    status: str  # VERIFIED | BLOCKED
    state_label: str
    ligand_resname: str | None = None
    block_reason: str = ""


STRUCTURES: tuple[StructureSpec, ...] = (
    StructureSpec(
        pdb_id="6PT0",
        receptor="cb2",
        chain="R",
        source_pdb="data/targets/cb2_multistate/6PT0_clean.pdb",
        status="VERIFIED",
        state_label="active_agonist_win_gi",
        ligand_resname="WI5",
    ),
    StructureSpec(
        pdb_id="6KPF",
        receptor="cb2",
        chain="R",
        source_pdb="data/targets/cb2_multistate/6KPF_clean.pdb",
        status="VERIFIED",
        state_label="active_agonist_cryoem",
        ligand_resname="E3R",
    ),
    StructureSpec(
        pdb_id="5ZTY",
        receptor="cb2",
        chain="A",
        source_pdb="data/targets/cb2_multistate/5ZTY_clean.pdb",
        status="VERIFIED",
        state_label="inactive_antagonist_am10257",
        ligand_resname="9JU",
    ),
    StructureSpec(
        pdb_id="8GUR",
        receptor="cb2",
        chain="R",
        source_pdb="data/targets/cb2_multistate/8GUR_clean.pdb",
        status="VERIFIED",
        state_label="active_agonist_cp55940_gi",
        ligand_resname="9GF",
    ),
    StructureSpec(
        pdb_id="5TGZ",
        receptor="cb1",
        chain="A",
        source_pdb="data/targets/cb1/5TGZ_clean.pdb",
        status="VERIFIED",
        state_label="inactive_antagonist_am6538",
        ligand_resname="ZDG",
    ),
    StructureSpec(
        pdb_id="5XRA",
        receptor="cb1",
        chain="A",
        source_pdb="data/targets/cb1/5XRA_clean.pdb",
        status="VERIFIED",
        state_label="active_agonist_am11542",
        ligand_resname="8D3",
    ),
    StructureSpec(
        pdb_id="5VEU",
        receptor="cb2",
        chain=None,
        source_pdb="",
        status="BLOCKED",
        state_label="blocked_cyp3a5",
        block_reason="PDB 5VEU is CYP3A5, not CB2 — excluded from Level-0.",
    ),
)


def tm_ca_residues(receptor: str) -> tuple[int, ...]:
    spans = TM_HELICES[receptor]
    return tuple(res for lo, hi in spans for res in range(lo, hi + 1))


def iter_verified_structures(receptor: str | None = None) -> Iterable[StructureSpec]:
    for spec in STRUCTURES:
        if spec.status != "VERIFIED":
            continue
        if receptor and spec.receptor != receptor:
            continue
        yield spec
