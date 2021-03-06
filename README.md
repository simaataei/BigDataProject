# BigDataProject
ABSTRACT

According to rapid improvements in genome sequencing, protein functional annotation is turned into the focus of interest in many academic efforts. In this project, we analyze the Transporter Classification Database (TCDB). The TCDB is a comprehensive database for membrane transport proteins, which is approved by the International Union of Biochemistry and Molecular Biology (IUBMB), known as the Transporter Classification (TC) system. The main goal of this analysis is to classify membrane transport proteins into families with the same functionality. Supposing sequences with similar features might have similar functionalities, classifying protein sequences based on their features could be a practical method for protein functional annotation. In this research, multiple classifiers are implemented: Support Vector Machine, Random Forrest, and K-Nearest Neighbor. This research finds the K-Nearest Neighbor algorithm using the Basic Local Alignment Search Tool as the best classifier with 97.57% f1-score for family and 97.81% f1-score for subfamily classification.


INTRODUCTION


Although the sequences of many membrane proteins are available now, their specific functions remain unknown. Therefore, there is a consistent need for computational methods that predict the function of membrane proteins. Transporter proteins is a term used for addressing proteins that serve the function of moving different substances across the cell [1]. Generally, finding the functions of each protein with experimental methods is not an easy task, because the function may be explicitly related to the native environment in which a particular organism lives; such an environment is hard to simulate in a lab. In this research, given a transporter protein amino acid sequence, a prediction of its TC family and subfamily is to be made. 
The TC system is a classified transporters dataset that incorporates both functional and phylogenetic information. Sequences in the TCDB database are organized in a five-level hierarchical system as follows: N1.L1.N2.N3.N4. Transporters are classified based on five criteria, and each of these criteria corresponds to one of the five numbers or letters within the TC number for a particular type of transporter. Here we classify the protein sequences based on N2 and N3. N2 represents the transporter subfamilies of which there are over 1000 in TCDB, and N3 represents the family or phylogenetic clusters within a family.
Barghas and Helms [2] worked on TCDB similarily. They performed a practical classification of transporter TC families and transported substrate molecules using a dataset from three model organisms. For each of the species, four groups of transporters were collected. They reported 26 common families from three various organisms that they worked on.


MATERIALS AND METHODS

1.  Preprocessing:


Preprocessing includes three major steps: First, excluding sequences with unacceptable amino acids (B, Z, X, J, O, U ). Then, excluding sequences with unacceptable length (length > 1000 or < 50). The third step is extracting a balanced dataset, which is explained in the following section. 



2.  DATASET


In this research, we analyze the Transporter Classification Database (TCDB ) [3]. TCBD contains more than 10,000 non-redundant transporter proteins. After preprocessing the data, we extracted two different datasets using down-sampling. We extract 30 sequences of each family/subfamily randomly based on the central limit theorem. Consequently, families and subfamilies with less than 30 sequences are excluded. The first dataset, family, includes 2880 samples (30 samples from 96 families), and the second dataset, subfamily, includes 1500 samples (30 samples from 50 subfamilies).

3.  FEATURE EXTRACTION

In this project, several features are explored: Amino Acid Composition (AAC), pair amino acid composition (PAAC), and resampled one-hot feature vector. The Amino Acid Composition or AAC is the number of amino acids of each type normalized with the total number of residues. PAAC is the normalized frequency of each pair of amino acids. Moreover, the third feature vector is the resampled one-hot encoding feature vector. First, one-hot encoding creates a binary column for each category and returns a sparse matrix or dense array. As a result, each amino acid chain is mapped to a binary string. Then, “scipy.signal” package is used to sample from each sparse binary strings. We set a maximum sample length to 100.
In addition to positional and combinational features, evolutional features might be useful in classifying transporter protein sequences. The alignment of protein sequences reveals practical evolutional information of protein sequences. BLAST or Basic Local Alignment Search Tool algorithm is a local sequence alignment method designed for protein sequence alignments. This algorithm takes a query protein sequence as input and searches the sequence databases for similarities [4]. Protein similarities could be used in predicting the families and subfamilies of each sequence.  

4.  CLASSIFICATION


In this project, we implemented four different classifiers with different configurations. 
  •  Support Vector Machines or SVM with multiple kernels (linear, RBF, multinomial)
  •  Random Forrest with various number of estimators (from 100 to 1500 with the step of 100)
  •  K-Nearest Neighbor with different numbers of K
  •  and K-Nearest Neighbor using BLAST
 The datasets are split to test and train segments with a proportion of 0.2 and 0.8, respectively. 5-folds cross-validation is implemented to assist with more accurate results. To implement the classifiers, we used scikit-learn, Bio-Python, BLAST command-line, and scipy.signal packages.

RESULTS:


Evaluations are reported with precision, recall, and f1-score. Since the multi-class classification and 5-fold cross-validation are implemented, evaluation metrics are calculated using a total number of True Positive (TP), False Positive (FP), False Negative (FN), True Negative (TN) on all folds. Macro and the micro average of metrics for each class are available on the result files. We examined all the classifiers, and the best results for each classifier on the family dataset are reported as following.
![](images/family-results.jpg)
Also, The best-achieved results for each classifier on the subfamily dataset are reported as following. 
![](images/subfamily-results.jpg)

. 

Hyper-parameter Tuning:


Multiple hyper-parameters are examined to find the best result. Here, we explore parameters relating to the best classifier, KNN, and BLAST metric. To improve the results, we tried different K values to find the best f1-score. As the following figure presents, K=1 is the reaches the best f1-score in both datasets. 


![](images/k.jpg)
Expectation value or E-value is BLAST hyper-parameter, required to be explored to find the best results. E-value is the number of different alignments with scores equivalent to or better than S that is expected to occur in a database search by chance. As the following picture presents, we examined different e-values for the KNN classifier. Comparing the results from different e-values ranged from 10 to 1e-10 show 15% improvements in f1-score. As the following figure shows, the results on different e-values, f1-score hits the highest on 1.0e-6 for the family dataset and 1.0e-7 for the subfamily dataset.

![](images/e-value.jpg)

DISCUSSION


As mentioned before, transport proteins are crucial parts of each living cell. They permit specific types of molecules to enter the cell and leave it. This research aims to classify the transport proteins based on their families and subfamilies. TCDB is used as our database in this research. Multiple classifiers are examined through this research and find KNN classification using the BLAST distance metric as the best approach. BLAST algorithm finds similar query sequences to a database based on a specific threshold, which was E-value in this research. Different E-values were tested on the 5-fold of the dataset, and the most accurate result was reached using e-value = 1.0e-6 for the family and e-value = 1.0e-7 for the sub-family. We measured f1-score as a combination of the precision and recall for result evaluation.



We believe that classifying the sequences of amino acids needs specific feature engineering/extraction. Therefore, characterizing the amino acid sequences with a number and computing different features, as on our first feature vectors, may not lead to success. The specific type of this problem necessitates utilizing background knowledge of transporter proteins, and the BLAST algorithm provides this knowledge using protein pairwise alignment. 

The purposed method reached 97.57% f1-score on classifying the sequences based on the 96 families and 97.81% for classifying the sequences based on the 50 different sub-families. The reliability of results is proved by using a 5-fold cross-validation method.
Relying on these results, we have a successful classification of protein sequences into 96 families and 50 sub-families using the BLAST and K-Nearest Neighbor algorithm. 

As future work, we are to investigate the results of the best classifier on the de novo protein sequences. De novo sequencing is the analytical process that derives a peptide’s amino acid sequence from its tandem mass spectrum (MS/MS) without the assistance of a sequence database. It is in contrast to a database search, which searches in a given database to find the target peptide. We are going to investigate the results and answer the question if the BLAST and KNN classification works for de novo protein sequences. 



REFERENCES:


[1] Chang, A. B., Lin, R., Studley, W. K., Tran, C. V., & Saier, Jr, M. H. (2004). Phylogeny as a guide to structure and function of membrane transport proteins. Molecular membrane biology, 21(3), 171-181.

[2] Barghash, A., & Helms, V. (2013). Transferring functional annotations of membrane transporters on the basis of sequence similarity and sequence motifs. BMC Bioinformatics, 14(1), 1–11. https://doi.org/10.1186/1471-2105-14-343

[3] Saier Jr, M. H., Tran, C. V., & Barabote, R. D. (2006). TCDB: the Transporter Classification Database for membrane transport protein analyses and information. Nucleic acids research, 34(suppl_1), D181-D186.

[4] Altschul, S. F., Gish, W., Miller, W., Myers, E. W., & Lipman, D. J. (1990). Basic local alignment search tool. Journal of molecular biology, 215(3), 403-410.


