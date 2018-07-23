# PUMA (Pipeline for Undergraduate Microbiome Analysis)
+ The Manual provided below will provide setup instructions as well as important tutorials for students/researchers for jumpstarting the analysis process with the various tools shown in the scema below

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
+ Automation of the cytoscape portion of the pipeline so it is not its own uploading process.

### Future Additions
+ Include more tools such as the iTOL tool and any other requested (please create Issue if you have one in mind)
+ Include more file input types from other sequencing services (please create Issue if you have one in mind)

## Notes for Developers
### TODO
+ Test piphillin script in STAMP
+ Test piphillin scenario with merge files
+ Decide how to incorporate Metadata 
+ Cytoscape script
+ Run testing in computer lab
+ double check logic everywhere to be sure we handle no rarefaction option fine
+ remove all temp files/clean folder and also have more subdirectories for parallel processing
+ accept the tar file for the piphillin part