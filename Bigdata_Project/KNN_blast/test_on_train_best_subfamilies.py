import numpy as np


with open("../Train_test_subfamilies/train_test_5fold/diff_evalues/output_test_on_train_subfamilies_fold_1_8.list", "r") as file:
    lines = file.readlines()
    id_count = {}
    classes = {}
    all_seqs_dict = {}
    blast_output_tuple = []
    classes_subfamily = {}
    for l in lines:
        this_line = l.split('\t')
        id = '|'.join(this_line[0].split('|')[2:4])
        if id not in id_count:
            id_count[id] = 1
        else:
            id_count[id] += 1
        if '.'.join(this_line[0].split('|')[-1].split('.')[0:4]) not in classes:
            classes['.'.join(this_line[0].split('|')[-1].split('.')[0:4])] = len(classes)
        if '|'.join(this_line[0].split('|')[2:4]) not in all_seqs_dict:
            all_seqs_dict['|'.join(this_line[0].split('|')[2:4])] = len(all_seqs_dict)
        blast_output_tuple.append(('|'.join(this_line[0].split('|')[2:4]), '|'.join(this_line[1].split('|')[2:4])))
        if '.'.join(this_line[0].split('|')[-1].split('.')[0:4]) not in classes_subfamily:
            classes_subfamily['.'.join(this_line[0].split('|')[-1].split('.')[0:4])] = len(classes_subfamily)

for k in range(10):
    pred_subfamily = {}
    for c in classes:
        i = 0
        while i < len(blast_output_tuple):
            id = '|'.join(blast_output_tuple[i][0].split('|')[:])
            classs = '.'.join(blast_output_tuple[i][0].split('|')[-1].split('.')[0:4])
            if classs == c:
                if id_count[id] > k:
                    pred_dict = {}
                    for selected_seqs in blast_output_tuple[i: i+k+1]:
                        if '.'.join(selected_seqs[1].split('|')[-1].split('.')[0:4]) not in pred_dict:
                            pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:4])] = 1
                        else:
                            pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:4])] += 1
                else:
                    for selected_seqs in blast_output_tuple[i: i+id_count[id]]:
                        if '.'.join(selected_seqs[1].split('|')[-1].split('.')[0:4]) not in pred_dict:
                            pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:4])] = 1
                        else:
                            pred_dict['.'.join(selected_seqs[1].split('|')[-1].split('.')[0:4])] += 1
                pred_subfamily[id] = max(pred_dict, key=pred_dict.get)
            i += id_count[id]

    evaluation_matrix_subfamily = np.zeros((len(classes_subfamily), 7))
    for item_classes in classes_subfamily:
        for item_pred_fm in pred_subfamily:
            if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) == item_classes and pred_subfamily[
                item_pred_fm] == item_classes:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 0] += 1  # tp
            if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) != item_classes and pred_subfamily[
                item_pred_fm] != item_classes:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 1] += 1  # tn
            if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) != item_classes and pred_subfamily[
                item_pred_fm] == item_classes:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 2] += 1  # fp
            if '.'.join(item_pred_fm.split('|')[-1].split('.')[0:4]) == item_classes and pred_subfamily[
                item_pred_fm] != item_classes:
                evaluation_matrix_subfamily[classes_subfamily[item_classes], 3] += 1  # fn

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
    print("\n Sub-families \n")
    print(f"Precision = {np.mean(evaluation_matrix_subfamily[:, 4])}")
    print(f"Recall = {np.mean(evaluation_matrix_subfamily[:, 5])}")
    print(f"F1 = {np.mean(evaluation_matrix_subfamily[:, 6])}")



