import phate
import scprep
import numpy as np 

ADJ_PATH = "../data/boosted_adj_matrix.npz"
SCORE_PATH = "../data/valid_scores.npy"

def load_adj() : 
    return np.load(ADJ_PATH, allow_pickle=True)['arr_0']


def score_classes(score) : 
    if float(score) < 0.65 : 
        return 0
    elif float(score) < 0.80 : 
        return 1
    elif float(score) < 0.90 : 
        return 2
    else : 
        return 3

def load_classes() : 
    # bin the scores 0|0.5|0.65|0.85|1.0 into classes
    scores = np.load(SCORE_PATH)
    classes = np.asarray([score_classes(s) for s in scores])

    # print stats
    print("Created these class divisions: ")
    print("Class 0 ", len(np.where(classes == 0)[0]))
    print("Class 1 ", len(np.where(classes == 1)[0]))
    print("Class 2 ", len(np.where(classes == 2)[0]))
    print("Class 3 ", len(np.where(classes == 3)[0]))
    return classes

# TODO load adj_matrix
adj = load_adj() 
classes = load_classes() 

num_nodes = len(adj) 

same = 0
diff = 0
for i in range(num_nodes) : 
    # same classes? 
    
    for j in range(num_nodes) : 
        if adj[i][j] != 0 and i != j : 
            same += int(classes[i] == classes[j])
            diff += int(classes[i] != classes[j])
    # print("I'm class {} and I have {} same and {} diff neighbors".format(classes[i], same, diff))
print("Overall, we had {0} dif and {1} same, resulting in {2:3.4f} ratio".format(diff, same, same/diff))
''' 
adj = load_adj()
num_nodes = len(adj) 
for i in range(num_nodes) : 
    for j in range(num_nodes) : 
        if adj[i][j] == 0 : 
            adj[i][j] = 10
        elif i == j :
            adj[i][j] = 0
        else :  
            adj[i][j] = max(0.1, 10 - 10*adj[i][j])
data = adj 

# TODO import classifications
classes = np.load(SCORE_PATH)

# instantiate phate obj
phate_op = phate.PHATE(knn_dist='precomputed') #, k=1) # k=15, t=100,  

# transform data
data_phate = phate_op.fit_transform(data)

# plot
scprep.plot.scatter2d(data_phate, c = classes)
'''