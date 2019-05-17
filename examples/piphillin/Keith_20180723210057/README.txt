
README - Piphillin version 6.0

The Piphillin algorithm
In the Piphillin algorithm, genome contents are predicted for each OTU. In order to transform
the OTU abundance table into a genome abundance table, the representative sequence of each OTU
(query) is searched against a database composed of 16S rRNA sequences using USEARCH v8.1.1861
with fixed sequence identity cutoff (see below).  A genome that has the closest matched 16S
rRNA sequence above the identity cutoff is considered as the inferred genome for that OTU. If
there are more than one nearest-neighbor genomes with equal identities, the count is equally
split among those genomes. The resulting genome abundance table is adjusted according to the 16S rRNA
copy number of each genome. Then, genome content is inferred by the copy number of the genes
within each inferred genome. Finally, inferred genome content of each genome bin is summed to
generate total metagenomics content of the sample.  Content is expressed in terms of ortholog
and pathway counts when using the KEGG genome database or RXN counts when using the BioCyc
genome database.

The abundance tables calculated by Piphillin contain floating point values due to split counts for 
multiple tied genome matches and due to ratios in 16S copy number to functional gene copy number. If the
downstream analysis requires integer values in the abundance table, e.g. when using DESeq2, we
recommend to use R's "floor" function to round the floating point values to the next lower
integer.  Also keep in mind that column sums (library sums) are not scaled to be equal and 
therefore we've added 'unnorm' to the file names.


Result files
(Depending on the selection on the Piphillin website, either one of the two folders or both can
be present in the downloadable zip file)

Folder biocyc_output
	rxn_abund_table_unnorm.txt		- 	BioCyc reaction abundance table

Folder kegg_output
	ko_abund_table_unnorm.txt		- 	KEGG KO abundance table 
	pathway_abund_table_unnorm.txt 	- 	KEGG pathway abundance table 



Please cite the following article when using Piphillin:
Iwai, S., Weinmaier, T., Schmidt, B., Albertson, D., Poloso, N., Dabbagh, K., DeSantis,
T., Piphillin: Improved Prediction of Metagenomic Content by Direct Inference from Human Microbiomes.
PLoS One. 2016 Nov 7;11(11):e0166104. doi: 10.1371/journal.pone.0166104. PMID: 27820856


For questions, suggestions or bug reports please contact us at Piphillin@secondgenome.com