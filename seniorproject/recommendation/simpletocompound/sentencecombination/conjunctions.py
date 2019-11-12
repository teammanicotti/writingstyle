"""Enumeration of English conjunctions"""
from enum import Enum

__author__ = 'Devon Welcheck'


class Conjunctions(str, Enum):
    """Enumeration of English conjunctions"""
    FOR = 'for'
    AND = 'and'
    # NOT = 'not'
    BUT = 'but'
    OR = 'or'
    YET = 'yet'
    SO = 'so'
