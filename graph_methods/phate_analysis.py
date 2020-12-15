import numpy as np
import phate
import scprep

ADJ_MATRIX_DEST = '../data/boosted_adj_matrix.npy'

# load adj_matrix
with open(ADJ_MATRIX_DEST, 'rb') as f:
  data = np.load(f)

# TODO import classifications
# classes = None

# instantiate phate obj
phate_op = phate.PHATE()

# transform data
data_phate = phate_op.fit_transform(data)

# plot
scprep.plot.scatter2d(data_phate) # , c = classes