import tabulate
import pickle
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import precision_score, recall_score
from nlp_utils import ConspiracyDataPreparer, ConspiracyLoader, create_pipeline

# smaller dataset for debugging
# preparer = ConspiracyDataPreparer(debug = True)
# preparer.combine()
# data = preparer.data

# Gathering and Preparing the New Data

ORIGINAL_RESULTS = '../data/training_set.json'
COMMENTS = '../data/training_comments.json'
VALID_IDS = '../data/training_valid_ids.txt'
SAVE_PATH = '../data/training_preproc_data.pkl'

training_data = ConspiracyDataPreparer(
    video_info_path = ORIGINAL_RESULTS,
    comments_path = COMMENTS,
    valid_ids_path = VALID_IDS
)

training_data.combine()
# training_data.save(SAVE_PATH)

# pre-tokenize the comments and descriptions to save time with models
training_data.normalize_comments()
training_data.normalize_descriptions()

training_data.save('../data/prenorm_training_data.json')
# load the data directly from the data preparer
dataloader = ConspiracyLoader()

# create a list of models
models = []
for form in (LogisticRegression, SGDClassifier, MLPClassifier, LinearSVC):
    models.append(create_pipeline(form(), lsa = True, prenormalized = True))
    models.append(create_pipeline(form(), lsa = False, prenormalized = True))

names = ['LogisticRegression', 'SGDClassifier', 'MLPClassifier', 'LinearSVC']
fields = ['model', 'precision', 'recall', 'accuracy', 'f1']
table = []

# fit each of the models
for idx, model in enumerate(models):
    scores = defaultdict(list)

    for idx2, (X_train, X_test, y_train, y_test) in enumerate(dataloader):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        scores['precision'].append(precision_score(y_test, y_pred, average = 'weighted'))
        scores['recall'].append(recall_score(y_test, y_pred, average = 'weighted'))
        scores['accuracy'].append(accuracy_score(y_test, y_pred))
        scores['f1'].append(f1_score(y_test, y_pred, average = 'weighted'))
        print(f"Model {idx + 1} of 8: Completed {idx2 + 1} of 5 iterations.")
    # add to table
    withSVD = " with TrSVD" if model.named_steps.get('lsa') else ""
    row = [str(model.named_steps['classifier']) + withSVD]
    for field in fields[1:]:
        row.append(np.mean(scores[field]))
    
    table.append(row)

# sort by f1 score
table.sort(key = lambda row: row[-1], reverse = True)
print(tabulate.tabulate(table, headers = fields))

table_df = pd.DataFrame(table, columns = fields)
table_df.to_csv('../data/class_model_chart.csv')

#trying with svc
model2 = [create_pipeline(MLPClassifier(), lsa = False, prenormalized = True)]

# create a new feature space
with open('../data/prenorm_training_data.json', 'rb') as f:
    alldata = pickle.load(f)
pipe = create_pipeline(prenormalized = True)
features = pipe.fit_transform(alldata)

with open('../data/training_set_features.pkl', 'wb') as f:
    pickle.dump(features, f)