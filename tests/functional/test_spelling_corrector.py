# Test GET /correct-terms/<term>

def test_get_correct_terms_returns_success(client):
    wrong_terms = "-"

    response = client.get(f"/correct-terms/{wrong_terms}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

def test_get_correct_terms_returns_valid_json(client):
    wrong_terms = "halbiut sausadge stenolepsis chese bnoculars parnsip farmacy pape"

    response = client.get(f"/correct-terms/{wrong_terms}")

    response_body = response.json

    assert  response_body["entities"]["correct_terms"] == ['halibut',
                                                           'sausage',
                                                           'stenolepis',
                                                           'cheese',
                                                           'binocular',
                                                           'parsnip',
                                                           'pharmacy',
                                                           'paper' ]

    assert  response_body["entities"]["original_terms"] == wrong_terms
