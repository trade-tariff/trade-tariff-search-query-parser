from flaskr.tokenizer import Tokenizer


def test_tokenizer_get_tokens(app):
    tokenizer = Tokenizer()
    search_query = "tall man"
    tokens = tokenizer.get_tokens(search_query)

    for token_type in ["all", "adjectives", "nouns", "verbs"]:
        assert token_type in tokens
