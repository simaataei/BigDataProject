from Bio import SeqIO
import numpy as np

records_original = list(SeqIO.parse("../Dataset/Selected30_subfamilies_tcdb.fasta", "fasta"))

# Find sequences with the same TC numbers -------------------------
# list_bood = []
# list_nabood = []
# list_non_redundant_limited_refined = []
# for ro in records_original:
#     if str(ro.id).split('|')[-1] not in list_bood:
#         list_bood.append(str(ro.id).split('|')[-1])
#         list_non_redundant_limited_refined.append(ro)
#     else:
#         if str(ro.id).split('|')[-1] not in list_nabood:
#             list_nabood.append(str(ro.id).split('|')[-1])
#
# with open("../Dataset/non_redundant_limited_refined_tcdb.fasta", "w") as handle:
#     SeqIO.write(list_non_redundant_limited_refined, handle, "fasta")
# -----------------

# max_length = 1000
# min_length = 50
# i = 0
# family_length = {}  # Key: family - Value: Number of deleted long sequences
# for ro in records_original:
#     if min_length > len(str(ro.seq)) or len(str(ro.seq)) > max_length:
#         if '.'.join(ro.id.split('|')[-1].split('.')[0:3]) not in family_length:
#             family_length['.'.join(ro.id.split('|')[-1].split('.')[0:3])] = 1
#         else:
#             family_length['.'.join(ro.id.split('|')[-1].split('.')[0:3])] += 1
#         records_original.pop(i)
#     i += 1
#
# import pickle
# f = open("family_deleted_long_sequences.pkl","wb")
# pickle.dump(family_length,f)
# f.close()


# records_original = list(SeqIO.parse("../Dataset/non_redundant_limited_refined_tcdb.fasta", "fasta"))

# remove extra amino acids ----------
Amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
               'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

i = 0
for ro in records_original:
    for r in str(ro.seq):
        if r not in Amino_acids:
            records_original.pop(i)
    i += 1
# ---------------------------

#sequences = [str(ro.seq) for ro in records_original]
#classes = np.array([int(ro.id.split('|')[-1].split('.')[0]) for ro in records_original])


# family_map = {}
# i = 0
# for item in records_original:
#     famil = item.id.split('|')[3].split('.')[0:3]
#     family = '.'.join(famil)
#
#     if family not in family_map:
#         family_map[family] = i
#         i += 1
#
# max_length = 1000
# min_length = 50
#
# selected_list_seqReq = []
# removed_list_seqReq = []
# for fm in family_map:
#     list_temp = []
#     for ro in records_original:
#         if '.'.join(ro.id.split('|')[-1].split('.')[0:3]) == fm and (min_length < len(str(ro.seq)) < max_length):
#             list_temp.append(ro)
#     if len(list_temp) > 29:
#         new_random_list = list(np.random.permutation(list_temp))[0:30]
#         selected_list_seqReq.append(new_random_list)
#     else:
#         removed_list_seqReq.append(fm)

# with open("../Dataset/Refined_Seqs_tcdb.fasta", "w") as handle:
#     SeqIO.write(records_original, handle, "fasta")
# with open("../Dataset/Selected30_nonRedundant_families_tcdb.fasta", "w") as handle:
#     for rec in selected_list_seqReq:
#         SeqIO.write(rec, handle, "fasta")


a = 2
