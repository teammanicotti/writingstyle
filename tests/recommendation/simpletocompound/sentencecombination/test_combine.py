import pytest

from seniorproject.recommendation.simpletocompound.sentencecombination.combine import \
    Combine
from tests.util.model import *


@pytest.fixture
def sentence1_mock():
    return spacy_span_mock(
        'He is watching videos.',
        0,
        0,
        [
            spacy_token_mock('He', 'PRON'),
            spacy_token_mock('is'),
            spacy_token_mock('watching'),
            spacy_token_mock('videos'),
            spacy_token_mock('.')
        ]
    )


@pytest.fixture
def sentence2_mock():
    return spacy_span_mock(
        'She is listening to the lecture.',
        0,
        0,
        [
            spacy_token_mock('She', 'PRON'),
            spacy_token_mock('is'),
            spacy_token_mock('listening'),
            spacy_token_mock('to'),
            spacy_token_mock('the'),
            spacy_token_mock('lecture'),
            spacy_token_mock('.')
        ]
    )


@pytest.fixture
def sentence3_mock():
    return spacy_span_mock(
        'He was more than happy to help me out.',
        0,
        0,
        [
            spacy_token_mock('He', 'PRON'),
            spacy_token_mock('was'),
            spacy_token_mock('more'),
            spacy_token_mock('than'),
            spacy_token_mock('happy'),
            spacy_token_mock('to'),
            spacy_token_mock('help'),
            spacy_token_mock('me'),
            spacy_token_mock('out'),
            spacy_token_mock('.')
        ]
    )


@pytest.fixture
def sentence4_mock():
    return spacy_span_mock(
        'I really appreciated it.',
        0,
        0,
        [
            spacy_token_mock('I', 'PRON'),
            spacy_token_mock('really'),
            spacy_token_mock('appreciate'),
            spacy_token_mock('it'),
            spacy_token_mock('.')
        ]
    )


@pytest.fixture
def sentence5_mock():
    return spacy_span_mock(
        'Jeff wants to go to the store.',
        0,
        0,
        [
            spacy_token_mock('Jeff', 'PROPN'),
            spacy_token_mock('wants'),
            spacy_token_mock('to'),
            spacy_token_mock('go'),
            spacy_token_mock('to'),
            spacy_token_mock('the'),
            spacy_token_mock('store'),
            spacy_token_mock('.')
        ]
    )


@pytest.fixture
def sentence6_mock():
    return spacy_span_mock(
        'Carol wants to eat ice cream.',
        0,
        0,
        [
            spacy_token_mock('Carol', 'PROPN'),
            spacy_token_mock('wants'),
            spacy_token_mock('to'),
            spacy_token_mock('eat'),
            spacy_token_mock('ice cream'),
            spacy_token_mock('.')
        ]
    )


def test_generate_combined_third_person_pronoun(sentence1_mock, sentence2_mock):
    expected = [
      "He is watching videos, for she is listening to the lecture.",
      "He is watching videos, and she is listening to the lecture.",
      "He is watching videos, but she is listening to the lecture.",
      "He is watching videos, or she is listening to the lecture.",
      "He is watching videos, yet she is listening to the lecture.",
      "He is watching videos, so she is listening to the lecture."
    ]
    assert Combine.generate_combined(sentence1_mock, sentence2_mock) == expected


def test_generate_combined_first_person_pronoun(sentence3_mock, sentence4_mock):
    expected = [
      "He was more than happy to help me out, for I really appreciated it.",
      "He was more than happy to help me out, and I really appreciated it.",
      "He was more than happy to help me out, but I really appreciated it.",
      "He was more than happy to help me out, or I really appreciated it.",
      "He was more than happy to help me out, yet I really appreciated it.",
      "He was more than happy to help me out, so I really appreciated it."
    ]
    assert Combine.generate_combined(sentence3_mock, sentence4_mock) == expected


def test_generate_combined_proper_noun(sentence5_mock, sentence6_mock):
    expected = [
      "Jeff wants to go to the store, for Carol wants to eat ice cream.",
      "Jeff wants to go to the store, and Carol wants to eat ice cream.",
      "Jeff wants to go to the store, but Carol wants to eat ice cream.",
      "Jeff wants to go to the store, or Carol wants to eat ice cream.",
      "Jeff wants to go to the store, yet Carol wants to eat ice cream.",
      "Jeff wants to go to the store, so Carol wants to eat ice cream."
    ]
    assert Combine.generate_combined(sentence5_mock, sentence6_mock) == expected

