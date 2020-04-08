import numpy as np

with open("train_test_5fold/best_hits_test_on_train_families_fold_1_1e05.list", "r") as file:
    lines = file.readlines()
    pred_family = {}
    classes = {}
    for ln in lines:
        i = 0
        this_line = ln.split('\t')
        if '|'.join(this_line[0].split('|')[2:4]) not in pred_family:
            pred_family['|'.join(this_line[0].split('|')[2:4])] = '.'.join(this_line[1].split('|')[-1].split('.')[0:3])

        if '.'.join(this_line[0].
                            split('|')[-1].split('.')[0:3]) not in classes:
            classes['.'.join(this_line[0].split('|')[-1].split('.')[0:3])] = len(classes)

        if '.'.join(this_line[1].
                            split('|')[-1].split('.')[0:3]) not in classes:
            classes['.'.join(this_line[1].split('|')[-1].split('.')[0:3])] = len(classes)

# tp, tn, fp, fn, precision, recall, f1
evaluation_matrix = np.zeros((len(classes), 7))
for item_classes in classes:
    for item_pred_fm in pred_family:
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[
            item_pred_fm] == item_classes:
            evaluation_matrix[classes[item_classes], 0] += 1  # tp
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[
            item_pred_fm] != item_classes:
            evaluation_matrix[classes[item_classes], 1] += 1  # tn
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[
            item_pred_fm] == item_classes:
            evaluation_matrix[classes[item_classes], 2] += 1  # fp
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[
            item_pred_fm] != item_classes:
            evaluation_matrix[classes[item_classes], 3] += 1  # fn

for item_classes in classes:
    if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 2] != 0:
        evaluation_matrix[classes[item_classes], 4] = evaluation_matrix[classes[item_classes], 0] / (
                evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[
            classes[item_classes], 2])  # precision
    if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 3] != 0:
        evaluation_matrix[classes[item_classes], 5] = evaluation_matrix[classes[item_classes], 0] / (
                evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[classes[item_classes], 3])  # recall
    if evaluation_matrix[classes[item_classes], 4] != 0 or evaluation_matrix[classes[item_classes], 5] != 0:
        evaluation_matrix[classes[item_classes], 6] = 2 * (
                evaluation_matrix[classes[item_classes], 4] * evaluation_matrix[classes[item_classes], 5]) / (
                                                              evaluation_matrix[classes[item_classes], 4] +
                                                              evaluation_matrix[classes[item_classes], 5])  # f1

print("\n Families \n")
print(f"Precision = {np.mean(evaluation_matrix[:, 4])}")
print(f"Recall = {np.mean(evaluation_matrix[:, 5])}")
print(f"F1 = {np.mean(evaluation_matrix[:, 6])}")
