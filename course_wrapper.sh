#to be ran on the hoffman cluster 

#!/bin/bash

#NOTE: talk to piphillin about accept zip files for the fasta sequences.
if [ $# -lt 6 ]
then
echo "********************************************************************"
echo "Script was written for 109BL course pipeline to create all files."
echo "This script was written by Keith Mitchell"
echo "********************************************************************"
echo ""
echo "1 <otutable>          - Ex: PATH/16S_ASV_raw_taxonomy_70.txt"
echo "2 <fwdseq>            - Ex: PATH/nochim_forward16S.fasta"
echo "3 <mergeseq>          - Ex: PATH/nochim_merged16S.fasta"
echo "4 <reverseseq>        - Ex: PATH/nochim_reverse16S.fasta"
echo "5 <depth>             - Ex: 3500"
echo "6 <rarefactioniter>   - Ex: 5"
echo "--------------------------------------"
echo " If you need to find the path to where you have the file stored then"
echo " just type 'pwd' in the directory of interest."
echo ""
echo " You may want to be sure that the OTU table as input (16S_ASV_raw_taxonomy) has"
echo " the same sample names as the metadata so you dont have to change all the files later."
echo ""
echo " Be sure that the otutable has '16S_seq_number' in the first column."
echo " Be sure that the otutable has 'sum taxonomy' in the last column."
#exit 1	
fi

#activate the qiime interpreter
. /u/local/Modules/default/init/modules.sh
module load anaconda
source activate qiime1

#take arguments
#should we specify an outdirectory ??????????????????????????????????????
# otutable=$1
# fwdseq=$2
# mergseq=$3
# revseq=$4
# rarefactiondepth=$5
# rarefactioniter=$6


otutable=16S_ASV_raw_taxonomy_70.txt
fwdseq=nochim_forward16S.fasta
mergeseq=nochim_merged16S.fasta
revseq=nochim_reverse16S.fasta
rarefactiondepth=3500
rarefactioniter=10

msa=pynast
phy=fasttree


echo "----------------------------------------------------------------------------------"
echo "1. Fix Header Row for creating .biom table"
echo "----------------------------------------------------------------------------------"

head -1 $otutable

#also we need to change the line in the header row here
sed -i -e 's/16S_seq_number\t/#OTU ID\t/g' $otutable
echo ""

head -1 $otutable

echo "----------------------------------------------------------------------------------"
echo "2. Creating .biom table"
echo "----------------------------------------------------------------------------------"

otucleaned=${otutable%.txt}
otubiom=$otucleaned.biom

echo "FYI: you may get a FutureWarning, but it is harmless (https://stackoverflow.com/a/48774337/7305166)"
echo ""

biom convert -i $otutable -o $otubiom --table-type="OTU table" --to-json


echo "----------------------------------------------------------------------------------"
echo "3. Making Rarefactions of the .biom file and create list of rarefactions"
echo "----------------------------------------------------------------------------------"

echo "FYI: you may get a FutureWarning, but it is harmless (https://stackoverflow.com/a/48774337/7305166)"
echo ""

raredir=$otucleaned"_rarefactions/"
mkdir $raredir

multiple_rarefactions_even_depth.py -i $otubiom -o $raredir -n $rarefactioniter -d $rarefactiondepth


echo ""
rm $otubiom
echo "Removing the original .biom file $otubiom"

for item in $raredir*;
do	
	if [[ $item == *"0.biom"* ]]; then 
		echo "Rarefaction: $item was found"
		mergerarefactions=$item
	fi		
done

for item in $raredir*;
do
	if [[ $item != *"0.biom"* ]]; then 
		echo "Rarefaction: $item was found"
		mergerarefactions=$mergerarefactions,$item
	fi
done

echo "Merged Rarefaction String: $mergerarefactions"

echo "----------------------------------------------------------------------------------"
echo "4. Merging Rarefactions of the .biom file"
echo "----------------------------------------------------------------------------------"

# Does Qiime 2 do this automatically????? Actually Curious?????????? should eventually make this qiime2 compatable
echo "FYI: you may get a FutureWarning, but it is harmless (https://stackoverflow.com/a/48774337/7305166)"
echo ""

mergedfile=$otucleaned"_rarefaction_merged_X"$rarefactioniter".biom"

merge_otu_tables.py -i $mergerarefactions -o $mergedfile
echo "The merged file $mergedfile was created."

rm -r $raredir
echo "Rarefaction files and directory were removed."

echo "----------------------------------------------------------------------------------"
echo "5. Convert the .biom table to TSV, remove top row, change '#OTU ID' to 'OTU'"
echo "----------------------------------------------------------------------------------"

# is this ok?? do we need t specify any further full directories.???????????????????????????????????????????
mergedtext=${mergedfile%.biom}.txt
echo "Converting $mergedfile to $mergedtext"
echo "FYI: you may get a FutureWarning, but it is harmless (https://stackoverflow.com/a/48774337/7305166)"
echo ""
biom convert -i $mergedfile -o $mergedtext --to-tsv


echo "----------------------------------------------------------------------------------"
echo "6. Average the ASV table and filter all sequences with piphillin.py"
echo "----------------------------------------------------------------------------------"
echo "This will create proper files for input to Piphillin (check .fasta size and split)"
echo "These files may be large since we take 10 rarefactions and just take the average."
echo "Due to this there may be multiple sets of files to run in Piphillin (about 2 or 3)" 

echo ""
head -2 $mergedtext
echo ""

echo "Getting Rid of the '# Constructed from biom file'"
sed -i '/# Constructed from biom file/d' $mergedtext
echo ""
head -2 $mergedtext
echo ""

echo "Making the '#OTU ID' into 'OTU'"
sed -i -e 's/#OTU ID\t/OTU\t/g' $mergedtext
echo ""
head -5 $mergedtext
echo ""


echo "Merging all the ASV reads together"
allfasta=$all_16S_ASV.fasta
cat $fwdseq $mergeseq $revseq > $allfasta

echo ""
echo "All ASV Reads"
head -10 $allfasta
echo ""

. /u/local/Modules/default/init/modules.sh
module load python

echo "Averaging the file and rounding based on the nubmer of iterations."
echo "Then splitting the files so they are not to large for Piphillin."
echo ""

# make a directory for the piphillin stuff specifically???
roundedtext="averaged_"$mergedtext
piphillinseqs="sequences_from_averaged.fasta"
python piphillin.py -input $mergedtext -output $roundedtext -iter $rarefactioniter -all_seqs $allfasta -seq_output $piphillinseqs


echo ""
echo "Averaged File"
head -10 $roundedtext

echo ""
echo "Filtered Sequences"
head -10 $piphillinseqs

echo "You can now go to the directory "piphillin" and begin running those file sets."

echo "----------------------------------------------------------------------------------"
echo "7. Create a MSA Alignment with QIIME1 with ALL sequences for Piphillin(rarefied)"
echo "----------------------------------------------------------------------------------"
echo "This might take a while since we have a lot of sequences due to the way we average the files."

echo "Performing the MSA with PyNast: (do you want to be able to specify this?)
msaout=$msa_aligned

align_seqs.py -i $piphillinseqs -m $msa -o $msaout


echo "----------------------------------------------------------------------------------"
echo "8. Create a Phylogenetic Tree to import to QIIME2 from result of step 7(rarefied)."
echo "----------------------------------------------------------------------------------"
echo "This might take a while since we have a lot of sequences due to the way we average the files."
echo ""

echo "Building Phylogenetic tree with FastTree: (do you want to be able to specify this?)

phyout=$phy_phylogeny_QIIME2.tre
make_phylogeny.py -i $msaout/$piphillinseqs_aligned.fasta -m $phy -o $phyout

echo "Done Building the Phylogenetic Tree"

echo ""
echo "----------------------------------------------------------------------------------"
echo "9. Create a .biom file from averaged file from Step 6 to import to QIIME2(rarefied)."
echo "----------------------------------------------------------------------------------"
echo "This file will be an OTU table with sequence ID's in the first column."
echo "This will enable student to perform alpha/beta diversity analysis based on the phylogenetic tree."
echo ""
echo "FYI: you may get a FutureWarning, but it is harmless (https://stackoverflow.com/a/48774337/7305166)"
echo ""
echo ""

echo "Making the 'OTU' into '#OTU ID'"
sed -i -e 's/OTU\t/#OTU ID\t/g' $roundedtext

biom convert -i $roundedtext -o $roundedtext_QIIME2 --table-type="OTU table" --to-json
echo ""

echo "----------------------------------------------------------------------------------"
echo "10. Create a File Use in STAMP(rarefied)."
echo "----------------------------------------------------------------------------------"

stamp=$otutable_STAMP_$rarefactiondepth
python stamp.py -input $otutable -output $stamp -rarefied $roundedtext -output_2


echo "DONE"


