import pytest

from seniorproject.recommendation.comperativesuperlative.comp_super import ComparativeSuperlativeAnalyzer
from seniorproject.recommendation.simpletocompound.model.sentencetype import SentenceType
from tests.util.model import *

anal = ComparativeSuperlativeAnalyzer()


def sentence_to_doc_mock(paras_string, sentences_string, pos_map):
    spacy_doc = spacy_doc_mock(
        list(
            map(
                lambda sentence: spacy_span_mock(
                    sentence, 0, 0,
                    list(
                        map(
                            lambda word:
                                spacy_token_mock(word, pos_map.get(word, '')),
                                sentence.split()
                        )
                    )
                ),
                sentences_string
            )
        )
    )
    paras = list(
        map(
            lambda x: paragraph_mock(x, spacy_doc),
            paras_string
        )
    )

    doc = document_mock("\n\n".join(paras_string), paras)
    doc.sentence_type = MagicMock(
        side_effect=lambda _: SentenceType.SIMPLE)

    return doc


def test_no_recs():
    para1_sentences = [
        "Johnny is a man."
    ]
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        {}
    )
    findings = anal.analyze(test_doc)

    assert findings == []


def test_comp_rec():
    para1_sentences = [
        "Johnny is more happy than Timothy."
    ]
    pos_map = {
        "happy": "ADJ"
    }
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        pos_map
    )
    findings = anal.analyze(test_doc)

    assert findings.__len__() == 1


def test_super_rec():
    para1_sentences = [
        "Johnny is a man."
    ]
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        {}
    )
    findings = anal.analyze(test_doc)

    assert findings == []


def test_comp_super_recs():
    para1_sentences = [
        "Johnny is a man."
    ]
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        {}
    )
    findings = anal.analyze(test_doc)

    assert findings == []
