# BigDataProject
ABSTRACT

According to rapid improvements in genome sequencing, protein functional annotation is turned into the focus of interest in many academic efforts. In this project, we analyze the Transporter Classification Database (TCDB). The TCDB is a comprehensive database for membrane transport proteins, which is approved by the International Union of Biochemistry and Molecular Biology (IUBMB), known as the Transporter Classification (TC) system. The main goal of this analysis is to classify membrane transport proteins into families with the same functionality. Supposing sequences with similar features might have similar functionalities, clustering protein sequences based on their features could be a practical method for protein functional annotation.


INTRODUCTION


Despite the fact that the amino acid sequences of many membrane proteins are available now, their specific functions remain unknown. There is a consistent need for computational methods that predict the function of membrane proteins. Supposing sequences with similar features might have similar functionalities, classifying protein sequences based on their features could be a practical method for protein functional annotation.
Transporter proteins is a term used for addressing proteins that serve the function of moving different substances across the cell. These are traffic gates that organize a variety of vital cellular functions including cell signaling, trafficking, metabolism and energy production. Generally, finding the functions of each proteins with experimental methods is not an easy task, because the function may be related specifically to the native environment in which a particular organism lives; such an environment is hard to simulate in a lab. There are different types of transporter proteins responsible for various tasks. In this research, we use different methods to classify transfer protein sequences on the TCDB database based on their TC families and super families. 
The TC system is a classified transporters dataset, analogous to the Enzyme Commission (EC) system for classification of enzymes, except that it incorporates both functional and phylogenetic information.
Sequences in the TCDB database are organized in a five level hierarchical system as follows: N1.L1.N2.N3.N4. As a matter of fact, transporters are classified on the basis of five criteria, and each of these criteria corresponds to one of the five numbers or letters within the TC number for a particular type of transporter. Here we classify the protein sequences based on N2 and N3. N2 represents the transporter super families of which there are over 1000 in TCDB and N3 represents the family or phylogenetic clusters within a family.


MATERIALS AND METHODS

1.DATASET

In this research, we use different methods to classify transfer protein sequences on the TCDB database. TCBD is an abbreviation for Transporter Classification Database, which is a web accessible database containing sequence, classification, structural, functional and evolutionary information about transport systems from a variety of living organisms. Transporter Classification Database is a database containing 10,000 non-redundant transporter proteins. The database details a comprehensive classification system for membrane transport proteins, Transporter Classification or TC system, approved by International Union of Biochemistry and Molecular Biology. The dataset includes transporter protein sequences, their descriptions, TC numbers, and examples of 1409 families. This dataset is downloaded from the TCDB website and the protein sequences in this dataset are in FASTA file format. 

2. Methods:

2.1 Feature Extraction

In protein sequence alignment multiple features are considered as valuable. We explore several features this includes positional and combinational features: Amino Acid Composition (AAC),  pair amino acid composition (PAAC) is the normalized frequency of each pair of amino acids, Pseudo Amino Acid Composition (PseAAC), Amino acid indices (AAindex), and Position-Specific Scoring Matrix (PSSM). 
In addition to positional and combinational features, evolutional features might be useful on classifying transfer protein sequences. Alignment of protein sequences reveals practical evolutional information of protein sequences. BLAST and PsiBLAST methods are used for protein sequence alignments. Basic Local Alignment Search Tool or BLAST algorithm, is a local sequence alignment method.  This algorithm compares nucleotide or protein sequences to sequence databases and calculates the statistical significance of matches. The BLAST program takes a query DNA or protein sequence as input, and search DNA or protein sequence databases for similarities. Protein similarities could be used on predicting the families and super families of each sequence. 
According to number of presented features, methods of feature engineering are required to extract the most related feature vector.  

2.2 classifiers:

Support Vector Machines (SVMs) has shown as the most reliable classifier on predicting protein sequences. In this research, SVMs are to be tested with different feature vectors. Other types of classifiers are to be trained and tested with the extracted data. Random Forrest and ensembled methods are going to be explored in this research. K-folds cross validations is going to implement to assist on more accurate results. 

   


