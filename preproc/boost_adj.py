import numpy as np 
import scipy.sparse
from scipy.sparse import find
import tqdm

ADJ_PATH = "../data/adj_matrix.npz" 
TAG_PATH = "../data/bag_tags.npz"
NEW_ADJ_PATH = "../data/boosted_adj_matrix.npz"

def load_old_adj() : 
    # npz file, no name assigned to np array so use key 'arr_0'
    adj = np.load(ADJ_PATH, allow_pickle=True)['arr_0']
    return adj

def load_tags() : 
    # sparse array len(ids) x len(corpus)
    # tags = np.load(TAG_PATH, allow_pickle=True)
    tags = scipy.sparse.load_npz(TAG_PATH)
    # print("Tags?", tags)
    return tags

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


def boost_adj() : 
    # load old adj matrix
    new_adj = load_old_adj() 

    # load the tag features (should be already ordered same as adj) 
    tag_feats = load_tags()
    # simple naive range through to add small edges
    # fine with the duplicated passes to keep matrix symmetric 
    num_vids = tag_feats.shape[0]
    for i in tqdm.tqdm(range(num_vids-1)) : 
        # grab encoding for this video 
        my_tags = tag_feats[i] 
        # for each other video, add edges when tags match
        for j in range(i+1, num_vids) :  
            # formula: log(#matching tags) 
            # Very slow to use == comparisons for sparse
            # instead use find() or .nonzero() to pull values
            _, my_spots = my_tags.nonzero()
            _, their_spots = tag_feats[j].nonzero()
            matches = 0.1 * np.log(len(np.intersect1d(my_spots, their_spots, assume_unique=True)) + 1)
            new_adj[i][j] = matches
            new_adj[j][i] = matches

    # what have you done??
    peek_adj(new_adj) 

    with open(NEW_ADJ_PATH, "wb") as file : 
        np.savez_compressed(file, new_adj)

    return 

def compress_boost_adj() : 
    OLD_BOOST = "../data/boosted_adj_matrix.npy"
    adj = np.load(OLD_BOOST, allow_pickle=True)
    np.savez_compressed(NEW_ADJ_PATH)
    return 

if __name__ == '__main__':
    # Boost the adjacency matrix edges with tag features
    # peek_adj(load_old_adj())
    boost_adj()
    # compress_boost_adj()