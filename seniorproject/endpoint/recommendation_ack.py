"""API entrypoint for `/recAck`"""
import logging
__author__ = 'Robert Liedka'


class RecommendationAcknowledger(object):
    """API entrypoint for `/recAck`"""

    def on_get(self, req, resp) -> None:
        if(req.params['accepted'] == 'true'):
            logging.info('User accepted recommendation')
        else:
            logging.info('User rejected recommendation')

