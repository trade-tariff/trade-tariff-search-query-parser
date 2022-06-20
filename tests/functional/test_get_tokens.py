# Test GET /tokens/<term>

def test_get_tokens_returns_success(client):
    response = client.get("/tokens/red car")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_get_tokens_returns_valid_json(client):
    response = client.get("/tokens/red car")

    response_body = response.json

    assert "noun_chunks" in response_body["entities"]

    for token_type in ["all", "adjectives", "nouns", "verbs"]:
        assert token_type in response_body["entities"]["tokens"]
