import requests
from spellchecker import SpellChecker
from spacy.tokens import Span


class GrammarChecking:

    def __init__(self, spacy_instance, stop_words=None):
        self.nlp = spacy_instance
        self.stop_words = spacy_instance.Defaults.stop_words if stop_words is None else stop_words
        self.whitelist_words = {'pajamas'}
        self.whitelist_grammar = {'UPPERCASE_SENTENCE_START'}
        self.spell = SpellChecker()
        Span.set_extension('is_invalid_sentence', default=False, force=True)

    def check_sentence_spell(self, sentence):
        """
        Checks spelling in a sentence
        :param sentence: Doc
        :return: boolean
        """
        words = []
        for token in sentence:
            if token.text not in self.stop_words and token.text.lower() not in self.whitelist_words:
                words.append(token.text)
        wrong_spells = self.spell.unknown(words)
        return len(wrong_spells) == 0

    def check_sentence_grammar(self, sentence):
        """
        Checks grammar of a sentence
        :param sentence: str
        :return: boolean
        """
        params = [('language', 'en'), ('text', sentence)]
        response = requests.get('http://grammar:8081/v2/check', params)
        response_json = response.json()
        matches = response_json['matches']
        if len(matches) == 1 and matches[0]['rule']['id'] in self.whitelist_grammar:
            return True
        return len(matches) == 0

    def check_sentences(self, sentences):
        """
        Checks all sentences and return spacy doc with custom Span that has attribute is_invalid_sentence.
        If a sentence has either grammar error or spelling, the is_invalid_sentence will be True. You can
        access this attribute by sentence._.is_invalid_sentence
        :param sentences: str
        :return: Doc
        """
        doc = self.nlp(sentences)
        for sentence in doc.sents:
            if not (self.check_sentence_spell(sentence) and self.check_sentence_grammar(sentence.text)):
                # noinspection PyProtectedMember
                sentence._.set("is_invalid_sentence", True)
        return doc
