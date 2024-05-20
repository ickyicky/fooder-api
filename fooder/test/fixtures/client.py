from fooder.app import app
from httpx import AsyncClient
import pytest
import httpx


class Client:
    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
    ):
        self.client = AsyncClient(app=app, base_url="http://testserver/api")
        self.client.headers["Accept"] = "application/json"

    def set_token(self, token: str) -> None:
        """set_token.

        :param token:
        :type token: str
        :rtype: None
        """
        self.client.headers["Authorization"] = "Bearer " + token

    async def create_user(self, username: str, password: str) -> None:
        data = {"username": username, "password": password}
        response = await self.post("user", json=data)
        response.raise_for_status()

    async def login(self, username: str, password: str, force_login: bool) -> None:
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

        response = await self.post("token", data=data)

        if response.status_code != 200:
            if force_login:
                await self.create_user(username, password)
                return await self.login(username, password, False)
            else:
                raise Exception(
                    f"Could not login as {username}! Detail: {response.text}"
                )

        result = response.json()
        self.set_token(result["access_token"])

    async def get(self, path: str, **kwargs) -> httpx.Response:
        return await self.client.get(path, **kwargs)

    async def delete(self, path: str, **kwargs) -> httpx.Response:
        return await self.client.delete(path, **kwargs)

    async def post(self, path: str, **kwargs) -> httpx.Response:
        return await self.client.post(path, **kwargs)

    async def patch(self, path: str, **kwargs) -> httpx.Response:
        return await self.client.patch(path, **kwargs)


@pytest.fixture
def unauthorized_client() -> Client:
    return Client()


@pytest.fixture
async def client(user_payload) -> Client:
    client = Client()
    await client.login(user_payload["username"], user_payload["password"], True)
    return client
