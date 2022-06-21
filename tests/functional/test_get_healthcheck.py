# Test GET /healthcheck


def test_get_healthcheck_returns_success(client):
    response = client.get("/api/search/healthcheck")

    assert response.status_code == 200


def test_get_healthcheck_returns_correct_header(client):
    response = client.get("/api/search/healthcheck")

    assert response.headers["Content-Type"] == "application/json"


def test_get_healthcheck_returns_valid_json(client):
    response_body = client.get("/api/search/healthcheck").json

    assert response_body["git_sha1"] == "aa603866"
    assert response_body["healthy"]
