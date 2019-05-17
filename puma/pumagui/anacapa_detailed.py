import csv
import argparse
# function to reverse complement a nucleotide sequence
def reverseComplement(forward_seq):
    nucleotide_dictionary = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join([nucleotide_dictionary[base] for base in reversed(forward_seq)])
def truncate_taxonomy(full_taxonomy, confidences, cutoff):
# the taxonomy and confidences may have an extra semicolon at the end
    full_taxonomy = full_taxonomy.rstrip(';')
    confidences = confidences.rstrip(';')
    taxonomy = dict([level.split(':', 1) for level in full_taxonomy.split(';')])
    truncated_taxonomy = {}
    for level_info in confidences.split(';'):
        level_name, confidence_value = level_info.split(':')
        if float(confidence_value) >= cutoff:
            truncated_taxonomy[level_name] = taxonomy[level_name]
    return truncated_taxonomy


parser = argparse.ArgumentParser(description='Creates sequence FASTA files from an Anacapa taxonomy detailed file')
parser.add_argument('-input', help='This is the input 16S_ASV_taxonomy_detailed from the Anacapa pipeline', required=True)
parser.add_argument('-forward', help='This is the output forward reads FASTA file', required=True)
parser.add_argument('-merged', help='This is the output merged reads FASTA file', required=True)
parser.add_argument('-reverse', help='This is the output reverse reads FASTA file, which are reverse complemented', required=True)
parser.add_argument('-otutable', help='This is the output OTU table in Anacapa format', required = True)
parser.add_argument('-confidence', help='This is the confidence level in percent (0-100) that the Anacapa taxonomy will be collapsed to. Default is 70%', required = False, default=70)
args = vars(parser.parse_args())
taxonomy_detailed = args['input']
taxonomy_raw = args['otutable']
forward_seq_file = args['forward']
merged_seq_file = args['merged']
reverse_seq_file = args['reverse']
cutoff = args['confidence']
with open(forward_seq_file, mode="w", newline="\n", encoding="utf-8") as f, open(merged_seq_file, mode="w", newline="\n", encoding="utf-8") as m, open(reverse_seq_file, mode="w", newline="\n", encoding="utf-8") as r, open(taxonomy_detailed, 'r') as taxonomy_table, open(taxonomy_raw, 'w', newline="\n", encoding="utf-8") as otu_out_file:
    reader = csv.reader(taxonomy_table, delimiter='\t')
    otu_out_writer = csv.writer(otu_out_file, delimiter='\t')
    csv_header = next(reader)
    startIndex = csv_header.index('forward_16S_seq_number') + 1
    endIndex = csv_header.index('merged_16S_seq_number')
    taxonomyIndex = csv_header.index('taxonomy')
    taxonomyConfidenceIndex = csv_header.index('taxonomy_confidence')
    otu_out_writer.writerow(["16S_seq_number"] + csv_header[startIndex:endIndex] + ["sum.taxonomy"])
    output_levels = ["superkingdom","phylum", "class", "order", "family", "genus", "species"]
    for row in reader:
        if row[0][0] == "f":
            f.write(">%s\n%s\n" % (row[0],row[1]))
        elif row[0][0] == "m":
            m.write(">%s\n%s\n" % (row[0],row[1]))
        else:
            r.write(">%s\n%s\n" % (row[0],reverseComplement(row[1])))
        if ':' in row[taxonomyIndex]:
            taxonomy_truncated = truncate_taxonomy(row[taxonomyIndex], row[taxonomyConfidenceIndex], cutoff)
            taxonomy_output= [taxonomy_truncated.get(level, '') for level in output_levels]
        else:
            taxonomy_output = ''
        taxonomy_output_str = ';'.join(taxonomy_output)
        otu_out_writer.writerow([row[0]] + row[startIndex:endIndex] + [taxonomy_output_str])