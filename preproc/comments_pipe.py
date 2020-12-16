from nlp_utils import *
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
from scipy.sparse import save_npz

def create_pipeline(lsa = False, debug = False):
    """Create a pipeline to clean, tokenize, lemmatize, and vectorize
    the titles, descriptions, tags, and comments for the video dataset."""

    model = Pipeline([
        ('dataloader', ConspiracyDataLoader(debug = debug)),
        ('text_union', FeatureUnion(
            transformer_list = [
                ('comments', Pipeline([
                    ('comments_extractor', CommentsExtractor()),
                    ('normalize', TextNormalizer()),
                    ('FastText', Doc2VecModel())
                ])),
                ('descriptions', Pipeline([
                    ('descript_extractor', DescriptionExtractor()),
                    ('desc_vect', TfidfVectorizer(
                        stop_words=stopwords.words('english')
                    ))
                ])),
                ('tags', Pipeline([
                    ('tags_extractor', TagsExtractor()), 
                    ('tags_vect', TfidfVectorizer(
                        stop_words=stopwords.words('english')
                    ))
                ])),
                ('titles', Pipeline([
                    ('titles_extractor', TitlesExtractor()),
                    ('titles_vect', TfidfVectorizer(
                        stop_words=stopwords.words('english')
                    ))
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

    if lsa:
        model.steps.append(['lsa', TruncatedSVD(n_components = 100)])

    return model

if __name__ == "__main__":

    # create pipeline to merge doc/word embeddings for
    # titles, descriptions, comments, 
    model = create_pipeline()
    combined_matrix = model.fit_transform(X = None)

    # save compressed sparse matrix to data folder
    save_npz('../data/combined_adj_matrix.npz', combined_matrix)