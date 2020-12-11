import numpy as np
import torch

FEAT_PATH = "../data/bag_features.npz"
ADJ_PATH = "../data/adj_matrix.npz"
SCORE_PATH = "../data/valid_scores.npy"

def convert_sparse_matrix_to_sparse_tensor(X):
    coo = X.tocoo()
    values = coo.data
    indices = np.vstack((coo.row, coo.col))
    i = torch.LongTensor(indices)
    return i

def load_features() : 
    return 

def load_adj() : 
    return 

def score_classes(score) : 
    if float(score) < 0.5 : 
        return 0
    elif float(score) < 0.65 : 
        return 1
    elif float(score) < 0.85 : 
        return 2
    else : 
        return 3

def load_scores() : 
    # bin the scores 0|0.5|0.65|0.85|1.0 into classes
    
    # print stats
    print("Created these class divisions: ")
    print("Class 0 ", len(np.where(scores == 0)[0]))
    print("Class 1 ", len(np.where(scores == 1)[0]))
    print("Class 2 ", len(np.where(scores == 2)[0]))
    print("Class 3 ", len(np.where(scores == 3)[0]))
    return 

# Return the pytorch geometric data object
def load_YouTube() : 
    # grab the features from baggify
    features = load_features()
    # grab the adjacency matrix
    adj = load_adj() 
    # grab the conspiracy scores
    scores = load_scores() 

    x = torch.FloatTensor(features)
    edge_index = convert_sparse_matrix_to_sparse_tensor(adj)

    # Convert to data object, just for cleanliness
    data = torchData.Data(x=x, edge_index=edge_index)
    data.y = torch.tensor(scores, dtype=torch.long)

    return data