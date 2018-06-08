import csv
import argparse
import re

parser = argparse.ArgumentParser(description='Converts an OTU table from MR DNA format to Anacapa (16S_raw_taxonomy)')

parser.add_argument('-input', help='This is the input file from MR DNA (Ex: 112415KR515F-pr.fasta.otus.fa.OTU.percentages.txt)', required=True)
parser.add_argument('-output', help='This is the output file in Anacapa format', required=True)
args = vars(parser.parse_args())

input_file = args['input']
output_file = args['output']

with open(input_file, 'r') as input_file_reader, open(output_file, 'w') as output_file_writer:

	input_csv_reader = csv.reader(input_file_reader, delimiter='\t')
	output_csv_writer = csv.writer(output_file_writer, delimiter='\t')
	csv_header = next(input_csv_reader)

	output_csv_writer.writerow(['16S_seq_number'] + csv_header[7:len(csv_header)-1] + ['sum.taxonomy'])

	for row in input_csv_reader:
		output_csv_writer.writerow([row[0]] + row[7:len(row)-1] + ["".join(re.findall('[kpcofgs]__([^;]+;?)', row[1])[0:7])[:-1]])


