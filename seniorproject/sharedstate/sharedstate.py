"""Contains state shared between WSGI forks"""
import os

import en_core_web_lg
import tensorflow as tf
import tensorflow_hub as hub
import sentencepiece as spm
from spacy.language import Language

from seniorproject.preprocessing import spacy_extensions
from seniorproject.sharedstate.ensemble_pipeline import EnsemblePipeline
from seniorproject.sharedstate.modellogic.formality import load_model

def init_tf():
    """Load in Universal Sentence Encoder and SentencePiece modules.
    Adapted from https://github.com/tensorflow/hub/blob/master/docs/common_issues.md#running-inference-on-a-pre-initialized-module  # pylint: disable=line-too-long
    """
    graph = tf.compat.v1.Graph()
    with graph.as_default():  # pylint: disable=not-context-manager
        input_placeholder = tf.compat.v1.sparse_placeholder(
            tf.int64,
            shape=[None, None]
        )
        module = hub.Module(
            'https://tfhub.dev/google/universal-sentence-encoder-lite/2'
        )
        init_op = tf.group(
            [
                tf.compat.v1.global_variables_initializer(),
                tf.compat.v1.tables_initializer()
            ]
        )
        encodings = module(
            inputs=dict(
                values=input_placeholder.values,
                indices=input_placeholder.indices,
                dense_shape=input_placeholder.dense_shape
            )
        )

        session = tf.compat.v1.Session(graph=graph)
        spm_path = session.run(module(signature='spm_path'))
        graph.finalize()
        session.run(init_op)
        sentence_piece_processor = spm.SentencePieceProcessor()
        sentence_piece_processor.Load(spm_path)

    # Reduce logging output.
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    return session, encodings, input_placeholder, sentence_piece_processor


spacy_instance: Language = en_core_web_lg.load()
spacy_extensions.enable_spacy_extensions()
spacy_instance.add_pipe(spacy_extensions.retokenize_citations, before='parser')

tf_session, tf_encodings, tf_input_placeholder, tf_sentence_piece_processor = \
    init_tf()

formality_models_fps = []
for subdir, dirs, files in os.walk("seniorproject/recommendation/formality/active_models"):
    formality_models_fps += list(map(lambda file: subdir + os.sep + file, files))

print(formality_models_fps)

formality_model = EnsemblePipeline(
    list(
        map(
            lambda model_file:
                load_model(model_file),
            formality_models_fps
        )
    )
)
