import numpy as np
import random
import itertools
from Similarity_fct import jaccard_similarity

# This function contains, singling, making binary vertors, minhashing, creating signitures as well as performing LSH


# shingling function
def shingle(text: str, N: int):
    shingled = []
    # devide the text into parts with k length
    for i in range(len(text) - N + 1):
        shingled.append(text[i:i+N])
    return set(shingled)

# functions for hash function
# Helper function to check if a number is prime
def is_prime(n):  
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
# Find the largest prime number smaller than k
def generate_random_prime(k):
    n = k - 1 if k > 1 else k  # Start from k - 1 if k > 1, otherwise use k
    while n > 1 and not is_prime(n):
        n -= 1
    return n

# Hash function hab(x) = (a + bx) mod p
def hab_hash(x, a, b, p):
    # Hash function hab(x) = (a + bx) mod p
    return (a + b * x) % p

# create hash function to compare the bands
# this hash function is equal to (number modulo size)
def hf_LSH(vector: list, size: int):
    # put the elements of a vector into one number
    number = int(''.join(map(str, vector)))
    return (number % size)

# LSH : splitting signature into b parts, b in number of bands
def splitting(signature, b):
    # make sure that the size of signature can be divided by b
    assert len(signature) % b == 0
    # r = length / b , make sure it is an integer
    r = int(len(signature) / b)
    subvectors = []
    # for loop by r elements 
    for i in range (0, len(signature), r):
        # each subvector has r elements
        subvectors.append(signature[i: i+r])
    return subvectors

def LSH (List: list, b: int, r: int, t: float, sh: int):
    shingled_vectors = [] # list of shingles of the elments of List
    # create the shingles of List
    for i in range (len(List)):
        # sh-Shingling and add them to list of shingles
        shingled_vectors.append(shingle(List[i], sh))
    
    # Create a vector equal to the union of every shingle      
    Union_vector = shingled_vectors[0] # initialize the union vector with the first element of the shingled vector
    for i in range (len(shingled_vectors)):
        Union_vector = Union_vector.union(shingled_vectors[i])
    
    # Create binary vectors of each element by comparing to the Union_vector
    Binary_vectors = []
    
    for i in range (len(shingled_vectors)):
        Binary_vectors.append([1 if x in shingled_vectors[i] else 0 for x in Union_vector])
    
    N = b * r # set the length of the signature
    l_BV = len(Binary_vectors[0]) # length of the binary vectors
    
    # chose a primary number large enough to avoid collisions
    p = generate_random_prime(100)

    # create rxb minhash vectors using this hash function  hab(x) = (a +dx)mod(p)
    hash_funcs= []
    for i in range(N):
        hash_func = []
        # for each raw a and b are different
        a = random.randint(1, 20)
        d = random.randint(1, 20)
        for j in range (l_BV):
            hash_func.append(hab_hash(j, a, d, p))
        hash_funcs.append(hash_func)


    # intialize signature matrix by putting inf values every where
    signature_Matrix = [[float('inf') for _ in range(N)] for _ in range(len(Binary_vectors))]
    # go through every binary vector of every element to create a r x b digits long signature 
    for i in range (len(Binary_vectors)):
        for j in range (l_BV):
            # if the element is 1 and the value of the hash function is less than the value in signature,
            # replace it with hash function value
            if Binary_vectors[i][j] == 1:
                for l in range (N):
                    if signature_Matrix[i][l] > hash_funcs[l][j]:
                        signature_Matrix[i][l] = hash_funcs[l][j]             


    # create a list b_bands that, to split the signature into b bands of r elements 
    b_Bands = []
    for i in range(len(signature_Matrix)):
        b_Bands.append(splitting(signature_Matrix[i], b))

    # apply the same hash function to all bands, the hash function is h(x) = x modulo(very big number)
    hash_bands = []
    for i in range(len(b_Bands)):
        hash_band = []
        for j in range(b):
            hash_band.append(hf_LSH(b_Bands[i][j], 9 * 10**12))
        hash_bands.append(hash_band)
    
    
    # this function puts similar bands in the same buckets and returns the set of similar pairs
    def find_similar_pairs(hash_bands, bands, threshold):
        similar_pairs = set()

        # Iterate over each band
        for band in range(bands):
            band_buckets = {}

            # Iterate over each item and hash value in the current band
            for i, hashed_band in enumerate(hash_bands):
                band_value = hashed_band[band]

                # Create buckets for each unique hash value in the current band
                if band_value in band_buckets:
                    band_buckets[band_value].append(i)
                else:
                    band_buckets[band_value] = [i]

            # Iterate over buckets in the current band
            for _, bucket in band_buckets.items():
                # If a bucket has more than one item, check for similar pairs
                if len(bucket) > 1:
                    for pair in itertools.combinations(bucket, 2):
                        # Calculate Jaccard similarity for each pair
                        jaccard_sim = jaccard_similarity(hash_bands[pair[0]], hash_bands[pair[1]])
                        
                        # If the Jaccard similarity is above the threshold, add the pair to the result set
                        if jaccard_sim > threshold:
                        #if hash_bands[pair[0]] ==  hash_bands[pair[1]]:
                            similar_pairs.add(pair)

        # Return the set of similar pairs
        return similar_pairs
    
    # convert the set of pairs into a list
    cand_pairs_indx = list(find_similar_pairs(hash_bands, b, t))
    return cand_pairs_indx