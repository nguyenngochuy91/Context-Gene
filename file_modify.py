#!/usr/bin/env python
"""
Created on Wed Jul 27 16:14:25 2016
@author: huyn
@purpose: parsing operon file to get the name, convert from ncbi name into normal
gene name and format into a file to blast against clade of genomes.
"""
from Bio import SeqIO
import os
import argparse
import time
import uuid
###############################################################################
## Helper function to parse arguments, check directoring, ...
###############################################################################
# traverse and get the file
def traverseAll(path):
    res=[]
    for root,dirs,files in os.walk(path):
        for f in files:
            res.append(root+f)
    return res

# get the arguments from command line
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--InputDataDirectory","-i",help="Original operon file from Nafiz")
    parser.add_argument("--OutputDirectory","-o", help="Output of this program will be stored in the path supplied here. It will make a new directory if path given is valid or it will raise an error")
    args = parser.parse_args()
    return args
    
'''@function: Parsing the operon file, return the operon name and the NCBI protein ID
   @input   : Operon file
   @output  : oepron name, and list of NCBI protein ID
'''    
    
def parse(myfile):
    infile = open(myfile,'r')
    lines  = infile.readlines()
    genes=[]
    for line in lines:
        if line[0] == '>':
            modified= line.split('|')
            operon = modified[0]
            operon = operon.split(':')[1]
            operon = operon.split('_')[0]
            gene   = modified[1].split(':')[1]
            if gene !="no protein id":
                genes.append(gene)
    return operon,genes
'''@function: Parsing the reference gbk file, get all the CDS feature, then
              create a dictionary for key as protein id and value as gene name
   @input   : reference file
   @output  : dictionary
'''    
def create_dic_proteinID_gene(referenceFile): 
    record = SeqIO.read(referenceFile,"genbank")
    dic={}
    for feature in record.features:
        if feature.type == 'CDS':
            try:
                dic[feature.qualifiers['protein_id'][0]] =  feature.qualifiers['gene'][0]
            except:
                gene = 'unknown'
    return dic
###############################################################################
## Main function 
###############################################################################
'''@function: Go through each operon file in the target directory from Nafiz,
              write out the operon in the right format with gene name
   @input   : 
   @output  : a single file with gene_block_names_and_genes 
''' 
if __name__ == "__main__":
    start     = time.time()
    args      = get_arguments()
    directory = args.InputDataDirectory
    outfile   = args.OutputDirectory
    outfile   = open('./'+outfile,'w')
    myDic     = create_dic_proteinID_gene('reference.gbk')
    res       = traverseAll(args.InputDataDirectory)
    for r in res:
        root,f = os.path.split(r)
        if "KO" not in f:
            continue
        else:
            operon,genes = parse(r)
            for gene in genes:
                operon += '\t'+ myDic[gene]
            operon +='\n'
            outfile.write(operon)
    outfile.close()
    print (time.time() - start)
        
