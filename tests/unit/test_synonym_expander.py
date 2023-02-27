import pytest

from flaskr.synonym_expander import SynonymExpander


@pytest.fixture
def terms_to_tokens():
    return {
        "testing empty tokens": set(),
        "testingemptytokens": set(),
        "abridgement": {
            "abridgement",
            "abridgment",
        },
        "condensation": {"abridgment", "capsule", "condensation", "abridgement"},
        "abyssinian": {"abyssinian", "cat"},
        "yellow lemon": {"fruit"},
        "lemon": {"citrus fruit"},
        "red kite": {"alarming", "bird of prey"},
        "test": {"spaces"},
    }


def test_expand_single_word_match(terms_to_tokens):
    query = "abyssinian"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "abyssinian cat"
    assert expander.expand(query) == expected


def test_expand_multi_word_match(terms_to_tokens):
    query = "red kite"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "alarming bird of prey"
    assert expander.expand(query) == expected


def test_expand_no_match(terms_to_tokens):
    query = "pineapple"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "pineapple"
    assert expander.expand(query) == expected


def test_expand_multi_token_match(terms_to_tokens):
    query = "something about an abridgement"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "something about an abridgement abridgment"

    assert expander.expand(query) == expected


def test_expand_phrase_and_word_collision(terms_to_tokens):
    query = "yellow lemon is delicious"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "fruit is delicious citrus fruit"

    assert expander.expand(query) == expected


def test_expand_empty_query(terms_to_tokens):
    query = ""
    expander = SynonymExpander(terms_to_tokens, query)
    expected = ""

    assert expander.expand(query) == expected


def test_empty_tokens_phrase(terms_to_tokens):
    query = "testing empty tokens"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "testing empty tokens"

    assert expander.expand(query) == expected


def test_empty_tokens_word(terms_to_tokens):
    query = "testingemptytokens"
    expander = SynonymExpander(terms_to_tokens, query)
    expected = "testingemptytokens"

    assert expander.expand(query) == expected


def test_expand_with(terms_to_tokens):
    with SynonymExpander(terms_to_tokens, "red kite") as expanded_query:
        expected = "alarming bird of prey"

        assert expanded_query == expected
