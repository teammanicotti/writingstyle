from typing import List
from unittest.mock import MagicMock

from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from seniorproject.model.document import Document
from seniorproject.model.paragraph import Paragraph


def document_mock(
        text: str,
        paragraphs: List[Paragraph]
) -> Document:
    """Creates a mock Document with the given text and paragraphs."""
    doc = MagicMock(spec=Document)
    doc.text = text
    doc.paragraphs = paragraphs
    return doc


def paragraph_mock(
        text: str,
        spacy_doc: Doc,
        idx: int = 0
) -> Paragraph:
    """Creates a mock Paragraph with the given text and spaCy Span instance"""
    paragraph = MagicMock(spec=Paragraph)
    paragraph.text = text
    paragraph.idx = idx
    paragraph.spacy_doc = spacy_doc

    return paragraph


def spacy_doc_mock(
        sentences: List[Span]
) -> Doc:
    """Creates a mock spaCy Doc with the given Span instances"""
    doc = MagicMock(spec=Doc)
    doc.sents.__iter__.side_effect = lambda: iter(sentences)
    return doc


def spacy_token_mock(
        text: str,
        pos_: str = ''
) -> Token:
    """Creates a mock spaCy Token with the given text and part-of-speech"""
    token = MagicMock(spec=Token)
    token.text = text
    token.pos_ = pos_
    return token


def spacy_span_mock(
        text: str,
        start_char: int = 0,
        end_char: int = 0,
        tokens: List[Token] = None
) -> Span:
    """Creates a mock spaCy Span with the given text, start/end, and tokens"""
    span = MagicMock(spec=Span)
    span.text = text
    span.start_char = start_char
    span.end_char = end_char
    if tokens is not None:
        span.__getitem__.side_effect = lambda x: tokens[x]
    span.__iter__.side_effect = lambda: iter(tokens)
    return span
