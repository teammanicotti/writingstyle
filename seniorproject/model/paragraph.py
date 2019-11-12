"""Represents a paragraph of a document."""


class Paragraph:
    """Represents a paragraph of a document."""
    text: str
    idx: int

    def __init__(self, text: str, idx: int):
        self.text = text
        self.idx = idx
