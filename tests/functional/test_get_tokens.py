# Test GET /tokens?q=query+terms


class ValidTokens(object):
    def __init__(self, client, path):
        self._client = client
        self._path = path

    def __enter__(self):
        response = self._client.get(self._path)
        response_body = response.json

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        for token_type in ["all", "adjectives", "nouns", "verbs", "noun_chunks"]:
            assert token_type in response_body["tokens"]

        for search_query in ["original_search_query", "corrected_search_query"]:
            assert search_query in response_body

        return response

    def __exit__(self, _a, _b, _c):
        pass


def test_stemmable_tokens_are_stemmed_returns_success(client):
    with ValidTokens(client, "/api/search/tokens?q=whiting") as r:
        actual = r.json
        expected = {
            'corrected_search_query': 'whiting',
            'expanded_search_query': 'merling whiting',
            'original_search_query': 'whiting',
            'tokens': {
                'adjectives': [],
                'all': ['merle', 'whiting'],
                'noun_chunks': ['whiting'],
                'nouns': ['whiting'],
                'verbs': ['merle'],
            },
        }

        assert actual == expected


def test_get_tokens_by_default_expands_explicit_synonyms_returns_success(client):
    with ValidTokens(client, "/api/search/tokens?q=red%20kite") as r:
        assert "red kite" in r.json["original_search_query"]
        assert "red kite" == r.json["corrected_search_query"]
        assert "bird" in r.json["expanded_search_query"]


def test_get_tokens_by_default_expands_equivalent_synonyms_returns_success(client):
    with ValidTokens(client, "/api/search/tokens?q=abdomen") as r:
        assert "abdomen" == r.json["original_search_query"]
        assert "abdomen" == r.json["corrected_search_query"]
        assert "abdomen belly stomach venter" == r.json["expanded_search_query"]


def test_get_tokens_expands_off_does_not_expand_synonyms_returns_success(client):
    with ValidTokens(client, "/api/search/tokens?q=abdomen&expand_synonyms=0") as r:
        assert "abdomen" == r.json["original_search_query"]
        assert "abdomen" == r.json["corrected_search_query"]
        assert "abdomen" == r.json["expanded_search_query"]


def test_get_tokens_by_default_corrects_spelling_returns_success(client):
    with ValidTokens(client, "/api/search/tokens?q=halbiut") as r:
        assert r.json["original_search_query"] != r.json["corrected_search_query"]


def test_get_tokens_spelling_on_corrects_spelling_returns_valid_json(client):
    with ValidTokens(client, "/api/search/tokens?q=halbiut&spell=1") as r:
        assert r.json["original_search_query"] != r.json["corrected_search_query"]


def test_get_tokens_spelling_off_corrects_spelling_returns_valid_json(client):
    with ValidTokens(client, "/api/search/tokens?q=halbiut&spell=0") as r:
        assert r.json["original_search_query"] == r.json["corrected_search_query"]


def test_get_tokens_empty_query_returns_200(client):
    with ValidTokens(client, "/api/search/tokens?q="):
        pass
