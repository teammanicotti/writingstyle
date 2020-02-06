"""API entrypoint for '/analyze'"""
import logging


class AnalyticsResource:
    """API entrypoint for '/analyze'"""

    def on_post(self, req, resp) -> None:
        """
        Handles the POST for `/analyze`.
        :param req: Falcon request object
        :param resp: Falcon response object
        :return: None
        """
        logging.info(req.media)
        resp.media = {'result': 'success'}
