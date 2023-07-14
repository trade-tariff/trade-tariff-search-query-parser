def test_isolated_healthcheck_returns_ok(client):
	response = client.get("/healthcheckz")
	response_body = response.json

	assert response.status_code == 200
	assert response_body["message"] == "OK"
