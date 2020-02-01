import requests
from spellchecker import SpellChecker
from spacy.tokens import Span, Token


# noinspection PyProtectedMember
class GrammarChecking:

    def __init__(self, spacy_instance, stop_words=None):
        self.nlp = spacy_instance
        self.stop_words = spacy_instance.Defaults.stop_words if stop_words is None else stop_words
        self.whitelist_words = {'pajamas'}
        self.whitelist_grammar = {'UPPERCASE_SENTENCE_START'}
        self.spell = SpellChecker()

        Span.set_extension('has_grammar_errors', default=False, force=True)
        Span.set_extension('grammar_recommendation', default=[], force=True)

        Span.set_extension('has_spelling_errors', default=False, force=True)
        Token.set_extension('correct_spelling_candidates', default=[], force=True)

    def check_sentence_has_spelling_error(self, sentence):
        """
        Checks spelling in a sentence and set token with correct spelling candidates if it
        has spelling error
        :param sentence: Doc
        :return: boolean
        """
        has_spelling_error = False
        for token in sentence:
            if token.text not in self.stop_words and token.text.lower() not in self.whitelist_words:
                wrong_spells = self.spell.unknown([token.text])
                if len(wrong_spells) > 0:
                    has_spelling_error = True
                    token._.set('correct_spelling_candidates', self.spell.candidates(token.text))
        return has_spelling_error

    def check_sentence_has_grammar_error(self, sentence):
        """
        Checks grammar of a sentence. If it has grammar errors, the function will return
        True and the recommendation to fix it
        :param sentence: str
        :return: boolean
        """
        params = [('language', 'en'), ('text', sentence)]
        response = requests.get('http://localhost:8081/v2/check', params)
        response_json = response.json()
        matches = response_json['matches']
        recommendation = []
        has_grammar_errors = False

        if len(matches) == 1 and matches[0]['rule']['id'] in self.whitelist_grammar:
            return {"has_grammar_errors": has_grammar_errors, "recommendation": recommendation}

        if len(matches) > 0:
            has_grammar_errors = True
            for match in matches:
                recommendation.append({ "message": match["message"], "context": match["context"] });

        return {"has_grammar_errors": has_grammar_errors, "recommendation": recommendation}

    def check_sentences(self, sentences):
        """
        Checks all sentences and return the Spacy doc with new extension so you can check
        if a Spacy span has spelling or grammar errors and the fixing recommendation
        :param sentences: str
        :return: doc
        """
        results = []
        doc = self.nlp(sentences)
        for sentence in doc.sents:
            grammar_result = self.check_sentence_has_grammar_error(sentence.text)
            sentence._.set("has_grammar_errors", grammar_result["has_grammar_errors"])
            sentence._.set("grammar_recommendation", grammar_result["recommendation"])

            if self.check_sentence_has_spelling_error(sentence):
                sentence._.set("has_spelling_errors", True)

        return doc
