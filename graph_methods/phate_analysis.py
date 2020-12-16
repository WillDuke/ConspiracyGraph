import numpy as np
import scipy.sparse
import phate
import scprep

SCORE_PATH = "../data/valid_scores.npy"
ADJ_MATRIX_PATH = '../data/combined_adj_matrix.npz'

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

# load adj_matrix
data = scipy.sparse.load_npz(ADJ_MATRIX_PATH)

# import classifications
classes = load_classes()

# instantiate phate obj
phate_op = phate.PHATE()

# transform data
data_phate = phate_op.fit_transform(data)

# plot
scprep.plot.scatter2d(data_phate, c = classes)