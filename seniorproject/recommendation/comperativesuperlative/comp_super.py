from typing import List

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.recommendation.recommendationengine import RecommendationEngine

from pattern.en import comparative, superlative

pos_with_comp_super = ('ADJ', 'ADV')


def annotate_sentence(sentence, index):
    improvements: List[Recommendation] = []

    for word in sentence:
        if word.text.lower() == "more":
            head = word.head
            if head.pos_ in pos_with_comp_super:
                new_comparative: str = comparative(head.text.lower())
                if "more" not in new_comparative:
                    improvements.append(
                        Recommendation(
                            RecommendationType.COMPARATIVE,
                            sentence.text,
                            sentence.start,
                            sentence.end,
                            index,  # paragraph index
                            sentence.text.replace("more " + head.text, new_comparative),
                            1  # Confidence
                        )
                    )

        if word.text.lower() == "most":
            head = word.head
            if head.pos_ in pos_with_comp_super:
                new_superlative: str = superlative(head.text.lower())
                if "most" not in new_superlative:
                    improvements.append(
                        Recommendation(
                            RecommendationType.SUPERLATIVE,
                            sentence.text,
                            sentence.start,
                            sentence.end,
                            index,  # paragraph index
                            sentence.text.replace("most " + head.text, new_superlative),
                            1  # Confidence
                        )
                    )
    return improvements


class ComparativeSuperlativeAnalyzer(RecommendationEngine):

    def __init__(self):
        super(ComparativeSuperlativeAnalyzer, self).__init__()

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
