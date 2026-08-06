# Mecanismo del flip bifásico CB1 de Δ9-THCV

> Marco biofísico operativo para Track 1 (diseño THCV-like).  
> Castellano; prosa + tablas unicode (sin LaTeX).  
> Fecha: 2026-08-06.  
> Complementa: [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) · [`criterio_exito_janus.md`](criterio_exito_janus.md) · historial H1–H5: [`../results/reports/h1_h5_design_history.md`](../results/reports/h1_h5_design_history.md) · Batch 3: [`../results/reports/h1_h5_batch3_plan.md`](../results/reports/h1_h5_batch3_plan.md).

---

## Por qué este documento

Δ9-THCV es el prototipo natural Janus imperfecto: a menudo antagoniza CB1 a dosis bajas y actúa como agonista parcial de CB2, pero en CB1 puede **cambiar de signo** a alta ocupación (*flip* bifásico). Este texto fija tres ángulos —equilibrio R ⇌ R\*, cadena C3 vs C5 / toggle TM6, e implicación H1–H5— con matices críticos para no confundir **modelo mental**, **literatura funcional** y **proxy Vina**.

**Regla de lectura:** los valores de eficacia intrínseca α que aparecen abajo son **órdenes de magnitud ilustrativos** (esquemáticos), no una tabla Ki/Emax exacta extraída de un único ensayo, salvo donde se cite un paper concreto. La farmacología clásica (Pertwee, Bolognini, Thomas) establece el *patrón* bifásico; no fija un α universal 0.15–0.20.

---

## 1. Equilibrio de dos estados (R ⇌ R\*)

El receptor CB1 no es un interruptor estático encendido/apagado. Es una proteína de membrana flexible que fluctúa entre formas principales:

| Estado | Lectura operativa |
|--------|-------------------|
| **Inactivo (R)** | No emite señal intracelular útil vía acoplamiento G típico. |
| **Activo (R\*)** | Conformación que permite acoplar Gi/Go e iniciar cascada. |

Los ligandos ortostéricos desplazan ese equilibrio según **afinidad** (ocupación) y **eficacia intrínseca** α (cuánto estabilizan R\* frente a R). Un antagonista neutro puro tendría α ≈ 0; un agonista pleno, α cercano a 1 (definición relativa al sistema de ensayo).

### Por qué THCV se comporta como antagonista a dosis bajas

A concentraciones submicromolares (orden &lt; 1 µM en muchos ensayos clásicos; el umbral exacto es tejido- y sistema-dependiente), THCV:

1. Compite por el bolsillo ortostérico con endocannabinoides (anandamida, 2-AG) y agonistas sintéticos.
2. Ocupa el bolsillo con afinidad razonable → desplaza agonistas fuertes.
3. Estabiliza R\* solo de forma débil → el efecto neto celular es **freno** (antagonismo / modulación negativa), no activación clara.

Eso encaja con la síntesis de Pertwee (2008): antagonismo CB1 tejido-/ligando-dependiente *in vitro* y a dosis bajas *in vivo*, junto a agonismo parcial CB2 en varios ensayos ([Pertwee 2008](#refs); [Thomas et al. 2005](#refs)).

### Por qué hace flip a agonista parcial a dosis altas

Cuando la concentración sube (orden &gt; 1–5 µM en narrativas *in vivo*/alta ocupación; de nuevo, no un corte universal):

1. **Saturación:** THCV ocupa la mayor parte de los CB1 disponibles.
2. **Eficacia residual (α &gt; 0):** THCV no es antagonista neutro puro. Es, en la lectura operativa de janusforge, un **agonista parcial de baja eficacia** en CB1: aunque estabilice R\* solo una fracción del tiempo, a ocupación casi completa esa activación basal puede volverse detectable (fenotipos agonistas a dosis altas en la revisión clásica).

Bolognini et al. (2010) cierran el círculo útil del perfil CB2-ago + bloqueo CB1 en inflamación/dolor, sin borrar la bifasicidad CB1 ([Bolognini 2010](#refs)). McPartland (2015) recuerda que THCV ≠ rimonabant: alta afinidad *in vitro* no garantiza antagonismo CB1 central estable ([McPartland 2015](#refs)).

**Matiz crítico:** afirmar “α ≈ 0.15–0.20 para THCV” o “α ≈ 0.8–1.0 para THC” en la tabla de abajo es **esquemático** — útil para ordenar el diseño, no como Ki/Emax tabular exacta transferable entre ensayos. El claim funcional a validar en wet-lab es el *signo* y la bifasicidad, no un número α congelado.

---

## 2. Física de la cadena lateral (C3 vs C5) y el “toggle” TM6

Desde biología estructural (cristalografía / criomicroscopía; p. ej. CB1 inactivo tipo **5TGZ**, estados activos en otras estructuras como **6K43**):

| Ligando (cadena) | Lectura estructural operativa |
|------------------|-------------------------------|
| **Δ9-THC (C5, pentilo)** | La cola hidrofóbica penetra un canal lipofílico y favorece el desplazamiento de la hélice transmembrana 6 (**TM6**) hacia la apertura intracelular → acoplamiento G más fácil → agonismo fuerte. |
| **Δ9-THCV (C3, propilo)** | Dos carbonos más corta: “se queda corta” en el canal. No fuerza la apertura constante de TM6 a baja ocupación (por eso no es agonista fuerte tipo THC). Tampoco impone un bloqueo estérico rígido que impida del todo el movimiento de TM6 → el receptor conserva flexibilidad hacia R\* cuando el bolsillo se satura. |

Esa es la base del modelo mental: el flip no es “magia de dosis”, sino **ocupación alta + eficacia residual + canal alquílico incompleto**. La planta (biosíntesis C3 vs C5) explica *por qué existe* THCV; no explica *cómo limpiar* el flip — eso es química de análogos ([`quimiotipos_varinas_thcv.md`](quimiotipos_varinas_thcv.md)).

**Matiz crítico (docking):** AutoDock Vina sobre **5TGZ** estima afinidad/pose en un snapshot (típicamente inactivo). **No mide α, no mide flip, no distingue agonista de antagonista.** Un score dual mejor que THCV es un proxy de ocupación/pose, no prueba de trinquete TM3–TM6.

---

## 3. Implicación directa para diseños H1–H5

### Tabla de eficacia (esquemática)

| Compuesto | Eficacia intrínseca α (orden ilustrativo) | Efecto a dosis altas en CB1 |
|-----------|------------------------------------------|------------------------------|
| Δ9-THC | α ≈ 0.8–1.0 *(esquemático)* | Agonista fuerte (dirección anti-semilla / profibrótica en la narrativa del programa) |
| Δ9-THCV (natural) | α ≈ 0.15–0.20 *(esquemático; no Ki/Emax tabular exacta)* | Bifásico / flip a agonista parcial |
| **Candidato ideal (meta H1–H5)** | **α ≤ 0** *(meta funcional a validar en ensayo)* | Antagonista neutro (α ≈ 0) o inverso (α &lt; 0): **cero flip** en la ventana relevante |

**Matiz crítico sobre α ≤ 0:** es una **meta de ensayo funcional** (cAMP / β-arrestin / tejido, dosis-respuesta a alta ocupación), no un claim in silico. Vina no puede certificar α ≤ 0. El gate 1 de [`criterio_exito_janus.md`](criterio_exito_janus.md) (“menos evidencia de flip CB1”) sigue abierto hasta dato húmedo.

### Regla de oro de diseño

Para evitar el flip, el candidato no debe limitarse a “parecerse a THCV”. Debe incorporar una modificación que actúe como **trinquete mecánico**: volumen o geometría que choque o penalice el paso a R\* (p. ej. región entre TM3 y TM6 / canal de la cadena) cuando el receptor intente activarse — *hipótesis estructural*, no hecho demostrado para ningún análogo del panel.

### Por qué JANUS_H1_02 (1′-Me) importa — y qué no prueba

En Batch 1–2, la ramificación **1′-metilo** (**JANUS_H1_02**) fue el único PASS proxy marginal frente a THCV/THC en el gate dual Vina ([historial](../results/reports/h1_h5_design_history.md)). La lectura de diseño coherente con este mecanismo:

- El metilo añade volumen cerca del eje de la cadena lateral C3, **hipótesis** de rellenar espacio vacante y limitar fluctuación hacia R\* (trinquete TM3–TM6).
- **Lo que sí es:** mejor score dual proxy en el panel local → priorización para refino (Batch 3: [`h1_h5_batch3_plan.md`](../results/reports/h1_h5_batch3_plan.md)).
- **Lo que no es:** prueba mecanística de α, ni de ausencia de flip, ni de éxito Janus funcional.

Batch 2 enseñó además que ácidos/ésteres aromáticos hunden CB1 en Vina estático y que volumen 1′ mayor (Et/cPr) no ayudó: el refino se ancla en **1′-Me + periferia sin -COOH libre**, sin reinterpretar scores como eficacia.

### Mapa rápido H1–H5 ↔ flip

| Hipótesis | Relación con este mecanismo |
|-----------|----------------------------|
| H1 (cadena/rama, incl. 1′-Me) | Modular el canal alquílico / volumen cerca del toggle — palanca principal del trinquete *hipotético*. |
| H2 (ácido / THCVA-like) | Polaridad/periferia; no “congela” α por sí sola; Batch 2: COOH libre castiga score CB1 en 5TGZ. |
| H3 (bioisóstero resorcinol) | Puede alterar pose/H-bond y eficacia; no confundir con medida de α in silico. |
| H4 (restricción / anti-flip) | Ataque directo a la bifasicidad (congelar modo R). |
| H5 (heterociclo polar) | Separación proxy / periferia; sigue sin medir flip. |

Norte operativo del quimioma: limpiar flip + CB2 ago, fibrosis después ([`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) §4).

---

## Resumen en cinco líneas (matices críticos)

1. α de la tabla = **orden ilustrativo**, no Ki/Emax exacta; ancla literaria = Pertwee / Bolognini / Thomas, no un número universal.
2. Vina–5TGZ **no mide α ni flip**; solo afinidad/pose proxy.
3. H1_02 “prometedor” = **mejor dual proxy** + hipótesis de trinquete — no prueba mecanística.
4. Meta de candidato: **α ≤ 0** (neutro o inverso) en **ensayo funcional**, no claim computacional.
5. Diseño Track 1: volumen/geometría anti-R\* + gates de [`criterio_exito_janus.md`](criterio_exito_janus.md); Batch 3 refina 1′-Me sin publicar SMILES.

---

## Referencias {#refs}

1. Thomas A. et al. Δ9-Tetrahydrocannabivarin… competitive antagonist at CB1/CB2. *Br J Pharmacol.* 2005. PMID [16205722](https://pubmed.ncbi.nlm.nih.gov/16205722/) · https://doi.org/10.1038/sj.bjp.0706414
2. Pertwee R.G. The diverse CB1 and CB2 receptor pharmacology of three plant cannabinoids… Δ9-THCV. *Br J Pharmacol.* 2008. https://doi.org/10.1038/sj.bjp.0707442
3. Bolognini D. et al. The plant cannabinoid Δ9-THCV can decrease signs of inflammation and inflammatory pain… *Br J Pharmacol.* 2010. PMID [20590571](https://pubmed.ncbi.nlm.nih.gov/20590571/)
4. McPartland J.M. et al. Are cannabidiol and Δ9-tetrahydrocannabivarin negative modulators of the endocannabinoid system? *Br J Pharmacol.* 2015. https://doi.org/10.1111/bph.12944
5. Janusforge — criterio de éxito / gates: [`criterio_exito_janus.md`](criterio_exito_janus.md)
6. Janusforge — quimioma §4 (limitaciones THCV): [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md)
7. Janusforge — design history H1–H5 (sin SMILES): [`../results/reports/h1_h5_design_history.md`](../results/reports/h1_h5_design_history.md)
8. Janusforge — Batch 3 plan (refino 1′-Me): [`../results/reports/h1_h5_batch3_plan.md`](../results/reports/h1_h5_batch3_plan.md)

*Documento vivo: sustituir α esquemáticos por valores de ensayo propio cuando existan; no publicar SMILES de análogos.*
