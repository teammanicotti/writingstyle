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

        # Change this to grab the last token, determine its offset in the
        # sentence, then get the substring until it.  Then, do the same for
        # sentence 2.  Store both whitespace-stripped last tokens to see if they
        # are the same.  If they are, use that as the new punctuation.  If they
        # are not, assume a period instead.
        # Doing a reverse string find for a period is inaccurate--any
        # punctuation could end the sentence.
        s1_punct = sentence1[-1].text.strip() if sentence1[-1].is_punct else '.'
        s1_punct_loc = sentence1[-1].idx - sentence1.start_char
        s1_without_punct = sentence1.text[0: s1_punct_loc]

        s2_punct = sentence2[-1].text.strip() if sentence2[-1].is_punct else '.'
        s2_punct_loc = sentence2[-1].idx - sentence2.start_char
        s2_without_punct = sentence2.text[0: s2_punct_loc]

        s2_first_letter: str = s2_without_punct[0].lower() \
            if (sentence2[0].pos_ != 'PROPN' and sentence2[0].text != 'I') \
            else s2_without_punct[0]

        punctuation = s1_punct if s1_punct == s2_punct else '.'

        return [
            f"{s1_without_punct}, {conjunction} "
            f"{s2_first_letter}{s2_without_punct[1:]}{punctuation}"
            for conjunction in Conjunctions
        ]
