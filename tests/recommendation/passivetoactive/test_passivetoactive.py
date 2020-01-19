import pytest
from seniorproject.recommendation.passivetoactive.passivetoactive import \
    PassiveAnalyzer
from tests.util.model import *

passiveAnalyzer = PassiveAnalyzer


@pytest.fixture
def passive_to_active():
    passive_to_active = PassiveAnalyzer()
    return passive_to_active


@pytest.fixture
def single_sentence_paragraph():
    text = 'The milk was drunk by the cat.'

    sentence1 = spacy_span_mock(
        'The milk was drunk by the cat.',
        0,
        0,
        [
            spacy_token_mock('The', 'DET', 'det'),
            spacy_token_mock('milk', 'NOUN', 'nsubj'),
            spacy_token_mock('was', 'AUX', 'ROOT'),
            spacy_token_mock('drunk', 'ADJ', 'acomp'),
            spacy_token_mock('by', 'ADP', 'prep'),
            spacy_token_mock('the', 'DET', 'det'),
            spacy_token_mock('cat', 'NOUN', 'pobj'),
            spacy_token_mock('.', 'PUNCT', 'punct')
        ]
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
        'The cat drank the milk.',
        0,
        0,
        [
            spacy_token_mock('The', 'DET', 'det'),
            spacy_token_mock('cat', 'NOUN', 'nsubj'),
            spacy_token_mock('drank', 'VERB', 'ROOT'),
            spacy_token_mock('the', 'DET', 'det'),
            spacy_token_mock('milk', 'NOUN', 'dobj'),
            spacy_token_mock('.', 'PUNCT', 'punct')
        ]
    )
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)

    return document_mock(text, [paragraph])


@pytest.fixture
def dual_sentence_paragraph():
    text = 'The milk was drunk by the cat. The metropolis has been scorched ' \
           'by the dragon’s fiery breath.'

    sentence1 = spacy_span_mock(
        'The milk was drunk by the cat.',
        0,
        0,
        [
            spacy_token_mock('The', 'DET', 'det'),
            spacy_token_mock('milk', 'NOUN', 'nsubj'),
            spacy_token_mock('was', 'AUX', 'ROOT'),
            spacy_token_mock('drunk', 'ADJ', 'acomp'),
            spacy_token_mock('by', 'ADP', 'prep'),
            spacy_token_mock('the', 'DET', 'det'),
            spacy_token_mock('cat', 'NOUN', 'pobj'),
            spacy_token_mock('.', 'PUNCT', 'punct')
        ]
    )
    sentence2 = spacy_span_mock(
        'The metropolis has been scorched by the dragon’s fiery breath.',
        0,
        0,
        [
            spacy_token_mock('The', 'DET', 'det'),
            spacy_token_mock('metropolis', 'NOUN', 'nsubjpass'),
            spacy_token_mock('has', 'AUX', 'aux'),
            spacy_token_mock('been', 'AUX', 'auxpass'),
            spacy_token_mock('scorched', 'VERB', 'ROOT'),
            spacy_token_mock('by', 'ADP', 'agent'),
            spacy_token_mock('the', 'DET', 'det'),
            spacy_token_mock('dragon', 'NOUN', 'poss'),
            spacy_token_mock("'s", 'PART', 'case'),
            spacy_token_mock('firey', 'ADJ', 'amod'),
            spacy_token_mock('breath', 'NOUN', 'pobj'),
            spacy_token_mock('.', 'PUNCT', 'punct')
        ]
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


# Test two sentences that require recommended changes
def test_analyze_dual_sentence_paragraph(
        passive_to_active,
        dual_sentence_paragraph
):
    assert passive_to_active.analyze(dual_sentence_paragraph)[0].new_values \
           == []


# Test a paragraph full of sentences that require no changes
def test_paragraph_no_recs(
        passive_to_active,
        no_recs
):
    assert passive_to_active.analyze(no_recs) == []
