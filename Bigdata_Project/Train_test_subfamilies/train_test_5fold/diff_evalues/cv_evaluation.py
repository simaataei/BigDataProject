import numpy as np
import matplotlib.pyplot as plt


e_values = {1: 10, 2: 1, 3: 0.1, 4: 0.01, 5: 0.001, 6: 0.0001, 7: 0.00001, 8: 0.000001, 9: 0.0000001, 10: 0.00000001,
            11: 0.000000001, 12: 0.0000000001}
chart_matrix_e_value = np.zeros((12, 3))  # precision, recall, f1
total_classes = 50
total_evaluation_matrix = np.zeros((total_classes, 7))
for e_value in e_values:
    total_evaluation_matrix = np.zeros((total_classes, 7))
    chart_matrix = np.zeros((5, 3))
    for f in range(1, 6):
        with open(f"output_test_on_train_subfamilies_fold_{f}_{e_value}.list", "r") as file:
            lines = file.readlines()
            pred_subfamily = {}
            classes_subfamily = {}
            for ln in lines:
                this_line = ln.split('\t')
                if '|'.join(this_line[0].split('|')[2:4]) not in pred_subfamily:
                    pred_subfamily['|'.join(this_line[0].split('|')[2:4])] = '.'.join(this_line[1].split('|')[-1].split('.')[0:4])
                if '.'.join(this_line[0].split('|')[-1].split('.')[0:4]) not in classes_subfamily:
                    classes_subfamily['.'.join(this_line[0].split('|')[-1].split('.')[0:4])] = len(classes_subfamily)
                if '.'.join(this_line[1].split('|')[-1].split('.')[0:4]) not in classes_subfamily:
                    classes_subfamily['.'.join(this_line[1].split('|')[-1].split('.')[0:4])] = len(classes_subfamily)

        evaluation_matrix_subfamily = np.zeros((total_classes, 7))
        for item_classes in classes_subfamily:
            for item_pred_fm in pred_subfamily:
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) == item_classes and pred_subfamily[
                    item_pred_fm] == item_classes:
                    evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] += 1  # tp
                    total_evaluation_matrix[classes_subfamily[item_classes], 0] += 1  # tp
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) != item_classes and pred_subfamily[
                    item_pred_fm] != item_classes:
                    evaluation_matrix_subfamily[classes_subfamily[item_classes], 1] += 1  # tn
                    total_evaluation_matrix[classes_subfamily[item_classes], 1] += 1  # tn
                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) != item_classes and pred_subfamily[
                    item_pred_fm] == item_classes:
                    evaluation_matrix_subfamily[classes_subfamily[item_classes], 2] += 1  # fp
                    total_evaluation_matrix[classes_subfamily[item_classes], 2] += 1  # fp

                if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) == item_classes and pred_subfamily[
                    item_pred_fm] != item_classes:
                    evaluation_matrix_subfamily[classes_subfamily[item_classes], 3] += 1  # fn
                    total_evaluation_matrix[classes_subfamily[item_classes], 3] += 1  # fn


        for item_classes in classes_subfamily:
            if evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] != 0 or evaluation_matrix_subfamily[
                classes_subfamily[item_classes], 2] != 0:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] = evaluation_matrix_subfamily[
                                                                                      classes_subfamily[
                                                                                          item_classes], 0] / (
                                                                                              evaluation_matrix_subfamily[
                                                                                                  classes_subfamily[
                                                                                                      item_classes], 0] +
                                                                                              evaluation_matrix_subfamily[
                                                                                                  classes_subfamily[
                                                                                                      item_classes], 2])  # precision
            if evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] != 0 or evaluation_matrix_subfamily[
                classes_subfamily[item_classes], 3] != 0:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 5] = evaluation_matrix_subfamily[
                                                                                      classes_subfamily[
                                                                                          item_classes], 0] / (
                                                                                              evaluation_matrix_subfamily[
                                                                                                  classes_subfamily[
                                                                                                      item_classes], 0] +
                                                                                              evaluation_matrix_subfamily[
                                                                                                  classes_subfamily[
                                                                                                      item_classes], 3])  # recall
            if evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] != 0 or evaluation_matrix_subfamily[
                classes_subfamily[item_classes], 5] != 0:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 6] = 2 * (
                            evaluation_matrix_subfamily[classes_subfamily[item_classes], 4] * evaluation_matrix_subfamily[
                        classes_subfamily[item_classes], 5]) / (evaluation_matrix_subfamily[
                                                                    classes_subfamily[item_classes], 4] +
                                                                evaluation_matrix_subfamily[
                                                                    classes_subfamily[item_classes], 5])  # f1
        # print(f"\n Sub-families Fold {f} \n")
        # print(f"Precision = {np.mean(evaluation_matrix_subfamily[:, 4])}")
        # print(f"Recall = {np.mean(evaluation_matrix_subfamily[:, 5])}")
        # print(f"F1 = {np.mean(evaluation_matrix_subfamily[:, 6])}")

        chart_matrix[f - 1] = (
            np.mean(evaluation_matrix_subfamily[:, 4]), np.mean(evaluation_matrix_subfamily[:, 5]), np.mean(evaluation_matrix_subfamily[:, 6]))

    my_folds = ('fold1', 'fold2', 'fold3', 'fold4', 'fold5')
    y_labels = ['precision', 'recall', 'f1']
    for chart in range(3):
        plt.figure()
        rects = plt.bar(np.arange(len(my_folds)), chart_matrix[:, chart], align='center')
        plt.xticks(np.arange(len(my_folds)), my_folds)
        plt.yticks(np.arange(0, 1, step=0.1))
        plt.ylabel(y_labels[chart])
        plt.xlabel('folds')
        plt.title(f'K-fold cross validation on e-value {e_values[e_value]}')
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., 1 * height, "{:.4f}".format(height), ha='center',
                     va='bottom')
        # plt.show()
        plt.savefig(f'Figs/subfamily_{y_labels[chart]}_evalue_{e_value}.jpg', dpi=300, format='png')

    for i in range(total_classes):
        if total_evaluation_matrix[i, 0] != 0 or total_evaluation_matrix[i, 2] != 0:
            total_evaluation_matrix[i, 4] = total_evaluation_matrix[i, 0] / (total_evaluation_matrix[i, 0] + total_evaluation_matrix[i, 2])  # precision
        if total_evaluation_matrix[i, 0] != 0 or total_evaluation_matrix[i, 3] != 0:
            total_evaluation_matrix[i, 5] = total_evaluation_matrix[i, 0] / (total_evaluation_matrix[i, 0] + total_evaluation_matrix[i, 3])  # recall
        if total_evaluation_matrix[i, 4] != 0 or total_evaluation_matrix[i, 5] != 0:
            total_evaluation_matrix[i, 6] = 2 * (total_evaluation_matrix[i, 4] * total_evaluation_matrix[i, 5]) / (total_evaluation_matrix[i, 4] + total_evaluation_matrix[i, 5])  # f1

    # print(f"\n Sub-families total \n")
    # print(f"Precision = {np.mean(total_evaluation_matrix[:, 4])}")
    # print(f"Recall = {np.mean(total_evaluation_matrix[:, 5])}")
    # print(f"F1 = {np.mean(total_evaluation_matrix[:, 6])}")

    chart_matrix_e_value[e_value - 1] = (np.mean(total_evaluation_matrix[:, 4]), np.mean(total_evaluation_matrix[:, 5]),
                                         np.mean(total_evaluation_matrix[:, 6]))

my_e_values = ('10', '1', '0.1', '1e-2', '1e-3', '1e-4', '1e-5', '1e-6', '1e-7', '1e-8',
               '1e-9', '1e-10')
y_labels = ['precision', 'recall', 'f1']

for chart in range(3):
    plt.figure()
    axis_font = {'fontname': 'Arial', 'size': '8'}
    rects = plt.bar(np.arange(len(my_e_values)), chart_matrix_e_value[:, chart], align='center', alpha = .6)
    plt.xticks(np.arange(len(my_e_values)), my_e_values)
    plt.ylabel(y_labels[chart])
    plt.yticks(np.arange(0, 1, step=0.1))
    plt.xlabel('e-values')
    plt.title(f'K-fold cross validation on final evaluation')
    plt.plot(np.arange(len(my_e_values)), chart_matrix_e_value[:, chart], marker='o', markerfacecolor='blue', markersize=8,
             color='skyblue', linewidth=4)
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.01 * height, "{:.4f}".format(height), ha='center',
                 va='bottom', fontdict=axis_font)
    # plt.show()
    plt.savefig(f'Figs/subfamily_Total_{y_labels[chart]}.jpg', dpi=300, format='png')
