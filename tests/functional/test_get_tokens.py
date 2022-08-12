# Test GET /tokens?q=query+terms


def test_get_tokens_returns_success(client):
    response = client.get("/api/search/tokens?q=query+terms")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_get_tokens_returns_valid_json(client):
    response = client.get("/api/search/tokens?q=query+terms")

    response_body = response.json

    for token_type in ["all", "adjectives", "nouns", "verbs", "noun_chunks"]:
        assert token_type in response_body["tokens"]

    for search_query in ["original_search_query", "corrected_search_query"]:
        assert search_query in response_body


# When query is empty
def test_get_tokens_returns_200(client):
    query = ""
    response = client.get(f"/api/search/tokens?q={query}")

    assert response.status_code == 200
