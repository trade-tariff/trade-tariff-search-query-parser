# Test GET /correct-terms?q=misspelled+terms

misspelled_terms = "halbiut sausadge stenolepsis chese bnoculars parnsip farmacy pape"


def test_get_correct_terms_returns_success(client):
    response = client.get(f"/api/search/correct-terms?q={misspelled_terms}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"


def test_get_correct_terms_returns_valid_json(client):
    response = client.get(f"/api/search/correct-terms?q={misspelled_terms}")

    response_body = response.json

    assert response_body["entities"]["correct_terms"] == [
        "halibut",
        "sausage",
        "stenolepis",
        "cheese",
        "binocular",
        "parsnip",
        "pharmacy",
        "paper",
    ]

    assert response_body["entities"]["original_terms"] == misspelled_terms


# When query is empty
def test_get_correct_terms_returns_400(client):
    misspelled_terms = ""
    response = client.get(f"/api/search/tokens?q={misspelled_terms}")

    assert response.status_code == 400
    assert response.text == "Error: the query params is empty."
