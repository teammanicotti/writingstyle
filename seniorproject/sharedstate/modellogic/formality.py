import pickle
import string
import pandas as pd
import os

from sklearn.base import TransformerMixin
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm


N_GRAM_RANGE = 2
USES_PUNCTUATION = True
USES_STOP_WORDS = True

# Create our list of punctuation marks
punctuations = [] if USES_PUNCTUATION else string.punctuation

# Create our list of stopwords
stop_words = [] if USES_STOP_WORDS else STOP_WORDS

# Load English tokenizer, tagger, parser, NER and word vectors
parser = English()
nlp = en_core_web_sm.load()


def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    mytokens = parser(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]

    # Removing stop words
    mytokens = [word for word in mytokens if word not in stop_words and word not in punctuations]

    # return preprocessed list of tokens
    return mytokens


class predictors(TransformerMixin):
    def transform(self, X, **transform_params):
        # Cleaning Text
        return [clean_text(text) for text in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}


def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()


def load_model(model_file):
    return pickle.load(open(model_file, "rb"))


# Formality Threshold for Training Data
FORMALITY_THRESHOLD = 3

SAMPLE_SIZE = 10000


def get_data(csvFile):
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), csvFile))

    # Fields for mturk data-set
    # x_sentences = data["Sentence"]
    # y_labels = data["Formality"]
    # y_labels = y_labels.map(lambda f: f < FORMALITY_THRESHOLD)

    # Fields for gyafc
    data = data.sample(n=SAMPLE_SIZE)
    x_sentences = data["Sentence"]
    y_labels = data["Informal"]

    return x_sentences, y_labels