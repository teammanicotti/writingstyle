"""Contains custom extensions for spaCy"""
import re
from contextlib import contextmanager
from itertools import zip_longest

from spacy.language import Language
from spacy.tokens.span import Span  # pylint: disable=no-name-in-module
from spacy.tokens.token import Token  # pylint: disable=no-name-in-module

# In theory, we should be able to set the 'SENT_START' attribute here,
# but since the method the retokenizer uses a `uint_64` parameter to
# set a stuct's signed int value, the value for false (-1) does not
# get set properly.
CITATION_ATTRS = {
    "_": {
        'is_in_text_citation': True,
        'is_excluded': True
    }
}

QUOTATION_ATTRS = {
    "_": {
        'is_quotation': True,
        'is_excluded': True
    }
}


def disable_quotation_exclude_extension(spacy_instance: Language):
    """Disables custom extensions for spaCy for dealing with citations."""
    return spacy_instance.disable_pipes('exclude_quotes')


def enable_extensions(spacy_instance: Language):
    """Enables custom extensions for spaCy for dealing with citations."""
    spacy_instance.add_pipe(
        retokenize_citations,
        name='exclude_citations',
        before='parser'
    )
    Token.set_extension('is_in_text_citation', default=False, force=True)
    Span.set_extension(
        'tokens_without_citations',
        getter=get_span_tokens_without_citations,
        force=True
    )
    Span.set_extension(
        'text_without_citations',
        getter=get_span_text_without_citations,
        force=True
    )
    Span.set_extension(
        'text_with_ws_without_citations',
        getter=get_span_text_with_ws_wo_cites,
        force=True
    )

    spacy_instance.add_pipe(
        retokenize_quotations,
        name='exclude_quotes',
        before='parser'
    )
    Token.set_extension('is_quotation', default=False, force=True)
    Span.set_extension(
        'tokens_without_quotations',
        getter=get_span_tokens_without_quotations,
        force=True
    )
    Span.set_extension(
        'text_without_quotations',
        getter=get_span_text_without_quotations,
        force=True
    )
    Span.set_extension(
        'text_with_ws_without_quotations',
        getter=get_span_text_with_ws_wo_quotations,
        force=True
    )

    Token.set_extension('is_excluded', default=False, force=True)
    Span.set_extension(
        'tokens_without_exclusions',
        getter=get_span_tokens_without_exclusions,
        force=True
    )
    Span.set_extension(
        'text_without_exclusions',
        getter=get_span_text_without_exclusions,
        force=True
    )
    Span.set_extension(
        'text_with_ws_without_exclusions',
        getter=get_span_text_with_ws_wo_exclusions,
        force=True
    )


def get_span_tokens_without_exclusions(span):
    """Returns an array of all tokens that are not quotations.
    :param span: Span object of the sentence
    """
    return [
        token for token in span if not
        (token._.is_quotation or token._.is_in_text_citation)
    ]


def get_span_text_without_exclusions(span):
    """Returns a string representation of the Span without quotations.
    :param span: Span object of the sentence
    """
    text = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not (tok._.is_quotation or tok._.is_in_text_citation):
            if next_tok is not None and \
                    (next_tok._.is_quotation or next_tok._.is_in_text_citation):
                text += tok.text
            else:
                text += tok.text_with_ws
    # Re-create whitespace stripping from original `Span.text()` method:
    # https://github.com/explosion/spaCy/blob/7ad000fce7824f237feec20e577f14c1c3a4a755/spacy/tokens/span.pyx#L500 # pylint: disable=line-too-long
    if span[-1].whitespace_:
        text = text[:-1]
    return text


def get_span_text_with_ws_wo_exclusions(span):
    """Returns a whitespace-included string of the Span w/o quotations.
    :param span: Span object of the sentence
    """
    text = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_quotation:
            if next_tok is not None and \
                    (next_tok._.is_quotation or next_tok._.is_in_text_citation):
                text += tok.text
            else:
                text += tok.text_with_ws
    return text


def get_span_tokens_without_quotations(span):
    """Returns an array of all tokens that are not quotations.
    :param span: Span object of the sentence
    """
    return [token for token in span if not token._.is_quotation]


def get_span_text_without_quotations(span):
    """Returns a string representation of the Span without quotations.
    :param span: Span object of the sentence
    """
    text = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_quotation:
            if next_tok is not None and next_tok._.is_quotation:
                text += tok.text
            else:
                text += tok.text_with_ws
    # Re-create whitespace stripping from original `Span.text()` method:
    # https://github.com/explosion/spaCy/blob/7ad000fce7824f237feec20e577f14c1c3a4a755/spacy/tokens/span.pyx#L500 # pylint: disable=line-too-long
    if span[-1].whitespace_:
        text = text[:-1]
    return text


def get_span_text_with_ws_wo_quotations(span):
    """Returns a whitespace-included string of the Span w/o quotations.
    :param span: Span object of the sentence
    """
    text = ''
    for tok, next_tok in zip_longest(span, span[1:]):
        if not tok._.is_quotation:
            if next_tok is not None and next_tok._.is_quotation:
                text += tok.text
            else:
                text += tok.text_with_ws
    return text


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


def retokenize_quotations(doc):
    """Locates quotations in the text, and makes them a single token.
    :param parsed_paragraphs: array of paragraphs as Doc objects
    """
    # Try me: regexr.com/50t16
    matches = re.finditer(
        r"\u201c.*\u201d",
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
            retokenizer.merge(span, attrs=QUOTATION_ATTRS)
            token_starts.append(span.start)

    for start in token_starts:
        doc[start].is_sent_start = False

    return doc


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
            retokenizer.merge(span, attrs=CITATION_ATTRS)
            token_starts.append(span.start)

    for start in token_starts:
        doc[start].is_sent_start = False

    return doc
