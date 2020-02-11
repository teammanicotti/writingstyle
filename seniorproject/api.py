"""Entry into the API system."""
import json
import os
from functools import partial
from pathlib import Path

import falcon
import sentry_sdk
from falcon import media
from sentry_sdk.integrations.falcon import FalconIntegration

from endpoint.analytics_resource import AnalyticsResource
from seniorproject.endpoint.analyze_resource import AnalyzeResource
from seniorproject.preprocessing.documentparser import DocumentParser
from seniorproject.recommendation.recommendationhandler import \
    RecommendationHandler
from seniorproject.sharedstate import sharedstate
from seniorproject.util.recommendationjsonencoder import \
    RecommendationJsonEncoder

__author__ = 'Devon Welcheck'

# Retrieve the environment.
in_docker: bool = os.path.isdir(os.path.isdir('/run/secrets'))

# Set up sentry.
if in_docker:
    if Path('/run/secrets/sentry').exists():
        sentry_sdk.init(
            dsn=open('/run/secrets/sentry').read(),
            integrations=[FalconIntegration()]
        )
else:
    if Path('.sentry_dsn').exists():
        sentry_sdk.init(
            dsn=open('.sentry_dsn').read(),
            integrations=[
                FalconIntegration(),
            ]
        )

RECOMMENDATION_HANDLER = RecommendationHandler(
    sharedstate.spacy_instance,
    sharedstate.tf_session,
    sharedstate.tf_encodings,
    sharedstate.tf_input_placeholder,
    sharedstate.tf_sentence_piece_processor,
)
DOCUMENT_PARSER = DocumentParser(
    sharedstate.spacy_instance
)

API = falcon.API()
API.add_route('/analyze', AnalyzeResource(
    DOCUMENT_PARSER,
    RECOMMENDATION_HANDLER,
))
API.add_route('/analytics', AnalyticsResource())

JSON_HANDLER = media.JSONHandler(
    dumps=partial(
        json.dumps,
        cls=RecommendationJsonEncoder
    ),
    loads=json.loads,
)
EXTRA_HANDLERS = {
    'application/json': JSON_HANDLER,
}
API.req_options.media_handlers.update(EXTRA_HANDLERS)
API.resp_options.media_handlers.update(EXTRA_HANDLERS)
print("Ready.")
