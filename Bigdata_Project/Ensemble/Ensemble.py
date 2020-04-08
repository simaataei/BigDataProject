import warnings
warnings.filterwarnings('ignore')

from Bio import SeqIO

import numpy as np

from pyspark.sql import SparkSession

from Functions.convert_to_aac import convert_to_aac
from Functions.convert_to_paac import convert_to_paac
from Functions.convert_to_one_hot import convert_to_one_hot
from Functions.return_labels import return_labels

from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.metrics import confusion_matrix




# Init_spark
def init_spark():
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    return spark


prf_svm_list = []
prf_rf_list = []
prf_knn_list = []
for fold in range(1, 6):
    print(f'fold {fold}\n')
    # Read the sequences
    training_set = list(
        SeqIO.parse(f"../Train_test_subfamilies/train_test_5fold/Selected30_subfamilies_train_tcdb_fold_{fold}.fasta",
                    "fasta"))
    test_set = list(
        SeqIO.parse(f"../Train_test_subfamilies/train_test_5fold/Selected30_subfamilies_test_tcdb_fold_{fold}.fasta",
                    "fasta"))

    X_training_aac = convert_to_aac(training_set)
    X_training_paac = convert_to_paac(training_set)
    X_training_one_hot = convert_to_one_hot(training_set)
    X_test_aac = convert_to_aac(test_set)
    X_test_paac = convert_to_paac(test_set)
    X_test_one_hot = convert_to_one_hot(test_set)

    y_train = return_labels(training_set)
    y_test = return_labels(test_set)

    X = [(X_training_aac, X_test_aac), (X_training_paac, X_test_paac), (X_training_one_hot, X_test_one_hot)]
    i = 0
    for x_train, x_test in X:
        if i == 0:
            print('AAC\n')
        elif i == 1:
            print('PAAC\n')
        else:
            print('One Hot\n')
        standard_scaler = StandardScaler().fit(x_train)
        X_train = standard_scaler.transform(x_train)
        X_test = standard_scaler.transform(x_test)

        print('SVM\n')
        clf1 = SVC(kernel='rbf', gamma=0.1, C=10).fit(X_train, y_train)
        y_pred = clf1.predict(X_test)
        print(precision_recall_fscore_support(y_true=y_test, y_pred=y_pred, average='macro'))
        print('\n')
        prf_svm_list.append(precision_recall_fscore_support(y_true=y_test, y_pred=y_pred, average='macro')[0:3])

        print('Random Forrest\n')
        clf2 = RandomForestClassifier(n_estimators=1000).fit(X_train, y_train)
        y_pred = clf2.predict(X_test)
        print(precision_recall_fscore_support(y_true=y_test, y_pred=y_pred, average='macro'))
        print('\n')
        prf_rf_list.append(precision_recall_fscore_support(y_true=y_test, y_pred=y_pred, average='macro')[0:3])

        print('KNN\n')
        clf3 = KNeighborsClassifier(n_neighbors=1).fit(X_train, y_train)
        y_pred = clf3.predict(X_test)
        print(precision_recall_fscore_support(y_true=y_test, y_pred=y_pred, average='macro'))
        print('\n')
        prf_knn_list.append(precision_recall_fscore_support(y_true=y_test, y_pred=y_pred, average='macro')[0:3])

        i += 1

print('Total:\n')
arr_svm_prf = np.asanyarray(prf_svm_list)
arr_rf_prf = np.asanyarray(prf_rf_list)
arr_knn_prf = np.asanyarray(prf_knn_list)

print(f'SVM: {np.mean(arr_svm_prf, axis=0)}\n')
print(f'RF: {np.mean(arr_rf_prf, axis=0)}\n')
print(f'KNN: {np.mean(arr_knn_prf, axis=0)}\n')
