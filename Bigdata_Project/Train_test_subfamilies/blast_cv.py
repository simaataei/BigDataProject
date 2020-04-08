# CV for blast

import subprocess
from Bio import SeqIO
import numpy as np

path = '../Dataset/Selected30_subfamilies_tcdb.fasta'
k = 5
total_seqs = 30
records_original = list(SeqIO.parse(path, "fasta"))
f = 0
parts = int(total_seqs / k)

for fold in range(0, total_seqs, parts):
    f += 1
    test_set = []
    train_set = []
    for i in range(0, 2880, 30):
        list_family = records_original[i: i + 30]
        test = list_family[fold:fold + parts]
        del list_family[fold:fold + parts]
        for t in test:
            test_set.append(t)
        for lf in list_family:
            train_set.append(lf)
    with open(f"train_test_5fold/Selected30_subfamilies_train_tcdb_fold_{f}.fasta", "w") as handle:
        for rec in train_set:
            SeqIO.write(rec, handle, "fasta")

    with open(f"train_test_5fold/Selected30_subfamilies_test_tcdb_fold_{f}.fasta", "w") as handle:
        for rec in test_set:
            SeqIO.write(rec, handle, "fasta")
    print(f)
