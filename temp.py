import course_wrapper

files_dictionary = {"otutable": '/media/sf_QIIME/Emily_Test/16S_ASV_raw_taxonomy_70.txt',
                    "fwdseq": '/media/sf_QIIME/Emily_Test/nochim_forward16S.fasta',
                    "reverseseq": '/media/sf_QIIME/Emily_Test/nochim_reverse16S.fasta',
                    "mergeseq": '/media/sf_QIIME/Emily_Test/nochim_merged16S.fasta',

                    # "allseqs": '/media/sf_QIIME/Emily_Test/16S_ASV_raw_taxonomy_70.txt',

                    "rarefactiondepth": 3500,
                    "rarefactioniter": 2}

anacapa_test = course_wrapper.Anacapa(files_dictionary)