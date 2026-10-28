# Reanálisis exploratorio GSE110147: CNR1 frente a fibrosis y reparación

- Muestras: 22 IPF y 11 controles; 15 diagnósticos distintos excluidos.
- Datos: expresión RMA log2, Affymetrix GPL6244; probes asignadas con la anotación oficial y agregadas por mediana por símbolo.
- Firmas: promedio de z-scores de los genes disponibles; correlaciones Spearman exploratorias, sin ajuste.
- No hay tratamientos en esta cohorte: esto no demuestra causalidad, reparación funcional ni respuesta a CB1.

## Genes disponibles
- **fibrosis:** COL1A1, COL1A2, COL3A1, FN1, ACTA2, POSTN, SPP1, CTGF, MMP7
- **AT2_repair:** SFTPC, SFTPD, SFTPA1, SFTPA2, SFTPB, ABCA3
- **AT1_repair:** AGER, PDPN, CAV1, HOPX, AQP5
- **aberrant_epithelial:** KRT17, KRT8, KRT19, CLDN4, MMP7, KRT5

## Correlación entre CNR1 y las firmas (Spearman)

| Grupo | Firma | n | rho | p nominal |
|---|---|---:|---:|---:|
| IPF | fibrosis | 22 | 0.029 | 0.8988 |
| IPF | AT2_repair | 22 | 0.407 | 0.06004 |
| IPF | AT1_repair | 22 | 0.322 | 0.1434 |
| IPF | aberrant_epithelial | 22 | -0.374 | 0.08607 |
| Control | fibrosis | 11 | -0.091 | 0.7904 |
| Control | AT2_repair | 11 | 0.273 | 0.4171 |
| Control | AT1_repair | 11 | -0.809 | 0.002559 |
| Control | aberrant_epithelial | 11 | -0.291 | 0.3855 |
| IPF+Control | fibrosis | 33 | 0.391 | 0.0243 |
| IPF+Control | AT2_repair | 33 | -0.160 | 0.3725 |
| IPF+Control | AT1_repair | 33 | -0.336 | 0.05625 |
| IPF+Control | aberrant_epithelial | 33 | 0.051 | 0.7761 |

## Diferencia IPF menos control en las firmas

| Firma | Diferencia de mediana (z) | p nominal Mann–Whitney |
|---|---:|---:|
| fibrosis | 1.437 | 4.188e-06 |
| AT2_repair | -1.387 | 7.214e-06 |
| AT1_repair | -1.136 | 4.188e-06 |
| aberrant_epithelial | 0.984 | 0.0009552 |

## Límites

El tejido bulk mezcla células y zonas; las asociaciones con CNR1 pueden reflejar composición celular o gravedad. SFTPC/SFTPD o genes aberrantes aislados no prueban regeneración. Interpretar como priorización de hipótesis para ensayos, no como efecto de tratamiento.

Fuentes: [GSE110147](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110147); [GPL6244](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL6244).
