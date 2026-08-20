# STATIC_TOPOLOGICAL_BOTTLENECKS — LigACN WT (exploratory)

**Branch:** `task/static-ligacn-topology`  
**Access / run UTC:** `2026-08-20T15:34:45Z`  
**Verdict field:** `STATIC_TOPOLOGICAL_BOTTLENECKS` = **`TOPOLOGICAL_HUBS_IDENTIFIED`**  

```yaml
STATIC_GRAPH_ANALYSIS: CLOSED
CB2_MINIMAL_GI_CORE: BLOCKED_PENDING_DYNAMIC_VALIDATION
CB1_COMPARISON: BLOCKED
DOCKING: STOP
DE_NOVO_GENERATION: STOP
NEW_CHEMISTRY: STOP
TECHNICAL_SEARCH_TRAJ: NOT_STARTED_THIS_RUN; prior ENLACE_REGISTRADO only
MODO: READ_ONLY / PUBLIC_DATA_REANALYSIS
report_field: STATIC_TOPOLOGICAL_BOTTLENECKS
```

**Interpretation limit:** ONLY topological properties of the aggregated published network — **not** causal necessity for Gi, **not** dynamic minimal core, **not** a switch.

---

## 1. Exact graph definition

- **Source object:** `results/network_core/_raw_downloads/41467_2025_60003_MOESM5_ESM.xlsx` sheet `WT_degeneracy` (Supp Data 3).
- **SHA256:** `ff53ec7bf227e0d2c3e5ced9fb81e2e56e61fb5d6ec373c1e3f2c574e77c09b9`
- **Nodes:** 100 labels from matrix index/columns (residue tokens `AA:pos` or ligand `8D0:1`).
- **Edges:** directed; edge `u→v` iff cell `(u,v) > 0`. **Weight** = published **degeneracy / information-transmission** value in that cell (fractional participation of contact in shortest ligand→intracellular pathways; paper metric).
- **Edge count (weight>0, excluding diagonal):** 239.
- **Path length for weighted shortest paths:** `length = 1/weight` (higher transmission → shorter).
- **Unweighted / hop shortest paths:** each positive edge length 1 (used for path participation counts).
- **Contact substrate (SD2):** `results/network_core/_raw_downloads/41467_2025_60003_MOESM4_ESM.xlsx` sheets `Inactive structure contacts` + `Active structure contacts` — columns are residue–residue (or residue–LIG) contact IDs; used only to **verify** Source Set S membership, not to rebuild edges. (Recovered MOESM4: residue–LIG columns are in **Inactive** only.)

## 2. Real composition of S and T

### Source Set S (locked rule)

**Rule:** S = {8D0:1} ∪ {nodes u | w(8D0:1→u)>0 in WT_degeneracy AND residue number of u appears in SD2 Inactive and/or Active contact columns}. Literature pocket names probed only for AUSENTE / exclusion log; no substitution of AUSENTE residues.

**Final S:** `['8D0:1', 'SER:285', 'PHE:87']`

| Member | Status | Basis |
|--------|--------|-------|
| `8D0:1` | IN_GRAPH | Present as node 8D0:1 in Supp Data 3 WT_degeneracy; Morales-Pastor Methods: Dijkstra source = ligand CHEMBL5085420. |
| `SER:285` | IN_GRAPH_AND_CONTACT_SET | Out-neighbor of 8D0:1 with weight>0 in WT_degeneracy AND residue number appears in SD2 contact columns (Inactive and/or Active); explicit LIG contact column(s): ['Inactive structure contacts:285-LIG']. |
| `PHE:87` | IN_GRAPH_AND_CONTACT_SET | Out-neighbor of 8D0:1 with weight>0 in WT_degeneracy AND residue number appears in SD2 contact columns (Inactive and/or Active); explicit LIG contact column(s): ['Inactive structure contacts:87-LIG']. |

**AUSENTE / excluded probes (no silent drop, no substitution):**

- `TRP:258` — **AUSENTE** — Not present in WT_degeneracy node set; not substituted. SD2 LIG-contact columns (if any): ['Inactive structure contacts:258-LIG'].
- `PHE:183` — **AUSENTE** — Not present in WT_degeneracy node set; not substituted. SD2 LIG-contact columns (if any): ['Inactive structure contacts:183-LIG'].

### Sink Set T

| Matrix node | Paper residue | BW | In graph |
|-------------|---------------|----|----------|
| `ARG:131` | Arg131 | 3x50 | True |
| `ASP:240` | Asp240 | 6x30 | True |
| `SER:303` | Ser303 | 8x47 | True |
| `SER:69` | Ser69 | 2x39 | True |

### Connectivity S (ligand source) → T

Primary path source used: `8D0:1` (paper Dijkstra source). Other S members are documented orthosteric contacts, not alternate Dijkstra sources unless noted.

| Sink | Status | Hop length | # hop-shortest paths | # simple paths (cutoff) |
|------|--------|------------|----------------------|-------------------------|
| `ARG:131` | PATH_EXISTS | 8 | 2 | 2 |
| `ASP:240` | PATH_EXISTS | 8 | 1 | 1 |
| `SER:303` | PATH_EXISTS | 6 | 1 | 12 |
| `SER:69` | PATH_EXISTS | 6 | 4 | 41 |

**Sinks with a path from ligand:** 4/4.

---

## 3. Nulls and enrichment

**Null model:** Directed configuration-model style rewiring preserving in- and out-degree sequences of WT LigACN DiGraph; n_null=200; seed=20260820. Self-loops/multiedges avoided when possible.

- Observed sinks reachable: **4**; null mean reachable: **4.0** (n_null realized=200).
- Alpha (pre-registered): **0.05**.

Top nodes by observed path participation (intermediates on hop-shortest paths):

| Node | obs participation | null mean | p_part | obs ST-betweenness | p_bb |
|------|-------------------|-----------|--------|--------------------|------|
| `ALA:83` | 0.1304 | 0.008896214441837365 | 0.0199 | 0.5000 | 0.0249 |
| `PHE:87` | 0.1304 | 0.01421886402688163 | 0.0348 | 0.5000 | 0.0249 |
| `ALA:79` | 0.1087 | 0.024189187821547664 | 0.0746 | 0.4375 | 0.0498 |
| `SER:75` | 0.0870 | 0.037265578728640385 | 0.1642 | 0.3750 | 0.1244 |
| `ILE:73` | 0.0652 | 0.013064622090101308 | 0.0796 | 0.1875 | 0.0746 |
| `ASN:291` | 0.0435 | 0.004984967522989344 | 0.0547 | 0.5000 | 0.0050 |
| `ASN:295` | 0.0435 | 0.010040682558110484 | 0.0945 | 0.5000 | 0.0149 |
| `LEU:287` | 0.0435 | 0.007988540411539367 | 0.0846 | 0.5000 | 0.0100 |
| `SER:285` | 0.0435 | 0.003536227661227661 | 0.0398 | 0.5000 | 0.0100 |
| `ILE:129` | 0.0435 | 0.017259377527376687 | 0.1692 | 0.2500 | 0.1244 |
| `SER:123` | 0.0435 | 0.016033590508786263 | 0.1393 | 0.2500 | 0.0896 |
| `ALA:77` | 0.0435 | 0.010429887387304588 | 0.0995 | 0.1250 | 0.0896 |
| `ARG:242` | 0.0217 | 0.018197029679325242 | 1.0000 | 0.2500 | 0.1294 |
| `ARG:302` | 0.0217 | 0.006981343143826448 | 0.0796 | 0.2500 | 0.0348 |
| `ILE:298` | 0.0217 | 0.013438904479297917 | 1.0000 | 0.2500 | 0.0796 |
| `TYR:299` | 0.0217 | 0.021712995671348097 | 1.0000 | 0.2500 | 0.1343 |
| `LEU:125` | 0.0217 | 0.013317393926926688 | 1.0000 | 0.1250 | 0.1393 |
| `THR:127` | 0.0217 | 0.039584137642895076 | 0.8109 | 0.1250 | 1.0000 |
| `LEU:71` | 0.0217 | 0.011462678852106731 | 1.0000 | 0.0625 | 0.9950 |
| `PHE:81` | 0.0217 | 0.007131202148764468 | 0.0896 | 0.0625 | 0.0945 |

---

## 4. Mutagenesis overlap (exact)

Overlap is **not** asserted qualitatively. Below: each high-interest topology node with SD1 (MOESM3) rows at that position and whether an SD3 degeneracy sheet exists.

### `ALA:83`
- **A83V** (pos 83): coupling_profile=`NoCoup_Gi_bArr`; simulated=`not simulated`; %wt_expr=72.1045113; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.0; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `ALA:79`
- **A79V** (pos 79): coupling_profile=`NoCoup_Gi_bArr`; simulated=`not simulated`; %wt_expr=20.42946591; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.0; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `SER:75`
- **S75A** (pos 75): coupling_profile=`NoCoup_Gi_bArr`; simulated=`not simulated`; %wt_expr=29.24568785; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.0; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `ILE:73`
- **I73A** (pos 73): coupling_profile=`NoCoup_Gi_bArr`; simulated=`not simulated`; %wt_expr=43.99828785; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.0; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `SER:123`
- **S123A** (pos 123): coupling_profile=`PrefCoup_Gi`; simulated=`not simulated`; %wt_expr=30.9058352; Gi2_Emax_raw=0.583980579333333; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.901412135975628; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `ILE:129`
- **I129A** (pos 129): coupling_profile=`Coup_Gi_bArr`; simulated=`not simulated`; %wt_expr=42.41777677; Gi2_Emax_raw=0.4698269395; bArr1_Emax_raw=0.074874582; Gi2_Emax_norm=0.657084635770894; bArr1_Emax_norm=1.24176800593117
- SD3 sheet `None` present: **False**

### `LEU:287`
- **L287A** (pos 287): coupling_profile=`Coup_Gi_bArr`; simulated=`not simulated`; %wt_expr=51.15821889; Gi2_Emax_raw=1.04638928666667; bArr1_Emax_raw=0.100127372333333; Gi2_Emax_norm=1.39385305159816; bArr1_Emax_norm=1.37686500121026
- SD3 sheet `None` present: **False**

### `ASN:291`
- **N291A** (pos 291): coupling_profile=`PrefCoup_Gi`; simulated=`simulated`; %wt_expr=101.8849675; Gi2_Emax_raw=0.396139751333333; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.464022590096628; bArr1_Emax_norm=0.0
- SD3 sheet `291_degeneracy` present: **True**

### `ASN:295`
- **N295A** (pos 295): coupling_profile=`NoCoup_Gi_bArr`; simulated=`not simulated`; %wt_expr=77.92948329; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.0; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `ALA:77`
- **A77V** (pos 77): coupling_profile=`PrefCoup_Gi`; simulated=`simulated`; %wt_expr=95.95876446; Gi2_Emax_raw=0.328452202333333; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.388023467638858; bArr1_Emax_norm=0.0
- SD3 sheet `77_degeneracy` present: **True**

### `LEU:125`
- **L125A** (pos 125): coupling_profile=`PrefCoup_Gi`; simulated=`simulated`; %wt_expr=73.10944835; Gi2_Emax_raw=1.02535195566667; bArr1_Emax_raw=0.0; Gi2_Emax_norm=1.26646257635446; bArr1_Emax_norm=0.0
- SD3 sheet `125_degeneracy` present: **True**

### `THR:127`
- **T127A** (pos 127): coupling_profile=`Coup_Gi_bArr`; simulated=`not simulated`; %wt_expr=150.1227541; Gi2_Emax_raw=1.10268199233333; bArr1_Emax_raw=0.227465932666667; Gi2_Emax_norm=1.23421595132239; bArr1_Emax_norm=1.06591800025802
- SD3 sheet `None` present: **False**

### `ARG:302`
- **R302A** (pos 302): coupling_profile=`PrefCoup_Gi`; simulated=`simulated`; %wt_expr=85.16676041; Gi2_Emax_raw=1.08423460433333; bArr1_Emax_raw=0.0; Gi2_Emax_norm=1.30452320622957; bArr1_Emax_norm=0.0
- SD3 sheet `302_degeneracy` present: **True**

### `PHE:87`
- **F87A** (pos 87): coupling_profile=`Coup_Gi_bArr`; simulated=`not simulated`; %wt_expr=77.15715749; Gi2_Emax_raw=1.11135225233333; bArr1_Emax_raw=0.194198912; Gi2_Emax_norm=1.3595179823372; bArr1_Emax_norm=1.77061659478227
- SD3 sheet `None` present: **False**

### `SER:285`
- **S285A** (pos 285): coupling_profile=`PrefCoup_Gi`; simulated=`simulated`; %wt_expr=76.74044807; Gi2_Emax_raw=0.851790526333333; bArr1_Emax_raw=0.0; Gi2_Emax_norm=1.04298578720081; bArr1_Emax_norm=0.0
- SD3 sheet `285_degeneracy` present: **True**

### `ILE:298`
- SD1: no mutant row at this position ().
- SD3 sheet `None` present: **False**

### `ARG:242`
- **R242A** (pos 242): coupling_profile=`Coup_Gi_bArr`; simulated=`not simulated`; %wt_expr=115.5916098; Gi2_Emax_raw=1.09643153066667; bArr1_Emax_raw=0.208756001666667; Gi2_Emax_norm=1.26324631922761; bArr1_Emax_norm=1.27047643930398
- SD3 sheet `None` present: **False**

### `TYR:299`
- **Y299A** (pos 299): coupling_profile=`NoCoup_Gi_bArr`; simulated=`not simulated`; %wt_expr=11.89642571; Gi2_Emax_raw=0.0; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.0; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

### `PHE:81`
- **F81A** (pos 81): coupling_profile=`Coup_Gi_bArr`; simulated=`not simulated`; %wt_expr=146.8209857; Gi2_Emax_raw=0.863705064333333; bArr1_Emax_raw=0.099715803; Gi2_Emax_norm=0.968868925712107; bArr1_Emax_norm=0.477782031747548
- SD3 sheet `None` present: **False**

### `LEU:71`
- **L71A** (pos 71): coupling_profile=`PrefCoup_Gi`; simulated=`not simulated`; %wt_expr=22.32105244; Gi2_Emax_raw=0.515802910333333; bArr1_Emax_raw=0.0; Gi2_Emax_norm=0.902164111495961; bArr1_Emax_norm=0.0
- SD3 sheet `None` present: **False**

---

## 5. Topological summary (non-causal)

- **Hubs (enriched):** ['ALA:83', 'ALA:79', 'ASN:291', 'ASN:295', 'LEU:287', 'ARG:302']
- **High path-participation intermediates (descriptive top):** ['ALA:83', 'ALA:79', 'SER:75', 'ILE:73', 'SER:123', 'ILE:129', 'LEU:287', 'ASN:291', 'ASN:295', 'ALA:77', 'LEU:125', 'THR:127', 'ILE:298']
- **Verdict rationale:** 6 non-S/T node(s) enriched vs degree-preserving null (alpha=0.05) on S→T shortest-path participation and/or betweenness.
- **Tag:** [INTERNAL_REANALYSIS]
- **Limit:** Describes topological properties of the aggregated published LigACN only. Does NOT establish residues as causally necessary for Gi. Dynamic causal core remains BLOCKED_PENDING_DYNAMIC_VALIDATION.

## 6. Trajectories / MSM (one-liner status)

Trajectories/MSM: **not recovered this run** — GPCRmd/1540 and Box `jzooa0o27z1w9ha0h6va3i51ir7l38j4` remain ENLACE_REGISTRADO only (no new multi-cycle hunt).

## 7. Future work (not now)

When trajectories exist: compare dynamic communication network vs this static map (do static bottlenecks survive dynamically?). Dynamic causal core remains `BLOCKED_PENDING_DYNAMIC_VALIDATION`.

**STOP.** No docking. No de novo. Human review next.
