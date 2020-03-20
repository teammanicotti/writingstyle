import pytest
from spacy.language import Language

from seniorproject.recommendation.simpletocompound.sentencecombination.\
    conjunctions import Conjunctions
from seniorproject.recommendation.simpletocompound.model.sentencetype import \
    SentenceType
from seniorproject.recommendation.simpletocompound.simpletocompound import \
    SimpleToCompound
from tests.util.model import *


@pytest.fixture
def simple_compound():
    spacy = MagicMock(spec=Language)
    tf_session = MagicMock()
    tf_encodings = MagicMock()
    tf_input_placeholder = MagicMock()
    tf_sentence_piece_processor = MagicMock()

    simple_compound = SimpleToCompound(
        spacy,
        tf_session,
        tf_encodings,
        tf_input_placeholder,
        tf_sentence_piece_processor
    )
    return simple_compound


@pytest.fixture
def single_sentence_paragraph():
    text = 'Mark went to the store.'

    sentence1 = spacy_span_mock(
        'Mark went to the store.'
    )
    sentence1._.text_without_citations = text
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])


@pytest.fixture
def simple_sentences():
    text = 'Mark went to the store. His mom did not have food for dinner.'

    sentence1 = spacy_span_mock(
        'Mark went to the store.',
        0,
        22,
        [
            spacy_token_mock('Mark'),
            spacy_token_mock('went'),
            spacy_token_mock('to'),
            spacy_token_mock('the'),
            spacy_token_mock('store'),
            spacy_token_mock('.', is_punct=True, idx=22)
        ]
    )
    sentence2 = spacy_span_mock(
        'His mom did not have food for dinner.',
        24,
        60,
        [
            spacy_token_mock('His'),
            spacy_token_mock('mom'),
            spacy_token_mock('did'),
            spacy_token_mock('not'),
            spacy_token_mock('have'),
            spacy_token_mock('food'),
            spacy_token_mock('for'),
            spacy_token_mock('dinner'),
            spacy_token_mock('.', is_punct=True, idx=60)
        ]
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
        'Despite his efforts, John still failed his test.',
        0,
        47,
        [
            spacy_token_mock('Despite'),
            spacy_token_mock('his'),
            spacy_token_mock('efforts'),
            spacy_token_mock(','),
            spacy_token_mock('John'),
            spacy_token_mock('still'),
            spacy_token_mock('failed'),
            spacy_token_mock('his'),
            spacy_token_mock('test'),
            spacy_token_mock('.', is_punct=True, idx=47)
        ]
    )
    sentence2 = spacy_span_mock(
        'This lowered his grade.',
        49,
        71,
        [
            spacy_token_mock('This'),
            spacy_token_mock('lowered'),
            spacy_token_mock('his'),
            spacy_token_mock('grade'),
            spacy_token_mock('.', is_punct=True, idx=71)
        ]
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

    similarity_classifier = MagicMock()
    similarity_scores = MagicMock()
    min_mock = MagicMock()

    min_mock.item = MagicMock(return_value=0.4)
    similarity_scores.min = MagicMock(return_value=min_mock)
    similarity_classifier.determine_similarity = MagicMock(return_value=similarity_scores)
    simple_compound.similarity_classifier = similarity_classifier

    result = simple_compound.analyze(
        simple_sentences,
        similarity_threshold=0.1
    )[0]
    assert result.new_parts == [
        'Mark went to the store, ',
        ' his mom did not have food for dinner.'
    ]
    assert result.conjunctions == [e.value for e in Conjunctions]


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

    assert simple_compound.analyze(
        simple_and_compound,
        similarity_threshold=0.1
    ) == []


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
