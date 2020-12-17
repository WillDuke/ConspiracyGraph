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
    # want informative features, so word must appear in at least 10 videos
    # what percent of videos is 10 videos? 
    min_percent = 10 / len(feature_list)
    # Since our class sizes are about 1,000, we don't want overly common words
    # Already have stop_words, will also use max_df for more than 1000 videos
    max_feats = 1_000 # 1000 / len(feature_list)

    vectorizer = CountVectorizer(stop_words='english', max_features=max_feats, min_df=min_percent)
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
    # title_bag = baggify([data_dict['title'][i] for i in ids])
    tag_bag = baggify(tag_cleanup([data_dict['tags'][i] for i in ids])) # is the tag bag a concern? '|' instead of spaces
    # des_bag = baggify([data_dict['description'][i] for i in ids])

    com_dict = load_json(COM_PATH) 
    # com_bag = baggify(com_cleanup([com_dict[i] for i in ids])) # 0 # waiting for comments data

    # Try a single corpus : 
    merged_corp = []
    clean_com = com_cleanup([com_dict[i] for i in ids])
    for idx, i in enumerate(ids) : 
        # print([data_dict['title'][i], data_dict['description'][i], com_dict[i]])
        video_all = ' '.join([data_dict['title'][i], data_dict['description'][i], clean_com[idx]])
        merged_corp.append(video_all)

    # print("MERGED: ", merged_corp[:5])
    merged_bag = baggify(merged_corp)
    # print(merged_bag)
    # Merge those sparse matrices, return the features
    # features = scipy.sparse.hstack([scipy.sparse.hstack([title_bag,des_bag]), com_bag]) 
    features = merged_bag
    return features, tag_bag


# A little extraneous but pulls scores via id
def save_valid_scores(data_dict, ids) : 
    scores = [data_dict['conspiracy_likelihood'][i] for i in ids]
    with open("../data/valid_scores.npy", "wb") as file : 
        np.save(file, np.asarray(scores))
    return 

# Make sure tags are working properly
def check_tag_corpus() :
    '''
    No broken issues with tags, top 20 (not in order) : 
    ['aliens', 'ancient', 'bible', 'conspiracy', 'earth', 'end', 'history', 
    'jesus', 'news', 'of', 'on', 'prophecy', 'roth', 'sid', 'supernatural', 
    'the', 'times', 'trump', 'ufo', 'world']
    Top word: 'the' appearing in over 20% of video tags
    Added 'the', 'of', and 'on' to stop words list
    '''
    data_dict = load_json(RAW_DATA_PATH)
    ids = np.loadtxt('../data/valid_ids.txt', delimiter=', ', dtype=str)
    clean_tags = tag_cleanup([data_dict['tags'][i] for i in ids])
    vectorizer = CountVectorizer(max_features=25, stop_words='english')
    X = vectorizer.fit_transform(clean_tags)
    print(vectorizer.get_feature_names())
    # analyze = vectorizer.build_analyzer(max_features=20)
    # print(analyze(' '.join(clean_tags)))  
    return 

if __name__ == '__main__':
    data_dict = load_json(RAW_DATA_PATH) 
    # peek(data_dict)

    # grab the IDs
    ids = np.loadtxt('../data/valid_ids.txt', delimiter=', ', dtype=str)

    # grab the features
    sparse_words, tag_bag = extract_features(data_dict, ids)
    # print("We made {} features for {} samples!".format(sparse_words.shape[0], sparse_words.shape[1]))

    # save 'em
    with open("../data/bag_ids.npy", "wb") as file : 
        np.save(file, ids)
    with open("../data/bag_features.npz", "wb") as file : 
        scipy.sparse.save_npz(file, sparse_words) 
    with open("../data/bag_tags.npz", "wb") as file : 
        scipy.sparse.save_npz(file, tag_bag)

    save_valid_scores(data_dict, ids) 