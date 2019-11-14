import itertools
from unittest.mock import MagicMock

import en_core_web_lg
import pytest
from spacy.language import Language
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span

from seniorproject.model.document import Document
from seniorproject.model.paragraph import Paragraph
from seniorproject.recommendation.recommendationhandler import \
    RecommendationHandler
from seniorproject.recommendation.simpletocompound.model.sentencetype import \
    SentenceType
from seniorproject.recommendation.simpletocompound.simpletocompound import \
    SimpleToCompound


# def duplicate_iter(iter):
#     return

@pytest.fixture
def simple_compound():
    spacy_instance = MagicMock(spec=Language)
    tf_session = MagicMock()
    tf_encodings = MagicMock()
    tf_input_placeholder = MagicMock()
    tf_sentence_piece_processor = MagicMock()

    simple_compound = SimpleToCompound(
        spacy_instance,
        tf_session,
        tf_encodings,
        tf_input_placeholder,
        tf_sentence_piece_processor
    )
    return simple_compound


@pytest.fixture
def spacy_instance():
    return en_core_web_lg.load()


@pytest.fixture
def single_sentence_paragraph():
    text = 'Mark went to the store.'

    paragraph = MagicMock(spec=Paragraph)
    spacy_doc = MagicMock(spec=Doc)

    spacy_doc.sents.__iter__.side_effect = lambda: iter(
        ['Mark went to the store.']
    )

    paragraph.text = text
    paragraph.idx = 0
    paragraph.spacy_doc = spacy_doc

    document = MagicMock(spec=Document)
    document.paragraphs = [paragraph]
    document.text = text

    return document


@pytest.fixture
def simple_sentences():
    text = 'Mark went to the store. His mom did not have food for dinner.'

    paragraph = MagicMock(spec=Paragraph)
    spacy_doc = MagicMock(spec=Doc)

    sentence1 = MagicMock(spec=Span)
    sentence1.text = 'Mark went to the store.'
    sentence1.start_char = 0
    sentence1.end_char = 0

    sentence2 = MagicMock(spec=Span)
    sentence2.text = 'His mom did not have food for dinner.'
    sentence2.start_char = 0
    sentence2.end_char = 0

    spacy_doc.sents.__iter__.side_effect = lambda: iter([sentence1, sentence2])

    paragraph.text = text
    paragraph.idx = 0
    paragraph.spacy_doc = spacy_doc

    document = MagicMock(spec=Document)
    document.paragraphs = [paragraph]
    document.text = text

    return document


@pytest.fixture
def simple_and_compound():
    text = 'Despite his efforts, John still failed his test. '
    'This lowered his grade.'

    paragraph = MagicMock(spec=Paragraph)
    spacy_doc = MagicMock(spec=Doc)

    sentence1 = MagicMock(spec=Span)
    sentence1.text = 'Despite his efforts, John still failed his test. '
    sentence1.start_char = 0
    sentence1.end_char = 0

    sentence2 = MagicMock(spec=Span)
    sentence2.text = 'This lowered his grade.'
    sentence2.start_char = 0
    sentence2.end_char = 0

    spacy_doc.sents.__iter__.side_effect = lambda: iter([sentence1, sentence2])

    paragraph.text = text
    paragraph.idx = 0
    paragraph.spacy_doc = spacy_doc

    document = MagicMock(spec=Document)
    document.paragraphs = [paragraph]
    document.text = text

    return document


def test_analyze_single_sentence_paragraph(
        simple_compound,
        single_sentence_paragraph
):
    assert simple_compound.analyze(single_sentence_paragraph) == []


def test_analyze_simple_sentences(
        simple_compound,
        simple_sentences
):
    simple_compound.sentence_type = MagicMock(
        side_effect=lambda _: SentenceType.SIMPLE)

    assert simple_compound.analyze(simple_sentences)[0].new_values == [
        'Mark went to the store, for his mom did not have food for dinner.',
        'Mark went to the store, and his mom did not have food for dinner.',
        'Mark went to the store, but his mom did not have food for dinner.',
        'Mark went to the store, or his mom did not have food for dinner.',
        'Mark went to the store, yet his mom did not have food for dinner.',
        'Mark went to the store, so his mom did not have food for dinner.'
    ]


def test_analyze_simple_and_compound_sentence(
        simple_compound,
        simple_and_compound
):
    def sent_type(sentence):
        if sentence == list(simple_and_compound.paragraphs[0].spacy_doc.sents)[
            0]:
            return SentenceType.SIMPLE
        else:
            return SentenceType.COMPLEX

    simple_compound.sentence_type = MagicMock(side_effect=sent_type)

    assert simple_compound.analyze(simple_and_compound) == []

def test_sentence_type_simple(
        simple_compound,
        spacy_instance
):
    document = spacy_instance('I like tea.')
    assert simple_compound.sentence_type(list(document.sents)[0]) == \
           SentenceType.SIMPLE


def test_sentence_type_compound(
        simple_compound,
        spacy_instance
):
    document = spacy_instance('I like tea, and he likes coffee.')
    assert simple_compound.sentence_type(list(document.sents)[0]) == \
           SentenceType.COMPOUND


def test_sentence_type_complex(
        simple_compound,
        spacy_instance
):
    document = spacy_instance(
        'When the kettle begins to whistle, you must take it off the stove.'
    )
    assert simple_compound.sentence_type(list(document.sents)[0]) == \
           SentenceType.COMPLEX


def test_sentence_type_complex_compound(
        simple_compound,
        spacy_instance
):
    document = spacy_instance(
        'Erin loves her brother, and he loves her too because she '
        'pays his bills.'
    )
    assert simple_compound.sentence_type(list(document.sents)[0]) == \
           SentenceType.COMPLEX_COMPOUND
