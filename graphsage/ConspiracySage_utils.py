import numpy as np
import scipy.sparse
import torch
import torch_geometric.data as torchData

FEAT_PATH = "../data/bag_features.npz"
ADJ_PATH = "../data/boosted_adj_matrix.npz"
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


# Take a look at our adjacency matrix
def peek_adj(test) : 
    print(test)
    print(test.size) 
    edge_weights = [] 
    edges = []
    for row in test : 
        edge_weights.append(row.sum())
        # how many edges are nonzero, excluding diagonal
        edges.append(len(np.where(row != 0)[0]) - 1)

    # Summary stats
    edges = np.asarray(edges)
    for i in range(edges.max()+1) : 
        num_nodes = len(np.where(edges == i)[0]) 
        if num_nodes > 0 : 
            print("There are {0} nodes with {1} edges ({2:3.2f}%)".format(num_nodes, i, 100*num_nodes/len(edges)))
    
    return 


# Return the pytorch geometric data object
def load_YouTube() : 
    # grab the features from baggify
    features = load_features()
    # grab the adjacency matrix
    adj = load_adj() 
    # delete the self-loops 
    for i in range(len(adj)) : 
        adj[i][i] = 0 

    # peek_adj(adj)
    # grab the conspiracy scores
    classes = load_classes() 

    x = torch.FloatTensor(features.toarray()) # convert_sparse_matrix_to_sparse_tensor(features) # torch.FloatTensor(features)
    edge_index = convert_sparse_matrix_to_sparse_tensor(scipy.sparse.csr_matrix(adj))

    # Suspicious of edges
    # torch.LongTensor(adj) # 
    # for i in range(50) : 
    #     print(edge_index[i].nonzero())

    # Convert to data object, just for cleanliness
    data = torchData.Data(x=x, edge_index=edge_index)
    data.y = torch.tensor(classes, dtype=torch.long)

    return data