"""Parses document text received through spaCy pipeline and into model"""
import os
from typing import List

from preprocessing import spacy_extensions
from seniorproject.model.document import Document
from seniorproject.preprocessing.grammarchecking.grammarchecking import GrammarChecking


class DocumentParser:
    """Parses document text received through spaCy pipeline and into model"""
    def __init__(self, spacy_instance):
        self.spacy_instance = spacy_instance
        self._grammar_instance = GrammarChecking(spacy_instance)
        self.use_grammar_checking = not bool(
            os.getenv('SKIP_GRAMMAR_CHECKING', 'False')
        )
        spacy_extensions.enable_extensions(spacy_instance)

    def parse_document(
            self,
            text: str,
            paragraphs: List[str],
            exclude_quotations: bool
    ) -> Document:
        """Creates a Document model object from document received from GSuite.
        :param text: str of document body
        :param paragraphs: List[str] of the text of each paragraph
        :param exclude_quotations: bool of whether to exclude quotations from
        processing
        """
        if exclude_quotations:
            parsed_paragraphs = self.parse_paragraphs(paragraphs)
        else:
            disabled = spacy_extensions.disable_quotation_exclude_extension(
                self.spacy_instance
            )
            parsed_paragraphs = self.parse_paragraphs(paragraphs)
            disabled.restore()

        return Document(text, parsed_paragraphs)


    def parse_paragraphs(
            self,
            paragraphs: List[str],
    ):
        """Parses text from paragraphs into spaCy Doc objects, and checks
        grammar if appropriate.
        :param paragraphs: List[str] of text of each paragraph
        """
        if self.use_grammar_checking:
            parsed_paragraphs = [
                self._grammar_instance.check_sentences(p) for p in paragraphs
            ]
        else:
            parsed_paragraphs = [
                self.spacy_instance(p) for p in paragraphs
            ]
        return parsed_paragraphs
