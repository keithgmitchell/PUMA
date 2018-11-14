import csv
import argparse
from collections import defaultdict

def unclassified(fix_list, classification_levels, parent_dict, repeat_dict):
    for x in range(0, classification_levels):
        thisValue = fix_list[x]
        if thisValue == '' or thisValue == 'NA' or thisValue is None or thisValue == " " or thisValue == 'unclassified':
            for y in range(x, classification_levels):
                fix_list[y] = 'unclassified'
                continue
        if x == 0 or thisValue == 'unclassified':
            continue
        parentValue = fix_list[x-1]
        if x not in parent_dict:
            parent_dict[x] = {}
        if fix_list[x] not in parent_dict[x]:
            parent_dict[x][thisValue]=parentValue
        else:
            if parent_dict[x][thisValue] != parentValue:
                if thisValue not in repeat_dict:
                    repeat_dict[thisValue] = thisValue + "__1"
                    fix_list[x] = thisValue + "__1"
                else:
                    value = repeat_dict[thisValue].split("__")[0] + "**" + str(int(repeat_dict[thisValue].split("__")[-1])+1)
                    repeat_dict[fix_list[x]] = value
                    fix_list[x] = value
    return fix_list


def reformat(rarefied, output, otu_dict, classification_count):
    csvin = open(rarefied, 'r')
    tsvout = open(output, 'w')
    csvin = csv.reader(csvin, delimiter='\t')
    tsvout = csv.writer(tsvout, delimiter='\t')

    header = next(csvin)
    header.pop(0)
    if classification_count == 7:
        new_header = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'] + header
    else:
        new_header = ['phylum', 'class', 'order', 'family', 'genus', 'species'] + header

    tsvout.writerow(new_header)
    condense_dict = {}
    parent_dict = defaultdict(dict)
    repeat_dict = {}
    for row in csvin:
        tax_list = otu_dict[row[0]].split(';')
        row.pop(0)

        #TODO should this be classification count
        while len(tax_list) < 6:
            tax_list.append(" ")
        new_tax_list = unclassified(tax_list, classification_count, parent_dict, repeat_dict)
        tax_list_key = ",".join(new_tax_list)
        if tax_list_key in condense_dict.keys():
            condense_dict[tax_list_key] = [float(x) + float(y) for x, y in zip(row, condense_dict[tax_list_key])]
        else:
            condense_dict[tax_list_key] = row
    for item in condense_dict:
        tax_list = item.split(",")
        tsvout.writerow(tax_list + condense_dict[item])


def get_key(input):
    with open(input, 'r') as input_file:
        input_csv = csv.reader(input_file, delimiter='\t')
        header = next(input_csv)
        find_tax = 0
        for item in header:
            if item == 'sum taxonomy' or item == 'sum.taxonomy':
                break
            find_tax += 1

        dict = {}
        for row in input_csv:
            dict[row[0]]=row[find_tax]
        return dict


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Normalizes a merged ASV table for number of files merged.')

    parser.add_argument('-input', help='This is the input file from ANACAPA (Ex: 16S_ASV_raw_taxonomy_70.txt)', required=True)
    parser.add_argument('-output', help='This is the name of the rarefied file ready for STAMP.', required=True)
    parser.add_argument('-rarefied', help='This is the name of the rarefied, averaged file.', required=True)



    args = vars(parser.parse_args())
    input = args['input']
    output = args['output']
    rarefied = args['rarefied']

    # first we will reformat the file for general stamp usage
    otu_key = get_key(input)
    reformat(rarefied, output, otu_key)
