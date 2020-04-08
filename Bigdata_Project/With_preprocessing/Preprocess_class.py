from Bio import SeqIO
import numpy as np

records_original = list(SeqIO.parse("../Dataset/non_redundant_limited_refined_tcdb.fasta", "fasta"))

# sequences = [str(ro.seq) for ro in records_original]
#classes = np.array([int(ro.id.split('|')[-1].split('.')[0]) for ro in records_original])
classes = [1, 2, 3, 4, 5, 6, 7, 8, 9]

max_length = 1000
min_length = 50

selected_list_seqReq = []
removed_list_seqReq = []
for cl in classes:
    list_temp = []
    for ro in records_original:
        if int('.'.join(ro.id.split('|')[-1].split('.')[0])) == cl and (min_length < len(str(ro.seq)) < max_length):
            list_temp.append(ro)
    if len(list_temp) > 29:
        new_random_list = list(np.random.permutation(list_temp))[0:30]
        selected_list_seqReq.append(new_random_list)
    else:
        removed_list_seqReq.append(cl)

with open("../Dataset/Selected30_nonRedundant_classes_tcdb.fasta", "w") as handle:
    for rec in selected_list_seqReq:
        SeqIO.write(rec, handle, "fasta")

a=2