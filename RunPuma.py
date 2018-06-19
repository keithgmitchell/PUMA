from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import course_wrapper
import time


class PUMA(Frame):
    def get_new_file_dict(self):
        files_dictionary = {"otutable": '', "fwdseq": '', "reverseseq": '', "mergeseq": '',
                            "allseqs": '', "taxonomy": '', "rarefactiondepth": 0, "rarefactioniter": 0}

        return files_dictionary

    #TODO pass the file types that can be opened as an argument here
    def load_file(self, string, dictionary):
        fname = filedialog.askopenfilename(filetypes=(("Text file.", "*.txt"),
                                           ("Tab seperated values", "*.tsv"), ("Fasta file", "*.fasta"), ("QIIME Artifact","*.qza")))
        if fname:
            try:
                dictionary[string] = fname
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return


#############################################################################################################
#ANACAPA

    def initiate_ancapa(self):
        self.anacapa_window = Toplevel()
        self.anacapa_window.title("Anacapa File Input")
        self.initiate_anacapa_labels()
        self.initiate_anacapa_fields()
        self.display_anacapa_fields()

    def initiate_anacapa_labels(self):

        self.description = Label(self.anacapa_window, wraplength=500,
                                 text="The anacapa pipeline will produce the following files of interest:")

        self.otutable_l = Label(self.anacapa_window, text="OTU/ASV Table (raw taxonomy .tsv file:")
        self.forwardseqs_l = Label(self.anacapa_window, text="OTU/ASV Forward Sequences (.fasta format):")
        self.reverseseqs_l = Label(self.anacapa_window, text="OTU/ASV Reverse Sequences (.fasta format):")
        self.mergeseqs_l = Label(self.anacapa_window, text="OTU/ASV Merged Sequences (.fasta format):")
        self.rarefactiondepth_l = Label(self.anacapa_window, text="Rarefaction Depth:")
        self.rarefactioniter_l = Label(self.anacapa_window, text="Rarefaction Iterations:")

    def initiate_anacapa_fields(self):
        self.anacapa_dict = self.get_new_file_dict()

        #TODO pass file types accepted
        self.otutable = Button(self.anacapa_window, text="OTU/ASV Table",
                               command=(lambda: self.load_file("otutable", self.anacapa_dict)), width=20)

        self.forwardseqs = Button(self.anacapa_window, text="OTU/ASV Sequences",
                                  command=(lambda: self.load_file("fwdseq", self.anacapa_dict)), width=20)

        self.mergeseqs = Button(self.anacapa_window, text="OTU/ASV Sequences",
                                  command=(lambda: self.load_file("mergeseq", self.anacapa_dict)), width=20)

        self.reverseseqs = Button(self.anacapa_window, text="OTU/ASV Sequences",
                                 command=(lambda: self.load_file("reverseseq", self.anacapa_dict)), width=20)

        self.rarefactiondepth = Entry(self.anacapa_window)
        self.rarefactioniter = Entry(self.anacapa_window)

        self.validate_submit = Button(self.anacapa_window, text="SUBMIT", command=(lambda: self.run_anacapa_fields()))

    def display_anacapa_fields(self):

        self.description.grid(row=0, column=0, columnspan=2, sticky=W)

        self.otutable_l.grid(row=1, column=0, sticky=W)
        self.otutable.grid(row=1, column=1)

        self.forwardseqs_l.grid(row=2, column=0, sticky=W)
        self.forwardseqs.grid(row=2, column=1)

        self.mergeseqs_l.grid(row=3, column=0, sticky=W)
        self.mergeseqs.grid(row=3, column=1)

        self.reverseseqs_l.grid(row=4, column=0, sticky=W)
        self.reverseseqs.grid(row=4, column=1)



        self.rarefactiondepth_l.grid(row=5, column=0, sticky=W)
        self.rarefactiondepth.grid(row=5, column=1)

        self.rarefactioniter_l.grid(row=6, column=0, sticky=W)
        self.rarefactioniter.grid(row=6, column=1)

        self.validate_submit.grid(row=7, column=1)

    def run_anacapa_fields(self):
        #TODO validate fields
        #TODO change box colors and display dictionary?
        self.anacapa_dict["rarefactiondepth"] = self.rarefactiondepth.get()
        self.anacapa_dict["rarefactioniter"] = self.rarefactioniter.get()
        print (self.anacapa_dict)
        new_anacapa = course_wrapper.Anacapa(self.anacapa_dict)

#############################################################################################################
#MR DNA


    def initiate_mrdna(self):
        self.mrdna_window = Toplevel()
        self.mrdna_window.title("MR DNA File Input")
        self.initiate_mrdna_labels()
        self.initiate_mrdna_fields()
        self.display_mrdna_fields()

    def initiate_mrdna_labels(self):

        self.description = Label(self.mrdna_window, text="This will be the description of the fields for the user.")

        self.otutable_l = Label(self.mrdna_window, text="OTU/ASV Table (fasta.otus.fa.OTU.txt file:")
        self.forwardseqs_l = Label(self.mrdna_window, text="OTU/ASV Sequences (.fasta format):")
        self.rarefactiondepth_l = Label(self.mrdna_window, text="Rarefaction Depth:")
        self.rarefactioniter_l = Label(self.mrdna_window, text="Rarefaction Iterations:")
	
    def initiate_mrdna_fields(self):
        self.mrdna_dict = self.get_new_file_dict()

        #TODO pass file types accepted
        self.otutable = Button(self.mrdna_window, text="OTU/ASV Table",
                               command=(lambda: self.load_file("otutable", self.mrdna_dict)), width=20)

        self.forwardseqs = Button(self.mrdna_window, text="OTU/ASV Sequences",
                                  command=(lambda: self.load_file("fwdseq", self.mrdna_dict)), width=20)


        self.rarefactiondepth = Entry(self.mrdna_window)
        self.rarefactioniter = Entry(self.mrdna_window)

        self.validate_submit = Button(self.mrdna_window, text="SUBMIT", command=(lambda: self.run_mrdna_fields()))

    def display_mrdna_fields(self):

        self.description.grid(row=0, column=0, columnspan=2, sticky=W)

        self.otutable_l.grid(row=1, column=0, sticky=W)
        self.otutable.grid(row=1, column=1)

        self.forwardseqs_l.grid(row=2, column=0, sticky=W)
        self.forwardseqs.grid(row=2, column=1)

        self.rarefactiondepth_l.grid(row=3, column=0, sticky=W)
        self.rarefactiondepth.grid(row=3, column=1)

        self.rarefactioniter_l.grid(row=4, column=0, sticky=W)
        self.rarefactioniter.grid(row=4, column=1)

        self.validate_submit.grid(row=5, column=1)

    def run_mrdna_fields(self):
        #TODO validate fields
        #TODO change box colors and display dictionary?
        self.mrdna_dict["rarefactiondepth"] = self.rarefactiondepth.get()
        self.mrdna_dict["rarefactioniter"] = self.rarefactioniter.get()
        print (self.mrdna_dict)
        new_anacapa = course_wrapper.MrDNA(self.mrdna_dict)

#############################################################################################################
#QIIME2


    def initiate_qiime2(self):
        self.qiime2_window = Toplevel()
        self.qiime2_window.title("QIIME2 File Input")
        self.initiate_qiime2_labels()
        self.initiate_qiime2_fields()
        self.display_qiime2_fields()

    def initiate_qiime2_labels(self):

        self.description = Label(self.qiime2_window, text="This will be the description of the fields for the user.")

        self.otutable_l = Label(self.qiime2_window, text="OTU/ASV Table from FeatureTable[Frequency] (table.biom)")
        self.taxonomy_l = Label(self.qiime2_window, text="Taxonomy TSV from FeatureData[Taxonomy] (taxonomy.tsv)")
        self.forwardseqs_l = Label(self.qiime2_window, text="OTU/ASV Sequences (.fasta format):")
        self.rarefactiondepth_l = Label(self.qiime2_window, text="Rarefaction Depth:")
        self.rarefactioniter_l = Label(self.qiime2_window, text="Rarefaction Iterations:")
	
    def initiate_qiime2_fields(self):
        self.qiime2_dict = self.get_new_file_dict()

        #TODO pass file types accepted
        self.otutable = Button(self.qiime2_window, text="FeatureTable[Frequency] Artifact",
                               command=(lambda: self.load_file("otutable", self.qiime2_dict)), width=30)
        self.taxonomy = Button(self.qiime2_window, text="FeatureData[Taxonomy] Artifact",
                               command=(lambda: self.load_file("taxonomy", self.qiime2_dict)), width=30)
        self.forwardseqs = Button(self.qiime2_window, text="OTU/ASV Sequences",
                                  command=(lambda: self.load_file("fwdseq", self.qiime2_dict)), width=30)


        self.rarefactiondepth = Entry(self.qiime2_window)
        self.rarefactioniter = Entry(self.qiime2_window)

        self.validate_submit = Button(self.qiime2_window, text="SUBMIT", command=(lambda: self.run_qiime2_fields()))

    def display_qiime2_fields(self):

        self.description.grid(row=0, column=0, columnspan=2, sticky=W)

        self.otutable_l.grid(row=1, column=0, sticky=W)
        self.otutable.grid(row=1, column=1)

        self.taxonomy_l.grid(row=2, column=0, sticky=W)
        self.taxonomy.grid(row=2, column=1)

        self.forwardseqs_l.grid(row=3, column=0, sticky=W)
        self.forwardseqs.grid(row=3, column=1)

        self.rarefactiondepth_l.grid(row=4, column=0, sticky=W)
        self.rarefactiondepth.grid(row=4, column=1)

        self.rarefactioniter_l.grid(row=5, column=0, sticky=W)
        self.rarefactioniter.grid(row=5, column=1)

        self.validate_submit.grid(row=6, column=1)

    def run_qiime2_fields(self):
        #TODO validate fields
        #TODO change box colors and display dictionary?
        self.qiime2_dict["rarefactiondepth"] = self.rarefactiondepth.get()
        self.qiime2_dict["rarefactioniter"] = self.rarefactioniter.get()
        print (self.qiime2_dict)
        new_qiime2 = course_wrapper.QIIME2(self.qiime2_dict)


    def get_file_set_dict(self, set_count):
        dict = {}
        for i in range(set_count):
            dict[i] = " "
        return dict

#########################################################################################
# PIPHILLIN
    #TODO
    def run_piphillin(self):
        pass

    def initiate_piphillin_fields(self, set_count):
        new_dict = {}
        for label in self.piphillin_window.grid_slaves():
            if int(label.grid_info()["row"]) in range(1, self.max_file_sets):
                label.grid_forget()
        for i in range(1, set_count+1):
            name = "otutable_" + str(i)
            new_dict[name] = Button(self.piphillin_window, text="KO Gene Table",
                                  command=(lambda: self.load_file(i, self.piphillin_dict)), width=20)
            name = "otutable_" + str(i) + "_l"
            new_dict[name] = Label(self.piphillin_window, text="Enter file #%s:" % i)

        for i in range(1, set_count+1):
            name = "otutable_" + str(i) + "_l"
            new_dict[name].grid(row=i, column=0, sticky=W)
            name = "otutable_" + str(i)
            new_dict[name].grid(row=i, column=1, stick=W)

        self.end_label = Label(self.piphillin_window, text="Enter as many files as the number you entered at the top of the screen")
        self.submit_piphillin = Button(self.piphillin_window, text="SUBMIT",
               command=(lambda: self.run_piphillin()), width=20)

        self.end_label.grid(row=i+1, column=0, columnspan=2)
        self.submit_piphillin.grid(row=i+1, column=3)



    def update_rows(self):

        self.number_1 = int(self.number_entry.get())
        self.piphillin_dict = self.get_file_set_dict(int(self.number_entry.get()))

        try:
            if self.number_2 is None:
                pass
        except:
            self.number_2 = None

        if self.number_1 != self.number_2:
            self.initiate_piphillin_fields(self.number_1)
            self.number_1 = self.number_2


    def initiate_piphillin(self):
        self.max_file_sets = 20

        self.piphillin_window = Toplevel()
        self.piphillin_window.title("Piphillin File Set Input")

        self.number_label = Label(self.piphillin_window, text="Enter file set #:")
        self.number_entry = Entry(self.piphillin_window)
        self.update_button = Button(self.piphillin_window, text="Update",
                                  command=(lambda: self.update_rows()), width=20)

        self.number_label.grid(row=0, column=0)
        self.number_entry.grid(row=0, column=1)
        self.update_button.grid(row=0, column=2)


##########################################################################################
#MAIN

    def initiate_main_fields(self):

        choices = ["Mr. DNA", "Anacapa", "QIIME2"]
        self.dropVar=StringVar()
        self.dropVar.set("Mr. DNA")
        self.main_label = Label(self, wraplength=500,
                                text="Below you will see options to connect various pipelines: \n "
                                            "ANACAPA \n "
                                            "QIIME2 \n"
                                            "MR. DNA \n"
                                            "\n"
                                            "Piphillin requires the use of a web browser for functional inference; \n"
                                            "therefore the files in the output folder in 'piphillin' will have to ran seperate. \n"
                                            "Once they have been ran you can see the input for those to retrieve the functional hierarchy below. \n"
                                            "If you would like any further pipelines supported please notify us using the github issues link: \n"
                                            "\t https://github.com/keithgmitchell/PUMA/issues ")
        self.main_choice_anacapa = Button(self, text="Anacapa", command=(lambda: self.initiate_ancapa()), width=20)

        #TODO edit the other views
        self.main_choice_qiime = Button(self, text="QIIME2", command=(lambda: self.initiate_qiime2()), width=20)
        self.main_choice_mrdna = Button(self, text="Mr. DNA", command=(lambda: self.initiate_mrdna()), width=20)

        self.space = Label(self, text = " ")
        self.main_label2 = Label(self, wraplength=500,
                                 text="Below you will see additional options in order to produce Funtional Hierarchy after running Piphillin or "
                                      "Make OTU Networks for Cytoscape which will require your metadata to be verified using the provided steps.")

        self.main_choice_functional = Button(self, text="Functional Hierarchy", command=(lambda: self.initiate_piphillin()), width=20)
        self.main_choice_cytoscape = Button(self, text="Cytoscape", command=None, width=20)

    def display_main_fields(self):

        self.main_label.grid(row=0, column=0, columnspan=3, sticky=W)
        self.main_choice_anacapa.grid(row=1, column=0, sticky=W)
        self.main_choice_qiime.grid(row=1, column=1, sticky=W)
        self.main_choice_mrdna.grid(row=1, column=2, sticky=W)

        self.space.grid(row=2)
        self.space.grid(row=3)
        self.main_label2.grid(row=4, column =0, columnspan=3, sticky=W)
        self.main_choice_functional.grid(row=5, column=0, columnspan=1, sticky=W)
        self.main_choice_cytoscape.grid(row=5, column=1, columnspan=1, sticky=W)


    def change_theme(self, theme):

        self.s.theme_use(theme)
        print(self.s.theme_use())

    ##########################################################################################



    def __init__(self):
        # s=ttk.Style()
        # s.theme_use('alt')
        # s.theme_use()
        self.s = ttk.Style()
        Frame.__init__(self)
        self.change_theme('clam')
        self.master.title("PUMA - Pipeline for Undergraduate Microbiome Analysis")
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)
       
        self.initiate_main_fields()
        self.display_main_fields()



if __name__ == "__main__":
    PUMA().mainloop()

