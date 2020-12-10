import json
import numpy as np
from math import log

ADJ_MATRIX_DEST = 'data/adj_matrix_half.npy'
RAW_RELATED_IDS = 'data/related_ids.json'

def score_ids(video_ids, related_ids):
    """Score each video based on its position in related_ids"""

    def score(id):

        if id in related_ids:
            return 1 / log(related_ids.index(id) + 2)
        else:
            return 0

    return np.array([score(id) for id in video_ids])

def create_adjacency_matrix(related_dict):
    """Create an adjacency matrix using score_ids as distance between videos."""

    all_ids = list(related_dict.keys())

    # list of arrays of scores for each video
    scores = [score_ids(all_ids, rel) for rel in related_dict.values()]

    # stack the scores into matrix
    mat = np.vstack(scores)

    # add transpose to make symmetric 
    sym = np.add(mat, mat.T)

    # set the diagonal (matching ids) to 2 (max score is ~1.44)
    np.fill_diagonal(sym, 2)

    return sym

if __name__ == "__main__":
    
    # load dictionary of related videos
    with open(RAW_RELATED_IDS) as f:
        related_dict = json.load(f)

    mat = create_adjacency_matrix(related_dict)
    
    # save as numpy binary
    with open(ADJ_MATRIX_DEST, 'wb') as f:
        np.save(f, mat)

    # how to load
    # with open(ADJ_MATRIX_DEST, 'rb') as f:
    #   mat = np.load(f)