# Paso 0D — Verificación estructural Qiu 2023 (compuestos 14, 15, 20, 24)

> Estricto: sin docking / PDBQT. Solo representación 2D publicada.  
> Fuente: Qiu et al., *Bioorg. Chem.* 2023, 133, 106377 — DOI [10.1016/j.bioorg.2023.106377](https://doi.org/10.1016/j.bioorg.2023.106377) (SSRN 4276225).  
> Fecha: 2026-08-11.

## Estado global

**0D = PASS 4/4**

## Recuperación de fuente

| Canal | Resultado |
|-------|-----------|
| PDF local (`Downloads` / `Desktop` / `projects` / repo) | No hallado (solo PDFs ajenos: memoria Janusforge) |
| SSRN live (`abstract_id=4276225`) | HTTP 403 (Cloudflare); Delivery.cfm PDF no descargable |
| Wayback SSRN abstract | Sí (HTML abstract); Delivery.cfm archivado como HTML login, **no PDF** |
| ScienceDirect full PDF | 403 |
| Elsevier CDN figuras (`ars.els-cdn.com` …`S0045206823000378-*`) | **Sí** — GA, fx1, gr1–gr6 |
| SI `mmc1.docx` (CDN) | **Sí** — Scheme S1 + Fig. S6 (texto) |

**Anclas inequívocas usadas:** graphical abstract (`ga1`), scaffold (`fx1`), Scheme S1 (SI `image15` / OCR), Fig. S6 SI (14/15/16 = o/m/p-morfolina).

## Anotación por compuesto (desde figura/SI)

Scaffold común (fx1 / GA / Scheme S1): **1H-pirazol-3-carboxamida** con **C4 = Me**, **C5 = Ph**, **C3 = –C(=O)NH–R³**, **N1 = fenilo–R¹**.

| Cpd | Núcleo | N1 (R¹) | C3 (carboxamida → R³) | C4 | C5 | IUPAC (reconstruido) |
|-----|--------|---------|------------------------|----|----|----------------------|
| **14** | pirazol | *o*-morfolinilo | 1-adamantilo | Me | Ph | *N*-(adamantan-1-il)-4-metil-1-(2-morfolinofenil)-5-fenil-1*H*-pirazol-3-carboxamida |
| **15** | pirazol | *m*-morfolinilo | 1-adamantilo | Me | Ph | *N*-(adamantan-1-il)-4-metil-1-(3-morfolinofenil)-5-fenil-1*H*-pirazol-3-carboxamida |
| **20** | pirazol | *o*-(4-metilpiperazin-1-ilo) | 1-adamantilo | Me | Ph | *N*-(adamantan-1-il)-4-metil-1-[2-(4-metilpiperazin-1-il)fenil]-5-fenil-1*H*-pirazol-3-carboxamida |
| **24** | pirazol | *o*-morfolinilo | CH₂–(1-adamantilo) | Me | Ph | *N*-(adamantan-1-ilmetil)-4-metil-1-(2-morfolinofenil)-5-fenil-1*H*-pirazol-3-carboxamida |

Evidencia numeración (Scheme S1 SI):  
`14: R1=Morpholinyl, R3=1-adamantyl, ortho` · `15: … meta` · `20: R1=4-Methylpiperazinyl, ortho` (serie Group I, R³=1-adamantilo implícito entre 17 y 23) · `24: R1=Morpholinyl, R3=CH2-1-adamantyl, ortho`.  
Fig. S6 SI confirma 14/15/16 = orto/meta/para-morfolina. GA muestra explícitamente **C3-carboxamida–adamantilo** (no adamantilo directo en C3).

**Corrección vs reconstrucción previa del panel QIU_14:** el lote docking anterior omitió el enlace carboxamida (C3–Ad directo). Esa estructura **no** es la publicada.

## Tabla 0D

| Compound | SMILES | InChI | Estructura verificada | Observaciones |
|----------|--------|-------|----------------------|---------------|
| 14 | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` | `InChI=1S/C31H36N4O2/c1-21-28(30(36)32-31-18-22-15-23(19-31)17-24(16-22)20-31)33-35(29(21)25-7-3-2-4-8-25)27-10-6-5-9-26(27)34-11-13-37-14-12-34/h2-10,22-24H,11-20H2,1H3,(H,32,36)` | **YES** | Yin–Yang lead; GA + Scheme S1 + Fig. S6; C₃₁H₃₆N₄O₂ |
| 15 | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2cccc(N3CCOCC3)c2)c1-c1ccccc1` | `InChI=1S/C31H36N4O2/c1-21-28(30(36)32-31-18-22-14-23(19-31)16-24(15-22)20-31)33-35(29(21)25-6-3-2-4-7-25)27-9-5-8-26(17-27)34-10-12-37-13-11-34/h2-9,17,22-24H,10-16,18-20H2,1H3,(H,32,36)` | **YES** | Regioisómero meta-morfolina; Scheme S1 + Fig. S6; C₃₁H₃₆N₄O₂ |
| 20 | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCN(C)CC2)c1-c1ccccc1` | `InChI=1S/C32H39N5O/c1-22-29(31(38)33-32-19-23-16-24(20-32)18-25(17-23)21-32)34-37(30(22)26-8-4-3-5-9-26)28-11-7-6-10-27(28)36-14-12-35(2)13-15-36/h3-11,23-25H,12-21H2,1-2H3,(H,33,38)` | **YES** | *o*-4-metilpiperazinilo; R³=1-adamantilo (Group I); Scheme S1; C₃₂H₃₉N₅O |
| 24 | `Cc1c(C(=O)NCC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` | `InChI=1S/C32H38N4O2/c1-22-29(31(37)33-21-32-18-23-15-24(19-32)17-25(16-23)20-32)34-36(30(22)26-7-3-2-4-8-26)28-10-6-5-9-27(28)35-11-13-38-14-12-35/h2-10,23-25H,11-21H2,1H3,(H,33,37)` | **YES** | Misma N1-*o*-morfolina que 14; R³ = adamantilmetilo; Scheme S1 Group II; C₃₂H₃₈N₄O₂ |

SMILES/InChI: RDKit (canónicos; forma neutra 2D publicada — sin protonación forzada). InChIKey: 14=`QQXQVTJJXRACOB-UHFFFAOYSA-N`, 15=`ZVVBFOFPAAUAGH-UHFFFAOYSA-N`, 20=`ZWCGYXUFIUXGBQ-UHFFFAOYSA-N`, 24=`RAQAMHLYXWAFRF-UHFFFAOYSA-N`.

## Artefactos locales (gitignored)

- CSV solo YES: `data/libraries/qiu_0d_structures.csv`
- Figuras/SI cache: `data/papers/` (no commit)

## Notas

- No CID PubChem / depósito ChEMBL hallado para estos cuatro.
- PDF principal Elsevier/SSRN no obtenido; verificación apoyada en CDN Elsevier (figuras + SI mmc1), suficientes para inequívoco 2D.
- Sin PDBQT / docking en este paso.
