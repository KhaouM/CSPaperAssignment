import json
import re
import pandas as pd
import numpy as np
import random
import itertools
import math
from collections import defaultdict
from LSH_function import LSH
from evaluation import performance
from evaluation import F1_star_measure
from classification import dissim_vec
from classification import classify
from bootstarp import bootstrap_split
from bootstarp import divisor_pairs
from evaluation import dulicates



# Load the JSON data
file_path = 'TVs-all-merged.json'
with open(file_path, 'r') as file:
    # Read the content of the file
    json_content = file.read()
    # Parse the JSON content
    data = json.loads(json_content)

    uncleaned_Title_List = []  # create a list of titles
    model_ids = []  # create a corresponding list of model_ids
    feature_maps = []
    joined_data = []
    # Extracting values for the "Brand", "shop" and "TV Type" keys or assigning an empty string if not present
    brands = [item['featuresMap'].get('Brand', '') for modelID_items in data.values() for item in modelID_items]
    shops = []
    TVtypes = [item['featuresMap'].get('TV Type', '') for modelID_items in data.values() for item in modelID_items]

    # Iterate through each key (modelID) and create a list of Titles, and all features
    for model_id, details_list in data.items():
        for details in details_list:
            joined = ''
            # get the title
            title = details.get('title')
            # get model id
            ID = details.get('modelID')           
            shop = details.get('shop', '')
            features = ''
            for value in details["featuresMap"].items():
                if value[1] != 'Yes' and value[1] != 'No':
                    features += ' ' + value[1]
            # add the title and model id to the corresponding lists
            uncleaned_Title_List.append(title)
            model_ids.append(ID)
            shops.append(shop)
            feature_maps.append(features)
            joined = f"{title} {features}"
            joined_data.append(joined)
    
    # clean data by define a function clean_title
    def cleaning(title):
        # Remove non-alphanumeric characters and spaces
        cleaned_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        #cleaned_title = re.sub(r'[^a-zA-Z0-9]', '', title)
        # Convert to lowercase
        cleaned_title = cleaned_title.lower()
        return cleaned_title
    
    # clean every element of joined data 
    Elements = [cleaning(elem) for elem in joined_data]
    
    # select a treshhold t
    T = [0.001, 0.002, 0.005, 0.008, 0.01, 0.025, 0.05, 0.085]

    # number of itirations of boosstrap
    iter = 10
    
    # create train and test samples, for a bootstrap
    train, test, train_ind, test_ind = bootstrap_split(Elements, 0.6, iter)

    #performance matrix depending on the value of t 
    P = np.zeros((4, len(T)))
    frac_comp = np.zeros(len(T))
    
    for index, t in enumerate(T):
        print('t')
        print(t)
        # define total performance matrix
        Total_per = [[0] * iter for _ in range(4)]
        # go through each sample
        for sample in range (len(test)) :
            print("sample")
            print(sample)
            # define ID models lists corresponding to the sample
            ID_train = [model_ids[i] for i in train_ind[sample]]
            ID_test = [model_ids[i] for i in test_ind[sample]]
            # for each sample compute the number of duplicates for train and test samples
            Dn_train = dulicates(ID_train)
            Dn_test = dulicates(ID_test)

            # get the possible pairs of b and r
            Par_pairs = divisor_pairs(100)

            # initialize the selected parameters
            b_selec = 1
            r_selec = 1
            F1_star_selec = 0

            # tunning b and r on train sample
            for pair in Par_pairs:    
                b, r = pair
                # apply LSH on the train sample to get the candidates pairs
                cand_pairs_indx = LSH(train[sample],b ,r, 0.3, 4)
                # the number of  the number of comparisons made
                Nc = len(cand_pairs_indx)
                # compute dissimilarity vector
                dissVec = dissim_vec(cand_pairs_indx, train[sample], brands, shops, TVtypes,train_ind[sample])
                # perform class
                clas = classify(cand_pairs_indx, ID_train, dissVec, t)
                TP = clas[0]
                # chose the best pair based of F1 measure
                F1_star = F1_star_measure (TP, Nc, Dn_train)
                if F1_star > F1_star_selec:
                    F1_star_selec = F1_star
                    b_selec = b
                    r_selec = r
                # print("b,r")
                # print(b,r)
                # print(TP, FP, FN)
                # print(F1)
            # apply the same process to the test sample with the optimal parameters
            cand_pairs_indx = LSH(test[sample],b_selec ,r_selec, 0.3, 4)
            # the number of  the number of comparisons made
            Nc = len(cand_pairs_indx)
            # compute dissimilarity vector
            dissVec = dissim_vec(cand_pairs_indx, test[sample], brands, shops, TVtypes,test_ind[sample])
            # perform class
            clas = classify(cand_pairs_indx, ID_test, dissVec, t)
            TP = clas[0]
            FP = clas[1]            
            FN = Dn_train - TP
            # evaluate the performance
            per = performance (Nc, Dn_test, TP, FP, FN)
            for k in range (4):
                Total_per[k][sample] = per[k]
            
            # compute fractions comparision
            L = len(test[sample])
            comb = (L * (L - 1)) / 2 # possible combinations
            frac_comp[index] = frac_comp[index] + Nc / comb
        # compute the average values of the total iterations
        for k in range (4):
            for l in range (iter):
                P[k][index] = P[k][index] + Total_per[k][l]
            P[k][index] =  P[k][index] / iter 
        
        frac_comp[index] = frac_comp[index] / iter

        print(P)
        print(frac_comp)

        y_values = np.array(P)
        x_values = np.array(frac_comp)
        sorted_indices = np.argsort(x_values)

        x_values_sorted = x_values[sorted_indices]
        y_values_sorted = y_values[:, sorted_indices]

        fig, axs = plt.subplots(nrows=len(y_values), ncols=1, figsize=(8, 6 * len(y_values)))

        for i in range(len(y_values_sorted)):
            axs[i].plot(x_values_sorted, y_values_sorted[i], marker='o', label=f'Array {i+1}')
            axs[i].set_xlabel('X-axis')
            axs[i].set_ylabel('Y-axis')
            axs[i].legend()

        plt.tight_layout()
        plt.show()



















    

    
    
    


  


           
        

