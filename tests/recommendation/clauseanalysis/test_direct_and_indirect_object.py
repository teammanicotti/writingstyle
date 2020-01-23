import en_core_web_lg
import pytest

from seniorproject.recommendation.clauseanalysis.clauseanalysis import ClauseAnalysis
from tests.util.model import spacy_span_mock, spacy_doc_mock, paragraph_mock, document_mock


clause_analysis = ClauseAnalysis()

@pytest.fixture
def test_rewrite_sentence_direct_and_indirect_obj():
    text = 'I kicked the ball to her.'

    sentence1 = spacy_span_mock(
        'I kicked the ball to her.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)
    mock_document = document_mock(text, [paragraph])
    assert clause_analysis.analyze(mock_document)[0].new_values == [
        'I kicked her the ball.',
    ]

@pytest.fixture
def test_not_rewrite_sentence_direct_and_indirect_obj():
    text = 'I read Peter the report.'

    sentence1 = spacy_span_mock(
        'I read Peter the report.'
    )
    spacy_doc = spacy_doc_mock(
        [sentence1]
    )
    paragraph = paragraph_mock(text, spacy_doc)
    mock_document = document_mock(text, [paragraph])
    assert clause_analysis.analyze(mock_document) == []
