"""Encapsulates the logic of determining sentence type and similarity."""

from typing import List
from spacy.tokens import Span

from seniorproject.model.document import Document
from seniorproject.model.recommendation import Recommendation
from seniorproject.model.recommendationtype import RecommendationType
from seniorproject.model.sentence import Sentence
from seniorproject.recommendation.recommendationengine import \
    RecommendationEngine
from seniorproject.recommendation.simpletocompound.model.sentencetype import \
    SentenceType
from seniorproject.recommendation.simpletocompound.semanticsimilarity import \
    similarityclassifier
from seniorproject.recommendation.simpletocompound.sentencecombination.combine import \
    Combine

__author__ = 'Devon Welcheck, Doanh Pham'

SUBJ_TAGS = ['nsubj', 'nsubjpass', 'expl']


class SimpleToCompound(RecommendationEngine):
    """Determines sentence type and similarity"""
    def __init__(
            self,
            spacy_instance,
            tf_session,
            tf_encodings,
            tf_input_placeholder,
            tf_sentence_piece_processor
    ):
        super(SimpleToCompound, self).__init__()
        self.nlp = spacy_instance
        self.similarity_classifier = \
            similarityclassifier.SimilarityClassifier(
                tf_session,
                tf_encodings,
                tf_input_placeholder,
                tf_sentence_piece_processor
            )

    def analyze(self, doc: Document, **kwargs) -> List[Recommendation]:
        """Determines the sentence type and similarity of sentence pairs

        Analyzes the provides text using spaCy.  Then, the sentences are
        lexically analyzed to determine their type.  After this, the sentences
        are paired and analyzed for their similarity and the results of the
        paired analysis are returned.
        :param doc: Document to be analyzed
        :param threshold: float threshold of minimum similarity.
        :return: list of recommendations created
        """
        results = []
        sentences = []
        for paragraph in doc.paragraphs:
            if len(list(paragraph.spacy_doc.sents)) < 2:
                continue
            for sent in paragraph.spacy_doc.sents:
                sent_type = self.sentence_type(sent)
                sentences.append(
                    Sentence(
                        sent.text,
                        sent.start_char,
                        sent.end_char,
                        doc.paragraphs.index(paragraph),
                        sent_type,
                        sent
                    )
                )

        sentence_pairs = list(zip(sentences, sentences[1:]))
        for first, second in sentence_pairs:
            if first.sentence_type is SentenceType.SIMPLE and \
                    second.sentence_type is SentenceType.SIMPLE:
                similarity_scores = self.similarity_classifier \
                    .determine_similarity([
                        first.span._.text_without_citations,
                        second.span._.text_without_citations
                ])
                similarity_score = similarity_scores.min().item()  # pylint: disable=no-member,line-too-long

                if similarity_score >= kwargs.get('similarity_threshold'):
                    results.append(Recommendation(
                        RecommendationType.SIMPLE_TO_COMPOUND,
                        f'{first.text} {second.text}',
                        first.start_position,
                        second.end_position,
                        first.paragraph_idx,
                        Combine.generate_combined(
                            first.span,
                            second.span
                        ),
                        f'{first.text} {second.text}',

                    ))
        return results

    @staticmethod
    def sentence_type(sentence: Span) -> SentenceType:
        """Determines the type of a sentence

        Determines the type of a sentence based on its lexical components.
        :param sentence: Span object containing a sentence
        :return: SentenceType enum object representing the sentence type
        """
        is_compound = False
        is_complex = False
        for token in sentence._.tokens_without_citations:
            if token.dep_ in SUBJ_TAGS and token.head.pos_ == 'VERB' and \
                    token.head.dep_ != 'ROOT':
                if token.head.dep_ == 'conj':
                    is_compound = True
                else:
                    is_complex = True
        if is_complex and is_compound:
            return SentenceType.COMPLEX_COMPOUND
        if is_complex:
            return SentenceType.COMPLEX
        if is_compound:
            return SentenceType.COMPOUND
        return SentenceType.SIMPLE
