"""
Formality:

Annotates each sentence with a recommendation if the Sklearn models produce
a positive result when detecting informality.
"""
from typing import List

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.recommendation.recommendationengine import RecommendationEngine
from seniorproject.sharedstate.sharedstate import formality_model


def annotate_sentence(sentence, index):
    """
    Returns a list of recommendations based on an input sentence
    """
    if formality_model.ensemble_predict([sentence.text]):
        # Sentence is informal
        return [
            Recommendation(
                            RecommendationType.FORMALITY,
                            sentence.text,
                            sentence.start,
                            sentence.end,
                            index,  # paragraph index
                            [],
                            .25  # Confidence
                        )
        ]
    return []


class FormalityAnalyzer(RecommendationEngine):
    """
    Class which maintains logic to provide recommendations on comparative and
    superlative usage
    """

    def analyze(self, doc: Document) -> List[Recommendation]:

        results = []
        paragraph_index = 0
        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                results.extend(
                    annotate_sentence(sent, paragraph_index)
                )
            paragraph_index += 1

        return results
