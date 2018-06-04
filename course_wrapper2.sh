#to be ran on the hoffman cluster 

#!/bin/bash

#NOTE: talk to piphillin about accept zip files for the fasta sequences.
if [ $# -lt 6 ]
then
echo "********************************************************************"
echo "Script was written for PUMA pipeline to create all files."
echo "This script was written by Keith Mitchell"
echo "To be ran on an environment with QIIME2."
echo "********************************************************************"
echo ""
echo "1 <otutable>          - Ex: PATH/16S_ASV_raw_taxonomy_70.txt"
echo "2 <fwdseq>            - Ex: PATH/nochim_forward16S.fasta"
echo "3 <mergeseq>          - Ex: PATH/nochim_merged16S.fasta"
echo "4 <reverseseq>        - Ex: PATH/nochim_reverse16S.fasta"
echo "5 <rarefactiondepth>             - Ex: 3500"
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


#take arguments
#should we specify an outdirectory ??????????????????????????????????????
# otutable=$1
# fwdseq=$2
# mergseq=$3
# revseq=$4
# rarefactiondepth=$5
# rarefactioniter=$6


otutable="/media/sf_QIIME/Emily_Test/16S_ASV_raw_taxonomy_70.txt"
fwdseq="/media/sf_QIIME/Emily_Test/nochim_forward16S.fasta"
mergeseq="/media/sf_QIIME/Emily_Test/nochim_merged16S.fasta"
revseq="/media/sf_QIIME/Emily_Test/nochim_reverse16S.fasta"
rarefactiondepth=3500
#TODO if rarefaction is 0 then be sure to include that logic
rarefactioniter=3


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
otucleaned=${otucleaned##*/}
echo "Otucleaned: $otucleaned"
otubiom=${otucleaned}.biom
echo "Otubiom: $otubiom"


biom convert -i $otutable -o $otubiom --table-type="OTU table" --to-json


echo "----------------------------------------------------------------------------------"
echo "3. Making Rarefactions of the .biom->.qza file and create list of rarefactions"
echo "----------------------------------------------------------------------------------"

echo ""
raredir=${otutable%.txt}"_rarefactions/"
echo "Making directory for the rarefactions."
mkdir $raredir

echo ""
echo "Importing the .biom table and converting to .qza"
qiime tools import \
  --input-path $otubiom \
  --type 'FeatureTable[Frequency]' \
  --source-format BIOMV100Format \
  --output-path ${otucleaned}.qza

echo ""
if [[ $rarefactioniter != 0 ]]; then
	rm $otubiom
	echo "Removing the original .biom file $otubiom"
fi 

otuqza=${otucleaned}.qza
echo ""
for ((i=1; i<=$rarefactioniter; i++)); do
	echo "Making rarefaction ${raredir}${otucleaned}_${i}.qza"
	qiime feature-table rarefy \
      --i-table $otuqza \
      --p-sampling-depth $rarefactiondepth \
      --o-rarefied-table ${raredir}${otucleaned}_${i}
done

for item in $raredir*;
do	
	if [[ $item == *"1.qza"* ]]; then 
		echo "Rarefaction: $item was found"
		mergerarefactions="--i-tables $item"
	fi		
done

for item in $raredir*;
do
	if [[ $item != *"1.qza"* ]]; then 
		echo "Rarefaction: $item was found"
		mergerarefactions="$mergerarefactions --i-tables $item"
	fi
done

echo ""
echo "Merged Rarefaction String: $mergerarefactions"

echo "----------------------------------------------------------------------------------"
echo "4. Merging Rarefactions of the .qza file"
echo "----------------------------------------------------------------------------------"


mergedfile=$otucleaned"_rarefaction_merged_X"$rarefactioniter".qza"

qiime feature-table merge \
  $mergerarefactions \
  --p-overlap-method sum \
  --o-merged-table $mergedfile

rm -r $raredir
echo "Rarefaction files and directory were removed."


echo "----------------------------------------------------------------------------------"
echo "5. Convert the .qza->.biom->TSV, remove top row, change '#OTU ID' to 'OTU'"
echo "----------------------------------------------------------------------------------"

mergedbiom=${mergedfile%.qza}.biom
mergedtext=${mergedfile%.qza}.txt

echo ""
echo "Converting $mergedfile to $mergedbiom"
qiime tools export $mergedfile --output-dir $mergedbiom

echo ""
echo "Converting $mergedbiom to mergedtext"
biom convert -i $mergedbiom -o $mergedtext --to-tsv


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
allfasta=$all_16S.fasta
cat $fwdseq $mergeseq $revseq > $allfasta

echo ""
echo "All ASV Reads"
head -10 $allfasta
echo ""


echo "Averaging the file and rounding based on the nubmer of iterations."
echo "Then splitting the files so they are not to large for Piphillin."
echo ""

# make a directory for the piphillin stuff specifically???
roundedtext="averaged_"$mergedtext
piphillinseqs="sequences_from_averaged.fasta"
python2 piphillin.py -input $mergedtext -output $roundedtext -iter $rarefactioniter -all_seqs $allfasta -seq_output $piphillinseqs


echo ""
echo "Averaged File"
head -10 $roundedtext

echo ""
echo "Filtered Sequences"
head -10 $piphillinseqs

echo "You can now go to the directory "piphillin" and begin running those file sets."