import en_core_web_lg
import pytest
from spacy.language import Language

from seniorproject.recommendation.simpletocompound.model.sentencetype import \
    SentenceType
from seniorproject.recommendation.simpletocompound.simpletocompound import \
    SimpleToCompound


from tests.util.model import *


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

    sentence1 = spacy_span_mock(
        'Mark went to the store.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])


@pytest.fixture
def simple_sentences():
    text = 'Mark went to the store. His mom did not have food for dinner.'

    sentence1 = spacy_span_mock(
        'Mark went to the store.'
    )
    sentence2 = spacy_span_mock(
        'His mom did not have food for dinner.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1, sentence2]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])


@pytest.fixture
def simple_and_compound():
    text = 'Despite his efforts, John still failed his test. '
    'This lowered his grade.'

    sentence1 = spacy_span_mock(
        'Despite his efforts, John still failed his test.'
    )
    sentence2 = spacy_span_mock(
        'This lowered his grade.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1, sentence2]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])


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
        if sentence == list(
                simple_and_compound.paragraphs[0].spacy_doc.sents)[0]:
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
