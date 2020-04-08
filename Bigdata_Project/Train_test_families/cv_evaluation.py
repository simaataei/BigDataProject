import numpy as np

total_classes = 96
total_evaluation_matrix = np.zeros((total_classes, 7))
for f in range(1, 6):
    with open(f"train_test_5fold/output_test_on_train_families_fold_{f}_1e05.list", "r") as file:
        lines = file.readlines()
        pred_family = {}
        classes = {}
        for ln in lines:
            this_line = ln.split('\t')
            if '|'.join(this_line[0].split('|')[2:4]) not in pred_family:
                pred_family['|'.join(this_line[0].split('|')[2:4])] = '.'.join(
                    this_line[1].split('|')[-1].split('.')[0:3])
            if '.'.join(this_line[0].split('|')[-1].split('.')[0:3]) not in classes:
                classes['.'.join(this_line[0].split('|')[-1].split('.')[0:3])] = len(classes)
            if '.'.join(this_line[1].split('|')[-1].split('.')[0:3]) not in classes:
                classes['.'.join(this_line[1].split('|')[-1].split('.')[0:3])] = len(classes)

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

    print(f"\n Families Fold {f}\n")
    print(f"Precision = {np.mean(evaluation_matrix[:, 4])}")
    print(f"Recall = {np.mean(evaluation_matrix[:, 5])}")
    print(f"F1 = {np.mean(evaluation_matrix[:, 6])}")

for i in range(total_classes):
    if total_evaluation_matrix[i, 0] != 0 or total_evaluation_matrix[i, 2] != 0:
        total_evaluation_matrix[i, 4] = total_evaluation_matrix[i, 0] / (total_evaluation_matrix[i, 0] + total_evaluation_matrix[i, 2])  # precision
    if total_evaluation_matrix[i, 0] != 0 or total_evaluation_matrix[i, 3] != 0:
        total_evaluation_matrix[i, 5] = total_evaluation_matrix[i, 0] / (total_evaluation_matrix[i, 0] + total_evaluation_matrix[i, 3])  # recall
    if total_evaluation_matrix[i, 4] != 0 or total_evaluation_matrix[i, 5] != 0:
        total_evaluation_matrix[i, 6] = 2 * (total_evaluation_matrix[i, 4] * total_evaluation_matrix[i, 5]) / (total_evaluation_matrix[i, 4] + total_evaluation_matrix[i, 5])  # f1

print(f"\n Families total \n")
print(f"Precision = {np.mean(total_evaluation_matrix[:, 4])}")
print(f"Recall = {np.mean(total_evaluation_matrix[:, 5])}")
print(f"F1 = {np.mean(total_evaluation_matrix[:, 6])}")
