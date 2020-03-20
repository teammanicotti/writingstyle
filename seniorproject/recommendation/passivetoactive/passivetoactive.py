"""
Passive to active: class containing method to identify passive voice
and generate new sentences in the active voice
Author: Robert Liedka (rl5849)
"""
import re
from typing import List

import sentry_sdk
from sentry_sdk import capture_exception
from pattern.en import conjugate, PRESENT, PAST, PL, SG, INFINITIVE, \
    PARTICIPLE  # Yes, these always have red sqiggles under them

from seniorproject.recommendation.passivetoactive.SentenceTools import \
    SentenceTools
from seniorproject.recommendation.recommendationengine import \
    RecommendationEngine
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.document import Document



class PassiveAnalyzer(RecommendationEngine):
    """
    Passive to active: class containing method to identify passive voice
    and generate new sentences in the active voice
    Author: Robert Liedka (rl5849)
    """
    def __init__(self):
        super(PassiveAnalyzer, self).__init__()

    def analyze(self, doc: Document, **kwargs) -> List[Recommendation]:
        """
        Main analyze method
        :param doc:
        :return: Recommendation[]
        """
        results = []
        paragraph_index = 0
        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                results.extend(
                    PassiveAnalyzer.annotate_sentence(sent, paragraph_index))
            paragraph_index += 1
        return results

    @staticmethod
    def annotate_sentence(sentence, paragraph_index):
        """
        Annotate sentence: Perform passive analysis and generate new sentence
        if passive
        :param sentence:
        :param paragraph_index:
        :return: Recommendation[], empty array if not passive
        """
        results = []
        is_passive = False
        # TODO: Are we going to do anything with this?
        is_hard = False  # pylint: disable=unused-variable
        recommend_phrases = {}

        for word in sentence._.tokens_without_citations:
            if word.dep_ == "nsubjpass":
                is_passive = True
            elif word.dep_ == "auxpass":
                recommend_phrases[word.text + " " + word.head.text] = {
                    "index": word.head.i}
                is_passive = True
            elif word.pos_ == "ADP" and word.right_edge.dep_ == "pobj":
                is_hard = True  # TODO: Are we going to do anything with this?

        if is_passive:
            for rec in recommend_phrases:
                is_advice = False
                new_rec = Recommendation(
                    RecommendationType.PASSIVE_TO_ACTIVE,
                    sentence.text,
                    sentence.start,
                    sentence.end,
                    paragraph_index,  # paragraph index
                    [PassiveAnalyzer.create_new_sentence(sentence, is_advice)],
                    sentence.text + RecommendationType.PASSIVE_TO_ACTIVE,
                    0  # Confidence
                )
                new_rec.is_replaceable = (not is_advice)
                new_rec.text_to_highlight = rec
                results.append(new_rec)
        return results

    @staticmethod
    def create_new_sentence(parsed_sentence, is_advise):
        """
        Create a new sentence: conjugate verb and re-order parts of speech to
        make an active voice sentence
        :param parsed_sentence: spaCy object
        :return: string of sentence
        """
        # Questions never come out right
        if parsed_sentence[-1].text == "?":
            return ""
        punct = "."
        if parsed_sentence[-1].is_punct:
            punct = parsed_sentence[-1].text

        actor = SentenceTools.get_object_of_prep(parsed_sentence)
        new_actor = ""
        if actor:
            new_actor = SentenceTools.convert_pronoun(actor)

        new_sentence = []
        sentence = ""
        verb = SentenceTools.get_verb(parsed_sentence)
        subject = SentenceTools.get_subject(parsed_sentence)
        adverb = SentenceTools.get_adverb(verb, parsed_sentence)
        citation = SentenceTools.get_citation(parsed_sentence)
        direct_obj = SentenceTools.get_direct_object(parsed_sentence)
        new_verb = PassiveAnalyzer.conjugate(verb)
        new_subject = SentenceTools.convert_pronoun_as_subject(subject.lower())

        if new_actor and new_verb and subject:
            sentence = PassiveAnalyzer.assemble_new_sentence(
                parsed_sentence,
                new_actor,
                adverb,
                new_verb,
                new_subject,
                direct_obj,
                citation,
                punct
            )
        elif new_actor and new_verb:
            new_sentence.append(new_actor)
            new_sentence.append(new_verb)
            sentence = SentenceTools.build_sentence_from_list(
                parsed_sentence, new_sentence, "...")
        elif subject and new_verb:
            is_advise = True
            sentence = "Consider adding a subject and putting it before the object."
        return sentence

    @staticmethod
    def conjugate(verb):
        """Attempt to conjugate verb to past tense
        :param verb string of verb to conjugate
        :return string of past-tense conjuated verb
        """  # TODO: Add param and return details here
        try:
            new_verb = conjugate(verb=verb, tense=PAST, number=PL)
            return new_verb
        except Exception as e:
            capture_exception(e)
            sentry_sdk.add_breadcrumb(
                category='conjugation',
                message='Patterns conjugation failed'
            )

    @staticmethod
    def assemble_new_sentence(
            parsed_sentence,
            new_actor,
            adverb,
            new_verb,
            subject,
            direct_obj,
            citation,
            punct
    ):
        """
        Assemble sentence in active voice
        """
        new_sentence = [new_actor]
        if adverb != "":
            new_sentence.append(adverb)
        new_sentence.append(new_verb)
        new_sentence.append(subject)
        if direct_obj != "":
            new_sentence.append(direct_obj)
        modifier = SentenceTools.get_verb_modifier(parsed_sentence)
        if modifier != "":
            new_sentence.append(modifier)
        preps = SentenceTools.get_prepositions(parsed_sentence)
        if len(preps) != 0:
            for prep in preps:
                present = False
                for component in new_sentence:
                    if prep in component:
                        present = True
                if not present:
                    new_sentence.append(prep)
        if citation != "":
            new_sentence.append(citation)

        if citation != "":
            for i in range(len(new_sentence)):
                if new_sentence[i] != citation:
                    new_sentence[i] = re.sub(
                        r"\s*" + re.escape(citation),
                        "",
                        new_sentence[i]
                    )

        return SentenceTools.build_sentence_from_list(
            parsed_sentence,
            new_sentence,
            punct
        )