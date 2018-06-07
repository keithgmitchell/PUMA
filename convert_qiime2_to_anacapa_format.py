# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 02:47:49 2018

@author: Christopher Dao
"""

#TODO: More elegant way to handle BIOM format than to use system biom convert to tsv

import csv
import argparse
import re
import os

parser = argparse.ArgumentParser(description='Converts an OTU table and taxonomy TSV from QIIME2 format to Anacapa (16S_raw_taxonomy)')

parser.add_argument('-inputOTU', help='This is the input OTU Table file from MR DNA (Ex: table.biom)', required=True)
parser.add_argument('-inputTaxonomy', help='This is the input file from MR DNA (Ex: taxonomy.tsv)', required=True)
parser.add_argument('-output', help='This is the output file in Anacapa format', required=True)
args = vars(parser.parse_args())

input_otu_file = args['inputOTU']
input_tax_file = args['inputTaxonomy']
output_file = args['output']

os.system("biom convert -i %s -o temp_otu_table.tsv --to-tsv" % input_otu_file)

with open('/home/qiime2/Desktop/PUMA-master/temp_otu_table.tsv', 'r') as input_otu_file_reader, open(input_tax_file, 'r') as input_tax_file_reader, open(output_file, 'w') as output_file_writer:

    input_otu_csv_reader = csv.reader(input_otu_file_reader, delimiter='\t')
    input_tax_csv_reader = csv.reader(input_tax_file_reader, delimiter='\t')
    output_csv_writer = csv.writer(output_file_writer, delimiter='\t')
    next(input_otu_csv_reader)
    otu_csv_header = next(input_otu_csv_reader)
    output_csv_writer.writerow(['16S_seq_number'] + otu_csv_header[1:len(otu_csv_header)] + ['sum.taxonomy'])
    taxonomy_dict = {}
    next(input_tax_csv_reader)
    for row in input_tax_csv_reader:
        anacapa_taxonomy_fmt = "".join(re.findall('[kpcofgs]__([^;]+;?)', row[1]))
        while anacapa_taxonomy_fmt.count(";") < 6:
            anacapa_taxonomy_fmt = anacapa_taxonomy_fmt + ";"
        taxonomy_dict[row[0]]=anacapa_taxonomy_fmt
    for row in input_otu_csv_reader:
        output_csv_writer.writerow(row + [taxonomy_dict[row[0]]])
os.system("rm temp_otu_table.tsv")


