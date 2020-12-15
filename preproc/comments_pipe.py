from nlp_utils import *
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer

data = ConspiracyDataLoader(debug = True)

model = Pipeline([
    ('text_union', FeatureUnion(
        transformer_list = [
            ('comments', Pipeline([
                ('comments_extractor', CommentsExtractor()),
                ('normalize', TextNormalizer()),
                ('FastText', Doc2VecModel())
            ])),
            ('descriptions', Pipeline([
                ('descript_extractor', DescriptionExtractor()),
                ('desc_vect', TfidfVectorizer())
            ])),
            ('tags', Pipeline([
                ('tags_extractor', TagsExtractor()), 
                ('tags_vect', TfidfVectorizer())
            ])),
            ('titles', Pipeline([
                ('titles_extractor', TitlesExtractor()),
                ('titles_vect', TfidfVectorizer())
            ]))
        ],
        transformer_weights = {
            'comments': 0.3,
            'descriptions': 0.3,
            'tags': 0.2,
            'titles': 0.2
        }
    ))
])

combined_matrix = model.fit_transform(data)

# import pickle
# import json
# import nltk
# import string
# from nltk import sent_tokenize
# from gensim.models.doc2vec import Doc2Vec, TaggedDocument, Doc2Vec
# from nltk.stem.wordnet import WordNetLemmatizer

# # import the comments
# with open('../data/comments.json', 'r') as f:
#     comments = json.load(f)


# # turn comments data into a list of lists
# corpus = [[info['text'] for info in comlist] 
#             for _, comlist in comments.items()]

# corpus = corpus[:50]

# def tokenize(comments):
#     """Custom tokenizer for comments structured as lists of individual comments."""
#     stem = nltk.stem.SnowballStemmer('english')
#     comments = " ".join(comments).lower()

#     for token in nltk.word_tokenize(comments):

#         if token in string.punctuation: 
#             continue

#         yield stem.stem(token)

# # tokenize each of the comment lists for each doc
# corpus = [list(tokenize(doc)) for doc in corpus]

# # use video ids as keys for the tagged document
# corpus = [
#     TaggedDocument(words, [vid])
#     for words, vid in zip(corpus, comments.keys())
# ]

# # run in model
# model = Doc2Vec(corpus, size = 40, min_count = 0)

# # with open("../data/word2vec_model.pkl", 'wb') as f:
# #     pickle.dump(model, f)

# # # create a data set that has everything
# from gensim.models import FastText
# model = FastText(corpus)

# words = list(model.wv.vocab)
# vectors = []
# for w in words:
#     vectors.append(model[w].tolist())
# embedding_matrix = np.array(vectors)

# # Import libraries

# from gensim.models import doc2vec
# from collections import namedtuple

# # Load data

# doc1 = ["This is a sentence", "This is another sentence"]

# # Transform data (you can add more data preprocessing steps) 

# docs = []
# analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
# for i, text in enumerate(doc1):
#     words = text.lower().split()
#     tags = [i]
#     docs.append(analyzedDocument(words, tags))

# # Train model (set min_count = 1, if you want the model to work with the provided example data set)

# model = doc2vec.Doc2Vec(docs, size = 100, window = 300, min_count = 1, workers = 4)

# # Get the vectors

# model.docvecs[0]
# model.docvecs[1]