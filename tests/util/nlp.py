import en_core_web_lg
import pytest

from preprocessing import spacy_extensions

@pytest.fixture(scope='session', autouse=True)
def nlp():
    spacy_instance = en_core_web_lg.load()
    spacy_extensions.enable_spacy_extensions()
    spacy_instance.add_pipe(
        spacy_extensions.retokenize_citations,
        before='parser'
    )
    return spacy_instance
