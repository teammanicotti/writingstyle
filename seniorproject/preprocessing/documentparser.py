"""Parses document text received through spaCy pipeline and into model"""
import re
from typing import List

from seniorproject.model.document import Document


class DocumentParser:
    ATTRS = {
        "_": {
            'is_in_text_citation': True
        }
    }

    """Parses document text received through spaCy pipeline and into model"""
    def __init__(self, spacy_instance):
        self.spacy_instance = spacy_instance

    def parse_document(self, text: str, paragraphs: List[str]) -> Document:
        """Creates a Document model object from document received from GSuite.
        :param text: str of document body
        :param paragraphs: List[str] of the text of each paragraph
        """
        parsed_paragraphs = [self.spacy_instance(p) for p in paragraphs]
        self.retokenize_citations(parsed_paragraphs)
        return Document(text, parsed_paragraphs)

    def retokenize_citations(self, parsed_paragraphs):
        """Locates in-text citations in the text, and makes them a single token.
        :param parsed_paragraphs: array of paragraphs as Doc objects
        """
        for paragraph in parsed_paragraphs:
            matches = re.finditer(
                r"\(((?:[a-zA-Z'`-][A-Za-z'`-]+)(?:,? (?:(?:and |& )?"
                r"(?:[a-zA-Z][A-Za-z'`-]+)|(?:et.? al.?)))*(?:, *(?:(?:"
                r"(?:19|20)[0-9][0-9])|n.? ?d.? ?)(?:, p{1,2}.? ?[0-9a-zA-Z]+"
                r"(?:(?:-[0-9a-zA-Z]+)|(?:(?:, ?[0-9a-zA-Z]+)+)))?| "
                r"*\\((?:19|20)[0-9][0-9](?:, p.? [0-9a-zA-Z]+)?\\)))\)",
                paragraph.text
            )
            spans = []
            for match in matches:
                start, end = match.span()
                span = paragraph.char_span(start, end)
                # This is a Span object or None if match
                # doesn't map to valid token sequence
                if span is not None:
                    spans.append(span)

            with paragraph.retokenize() as retokenizer:
                for span in spans:
                    retokenizer.merge(span, attrs=self.ATTRS)
