# Test GET /tokens?q=query+terms


def test_get_tokens_returns_success(client):
    response = client.get("/api/search/tokens?q=query+terms")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_get_tokens_returns_valid_json(client):
    response = client.get("/api/search/tokens?q=query+terms")

    response_body = response.json

    assert "noun_chunks" in response_body["entities"]

    for token_type in ["all", "adjectives", "nouns", "verbs"]:
        assert token_type in response_body["entities"]["tokens"]


# When query is empty
def test_get_tokens_returns_400_when_query_is_(client):
    query = ""
    response = client.get(f"/api/search/tokens?q={query}")

    assert response.status_code == 400
    assert response.text == "Error: the query params is empty."
