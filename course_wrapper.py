import datetime
import os
import piphillin
import stamp
import sys
import metadata_verification
import cytoscape


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_file(outdir):
    pass

class General():


    def clean_temp(self):
        os.system('rm temp/*')

    def create_output_directory(self, type, unique_string, outdir):
        if unique_string is not None:
            self.time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + "_" + unique_string
        else:
            self.time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M")

        if outdir is None or outdir == "":
            os.system("mkdir output/%s_%s_storage" % (self.time, type))
            directory = "%s/output/%s_%s_storage/" % (self.dir_path, self.time, type)

        else:
            #TODO I still need to fix this and change the output command elsewhere
            outdir = outdir.rstrip('/')
            os.system("mkdir %s/%s_%s_storage" % (outdir, self.time, type))
            directory = "%s/%s_%s_storage/" % (self.dir_path, self.time, type)

        self.output_directory = directory

    def start_log(self):
        log_path = self.output_directory + 'log.txt'

        print('Starting a log file at %s' % log_path)
        self.old_stdout = sys.stdout
        self.log_file = open(log_path, "w")
        sys.stdout = self.log_file

    def end_log(self):
        sys.stdout = self.old_stdout
        self.log_file.close()

    def verify_metadata(self, metadata, standard_otu):
        self.metadata_fileout = self.output_directory + "verified_metadata.tsv"
        self.metadata_validation = metadata_verification.verify_metadata(self.standard_otu, self.metadata, self.metadata_fileout)

        if self.metadata_validation != True:
            sys.exit(bcolors.FAIL + self.metadata_validation + bcolors.ENDC)
        else:
            print (bcolors.OKGREEN + "Metadata Successfully Verified." + bcolors.ENDC)
            pass



    def create_biom(self, input):

        print("Create .biom: clean header")
        os.system("head -1 %s" % input)
        os.system("sed -i -e 's/16S_seq_number\t/#OTU ID\t/g' %s" % input)

        print("Create .biom: done cleaning header")
        os.system("head -1 %s" % input)


        output = "temp/%s_standard_otu.biom" % (self.time)
        print("Create biom: make biom")
        os.system("biom convert -i %s -o %s --table-type='OTU table' --to-json" % (input, output))

        print("Create biom: done making .biom file")
        self.extra_biomtext = "%s/temp/%s_extra_file.txt" % (self.dir_path, self.time)

        print ("Create extra non-biom: in case user does not want rarefaction performed.")
        os.system("biom convert -i %s -o %s --to-tsv" % (output, self.extra_biomtext))

        return output

    def rarefy_and_merge(self, input):

        print("Rarefy and merge: import.")

        original_artifact = "%s/temp/%s_standard_otu.qza" % (self.dir_path, self.time)
        os.system("qiime tools import \
                    --input-path %s \
                    --type 'FeatureTable[Frequency]' \
                    --source-format BIOMV100Format \
                    --output-path %s" %(input, original_artifact))



        rarefaction_str = ""
        rarefaction_list = []

        print("Rarefy and merge: rarefactions.")
        for i in range(int(self.rarefactioniter)):
            output = "%s/temp/%s_rarefaction%s.qza" % (self.dir_path, self.time, i)
            rarefaction_list.append(output)
            rarefaction_str = rarefaction_str + " --i-tables %s" % output
            os.system("qiime feature-table rarefy \
                        --i-table %s \
                        --p-sampling-depth %s \
                        --o-rarefied-table %s" %(original_artifact, self.rarefactiondepth, output))

        print(rarefaction_str)

        merged_artifact = "%s/temp/%s_merged_file.qza" % (self.dir_path, self.time)
        export_dir = "%s/temp/" % self.dir_path
        merged_biom = "%s/temp/feature-table.biom" % (self.dir_path)
        merged_text = "%s/temp/%s_merged_file.txt" % (self.dir_path, self.time)

        print("Rarefy and merge: merge.")
        os.system("qiime feature-table merge \
                    %s \
                    --p-overlap-method sum \
                    --o-merged-table %s" %(rarefaction_str, merged_artifact))


        print("Rarefy and merge: export.")
        print("Input directory: %s" % merged_artifact)
        print("Output directory: %s" % export_dir)

        os.system("qiime tools export %s --output-dir %s" % (merged_artifact, export_dir))


        print("Rarefy and merge: convert to .txt from .biom.")
        os.system("biom convert -i %s -o %s --to-tsv" % (merged_biom, merged_text))

        print("Rarefy and merge: cleaning the text file.")

        os.system("sed -i '/# Constructed from biom file/d' %s" % merged_text)
        os.system("head -1 %s" % merged_text)

        os.system("sed -i -e 's/#OTU ID\t/OTU\t/g' %s" % merged_text)
        os.system("head -1 %s" % merged_text)

        self.merged_text = merged_text
        # TODO remove the rarefied files

    def run_piphillin(self):
        self.piphillin_out = self.output_directory + "piphillin/"
        print("Run Piphillin: mkdir")
        os.system("mkdir %s" % self.piphillin_out)

        #TODO make an integer table for piphillin and this one is ok for stamp
        self.piphillin_dec  = "%s/piphillinotu.csv" % (self.piphillin_out)
        piphillin_seq_out = "%s/piphillinseqs.fasta" % (self.piphillin_out)

        print("Run Piphillin: handling files")
        piphillin.handle_files(self.merged_text, self.piphillin_dec,
                               self.rarefactioniter, self.standard_sequences, piphillin_seq_out)

    def run_stamp(self, type):
        print("Run STAMP: mkdir")
        otu_key = stamp.get_key(self.standard_otu)
        self.stamp_directory = self.output_directory + "stamp_excel/"
        os.system("mkdir %s" % self.stamp_directory)
        self.stamp_taxa  = "%s/%s_stamp_excel_otu.tsv" % (self.stamp_directory, self.time)

        if type == "anacapa":
            self.taxa_levels = 6
        elif type == "MrDNA":
            self.taxa_levels = 7
        elif type == "QIIME2":
            self.taxa_levels = 7

        print("Run STAMP: reformatting")
        stamp.reformat(self.piphillin_dec, self.stamp_taxa, otu_key, self.taxa_levels)

    def msa(self):
        self.multiple_sequence_alignment = "%s/temp/%s_msa" % (self.dir_path, self.time)
        os.system('mafft %s > %s' % (self.standard_sequences, self.multiple_sequence_alignment))

    def phylogeny(self):
        self.phylogenetic_tree = "%s/temp/%s_phylotree" % (self.dir_path, self.time)
        os.system('fasttree -fastest -nt %s > %s ' % (self.multiple_sequence_alignment, self.multiple_sequence_alignment))


    def course_wrapper(self, type):
        """
        :param type: string from standard list of services
        :return: none: tells user that files have been ran :)
        """

        self.verify_metadata(self.standard_otu, self.metadata)
        self.standard_biom = self.create_biom(self.standard_otu)

        # RAREFY AND MERGE (if applicable)
        if self.rarefactiondepth is not None and self.rarefactiondepth != '' and int(self.rarefactiondepth) !=0 and \
                self.rarefactioniter is not None and self.rarefactioniter != '' and int(self.rarefactioniter) !=0:

            print (bcolors.WARNING + "Course Wrapper: Running Rarefaction and Merge" + bcolors.ENDC)
            self.rarefy_and_merge(self.standard_biom)
        else:
            print (bcolors.WARNING + "Course Wrapper: Skipping Rarefaction and Merge" + bcolors.ENDC)
            self.merged_text = self.extra_biomtext

        # PIPHILLIN
        print(bcolors.HEADER + "Piphillin: Producing formatted file sets for Piphillin @Secondgenome (only upload those with a number)." + bcolors.ENDC)
        self.run_piphillin()

        # STAMP/EXCEL
        print(bcolors.HEADER + "STAMP/Excel: running script to make files for STAMP/Excel." + bcolors.ENDC)
        self.run_stamp(type)

        # CYTOSCAPE
        self.cytoscape_directory = self.output_directory + "cytoscape/"
        print("Cytoscape: making directory.")
        os.system("mkdir %s" % self.cytoscape_directory)

        print(bcolors.WARNING + "Cytoscape: running cytoscape script." + bcolors.ENDC)
        outfile = self.cytoscape_directory + self.time + '_species_cytoscape.tsv'
        #TODO check to make sure 5 is always accurate? or should be self.taxa_levels
        self.cytoscape = cytoscape.handle_files(self.stamp_taxa, self.metadata, outfile, 5)

        # MSA/PHYLO
        if self.run_msa_phylo != False and self.run_msa_phylo != '' and self.run_msa_phylo is not None:
            print(bcolors.WARNING + "MSA: Running multiple sequence alignment using 'mafft'" + bcolors.ENDC)
            self.msa()

            print(bcolors.WARNING + "Phylogenetic Tree: Running phylogenetic tree construction." + bcolors.ENDC)
            self.phylogeny()

        # CLEAN TEMP
        # self.clean_temp()

        print("----------------------------------------------------------------------------------------------------")
        print(bcolors.OKGREEN + "DONE: You may now retrieve your files in the %s prefix folder in the output folder." % self.time + bcolors.ENDC)
        print("----------------------------------------------------------------------------------------------------")

        # self.end_log()
        sys.exit()


    def __init__(self, general_dict, metadata_dict):
        self.dir_path = os.getcwd()
        print (general_dict)
        self.create_output_directory(self.type, general_dict["unique_id"], general_dict["outdir"])
        # self.start_log()

        print (metadata_dict)

        self.metadata = metadata_dict['metadata']
        self.rarefactioniter = general_dict["rarefactioniter"]
        self.rarefactiondepth = general_dict["rarefactiondepth"]
        self.run_msa_phylo = general_dict["msa_phylo"]

        #TODO set this object for each tool
        self.standard_otu = " "
        self.standard_sequences = " "



#######################################################################################################
# ANACAPA WRAPPER
#######################################################################################################

class Anacapa(General):

    def handle_arguments(self, file_dictionary):

        self.otu_table = file_dictionary["otutable"]
        self.fwd_seq = file_dictionary["fwdseq"]
        self.merge_seq = file_dictionary["mergeseq"]
        self.reverse_seq = file_dictionary["reverseseq"]


    def get_all_seqs(self):
        #TODO add reverse compliment script
        os.system("cat %s %s %s > %s" %(self.fwd_seq, self.reverse_seq, self.merge_seq, "temp/%s_standard_sequences.fasta" % self.time))
        return "temp/%s_standard_sequences.fasta" % self.time


    def __init__(self, dictionary, metadata_dict):

        self.type = "anacapa"
        General.__init__(self, dictionary, metadata_dict)
        self.handle_arguments(dictionary)
        self.standard_otu = self.otu_table
        self.standard_sequences = self.get_all_seqs()

        # Run the Standard functions
        self.course_wrapper(self.type)


#######################################################################################################
# MrDNA WRAPPER
#######################################################################################################

class MrDNA(General):

    def handle_arguments(self, file_dictionary):

        self.otu_table = file_dictionary["otutable"]
        self.fwd_seq = file_dictionary["fwdseq"]

    def convert_otu_to_anacapa(self):
        os.system("mkdir temp")
        os.system("python convert_mrdna_to_anacapa_format.py -i %s -o temp/anacapa_format_otu_table.txt" % self.otu_table)
        return "temp/anacapa_format_otu_table.txt"


    def __init__(self, dictionary, metadata_dict):
        self.type = "MrDNA"
        General.__init__(self, dictionary, metadata_dict)

        self.handle_arguments(dictionary)
        self.standard_otu = self.convert_otu_to_anacapa()
        self.standard_sequences = self.fwd_seq

        # Run the Standard functions
        self.course_wrapper(self.type)


#######################################################################################################
# QIIME2 WRAPPER
#######################################################################################################

class QIIME2(General):

    def handle_arguments(self, file_dictionary):

        self.otu_table = file_dictionary["otutable"]
        self.fwd_seq = file_dictionary["fwdseq"]
        self.taxonomy = file_dictionary["taxonomy"]

    def convert_otu_to_anacapa(self):
        os.system("mkdir temp")
        os.system("qiime tools export %s --output-dir temp/otu_table" % self.otu_table)
        os.system("qiime tools export %s --output-dir temp/taxonomy" % self.taxonomy)
        os.system("python convert_qiime2_to_anacapa_format.py -inputOTU %s -inputTaxonomy %s -o temp/anacapa_format_otu_table.txt" % ("temp/otu_table/feature-table.biom", "temp/taxonomy/taxonomy.tsv"))
        return "temp/anacapa_format_otu_table.txt"

    def export_qza_sequences(self):
        os.system("qiime tools export %s --output-dir temp/sequences" % self.fwd_seq)
        return "temp/sequences/dna-sequences.fasta"

    def __init__(self, dictionary, metadata_dict):
        self.type = "QIIME2"
        General.__init__(self, dictionary, metadata_dict)
        self.handle_arguments(dictionary)
        self.standard_otu = self.convert_otu_to_anacapa()
        if not ".qza" in self.fwd_seq:
            self.standard_sequences = self.fwd_seq
        else:
            self.standard_sequences = self.export_qza_sequences()


        # Run the Standard functions
        self.course_wrapper(self.type)

