"""API entrypoint for `/analyze`"""

from seniorproject.model.document import Document
from seniorproject.recommendation.recommendationhandler import \
    RecommendationHandler

__author__ = 'Devon Welcheck'


class AnalyzeResource:
    """API entrypoint for `/analyze`"""

    def __init__(
            self,
            recommendation_handler: RecommendationHandler
    ):
        self.recommendation_handler = recommendation_handler

    def on_post(self, req, resp) -> None:
        """
        Handles the POST for `/analyze`.
        :param req: Falcon request object
        :param resp: Falcon response object
        :return: None
        """
        doc = Document(req.media['text'], req.media['paragraphs'])
        recs = self.recommendation_handler.collect_recommendations(doc)
        resp.media = {'results': recs}
