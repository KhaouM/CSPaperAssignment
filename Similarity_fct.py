def jaccard_similarity(a, b):
    set1 = set(a)
    set2 = set(b)
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    else:
        return float(intersection) / union


def jaccard_similarity2(title1, title2):
    # Tokenize the titles into sets of words
    words1 = set(title1.lower().split())
    words2 = set(title2.lower().split())

    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    # Avoid division by zero
    if union == 0:
        return 0.0

    similarity = intersection / union
    return similarity

def qgram_similarity(str1, str2, q):
    qgrams1 = set([str1[i:i+q] for i in range(len(str1)-q+1)])
    qgrams2 = set([str2[i:i+q] for i in range(len(str2)-q+1)])
    intersection = len(qgrams1.intersection(qgrams2))
    union = len(qgrams1.union(qgrams2))
     # Avoid division by zero
    if union == 0:
        return 0.0
    return intersection / union




