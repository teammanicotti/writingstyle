"""
Comparative and Superlative:

Contains a method to annotate a sentence with improvements to
comparative and superlative usage
"""
from typing import List
from pattern.en import comparative, superlative

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.recommendation.recommendationengine import RecommendationEngine

POS_WITH_COMP_SUPER = ('ADJ', 'ADV')


def annotate_sentence(sentence, index):
    """
    Returns a list of recommendations based on an input sentence
    """
    improvements: List[Recommendation] = []

    for word in sentence:
        if word.text.lower() == "more":
            head = word.head
            if head.pos_ in POS_WITH_COMP_SUPER:
                new_comparative: str = comparative(head.text.lower())
                if "more" not in new_comparative:
                    improvements.append(
                        Recommendation(
                            RecommendationType.COMPARATIVE,
                            sentence.text,
                            sentence.start,
                            sentence.end,
                            index,  # paragraph index
                            sentence.text.replace(
                                "more " + head.text, new_comparative
                            ),
                            RecommendationType.COMPARATIVE + head.text,
                            1  # Confidence
                        )
                    )

        if word.text.lower() == "most":
            head = word.head
            if head.pos_ in POS_WITH_COMP_SUPER:
                new_superlative: str = superlative(head.text.lower())
                if "most" not in new_superlative:
                    improvements.append(
                        Recommendation(
                            RecommendationType.SUPERLATIVE,
                            sentence.text,
                            sentence.start,
                            sentence.end,
                            index,  # paragraph index
                            sentence.text.replace(
                                "most " + head.text, new_superlative
                            ),
                            RecommendationType.SUPERLATIVE + head.text,
                            1  # Confidence
                        )
                    )
    return improvements


class ComparativeSuperlativeAnalyzer(RecommendationEngine):
    """
    Class which maintains logic to provide recommendations on comparative and
    superlative usage
    """

    def analyze(self, doc: Document, **kwargs) -> List[Recommendation]:

        results = []
        paragraph_index = 0
        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                results.extend(
                    annotate_sentence(sent, paragraph_index)
                )
            paragraph_index += 1

        return results
