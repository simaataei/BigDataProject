from Bio import SeqIO
import numpy as np
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.svm import SVC



np.random.seed(2020)
records_original = list(SeqIO.parse("tcdb17feb2020.fasta", "fasta"))
family_dict = {}
i = 0
for item in records_original:
    famil = item.id.split('|')[3].split('.')[0:3]
    family = '.'.join(famil)

    if family not in family_dict:
        family_dict[family] = i
        i += 1

i = 0
j = 0
X_aac = np.zeros((len(records_original), 20))
y_aac = np.zeros((len(records_original),))
for seq in records_original:
    analysed_seq = ProteinAnalysis(str(seq.seq))
    famil = '.'.join(seq.id.split('|')[3].split('.')[0:3])
    y_aac[i] = family_dict[famil]
    for val in analysed_seq.count_amino_acids().values():
        X_aac[i][j] = val / analysed_seq.length
        j += 1
    i += 1
    j = 0

family_dict_count = {}
i = 0
for item in records_original:
    famil = item.id.split('|')[3].split('.')[0:3]
    family = '.'.join(famil)

    if family not in family_dict_count:
        family_dict_count[family] = 1
    else:
        family_dict_count[family] += 1

X_train, X_test, y_train, y_test = train_test_split(X_aac, y_aac, test_size=0.2, random_state=2020)

scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# clf = SVC(gamma=1).fit(X_train, y_train)
# print(classification_report(y_test, clf.predict(X_test)))

clf = RandomForestClassifier(n_estimators=9).fit(X_train, y_train)
print(classification_report(y_test, clf.predict(X_test)))



a=1