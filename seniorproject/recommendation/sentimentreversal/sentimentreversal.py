"""
Sentiment reversal recommendation generator
Author: Robert Liedka (rl5849)
"""
from seniorproject.recommendation.recommendationengine import \
    RecommendationEngine
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.document import Document
from nltk.corpus import wordnet
from typing import List


class SentimentReversal(RecommendationEngine):

    def __init__(self):
        super(SentimentReversal, self).__init__()

    def analyze(self, doc: Document) -> List[Recommendation]:
        """
        Main analyze method - Reports all recommendations for sentiment reversal
        Ex: He was not happy -> He was unhappy
        :param doc: Document
        :return: List of recommendations
        """
        results = []
        sent_index = 0
        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                results.extend(
                    SentimentReversal.get_antonyms_for_sentence(
                        sent,
                        sent_index
                    )
                )
                sent_index += 1
        return results

    @staticmethod
    def get_antonyms_for_sentence(sentence, sentence_index):
        """
        Generate recommendations for a sentence
        :param sentence: a spaCy sentence object
        :param sentence_index: Sentences index in doc
        :return: Recommendation[]
        """
        results = []

        for word in sentence:
            if word.text == 'not':
                ants = SentimentReversal.get_antonyms_for_word(
                    sentence[word.i - sentence[0].i + 1].text)
                if len(ants) > 0:
                    rec_text = ""
                    old_val = word.text + " " + sentence[
                        word.i - sentence[0].i + 1].text
                    if len(ants) == 1:
                        rec_text = "Consider changing '{}' to {}.".format(
                            old_val, ants[0])
                    elif len(ants) == 2:
                        rec_text = "Consider changing '{}' to {} or {}".format(
                            old_val, ants[0], ants[1])
                    elif len(ants) > 2:
                        rec_text = "Consider changing '{}' to {}, {} or {}"\
                            .format(old_val, ants[0], ants[1], ants[2])

                    results.append(Recommendation(
                        RecommendationType.SENTIMENT_REVERSAL,
                        "not " + sentence[word.i - sentence[0].i + 1].text,
                        word.i,  # word start index
                        word.i + 1,  # edge end index
                        sentence_index,  # sentence index
                        [rec_text],
                        0  # Confidence
                    ))
        return results

    @staticmethod
    def get_antonyms_for_word(word):
        """
        Get the antonyms for a specific word
        :param word: string
        :return: string[]
        """
        antonyms = []
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
        return antonyms
