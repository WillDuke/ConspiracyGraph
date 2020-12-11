import numpy as np 
import scipy.sparse


ADJ_PATH = "../data/adj_matrix.npz" 
TAG_PATH = "../data/bag_tags.npy"
NEW_ADJ_PATH = "../data/boosted_adj_matrix.npy"

def load_old_adj() : 
    # npz file, no name assigned to np array so use key 'arr_0'
    adj = np.load(ADJ_PATH, allow_pickle=True)['arr_0']
    return adj

def load_tags() : 
    # np array len(ids) x len(corpus)
    tags = np.load(TAG_PATH, allow_pickle=True)
    return tags

# Take a look at our adjacency matrix
def peek_adj(test) : 
    # test = scipy.sparse.load_npz(ADJ_PATH).toarray()
    # test = load_old_adj() 

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
    num_vids = len(tag_feats)
    for i in range(num_vids) : 
        # grab encoding for this video 
        my_tags = tag_feats[i] 
        # for each other video, add edges when tags match
        for j in range(num_vids) :  
            # formula: log(#matching tags) 
            new_adj[i][j] += np.log((my_tags == tag_feats[j]).sum())

    # what have you done??
    peek_adj(new_adj) 

    with open(NEW_ADJ_PATH, "wb") as file : 
        np.save(file, new_adj)

    return 

if __name__ == '__main__':
    # Boost the adjacency matrix edges with tag features
    # peek_adj(load_old_adj())