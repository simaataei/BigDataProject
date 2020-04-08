import numpy as np

with open("../Dataset/output_Selected30_nonRedundant_families_tcdb.list", "r") as file:
    lines = file.readlines()
    all_seq_dict = {}
    for ln in lines:
        i = 0
        for part in ln.split('\t'):
            key = part.split('|')[-1]
            if key not in all_seq_dict:
                all_seq_dict[key] = len(all_seq_dict)
            i += 1
            if i == 2:
                break

blast_matrix = np.zeros((len(all_seq_dict), len(all_seq_dict)))

with open("../Dataset/output_Selected30_nonRedundant_families_tcdb.list", "r") as file:
    lines = file.readlines()
    for ln in lines:
        this_line = ln.split('\t')
        first = this_line[0].split('|')[-1]
        second = this_line[1].split('|')[-1]
        evalue = float(this_line[10])

        blast_matrix[all_seq_dict[first]][all_seq_dict[second]] = evalue

matrix_families = np.zeros((68, 68))

k = 0
for i in range(matrix_families.shape[0]):
    for j in range(matrix_families.shape[0]):
        for l in range(0, blast_matrix.shape[0], 30):
            for k in range(0, blast_matrix.shape[0], 30):
                matrix_families[i][j] = np.median(blast_matrix[l:l + 30][k:k + 30])

a = 1
