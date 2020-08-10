import os

gff = 'genes.gff3'
out = 'genes_shortList.bb'

colors = ['44,160,44','31,119,180','255,127,14','214,39,40','31,119,180']
biotype2color = {}

with open(out, 'w') as f:
	for line in open(gff):
		tab = line.strip().split('\t')
		if len(tab) < 8:
			continue
		desc = tab[8]
		extra = desc
		if tab[2] == 'gene':
			if 'old_locus_tag=' in desc:
				xid = desc.split('old_locus_tag=')[1].strip()
			else:
				xid = desc.split('ID=')[1].split(';')[0]
			if xid.startswith('gene-SSO_RS'):
				continue
			biotype = 'protein_coding'
			if 'gene_biotype=' in desc:
				biotype = desc.split('gene_biotype=')[1].split(';')[0]
			if biotype in biotype2color:
				col = biotype2color[biotype]
			else:
				col = colors.pop()
				biotype2color[biotype] = col

			print(tab[0], tab[3], tab[4], xid, 1000, tab[6], tab[3], tab[4], col, extra, sep='\t', file=f)


os.system('sort -k1,1 -k2,2n %s > tmp2' % out)
#os.system('echo "track name=Genes type=bedDetail" > tmp1')
#os.system('cat tmp1 tmp2 > tmp3')
os.system('bedToBigBed -as=genes.as -extraIndex=name -type=bed9+1 -tab tmp2 chrom.sizes %s' % out)
os.system('rm tmp2')
