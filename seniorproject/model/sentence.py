"""Represents a sentence analyzed by the similarity classifier."""
from spacy.tokens import Span

from seniorproject.recommendation.simpletocompound.model.sentencetype import \
    SentenceType

__author__ = 'Devon Welcheck'


class Sentence:
    """Represents a sentence analyzed by the similarity classifier."""
    text: str
    start_position: int
    end_position: int
    paragraph_idx: int
    span: Span

    def __init__(
            self,
            text: str,
            start_position: int,
            end_position: int,
            paragraph_idx: int,
            sentence_type: SentenceType,
            span: Span
    ) -> None:
        self.text = text.strip()
        self.start_position = start_position
        self.end_position = end_position
        self.paragraph_idx = paragraph_idx
        self.sentence_type = sentence_type
        self.span = span

    def to_json(self):
        """Creates dictionary representation for JSON encoding."""
        return {k: v for k, v in self.__dict__.items() if k not in 'span'}
