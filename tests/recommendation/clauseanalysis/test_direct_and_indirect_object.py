from seniorproject.recommendation.clauseanalysis.clauseanalysis import ClauseAnalysis
from tests.util.model import spacy_span_mock, spacy_doc_mock, paragraph_mock, document_mock

clause_analysis = ClauseAnalysis()


def sentence_to_mock_doc(text):
    sentence = spacy_span_mock(text)
    spacy_doc = spacy_doc_mock([sentence])
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])


def test_rewrite_sentence_direct_and_indirect_obj():
    text = 'I kicked the ball to her.'
    mock_document = sentence_to_mock_doc(text)
    assert clause_analysis.analyze(mock_document)[0].new_values == [
        'I kicked her the ball.',
    ]


def test_not_rewrite_sentence_direct_and_indirect_obj():
    text = 'I read Peter the report.'
    mock_document = sentence_to_mock_doc(text)
    assert clause_analysis.analyze(mock_document) == []
