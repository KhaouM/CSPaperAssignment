# function to compute duplicates:
def dulicates(list):
    unique = set(list)
    dup = len(list) - len(unique)
    return dup

# performance evaluation 
def performance (Nc, Dn, TP, FP, FN):
    # compute Pair Quality
    PQ = TP / Nc
    # compute Pair Completeness
    PC = TP / Dn
    # F1 measure formula
    if PQ + PC == 0:
        F1_star = 0
    else:
        F1_star = (2 * PQ * PC) / (PQ + PC)
    # compute precison
    if TP + FP == 0:
        prec = 0
    else: prec = TP / (TP + FP)
    # compute recall
    if TP + FN == 0:
        rec = 0
    else : rec = TP / (TP + FN)
    # compute F1 measure
    if prec + rec == 0:
        F1 =0
    else:
        F1 = (2 * prec * rec) / (prec + rec)
    return PQ, PC, F1_star, F1

# create only a function of F1 measure
def F1_measure (TP, FP, FN):
    # compute precison
    if TP + FP == 0:
        prec = 0
    else: prec = TP / (TP + FP)
    # compute recall
    if TP + FN == 0:
        rec = 0
    else : rec = TP / (TP + FN)
    # compute F1 measure
    if prec + rec == 0:
        F1 =0
    else:
        F1 = (2 * prec * rec) / (prec + rec)
    return F1
# create a function for F1 star

def F1_star_measure (TP, Nc, Dn):
    # compute Pair Quality
    PQ = TP / Nc
    # compute Pair Completeness
    PC = TP / Dn
    # F1 measure formula
    if PQ + PC == 0:
        F1_star = 0
    else:
        F1_star = (2 * PQ * PC) / (PQ + PC)
    return F1_star