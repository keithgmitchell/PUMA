from __future__ import division
from Bio import pairwise2, SeqIO
import csv
import argparse
import os
import math

def get_seqs(sequences_file, sequence_output, seq_key):
    output_file = open(sequence_output, 'w')
    parsed_sequences = SeqIO.parse(sequences_file, 'fasta')
    for rec in parsed_sequences:
        if rec.description in seq_key:
            output_file.write('>' + str(rec.description) + '\r\n')
            output_file.write(str(rec.seq) + '\r\n')


def refactor_asv(input_file, output_file, count):
    merged = open(input_file, 'r')
    rounded = open(output_file, 'w')

    merged_csv = csv.reader(merged, delimiter='\t')
    rounded_csv = csv.writer(rounded, delimiter='\t')

    seq_descriptions = []
    for row in merged_csv:
        if row[0] == "OTU" or row[0] == "#OTU ID":
            rounded_csv.writerow(row)
        else:
            row_list = [row[0], ]
            found_nonzero = False
            for item in row[1:len(row)]:
                averaged_int = int(float(item))
                if averaged_int != 0:
                    found_nonzero = True
                row_list.append(averaged_int)
            if found_nonzero:
                rounded_csv.writerow(row_list)
                seq_descriptions.append(row_list[0])

    return seq_descriptions

def get_seq_descriptions(split_otu_table):
    seq_descriptions = []
    split_table = open(split_otu_table, 'r')
    split_csv = csv.reader(split_table, delimiter=',')
    for row in split_csv:
        if row[0] == "OTU" or row[0] == "#OTU ID":
            continue
        else:
            seq_descriptions.append(row[0])

    return seq_descriptions


def split_otu(averaged_file, splits):
    length = sum(1 for line in open(averaged_file))
    split_size = int(length/splits)
    file_list = []
    position = 0
    for split in range(1, splits + 1):
        averaged = open(averaged_file, 'r')
        averaged_csv = csv.reader(averaged, delimiter='\t')
        averaged_cleaned = averaged_file.replace(".txt", "")

        file_split = open(averaged_cleaned + str(split) + ".csv", 'w')
        split_csv = csv.writer(file_split, delimiter=',')

        headers = next(averaged_csv)
        split_csv.writerow(headers)

        if (position + split_size) >= length:
            end = length
        else:
            end = position + split_size

        print (position, end, length, split, averaged_cleaned + str(split) + ".csv")
        # selected_rows = [row for idx, row in enumerate(averaged_csv) if idx in (position, end - 1)]
        for location, row in zip(range(0, length), averaged_csv):
            if location in range(position, end):
                split_csv.writerow(row)

        position = end
        file_list.append((averaged_cleaned + str(split) + ".csv"))

    return file_list


def handle_files(input, output, iterations, all_seqs, seq_out):
    seq_list = refactor_asv(input, output, iterations)
    get_seqs(all_seqs, seq_out, seq_list)

    size_sequence = os.path.getsize(seq_out)
    piphillin_limit = 10000000
    if float(size_sequence / piphillin_limit) >= 1:
        number_of_splits = int(math.ceil(size_sequence / piphillin_limit))
        split_files = split_otu(output, number_of_splits)

        for file, split in zip(split_files, range(1, number_of_splits + 1)):
            key = get_seq_descriptions(file)
            get_seqs(all_seqs, seq_out.replace(".fasta", "") + str(split) + ".fasta", key)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Normalizes a merged ASV table for number of files merged.')

    parser.add_argument('-input', help='This is the merged rarefaction .txt file', required=True)
    parser.add_argument('-output', help='This is the path to the output .txt file.', required=True)
    parser.add_argument('-iter', help='Number of .biom files created and merged.', required=True)
    parser.add_argument('-all_seqs', help='All the ASV sequences in one file.', required=True)
    parser.add_argument('-seq_output', help='Piphillin output sequences file', required=True)


    args = vars(parser.parse_args())
    input = args['input']
    output = args['output']
    iterations = args['iter']
    all_seqs = args['all_seqs']
    seq_out = args['seq_output']

    handle_files(input, output, iterations, all_seqs, seq_out)




