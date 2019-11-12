"""Enumeration of sentence types analyzed by the similarity classifier."""
from enum import Enum

__author__ = 'Devon Welcheck'


class SentenceType(str, Enum):
    """Enumeration of sentence types analyzed by the similarity classifier."""
    SIMPLE = 'Simple'
    COMPLEX = 'Complex'
    COMPOUND = 'Compound'
    COMPLEX_COMPOUND = 'Complex/Compound'
