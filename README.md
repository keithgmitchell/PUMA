# PUMA (Pipeline for Undergraduate Microbiome Analysis)

# Version 1.1 (current)
+ The Manual provided below will provide setup instructions as well as important tutorials for 
students/researchers for jumpstarting the analysis process with the various tools shown in the 
schema above.

## How to install:

1. Follow the steps (steps 1-6 but optional steps are nice to have as well) here https://docs.qiime2.org/2018.11/install/virtual/virtualbox/
+ Currently tested with the 2018.8 version of the virtual machine. (https://data.qiime2.org/distro/core/2018.8)

2. The VM will also double as an environment to run the QIIME2 program.
3. Run `git clone https://github.com/keithgmitchell/PUMA.git` by opening terminal in the folder of your choice.
4. For the CLI and the GUI run `python PumaCLI.py --help` and `python RunPuma.py` respectively.


## How to run:
Results from running the PUMA scripts will produce output in the directory ‘output/’, 
or a specified output directory, with a prefix for the time the job was completed YEAR_MONTH_DAY_HOUR_MINUTE 
as well as a descriptive suffix such as ‘functional_profile’, ‘anacapa’, ‘MrDNA’, or ‘QIIME 2’ such as that 
shown in the Protocol sections. In addition; the CLI version provides the option for a user to specify an additional 
unique string to enable automation and parallel processing.

Be sure all sample names in the metadata and in the ASV/OTU table are matching an are only alphanumeric titles.
+ Running Anacapa Data:

        python PumaCLI.py -otutable examples/anacapa_skirball_S18/16S_ASV_raw_taxonomy_70.tsv \
        -fwdseq examples/anacapa_skirball_S18/nochim_forward16S.fasta \
        -mergeseq examples/anacapa_skirball_S18/nochim_merged16S.fasta \
        -reverseseq examples/anacapa_skirball_S18/nochim_reverse16S.fasta \
        -rarefactioniter 3 -rarefactiondepth 3500 -metadata examples/metadata/anacapa_skirball_metadata_3_11_18.tsv \
        -type anacapa -unique_id demo -msa_phylo True

+ Running MrDNA example data:

        python PumaCLI.py -type MrDNA -metadata examples/metadata/mrdna_F15_mock_metadata.tsv \
        -otutable examples/mrdna_F15/112415KR515F-pr.fasta.otus.fa.OTU.txt \
        -seqs examples/mrdna_F15/sequences.fasta
        
+ Running the Functional Profile following input of file sets from piphillin:  

        python functional_profile.py \
        -i examples/piphillin/Keith_20180723210057.tar,examples/piphillin/Keith_20180723214258.tar \
        -o UCLA -metadata examples/metadata/anacapa_skirball_metadata_3_11_18.tsv      

+ Or use the GUI (keep terminal open to see system feedback):
        python RunPuma.py
![PUMA GENERAL FLOWCHART](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_GUI.PNG)




## Version 1.2 (In progress)
+ Introduced Command Line Interface Version for systems with QIIME2/Musket for automizing GUI process for those 
interested as well as to provide non Virtual Machine version for convenient Linux systems downloads. 
+ Automated Rarefaction Depth Option
+ Capability to select output files (rather then produce all mentioned)
+ Add full functionality for automating production of MSA/phylogenetic tree.
+ Better error log/system output filing 
+ Include more tools such as the iTOL tool and any other requested (please create Issue if you have one in mind)
+ Include more file input types from other sequencing services (please create Issue if you have one in mind)
+ Bioconda package installation for non-VM based environments.

### NEAR FUTURE:
+ install dependencies on running the CLI
+ clean up gui
+ upload standard otu and seqs
+ Test piphillin script in STAMP
+ test cli on hoffman and dependencies
+ double check with caledna and mrdna for standard format
+ add rarefaction_depth/iter_ to the file names
