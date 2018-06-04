import datetime
import os
import piphillin
import stamp


class General():

    def clean_temp(self):
        return 0

    def create_output_directory(self, type):
        self.time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M")
        os.system("mkdir output/%s_%s_storage" % (self.time, type))
        directory = "%s/output/%s_%s_storage/" % (self.dir_path, self.time, type)
        self.output_directory = directory

    def create_biom(self, input):

        print("Create .biom: clean header")
        os.system("head -1 %s" % input)
        os.system("sed - i -e 's/16S_seq_number\t/#OTU ID\t/g' %s" % input)

        # TODO figure out why i need to do this
        os.system("^C")

        print (" ")
        print("Create .biom: done cleaning header")
        os.system("head -1 %s" % input)



        output = "temp/standard_otu.biom"
        print("Create biom: make biom")
        os.system("biom convert -i %s -o %s --table-type='OTU table' --to-json" % (input, output))

        print("Create biom: done making .biom file")

        return output

    def rarefy_and_merge(self, input):

        print("Rarefy and merge: import.")

        original_artifact = "%s/temp/standard_otu.qza" % self.dir_path
        os.system("qiime tools import \
                    --input-path %s \
                    --type 'FeatureTable[Frequency]' \
                    --source-format BIOMV100Format \
                    --output-path %s" %(input, original_artifact))



        rarefaction_str = ""
        rarefaction_list = []

        print("Rarefy and merge: rarefactions.")
        for i in range(int(self.rarefactioniter)):
            output = "%s/temp/rarefaction%s.qza" % (self.dir_path, i)
            rarefaction_list.append(output)
            rarefaction_str = rarefaction_str + " --i-tables %s" % output
            os.system("qiime feature-table rarefy \
                        --i-table %s \
                        --p-sampling-depth %s \
                        --o-rarefied-table %s" %(original_artifact, self.rarefactiondepth, output))

        print(rarefaction_str)

        merged_artifact = "%s/temp/merged_file.qza" % self.dir_path
        export_dir = "%s/temp/" % self.dir_path
        merged_biom = "%s/temp/feature-table.biom" % self.dir_path
        merged_text = "%s/temp/merged_file.txt" % self.dir_path

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
        export_dir = self.output_directory + "piphillin/"
        print("Run Piphillin: mkdir")
        os.system("mkdir %s" % export_dir)
        piphillin_text_out = "%s/piphillinotu.csv" % export_dir
        piphillin_seq_out = "%s/piphillinseqs.fasta" %export_dir

        print("Run Piphillin: handling files")
        piphillin.handle_files(self.merged_text, piphillin_text_out,
                               self.rarefactioniter, self.standard_sequences, piphillin_seq_out)

    def run_stamp(self):
        return 0

    def msa(self):
        print("MSA: import the sequences file as qza")
        # TODO make this for the filtered sequences

        sequences_msa_import = "%s/temp/sequences_for_msa.qza" % self.dir_path
        os.system("qiime tools import \
                            --input-path %s \
                            --type 'FeatureData[Sequence]' \
                            --source-format DNAFASTAFormat \
                            --output-path %s" % (self.standard_sequences, sequences_msa_import))

        #TODO find the proper argument for MSA qiime2 or just use mafft cli

    def phylogeny(self):
        # TODO find the proper argument for MSA qiime2 or just use fasttree cli
        print("Phylogeny.")

    def course_wrapper(self):
        self.standard_biom = self.create_biom(self.standard_otu)
        self.rarefy_and_merge(self.standard_biom)
        self.run_piphillin()
        self.run_stamp()
        self.msa()
        self.phylogeny()


    def __init__(self, general_dict):
        self.rarefactioniter = general_dict["rarefactioniter"]
        self.rarefactiondepth = general_dict["rarefactiondepth"]
        self.dir_path = os.getcwd()

        #TODO set this object for each tool
        self.standard_otu = " "
        self.standard_sequences = " "



class Anacapa(General):

    def handle_arguments(self, file_dictionary):

        self.otu_table = file_dictionary["otutable"]
        self.fwd_seq = file_dictionary["fwdseq"]
        self.merge_seq = file_dictionary["mergeseq"]
        self.reverse_seq = file_dictionary["reverseseq"]


    def get_all_seqs(self):
        #TODO add reverse compliment script
        os.system("cat %s %s %s > %s" %(self.fwd_seq, self.reverse_seq, self.merge_seq, "temp/standard_sequences.fasta"))
        return "temp/standard_sequences.fasta"


    def __init__(self, dictionary):

        General.__init__(self, dictionary)

        self.handle_arguments(dictionary)
        self.standard_otu = self.otu_table
        self.standard_sequences = self.get_all_seqs()

        self.type = "anacapa"
        self.create_output_directory(self.type)
        self.course_wrapper()


