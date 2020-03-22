"""Represents a simple-to-compound recommendation."""
from typing import List

from seniorproject.model.recommendation import Recommendation
from seniorproject.model.recommendationtype import RecommendationType


class SimpleToCompoundRecommendation(Recommendation):
    """Represents a simple-to-compound recommendation."""

    conjunctions: List[str]
    new_parts: List[str]

    def __init__(
            self,
            recommendation_type: RecommendationType,
            original_text: str,
            start_offset: int,
            end_offset: int,
            paragraph_index: int,
            new_values: List[str],
            hash_value: str,
            conjunctions: List[str],
            new_parts: List[str],
            confidence: float = None
    ):
        self.conjunctions = conjunctions
        self.new_parts = new_parts
        super().__init__(
            recommendation_type,
            original_text,
            start_offset,
            end_offset,
            paragraph_index,
            new_values,
            hash_value,
            confidence
        )
