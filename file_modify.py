#!/usr/bin/env python
"""
Created on Wed Jul 27 16:14:25 2016
@author: huyn
@purpose: parsing operon file to get the name, convert from ncbi name into normal
gene name and format into a file to blast against clade of genomes.
"""
# from Bio import Entrez, SeqIO
import os
import argparse
import time
import uuid
db = 'gene'
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
    
# parsing Nafiz file to get the info
def parse(myfile):
    infile = open(myfile,'r')
    lines  = infile.readlines()
    genes=''
    for line in lines:
        if line[0] == '>':
            modified= line.split('|')
            operon = modified[0]
            operon = operon.split(':')[1]
            operon = operon.split('_')[0]
            gene   = modified[1].split(':')[1]
            if gene !="no protein id":
                genes+=gene+'\t'
    mystring = operon+'\t'+genes+'\n'
    return mystring
    # return operon,genes
###############################################################################
## Main function 
###############################################################################
'''@function: Go through each operon file in the target directory from Nafiz,
              write out the operon in the right format with gene name
   @input   : 
   @output  : a single file with gene_block_names_and_genes 
''' 
if __name__ == "__main__":
    start = time.time()
    args = get_arguments()
    directory = args.InputDataDirectory
    outfile   = args.OutputDirectory
    outfile=open('./'+outfile,'w')
    res = traverseAll(args.InputDataDirectory)
    for r in res:
        root,f = os.path.split(r)
        if "KO" not in f:
            continue
        else:
            mystring = parse(r)
            outfile.write(mystring)
    outfile.close()
    print (time.time() - start)
        