# CV for blast

import subprocess
from Bio import SeqIO
import numpy as np

path = '../Dataset/Selected30_500_cutlength_families_tcdb.fasta'
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
    with open(f"train_test_5fold/Selected30_cut500_families_train_tcdb_fold_{f}.fasta", "w") as handle:
        for rec in train_set:
            SeqIO.write(rec, handle, "fasta")

    with open(f"train_test_5fold/Selected30_cut500_families_test_tcdb_fold_{f}.fasta", "w") as handle:
        for rec in test_set:
            SeqIO.write(rec, handle, "fasta")
    print(f)

    #
    # command_line = f"makeblastdb -in Dataset/Selected30_families_train_tcdb_fold_{fold}.fasta -dbtype 'prot' -out Dataset/DB_train_fold_{fold}"
    # # output = subprocess.run(command_line)
    # command_line = f"blastp -query Dataset/Selected30_families_test_tcdb_fold_{fold}.fasta -db Dataset/DB_train_fold_{fold} -outfmt '6 std qlen slen' -out Dataset/output_fold_{fold}.list -evalue {evalue}"
    # # output = subprocess.run(command_line)
    #
    # with open(f"../Dataset/output_fold_{fold}.list", "r") as file:
    #     lines = file.readlines()
    #     pred_family = {}
    #     pred_subfamily = {}
    #     classes = {}
    #     classes_subfamily = {}
    #     for ln in lines:
    #         i = 0
    #         this_line = ln.split('\t')
    #         if '|'.join(this_line[0].split('|')[2:4]) not in pred_family:
    #             pred_family['|'.join(this_line[0].split('|')[2:4])] = '.'.join(
    #                 this_line[1].split('|')[-1].split('.')[0:3])
    #         if '|'.join(this_line[0].split('|')[2:4]) not in pred_subfamily:
    #             pred_subfamily['|'.join(this_line[0].split('|')[2:4])] = '.'.join(
    #                 this_line[1].split('|')[-1].split('.')[0:4])
    #         if '.'.join(this_line[0].
    #                             split('|')[-1].split('.')[0:3]) not in classes:
    #             classes['.'.join(this_line[0].split('|')[-1].split('.')[0:3])] = len(classes)
    #         if '.'.join(this_line[0].split('|')[-1].split('.')[0:4]) not in classes_subfamily:
    #             classes_subfamily['.'.join(this_line[0].split('|')[-1].split('.')[0:4])] = len(classes_subfamily)
    #
    # # tp, tn, fp, fn, precision, recall, f1
    # evaluation_matrix = np.zeros((len(classes), 7))
    # for item_classes in classes:
    #     for item_pred_fm in pred_family:
    #         if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[
    #             item_pred_fm] == item_classes:
    #             evaluation_matrix[classes[item_classes], 0] += 1  # tp
    #         if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[
    #             item_pred_fm] != item_classes:
    #             evaluation_matrix[classes[item_classes], 1] += 1  # tn
    #         if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[
    #             item_pred_fm] == item_classes:
    #             evaluation_matrix[classes[item_classes], 2] += 1  # fp
    #         if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[
    #             item_pred_fm] != item_classes:
    #             evaluation_matrix[classes[item_classes], 3] += 1  # fn
    #
    # for item_classes in classes:
    #     if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 2] != 0:
    #         evaluation_matrix[classes[item_classes], 4] = evaluation_matrix[classes[item_classes], 0] / (
    #                 evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[
    #             classes[item_classes], 2])  # precision
    #     if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 3] != 0:
    #         evaluation_matrix[classes[item_classes], 5] = evaluation_matrix[classes[item_classes], 0] / (
    #                 evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[
    #             classes[item_classes], 3])  # recall
    #     if evaluation_matrix[classes[item_classes], 4] != 0 or evaluation_matrix[classes[item_classes], 5] != 0:
    #         evaluation_matrix[classes[item_classes], 6] = 2 * (
    #                 evaluation_matrix[classes[item_classes], 4] * evaluation_matrix[classes[item_classes], 5]) / (
    #                                                               evaluation_matrix[classes[item_classes], 4] +
    #                                                               evaluation_matrix[classes[item_classes], 5])  # f1
    #
    # print(f"\n Families fold {fold} \n")
    # print(f"Precision = {np.mean(evaluation_matrix[:, 4])}")
    # print(f"Recall = {np.mean(evaluation_matrix[:, 5])}")
    # print(f"F1 = {np.mean(evaluation_matrix[:, 6])}")
    #
    # np.savetxt(f"eval_family_cv_fold_{fold}.txt", evaluation_matrix)
