# CSPaperAssignment
This code is made of several files to construct the final code:
- LSH_function: 
	- contains all the functions used to perform LSH (shingling, creating binary vectors, minhashing, creating the signatures, spliting the signature into b bands and selecting the potential duplicates)
	- LSH function perform the LSH method, it has the data set, b number of bands, r , t the treshold of jaccard similarity used in LSH, sh denoting the type shingling (sh-shingling) as input and give the list of indexes of candidate pairs as output

- Classification:
	- dis_vector : computes the dissimilarity matrix based on the brand, shope, TV type and q-grams similarity
	- classify : based on a fixed treshold it classifies the pair as duplicate or not. With the use of model ids it has as output TP and FP.

- Similarity: computes jaccard similarity and q-grams similarity

- evaluation:
	- dulicates : give the number of duplicated in the given data
	- performance : computes PQ, PC, F1_star and F1
	- F1_star_measure : give F1_star
- bootstarp:
	- perm : gives permutations to apply to give different samples
	- bootstrap_split : splits the data into samples of training and others for testing depending on the train fraction and also creates number of samples based on the number of wanted iteration. it gives as output the train and test samples as well as their original indices, because they are used to get the corresponding brand, shop, TV type and model id.
	- divisor_pairs : gives the potential pairs of b and r based on signature length

- main: gets the data, cleans it and performs bootstraping. The training set is used to tune b and r to select the best values based on F1_star to use them to get on the testing set. All metrics given at the end are averaged
