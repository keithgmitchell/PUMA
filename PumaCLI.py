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
    
    parser = argparse.ArgumentParser(description='Implementation by Keith Mitchell (keithgmitchell@g.ucla.edu) \n'
                                                 '> This is the CLI for the PUMA tool, the set of variables required will \n'
                                                 '  follow the example (in the "examples" folder) files for the \n'
                                                 '  corresponding services folders.\n'
                                                 '> All of the following arguments are file paths, except -type.')

    parser.add_argument('-type', help='This is the sequencing service to run the tool for \n.'
                                      ' OPTIONS: "MrDNA","QIIME2","anacapa"', required=True)
    parser.add_argument('-metadata', help='Metadata corresponding to the taxonomy table.', required=True)
    parser.add_argument('-otutable', help='OTU/ASV from the corresponding service variable.', required=True)
    parser.add_argument('-seqs', help='Master file of DNA seqs.', required=False)
    parser.add_argument('-fwdseqs', help='Forward DNA seqs.', required=False)
    parser.add_argument('-mergeseqs', help='Merged DNA seqs.', required=False)
    parser.add_argument('-reverseseqs', help='Reversed DNA seqs.', required=False)
    parser.add_argument('-taxonomy', help='Some services have a seperate taxonomy file.', required=False)
    parser.add_argument('-rarefactioniter', help='Some services have a seperate taxonomy file.', default=5, required=False)
    parser.add_argument('-rarefactiondepth', help='If this is not provided we will automatically calculate a good '
                                                  'depth and report it back to you.', default=5, required=False)
    args = vars(parser.parse_args())


    files_dictionary = {"otutable": '', "fwdseq": '', "reverseseq": '', "mergeseq": '',
                        "allseqs": '', "taxonomy": '', "rarefactiondepth": 0, "rarefactioniter": 0}
    metadata_dict = {"metadata": ''}

    #STANDARD
    files_dictionary["otutable"] = args['otutable']
    metadata_dict["metadata"] = args['metadata']

    if args['rarefactioniter']:
        files_dictionary["rarefactioniter"] = args['rarefactioniter']
    else:
        files_dictionary["rarefactioniter"] = 5

    if args['rarefactiondepth']:
        files_dictionary["rarefactiondepth"] = args['rarefactiondepth']
    else:
        #TODO automate the rarefaction depth....
        pass



    #UNIQUE TO ANACAPA
    if args['type'] == 'anacapa':
        files_dictionary["fwdseqs"] = args['fwdseqs']
        files_dictionary["mergeseqs"] = args['mergeseqs']
        files_dictionary["reverseseqs"] = args['reverseseqs']

    #TODO is this true for mrdna/qiime2
    #TODO if not provided throw error.
    else:
        files_dictionary["seqs"] = args['seqs']
        files_dictionary["taxonomy"] = args['taxonomy']

    run_wrapper(files_dictionary, metadata_dict, args['type'])
