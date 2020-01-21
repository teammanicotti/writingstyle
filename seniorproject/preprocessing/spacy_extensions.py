"""Contains custom extensions for spaCy"""
from itertools import zip_longest

from spacy.tokens.span import Span
from spacy.tokens.token import Token


def enable_spacy_extensions():
    """Enables custom extensions for spaCy for dealing with citations."""
    Token.set_extension('is_in_text_citation', default=False)
    Span.set_extension('tokens_without_citations',
                       method=get_span_toks_wo_cites)
    Span.set_extension('text_without_citations', method=get_span_text_wo_cites)
    Span.set_extension('text_with_ws_without_citations',
                       method=get_span_text_with_ws_wo_cites)


def get_span_toks_wo_cites(span):
    """Returns an array of all tokens that are not in-text citations.
    :param span: Span object of the sentence
    """
    return [token for token in span if not token._.is_in_text_citation]


def get_span_text_wo_cites(span):
    """Returns a string representation of the Span without in-text citations.
    :param span: Span object of the sentence
    """
    txt = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_in_text_citation:
            if next_tok is not None and next_tok._.is_in_text_citation:
                txt += tok.text
            else:
                txt += tok.text_with_ws
    # Re-create whitespace stripping from original `Span.text()` method:
    # https://github.com/explosion/spaCy/blob/7ad000fce7824f237feec20e577f14c1c3a4a755/spacy/tokens/span.pyx#L500 # pylint: disable=line-too-long
    if span[-1].whitespace_:
        txt = txt[:-1]
    return txt


def get_span_text_with_ws_wo_cites(span):
    """Returns a whitespace-included string of the Span w/o in-text citations.
    :param span: Span object of the sentence
    """
    txt = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_in_text_citation:
            if next_tok is not None and next_tok._.is_in_text_citation:
                txt += tok.text
            else:
                txt += tok.text_with_ws
    return txt

