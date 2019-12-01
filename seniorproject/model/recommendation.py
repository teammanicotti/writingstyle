"""Represents a recommendation made by a recommendation engine."""
from typing import List

from seniorproject.model.recommendationtype import RecommendationType
import uuid
import random

class Recommendation:
    """Represents a recommendation made by a recommendation engine."""
    recommendation_type: RecommendationType
    original_text: str
    start_offset: int
    end_offset: int
    paragraph_index: int
    new_values: List[str]
    confidence: float

    def __init__(
            self,
            recommendation_type: RecommendationType,
            original_text: str,
            start_offset: int,
            end_offset: int,
            paragraph_index: int,
            new_values: List[str],
            confidence: float = None,
    ):
        self.recommendation_type = recommendation_type
        self.original_text = original_text
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.paragraph_index = paragraph_index
        self.new_values = new_values
        self.confidence = confidence
        self.uuid = str(uuid.uuid4())

    def to_json(self):
        """Creates a JSON-compatible representation of the recommendation."""
        return self.__dict__

    def __str__(self):
        """Creates a string representation of the recommendation."""
        return self.__dict__
