import csv

def check_csv_tsv(file):
    if ".tsv" in file:
        return '\t'
    if ".csv" in file:
        return ','

def clean_metadata_values(file, time, outfile):
    with open(file) as infile, open(outfile % time, 'w') as out:
        metadata_fix_values = csv.writer(out, delimiter='\t')
        metadata_read_values = csv.reader(infile, delimiter='\t')
        # close the files
        items_to_strip = ['[',']', "'", '"', '(', ')', '{', '}']
        for row in metadata_read_values:
            new_line = []
            for object in row:
                for item in items_to_strip:
                    object = object.replace(item, '')
                new_line.append(object)
            metadata_fix_values.writerow(new_line)


def verify_metadata(standard_otu, metadata, time, outfile):
    metadata_type = check_csv_tsv(metadata)
    otu_type = check_csv_tsv(standard_otu)
    with open(standard_otu) as otu_file, open(metadata, "r+") as metadata_in:

        #read files into convenient data structure (matrix)
        metadata_reader = csv.reader(metadata_in, delimiter=metadata_type)
        otu_reader = csv.reader(otu_file, delimiter=otu_type)

        #check sample names, create lists to compare later
        metadata_samplenames = []
        first_otu_line = otu_reader.__next__()
        otu_samplenames = []

        #check if sample names are only alphanumeric values
        for line in metadata_reader:
            if line[0].replace(' ', '').isalnum():
                pass
            else:
                error_string = "PROCESSING METADATA DID NOT WORK: Check your metadata it seems the value %s is not alphanumeric." % line[0]
                return error_string
            metadata_samplenames.append(line[0])

        for column in first_otu_line[1:len(first_otu_line)-1]:
            if column.replace(' ', '').isalnum():
                pass
            else:
                error_string = "PROCESSING OTU TABLE DID NOT WORK: Check your otu/asv table it seems the value %s is not alphanumeric." % column
                return error_string
            otu_samplenames.append(column)


        #TODO be sure the OTU table has the same number of obects in each row

        #check if differences between the two sample name sets
        if len(set(otu_samplenames) - set(metadata_samplenames)) == 0:
            #clean values
            clean_metadata_values(metadata, time, outfile)
            return True

        else:
            error_string = "PROCESSING SAMPLE NAMES DID NOT WORK: Check your metadata it seems the values %s do not match." % \
                           (set(otu_samplenames) - set(metadata_samplenames))
            return error_string




