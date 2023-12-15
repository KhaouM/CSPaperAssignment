from Similarity_fct import jaccard_similarity2
from Similarity_fct import qgram_similarity

# compare brand, shop and 
# compute dissimilarity matrix
# same brand, different shop and same TV type

def dissim_vec(cand_pairs_indx, Elements, brands, shops, TVtype, indexes):
    # ininitial all values at -inf
    dis_vector = [float('-inf') for _ in range(len(cand_pairs_indx))]

    for i in range (len(cand_pairs_indx)):
        # after permutation of bootstrapping elements are not in the same index anymore
        ind1 = indexes[cand_pairs_indx[i][0]]
        ind2 = indexes[cand_pairs_indx[i][1]]
        if brands[ind1] == brands[ind2] and shops[ind1] != shops[ind2] and TVtype[ind1] == TVtype[ind2]:
            distance = qgram_similarity(Elements[cand_pairs_indx[i][0]], Elements[cand_pairs_indx[i][1]], 3)
            dis_vector[i] = distance
    return dis_vector

# Classifying into duplicates or not duplicates, it returns TP and FP
def classify(cand_pairs_indx, model_IDs, dis_vector, t): 
    TP = 0
    FP = 0
    for i in range (len(dis_vector)):
        if dis_vector[i] > t:            
            if model_IDs[cand_pairs_indx[i][0]] == model_IDs[cand_pairs_indx[i][1]]:
                TP += 1
            else:
                FP += 1
    return TP, FP