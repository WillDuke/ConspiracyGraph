import pickle
from re import S
from nlp_utils import ConspiracyLoader, create_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report

# load the data
dataloader = ConspiracyLoader()

# create a list of models
models = []
for form in (LogisticRegression, MultinomialNB, SGDClassifier):
    models.append(create_pipeline(form(), True))
    # models.append(create_pipeline(form(), False))

# fit each of the models
for model in models:
    for X_train, X_test, y_train, y_test in dataloader:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)


model = create_pipeline(SGDClassifier(), False)
    
for X_train, X_test, y_train, y_test in dataloader:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    break