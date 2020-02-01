from seniorproject.recommendation.clauseanalysis.clauseanalysis import ClauseAnalysis
from tests.util.model import spacy_span_mock, spacy_doc_mock, paragraph_mock, document_mock, spacy_token_mock
import spacy

nlp = spacy.load('en_core_web_lg')
clause_analysis = ClauseAnalysis()


def sentence_to_mock_doc(text, mock_tokens=None):
    sentence = spacy_span_mock(text, tokens=mock_tokens)
    spacy_doc = spacy_doc_mock([sentence])
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])


def test_check_sentence_direct_and_indirect_obj_rewrite():
    text = 'I kicked the ball to her.'
    doc = nlp(text)
    assert ClauseAnalysis.check_sentence_direct_and_indirect_obj(next(doc.sents)) == 'I kicked her the ball.'


def test_check_sentence_direct_and_indirect_obj_not_rewrite():
    text = 'I rang your doorbell, but you didn’t answer.'
    doc = nlp(text)
    assert ClauseAnalysis.check_sentence_direct_and_indirect_obj(next(doc.sents)) is None


def test_check_sentence_direct_and_indirect_obj_not_rewrite_2():
    text = 'I kicked the ball to her.'
    doc = nlp(text)
    assert ClauseAnalysis.check_sentence_direct_and_indirect_obj(next(doc.sents)) == 'I kicked her the ball.'


def test_not_rewrite_sentence_direct_and_indirect_obj():
    text = 'I read Peter the report.'
    mock_tokens = [
        spacy_token_mock('read', 'VERB', 'ROOT'),
        spacy_token_mock('report', dep_='dobj')
    ]
    mock_document = sentence_to_mock_doc(text, mock_tokens)
    assert clause_analysis.analyze(mock_document) == []
