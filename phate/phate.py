import phate
import scprep

# TODO load adj_matrix
data = None

# TODO import classifications
classes = None

# instantiate phate obj
phate_op = phate.PHATE()

# transform data
data_phate = phate_op.fit_transform(data)

# plot
scprep.plot.scatter2d(data_phate, c = classes)