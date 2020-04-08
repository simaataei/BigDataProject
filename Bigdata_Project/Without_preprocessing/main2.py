from Bio import SeqIO
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.svm import SVC

def convert_to_aac(set):
    i = 0
    j = 0
    feature_matrix_aac = np.zeros((len(set), 20))
    set_labels_aac = np.zeros((len(set),))
    for seq in set:
        analysed_seq = ProteinAnalysis(str(seq.seq))
        famil = '.'.join(seq.id.split('|')[3].split('.')[0:3])
        set_labels_aac[i] = family_dict[famil]
        for val in analysed_seq.count_amino_acids().values():
            feature_matrix_aac[i][j] = val / analysed_seq.length
            j += 1
        i += 1
        j = 0
    return feature_matrix_aac, set_labels_aac

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def plot_family_count(dic, n):
    sorted_tuples = sorted(dic.items(), key=lambda x: x[1], reverse=True)[0:n]
    x = [x[0] for x in sorted_tuples]
    y = [y[1] for y in sorted_tuples]
    plt.bar(range(len(x)), y, align='center')
    plt.xticks(range(len(x)), x)
    plt.show()

np.random.seed(2020)
records = list(SeqIO.parse("tcdb17feb2020.fasta", "fasta"))
records_original = list(SeqIO.parse("tcdb17feb2020.fasta", "fasta"))
test_records = np.round(len(records) * .2)
num_test = np.random.permutation(int(test_records))

list_test = []
for i in num_test:
    list_test.append(records[i])
    records.pop(i)

family_dict = {}
i = 0
for item in records_original:
    famil = item.id.split('|')[3].split('.')[0:3]
    family = '.'.join(famil)

    if family not in family_dict:
        family_dict[family] = i
        i += 1
labels = list(range(0, 1234))

train_labels = []
for item in records:
    famil = '.'.join(item.id.split('|')[3].split('.')[0:3])
    train_labels.append(family_dict[famil])

test_labels = []
for item in list_test:
    famil = '.'.join(item.id.split('|')[3].split('.')[0:3])
    test_labels.append(family_dict[famil])

test_set = list_test
train_set = records

family_dict_count = {}
i = 0
for item in records_original:
    famil = item.id.split('|')[3].split('.')[0:3]
    family = '.'.join(famil)

    if family not in family_dict_count:
        family_dict_count[family] = 1
    else:
        family_dict_count[family] += 1

train_features, train_labels = convert_to_aac(train_set)
test_features, test_labels = convert_to_aac(test_set)

clf = RandomForestClassifier().fit(train_features, train_labels)
y_pred = clf.predict(test_features)
print(classification_report(test_labels, y_pred))

clf = SVC(gamma='auto')
clf.fit(train_features, train_labels)
y_pred = clf.predict(test_features)
print(classification_report(test_labels, y_pred))
a = 2
