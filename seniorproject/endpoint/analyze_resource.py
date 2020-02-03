"""API entrypoint for `/analyze`"""
from seniorproject.recommendation.recommendationhandler import \
    RecommendationHandler
from seniorproject.preprocessing.documentparser import DocumentParser

__author__ = 'Devon Welcheck'


class AnalyzeResource:
    """API entrypoint for `/analyze`"""

    def __init__(
            self,
            document_paraser: DocumentParser,
            recommendation_handler: RecommendationHandler
    ):
        self.document_parser = document_paraser
        self.recommendation_handler = recommendation_handler

    def on_post(self, req, resp) -> None:
        """
        Handles the POST for `/analyze`.
        :param req: Falcon request object
        :param resp: Falcon response object
        :return: None
        """
        doc = self.document_parser.parse_document(
            req.media['text'],
            req.media['paragraphs']
        )
        similarity_threshold = req.media['similarityThreshold']
        recs = self.recommendation_handler.collect_recommendations(
            doc,
            similarity_threshold
        )
        resp.media = {'results': recs}
