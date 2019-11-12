"""Calculates the semantic similarity of sentences."""

import tensorflow as tf
import tensorflow_hub as hub
import sentencepiece as spm
import numpy as np

__author__ = 'Devon Welcheck'


class SimilarityClassifier:
    """Calculates the similarity score between two sentences.
    Similarity scores provided are on a scale of 0 to 1.
    Scores are generated using the Google TensorFlow Universal Sentence Encoder
    (Lite) v2.
    """

    def __init__(
            self,
            tf_session,
            tf_encodings,
            tf_input_placeholder,
            tf_sentence_piece_processor
    ):
        self.session = tf_session
        self.encodings = tf_encodings
        self.input_placeholder = tf_input_placeholder
        self.sentence_piece_processor = tf_sentence_piece_processor

    def determine_similarity(self, sentences: list) -> np.ndarray:
        """Determines the similarity of a list of sentences.

        Given a list of sentences, get their embeddings to perform semantic
        similarity analysis.
        :param sentences: list of sentence strings
        :return: ndarray of similarity scores
        """
        values, indices, dense_shape = self.sentence_to_sparse(sentences)
        message_embeddings = self.session.run(
            self.encodings,
            feed_dict={self.input_placeholder.values: values,
                       self.input_placeholder.indices: indices,
                       self.input_placeholder.dense_shape: dense_shape}
        )
        similarity_scores = np.inner(message_embeddings, message_embeddings)
        return similarity_scores

    def sentence_to_sparse(self, sentences: list) -> tuple:
        """Converts sentences to SparseTensor-similar format.

        Utility method that processes sentences with the sentence piece
        processor and returns the results in tf.SparseTensor-similar format
        (values, indices, dense_shape)
        :param sentences: list of sentence strings
        :return: tuple of id encodings, indices, and dense_shape
        """
        ids = [self.sentence_piece_processor.EncodeAsIds(x) for x in sentences]
        max_len = max(len(x) for x in ids)
        dense_shape = (len(ids), max_len)
        values = [item for sublist in ids for item in sublist]
        indices = [[row, col] for row in range(len(ids)) for col in
                   range(len(ids[row]))]
        return values, indices, dense_shape
