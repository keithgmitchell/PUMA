import csv

def metadata_to_dict(metdata):
    """
    :param metdata: file path
    :return: dict of lists regarding the metadata information, header row
    """
    with open(metdata) as metadata_file:
        sample_dict = {}
        metadata_read = csv.reader(metadata_file, delimiter='\t')
        header = metadata_read.__next__()
        for line in metadata_read:
            sample_dict[line[0]] = line[1:len(line)]

    # print (sample_dict, header)
    return sample_dict, header[1:len(header)]


# def handle_files(standard_otu, metadata, outdir, time_id, type):
def handle_files(standard_otu, metadata, outfile, end_pos):
    """
    :param standard_otu: file path
    :param metadata: file path
    :return: file path to real_edge_table
    """
    # type = 'genes'
    # type = 'functional_hierarchy'
    type = 'community'

    metadata_breakdown = metadata_to_dict(metadata)
    header_row = ['from', 'to', 'eweight'] + metadata_breakdown[1]

    #TODO groupby before writing then add different levels
    for start, level in zip([end_pos], ['species']):
        with open(standard_otu) as otu_file, open(outfile, 'w') as cyto_out:
            otu_read = csv.reader(otu_file, delimiter='\t')
            cyto_write = csv.writer(cyto_out, delimiter='\t')
            cyto_write.writerow(header_row)
            otu_header = otu_read.__next__()
            for line in otu_read:
                for weight, sample_id in zip(line[start+1:len(line)], otu_header[start+1:len(otu_header)]):
                    if float(weight) > 0:
                        cyto_write.writerow([','.join(str(i) for i in line[0:start+1])] + [line[0], weight] + [i for i in metadata_breakdown[0][sample_id]])
