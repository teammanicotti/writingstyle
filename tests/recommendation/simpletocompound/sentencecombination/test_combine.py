import pytest

from seniorproject.recommendation.simpletocompound.sentencecombination.combine import \
    Combine
from tests.util.model import *


@pytest.fixture
def sentence1_mock():
    return spacy_span_mock(
        'He is watching videos.',
        0,
        21,
        [
            spacy_token_mock('He', 'PRON'),
            spacy_token_mock('is'),
            spacy_token_mock('watching'),
            spacy_token_mock('videos'),
            spacy_token_mock('.', is_punct=True, idx=21)
        ]
    )


@pytest.fixture
def sentence2_mock():
    return spacy_span_mock(
        'She is listening to the lecture.',
        23,
        54,
        [
            spacy_token_mock('She', 'PRON'),
            spacy_token_mock('is'),
            spacy_token_mock('listening'),
            spacy_token_mock('to'),
            spacy_token_mock('the'),
            spacy_token_mock('lecture'),
            spacy_token_mock('.', is_punct=True, idx=54)
        ]
    )


@pytest.fixture
def sentence3_mock():
    return spacy_span_mock(
        'He was more than happy to help me out.',
        0,
        37,
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
            spacy_token_mock('.', is_punct=True, idx=37)
        ]
    )


@pytest.fixture
def sentence4_mock():
    return spacy_span_mock(
        'I really appreciated it!',
        39,
        62,
        [
            spacy_token_mock('I', 'PRON'),
            spacy_token_mock('really'),
            spacy_token_mock('appreciate'),
            spacy_token_mock('it'),
            spacy_token_mock('!', is_punct=True, idx=62)
        ]
    )


@pytest.fixture
def sentence5_mock():
    return spacy_span_mock(
        'Jeff wants to go to the store.',
        0,
        29,
        [
            spacy_token_mock('Jeff', 'PROPN'),
            spacy_token_mock('wants'),
            spacy_token_mock('to'),
            spacy_token_mock('go'),
            spacy_token_mock('to'),
            spacy_token_mock('the'),
            spacy_token_mock('store'),
            spacy_token_mock('.', is_punct=True, idx=29)
        ]
    )


@pytest.fixture
def sentence6_mock():
    return spacy_span_mock(
        'Carol wants to eat ice cream.',
        31,
        59,
        [
            spacy_token_mock('Carol', 'PROPN'),
            spacy_token_mock('wants'),
            spacy_token_mock('to'),
            spacy_token_mock('eat'),
            spacy_token_mock('ice cream'),
            spacy_token_mock('.', is_punct=True, idx=59)
        ]
    )


@pytest.fixture
def sentence7_mock():
    return spacy_span_mock(
      'This is good!',
      0,
      12,
      [
          spacy_token_mock('This'),
          spacy_token_mock('is'),
          spacy_token_mock('good'),
          spacy_token_mock('!', is_punct=True, idx=12)
      ]
    )


@pytest.fixture
def sentence8_mock():
    return spacy_span_mock(
        'This is better!',
        14,
        28,
        [
            spacy_token_mock('This'),
            spacy_token_mock('is'),
            spacy_token_mock('better'),
            spacy_token_mock('!', is_punct=True, idx=28)
        ]
    )

@pytest.fixture
def sentence9_mock():
    return spacy_span_mock(
      'Is this good?',
      0,
      12,
      [
          spacy_token_mock('Is'),
          spacy_token_mock('this'),
          spacy_token_mock('good'),
          spacy_token_mock('?', is_punct=True, idx=12)
      ]
    )


@pytest.fixture
def sentence10_mock():
    return spacy_span_mock(
        'Is this better?',
        14,
        28,
        [
            spacy_token_mock('Is'),
            spacy_token_mock('this'),
            spacy_token_mock('better'),
            spacy_token_mock('?', is_punct=True, idx=28)
        ]
    )


@pytest.fixture
def sentence11_mock():
    return spacy_span_mock(
      'This is good.',
      0,
      12,
      [
          spacy_token_mock('This'),
          spacy_token_mock('is'),
          spacy_token_mock('good'),
          spacy_token_mock('.', is_punct=True, idx=12)
      ]
    )


@pytest.fixture
def sentence12_mock():
    return spacy_span_mock(
        'This is better!',
        14,
        28,
        [
            spacy_token_mock('This'),
            spacy_token_mock('is'),
            spacy_token_mock('better'),
            spacy_token_mock('!', is_punct=True, idx=28)
        ]
    )

def test_generate_combined_third_person_pronoun(sentence1_mock, sentence2_mock):
    expected = [
      'He is watching videos, for she is listening to the lecture.',
      'He is watching videos, and she is listening to the lecture.',
      'He is watching videos, but she is listening to the lecture.',
      'He is watching videos, or she is listening to the lecture.',
      'He is watching videos, yet she is listening to the lecture.',
      'He is watching videos, so she is listening to the lecture.'
    ]
    assert Combine.generate_combined(sentence1_mock, sentence2_mock) == expected


def test_generate_combined_first_person_pronoun(sentence3_mock, sentence4_mock):
    expected = [
      'He was more than happy to help me out, for I really appreciated it.',
      'He was more than happy to help me out, and I really appreciated it.',
      'He was more than happy to help me out, but I really appreciated it.',
      'He was more than happy to help me out, or I really appreciated it.',
      'He was more than happy to help me out, yet I really appreciated it.',
      'He was more than happy to help me out, so I really appreciated it.'
    ]
    assert Combine.generate_combined(sentence3_mock, sentence4_mock) == expected


def test_generate_combined_proper_noun(sentence5_mock, sentence6_mock):
    expected = [
      'Jeff wants to go to the store, for Carol wants to eat ice cream.',
      'Jeff wants to go to the store, and Carol wants to eat ice cream.',
      'Jeff wants to go to the store, but Carol wants to eat ice cream.',
      'Jeff wants to go to the store, or Carol wants to eat ice cream.',
      'Jeff wants to go to the store, yet Carol wants to eat ice cream.',
      'Jeff wants to go to the store, so Carol wants to eat ice cream.'
    ]
    assert Combine.generate_combined(sentence5_mock, sentence6_mock) == expected


def test_exclamation_endings(sentence7_mock, sentence8_mock):
    expected = [
        'This is good, for this is better!',
        'This is good, and this is better!',
        'This is good, but this is better!',
        'This is good, or this is better!',
        'This is good, yet this is better!',
        'This is good, so this is better!',
    ]
    assert Combine.generate_combined(sentence7_mock, sentence8_mock) == expected

def test_question_endings(sentence9_mock, sentence10_mock):
    expected = [
        'Is this good, for is this better?',
        'Is this good, and is this better?',
        'Is this good, but is this better?',
        'Is this good, or is this better?',
        'Is this good, yet is this better?',
        'Is this good, so is this better?',
    ]
    assert Combine.generate_combined(sentence9_mock, sentence10_mock) == expected


def test_differing_endings(sentence11_mock, sentence12_mock):
    expected = [
        'This is good, for this is better.',
        'This is good, and this is better.',
        'This is good, but this is better.',
        'This is good, or this is better.',
        'This is good, yet this is better.',
        'This is good, so this is better.',
    ]
    assert Combine.generate_combined(sentence11_mock, sentence12_mock) == expected
