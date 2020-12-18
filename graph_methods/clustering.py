import pickle
import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.sparse import load_npz

with open('../data/training_set_features.pkl', 'rb') as f:
    features = pickle.load(f)

clustering = SpectralClustering(
    n_clusters=2, affinity = 'nearest_neighbors'
).fit(features)

from sklearn.cluster import AgglomerativeClustering

agglom_cluster = AgglomerativeClustering(affinity = 'cosine', linkage = 'average')
agglom_cluster.fit(features.toarray())

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(children, **kwargs):

    distance = position = np.arange(children.shape[0])

    linkage_matrix = np.column_stack([children, distance, position]).astype('float')

    fig, ax = plt.subplots(figsize = (10, 5))
    ax = dendrogram(linkage_matrix, **kwargs)
    plt.tick_params(axis = 'x', bottom = 'off', top = 'off', labelbottom = 'off')
    plt.tight_layout()
    plt.show()


children = agglom_cluster.children_
plot_dendrogram(children)