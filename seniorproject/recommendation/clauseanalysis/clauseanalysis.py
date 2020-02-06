from typing import List

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.recommendation.recommendationengine import RecommendationEngine

SUBJ_TAGS = ['nsubj', 'nsubjpass']
CONNECTION_WORDS = ['to', 'for']


class ClauseAnalysis(RecommendationEngine):

    def __init__(self):
        super(ClauseAnalysis, self).__init__()

    def analyze(self, doc: Document) -> List[Recommendation]:
        results = []
        paragraph_index = 0

        for paragraph in doc.paragraphs:
            for sent in paragraph.spacy_doc.sents:
                result = ClauseAnalysis.check_sentence_direct_and_indirect_obj(sent)
                if result is not None:
                    results.append(
                        Recommendation(
                            RecommendationType.DIRECT_INDIRECT_CHECKING,
                            sent.text,
                            sent.start,
                            sent.end,
                            paragraph_index,
                            [result],
                            f'{sent.text}{result}{RecommendationType.DIRECT_INDIRECT_CHECKING}',
                            1
                        )
                    )
            paragraph_index += 1

        return results

    @staticmethod
    def check_sentence_direct_and_indirect_obj(sentence):
        """
        Rewrite the sentence if the direct object comes before indirect object
        :param sentence: Span
        :return: str
        """
        for token in sentence:
            if token.pos_ == "VERB" and token.dep_ == 'ROOT':
                token_index = token.i - sentence.start
                has_dobj = False
                has_obj = False

                for next_token in sentence[token_index + 1:]:
                    if next_token.dep_ in SUBJ_TAGS:
                        break

                    if next_token.text in CONNECTION_WORDS and has_dobj:
                        next_token_index = next_token.i - sentence.start
                        right_text = sentence[0:token_index + 1].text
                        middle_text = sentence[token_index + 1:next_token_index].text
                        left_text = sentence[next_token_index + 1:].text

                        for temp in sentence[next_token_index + 1:]:
                            if temp.dep_ in ['pobj']:
                                has_obj = True
                                break

                        if not has_obj:
                            return None

                        for temp in sentence[next_token_index + 1:]:
                            if temp._.is_in_text_citation:
                                temp_index = temp.i - sentence.start
                                middle_text += " " + sentence[temp_index:].text
                                left_text = sentence[next_token_index + 1:temp_index].text
                                break

                        end_sentence = left_text[len(left_text) - 1]

                        if end_sentence not in [".", "!", "?"]:
                            return right_text + ' ' + left_text + ' ' + middle_text

                        return right_text + ' ' + left_text[:len(left_text) - 1] + ' ' + middle_text + end_sentence

                    if next_token.dep_ in ['dobj']:
                        has_dobj = True

        return None
