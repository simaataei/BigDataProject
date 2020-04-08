import numpy as np

total_classes = 96

total_evaluation_matrix = np.zeros((total_classes, 7))
max_k = 0
max_f1 = 0
for k in range(1, 2):
    for f in range(1, 2):
        with open(f"output_test_on_train_families_fold_{f}_8.list", "r") as file:
            lines = file.readlines()
            pred_family = {}
            classes = {}
            id_count = {}
            blast_output_tuple = []
            for ln in lines:
                this_line = ln.split('\t')
                id = '|'.join(this_line[0].split('|')[2:4])
                if id not in id_count:
                    id_count[id] = 1
                else:
                    id_count[id] += 1
                if id not in pred_family:
                    pred_family[id] = '.'.join(this_line[1].split('|')[-1].split('.')[0:3])
                if '.'.join(this_line[0].split('|')[-1].split('.')[0:3]) not in classes:
                    classes['.'.join(this_line[0].split('|')[-1].split('.')[0:3])] = len(classes)
                if '.'.join(this_line[1].split('|')[-1].split('.')[0:3]) not in classes:
                    classes['.'.join(this_line[1].split('|')[-1].split('.')[0:3])] = len(classes)
                blast_output_tuple.append(('|'.join(this_line[0].split('|')[2:4]), '|'.join(this_line[1].split('|')[2:4])))

        pred_family = {}
        for c in classes:
            i = 0
            while i < len(blast_output_tuple):
                id = '|'.join(blast_output_tuple[i][0].split('|')[:])
                classs = '.'.join(blast_output_tuple[i][0].split('|')[-1].split('.')[0:3])
                if classs == c:
                    if id_count[id] > 0:
                        pred_dict = {}
                        for selected_seqs in blast_output_tuple[i: i + 1]:
                            if '.'.join(selected_seqs[1].split('|')[-1].split('.')[0:3]) not in pred_dict:
                                pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:3])] = 1
                            else:
                                pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:3])] += 1
                    else:
                        for selected_seqs in blast_output_tuple[i: i + id_count[id]]:
                            if '.'.join(selected_seqs[1].split('|')[-1].split('.')[0:3]) not in pred_dict:
                                pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:3])] = 1
                            else:
                                pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:3])] += 1
                    pred_family[id] = max(pred_dict, key=pred_dict.get)
                i += id_count[id]


        # tp, tn, fp, fn, precision, recall, f1
        evaluation_matrix = np.zeros((total_classes, 7))
        for item_classes in classes:
            for item_pred_fm in pred_family:
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[
                    item_pred_fm] == item_classes:
                    evaluation_matrix[classes[item_classes], 0] += 1  # tp
                    total_evaluation_matrix[classes[item_classes], 0] += 1
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[
                    item_pred_fm] != item_classes:
                    evaluation_matrix[classes[item_classes], 1] += 1  # tn
                    total_evaluation_matrix[classes[item_classes], 1] += 1
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[
                    item_pred_fm] == item_classes:
                    evaluation_matrix[classes[item_classes], 2] += 1  # fp
                    total_evaluation_matrix[classes[item_classes], 2] += 1
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[
                    item_pred_fm] != item_classes:
                    evaluation_matrix[classes[item_classes], 3] += 1  # fn
                    total_evaluation_matrix[classes[item_classes], 3] += 1

        for item_classes in classes:
            if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 2] != 0:
                evaluation_matrix[classes[item_classes], 4] = evaluation_matrix[classes[item_classes], 0] / (
                        evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[
                    classes[item_classes], 2])  # precision
            if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 3] != 0:
                evaluation_matrix[classes[item_classes], 5] = evaluation_matrix[classes[item_classes], 0] / (
                        evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[
                    classes[item_classes], 3])  # recall
            if evaluation_matrix[classes[item_classes], 4] != 0 or evaluation_matrix[classes[item_classes], 5] != 0:
                evaluation_matrix[classes[item_classes], 6] = 2 * (
                        evaluation_matrix[classes[item_classes], 4] * evaluation_matrix[classes[item_classes], 5]) / (
                                                                      evaluation_matrix[classes[item_classes], 4] +
                                                                      evaluation_matrix[classes[item_classes], 5])  # f1

        # print(f"\n Families Fold {f}\n")
        # print(f"Precision = {np.mean(evaluation_matrix[:, 4])}")
        # print(f"Recall = {np.mean(evaluation_matrix[:, 5])}")
        # print(f"F1 = {np.mean(evaluation_matrix[:, 6])}")

    for i in range(total_classes):
        if total_evaluation_matrix[i, 0] != 0 or total_evaluation_matrix[i, 2] != 0:
            total_evaluation_matrix[i, 4] = total_evaluation_matrix[i, 0] / (
                    total_evaluation_matrix[i, 0] + total_evaluation_matrix[i, 2])  # precision
        if total_evaluation_matrix[i, 0] != 0 or total_evaluation_matrix[i, 3] != 0:
            total_evaluation_matrix[i, 5] = total_evaluation_matrix[i, 0] / (
                    total_evaluation_matrix[i, 0] + total_evaluation_matrix[i, 3])  # recall
        if total_evaluation_matrix[i, 4] != 0 or total_evaluation_matrix[i, 5] != 0:
            total_evaluation_matrix[i, 6] = 2 * (total_evaluation_matrix[i, 4] * total_evaluation_matrix[i, 5]) / (
                    total_evaluation_matrix[i, 4] + total_evaluation_matrix[i, 5])  # f1

    # print(f"\n Families total evalue {e_values[e_value]} \n")
    # print(f"Precision = {np.mean(total_evaluation_matrix[:, 4])}")
    # print(f"Recall = {np.mean(total_evaluation_matrix[:, 5])}")
    # print(f"F1 = {np.mean(total_evaluation_matrix[:, 6])}")
    if np.mean(total_evaluation_matrix[:, 6]) > max_f1:
        max_k = k
        max_f1 = np.mean(total_evaluation_matrix[:, 6])
print(max_k)
print('\n')
print(max_f1)
