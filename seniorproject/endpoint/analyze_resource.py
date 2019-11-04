"""API entrypoint for `/analyze`"""
import falcon

from seniorproject.postprocessing import postprocess_sample
from seniorproject.preprocessing import preprocess_sample

__author__ = 'Devon Welcheck'


@falcon.before(preprocess_sample.preprocess)
@falcon.after(postprocess_sample.postprocess)
class AnalyzeResource:
    """API entrypoint for `/analyze`"""

    def __init__(self):
        pass

    def on_post(self, req, resp) -> None:
        """
        Handles the POST for `/analyze`.
        :param req: Falcon request object
        :param resp: Falcon response object
        :return: None
        """
