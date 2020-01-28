from seniorproject.preprocessing.grammarchecking.grammarchecking import GrammarChecking
import spacy

nlp = spacy.load('en_core_web_lg')
grammar = GrammarChecking(nlp)


# noinspection PyProtectedMember
def test_sentences_that_contains_sentence_has_spelling_error():
    sentences = "One morning I shot an elephant in my pajamas. How he got intto my pajamas I'll never know."
    doc = grammar.check_sentences(sentences)
    for sentence in doc.sents:
        if sentence.text is "One morning I shot an elephant in my pajamas.":
            assert sentence._.is_invalid_sentence is False
        elif sentence.text is "How he got intto my pajamas I'll never know.":
            assert sentence._.is_invalid_sentence is True


# noinspection PyProtectedMember
def test_sentences_that_contains_sentence_has_grammar_error():
    sentences = "The food was eat by the man. The food was eaten by John."
    doc = grammar.check_sentences(sentences)
    for sentence in doc.sents:
        if sentence.text is "The food was eat by the man.":
            assert sentence._.is_invalid_sentence is True
        elif sentence.text is "The food was eaten by John.":
            assert sentence._.is_invalid_sentence is False


# noinspection PyProtectedMember
def test_sentences_that_contains_all_valid_sentence():
    sentences = "Mark went to the store. His mom did not have food for dinner."
    doc = grammar.check_sentences(sentences)
    for sentence in doc.sents:
        assert sentence._.is_invalid_sentence is False


def test_sentence_has_spelling_error():
    sentence = "The rat the ccat the dog chased killed ate the malt."
    assert grammar.check_sentence_spell(nlp(sentence)) is False


def test_sentence_not_have_spelling_error():
    sentence = "The horse raced past the barn fell."
    assert grammar.check_sentence_spell(nlp(sentence)) is True


def test_sentence_has_grammar_error():
    sentence = "The boy was was grumpy."
    assert grammar.check_sentence_grammar(sentence) is False


def test_sentence_not_have_grammar_error():
    sentence = "The food was eaten by John."
    assert grammar.check_sentence_grammar(sentence) is True

