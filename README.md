# PUMA (Pipeline for Undergraduate Microbiome Analysis)

![PUMA GENERAL FLOWCHART](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_flowchart.PNG)


# Version 1.1 (current)
+ The Manual provided below will provide setup instructions as well as important tutorials for 
students/researchers for jumpstarting the analysis process with the various tools shown in the 
schema above.

##How to install:

+ Follow the protocol for PUMA Environment Setup Instructions using a VM at the following
**manual Link**: https://app.box.com/file/306629203695
+ The VM will also double as an environment to run the QIIME2 program:)


##How to run:
Results from running the PUMA scripts will produce output in the directory ‘output/’, 
or a specified output directory, with a prefix for the time the job was completed YEAR_MONTH_DAY_HOUR_MINUTE 
as well as a descriptive suffix such as ‘functional_profile’, ‘anacapa’, ‘MrDNA’, or ‘QIIME 2’ such as that 
shown in the Protocol sections. In addition; the CLI version provides the option for a user to specify an additional 
unique string to enable automation and parallel processing.
+ Running Anacapa Data:

        `python PumaCLI.py -otutable examples/anacapa_skirball_S18/16S_ASV_raw_taxonomy_70.tsv 
        -fwdseq examples/anacapa_skirball_S18/nochim_forward16S.fasta 
        -mergeseq examples/anacapa_skirball_S18/nochim_merged16S.fasta 
        -reverseseq examples/anacapa_skirball_S18/nochim_reverse16S.fasta 
        -rarefactioniter 3 -rarefactiondepth 3500 -metadata examples/metadata/anacapa_skirball_metadata_3_11_18.tsv 
        -type anacapa -unique_id demo -msa_phylo True`

+ Running MrDNA example data:

        `python PumaCLI.py -type MrDNA -metadata examples/metadata/mrdna_F15_mock_metadata.tsv 
        -otutable examples/mrdna_F15/112415KR515F-pr.fasta.otus.fa.OTU.txt 
        -seqs examples/mrdna_F15/sequences.fasta`
        
+ Running the Functional Profile following input of file sets to piphillin ():  

        `python functional_profile.py 
        -i examples/piphillin/Keith_20180723210057.tar,examples/piphillin/Keith_20180723214258.tar 
        -o UCLA -metadata examples/metadata/anacapa_skirball_metadata_3_11_18.tsv`      

+ Or use the GUI (keep terminal open to ):
        `python RunPuma.py`
![PUMA GENERAL FLOWCHART](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_GUI.PNG)




# Version 1.2 (In progress)
+ Introduced Command Line Interface Version for systems with QIIME2/Musket for automizing GUI process for those 
interested as well as to provide non Virtual Machine version for convenient Linux systems downloads. 
+ Automated Rarefaction Depth Option
+ Capability to select output files (rather then produce all mentioned)
+ Add full functionality for automating production of MSA/phylogenetic tree.
+ Better error log

## Future Additions
+ Include more tools such as the iTOL tool and any other requested (please create Issue if you have one in mind)
+ Include more file input types from other sequencing services (please create Issue if you have one in mind)
+ Bioconda package installation for non-VM based environments.

#### NEAR FUTURE:
+ clean up gui
+ upload standard otu and seqs
+ iPath formatted file??
+ Test piphillin script in STAMP
+ Test piphillin scenario with merge files
+ test cli on hoffman and dependencies
+ double check with caledna and mrdna for standard format

#### FEATURES
+ add rarefaction_depth/iter_ to the file names?
+ add zymo and change everything to caledna, remove ranacapa/talk to guarav???
+ make functional file for ranacapa?