# Ficha experimental H1-a — Qiu-14 / CB2-first

> **1 página.** Extraído de 0L/0M. Spec cerrada; **wet no iniciado**.  
> **Umbrales numéricos = TBD** — no inventados aquí.

---

## Objetivo

Determinar si **Qiu-14** produce **agonismo funcional hCB2** claro vs vehículo, con control agonista CB2 de referencia.

| Si | Entonces |
|----|----------|
| **PASS** (bajo TBD-05 firmado) | Autorizar drafting **H1-b** (CB1) — spec separada |
| **KILL** | Stop Qiu-14 como ancla operativa; QC material/ensayo; pivot per 0K |

**Fuera de alcance:** H1-b, H2, H3, docking/MD, NCE, binding como sustituto de función.

---

## Artículo de ensayo

| Campo | Valor |
|-------|-------|
| Compuesto | **Qiu-14** (publicado; vehículo de validación) |
| Identidad | *o*-morfolinofenil + CONH–1-adamantilo (pirazol-3-carboxamida) |
| SMILES 0D | `Cc1c(C(=O)NC23CC4CC(CC(C4)C2)C3)nn(-c2ccccc2N2CCOCC2)c1-c1ccccc1` |
| Fuente / lote | **TBD-11** |
| Pureza / ID | **TBD-10** (HPLC, LC-MS, NMR; COA) |
| Vehículo | **TBD-08** (debe igualar control vehículo) |

Qiu-15/20/24 **no** requeridos para el gate H1-a.

---

## Controles (requeridos)

| Control | Rol | Estado |
|---------|-----|--------|
| Vehículo | Baseline | **TBD-08** |
| Agonista CB2 referencia | Control positivo / escala Emax | **TBD-08** |
| Antagonista CB2 (opcional) | Confirmar mediación CB2 | Local-C |
| Viabilidad @ conc. tope | Artefacto | Local-C |
| Z′ / CV placa | QC ensayo | **TBD-08** |

---

## Endpoint

| Elemento | Spec |
|----------|------|
| Receptor | **hCB2** (constructo/línea **TBD-01**) |
| Clase | **Funcional** agonismo CB2 |
| Formato | **TBD-02:** cAMP **o** β-arrestin **o** GTPγS (uno primario) |
| Métricas | EC₅₀ y/o Emax (o lectura pre-registrada) vs vehículo y vs ref |
| Ventana conc. / puntos curva | **TBD-07** |
| Réplicas | Local-A |

**No son endpoints:** Vina, overlap, Jaccard, H-bonds computacionales.

---

## PASS / KILL (estructura; números TBD)

| Decisión | Dirección (protocolo) | Umbral numérico |
|----------|----------------------|-----------------|
| **PASS** | Agonismo CB2 claro vs vehículo + calidad de ensayo aceptable | **TBD-05** (EC₅₀ techo y/o Emax mín. % ref y/o Δ vs vehículo) |
| **KILL** | Sin agonismo por encima de TBD-05, **o** señal no interpretable tras QC material/ensayo | Mismo TBD-05 / reglas QC |

Números de literatura Qiu (**TBD-18**), si se recuperan = **contexto only**, nunca auto-PASS salvo adopción escrita del PI.

---

## Hard-stop TBD (cerrar antes del primer wet)

| ID | Qué | Bloquea start |
|----|-----|---------------|
| **TBD-01** | Sistema celular / constructo hCB2 | **Y** |
| **TBD-02** | Formato funcional (cAMP / β-arrestin / GTPγS) | **Y** |
| **TBD-05** | Criterio numérico PASS/KILL **firmado por PI** | **Y** |
| **TBD-07** | Ventana de concentraciones + # puntos | **Y** |
| **TBD-08** | Refs, vehículo, Z′/CV | **Y** |
| **TBD-10** | Pureza/ID/COA Qiu-14 | **Y** |
| **TBD-11** | Material Qiu-14 en mano (o fecha firme) | **Y** |
| **TBD-17** | CRO vs in-house + SOP | **Y** |
| Local-A / Local-B | Réplicas; SOP análisis/placa-fail | **Y** |

Si falta alguno → **no iniciar wet** (0M = BLOCKED).
