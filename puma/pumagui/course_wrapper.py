import datetime
import os
import sys
from . import metadata_verification, cytoscape, convert_mrdna_to_anacapa_format, piphillin, \
    convert_qiime2_to_anacapa_format, stamp
from biom import load_table
import zipfile
from Bio.Align.Applications import MafftCommandline
from Bio.Phylo.Applications import _Fasttree
from shutil import copyfile
from shutil import copyfileobj
import re, shutil, tempfile


class bcolors:
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''
    # HEADER = '\033[95m'
    # OKBLUE = '\033[94m'
    # OKGREEN = '\033[92m'
    # WARNING = '\033[93m'
    # FAIL = '\033[91m'
    # ENDC = '\033[0m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'


#TODO the parent class and lower class could have the same time...

def log_file(outdir):
    pass

def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    Code from https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python/31499114
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


class General():

    def create_output_directory(self, type, unique_string, outdir):
        if unique_string is not None:
            self.time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M") + "_" + unique_string
        else:
            self.time = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M")

        if outdir is None or outdir == "":
            directory = "%s/output/%s_%s_storage/" % (self.dir_path, self.time, type)
            if not os.path.exists(directory):
                os.mkdir(directory)

        else:
            # outdir = outdir.rstrip('/')
            directory = "%s/%s_%s_storage/" % (self.dir_path, self.time, type)
            if not os.path.exists(directory):
                os.mkdir(directory)

        self.log_file = directory + 'log.txt'
        sys.stdout = open(self.log_file, 'w')
        self.output_directory = directory


    def verify_metadata(self, metadata, standard_otu):
        self.metadata_fileout = self.output_directory + "verified_metadata.tsv"
        self.metadata_validation = metadata_verification.verify_metadata(self.standard_otu, self.metadata, self.metadata_fileout)

        if self.metadata_validation != True:
            print("ERROR: Metadata Verification." + '\n\t' + self.metadata_validation)
        else:
            print("Metadata: Successfully Verified.")
            pass

    def create_biom(self, input): # returns the biom file

        print("Create .biom: clean header")
        sed_inplace(input, '16S_seq_number\t', '#OTU ID\t')
        output = "temp/%s_standard_otu.biom" % (self.time)
        print("Create biom: make biom")



        self.extra_biomtext = "%s/temp/%s_extra_file.txt" % (self.dir_path, self.time)
        self.extra_qza = "%s/temp/%s_extra_qza.qza" % (self.dir_path, self.time)

        print("Create extra non-biom: in case user does not want rarefaction performed.")
        # load the biom as a table
        table = load_table(input)
        with open(output, 'w') as output_file, open(self.extra_biomtext, 'w') as merged_text_file:
            # output the biom table as a json file
            table.to_json("PUMA", output_file)
            out_tsv = table.to_tsv()
            merged_text_file.write(out_tsv)

        print("Create biom: done making .biom file")

        # TODO here
        # table = load_table(output)
        # with open(self.extra_biomtext, 'w') as extra_biomtext_out:
        #     table.to_json("PUMA", extra_biomtext_out)
        #     out_tsv = table.to_tsv()
        #     extra_biomtext_out.write(out_tsv)

        # print("Rarefy and merge: merge.")
        # with open(merged_biom, 'w') as merged_biom_file, open(merged_text, 'w') as merged_text_file:
        #     output_table.to_json("PUMA", merged_biom_file)
        #     out_tsv = output_table.to_tsv()
        #     merged_text_file.write(out_tsv)
        #
        # print("Rarefy and merge: convert to .txt from .biom.")
        # print("Rarefy and merge: cleaning the text file.")
        #
        # sed_inplace(merged_text, '#Constructed from biom file', '')
        # sed_inplace(merged_text, '#OTU ID\t', 'OTU\t')
        # self.merged_text = merged_text

        return output

    def rarefy_and_merge(self, input):

        print("Rarefy and merge: import.")

        original_biom_file = input
        table = load_table(original_biom_file)

        print("Rarefy and merge: rarefactions. %s (if 0 none is being performed)" % str(self.rarefactioniter))
        for i in range(int(self.rarefactioniter)):
            if i == 0:
                output_table = table.subsample(int(self.rarefactiondepth))
            else:
                output_table.merge(table.subsample(int(self.rarefactiondepth)))

        self.merged_artifact = "%s/temp/%s_merged_file.qza" % (self.dir_path, self.time)
        merged_biom = "%s/temp/feature-table.biom" % (self.dir_path)
        self.merged_biom = merged_biom
        merged_text = "%s/temp/%s_merged_file.txt" % (self.dir_path, self.time)

        print("Rarefy and merge: merge.")
        with open(merged_biom, 'w') as merged_biom_file, open(merged_text, 'w') as merged_text_file:
            output_table.to_json("PUMA", merged_biom_file)
            out_tsv = output_table.to_tsv()
            merged_text_file.write(out_tsv)

        print("Rarefy and merge: convert to .txt from .biom.")
        print("Rarefy and merge: cleaning the text file.")

        sed_inplace(merged_text, '#Constructed from biom file', '')
        sed_inplace(merged_text, '#OTU ID\t', 'OTU\t')
        self.merged_text = merged_text

    def run_piphillin(self):
        self.piphillin_out = self.output_directory + "piphillin/"
        print("Piphillin: mkdir")
        os.mkdir(self.piphillin_out)

        self.piphillin_dec  = "%s/piphillinotu.csv" % (self.piphillin_out)
        piphillin_seq_out = "%s/piphillinseqs.fasta" % (self.piphillin_out)

        print("Piphillin: handling files")
        piphillin.handle_files(self.merged_text, self.piphillin_dec,
                               self.rarefactioniter, self.standard_sequences, piphillin_seq_out)

    def run_stamp(self, type):
        print("STAMP: mkdir")
        otu_key = stamp.get_key(self.standard_otu)
        self.stamp_directory = self.output_directory + "stamp_excel/"
        os.mkdir(self.stamp_directory)
        self.stamp_taxa  = "%s/%s_stamp_excel_otu.tsv" % (self.stamp_directory, self.time)

        if type == "anacapa":
            self.taxa_levels = 7
        elif type == "MrDNA":
            self.taxa_levels = 7
        elif type == "QIIME2":
            self.taxa_levels = 7

        print("STAMP: reformatting")
        stamp.reformat(self.piphillin_dec, self.stamp_taxa, otu_key, self.taxa_levels)

    def msa(self):
        self.multiple_sequence_alignment = os.path.join(self.dir_path, "temp/%s_msa.txt"%(self.time))
        self.multiple_sequence_alignment_2 = os.path.join(self.dir_path, "temp/%s_msa2.txt"%(self.time))
        self.qiime_msa = os.path.join(self.qiime_out, "%s_qiime_msa.msa" % (self.time))

        script_fname = sys.argv[0]
        script_path = os.path.abspath(os.path.dirname(script_fname))
        mafft_exe_path = os.path.join(script_path, "mafft", "mafft-win", "mafft.bat")
        mafft_cline = MafftCommandline("mafft", input=os.path.abspath(self.standard_sequences))
        stdout, stderr = mafft_cline()
        with open(self.multiple_sequence_alignment, 'w') as handle1, open(self.multiple_sequence_alignment_2, 'w') as handle2, open(self.qiime_msa, 'w') as handle3:
            handle1.write(stdout)
            handle2.write(stdout)
            handle3.write(stdout)

    def phylogeny(self):
        script_fname = sys.argv[0]
        script_path = os.path.abspath(os.path.dirname(script_fname))

        self.phylogenetic_tree = os.path.join(self.dir_path, "temp", "%s_phylotree" % (self.time))
        cmd = _Fasttree.FastTreeCommandline('fasttree', input=os.path.abspath(self.multiple_sequence_alignment_2), out=os.path.abspath(self.phylogenetic_tree))

        self.qiime_phylo = os.path.join(self.qiime_out, "%s_qiime_phylo.phy" % (self.time))
        cmd()
        copyfile(self.phylogenetic_tree, self.qiime_phylo)

    def qiime_otu(self):
        # TODO this wont work with no rarefaction option
        self.qiime_out = os.path.join(self.output_directory, "qiime/")
        os.mkdir(self.qiime_out)
        qiime_file = os.path.join(self.qiime_out, "%s_qiime_otu.biom" % (self.time))
        copyfile(self.merged_biom, qiime_file)

    def ranacapa(self):
        self.ranacapa_out = os.path.join(self.output_directory, "ranacapa/")
        os.mkdir(self.ranacapa_out)
        ranacapa_file = os.path.join(self.ranacapa_out, "%s_ranacapa_otu.txt"%(self.time))
        copyfile(self.merged_text, ranacapa_file)

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

            print("Course Wrapper: Running Rarefaction and Merge")
            sys.stdout.flush()
            self.perform_rarefaction = True
            self.rarefy_and_merge(self.standard_biom)


        else:
            print("Course Wrapper: Skipping Rarefaction and Merge")
            self.perform_rarefaction = False
            self.merged_biom = self.standard_biom
            self.merged_text = self.extra_biomtext
            self.merged_artifact = self.extra_qza
            sys.stdout.flush()

        # RANACAPA
        sys.stdout.flush()
        self.ranacapa()

        # QIIME OTU
        sys.stdout.flush()
        self.qiime_otu()

        # PIPHILLIN
        print("Piphillin: Producing formatted file sets for Piphillin @Secondgenome (only upload those with a number).")
        sys.stdout.flush()
        self.run_piphillin()

        # STAMP/EXCEL
        print("STAMP/Excel: running script to make files for STAMP/Excel.")
        sys.stdout.flush()
        self.run_stamp(type)

        # CYTOSCAPE
        self.cytoscape_directory = self.output_directory + "cytoscape/"
        print("Cytoscape: making directory.")
        os.mkdir(self.cytoscape_directory)
        print("Cytoscape: running cytoscape script.")
        outfile = self.cytoscape_directory + self.time + '_species_cytoscape.tsv'
        sys.stdout.flush()
        self.cytoscape = cytoscape.handle_files(self.stamp_taxa, self.metadata, outfile, self.taxa_levels - 1)

        # MSA/PHYLO
        if self.run_msa_phylo != 'False' and self.run_msa_phylo != False and self.run_msa_phylo != '' and self.run_msa_phylo is not None:
            print("MSA: Running multiple sequence alignment using 'mafft'")
            sys.stdout.flush()
            self.msa()

            print("Phylogenetic Tree: Running phylogenetic tree construction.")
            sys.stdout.flush()
            self.phylogeny()


        print("----------------------------------------------------------------------------------------------------")
        print("DONE: You may now retrieve your files in the %s prefix folder in the output folder." % self.output_directory)
        print("----------------------------------------------------------------------------------------------------")
        sys.stdout.flush()

    def __init__(self, general_dict, metadata_dict):
        self.dir_path = os.getcwd()
        self.create_output_directory(self.type, general_dict["unique_id"], general_dict["outdir"])

        self.metadata = metadata_dict['metadata']
        self.rarefactioniter = general_dict["rarefactioniter"]
        self.rarefactiondepth = general_dict["rarefactiondepth"]
        self.run_msa_phylo = general_dict["msa_phylo"]

        # set this object for each tool
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
        with open("temp/%s_standard_sequences.fasta" % self.time, 'wb') as wfd:
            for f in [self.fwd_seq, self.reverse_seq, self.merge_seq]:
                with open(f, 'rb') as fd:
                    copyfileobj(fd, wfd)
        return "temp/%s_standard_sequences.fasta" % self.time


    def __init__(self, dictionary, metadata_dict):

        self.type = "anacapa"
        General.__init__(self, dictionary, metadata_dict)
        print(dictionary)
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
        convert_mrdna_to_anacapa_format.execute_conversion(self.otu_table, 'temp/%s_anacapa_format_otu_table.txt' % self.time)
        return "temp/%s_anacapa_format_otu_table.txt" % self.time


    def __init__(self, dictionary, metadata_dict):
        self.type = "MrDNA"
        General.__init__(self, dictionary, metadata_dict)
        print(dictionary)
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
        with zipfile.ZipFile(os.path.abspath(self.otu_table), "r") as zip_ref:
            zip_ref.extractall("temp/%s_otu_table" % self.time)
        with zipfile.ZipFile(os.path.abspath(self.taxonomy), "r") as zip_ref:
            zip_ref.extractall("temp/%s_taxonomy" % self.time)
        with zipfile.ZipFile(os.path.abspath(self.fwd_seq), "r") as zip_ref:
            zip_ref.extractall("temp/%s_sequences" % self.time)

        otu_name = "feature-table.biom"
        for root, dirs, files in os.walk("temp/%s_otu_table" % self.time):
            if otu_name in files:
                otu_file = os.path.join(root, otu_name)
                break
        tax_name = "taxonomy.tsv"
        for root, dirs, files in os.walk("temp/%s_taxonomy" % self.time):
            if tax_name in files:
                tax_file = os.path.join(root, tax_name)
                break
        seq_name = "dna-sequences.fasta"
        for root, dirs, files in os.walk("temp/%s_sequences" % self.time):
            if seq_name in files:
                seq_file = os.path.join(root, seq_name)
                break
        self.standard_sequences = seq_file
        convert_qiime2_to_anacapa_format.exec_qiime2_anacapa(otu_file, tax_file, "temp/%s_anacapa_format_otu_table.txt" % self.time)
        return "temp/%s_anacapa_format_otu_table.txt" % self.time

    # def export_qza_sequences(self):
    #     os.system("qiime tools export %s --output-dir temp/%s_sequences" % (self.fwd_seq, self.time))
    #     return "temp/sequences/%s_dna-sequences.fasta" % self.time

    def __init__(self, dictionary, metadata_dict):
        self.type = "QIIME2"
        General.__init__(self, dictionary, metadata_dict)
        print(dictionary)
        self.handle_arguments(dictionary)
        self.standard_otu = self.convert_otu_to_anacapa()
        # if not ".qza" in self.fwd_seq:
        #     self.standard_sequences = self.fwd_seq
        # else:
        #     self.standard_sequences = self.export_qza_sequences()

        self.course_wrapper(self.type)

