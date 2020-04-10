from Bio import SeqIO
import numpy as np

records_original = list(SeqIO.parse("../Dataset/Refined_Seqs_tcdb.fasta", "fasta"))

subfamily_map = {}
for item in records_original:
    subfamil = item.id.split('|')[-1].split('.')[0:4]
    subfamily = '.'.join(subfamil)

    if subfamily not in subfamily_map:
        subfamily_map[subfamily] = len(subfamily_map)

max_length = 1000
min_length = 50

selected_list_seqReq = []
removed_list_seqReq = []
for fm in subfamily_map:
    list_temp = []
    for ro in records_original:
        if '.'.join(ro.id.split('|')[-1].split('.')[0:4]) == fm and (min_length < len(str(ro.seq)) < max_length):
            list_temp.append(ro)
    if len(list_temp) > 29:
        new_random_list = list(np.random.permutation(list_temp))[0:30]
        selected_list_seqReq.append(new_random_list)
    else:
        removed_list_seqReq.append(fm)

with open("../Dataset/Selected30_subfamilies_tcdb.fasta", "w") as handle:
    for rec in selected_list_seqReq:
        SeqIO.write(rec, handle, "fasta")
