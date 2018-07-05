# PUMA
## Pipeline for Undergraduate Microbiome Analysis

### Requirements (on the QIIME2 VM)
+ Biopython-1.71

## TODO

+ Test piphillin script in STAMP
+ Test piphillin scenario with merge files
+ Decide how to incorporate Metadata 
+ Cytoscape script
+ Run testing in computer lab
+ file validation
+ double check logic everywhere to be sure we handle no rarefaction option fine

## functional_profile.py

**For usage from files from Piphillin to create functional hierarchy and append gene descriptions to IDs.**

1. This function will also be ran on the hoffman cluster, but it may not need an actual qsub since it should be fairly quick.

2. Type ```module load python`` first. 

3. Help: 
```python functional_profile.py --help```

4. Example run:
```python functional_profile.py -i 109BL-W18_ko_abund_table_unnorm_90cutoff_assigned.txt -o 109BL-W18_90cutoff```

5. The output with the suffix `_genedes.txt` may contain "None" for a few of the gene descriptions, which may cause the programs to crash. So it may be best to delete these rows but it is at the liberty of the user to emit this data.

6. The output with the suffix `_pathway_hierarchy_table.txt` may contain "" (empty string) for a few of the pathway level descriptions, which may cause the programs to crash. So it may be best to delete these rows but it is at the liberty of the user to emit this data.


## course_wrapper.sh

**This is to be ran at the start of the quarter to have all files prepared, see step 3 for files needed.**

1. This shell script will produce the following files using the Hoffman cluster: rarefied taxonomy ASV file for STAMP, rarefied taxonomy ASV .biom file to import to QIIME2, rarefied real_edge_table.txt for use in Cytoscape, representative sequence file for Piphillin, rarefied sequence ID ASV table for Piphillin, metagenomic phylogenetic tree constructed from the representative sequence file for Piphillin to import into QIIME2, rarefied sequence ID ASV .biom table to import in QIIME2. Basically all that you should need to worry about is the metadata.

2. Run ```chmod +x course_wrapper.sh``` to create an executable.

3. Type ```./course_wrapper.sh``` to get help regarding parameter input. You will see the only files needed should be the ```16S_ASV_raw_taxonomy.txt```, ```nochim_forward16S.fasta```, ```nochim_merged16S.fasta```, and ```nochim_reverse16S.fasta```. 

4. Example run:
```./piphillin.sh PATH/16S_ASV_raw_taxonomy_70.txt PATH/nochim_forward16S.fasta PATH/nochim_merged16S.fasta PATH/nochim_reverse16S.fasta 5```

5. It is likely that this may take some time to build phylogenetic trees with many sequences so I suggest running a qsub, for example:
```qsub -cwd -V -N S18_Files -l h_data=12G,h_rt=24:00:00 -M $USER PATH/ ./piphillin.sh PATH/16S_ASV_raw_taxonomy_70.txt PATH/nochim_forward16S.fasta PATH/nochim_merged16S.fasta PATH/nochim_reverse16S.fasta 3500 5 ``` You can then look at the output files for this job to make sure everything ran ok, from the directory you ran the job type: ```cat JobName.o######``` where the number is the number of the job when you submitted it.

6. If you would like to monitor the job as it progresses then type ```qrsh h_data=12G``` and run the command from step 4. 

## stamp.py

1. This will be ran as a part of the shell script ```course_wrapper.sh```


## piphillin.py

1. This will be ran as a part of the shell script ```course_wrapper.sh```




