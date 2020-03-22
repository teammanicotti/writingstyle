import en_core_web_lg
import pytest

from seniorproject.preprocessing import spacy_extensions


@pytest.fixture(scope='session')
def spacy_instance():
    nlp = en_core_web_lg.load()
    spacy_extensions.enable_extensions(nlp)
    return nlp
