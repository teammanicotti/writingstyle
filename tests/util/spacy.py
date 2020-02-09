import en_core_web_lg
import pytest

from seniorproject.preprocessing import spacy_extensions


@pytest.fixture(scope='session')
def spacy_instance():
    nlp = en_core_web_lg.load()
    spacy_extensions.enable_spacy_extensions()
    nlp.add_pipe(spacy_extensions.retokenize_citations, before='parser')
    return nlp
