import json 
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse
import numpy as np 

RAW_DATA_PATH = "../data/conspiracy_results.json"
COM_PATH = "../data/comments.json"

def load_json(path) : 
    with open(path, "r") as file : 
        d = json.load(file)
    return d

# Flag-ship function here
def baggify(feature_list) : 
    # The feature_list is a corpus- a list of strings, each string being a "document"/sample
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(feature_list) 
    return X 

def tag_cleanup(dict_list) : 
    # Clean up pesky tagless videos
    tags = list(dict_list)
    tag_features = []
    for i, s in enumerate(tags) : 
        if s == None : 
            x = ' '
        else : 
            x = ' '.join(s) 
        tag_features.append(x)
    return tag_features

def com_cleanup(dict_list) : 
    # aggregate the comments for each video 
    comments = [] 
    for i, c in enumerate(dict_list) : 
        x = ' '
        if c != None : 
            # we have a big ol' list of dictionaries
            # each comment is a dictionary 
            words = [d['text'] for d in c]
            x = x.join(words)
        comments.append(x)
    return comments 

def extract_features(data_dict, ids) : 
    '''
    UPDATE: 12/11 
    Features are the video title, description, and comments
    Tags will be returned for use in building edges
    '''

    # Going to keep a separate corpus for 
    # the title, the description, and the tags
    title_bag = baggify([data_dict['title'][i] for i in ids])
    tag_bag = baggify(tag_cleanup([data_dict['tags'][i] for i in ids])) # is the tag bag a concern? '|' instead of spaces
    des_bag = baggify([data_dict['description'][i] for i in ids])

    com_dict = load_json(COM_PATH) 
    com_bag = baggify(com_cleanup([com_dict[i] for i in ids])) # 0 # waiting for comments data

    # Merge those sparse matrices, return the features
    features = scipy.sparse.hstack([scipy.sparse.hstack([title_bag,des_bag]), com_bag]) 

    return features, tag_bag


# A little extraneous but pulls scores via id
def save_valid_scores(data_dict, ids) : 
    scores = [data_dict['conspiracy_likelihood'][i] for i in ids]
    with open("../data/valid_scores.npy", "wb") as file : 
        np.save(file, np.asarray(scores))
    return 

if __name__ == '__main__':
    data_dict = load_json(RAW_DATA_PATH) 
    # peek(data_dict)

    # grab the IDs
    ids = np.loadtxt('../data/valid_ids.txt', delimiter=', ', dtype=str)

    # grab the features
    sparse_words, tag_bag = extract_features(data_dict, ids)
    
    # save 'em
    with open("../data/bag_ids.npy", "wb") as file : 
        np.save(file, ids)
    with open("../data/bag_features.npz", "wb") as file : 
        scipy.sparse.save_npz(file, sparse_words) 
    with open("../data/bag_tags.npz", "wb") as file : 
        scipy.sparse.save_npz(file, tag_bag)

    save_valid_scores(data_dict, ids) 