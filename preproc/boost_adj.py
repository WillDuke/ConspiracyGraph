import numpy as np 

ADJ_PATH = "../data/adj_matrix.npz"

# Take a look at our adjacency matrix
def peek_adj() : 
    test = np.load(ADJ_PATH, allow_pickle=True)
    print(test)
    print(test.size) 
    edge_weights = [] 
    edges = []
    for row in test : 
        edge_weights.append(row.sum())
        edges.append(len(np.where(row != 0)[0]) - 1)

    # Summary stats
    edges = np.asarray(edges)
    for i in range(edges.max()+1) : 
        num_nodes = len(np.where(edges == i)[0]) 
        if num_nodes > 0 : 
            print("There are {0} nodes with {1} edges ({2:3.2f}%)".format(num_nodes, i, 100*num_nodes/len(edges)))
    
    return 


if __name__ == '__main__':
    # Boost the adjacency matrix edges with tag features
    peek_adj()