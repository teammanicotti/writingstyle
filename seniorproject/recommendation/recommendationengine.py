"""Abstract base class for recommendation engines."""
from abc import abstractmethod, ABC
from typing import List

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation


class RecommendationEngine(ABC):
    """Abstract base class for recommendation engines.
    All engines must at minimum implement an analyze method that takes in
    a document and returns a list of recommendations.
    """
    @abstractmethod
    def analyze(self, doc: Document, **kwargs) -> List[Recommendation]:
        """Generates a list of recommendations for a given document"""
