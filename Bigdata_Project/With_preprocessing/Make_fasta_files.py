from Bio import SeqIO

path = '../Dataset/'
with open(path + 'clusters_output_Selected30_nonRedundant_families_tcdb.txt', 'rt') as file:
    mclfile = file.read()
    clusters = mclfile.split('\n')

with open(path + 'Selected30_nonRedundant_families_tcdb.fasta', 'rU') as handle:
    IC_dataset = SeqIO.to_dict(SeqIO.parse(handle, 'fasta'))

i = 0
for cluster in clusters:
    current_sequences = []
    i += 1
    current_cluster = cluster.split('\t')
    for sequences in current_cluster:
        current_sequences.append(IC_dataset[sequences])
    with open(path + 'Clusters/cluster_' + str(i) + '.fasta', 'w') as file:
        SeqIO.write(current_sequences, file, 'fasta')
