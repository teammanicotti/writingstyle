"""Parses document text received through spaCy pipeline and into model"""
from typing import List

from seniorproject.model.document import Document
from seniorproject.preprocessing.grammarchecking.grammarchecking import GrammarChecking


class DocumentParser:
    """Parses document text received through spaCy pipeline and into model"""
    def __init__(self, spacy_instance):
        self.spacy_instance = spacy_instance
        self._grammar_instance = GrammarChecking(spacy_instance)

    def parse_document(self, text: str, paragraphs: List[str]) -> Document:
        """Creates a Document model object from document received from GSuite.
        :param text: str of document body
        :param paragraphs: List[str] of the text of each paragraph
        """
        parsed_paragraphs = [self._grammar_instance.check_sentences(p) for p in paragraphs]
        return Document(text, parsed_paragraphs)
