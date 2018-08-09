import datetime
import os
import piphillin
import stamp
import sys
import metadata_verification


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class General():

    def clean_temp(self):
        os.system('rm temp/*')

    def create_output_directory(self, type):
        self.time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M")
        os.system("mkdir output/%s_%s_storage" % (self.time, type))
        directory = "%s/output/%s_%s_storage/" % (self.dir_path, self.time, type)
        self.output_directory = directory

    def verify_metadata(self, metadata, standard_otu):
        self.metadata_validation = metadata_verification.verify_metadata(self. standard_otu, self.metadata, self.time)
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
        self.stamp_out = self.output_directory + "stamp/"
        os.system("mkdir %s" % self.stamp_out)
        self.stamp_taxa  = "%s/%s_stamp_otu.tsv" % (self.stamp_out, self.time)

        if type == "anacapa":
            self.taxa_levels = 6
        elif type == "MrDNA":
            self.taxa_levels = 7
        elif type == "QIIME2":
            self.taxa_levels = 7

        print("Run STAMP: reformatting")
        stamp.reformat(self.piphillin_dec, self.stamp_taxa, otu_key, self.taxa_levels)

    def msa(self):
        # TODO take user path to executable mafft?


        self.multiple_sequence_alignment = "%s/temp/%s_msa" % (self.dir_path, self.time)
        os.system('mafft %s > %s' % (self.standard_sequences, self.multiple_sequence_alignment))


        # TODO this next part
        print("MSA: import the sequences file as qza")

        #
        #
        # sequences_import = "%s/temp/sequences_for_msa.qza" % self.dir_path
        # os.system("qiime tools import \
        #                     --input-path %s \
        #                     --type 'FeatureData[Sequence]' \
        #                     --source-format DNAFASTAFormat \
        #                     --output-path %s" % (self.standard_sequences, sequences_import))
        #
        # self.aligned_sequences = "%s/temp/aligned_sequences.qza" % self.dir_path
        # os.system("qiime alignment mafft \
        #                     --i-sequences %s \
        #                     --o-alignment %s" % (sequences_import, self.aligned_sequences))

    def phylogeny(self):
        print("Phylogeny.")
        phylogeny = "%s/temp/phylogeny.qza" % self.dir_path
        os.system("qiime phylogeny fasttree \
                            --i-alignment %s \
                            --o-tree %s" % (self.aligned_sequences, phylogeny))


    def course_wrapper(self, type):
        """
        :param type: string from standard list of services
        :return: none: tells user that files have been ran :)
        """
        self.verify_metadata(self.standard_otu, self.metadata)
        self.standard_biom = self.create_biom(self.standard_otu)

        #Check if user wants rarefaction
        if self.rarefactiondepth is not None and self.rarefactiondepth != '' and int(self.rarefactiondepth) !=0 and \
                self.rarefactioniter is not None and self.rarefactioniter != '' and int(self.rarefactioniter) !=0:

            print (bcolors.OKBLUE + "Course Wrapper: Running Rarefaction and Merge" + bcolors.ENDC)
            self.rarefy_and_merge(self.standard_biom)
        else:
            print (bcolors.WARNING + "Course Wrapper: Skipping Rarefaction and Merge" + bcolors.ENDC)
            self.merged_text = self.extra_biomtext

        self.run_piphillin()
        self.run_stamp(type)

        #TODO take arguments to see if user wants these
        print(bcolors.WARNING + "MSA: Running multiple sequence alignment using 'mafft'" + bcolors.ENDC)
        self.msa()
        # self.phylogeny()

        #self.clean_temp()
        print ("----------------------------------------------------------------------------------------------------")
        print (bcolors.OKGREEN + "DONE: You may now retrieve your files in the %s prefix folder in the output folder." % self.time + bcolors.ENDC)
        print ("----------------------------------------------------------------------------------------------------")
        sys.exit()


    def __init__(self, general_dict, metadata_dict):
        self.metadata = metadata_dict['metadata']
        self.rarefactioniter = general_dict["rarefactioniter"]
        self.rarefactiondepth = general_dict["rarefactiondepth"]
        self.dir_path = os.getcwd()

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

        General.__init__(self, dictionary, metadata_dict)
        self.type = "anacapa"
        self.create_output_directory(self.type)

        self.handle_arguments(dictionary)
        self.standard_otu = self.otu_table
        self.standard_sequences = self.get_all_seqs()


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

        General.__init__(self, dictionary, metadata_dict)
        self.type = "MrDNA"
        self.create_output_directory(self.type)

        self.handle_arguments(dictionary)
        self.standard_otu = self.convert_otu_to_anacapa()
        self.standard_sequences = self.fwd_seq


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


    def __init__(self, dictionary, metadata_dict):

        General.__init__(self, dictionary, metadata_dict)
        self.type = "QIIME2"
        self.create_output_directory(self.type)

        self.handle_arguments(dictionary)
        self.standard_otu = self.convert_otu_to_anacapa()
        self.standard_sequences = self.fwd_seq


        self.course_wrapper(self.type)

