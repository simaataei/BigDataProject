import numpy as np

with open("../Dataset/output_test_on_train_subfamilies_1e05.list", "r") as file:
    lines = file.readlines()
    pred_subfamily = {}
    classes_subfamily = {}
    for ln in lines:
        i = 0
        this_line = ln.split('\t')
        if '|'.join(this_line[0].split('|')[2:4]) not in pred_subfamily:
            pred_subfamily['|'.join(this_line[0].split('|')[2:4])] = '.'.join(this_line[1].split('|')[-1].split('.')[0:4])

        if '.'.join(this_line[0].split('|')[-1].split('.')[0:4]) not in classes_subfamily:
            classes_subfamily['.'.join(this_line[0].split('|')[-1].split('.')[0:4])] = len(classes_subfamily)


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

# np.savetxt("eval_subfamily.txt", evaluation_matrix_subfamily)