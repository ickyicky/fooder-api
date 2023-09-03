import requests
import pytest
import os
import yaml


def get_api_url(service_name) -> str:
    with open("docker-compose.test.yml") as f:
        config = yaml.safe_load(f)

    port = config["services"][service_name]["ports"][0].split(":")[0]

    return f"http://localhost:{port}/"


class Client:
    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
    ):
        self.base_url = os.path.join(base_url, "api")
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/json"

        if username and password:
            self.login(username, password, True)

    def set_token(self, token: str) -> None:
        """set_token.

        :param token:
        :type token: str
        :rtype: None
        """
        self.session.headers["Authorization"] = "Bearer " + token

    def create_user(self, username: str, password: str) -> None:
        data = {"username": username, "password": password}
        response = self.post("user", json=data)
        response.raise_for_status()

    def login(self, username: str, password: str, force_login: bool) -> None:
        """login.

        :param username:
        :type username: str
        :param password:
        :type password: str
        :param force_login:
        :type password: bool
        :rtype: None
        """
        data = {"username": username, "password": password}

        response = self.post("token", data=data)

        if response.status_code != 200:
            if force_login:
                self.create_user(username, password)
                return self.login(username, password, False)
            else:
                raise Exception(f"Could not login as {username}")

        result = response.json()
        self.set_token(result["access_token"])

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(os.path.join(self.base_url, path), **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(os.path.join(self.base_url, path), **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(os.path.join(self.base_url, path), **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.session.patch(os.path.join(self.base_url, path), **kwargs)


@pytest.fixture
def unauthorized_client() -> Client:
    return Client(get_api_url("api"))


@pytest.fixture
def client(user_payload) -> Client:
    return Client(
        get_api_url("api"),
        username=user_payload["username"],
        password=user_payload["password"],
    )
