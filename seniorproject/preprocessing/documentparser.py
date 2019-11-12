from typing import List

from seniorproject.model.document import Document


class DocumentParser:
    def __init__(self, spacy_instance):
        self.spacy_instance = spacy_instance

    def parse_document(self, text: str, paragraphs: List[str]) -> Document:
        parsed_paragraphs = [self.spacy_instance(p) for p in paragraphs]
        return Document(text, parsed_paragraphs)
