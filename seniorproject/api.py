"""Entry into the API system."""
import os
from pathlib import Path

import falcon
import sentry_sdk
from sentry_sdk.integrations.falcon import FalconIntegration

from seniorproject.db.db_connector import DBConnector
from seniorproject.endpoint.analyze_resource import AnalyzeResource

__author__ = 'Devon Welcheck'

# Retrieve the environment.
if os.path.isdir('/run/secrets'):  # If running in Docker
    DB_NAME = open('/run/secrets/db_name').read()
    DB_USER = open('/run/secrets/db_user').read()
    DB_PASSWORD = open('/run/secrets/db_password').read()
    DB_URL = open('/run/secrets/db_url').read()
    if Path('/run/secrets/sentry').exists():
        sentry_sdk.init(
            dsn=open('/run/secrets/sentry').read(),
            integrations=[FalconIntegration()]
        )
else:
    DB_NAME = open('.db_name').read()
    DB_URL = open('.db_url').read()
    DB_USER = open('.db_user').read()
    DB_PASSWORD = open('.db_password').read()
    if Path('.sentry_dsn').exists():
        sentry_sdk.init(
            dsn=open('.sentry_dsn').read(),
            integrations=[FalconIntegration()]
        )

DB_CONNECTOR = DBConnector(f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')
API = falcon.API()
API.add_route('/analyze', AnalyzeResource())

# JSON_HANDLER = media.JSONHandler(
#     dumps=partial(
#         json.dumps,
#         cls=SentenceJsonEncoder
#     ),
#     loads=json.loads,
# )
# EXTRA_HANDLERS = {
#     'application/json': JSON_HANDLER,
# }
# API.req_options.media_handlers.update(EXTRA_HANDLERS)
# API.resp_options.media_handlers.update(EXTRA_HANDLERS)
