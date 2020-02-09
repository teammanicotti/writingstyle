from seniorproject.recommendation.clauseanalysis.clauseanalysis import ClauseAnalysis
from tests.util.model import spacy_span_mock, spacy_doc_mock, paragraph_mock, document_mock, spacy_token_mock
from tests.util.spacy import spacy_instance as nlp

clause_analysis = ClauseAnalysis()


def sentence_to_mock_doc(text, mock_tokens=None):
    sentence = spacy_span_mock(text, tokens=mock_tokens)
    spacy_doc = spacy_doc_mock([sentence])
    paragraph = paragraph_mock(text, spacy_doc)
    return document_mock(text, [paragraph])


def test_check_sentence_direct_and_indirect_obj_rewrite_with_citation():
    text = 'I kicked the ball to her mom (n.d., ppg. 34).'
    doc = nlp(text)
    result = ClauseAnalysis.check_sentence_direct_and_indirect_obj(next(doc.sents))
    assert result == 'I kicked her mom the ball (n.d., ppg. 34).'


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
