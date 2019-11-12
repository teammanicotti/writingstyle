"""Combines simple sentences with common conjunctions."""
from typing import List

from spacy.tokens import Span

from seniorproject.recommendation.simpletocompound.sentencecombination.conjunctions import \
    Conjunctions

__author__ = 'Devon Welcheck'


class Combine:
    """Combines simple sentences with common conjunctions."""

    @staticmethod
    def generate_combined(sentence1: Span, sentence2: Span) -> List[str]:
        """Combines simple sentences with common conjunctions.

        :param sentence1: spaCy Span object of the first sentence
        :param sentence2: spaCy Span object of the second sentence
        :return: list[str] of generated combined sentences
        """
        s1_period_pos: int = sentence1.text.rfind('.')  # Find the period
        s1_content: str = sentence1.text[0: s1_period_pos]

        s2_period_pos: int = sentence2.text.rfind('.')  # Find the period
        s2_content: str = sentence2.text[0: s2_period_pos]

        s2_first_letter: str = s2_content[0].lower() \
            if (sentence2[0].pos_ != 'PROPN' and sentence2[0].text != 'I') \
            else s2_content[0]

        return [
            f"{s1_content}, {conjunction} {s2_first_letter}{s2_content[1:]}."
            for conjunction in Conjunctions
        ]
