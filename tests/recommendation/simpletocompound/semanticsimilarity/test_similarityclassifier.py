import pytest
import tensorflow as tf
import tensorflow_hub as hub
import sentencepiece as spm

from seniorproject.recommendation.simpletocompound.semanticsimilarity import \
    similarityclassifier


@pytest.fixture
def similarity_classifier():
    session, encodings, input_placeholder, sentence_piece_processor = init_tf()
    return similarityclassifier.SimilarityClassifier(
        session,
        encodings,
        input_placeholder,
        sentence_piece_processor
    )


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
            "https://tfhub.dev/google/universal-sentence-encoder-lite/2"
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
        spm_path = session.run(module(signature="spm_path"))
        graph.finalize()
        session.run(init_op)
        sentence_piece_processor = spm.SentencePieceProcessor()
        sentence_piece_processor.Load(spm_path)

    # Reduce logging output.
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    return session, encodings, input_placeholder, sentence_piece_processor


def test_sentence_to_sparse(similarity_classifier):
    actual = similarity_classifier.sentence_to_sparse([
        'Mark went to the store.',
        'His mom did not have food for dinner.'
    ])
    expected = (
        [3008, 609, 10, 9, 1097, 6, 1159, 1593, 235, 35, 32, 568, 22, 3852, 6],
        [
            [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [1, 1],
            [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8]
        ],
        (2, 9)
    )
    assert actual == expected


def test_sentence_similarity_pair_pair1(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Mark went to the store.",
        "His mom did not have food for dinner."
    ])
    assert pytest.approx(score.min()) == 0.37345582


def test_sentence_similarity_pair_pair2(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "He was hungry.",
        "He went to the store."
    ])
    assert pytest.approx(score.min()) == 0.6078238


def test_sentence_similarity_pair_pair3(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "John's snacks were salty.",
        "He got some water to drink."
    ])
    assert pytest.approx(score.min()) == 0.43913352


def test_sentence_similarity_pair_pair4(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Thelma has homework due tomorrow.",
        "She went to dinner."
    ])
    assert pytest.approx(score.min()) == 0.3347076


def test_sentence_similarity_pair_pair5(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "I want to learn about their languages since it is my hobby.",
        "Moreover, I love cooking."
    ])
    assert pytest.approx(score.min()) == 0.34918985


def test_sentence_similarity_pair_pair6(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Moreover, I love cooking.",
        "I want to taste their varieties of foods from them."
    ])
    assert pytest.approx(score.min()) == 0.49475044


def test_sentence_similarity_pair_pair7(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "He was more than happy to help me out.",
        "I really appreciated it."
    ])
    assert pytest.approx(score.min()) == 0.53130245


def test_sentence_similarity_pair_pair8(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "The rooms were so roomy.",
        "And the furniture was spacious for my clothes."
    ])
    assert pytest.approx(score.min()) == 0.64702916


def test_sentence_similarity_pair_pair9(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "I was born in Febuaray 4th, 1994.",
        "I born at Clarktown Regional Hosptail."
    ])
    assert pytest.approx(score.min()) == 0.469665


def test_sentence_similarity_pair_pair10(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "He hitted fence with his face.",
        "He was still alive."
    ])
    assert pytest.approx(score.min()) == 0.53307056


def test_sentence_similarity_pair_pair11(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "She called the ambulance to come.",
        "So, I left and went to school."
    ])
    assert pytest.approx(score.min()) == 0.32369423


def test_sentence_similarity_pair_pair12(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Then, I move to Olston Co.",
        "I live in country farm!"
    ])
    assert pytest.approx(score.min()) == 0.4497968


def test_sentence_similarity_pair_pair13(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Mark went to the butcher shop.",
        "He does not like meat."
    ])
    assert pytest.approx(score.min()) == 0.45000637


def test_sentence_similarity_pair_pair14(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Martha likes Mary.",
        "She is her best friend."
    ])
    assert pytest.approx(score.min()) == 0.46784163


def test_sentence_similarity_pair_pair15(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Jeff wants to go to the store.",
        "Carol wants to eat ice cream."
    ])
    assert pytest.approx(score.min()) == 0.5396721


def test_sentence_similarity_pair_pair16(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Paul is scared of ghosts.",
        "He wrote an essay."
    ])
    assert pytest.approx(score.min()) == 0.14849013


def test_sentence_similarity_pair_pair17(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "She is good at writing.",
        "Stuart is a mouse."
    ])
    assert pytest.approx(score.min()) == 0.282171


def test_sentence_similarity_pair_pair18(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "Jessica likes to play games.",
        "Mark enjoys teriyaki chicken."
    ])
    assert pytest.approx(score.min()) == 0.29278386


def test_sentence_similarity_pair_pair19(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "He is watching videos.",
        "She is listening to the lecture."
    ])
    assert pytest.approx(score.min()) == 0.4729926


def test_sentence_similarity_pair_pair20(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "I am voting.",
        "Paul is in class."
    ])
    assert pytest.approx(score.min()) == 0.19630712


def test_sentence_similarity_pair_pair21(similarity_classifier):
    score = similarity_classifier.determine_similarity([
        "I have assignments due.",
        "Tom likes pizza."
    ])
    assert pytest.approx(score.min()) == 0.09610552
