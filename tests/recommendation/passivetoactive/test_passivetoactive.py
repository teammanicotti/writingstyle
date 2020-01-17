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
def two_sentences():
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


# @pytest.fixture
# def simple_and_compound():
#     text = 'Despite his efforts, John still failed his test. '
#     'This lowered his grade.'
#
#     sentence1 = spacy_span_mock(
#         'Despite his efforts, John still failed his test.'
#     )
#     sentence2 = spacy_span_mock(
#         'This lowered his grade.'
#     )
#     spacy_doc = spacy_doc_mock(
#         [sentence1, sentence2]
#     )
#     paragraph = paragraph_mock(text, spacy_doc)
#
#     return document_mock(text, [paragraph])
#

def test_analyze_single_sentence_paragraph(
        passive_to_active,
        single_sentence_paragraph
):
    x = passive_to_active.analyze(single_sentence_paragraph)
    assert x == []


# def test_analyze_two_sentences(
#         passive_to_active,
#         two_sentences
# ):
    # assert passive_to_active.analyze(two_sentences)[0].new_values == [
    #     'Mark went to the store, for his mom did not have food for dinner.',
    #     'Mark went to the store, and his mom did not have food for dinner.',
    #     'Mark went to the store, but his mom did not have food for dinner.',
    #     'Mark went to the store, or his mom did not have food for dinner.',
    #     'Mark went to the store, yet his mom did not have food for dinner.',
    #     'Mark went to the store, so his mom did not have food for dinner.'
    # ]


# def test_analyze_simple_and_compound_sentence(
#         passive_to_active,
#         simple_and_compound
# ):
#     def sent_type(sentence):
#         if sentence == list(
#                 simple_and_compound.paragraphs[0].spacy_doc.sents)[0]:
#             return SentenceType.SIMPLE
#         else:
#             return SentenceType.COMPLEX
#
#     passive_to_active.sentence_type = MagicMock(side_effect=sent_type)
#
#     assert passive_to_active.analyze(simple_and_compound) == []


# def test_sentence_type_simple(
#         passive_to_active,
#         spacy_instance
# ):
#     document = spacy_instance('I like tea.')
#     assert passive_to_active.sentence_type(list(document.sents)[0]) == \
#        SentenceType.SIMPLE
#
#
# def test_sentence_type_compound(
#         passive_to_active,
#         spacy_instance
# ):
#     document = spacy_instance('I like tea, and he likes coffee.')
#     assert passive_to_active.sentence_type(list(document.sents)[0]) == \
#        SentenceType.COMPOUND

#
# def test_sentence_type_complex(
#         passive_to_active,
#         spacy_instance
# ):
#     document = spacy_instance(
#         'When the kettle begins to whistle, you must take it off the stove.'
#     )
#     assert passive_to_active.sentence_type(list(document.sents)[0]) == \
#        SentenceType.COMPLEX


# def test_sentence_type_complex_compound(
#         passive_to_active,
#         spacy_instance
# ):
#     document = spacy_instance(
#         'Erin loves her brother, and he loves her too because she '
#         'pays his bills.'
#     )
#     assert passive_to_active.sentence_type(list(document.sents)[0]) == \
#        SentenceType.COMPLEX_COMPOUND

# @pytest.fixture
# def do_test(test_type, test_text, expectation):
#     sentence = spacy_span_mock(
#         test_text
#     )
#     spacy_doc = spacy_doc_mock(
#         [sentence]
#     )
#     test_result = passiveAnalyzer.analyze(spacy_doc)
#
#     passed = test_result == expectation
#
#     if not passed:
#         print("Test failed: " + test_type)
#
# def test_analyze_simple_sentences():
#     test_cases = get_test_cases()
#
#     for test in test_cases:
#         do_test(test)
#
# def get_test_cases():
#     return [
#         ("Single sentence with recommendation", "The milk was drunk by the cat.", "The cat drank the milk.")
#     ]
#
#
# if __name__ == '__main__':
#     test_analyze_simple_sentences()