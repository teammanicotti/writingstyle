"""Parses document text received through spaCy pipeline and into model"""
import re
from typing import List

from seniorproject.model.document import Document


class DocumentParser:
    """Parses document text received through spaCy pipeline and into model"""
    def __init__(self, spacy_instance):
        self.spacy_instance = spacy_instance

    def parse_document(self, text: str, paragraphs: List[str]) -> Document:
        """Creates a Document model object from document received from GSuite.
        :param text: str of document body
        :param paragraphs: List[str] of the text of each paragraph
        """
        parsed_paragraphs = [self.spacy_instance(p) for p in paragraphs]
        return Document(text, parsed_paragraphs)
