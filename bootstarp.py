import numpy as np
from random import shuffle
import random

# create permutations
def perm(size: int):
    # create a list of numbers from 1 to size +1
    hash_ex = list(range(1, size + 1))
    # create permutation of the numbers usings shuffle function
    shuffle(hash_ex)
    return hash_ex

def bootstrap_split(data, train_fraction, num_bootstrap_samples):
    # initial lists of train and test sample
    train_samples = []
    test_samples = []

    # splitting the models ids list to use them for the evaluation
    train_ind =[]
    test_ind = []

    # create num_bootstrap_samples of train and test samples
    for _ in range(num_bootstrap_samples):
        
        #  shuffle the indices (1 to len(data) +1)
        indices = perm(len(data))

        # Split the bootstrap sample into train and test based on the specified fraction
        train_size = int(len(data) * train_fraction)
        # make sure that train size + test size = len(data)
        test_size = len(data) - train_size
       
        # Create train and test samples ensuring they are disjoint
        train_set = []
        train_set_ind = []
        for indx in range (train_size):
            # -1 is because of the definition of hash_function that starts at 1 (not 0)
            train_set.append(data[indices[indx]-1])
            train_set_ind.append(indices[indx]-1)
      
        test_set = []
        test_set_ind = []
        for indx in range (test_size):
            test_set.append(data[indices[train_size + indx]-1])
            test_set_ind.append(indices[train_size + indx]-1)

        # Append the train and test sets to the respective lists
        train_samples.append(train_set)
        test_samples.append(test_set)
        train_ind.append(train_set_ind)       
        test_ind.append(test_set_ind)

    return train_samples, test_samples, train_ind, test_ind

# find pairs of divisors that don't include 1 as divisor
def divisor_pairs(N):
    divisor_pairs = []
    # starting at 2 to avoid 1 as divisor
    for i in range(2, N + 1):
        # making sure the other element of the pair is not 1
        if N % i == 0 and N // i != 1:
            divisor_pairs.append((i, N // i))
    return divisor_pairs

#data = [0,0,11,4,5,6,7]
#print(bootstrap_split(data, 0.7, 2))