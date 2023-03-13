from flaskr.tokenizer import Tokenizer


def test_tokenizer_get_tokens(app):
    search_query = "The 'quick' brown fox jumped over the \"lazy\" dog."
    tokenizer = Tokenizer(search_query)
    tokens = tokenizer.get_tokens()

    expected = {
        'quoted': [
            "'quick'",
            '"lazy"'
        ],
        'unquoted': [
            'The',
            'brown',
            'fox',
            'jumped',
            'over',
            'the',
            'dog.',
        ],
        'nouns': [
            'fox',
            'dog',
        ],
        'verbs': ['jump'],
        'adjectives': ['brown'],
        'noun_chunks': ['The brown fox', 'the dog'],
    }

    assert tokens == expected


def test_stem_excluded_token(app):
    search_query = "clothes and clothing"
    tokenizer = Tokenizer(search_query)
    tokens = tokenizer.get_tokens()

    assert "clothes" in tokens["nouns"]
