# PUMA (Pipeline for Undergraduate Microbiome Analysis)
+ The Manual provided below will provide setup instructions as well as important tutorials for students/researchers for jumpstarting the analysis process with the various tools shown in the schema below.

![PUMA GENERAL FLOWCHART](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_flowchart.PNG)

### Version 1.1
+ **Manual Link**: https://app.box.com/file/306629203695
+ Added timestamps to all files produced in the pipeline to the output folder

### Version 1.2 (In progress)
+ Introduced Command Line Interface Version for systems with QIIME2/Musket for automizing GUI process for those 
interested as well as to provide non Virtual Machine version for convenient Linux systems downloads. 
+ Automated Rarefaction Depth Option
+ Capability to select output files (rather then produce all mentioned)
+ Add full functionality for automating production of MSA/phylogenetic tree.
+ Cytoscape script


### Future Additions
+ Include more tools such as the iTOL tool and any other requested (please create Issue if you have one in mind)
+ Include more file input types from other sequencing services (please create Issue if you have one in mind)



## Notes for Developers
### TODO

TESTING
+ Test piphillin script in STAMP
+ Test piphillin scenario with merge files
+ test cli on hoffman and dependencies
+ double check with caledna and mrdna for standard format

FEATURES
+ no rarefaction option
+ remove all temp files/clean folder and also have more subdirectories for parallel processing
+ accept the tar file for the piphillin part
+ add rarefaction_depth/iter_ to the file names
+ add zymo and change everything to caledna, remove ranacapa/talk to guarav???
+ make functional file for ranacapa
+ make default submission option for those from other platforms
