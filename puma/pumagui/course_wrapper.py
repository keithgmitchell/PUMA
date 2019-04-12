import datetime
import os
import sys
from puma.puma import stamp, metadata_verification, piphillin, cytoscape, convert_mrdna_to_anacapa_format, \
    convert_qiime2_to_anacapa_format
from biom import load_table
import zipfile
from Bio.Align.Applications import MafftCommandline
from Bio.Phylo.Applications import _Fasttree
from shutil import copyfile
from shutil import copyfileobj
import re, shutil, tempfile


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
        sed_inplace(input, '16S_seq_number\t', '#OTU ID\t')
        output = "temp/%s_standard_otu.biom" % (self.time)
        print("Create biom: make biom")
        table = load_table(input)
        with open(output, 'w') as output_file:
            table.to_json("PUMA", output_file)

        print("Create biom: done making .biom file")
        self.extra_biomtext = "%s/temp/%s_extra_file.txt" % (self.dir_path, self.time)
        self.extra_qza = "%s/temp/%s_extra_qza.qza" % (self.dir_path, self.time)

        print ("Create extra non-biom: in case user does not want rarefaction performed.")
        table = load_table(output)
        with open(self.extra_biomtext, 'w') as output_file:
            table.to_json("PUMA", output_file)
        return output

    def rarefy_and_merge(self, input):

        print("Rarefy and merge: import.")

        # original_dir = "%s/temp/%s_original_dir" % (self.dir_path, self.time)

        original_biom_file = input
        table = load_table(original_biom_file)
        # rarefaction_str = ""
        # rarefaction_list = []

        print("Rarefy and merge: rarefactions.")
        for i in range(int(self.rarefactioniter)):
            if i == 0:
                output_table = table.subsample(int(self.rarefactiondepth))
            else:
                output_table.merge(table.subsample(int(self.rarefactiondepth)))
            # output = "%s/temp/%s_rarefaction%s.qza" % (self.dir_path, self.time, i)

        self.merged_artifact = "%s/temp/%s_merged_file.qza" % (self.dir_path, self.time)
        # export_dir = "%s/temp/" % self.dir_path
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
        # TODO remove the rarefied files

    def run_piphillin(self):
        self.piphillin_out = self.output_directory + "piphillin/"
        print("Run Piphillin: mkdir")
        os.mkdir(self.piphillin_out)

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
        os.mkdir(self.stamp_directory)
        self.stamp_taxa  = "%s/%s_stamp_excel_otu.tsv" % (self.stamp_directory, self.time)

        if type == "anacapa":
            self.taxa_levels = 7
        elif type == "MrDNA":
            self.taxa_levels = 7
        elif type == "QIIME2":
            self.taxa_levels = 7

        print("Run STAMP: reformatting")
        stamp.reformat(self.piphillin_dec, self.stamp_taxa, otu_key, self.taxa_levels)

    def msa(self):
        self.multiple_sequence_alignment = os.path.join(self.dir_path, "temp/%s_msa.txt"%(self.time))
        self.multiple_sequence_alignment_2 = os.path.join(self.dir_path, "temp/%s_msa2.txt"%(self.time))
        self.qiime_msa = os.path.join(self.qiime_out, "%s_qiime_msa.msa" % (self.time))

        script_fname = sys.argv[0]
        script_path = os.path.abspath(os.path.dirname(script_fname))
        mafft_exe_path = os.path.join(script_path, "mafft", "mafft-win", "mafft.bat")
        mafft_cline = MafftCommandline(mafft_exe_path, input=os.path.abspath(self.standard_sequences))
        stdout, stderr = mafft_cline()
        with open(self.multiple_sequence_alignment, 'w') as handle1, open(self.multiple_sequence_alignment_2, 'w') as handle2, open(self.qiime_msa, 'w') as handle3:
            handle1.write(stdout)
            handle2.write(stdout)
            handle3.write(stdout)

    def phylogeny(self):
        script_fname = sys.argv[0]
        script_path = os.path.abspath(os.path.dirname(script_fname))
        fasttree_exe = os.path.join(script_path, "fasttree", "FastTree.exe")

        self.phylogenetic_tree = os.path.join(self.dir_path, "temp", "%s_phylotree" % (self.time))
        cmd = _Fasttree.FastTreeCommandline(fasttree_exe, input=os.path.abspath(self.multiple_sequence_alignment_2), out=os.path.abspath(self.phylogenetic_tree))

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

            print(bcolors.WARNING + "Course Wrapper: Running Rarefaction and Merge" + bcolors.ENDC)
            self.perform_rarefaction = True
            self.rarefy_and_merge(self.standard_biom)
        else:
            print(bcolors.WARNING + "Course Wrapper: Skipping Rarefaction and Merge" + bcolors.ENDC)
            self.perform_rarefaction = False
            self.merged_text = self.extra_biomtext
            self.merged_artifact = self.extra_qza

        # RANACAPA
        self.ranacapa()

        # QIIME OTU
        self.qiime_otu()

        # PIPHILLIN
        print(bcolors.HEADER + "Piphillin: Producing formatted file sets for Piphillin @Secondgenome (only upload those with a number)." + bcolors.ENDC)
        self.run_piphillin()

        # STAMP/EXCEL
        print(bcolors.HEADER + "STAMP/Excel: running script to make files for STAMP/Excel." + bcolors.ENDC)
        self.run_stamp(type)

        # CYTOSCAPE
        self.cytoscape_directory = self.output_directory + "cytoscape/"
        print("Cytoscape: making directory.")
        os.mkdir(self.cytoscape_directory)

        print(bcolors.WARNING + "Cytoscape: running cytoscape script." + bcolors.ENDC)
        outfile = self.cytoscape_directory + self.time + '_species_cytoscape.tsv'
        #TODO check to make sure 5 is always accurate? or should be self.taxa_levels
        self.cytoscape = cytoscape.handle_files(self.stamp_taxa, self.metadata, outfile, self.taxa_levels - 1)

        # MSA/PHYLO
        if self.run_msa_phylo != False and self.run_msa_phylo != '' and self.run_msa_phylo is not None:
            print(bcolors.WARNING + "MSA: Running multiple sequence alignment using 'mafft'" + bcolors.ENDC)
            self.msa()

            print(bcolors.WARNING + "Phylogenetic Tree: Running phylogenetic tree construction." + bcolors.ENDC)
            self.phylogeny()


        print("----------------------------------------------------------------------------------------------------")
        print(bcolors.OKGREEN + "DONE: You may now retrieve your files in the %s prefix folder in the output folder." % self.time + bcolors.ENDC)
        print("----------------------------------------------------------------------------------------------------")
        sys.exit()


    def __init__(self, general_dict, metadata_dict):
        self.dir_path = os.getcwd()
        print (general_dict)
        self.create_output_directory(self.type, general_dict["unique_id"], general_dict["outdir"])

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
        with open("temp/%s_standard_sequences.fasta" % self.time, 'wb') as wfd:
            for f in [self.fwd_seq, self.reverse_seq, self.merge_seq]:
                with open(f, 'rb') as fd:
                    copyfileobj(fd, wfd)
        return "temp/%s_standard_sequences.fasta" % self.time


    def __init__(self, dictionary, metadata_dict):

        self.type = "anacapa"
        General.__init__(self, dictionary, metadata_dict)
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
        convert_mrdna_to_anacapa_format.execute_conversion(self.otu_table, 'temp/anacapa_format_otu_table.txt')
        return "temp/anacapa_format_otu_table.txt"


    def __init__(self, dictionary, metadata_dict):
        self.type = "MrDNA"
        General.__init__(self, dictionary, metadata_dict)

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
            zip_ref.extractall("temp/otu_table")
        with zipfile.ZipFile(os.path.abspath(self.taxonomy), "r") as zip_ref:
            zip_ref.extractall("temp/taxonomy")

        otu_name = "feature-table.biom"
        for root, dirs, files in os.walk("temp/otu_table"):
            if otu_name in files:
                otu_file = os.path.join(root, otu_name)
                break
        tax_name = "taxonomy.tsv"
        for root, dirs, files in os.walk("temp/taxonomy"):
            if tax_name in files:
                tax_file = os.path.join(root, tax_name)
                break
        convert_qiime2_to_anacapa_format.exec_qiime2_anacapa(otu_file, tax_file, "temp/anacapa_format_otu_table.txt")
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

        self.course_wrapper(self.type)
