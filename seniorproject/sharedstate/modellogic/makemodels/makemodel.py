"""
This python script is used to make and pickle a model using sklearn with
spaCy processing. This script is intended to be run only as a stand-alone
single-execution script.

No packages in this module should be used elsewhere in the project.
(Hence the missing `__init__.py` file).
"""

import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from seniorproject.sharedstate.modellogic import formality
from sklearn.model_selection import train_test_split
import pickle
from sklearn import metrics

# Modify this to change the output file
OUT_MODEL_NAME = "gyafc_model_1.mdl"  # Will be output to the root dir of the project
TRAINING_FILE_NAME = os.sep.join(["makemodels", "data", "gyafc.csv"])

# Model Logic Module
model_logic = formality


if __name__ == "__main__":

    """ Vectorize """
    bow_vector = CountVectorizer(tokenizer=model_logic.spacy_tokenizer, ngram_range=(1, model_logic.N_GRAM_RANGE))

    """ Split Data-set """

    x_sentences, y_labels = model_logic.get_data(TRAINING_FILE_NAME)

    X_train, X_test, y_train, y_test = train_test_split(x_sentences, y_labels, test_size=0.2)

    """ Train a Model """
    # Logistic Regression Classifier
    from sklearn.linear_model import LogisticRegression

    classifier = LogisticRegression()

    # Create pipeline using Bag of Words
    pipe = Pipeline([("cleaner", model_logic.Predictors()),
                     ('vectorizer', bow_vector),
                     ('classifier', classifier)])

    # model generation
    pipe.fit(X_train, y_train)

    s = pickle.dump(pipe, open(OUT_MODEL_NAME, "wb"))

    pipe_loaded = pickle.load(open(OUT_MODEL_NAME, "rb"))

    predicted = pipe_loaded.predict(X_test)
    print("Logistic Regression Accuracy:", metrics.accuracy_score(y_test, predicted))
    print("Logistic Regression Precision:", metrics.precision_score(y_test, predicted))
    print("Logistic Regression Recall:", metrics.recall_score(y_test, predicted))
