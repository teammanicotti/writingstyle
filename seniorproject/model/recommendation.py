"""Represents a recommendation made by a recommendation engine."""
import uuid
from typing import List
from seniorproject.model.recommendationtype import RecommendationType


class Recommendation:
    """Represents a recommendation made by a recommendation engine."""
    UUID_BASE = uuid.UUID('589B3E05-5ECD-438B-88EF-86D2160DCC7E')

    recommendation_type: RecommendationType
    original_text: str
    start_offset: int
    end_offset: int
    paragraph_index: int
    new_values: List[str]
    uuid: str
    confidence: float

    def __init__(
            self,
            recommendation_type: RecommendationType,
            original_text: str,
            start_offset: int,
            end_offset: int,
            paragraph_index: int,
            new_values: List[str],
            hash_value: str,
            confidence: float = None,
    ):
        self.recommendation_type = recommendation_type
        self.original_text = original_text
        self.start_offset = start_offset
        self.end_offset = end_offset
        self.paragraph_index = paragraph_index
        self.new_values = new_values
        self.uuid = str(uuid.uuid5(self.UUID_BASE, hash_value))
        self.confidence = confidence

    def to_json(self):
        """Creates a JSON-compatible representation of the recommendation."""
        return self.__dict__

    def __str__(self):
        """Creates a string representation of the recommendation."""
        return self.__dict__
