import json
import nltk
import unicodedata
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, Doc2Vec
from nltk.corpus import wordnet as wn
from tqdm import tqdm

class ConspiracyDataLoader():
    
    def __init__(self, debug = False) -> None:
        self.videoinfo_path = '../data/conspiracy_results.json'
        self.comments_path = '../data/comments.json'
        self.valid_ids_path = '../data/valid_ids.txt'

        self.debug = debug
        self.data = self.combine()

    def load_data(self):
        with open(self.videoinfo_path, 'rb') as f:
            video_info = json.load(f)

        with open(self.comments_path, 'rb') as f:
            comments = json.load(f)

        with open(self.valid_ids_path, 'r') as f:
            valid_ids = f.readlines()[0].split(', ')

        return valid_ids, video_info, comments
    
    def tag_parser(self, tags):
        """Handle the nonstandard tags."""
        
        if tags is None:
            return []

        elif type(tags) is list:
            return tags

        elif type(tags) is str:
            return tags.split('|')
        
    def combine(self):

        valid_ids, video_info, comments = self.load_data()

        if self.debug:
            valid_ids = valid_ids[:50]

        combined = {}
        for vid in valid_ids:
            tags = video_info['tags'][vid]
            combined[vid] = {
                'title': video_info['title'][vid],
                'description': video_info['description'][vid],
                'tags': self.tag_parser(tags),
                'comments': [info['text'] for info in comments[vid]]
            }

        return combined

    def fit(self, X, y = None):

        self.data = self.combine()
        return self
    
    def transform(self, X):

        return self

    def __iter__(self):

        for key, data in self.data.items():
            yield key, data

class TitlesExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, dataloader):
        for _, data in dataloader:
            yield data['title']
            
class DescriptionExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self

    def transform(self, dataloader):
        for _, data in dataloader:
            yield data['description']

class TagsExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self

    def transform(self, dataloader):
        for _, data in dataloader:
            yield " ".join(data['tags'])

class CommentsExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self
    
    def transform(self, dataloader):
        for _, data in dataloader:
            yield data['comments']

class TextNormalizer(BaseEstimator, TransformerMixin):

    def __init__(self, language = 'english') -> None:
        self.stopwords = set(nltk.corpus.stopwords.words(language))
        self.lemmatizer = nltk.WordNetLemmatizer()
    
    def is_punct(self, token):
        return(all(unicodedata.category(char).startswith('P') for char in token))

    def is_stopword(self, token):
        return token.lower() in self.stopwords
    
    def lemmatize(self, token, pos_tag):
        tag = {'N': wn.NOUN,
               'V': wn.VERB,
               'R': wn.ADV,
               'J': wn.ADJ
            }.get(pos_tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def normalize(self, text):
        return [self.lemmatize(token, tag).lower()
                for (token, tag) in nltk.pos_tag(nltk.word_tokenize(" ".join(text)))
                if not self.is_punct(token) and not self.is_stopword(token)]
    
    def fit(self, X, y = None):
        return self
         
    def transform(self, text_list):

        for comments in tqdm(text_list):
            yield self.normalize(comments)

class Doc2VecModel():
    def fit(self, X, y = None):
        return self
    
    def transform(self, comments):

        corpus = [
            TaggedDocument(words, [f'd{idx}'])
            for idx, words in enumerate(comments)
        ]

        model = Doc2Vec(vector_size=300, window=10, min_count=3, 
                    workers=4, epochs = 40)
        model.build_vocab(corpus)
        model.train(corpus, 
                    total_examples=model.corpus_count, 
                    epochs=model.epochs)

        print('Doc2Vec vector conversion complete.')
        return np.array(model.docvecs.doctag_syn0)