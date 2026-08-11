# Mapa de ligandos CB1-antagonista / CB2-agonista (precedentes Janus)

> Auditoría literario-farmacológica aportada por el usuario (2026-08-10).  
> Idioma: castellano. **Sin inventar números faltantes.**  
> Complementa: [`literatura_prioridad_y_novelty.md`](literatura_prioridad_y_novelty.md) · [`literatura_fibrosis_cb1_cb2.md`](literatura_fibrosis_cb1_cb2.md) · [`mecanismo_flip_thcv_cb1.md`](mecanismo_flip_thcv_cb1.md) · [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md) · Batch D1: [`../results/reports/option_d_batch_d1_gate_summary.md`](../results/reports/option_d_batch_d1_gate_summary.md).

**Nota operativa janusforge.** **JANUS_D2_22** es el lead de docking Opción D / Batch D1 (dual Vina = −11.277). MD membrana POPC 20 ns **completo** (`EXIT_CODE=0`) — ver [`../results/reports/md_d2_22_20ns_summary.md`](../results/reports/md_d2_22_20ns_summary.md): no-go de trinquete demostrado / go exploratorio débil; no overclaim de función Janus ni antifibrosis.

---

## 1. Tabla resumen

| Ligando | Andamiaje / rasgos estructurales | CB2 | CB1 | ¿Supera umbral ≈ −11 kcal/mol (Kd ≈ 8.5 nM)?* | Fibrosis específica |
|---------|----------------------------------|-----|-----|-----------------------------------------------|---------------------|
| **URB447** | Pirrol 1,4,5-trisustituido; 4-amino, *p*-Cl-bencil, dos fenilos | IC₅₀ ≈ 41 nM (unión hCB2) | IC₅₀ ≈ 313 nM; antagonista neutro | **No** si se compara 41 nM directamente con el umbral | No se encontró ensayo antifibrótico directo |
| **GW405833 / L-768,242** | Indol N-acilado; 2,3-diclorobenzoyl + 5-metoxi + 2-morfolinoetilo | Kᵢ humano ≈ 4–12 nM; agonista parcial | Kᵢ humano ≈ 1.9–4.8 µM; antagonismo funcional complejo | **Sí / frontera:** 4 nM ≈ −11.4 kcal/mol; 12 nM ≈ −10.8 | No se encontró modelo de fibrosis específico con este ligando |
| **AM1710** | Cannabilactona / benzo[*c*]cromen-6-ona; 1-hidroxi-9-metoxi + cadena alquilo ramificada | Kᵢ ≈ 6.7 nM (hCB2); EC₅₀ ≈ 11 nM en un ensayo | Kᵢ ≈ 360 nM; antagonista/inverso de baja potencia | **Sí**, por Kᵢ 6.7 nM ≈ −11.2 kcal/mol | No se encontró ensayo antifibrótico directo |
| **Compuesto 14** (Qiu et al. 2023) | Pirazol; N1-(2-morfolinofenilo), C3-adamantilo; C5-fenilo / C4-metilo | Agonista CB2 | Antagonista CB1 | **No clasificable con rigor** sin el valor cuantitativo de la tabla experimental; el texto accesible confirma bifuncionalidad | No se encontró ensayo antifibrótico directo |

\*A 298 K, ΔG = RT ln Kd; **−11.0 kcal/mol ≈ Kd ≈ 8.5 nM**.

### Matiz obligatorio — no comparar mecánicamente docking ΔG con IC₅₀/Kᵢ

El umbral −11 kcal/mol del cribado janusforge es un **proxy de docking (Vina)** en un panel fijo (CB1 5TGZ / CB2 6PT0). IC₅₀ y Kᵢ son magnitudes **experimentales** (ensayo, radioligando, temperatura, condiciones). Convertir nM ↔ kcal/mol sirve solo como **lectura de orden de magnitud** frente al corte interno; **no** equivale a afirmar que un score Vina “es” una Kᵢ ni a rankear ligandos publicados contra D2_22 por ese puente.

---

## 2. Conversión ΔG ↔ nM (298 K)

Relación de equilibrio aproximada:

\[
\Delta G = RT \ln K_d
\]

con \(R \approx 1.987 \times 10^{-3}\) kcal·mol⁻¹·K⁻¹ y \(T = 298\) K. De ahí:

| ΔG (kcal/mol) | Kd aproximada |
|---------------|---------------|
| −11.0 | ≈ **8.5 nM** |
| −11.2 | ≈ **6.7 nM** (coincide con Kᵢ CB2 de AM1710 citada abajo) |
| −11.4 | ≈ **4 nM** (borde inferior del rango GW405833) |
| −10.8 | ≈ **12 nM** (borde superior del rango GW405833) |

**Aplicación al mapa (solo afinidad CB2 publicada, no docking):**

- **AM1710:** 6.7 nM → pasa el corte energético aproximado.
- **GW405833:** 4–12 nM → justo alrededor del corte (4 nM lo supera; 12 nM queda ligeramente por debajo).
- **URB447:** 41 nM → no pasa por este criterio.
- **Compuesto 14:** pendiente hasta recuperar los valores experimentales de la tabla original (Qiu 2023).

**Observación para janusforge:** que URB447 sea el precedente *conceptual* no implica que sea el de mayor afinidad CB2. AM1710 y GW405833 tienen mejor afinidad CB2 experimental; su antagonismo CB1 es, en cambio, **menos limpio** que el de URB447 (neutro / GTPγS).

---

## 3. Fichas por ligando

### 3.1. URB447

URB447 fue el primer ejemplo explícitamente descrito como híbrido **CB1-antagonista / CB2-agonista**. Andamiaje: **pirrol**. Valores publicados: IC₅₀ ≈ **313 nM** (CB1) y ≈ **41 nM** (CB2); el ensayo funcional de GTPγS lo caracterizó como **antagonista neutro** en CB1. Acción periférica (metabólica) en el paper fundacional; no sustituye validación antifibrótica.

Fuente ancla: LoVerme et al., *Bioorg Med Chem Lett.* 2009; https://doi.org/10.1016/j.bmcl.2008.12.059

### 3.2. GW405833 / L-768,242

Estructuralmente muy distinto: **indol N-acilado** con grupo morfolinoetilo. Literatura CB2: Kᵢ ≈ **4–12 nM** (hCB2) y ≈ **1.9–4.8 µM** (hCB1). El trabajo de 2017 demostró que, además de agonista CB2, antagoniza señalización CB1 de forma **predominantemente no competitiva** y dependiente del ensayo — bifuncionalidad aparente ≠ mecanismo URB447.

Fuente ancla: Dhopeshwarkar et al., *JPET* 2017; https://doi.org/10.1124/jpet.116.236539

### 3.3. AM1710

Aún más distante de URB447: familia **cannabilactonas**. Kᵢ ≈ **6.7 nM** (CB2) frente a ≈ **360 nM** (CB1); posteriormente se confirmó actividad antagonista/inversa de **baja potencia** en CB1. Es el precedente que más claramente **desafía el corte energético** interno (~ −11 kcal/mol) por afinidad CB2 experimental.

### 3.4. Compuesto 14 (Qiu et al. 2023)

Especialmente relevante para el **eje Qiu activo** (post descarte D2_22): diseño deliberado de un ligando **Yin–Yang** con núcleo **pirazol**. El compuesto 14 (orto-morfolina en el brazo N1 + adamantilo en C3) presenta simultáneamente antagonismo CB1 y agonismo CB2. Proponen que la bifuncionalidad deriva de interacciones del grupo morfolino con **S173 (CB1)** y **S285 (CB2)**. Valores numéricos de Kᵢ/IC₅₀ de la tabla experimental: **no recuperados aquí** — no se inventan.

**SMILES / depósito:** sin CID PubChem ni documento ChEMBL fiable en la recuperación 2026-08-11. Panel local usa reconstrucción desde descriptores publicados (`QIU_14`, gitignored). Gate docking: [`../results/reports/qiu_pyrazole_batch1_gate_summary.md`](../results/reports/qiu_pyrazole_batch1_gate_summary.md).

Fuente ancla: Qiu et al., *Bioorg Chem.* 2023; https://doi.org/10.1016/j.bioorg.2023.106377

---

## 4. Fibrosis: racional sólido, Janus monomolecular no demostrado (estos 4)

La literatura establece bien el racional farmacológico: **CB1 favorece fibrogénesis**; **CB2 tiene efectos antifibróticos**.

- **Hígado:** bloqueo CB1 (p. ej. rimonabant en modelos) y activación CB2 se asocian a reducción de fibrosis (brazos separados).
- **Riñón:** CB1 y CB2 ejercen efectos opuestos; la **combinación** AM6545 (antagonista CB1) + AM1241 (agonista CB2) produjo efectos antifibróticos **superiores** a cada intervención individual en diabetes experimental.

Eso **no** equivale a un único ligando Janus.

En la búsqueda dirigida de esta auditoría **no** se encontró evidencia de que URB447, GW405833, AM1710 o el compuesto 14 hayan sido probados como moléculas bifuncionales **únicas** en un modelo *in vivo* de fibrosis hepática, renal o pulmonar. Qiu 2023 plantea que los Yin–Yang ligands *podrían* sustituir la combinación CB1-ant + CB2-ago en indicaciones como lesión hepática crónica — como **potencial terapéutico**, no como demostración antifibrótica del compuesto 14.

Contraste metodológico: muchos estudios prueban cada brazo por separado o una **combo de dos fármacos**. Actividad antifibrótica de otros CB1-ant o CB2-ago **no Janus** no debe contaminar el mapa de precedentes estructurales de esta clase.

---

## 5. Lectura para Batch D1 / janusforge (5 puntos)

1. El espacio de precedentes directos es **pequeño**: cuatro familias/ligandos claramente documentados.
2. **URB447** es el precedente estructural más cercano a la referencia actual de Opción D: bifuncional genuino (no solo CB2-ago con CB1 secundaria). Su **pirrol**, sin embargo, es bastante distinto del **pirazol** de Qiu et al.
3. El **compuesto 14 (2023)** es el precedente más importante para comparación **farmacofórica**: primer caso de diseño racional del perfil CB1-ant/CB2-ago con pirazol + orto-morfolina + adamantilo.
4. **AM1710** es el precedente que más claramente desafía el corte energético de CB2: Kᵢ 6.7 nM ≈ −11.2 kcal/mol.
5. El **hueco antifibrótico** parece real: fundamento biológico sólido + evidencia de que bloquear CB1 *y* activar CB2 funciona (a menudo en combo), pero **no** una demostración equivalente con un único ligando Janus de estas cuatro familias.

### Panel mínimo de referencia para novelty

**URB447 / GW405833 / AM1710 / compound-14**

### Tres capas de comparación vs D1 (derivados / lead D2_22)

| Capa | Qué comparar | Por qué |
|------|--------------|---------|
| **(i) Scaffold / topología** | Pirrol (URB447) vs indol (GW) vs cannabilactona (AM1710) vs pirazol (Qiu-14) vs serie D1 | Evitar conflar “misma clase Janus” con misma química |
| **(ii) Farmacóforo CB2 (esp. S285)** | Contactos / rasgos tipo morfolina–S285 (hipótesis Qiu) | Ancla estructural CB2 del diseño Yin–Yang |
| **(iii) Elementos de estado inactivo CB1** vs activo CB2 | Rasgos que estabilizan antagonismo CB1 limpio (tipo URB447) frente a mecanismos CB1 “sucios” | GW405833 y AM1710 muestran que bifuncionalidad aparente ≠ mismo mecanismo CB1 |

Punto crítico: distinguir **similitud de binding pose** de **similitud de mecanismo funcional**.

### Enlace a scores Batch D1 (proxy docking, no Ki)

En el mismo run de gate ([`option_d_batch_d1_gate_summary.md`](../results/reports/option_d_batch_d1_gate_summary.md)): semilla URB447 dual = −10.695 (PASS); GW405833 dual = −10.033 (PASS); lead **JANUS_D2_22** dual = −11.277. Vina ≠ éxito Janus funcional; MD 20 ns completo — [`md_d2_22_20ns_summary.md`](../results/reports/md_d2_22_20ns_summary.md).

---

## 6. Fuentes ancla (no exhaustivo)

1. LoVerme J. et al. URB447. *Bioorg Med Chem Lett.* 2009. https://doi.org/10.1016/j.bmcl.2008.12.059  
2. Dhopeshwarkar A. et al. Two Janus cannabinoids (GW405833, AM1710). *JPET* 2017. https://doi.org/10.1124/jpet.116.236539  
3. Qiu et al. Yin–Yang pyrazole design (compuesto 14). *Bioorg Chem.* 2023. https://doi.org/10.1016/j.bioorg.2023.106377  
4. Novelty / prior art del repo: [`literatura_prioridad_y_novelty.md`](literatura_prioridad_y_novelty.md)  
5. Flip CB1 / THCV: [`mecanismo_flip_thcv_cb1.md`](mecanismo_flip_thcv_cb1.md)  
6. Brújula química: [`quimioma_cannabico_cb1_cb2.md`](quimioma_cannabico_cb1_cb2.md)

**Matiz de búsqueda:** ausencia en esta auditoría ≠ inexistencia absoluta (literatura gris, tablas no recuperadas, patentes no indexadas).
