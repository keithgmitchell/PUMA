import datetime
import os


class General():

    def create_output_directory(self, type):
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        os.system("mkdir output/%s_%s_storage" % (time, type))
        directory = "output/%s_%s_storage/" % (time, type)
        self.output_directory = directory

    def create_biom(self, input):
        print ("Create biom: clean header")
        os.system("sed - i -e 's/16S_seq_number\t/#OTU ID\t/g' %s" %input)
        output = "temp/converged_otu.biom"
        print ("Create biom: make biom")
        os.system("biom convert -i %s -o %s --table-type='OTU table' --to-json" %(input, output))
        return output

    def rarefy_and_merge(self, input):

        print("Rarefy and merge: import.")
        dir_path = os.getcwd()
        original_artifact = "%stemp/standard_qza" %dir_path
        os.system("qiime tools import \
                    --input-path %s \
                    --type 'FeatureTable[Frequency]' \
                    --source-format BIOMV100Format \
                    --output-path %s.qza" %(input, original_artifact))



        rarefaction_str = ""
        rarefaction_list = []

        print("Rarefy and merge: rarefactions.")
        for i in range(int(self.rarefactioniter)):
            output = "%stemp/rarefaction%s.qza" %(dir_path, i)
            rarefaction_list.append(output)
            rarefaction_str = rarefaction_str + " --i-tables %s" %output
            os.system("qiime feature-table rarefy \
                        --i-table %s \
                        --p-sampling-depth %s \
                        --o-rarefied-table %s" %(original_artifact, self.rarefactiondepth, output))

        print(rarefaction_str)

        merged_artifact = "temp/merged_file.qza"
        merged_biom = "%stemp/merged_file.biom" %dir_path
        merged_text = "%stemp/merged_file.txt" %dir_path

        print("Rarefy and merge: merge.")
        os.system("qiime feature-table merge \
                    %s \
                    --p-overlap-method sum \
                    --o-merged-table %s" %(rarefaction_str, merged_artifact))


        print("Rarefy and merge: export.")
        os.system("qiime tools export %s --output-dir %s" %(merged_artifact, merged_biom))

        print("Rarefy and merge: convert to .txt from .biom.")
        os.system("biom convert -i %s -o %s --to-tsv" %(merged_biom, merged_text))

        print("Rarefy and merge: cleaning the text file.")
        os.system("sed -i '/# Constructed from biom file/d' %s" %merged_text)

        os.system("sed -i -e 's/#OTU ID\t/OTU\t/g' %s" %merged_text)

        self.merged_text = merged_text
        # TODO remove the rarefied files



    def msa(self):
        print("MSA.")
        msa = "temp/msa.qza"
        os.system("qiime tools import \
            --input-path %s \
            --type 'FeatureData[Sequences]' \
            --source-format DNAFASTAFormat \
            --output-path %s" %(self.standard_sequences, msa))

    def phylogeny(self):
        print ("Phylogeny.")

    def course_wrapper(self):
        self.standard_biom = self.create_biom(self.standard_otu)
        self.rarefy_and_merge(self.standard_biom)
        self.msa()
        self.phylogeny()


    def __init__(self, general_dict):
        self.rarefactioniter = general_dict["rarefactioniter"]
        self.rarefactiondepth = general_dict["rarefactiondepth"]

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
        self.create_output_directory("anacapa")
        self.course_wrapper()


