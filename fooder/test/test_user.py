import pytest


@pytest.mark.dependency()
def test_user_creation(unauthorized_client, user_payload_factory):
    response = unauthorized_client.post("user", json=user_payload_factory())
    assert response.status_code == 200, response.json()


@pytest.mark.dependency(depends=["test_user_creation"])
def test_user_login(client, user_payload):
    response = client.post("token", data=user_payload)
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["access_token"] is not None
    assert data["refresh_token"] is not None


@pytest.mark.dependency(depends=["test_user_login"])
def test_user_refresh_token(client, user_payload):
    response = client.post("token", data=user_payload)
    assert response.status_code == 200, response.json()

    token = response.json()["refresh_token"]
    payload = {"refresh_token": token}

    response = client.post("token/refresh", json=payload)
    assert response.status_code == 200, response.json()
