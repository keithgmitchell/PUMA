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


def handle_files(standard_otu, metadata, outfile):
    """
    :param standard_otu: file path
    :param metadata: file path
    :return: file path to real_edge_table
    """
    metadata_breakdown = metadata_to_dict(metadata)

    header_row = ['from', 'to', 'eweight'] + metadata_breakdown[1]

    #TODO make this the rarefied file
    with open(standard_otu) as otu_file, open(outfile, 'w') as cyto_out:
        otu_read = csv.reader(otu_file, delimiter='\t')
        cyto_write = csv.writer(cyto_out, delimiter='\t')
        cyto_write.writerow(header_row)
        otu_header = otu_read.__next__()
        for line in otu_read:
            for object, pos in zip(line[1:len(line)], otu_header[1:len(otu_header)-1]):
                cyto_write.writerow([pos, line[len(otu_header)-1], object] + [i for i in metadata_breakdown[0][pos]])
