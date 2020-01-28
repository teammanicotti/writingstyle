import requests
from spellchecker import SpellChecker

spell = SpellChecker()


def check_sentence_spell(sentence, stopwords):
    whitelist_words = {'pajamas'}
    words = []
    for token in sentence:
        if token.text not in stopwords and token.text.lower() not in whitelist_words:
            words.append(token.text)
    wrong_spells = spell.unknown(words)
    return len(wrong_spells) > 0


def check_sentence_grammar(sentence):
    URL = 'http://grammar:8081/v2/check'
    whitelist_grammar = {'UPPERCASE_SENTENCE_START'}
    params = [('language', 'en'), ('text', sentence)]
    response = requests.get(URL, params)
    response_json = response.json()
    matches = response_json['matches']
    if len(matches) == 1 and matches[0]['rule']['id'] in whitelist_grammar:
        return False
    return len(matches) > 0


def check_sentences(doc, stopwords):
    results = []
    for sentence in doc.sents:
        if check_sentence_spell(sentence, stopwords) or check_sentence_grammar(sentence.text):
            results.append({'sentence_start': sentence.start, 'sentence_end': sentence.end, 'text': sentence.text})
    return results
