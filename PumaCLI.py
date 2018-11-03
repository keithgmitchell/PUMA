import install
# install.check_dependencies()
install.make_directories()
from course_wrapper import bcolors
import argparse
import sys
import course_wrapper

def run_wrapper(files, metadata_dict, type):
    if type == 'anacapa':
        course_wrapper.Anacapa(files, metadata_dict)
    elif type == 'MrDNA':
        course_wrapper.MrDNA(files, metadata_dict)
    elif type == 'QIIME2':
        course_wrapper.QIIME2(files, metadata_dict)
    else:
        sys.exit("ARGUMENT ERROR: Proper sequencing service '-type' not provided. Please use '--help' to see more info.")


if __name__ == "__main__":



    parser = argparse.ArgumentParser(description='  This is the CLI for the PUMA tool, the set of variables required will'
                                                 '  follow the example (in the "examples" folder) files for the'
                                                 '  corresponding services folders.'
                                                 '  All of the following arguments are file paths, except -type.')

    parser.add_argument('-type', help='This is the sequencing service to run the tool for \n.'
                                      ' OPTIONS: "MrDNA","QIIME2","anacapa"', required=True)
    parser.add_argument('-metadata', help='Metadata corresponding to the taxonomy table.', required=True)
    parser.add_argument('-otutable', help='OTU/ASV from the corresponding service variable.', required=True)
    parser.add_argument('-seqs', help='Master file of DNA seqs.', required=False)
    parser.add_argument('-fwdseq', help='Forward DNA seqs.', required=False)
    parser.add_argument('-mergeseq', help='Merged DNA seqs.', required=False)
    parser.add_argument('-reverseseq', help='Reversed DNA seqs.', required=False)
    parser.add_argument('-taxonomy', help='Some services have a seperate taxonomy file.', required=False)
    parser.add_argument('-rarefactioniter', help='Some services have a seperate taxonomy file.', required=False)
    parser.add_argument('-rarefactiondepth', help='If this is not provided we will automatically calculate a good '
                                                  'depth and report it back to you.', required=False)

    parser.add_argument('-unique_id', help='If you would like to specify any other identifier in the naming of output '
                                           'files please place that here.', required=False)

    parser.add_argument('-msa_phylo', help='Include this argument if you want to run MSA using muscle and Phylogenetic'
                                           ' Tree using FastTree.', required=False)

    parser.add_argument('-outdir', help='If you would like to specify where the output goes other then the output '
                                        'diretory in this folder.', required=False)

    args = vars(parser.parse_args())


    files_dictionary = {"otutable": '', "fwdseq": '', "reverseseq": '', "mergeseq": '', "unique_id":'',
                        "allseqs": '', "taxonomy": '', "rarefactiondepth": 0, "rarefactioniter": 0,
                        "msa_phylo": False, "outdir": '' }


    metadata_dict = {"metadata": ''}

    #STANDARD
    files_dictionary["otutable"] = args['otutable']
    metadata_dict["metadata"] = args['metadata']
    files_dictionary["rarefactioniter"] = args['rarefactioniter']
    files_dictionary["rarefactiondepth"] = args['rarefactiondepth']
    files_dictionary["unique_id"] = args["unique_id"]
    files_dictionary["msa_phylo"] = args["msa_phylo"]
    files_dictionary["outdir"] = args["outdir"]


    if args['type'] == 'anacapa':
        if args["fwdseq"] is not None and args["mergeseq"] is not None and args["reverseseq"] is not None:

            files_dictionary["fwdseq"] = args['fwdseq']
            files_dictionary["mergeseq"] = args['mergeseq']
            files_dictionary["reverseseq"] = args['reverseseq']

        else:
            print("----------------------------------------------------------------------------------------------------")
            print(bcolors.FAIL + "ANACAPA: Must have fwdseq, mergedseq, and reverseq files provided." + bcolors.ENDC)
            print("----------------------------------------------------------------------------------------------------")
            sys.exit()

    elif args['type'] == 'MrDNA':
        files_dictionary["fwdseq"] = args['seqs']
    elif args['type'] == 'QIIME2':
        files_dictionary["fwdseq"] = args['seqs']
        files_dictionary["taxonomy"] = args['taxonomy']


    run_wrapper(files_dictionary, metadata_dict, args['type'])
