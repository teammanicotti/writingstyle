from seniorproject.preprocessing.grammarchecking.grammarchecking import GrammarChecking
import spacy

nlp = spacy.load('en_core_web_lg')
grammar = GrammarChecking(nlp)


# noinspection PyProtectedMember
def test_sentences_that_contains_sentence_has_spelling_error():
    sentences = "One morning I shot an elephant in my pajamas. How he got intto my pajamas? I'll never know."
    doc = grammar.check_sentences(sentences)

    index = 0
    for sentence in doc.sents:
        if index == 0:
            assert sentence._.has_grammar_errors is False
            assert sentence._.has_spelling_errors is False
        elif index == 1:
            assert sentence._.has_grammar_errors is False
            assert sentence._.has_spelling_errors is True
            for token in sentence:
                if token.text == "intto":
                    assert len(token._.correct_spelling_candidates) > 0
                else:
                    assert len(token._.correct_spelling_candidates) == 0
        elif index == 2:
            assert sentence._.has_grammar_errors is False
            assert sentence._.has_spelling_errors is False
        index += 1


# noinspection PyProtectedMember
def test_sentences_that_contains_sentence_has_grammar_error():
    sentences = "The food was eat by the man. The food was eaten by John."
    doc = grammar.check_sentences(sentences)

    index = 0
    for sentence in doc.sents:
        if index == 0:
            assert sentence._.has_grammar_errors is True
            assert len(sentence._.grammar_recommendation) > 0
            assert sentence._.has_spelling_errors is False
        elif index == 1:
            assert sentence._.has_grammar_errors is False
            assert sentence._.has_spelling_errors is False
        index += 1


# noinspection PyProtectedMember
def test_sentences_that_contains_sentence_has_grammar_error_and_spelling_error():
    sentences = "The food was eat by the mcn. The food was eaten by John."
    doc = grammar.check_sentences(sentences)

    index = 0
    for sentence in doc.sents:
        if index == 0:
            assert sentence._.has_grammar_errors is True
            assert len(sentence._.grammar_recommendation) > 0
            assert sentence._.has_spelling_errors is True
        elif index == 1:
            assert sentence._.has_grammar_errors is False
            assert sentence._.has_spelling_errors is False
        index += 1


# noinspection PyProtectedMember
def test_sentences_that_contains_all_valid_sentence():
    sentences = "Mark went to the store. His mom did not have food for dinner."
    doc = grammar.check_sentences(sentences)
    for sentence in doc.sents:
        assert sentence._.has_grammar_errors is False
        assert len(sentence._.grammar_recommendation) == 0
        assert sentence._.has_spelling_errors is False


def test_sentence_has_spelling_error():
    sentence = "The rat the ccat the dog chased killed ate the malt."
    assert grammar.check_sentence_has_spelling_error(nlp(sentence)) is True


def test_sentence_not_have_spelling_error():
    sentence = "The horse raced past the barn fell."
    assert grammar.check_sentence_has_spelling_error(nlp(sentence)) is False


def test_sentence_has_grammar_error():
    sentence = "The boy was was grumpy."
    result = grammar.check_sentence_has_grammar_error(sentence)
    assert result["has_grammar_errors"] is True
    assert len(result["recommendation"]) > 0


def test_sentence_not_have_grammar_error():
    sentence = "The food was eaten by John."
    result = grammar.check_sentence_has_grammar_error(sentence)
    assert result["has_grammar_errors"] is False
    assert len(result["recommendation"]) == 0
