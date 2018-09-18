# PUMA (Pipeline for Undergraduate Microbiome Analysis)

![PUMA GENERAL FLOWCHART](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_flowchart.PNG)


## Version 1.1 (current)
+ The Manual provided below will provide setup instructions as well as important tutorials for 
students/researchers for jumpstarting the analysis process with the various tools shown in the 
schema above.
+ **Manual Link**: https://app.box.com/file/306629203695

###How to install/dependencies:

+ Using virtual machine:
+ Using conda


+ QIIME2
+ MAFFT (multiple sequence aligner)
+ Python 3.5 +
    + biopython
    + argparse
    + csv

###How to run:

+ `python PumaCLI.py -otutable examples/anacapa_skirball_S18/16S_ASV_raw_taxonomy_70.tsv 
-fwdseq examples/anacapa_skirball_S18/nochim_forward16S.fasta 
-mergeseq examples/anacapa_skirball_S18/nochim_merged16S.fasta 
-reverseseq examples/anacapa_skirball_S18/nochim_reverse16S.fasta 
-rarefactioniter 3 -rarefactiondepth 3500 -metadata examples/metadata/anacapa_skirball_metadata_3_11_18.tsv 
-type anacapa -unique_id demo -msa_phylo True`


+  How to run:

## Version 1.2 (In progress)
+ Introduced Command Line Interface Version for systems with QIIME2/Musket for automizing GUI process for those 
interested as well as to provide non Virtual Machine version for convenient Linux systems downloads. 
+ Automated Rarefaction Depth Option
+ Capability to select output files (rather then produce all mentioned)
+ Add full functionality for automating production of MSA/phylogenetic tree.
+ Cytoscape script
+ CLI for scripts seperately 


### Future Additions
+ Include more tools such as the iTOL tool and any other requested (please create Issue if you have one in mind)
+ Include more file input types from other sequencing services (please create Issue if you have one in mind)


## Notes for Developers
### TODO
NOW
+ clean up gui
+ upload standard otu and seqs
+ Ranacapa output folder
+ verified metadata in output directory(double check)
+ test on the aws
+ upload .yml file?
+ iPath formatted file??

TESTING
+ Test piphillin script in STAMP
+ Test piphillin scenario with merge files
+ test cli on hoffman and dependencies
+ double check with caledna and mrdna for standard format

FEATURES
+ add rarefaction_depth/iter_ to the file names?
+ add zymo and change everything to caledna, remove ranacapa/talk to guarav???
+ make functional file for ranacapa?