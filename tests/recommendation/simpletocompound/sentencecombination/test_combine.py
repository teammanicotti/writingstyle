# pylint: disable-all
from unittest.mock import MagicMock

import pytest
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from seniorproject.recommendation.simpletocompound.sentencecombination.combine import \
    Combine


@pytest.fixture
def sentence1_mock():
    token_mock = MagicMock(spec=Token)
    token_mock.pos_ = 'PRON'
    token_mock.text = 'He'

    sentence_mock = MagicMock(spec=Span)
    sentence_mock.text = 'He is watching videos.'
    sentence_mock.__getitem__.return_value = token_mock

    return sentence_mock


@pytest.fixture
def sentence2_mock():
    token_mock = MagicMock(spec=Token)
    token_mock.pos_ = 'PRON'
    token_mock.text = 'He'

    sentence_mock = MagicMock(spec=Span)
    sentence_mock.text = 'She is listening to the lecture.'
    sentence_mock.__getitem__.return_value = token_mock

    return sentence_mock


@pytest.fixture
def sentence3_mock():
    token_mock = MagicMock(spec=Token)
    token_mock.pos_ = 'PRON'
    token_mock.text = 'He'

    sentence_mock = MagicMock(spec=Span)
    sentence_mock.text = 'He was more than happy to help me out.'
    sentence_mock.__getitem__.return_value = token_mock

    return sentence_mock


@pytest.fixture
def sentence4_mock():
    token_mock = MagicMock(spec=Token)
    token_mock.pos_ = 'PRON'
    token_mock.text = 'I'

    sentence_mock = MagicMock(spec=Span)
    sentence_mock.text = 'I really appreciated it.'
    sentence_mock.__getitem__.return_value = token_mock

    return sentence_mock


@pytest.fixture
def sentence5_mock():
    token_mock = MagicMock(spec=Token)
    token_mock.pos_ = 'PROPN'
    token_mock.text = 'Jeff'

    sentence_mock = MagicMock(spec=Span)
    sentence_mock.text = 'Jeff wants to go to the store.'
    sentence_mock.__getitem__.return_value = token_mock

    return sentence_mock


@pytest.fixture
def sentence6_mock():
    token_mock = MagicMock(spec=Token)
    token_mock.pos_ = 'PROPN'
    token_mock.text = 'Carol'

    sentence_mock = MagicMock(spec=Span)
    sentence_mock.text = 'Carol wants to eat ice cream.'
    sentence_mock.__getitem__.return_value = token_mock

    return sentence_mock


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

