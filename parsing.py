#!/usr/bin/env python
''' Author : Huy Nguyen
    Project: Parsing bacterioxin file
    Start  : 19/06/2016
    End    : 15/07/2016
'''
import os
from Bio import Entrez, SeqIO
import time
Entrez.email ="huyn@iastate.edu"
db="nucleotide" # database we want to focus on
os.chdir('/home/huyn/Nafiz_Huy/all_non_overlapping_operons')
infile = open('lc_set.txt','r')
lines = infile.readlines()
dic ={}
for line in lines:
    if line[:3]=="#GI":
        key= line.split(':')[1]
        key = key.replace(' ','')
        key = key.split('\n')[0]
        dic[key] =[]
    elif line[0]=='#':
        continue
    else:
        modify = line.split(' ')
        gene = modify[2].split('\n')[0]
        dic[key].append(gene)
        
print dic
for key in dic:
    handle = Entrez.efetch(db=db, id=key, rettype="gb", retmode="text")
    seq_record = SeqIO.read(handle, "genbank")
    handle.close()
    file= open(key,'w')
    SeqIO.write(seq_record, file, "genbank")
    file.close()
outfile = open('gene_block_names_and_genes.txt','w')
for key in dic:
    modify= key.split(',')[0]
    outfile.write(modify)
    for value in dic[key]:
        outfile.write('\t'+value)
    outfile.write('\n')
outfile.close()