import install
# install.check_dependencies()
install.make_directories()

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

    #TODO add chris email and name here
    parser = argparse.ArgumentParser(description='Implementation by Keith Mitchell (keithgmitchell@g.ucla.edu)'
                                                 '  This is the CLI for the PUMA tool, the set of variables required will'
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
    args = vars(parser.parse_args())


    files_dictionary = {"otutable": '', "fwdseq": '', "reverseseq": '', "mergeseq": '',
                        "allseqs": '', "taxonomy": '', "rarefactiondepth": 0, "rarefactioniter": 0}
    metadata_dict = {"metadata": ''}

    #STANDARD
    files_dictionary["otutable"] = args['otutable']
    metadata_dict["metadata"] = args['metadata']

    files_dictionary["rarefactioniter"] = args['rarefactioniter']
    files_dictionary["rarefactiondepth"] = args['rarefactiondepth']


    #UNIQUE TO ANACAPA

    if args['type'] == 'anacapa':
        files_dictionary["fwdseq"] = args['fwdseq']
        files_dictionary["mergeseq"] = args['mergeseq']
        files_dictionary["reverseseq"] = args['reverseseq']

    #TODO is this true for mrdna/qiime2
    #TODO if not provided throw error.
    #TODO automate rarefaction option
    #TODO msa option
    else:
        files_dictionary["seqs"] = args['seqs']
        files_dictionary["taxonomy"] = args['taxonomy']

    print (files_dictionary)
    run_wrapper(files_dictionary, metadata_dict, args['type'])
