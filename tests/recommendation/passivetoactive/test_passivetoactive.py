import pytest
import spacy
from seniorproject.recommendation.passivetoactive.passivetoactive import \
    PassiveAnalyzer
from tests.util.model import *
from tests.util.spacy import spacy_instance as nlp

passiveAnalyzer = PassiveAnalyzer

'''
Begin test fixtures
'''
@pytest.fixture
def passive_to_active():
    passive_to_active = PassiveAnalyzer()
    return passive_to_active


@pytest.fixture
def single_sentence_pass_paragraph(nlp):
    text = '"Help!" was called out by the man.'
    spacy_doc = nlp(text)
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])


@pytest.fixture
def no_errors_single_setence(nlp):
    text = 'The cat drank the milk.'
    spacy_doc = nlp(text)
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])

@pytest.fixture
def dual_sentence_paragraph(nlp):
    text = 'Odnblasnflqboanwfonj was written by the QA Engineer. This sentence was completed by a question mark?'

    spacy_doc = nlp(text)
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])

@pytest.fixture
def single_sentence_ellipsis(nlp):
    text = 'The input was ended by the QA Engineer...'
    spacy_doc = nlp(text)
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])


@pytest.fixture
def paragraph_no_recs(nlp):
    text = 'The cat drank the milk. Susan will bake two dozen cupcakes for ' \
           'the bake sale. The homeowners remodeled the house to help it sell. ' \
           'John was wrong all along.'
    spacy_doc = nlp(text)
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])


@pytest.fixture
def paragraph_multiple_recs(nlp):
    text = 'Patch 1.2.1231e was deployed by the System Administrator. The input was correctly rendered by the system. Odnblasnflqboanwfonj ' \
           'was written by the QA Engineer.'
    spacy_doc = nlp(text)
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])
'''
End Fixtures

Begin Tests
'''


#Single sentence w/ recommendation needed
#Original sent: "Help!" was called out by the man.
def test_analyze_single_sentence_pass_paragraph(
        passive_to_active,
        single_sentence_pass_paragraph
):
    x = passive_to_active.analyze(single_sentence_pass_paragraph)
    assert len(x) == 1 and x[0].new_values == ['The man called "help!".']


# Test two sentences that require recommended changes
#Original sent: Odnblasnflqboanwfonj was written by the QA Engineer. This sentence was completed by a question mark?
#The sentence with a question should be ignored
def test_analyze_dual_sentence_paragraph(
        passive_to_active,
        dual_sentence_paragraph
):
    result = passive_to_active.analyze(dual_sentence_paragraph)
    assert len(result) == 2 and result[0].new_values == ['The Qa engineer wrote Odnblasnflqboanwfonj.']


# Test a paragraph full of sentences that require no changes
def test_no_errors_single_setence(
        passive_to_active,
        no_errors_single_setence
):
    assert passive_to_active.analyze(no_errors_single_setence) == []

# Test a sentence that ends with an ellipsis
def test_single_sentence_ellipsis(
        passive_to_active,
        single_sentence_ellipsis
):
    assert passive_to_active.analyze(single_sentence_ellipsis)[0].new_values == ['The Qa engineer ended the input...']

# Test a sentence that ends with an ellipsis
def test_paragraph_no_recs(
        passive_to_active,
        paragraph_no_recs
):
    assert passive_to_active.analyze(paragraph_no_recs)== []

# Test a paragraph that contains multiple recommendations
def test_paragraph_multiple_recs(
        passive_to_active,
        paragraph_multiple_recs
):
    result = passive_to_active.analyze(paragraph_multiple_recs)
    assert result[0].new_values == ['The System administrator deployed patch 1.2.1231e.']
    assert result[1].new_values == ['The system correctly rendered the input.']
    assert result[2].new_values == ['The qa engineer wrote Odnblasnflqboanwfonj.']