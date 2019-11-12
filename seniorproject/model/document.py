"""Represents a document provided to the system."""
from typing import List

from seniorproject.model.paragraph import Paragraph


class Document:
    """Represents a document provided to the system."""
    text: str
    paragraphs: List[Paragraph]

    def __init__(self, text: str, paragraphs: List[str]):
        self.text = text
        self.paragraphs = [Paragraph(p, paragraphs.index(p)) for p in paragraphs]
