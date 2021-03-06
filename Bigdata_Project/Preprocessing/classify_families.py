from Bio import SeqIO
import numpy as np

from scipy.signal import resample

from tqdm import tnrange, tqdm_notebook

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier

from Bio.SeqUtils.ProtParam import ProteinAnalysis

records_original = list(SeqIO.parse("../Dataset/Selected30_nonRedundant_families_tcdb.fasta", "fasta"))

sequences = [str(ro.seq) for ro in records_original]

classes = []
family_map = {}
i = 0
for item in records_original:
    famil = item.id.split('|')[3].split('.')[0:3]
    family = '.'.join(famil)
    if family not in family_map:
        family_map[family] = len(family_map)
    classes.append(family_map[family])



amino_map = {amino: i for i, amino in enumerate(list(set(''.join(sequences))))}

list_pair_dict = {}
for first in amino_map.keys():
    for second in amino_map.keys():
        if first + second not in list_pair_dict:
            list_pair_dict[first + second] = len(list_pair_dict)

i = 0
j = 0
X_aac = np.zeros((len(records_original), 20))
y = classes
for seq in records_original:
    analysed_seq = ProteinAnalysis(str(seq.seq))
    famil = '.'.join(seq.id.split('|')[3].split('.')[0:3])
    for val in analysed_seq.count_amino_acids().values():
        X_aac[i][j] = val / analysed_seq.length
        j += 1
    i += 1
    j = 0

i = 0
j = 0
row = 0
X_paac = np.zeros((len(records_original), 625))
for seq in records_original:
    analysed_seq = ProteinAnalysis(str(seq.seq))
    pair_amino_dict = {}
    i = 0
    pair_str = ''
    for char in str(seq.seq):
        pair_str += char
        i += 1
        if i == 2:
            if pair_str not in pair_amino_dict:
                pair_amino_dict[pair_str] = 1
                i = 0
                pair_str = ''
            else:
                pair_amino_dict[pair_str] += 1
                i = 0
                pair_str = ''
    for pair in pair_amino_dict:
        X_paac[row][list_pair_dict[pair]] = pair_amino_dict[pair] / analysed_seq.length
    row += 1

X = np.hstack((X_aac, X_paac))
# temp = []
# for i in range(X.shape[0]):
#     temp.append(resample(X[i, :], sample_length))
# resampled_features = np.array(temp)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

clf = svm.SVC(gamma='scale', kernel='linear')
#clf = RandomForestClassifier(n_estimators=1000)
clf.fit(X_train, y_train)
p_test = clf.predict(X_test)

print(classification_report(y_test, p_test))