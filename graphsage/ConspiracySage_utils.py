import numpy as np
import scipy.sparse
import torch

FEAT_PATH = "../data/bag_features.npz"
ADJ_PATH = "../data/boosted_adj_matrix.npy"
SCORE_PATH = "../data/valid_scores.npy"

def convert_sparse_matrix_to_sparse_tensor(X):
    coo = X.tocoo()
    values = coo.data
    indices = np.vstack((coo.row, coo.col))
    i = torch.LongTensor(indices)
    return i

def load_features() : 
    return scipy.sparse.load_npz(FEAT_PATH)

def load_adj() : 
    return np.load(ADJ_PATH)

def score_classes(score) : 
    if float(score) < 0.5 : 
        return 0
    elif float(score) < 0.65 : 
        return 1
    elif float(score) < 0.85 : 
        return 2
    else : 
        return 3

def load_classes() : 
    # bin the scores 0|0.5|0.65|0.85|1.0 into classes
    scores = np.load(SCORE_PATH)
    classes = [score_classes(s) for s in scores]

    # print stats
    print("Created these class divisions: ")
    print("Class 0 ", len(np.where(classes == 0)[0]))
    print("Class 1 ", len(np.where(classes == 1)[0]))
    print("Class 2 ", len(np.where(classes == 2)[0]))
    print("Class 3 ", len(np.where(classes == 3)[0]))
    return classes

# Return the pytorch geometric data object
def load_YouTube() : 
    # grab the features from baggify
    features = load_features()
    # grab the adjacency matrix
    adj = load_adj() 
    # grab the conspiracy scores
    classes = load_classes() 

    x = torch.FloatTensor(features)
    edge_index = convert_sparse_matrix_to_sparse_tensor(adj)

    # Convert to data object, just for cleanliness
    data = torchData.Data(x=x, edge_index=edge_index)
    data.y = torch.tensor(classes, dtype=torch.long)

    return data