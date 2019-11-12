"""Represents a paragraph of a document."""
from spacy.tokens.doc import Doc


class Paragraph:
    """Represents a paragraph of a document."""
    text: str
    idx: int
    spacy_doc: Doc

    def __init__(self, text: str, idx: int, spacy_doc: Doc):
        self.text = text
        self.idx = idx
        self.spacy_doc = spacy_doc
