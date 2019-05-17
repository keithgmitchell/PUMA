import csv

with open('S1816SASV.fasta', 'r') as fasta_in, open('S1816SASV_reversed.fasta', 'w') as fasta_out:
    fasta_out_csv = csv.writer(fasta_out)
    next_reversed = False
    count_reversed = 0
    for line in fasta_in:
        if line[0]=='>':
            if line[1]=='r':
                count_reversed+=1
                fasta_out.write(str(line))
                next_reversed=True
            else:
                fasta_out.write(str(line))
        elif line[0]==' ':
            continue
        elif next_reversed == True:
            line2 = line.strip('\n')
            fasta_out.write(line2[::-1]+'\n')
            next_reversed=False
        else:
            fasta_out.write(str(line))




