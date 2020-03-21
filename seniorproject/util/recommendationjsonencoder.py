"""JSONEncoder to return dictionary representation of custom objects."""
import json

from seniorproject.model.simpletocompoundrecommendation import \
    SimpleToCompoundRecommendation
from seniorproject.model.recommendation import Recommendation

__author__ = 'Devon Welcheck'


class RecommendationJsonEncoder(json.JSONEncoder):
    """JSONEncoder to return dictionary representation of custom objects."""

    def default(self, o):
        # pylint: disable=method-hidden
        if isinstance(o, (Recommendation, SimpleToCompoundRecommendation)):
            return o.to_json()
        return super().default(o)
