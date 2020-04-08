import numpy as np

with open("output_Selected30_families_test_on_train_tcdb.list", "r") as file:
    lines = file.readlines()
    pred_family = {}
    pred_subfamily = {}
    classes = {}
    classes_subfamily = {}
    for ln in lines:
        i = 0
        this_line = ln.split('\t')
        if '|'.join(this_line[0].split('|')[2:4]) not in pred_family:
            pred_family['|'.join(this_line[0].split('|')[2:4])] = '.'.join(this_line[1].split('|')[-1].split('.')[0:3])
        if '|'.join(this_line[0].split('|')[2:4]) not in pred_subfamily:
            pred_subfamily['|'.join(this_line[0].split('|')[2:4])] = '.'.join(this_line[1].split('|')[-1].split('.')[0:4])
        if '.'.join(this_line[0].
                            split('|')[-1].split('.')[0:3]) not in classes:
            classes['.'.join(this_line[0].split('|')[-1].split('.')[0:3])] = len(classes)
        if '.'.join(this_line[0].split('|')[-1].split('.')[0:4]) not in classes_subfamily:
            classes_subfamily['.'.join(this_line[0].split('|')[-1].split('.')[0:4])] = len(classes_subfamily)

# tp, tn, fp, fn, precision, recall, f1
evaluation_matrix = np.zeros((len(classes), 7))
for item_classes in classes:
    for item_pred_fm in pred_family:
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[item_pred_fm] == item_classes:
            evaluation_matrix[classes[item_classes], 0] += 1  # tp
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[item_pred_fm] != item_classes:
            evaluation_matrix[classes[item_classes], 1] += 1  # tn
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) != item_classes and pred_family[item_pred_fm] == item_classes:
            evaluation_matrix[classes[item_classes], 2] += 1  # fp
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:3]) == item_classes and pred_family[item_pred_fm] != item_classes:
            evaluation_matrix[classes[item_classes], 3] += 1  # fn

for item_classes in classes:
    if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 2] != 0:
        evaluation_matrix[classes[item_classes], 4] = evaluation_matrix[classes[item_classes], 0] / (evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[classes[item_classes], 2])  # precision
    if evaluation_matrix[classes[item_classes], 0] != 0 or evaluation_matrix[classes[item_classes], 3] != 0:
        evaluation_matrix[classes[item_classes], 5] = evaluation_matrix[classes[item_classes], 0] / (evaluation_matrix[classes[item_classes], 0] + evaluation_matrix[classes[item_classes], 3])  # recall
    if evaluation_matrix[classes[item_classes], 4] != 0 or evaluation_matrix[classes[item_classes], 5] != 0:
        evaluation_matrix[classes[item_classes], 6] = 2 * (evaluation_matrix[classes[item_classes], 4] * evaluation_matrix[classes[item_classes], 5]) / (evaluation_matrix[classes[item_classes], 4] + evaluation_matrix[classes[item_classes], 5])  # f1

print("\n Families \n")
print(f"Precision = {np.mean(evaluation_matrix[:, 4])}")
print(f"Recall = {np.mean(evaluation_matrix[:, 5])}")
print(f"F1 = {np.mean(evaluation_matrix[:, 6])}")


# Sub-families

evaluation_matrix_subfamily = np.zeros((len(classes_subfamily), 7))
for item_classes in classes_subfamily:
    for item_pred_fm in pred_subfamily:
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) == item_classes and pred_subfamily[item_pred_fm] == item_classes:
            evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] += 1  # tp
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) != item_classes and pred_subfamily[item_pred_fm] != item_classes:
            evaluation_matrix_subfamily[classes_subfamily[item_classes], 1] += 1  # tn
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) != item_classes and pred_subfamily[item_pred_fm] == item_classes:
            evaluation_matrix_subfamily[classes_subfamily[item_classes], 2] += 1  # fp
        if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) == item_classes and pred_subfamily[item_pred_fm] != item_classes:
            evaluation_matrix_subfamily[classes_subfamily[item_classes], 3] += 1  # fn

for item_classes in classes_subfamily:
    if evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] != 0 or evaluation_matrix_subfamily[classes_subfamily[item_classes], 2] != 0:
        evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] = evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] / (evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] + evaluation_matrix_subfamily[classes_subfamily[item_classes], 2])  # precision
    if evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] != 0 or evaluation_matrix_subfamily[classes_subfamily[item_classes], 3] != 0:
        evaluation_matrix_subfamily[classes_subfamily[item_classes], 5] = evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] / (evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] + evaluation_matrix_subfamily[classes_subfamily[item_classes], 3])  # recall
    if evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] != 0 or evaluation_matrix_subfamily[classes_subfamily[item_classes], 5] != 0:
        evaluation_matrix_subfamily[classes_subfamily[item_classes], 6] = 2 * (evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] * evaluation_matrix_subfamily[classes_subfamily[item_classes], 5]) / (evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] + evaluation_matrix_subfamily[classes_subfamily[item_classes], 5])  # f1
print("\n Sub-families \n")
print(f"Precision = {np.mean(evaluation_matrix_subfamily[:, 4])}")
print(f"Recall = {np.mean(evaluation_matrix_subfamily[:, 5])}")
print(f"F1 = {np.mean(evaluation_matrix_subfamily[:, 6])}")

np.savetxt("eval_family.txt", evaluation_matrix)
np.savetxt("eval_subfamily.txt", evaluation_matrix_subfamily)
