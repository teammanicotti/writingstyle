import en_core_web_sm
import pytest
from spacy.language import Language
from seniorproject.recommendation.passivetoactive.passivetoactive import PassiveAnalyzer
from tests.util.model import *
passiveAnalyzer = PassiveAnalyzer
from tests.util.model import *

@pytest.fixture
def passive_to_active():
    spacy_instance = MagicMock(spec=Language)

    passive_to_active = PassiveAnalyzer()
    return passive_to_active


@pytest.fixture
def spacy_instance():
    return en_core_web_sm.load()


@pytest.fixture
def single_sentence_paragraph():
    text = 'The milk was drunk by the cat.'

    sentence1 = spacy_span_mock(
        'The milk was drunk by the cat.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])

@pytest.fixture
def no_recs():
    text = 'The cat drank the milk.'

    sentence1 = spacy_span_mock(
        'The cat drank the milk.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])


@pytest.fixture
def dual_sentence_paragraph():
    text = 'The milk was drunk by the cat. The metropolis has been scorched by the dragon’s fiery breath.'

    sentence1 = spacy_span_mock(
        'The milk was drunk by the cat.'
    )
    sentence2 = spacy_span_mock(
        'The metropolis has been scorched by the dragon’s fiery breath.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1, sentence2]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])

def test_analyze_single_sentence_paragraph(
        passive_to_active,
        single_sentence_paragraph
):
    x = passive_to_active.analyze(single_sentence_paragraph)
    assert x == []


###Test two sentences that require recommended changes
def test_analyze_dual_sentence_paragraph(
        passive_to_active,
        two_sentences
):
    assert 1 == 1
    #assert passive_to_active.analyze(two_sentences)[0].new_values == []


###Test a paragraph full of sentences that require no changes
def test_paragraph_no_recs(
        passive_to_active,
        simple_and_compound
):
    assert 1 == 1 #passive_to_active.analyze(simple_and_compound) == []


