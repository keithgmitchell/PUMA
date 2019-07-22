# PUMA (Pipeline for Unifying Microbiome Analysis) (Version 1.2)
Pre-print: https://doi.org/10.1101/482380
+ The Manual provided below will provide setup instructions as well as important tutorials for 
students/researchers for jumpstarting the analysis process with the various tools shown in the 
schema above.
    + Manual: https://app.box.com/file/358362942079

## How to install: (MacOSx and Linux supported)

1. Install Conda for your operating system (https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
2. Run `git clone https://github.com/keithgmitchell/PUMA.git` by opening terminal in the folder of your choice.
3. `conda config --append channels conda-forge`; `conda config --append channels bioconda`
4. `conda create -n puma_env --file requirements.txt`
    - If you encounter 
    - Be sure to select "Yes" by clicking "y" when prompted. 
    - This may take 15-20 mins. 
5. `conda activate puma_env`
6. `pip install -r pip_requirements.txt`
7. For the CLI and the GUI run `python PumaCLI.py --help` and `python puma/RunPuma.py` respectively.


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
        
+ Running the Functional Profile following input of file sets to piphillin (https://piphillin.secondgenome.com/):  

        python functional_profile.py \
        -i examples/piphillin/Keith_20180723210057.tar,examples/piphillin/Keith_20180723214258.tar \
        -o UCLA -metadata examples/metadata/anacapa_skirball_metadata_3_11_18.tsv      

+ Or use the GUI (keep terminal open to see system feedback):
        `python RunPuma.py`
        
        
![PUMA GENERAL FLOWCHART Version 1.1](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_GUI.PNG)
![PUMA GENERAL FLOWCHART Version 1.2](https://github.com/keithgmitchell/PUMA/blob/master/examples/PUMA_GUI_1.2)


## Version 1.3 (In progress)
+ Automated Rarefaction Depth Option
+ Capability to select output files (rather then produce all mentioned)
+ Include more tools such as the iTOL tool and any other requested (please create Issue if you have one in mind)
+ Include more file input types from other sequencing services (please create Issue if you have one in mind)
+ Fix the anacapa input functions.
+ Add picrust 2.0
+ Add merge files option that includes the metadata. 
+ upload standard otu and seqs
+ add rarefaction_depth/iter_ to the file names
+ double check that no rarefaction option still works
+ fix background process
+ finish piphillin view and logging

### NEAR FUTURE:
