Big data project

Folders:

Preprocessing:
In this folder there are different py files which do different preprocessing such as down sampling, eliminating unknown amino acids, ... on families and sub-families.

Classifier:
In this folder there is a classifier.py file, which use sklearn library to classify the sequences based on families and sub-families(Once for family and the changed to sub-family). Also, f1 measure is computed in this file.

Dataset:
This folder has several fasta files format which are the raw dataset and the preprocessed ones.

KNN_blast:
In this folder, we tried to use knn on the blast metric command line tool.

Train_test_families and train_test_subfamilies:
These are important folders which include 5-folds for families and sub-families. Also computing with different parameter which is evalue is done in these folders.