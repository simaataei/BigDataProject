from Bio import SeqIO
from random import shuffle

records_original = list(SeqIO.parse("../Dataset/Selected30_subfamilies_tcdb.fasta", "fasta"))

list_subfamily = []
test_set = []
train_set = []
for i in range(0, 1500, 30):
    list_subfamily = records_original[i: i + 30]
    shuffle(list_subfamily)
    i = 0
    for lf in list_subfamily:
        if i < 6:
            test_set.append(lf)
            i += 1
        else:
            train_set.append(lf)
            i += 1

with open("../Dataset/Selected30_subfamilies_train_tcdb.fasta", "w") as handle:
    for rec in train_set:
        SeqIO.write(rec, handle, "fasta")

with open("../Dataset/Selected30_subfamilies_test_tcdb.fasta", "w") as handle:
    for rec in test_set:
        SeqIO.write(rec, handle, "fasta")