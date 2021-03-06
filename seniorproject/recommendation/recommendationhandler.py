"""Handles compiling list of recommendations from various recommendation engines"""
from typing import List

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation
from seniorproject.recommendation.comperativesuperlative import comp_super
from seniorproject.recommendation.recommendationengine import \
    RecommendationEngine
from seniorproject.recommendation.simpletocompound.simpletocompound import \
    SimpleToCompound
from seniorproject.recommendation.passivetoactive import passivetoactive
from seniorproject.recommendation.sentimentreversal import sentimentreversal
from seniorproject.recommendation.clauseanalysis import clauseanalysis
from seniorproject.recommendation.formality import formality


class RecommendationHandler:
    """Compiles overall list of recommendations from various engines."""

    def __init__(
            self,
            spacy_instance,
            tf_session,
            tf_encodings,
            tf_input_placeholder,
            tf_sentence_piece_processor,
    ):
        self.recommendation_engines: List[RecommendationEngine] = [
            SimpleToCompound(
                spacy_instance,
                tf_session,
                tf_encodings,
                tf_input_placeholder,
                tf_sentence_piece_processor
            ),
            passivetoactive.PassiveAnalyzer(),
            sentimentreversal.SentimentReversal(),
            comp_super.ComparativeSuperlativeAnalyzer(),
            clauseanalysis.ClauseAnalysis(),
            formality.FormalityAnalyzer()
        ]

    def collect_recommendations(
            self,
            doc: Document,
            similarity_threshold: float
    ) -> List[Recommendation]:
        """Requests recommendations from each engine and combines them.
        :param doc Document to be analyzed
        :param similarity_threshold threshold of whether to keep
        simple-to-complex recommendation
        :return List[Recommendation] combined list of recommendations
        """
        recommendations = []
        for engine in self.recommendation_engines:
            recommendations += engine.analyze(
                doc=doc,
                similarity_threshold=similarity_threshold
            )

        return recommendations
