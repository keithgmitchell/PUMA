################################################################################################################
# Code for producing hierarchial functional composition
#   ucla mimg 109bl
#   4/30/18
#   Keith Mitchell (keithgmitchell@g.ucla.edu).
#   Functions Contained: extract_info, clean_brite_file, extract_hierarchy, construct_output, list_hierarchy
################################################################################################################

import csv
import requests
import sys
import argparse
import datetime
import os
import cytoscape
from shutil import copyfile
import zipfile

def extract_info(request):

    """
        Function: extract_info
        Input 1: (request) file to be stripped for important gene to path connections
                    see link from main function for kegg api
                EX:         ko:K00001	path:map00010
                            ko:K00001	path:ko00010

        Returns:
            Object 1: (dictionary) stats_dict which has the base level counts for the sequence:
            Object 2: (dictionary)
                EX:        data_leafs = {'K00001': [ko00010, ....], ....}
                EX:        data_nodes = {'ko00010': [K00001, ....], ....}
    """

    document = request.text
    lines = document.split("\n")
    data_leafs = {}
    data_nodes = {}

    for x in range(0, len(lines)):
        if len(lines[x])>1:
            #create a matrix for the data
            data = lines[x].split("\t")

            #get rid of extra unnecessary text for the lines we care about
            gene = data[0].strip('ko:')
            path_ko = data[1].strip('path:')

            #we dont care about the map identifier, just the path identifier so dont read rows that start with m.
            if (path_ko[0] != 'm') and gene not in data_leafs.keys():
                data_leafs[gene] = [path_ko]
            elif (path_ko[0] != 'm'):
                data_leafs[gene].append(path_ko)

            if path_ko not in data_nodes.keys() and (path_ko[0] != 'm'):
                data_nodes[path_ko] = [gene]
            elif (path_ko[0] != 'm'):
                data_nodes[path_ko].append(gene)

    return data_leafs, data_nodes

def extract_gene_description(request):
    """
        Function: extract_info
        Input 1: (request) file to be stripped for important gene to path connections
                    see link from main function for kegg api
                EX:         ko:K00001	E1.1.1.1, adh; alcohol dehydrogenase [EC:1.1.1.1]
                            ko:K00002	AKR1A1, adh; alcohol dehydrogenase (NADP+) [EC:1.1.1.2]

        Returns:
            Object 1: (dictionary) stats_dict which has the base level counts for the sequence:
            Object 2: (dictionary)
                EX:        dict = {'K00001': E1.1.1.1, adh; alcohol dehydrogenase [EC:1.1.1.1]}
    """
    document = request.text
    lines = document.split("\n")
    dict = {}
    for x in range(0, len(lines)):
        if len(lines[x]) > 1:
            # create a matrix for the data
            data = lines[x].split("\t")
            data[0] = data[0].strip('ko:')
            dict[data[0]] = data[1]
    return dict

def clean_brite_file(file):

    """
       Function: cleans some of the unnecessary symbols from the brite file
       Input 1: (file) file to be stripped for important hierarchy information
                   see link from main function for brite file
       Returns: (file) ready to be stripped for the information
    """

    data = []
    for line in file:
        if len(line) > 0:

            # file clean-up
            newstr = line.replace("<b>", "")
            line_1 = newstr.replace("</b>", "")
            split_line = [line_1[0], line_1[1:len(line_1)]]
            split_line[1] = split_line[1].strip(" ")

        # for some reason I am getting an extra row with nothin in it but all data seems to be there
        #['B', ''], which is the reason for the next if statement
        if split_line[1] != '':
            data.append(split_line)
    return data



def extract_hierarchy(request):

    """
        Function: takes a dictionary (C->B or B->A) connections and extracts relevant info from the brite file
        Input 1: (request) brite hierarchy api request
        Returns:
            Object 1: (dict) B->A connections)
                EX: {'Carbohydrate metabolism': 'Metabolism', 'Energy metabolism': 'Metabolism', .....}
            Object 2: (dict) B->A connections)
                EX: {'00010 Glycolysis / Gluconeogenesis [PATH:ko00010]': 'Carbohydrate metabolism', ....}
    """

    document = request.text
    lines = document.split("\n")
    file = clean_brite_file(lines)

    levels = (['A', 'B'],['B', 'C'])
    dict_B_A = {}
    dict_C_B = {}

    for dict, key in zip([dict_B_A, dict_C_B], levels):
        parent = ''
        for pos in range(0, len(file) - 1):
            if pos >= len(file):
                return dict
            elif file[pos][0] == key[0]:
                parent = file[pos][1]
            elif file[pos][0] == key[1]:
                dict[file[pos][1]] = parent

    return dict_B_A, dict_C_B


def list_hierarchy_pw(dict_B_A, dict_C_B, pathway):

    """
        Function: returns a list of the hierarchy for a given pathway identifier
        Object 1: (dictionary) B->A connections from extract_hierarchy
        Object 2: (dictionary) C->B connections from extract hierarchy
        Returns:
            Object 1: (list) hierarchy
                EX:        Genetic Information Processing	Replication and repair	 Non-homologous end-joining [PATH:ko03450]
    """

    for key in dict_C_B:
        if key[0:5] == pathway.strip('ko'):
            try:
                #first insert the level 3 classification from the
                level_3 = key

                #then insert the level 2 classification from the C->B node dictionary
                level_2 = dict_C_B[level_3]

                #then insert the level 1 classifcation from the B->A node dictionary
                level_1 = dict_B_A[level_2]

                return [level_1, level_2, level_3[5:len(level_3)]]
            except:

                #TODO
                print ("ERROR: No hierarchy found")


    return ['','','[PATH:%s]'%(pathway)]


def construct_output(input, output, path_ko, tree_data, input_detailed):

    """
        Function: creates the final hierarchy file
        Input 1: (file) input file from piphillin (example file should be provided with code)
                 (INPUT: Gene ID, Gene Description, Sample 1, Sample 2 ....)
        Input 2: (file) for hierarchy to be written to
                 (STAMP OUTPUT: L1, L2, L3,  Sample 1, Sample 2 ....)
    """
    header_row = next(input)

    del header_row[0]
    header_row.insert(0, "Pathway L1")
    header_row.insert(1, "Pathway L2")
    header_row.insert(2, "Pathway L3")

    output.writerow(header_row)

    # here we are constructing the list of dictionaries {key: sample, item: {key: gene_id, item:[pathway1, ...] }}
    dict_list = {}

    # list of sample ID's extracted from the input header row
    sample_list = []
    for sample in header_row[3:len(header_row)]:
        sample_list.append(sample)
        dict_list[sample] = {}
        for gene in path_ko:
            for pathway in path_ko[gene]:
                dict_list[sample][pathway] = 0


    # adding the values to the dictionaries in the previous step as we iterate through the input file.
    req = requests.get('http://rest.kegg.jp/list/ko')
    get_gene_desc = extract_gene_description(req)
    top = ['Gene(KO)', 'Gene Description']
    top.extend(header_row[3:len(header_row)])

    input_detailed.writerow(top)
    repeat_gene_desc_list = {}
    for row in input:
        try:
            gene_description = get_gene_desc[row[0]]
            if gene_description in repeat_gene_desc_list:
                new_row = [repeat_gene_desc_list[row[0]], gene_description]
            else:
                new_row = [row[0], gene_description]
                repeat_gene_desc_list[gene_description] = row[0]
            new_row.extend(row[1:len(row)])
            input_detailed.writerow(new_row)
        except:
            new_row = [row[0], "unclassified"]
            new_row.extend(row[1:len(row)])
            input_detailed.writerow(new_row)

        if row[0][0] == 'K' and row[0][0:6] in path_ko.keys():
            paths = path_ko[row[0][0:6]]
            for item in paths:
                for head, col in zip(range(3, len(header_row)), range(1, len(row))):
                    dict_list[header_row[head]][item] += float(row[col])

    # all samples will have the samedictionary of pathways but different counts
    # so here we will iterate through the pathway IDs in order
    for item in sorted(dict_list[sample].items()):
        sample_pathcounts = []
        levels = list_hierarchy_pw(tree_data[0], tree_data[1], item[0])

        # then iterate through the samples and use the nested dictionary (dict_list)
        encounter_nonzero = False
        for sample_id in sample_list:
            if dict_list[sample_id][item[0]]!= 0:
                encounter_nonzero = True
            sample_pathcounts.append(dict_list[sample_id][item[0]])

        master_list = []
        master_list.extend(levels)
        master_list.extend(sample_pathcounts)
        if encounter_nonzero is True:
            output.writerow(master_list)



def merge_files(list):
    output_name = "temp/piphillin_script_merge.txt"
    line_dict = {}
    header = []
    with open(output_name, 'w') as merged_file:
        output = csv.writer(merged_file, delimiter='\t')
        x = 0
        for file in list:
            with open(file) as infile:
                infile = csv.reader(infile, delimiter='\t')
                list_infile = [line for line in infile]
                if x == 0:
                    header = list_infile[0]
                else: 
                    if header != list_infile[0]:
                        print ("Inconsistent formatting for the piphillin headers..")
                        
                for line in list_infile[1:len(list_infile)]:
                    if line[0] in line_dict.keys():
                        line_dict[line[0]] = [float(x) + float(y) for x, y in zip(line[1:len(line)], line_dict[line[0]])]
                    else:
                        line_dict[line[0]] = line[1:len(line)]
            x += 1
        
        output.writerow(header)
        for key in line_dict.keys():
            output.writerow([key] + line_dict[key])
    return output_name


def run_functional_profile(input, output, metadata):
    print("Arguments")

    # TODO
    log_file = ''
    sys.stdout = open(log_file, 'w')

    # request data linking genes to pathways, can be seen by entering the link into a browser too
    k = requests.get('http://rest.kegg.jp/link/pathway/ko')
    path_ko = extract_info(k)

    print("Hierarchy")

    # hierarchy level information extracted from the download link
    brite_htext = requests.get('http://www.genome.jp/kegg-bin/download_htext?htext=ko00001&format=htext&filedir=')
    tree_data = extract_hierarchy(brite_htext)

    input_list = input.split(',')
    full_path_list = []
    for object in input_list:
        objectName = object.replace('.zip', '').split('/')[-1]
        print(object)
        with zipfile.ZipFile(object, "r") as zip_ref:
            zip_ref.extractall("temp/" + objectName)
        name = "ko_abund_table_unnorm.txt"
        for root, dirs, files in os.walk('temp/'+objectName):
            if name in files:
                full_path_list.append(os.path.join(root, name))
                break

    print(full_path_list)

    if len(full_path_list)>1:
        print("Functional Profile: More then 1 file was passed so merging files.")
        input = merge_files(full_path_list)
    else:
        input = full_path_list[0]

    if output is None or output == '':
        output_hier = '%s_pathway_hierarchy_table.txt' %(output)
        output_des = '%s_genedes.txt' % (output)

    else:
        input_temp = input.split('/')[-1]
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M")
        os.mkdir("output/%s_functional_profile"%(time))
        #os.system("mkdir output/%s_functional_profile" % (time))
        output_str = "output/%s_functional_profile" % (time)
        output_hier = '%s/%s_pathway_hierarchy_table.txt' %(output_str, input_temp.strip('.txt'))
        output_des = '%s/%s_genedes_.txt' % (output_str, input_temp.strip('.txt'))
        print(output_str, input_temp.strip('.txt'))

        # TODO copy the metadata over I think??
        # copyfile(output_str, input_temp.strip('.txt'))
        #os.system('cp %s %s' %(input, "%s/%s_ipath.txt" %(output_str, input_temp.strip('.txt'))))

    input_temp = input.split('/')[-1]
    with open(input, 'r') as tsvin, open(output_hier, 'w', newline='') as hierarchy_out, \
            open(output_des, 'w', newline='') as detailed_out:
        input = csv.reader(tsvin, delimiter='\t')
        output = csv.writer(hierarchy_out, delimiter='\t', lineterminator="\n")
        input_detailed = csv.writer(detailed_out, delimiter='\t')

    # make adjustments here based on the type of file needed from the in put file header row
        print("Functional Profile: Constructing output for the functional profile.")
        construct_output(input, output, path_ko[0], tree_data, input_detailed)
        print("Functional Profile: Done Constructing output for the functional profile.")

    print("Functional Profile: Constructing Cytoscape output for the functional profile.")
    cytoscape_hier = '%s/%s_cytoscape_hierarchy.txt' % (output_str, input_temp.strip('.txt'))
    cytoscape.handle_files(output_hier, metadata, cytoscape_hier, 2)
    print("Functional Profile: Done Constructing Cytoscape output for the functional profile.\
            You may now retrieve your files:)")


if __name__ == '__main__':
    # system arguments
    parser = argparse.ArgumentParser(description='Input and Output file name options for t')
    parser.add_argument('-i', help='This is the file from Piphillin (.zip file). \
                                    If there is more then one input then arguments should be comma seperated.',
                        required=True)
    parser.add_argument('-o', help='This is the prefix for what you wish the output files to have. \
                                    For example: UCLA_109BL-W18_90cutoff',
                        required=True)
    parser.add_argument('-metadata', help='This should be the verified metadata from the first portion \
                                           of running the community profile.',
                        required=True)
    args = vars(parser.parse_args())
    input = args['i']
    output = args['o']
    # directory = args['dir']
    metadata = args['metadata']
    run_functional_profile(input, output, metadata)


