import json 
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse
import numpy as np 

def load_json() : 
    with open("conspiracy_results.json", "r") as file : 
        d = json.load(file)
    return d

# Looking at how the raw data is formatted
def peek(data_dict) : 
    print("Here are the keys")
    print(data_dict.keys())
    '''
    (['title', 'channel_title', 'reco_count', 'view_count', 
    'comment_count', 'like_count', 'topic_number', 'tags', 
    'description', 'conspiracy_likelihood', 'query_date'])
    '''
    print("Here's how the titles are formatted: ") 
    '''
    Inside data_dict['title'] is another dictionary, e.g. 
    'vrWlQeVX488': 'HISTORY OF RELIGION (Part 33): LAZARUS RAISED FROM THE DEAD', 
    'PJAuq_xqS80': '1-Second Puzzle During Earthfiles YouTube Channel Live Streaming Podcast Wednesday, October 3, 2018',
    '''
    # print(data_dict['title'])
    print("Here's how the topics and tags are formatted")
    print(data_dict['topic_number']['vrWlQeVX488'])
    # 2.0
    print(data_dict['tags']['vrWlQeVX488'])
    # Holy|Bible|Jesus|Spirit|Yahshua|God|Christian|Preacher|Church|DeviL|Scriptures|Pastor|Sermon|Israel|Jews|Jewish|Religion|History|Truth|BIBLE STUDY|END TIMES|JESUS CHRIST|HEAVEN|PRAY|LORD|NEW TESTAMENT|LAZARUS|DEATH|JUDGEMENT|JUDGMENT DAY|DAY|DAY OF THE LORD|NUCLEAR WAR|PUTIN|NUCLEAR HOLOCAUST|WORLD WAR 3|END OF THE WORLD

    print(data_dict['description']['vrWlQeVX488'])
    '''
    SUBSCRIBE: https://www.youtube.com/c/Truthunedited

    DONATE:  bit.ly/Donate_to_Truthunedited
    Your support is greatly appreciated.

    In Part 33 we see Yahshua raise Lazarus from the dead.  He also speaks about judgment.   We should all be thinking about judgment day and His 2nd coming.  He speaks in detail on this and we need to pay attention and apply His Words to our life.  Judgment is not a subject we all want to think about it but it is absolutely something we need to understand and prepare for because we all will stand before Him.

    PLEASE FOLLOW ME ON SOCIAL MEDIA
    INSTAGRAM: bit.ly/Truthunedited-Instagram
    FACEBOOK: bit.ly/Truthunedited-Facebook
    BLOG: bit.ly/Truthunedited-Site

    To reach me directly you can email me at questions@truthunedited.com
    Please give me time to respond.

    Thank you greatly for watching and all of your support! May Elohim Bless You!
    '''
    print(data_dict['conspiracy_likelihood']['vrWlQeVX488'])
    # 0.5432691734
    return 


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

def extract_features(data_dict) : 
    # Going to keep a separate corpus for 
    # the title, the description, and the tags
    title_bag = baggify(list(data_dict['title'].values()))
    tag_bag = baggify(tag_cleanup(data_dict['tags'].values())) # is the tag bag a concern? '|' instead of spaces
    des_bag = baggify(list(data_dict['description'].values()))

    # Merge those sparse matrices, return the features
    features = scipy.sparse.hstack([scipy.sparse.hstack([title_bag,tag_bag]), des_bag]) 

    return features

if __name__ == '__main__':
    data_dict = load_json() 
    # peek(data_dict)

    # grab the features
    sparse_words = extract_features(data_dict)
    # grab the IDs
    ids = np.asarray(list(data_dict['title'].keys()))
    # save 'em
    with open("bag_ids.npy", "wb") as file : 
        np.save(file, ids)
    with open("bag_features.npz", "wb") as file : 
        scipy.sparse.save_npz(file, sparse_words) 
    