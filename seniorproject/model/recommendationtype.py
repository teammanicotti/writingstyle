"""Enumeration of the types of recommendations generated by the system"""
from enum import Enum


class RecommendationType(str, Enum):
    """Enumeration of the types of recommendations generated by the system"""
    SIMPLE_TO_COMPOUND = 'SimpleToCompound'
    PASSIVE_TO_ACTIVE = 'PassiveToActive'
    SENTIMENT_REVERSAL = 'SentimentReversal'
    COMPARATIVE = 'Comparative'
    SUPERLATIVE = 'Superlative'
    DIRECT_INDIRECT_CHECKING = 'DirectIndirectObjectChecking'
