import argparse, csv, gzip, json, re, statistics
from pathlib import Path
from scipy.stats import spearmanr, mannwhitneyu

PANELS = {
    'fibrosis': ['COL1A1','COL1A2','COL3A1','FN1','ACTA2','POSTN','SPP1','CTGF','MMP7'],
    'AT2_repair': ['SFTPC','SFTPD','SFTPA1','SFTPA2','SFTPB','ABCA3'],
    'AT1_repair': ['AGER','PDPN','CAV1','HOPX','AQP5'],
    'aberrant_epithelial': ['KRT17','KRT8','KRT19','CLDN4','MMP7','KRT5'],
}

def median(xs): return statistics.median(xs) if xs else float('nan')
def zscore(xs):
    m=statistics.mean(xs); sd=statistics.stdev(xs)
    return [(x-m)/sd if sd else 0.0 for x in xs]

def main(matrix_path, annot_path, outdir):
    annot={}
    with gzip.open(annot_path,'rt',encoding='utf-8',errors='replace',newline='') as f:
        header=None
        for line in f:
            if line.startswith('ID\t'):
                header=next(csv.reader([line.rstrip('\r\n')],delimiter='\t'))
                break
        for row in csv.DictReader(f,delimiter='\t',fieldnames=header):
            probe=(row.get('ID') or '').strip().strip('"')
            syms={s.strip().upper() for s in re.split(r'\s*///\s*',row.get('Gene symbol') or '') if s.strip() and s.strip()!='---'}
            if probe and syms: annot[probe]=syms
    meta={}; characteristics=[]
    with gzip.open(matrix_path,'rt',encoding='utf-8',errors='replace',newline='') as f:
        for line in f:
            if line.startswith('!Sample_characteristics_ch1'):
                row=next(csv.reader([line.rstrip('\r\n')],delimiter='\t',quotechar='"')); characteristics.append(row[1:])
            elif line.startswith('!Sample_'):
                row=next(csv.reader([line.rstrip('\r\n')],delimiter='\t',quotechar='"')); meta[row[0]]=row[1:]
            if line.startswith('!series_matrix_table_begin'): break
        reader=csv.reader(f,delimiter='\t',quotechar='"'); header=next(reader)
        ids=[x.strip('"') for x in header[1:]]; titles=[x.strip('"') for x in meta['!Sample_title']]
        diseases=['']*len(ids)
        for vals in characteristics:
            for i,val in enumerate(vals):
                v=val.strip('"')
                if v.lower().startswith('disease state:'): diseases[i]=v.split(':',1)[1].strip()
        all_samples=[]
        for i,sid in enumerate(ids):
            d=diseases[i].lower()
            group='IPF' if 'idiopathic pulmonary fibrosis' in d else ('Control' if 'normal' in d else 'Other')
            all_samples.append({'sample':sid,'title':titles[i],'disease':diseases[i],'group':group})
        keep=[i for i,s in enumerate(all_samples) if s['group'] in ('IPF','Control')]
        samples=[all_samples[i] for i in keep]
        probes={}
        for row in reader:
            if not row or row[0].startswith('!series_matrix_table_end'): break
            if len(row)<len(ids)+1: continue
            try: probes[row[0].strip('"')]=[float(x.strip('"')) for x in row[1:len(ids)+1]]
            except ValueError: continue
    gp={}
    for probe,syms in annot.items():
        if probe in probes:
            for sym in syms: gp.setdefault(sym,[]).append(probe)
    genes={sym:[median([probes[p][i] for p in plist]) for i in keep] for sym,plist in gp.items()}
    panels={}; used={}
    for name,markers in PANELS.items():
        used[name]=[g for g in markers if g in genes]
        zg={g:zscore(genes[g]) for g in used[name]}
        panels[name]=[statistics.mean(zg[g][i] for g in used[name]) for i in range(len(samples))]
    cnr=genes['CNR1']
    for i,s in enumerate(samples):
        s['CNR1_log2']=cnr[i]
        for name in PANELS: s[name+'_score']=panels[name][i]
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/'GSE110147_sample_scores.tsv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(samples[0]),delimiter='\t'); w.writeheader(); w.writerows(samples)
    summary={'dataset':'GSE110147','platform':'GPL6244','n_IPF':sum(s['group']=='IPF' for s in samples),'n_control':sum(s['group']=='Control' for s in samples),'n_other_excluded':sum(s['group']=='Other' for s in all_samples),'available_signature_genes':used,'groups':{},'correlations':{},'group_tests':{}}
    for group in ['IPF','Control']:
        ix=[i for i,s in enumerate(samples) if s['group']==group]
        summary['groups'][group]={'n':len(ix),'CNR1_median_log2':median([cnr[i] for i in ix])}
        for name in PANELS: summary['groups'][group][name+'_median_zscore']=median([panels[name][i] for i in ix])
    for group in ['IPF','Control','IPF+Control']:
        ix=[i for i,s in enumerate(samples) if group=='IPF+Control' or s['group']==group]
        summary['correlations'][group]={}
        for name in PANELS:
            rho,p=spearmanr([cnr[i] for i in ix],[panels[name][i] for i in ix])
            summary['correlations'][group][name]={'n':len(ix),'rho':float(rho),'p_nominal':float(p)}
    for name in PANELS:
        a=[panels[name][i] for i,s in enumerate(samples) if s['group']=='IPF']
        b=[panels[name][i] for i,s in enumerate(samples) if s['group']=='Control']
        u,p=mannwhitneyu(a,b,alternative='two-sided')
        summary['group_tests'][name]={'IPF_minus_control_median_z':median(a)-median(b),'p_nominal':float(p)}
    (outdir/'GSE110147_CNR1_repair_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    md=['# Reanálisis exploratorio GSE110147: CNR1 frente a fibrosis y reparación','',f"- Muestras: {summary['n_IPF']} IPF y {summary['n_control']} controles; {summary['n_other_excluded']} diagnósticos distintos excluidos.",'- Datos: expresión RMA log2, Affymetrix GPL6244; probes asignadas con la anotación oficial y agregadas por mediana por símbolo.','- Firmas: promedio de z-scores de los genes disponibles; correlaciones Spearman exploratorias, sin ajuste.','- No hay tratamientos en esta cohorte: esto no demuestra causalidad, reparación funcional ni respuesta a CB1.','','## Genes disponibles']
    for n,gs in used.items(): md.append(f"- **{n}:** {', '.join(gs) if gs else 'ninguno'}")
    md+=['','## Correlación entre CNR1 y las firmas (Spearman)','','| Grupo | Firma | n | rho | p nominal |','|---|---|---:|---:|---:|']
    for group,vals in summary['correlations'].items():
        for name,v in vals.items(): md.append(f"| {group} | {name} | {v['n']} | {v['rho']:.3f} | {v['p_nominal']:.4g} |")
    md+=['','## Diferencia IPF menos control en las firmas','','| Firma | Diferencia de mediana (z) | p nominal Mann–Whitney |','|---|---:|---:|']
    for name,v in summary['group_tests'].items(): md.append(f"| {name} | {v['IPF_minus_control_median_z']:.3f} | {v['p_nominal']:.4g} |")
    md+=['','## Límites','','El tejido bulk mezcla células y zonas; las asociaciones con CNR1 pueden reflejar composición celular o gravedad. SFTPC/SFTPD o genes aberrantes aislados no prueban regeneración. Interpretar como priorización de hipótesis para ensayos, no como efecto de tratamiento.','','Fuentes: [GSE110147](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE110147); [GPL6244](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GPL6244).']
    (outdir/'GSE110147_CNR1_repair_summary.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--matrix',required=True); ap.add_argument('--annotation',required=True); ap.add_argument('--outdir',required=True); a=ap.parse_args(); main(a.matrix,a.annotation,a.outdir)


