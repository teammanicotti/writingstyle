"""Contains custom extensions for spaCy"""
import re
from itertools import zip_longest

from spacy.tokens.span import Span  # pylint: disable=no-name-in-module
from spacy.tokens.token import Token  # pylint: disable=no-name-in-module

# In theory, we should be able to set the 'SENT_START' attribute here,
# but since the method the retokenizer uses a `uint_64` parameter to
# set a stuct's signed int value, the value for false (-1) does not
# get set properly.
ATTRS = {
    "_": {
        'is_in_text_citation': True
    }
}


def enable_spacy_extensions():
    """Enables custom extensions for spaCy for dealing with citations."""
    Token.set_extension('is_in_text_citation', default=False)
    Span.set_extension(
        'tokens_without_citations',
        getter=get_span_tokens_without_citations
    )
    Span.set_extension(
        'text_without_citations',
        getter=get_span_text_without_citations
    )
    Span.set_extension(
        'text_with_ws_without_citations',
        getter=get_span_text_with_ws_wo_cites
    )


def get_span_tokens_without_citations(span):
    """Returns an array of all tokens that are not in-text citations.
    :param span: Span object of the sentence
    """
    return [token for token in span if not token._.is_in_text_citation]


def get_span_text_without_citations(span):
    """Returns a string representation of the Span without in-text citations.
    :param span: Span object of the sentence
    """
    text = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_in_text_citation:
            if next_tok is not None and next_tok._.is_in_text_citation:
                text += tok.text
            else:
                text += tok.text_with_ws
    # Re-create whitespace stripping from original `Span.text()` method:
    # https://github.com/explosion/spaCy/blob/7ad000fce7824f237feec20e577f14c1c3a4a755/spacy/tokens/span.pyx#L500 # pylint: disable=line-too-long
    if span[-1].whitespace_:
        text = text[:-1]
    return text


def get_span_text_with_ws_wo_cites(span):
    """Returns a whitespace-included string of the Span w/o in-text citations.
    :param span: Span object of the sentence
    """
    text = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_in_text_citation:
            if next_tok is not None and next_tok._.is_in_text_citation:
                text += tok.text
            else:
                text += tok.text_with_ws
    return text


def retokenize_citations(doc):
    """Locates in-text citations in the text, and makes them a single token.
    :param parsed_paragraphs: array of paragraphs as Doc objects
    """
    # Try me: regexr.com/4ssv9
    matches = re.finditer(
        r"\(((?:(?:[a-zA-Z'`-][A-Za-z'`-]+)(?:,? (?:(?:and |& )?(?:[a-zA-Z]"
        r"[A-Za-z'`-]+)|(?:et.? al.?)))*(?:, *(?:(?:[0-9]{1,4})|n.? ?d.? ?)"
        r"(?:, p{1,2}g?.? ?[0-9a-zA-Z]+(?:[-,] ?[0-9a-zA-Z]+)*)?))|(?:(?:"
        r"(?:[0-9]{1,4})|n.? ?d.? ?)(?:, p{1,2}g?.? ?[0-9a-zA-Z]+(?:[-,] "
        r"?[0-9a-zA-Z]+)*))|(?:(?:p{1,2}g?.? ?[0-9a-zA-Z]+(?:[-,] ?[0-9a-zA-Z]"
        r"+)*)?))\)",
        doc.text
    )
    spans = []
    token_starts = []
    for match in matches:
        start, end = match.span()
        span = doc.char_span(start, end)
        # This is a Span object or None if match
        # doesn't map to valid token sequence
        if span is not None:
            spans.append(span)

    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span, attrs=ATTRS)
            token_starts.append(span.start)

    for start in token_starts:
        doc[start].is_sent_start = False

    return doc
