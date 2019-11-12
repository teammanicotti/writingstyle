"""Represents a document provided to the system."""
from typing import List

from spacy.tokens import Doc

from seniorproject.model.paragraph import Paragraph


class Document:
    """Represents a document provided to the system."""
    text: str
    paragraphs: List[Paragraph]

    def __init__(self, text: str, paragraphs: List[Doc]):
        self.text = text
        self.paragraphs = [Paragraph(p.text, paragraphs.index(p), p) for p in paragraphs]
