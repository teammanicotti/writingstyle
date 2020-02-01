from seniorproject.recommendation.comperativesuperlative.comp_super import ComparativeSuperlativeAnalyzer
from seniorproject.recommendation.simpletocompound.model.sentencetype import SentenceType
from tests.util.model import *

anal = ComparativeSuperlativeAnalyzer()


def sentence_to_doc_mock(paras_string, sentences_string, pos_map, head_map):
    # Mock all nodes that will be needed as head references by the spacy spans
    mocked_heads = dict(
        map(
            lambda head_word:
                (head_word, spacy_token_mock(head_word, pos_map.get(head_word, ''))),
                head_map.values()
        )
    )

    # Mock the entire spacy doc
    spacy_doc = spacy_doc_mock(
        list(
            map(
                lambda sentence: spacy_span_mock(
                    sentence, 0, 0,
                    list(
                        map(
                            lambda word:
                                spacy_token_mock(
                                    word,
                                    pos_=pos_map.get(word, ''),
                                    head=mocked_heads.get(head_map.get(word, None), None)),
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
        {},
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
    head_map = {
        "more": "happy"
    }
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        pos_map,
        head_map
    )
    findings = anal.analyze(test_doc)

    assert findings.__len__() == 1


def test_super_rec():
    para1_sentences = [
        "Johnny is the most angry."
    ]
    pos_map = {
        "angry": "ADJ"
    }
    head_map = {
        "most": "angry"
    }
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        pos_map,
        head_map
    )
    findings = anal.analyze(test_doc)

    assert findings.__len__() == 1


def test_comp_super_recs():
    para1_sentences = [
        "Johnny is more friendly than Jim, and the most smart student in his class."
    ]
    pos_map = {
        "friendly": "ADJ",
        "smart": "ADJ"
    }
    head_map = {
        "most": "smart",
        "more": "friendly"
    }
    test_doc = sentence_to_doc_mock(
        [" ".join(para1_sentences)],
        para1_sentences,
        pos_map,
        head_map
    )
    findings = anal.analyze(test_doc)

    assert findings.__len__() == 2
