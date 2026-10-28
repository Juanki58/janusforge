import argparse, csv, gzip, os, re, tarfile
from scipy.io import mmread

MAC_MARKERS = ['LST1','FCER1G','TYROBP','C1QA','C1QB','C1QC','CTSS','AIF1','SPI1','MARCO','FABP4','INHBA','SPP1','MERTK']
FIB_MARKERS = ['COL1A1','COL1A2','COL3A1','DCN','LUM','PDGFRA','COL6A1']
TARGETS = ['CNR1','CNR2','NOS2','SPP1','MERTK','FABP4','INHBA']

def analyze(tar_path, output_path):
    rows=[]
    with tarfile.open(tar_path) as tf:
        members=tf.getmembers()
        for i in range(0,len(members),3):
            barcode_file,gene_file,matrix_file=members[i:i+3]
            stem=barcode_file.name.rsplit('_barcodes.tsv.gz',1)[0]
            sample=re.match(r'(GSM\d+)',stem).group(1)
            label=stem.split('_',1)[1]
            if 'bal' in label.lower():
                continue
            genes=[line.split('\t')[-1] for line in gzip.decompress(tf.extractfile(gene_file).read()).decode().splitlines()]
            with gzip.GzipFile(fileobj=tf.extractfile(matrix_file)) as stream:
                matrix=mmread(stream).tocsr()
            gene_index={gene:i for i,gene in enumerate(genes)}
            detected_genes=matrix.getnnz(axis=0)
            valid=(detected_genes>=200)&(detected_genes<=6000)
            def marker_mask(markers):
                ix=[gene_index[g] for g in markers if g in gene_index]
                return matrix[ix,:].getnnz(axis=0)>=3 if ix else [False]*matrix.shape[1]
            macrophage=marker_mask(MAC_MARKERS)&valid
            fibroblast=marker_mask(FIB_MARKERS)&valid&(~macrophage)
            spp1=(matrix[gene_index['SPP1'],:].toarray().ravel()>0)&macrophage
            fabp4=(matrix[gene_index['FABP4'],:].toarray().ravel()>0)&macrophage
            groups={'mac':macrophage,'SPP1pos':spp1,'FABP4pos':fabp4,'SPP1_FABP4_double':spp1&fabp4,'fibro':fibroblast}
            row={'sample':sample,'label':label,'valid_cells':int(valid.sum())}
            for name,mask in groups.items():
                row[name+'_n']=int(mask.sum())
                for gene in ['CNR1','CNR2','NOS2']:
                    row[name+'_'+gene]=int(matrix[gene_index[gene],mask].getnnz()) if gene in gene_index else 0
            for gene in TARGETS:
                row['mac_'+gene]=int(matrix[gene_index[gene],macrophage].getnnz()) if gene in gene_index else 0
            rows.append(row)
            print(sample,label,'valid',row['valid_cells'],'macrophage marker+',row['mac_n'])
    with open(output_path,'w',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]),delimiter='\t')
        writer.writeheader(); writer.writerows(rows)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Reproduce the marker-based GSE128033 CNR1/CNR2 screen.')
    parser.add_argument('geo_tar',help='Path to GSE128033_RAW.tar from NCBI GEO')
    parser.add_argument('output_tsv',help='Output table path')
    args=parser.parse_args(); analyze(args.geo_tar,args.output_tsv)
