from Bio.SeqUtils.ProtParam import ProteinAnalysis
import numpy as np

def omega(seq1, seq2):
    pass


def convert_to_pseaac(dataset):
    for sequence in dataset:
        this_lambda = len(sequence) - 2

        list_theta = []
        for theta in range(1, this_lambda + 1):
            upper_bound = len(sequence) - theta
            sum_omega = 0
            for i in range(upper_bound):
                sum_omega += omega(sequence.seq[i], sequence.seq[i + theta])
            my_theta = (1 / upper_bound) * sum_omega
            list_theta.append(my_theta)


