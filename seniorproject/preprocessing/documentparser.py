"""Parses document text received through spaCy pipeline and into model"""
import os
from typing import List

from seniorproject.model.document import Document
from seniorproject.preprocessing.grammarchecking.grammarchecking import GrammarChecking


class DocumentParser:
    """Parses document text received through spaCy pipeline and into model"""
    def __init__(self, spacy_instance):
        self.spacy_instance = spacy_instance
        self._grammar_instance = GrammarChecking(spacy_instance)
        self.use_grammar_checking = bool(
            os.getenv('SKIP_GRAMMAR_CHECKING', 'False')
        )

    def parse_document(
            self,
            text: str,
            paragraphs: List[str],
    ) -> Document:
        """Creates a Document model object from document received from GSuite.
        :param text: str of document body
        :param paragraphs: List[str] of the text of each paragraph
        """

        if self.use_grammar_checking:
            parsed_paragraphs = [
                self._grammar_instance.check_sentences(p) for p in paragraphs
            ]
        else:
            parsed_paragraphs = [
                self.spacy_instance.check_sentences(p) for p in paragraphs
            ]
        return Document(text, parsed_paragraphs)
