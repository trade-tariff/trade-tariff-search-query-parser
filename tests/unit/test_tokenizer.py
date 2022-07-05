from flaskr import tokenizer


def test_tokenizer_get_tokens(app):
    search_query = "tall man"
    tokens = tokenizer.get_tokens(search_query)

    for token_type in ["all", "adjectives", "nouns", "verbs"]:
        assert token_type in tokens
