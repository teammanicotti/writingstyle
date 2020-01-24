import en_core_web_sm
import pytest

from preprocessing import spacy_extensions


@pytest.fixture
def nlp():
    spacy_instance = en_core_web_sm.load()
    spacy_extensions.enable_spacy_extensions()
    spacy_instance.add_pipe(
        spacy_extensions.retokenize_citations,
        before='parser'
    )
    return spacy_instance


def test_et_al_author_nd_pp(nlp):
    parsed_sent = nlp(
        'He is eating a sandwich (Robers et al., n.d., pp. 34-36).'
    )

    assert list(parsed_sent.sents)[0]._.text_without_citations \
           == 'He is eating a sandwich.'

    assert list(parsed_sent.sents)[0][5].text \
           == '(Robers et al., n.d., pp. 34-36)'

    assert list(filter(
        lambda x: x.text == '(Robers et al., n.d., pp. 34-36)',
        list(list(parsed_sent.sents)[0]._.tokens_without_citations)
    )) == []


def test_et_al_author_year_p(nlp):
    parsed_sent = nlp(
        'John likes pizza (Markowski et al., 1872, p. 34).'
    )

    assert list(parsed_sent.sents)[0]._.text_without_citations \
           == 'John likes pizza.'

    assert list(parsed_sent.sents)[0][3].text \
           == '(Markowski et al., 1872, p. 34)'

    assert list(filter(
        lambda x: x.text == '(Markowski et al., 1872, p. 34)',
        list(list(parsed_sent.sents)[0]._.tokens_without_citations)
    )) == []


def test_ampersand_year_ppg(nlp):
    parsed_sent = nlp(
        'Our grades are exceptional (Markowski & Sarkowitz, 1995, ppg. 34).'
    )

    assert list(parsed_sent.sents)[0]._.text_without_citations \
           == 'Our grades are exceptional.'

    assert list(parsed_sent.sents)[0][4].text \
           == '(Markowski & Sarkowitz, 1995, ppg. 34)'

    assert list(filter(
        lambda x: x.text == '(Markowski & Sarkowitz, 1995, ppg. 34)',
        list(list(parsed_sent.sents)[0]._.tokens_without_citations)
    )) == []


def test_year_pg(nlp):
    parsed_sent = nlp(
        'Markowski describes our grades as exceptional (1995, ppg. 34).'
    )

    assert list(parsed_sent.sents)[0]._.text_without_citations \
           == 'Markowski describes our grades as exceptional.'

    assert list(parsed_sent.sents)[0][6].text \
           == '(1995, ppg. 34)'

    assert list(filter(
        lambda x: x.text == '(1995, ppg. 34)',
        list(list(parsed_sent.sents)[0]._.tokens_without_citations)
    )) == []


def test_nd_p(nlp):
    parsed_sent = nlp(
        'Markowski describes our grades as exceptional (n.d., ppg. 34).'
    )

    assert list(parsed_sent.sents)[0]._.text_without_citations \
           == 'Markowski describes our grades as exceptional.'

    assert list(parsed_sent.sents)[0][6].text \
           == '(n.d., ppg. 34)'

    assert list(filter(
        lambda x: x.text == '(n.d., ppg. 34)',
        list(list(parsed_sent.sents)[0]._.tokens_without_citations)
    )) == []


def test_page_only(nlp):
    parsed_sent = nlp(
        'Tilly (1992) describes war as the primary driver of the creation of a '
        'durable state structure (p. 79).'
    )

    assert list(parsed_sent.sents)[0]._.text_without_citations \
           == 'Tilly (1992) describes war as the primary driver of the ' \
              'creation of a durable state structure.'

    assert list(parsed_sent.sents)[0][18].text \
           == '(p. 79)'

    assert list(filter(
        lambda x: x.text == '(p. 79)',
        list(list(parsed_sent.sents)[0]._.tokens_without_citations)
    )) == []
