import logging
import base64

from urllib.parse import urlencode

from httpx import HTTPStatusError

from app.spotify.utils import HTTPClient

import redis.asyncio as redis

from app.config import settings
from app.spotify.models import AuthModel, RefreshTokenAuthModel


logger = logging.getLogger(__name__)


class AuthAPIClient:

    def __init__(self) -> None:
        self.client_id: str = settings.spotify_client_id
        self.client_secret: str = settings.spotify_client_secret
        self.redirect_uri: str = settings.spotify_redirect_uri
        self.scope: str = settings.spotify_scope

    @property
    def _auth_token(self) -> str:
        token = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(token.encode()).decode()

    @property
    def authorize_url(self) -> str:
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": self.scope,
            "redirect_uri": self.redirect_uri,
        }
        return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

    @staticmethod
    async def _post_token_request(url: str, headers: dict, data: dict) -> dict:
        async with HTTPClient() as c:
            response = await c.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()

    async def _refresh_token_request(
        self, refresh: str, auth: str
    ) -> RefreshTokenAuthModel:
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh,
            "client_id": self.client_id,
        }
        try:
            json_response = await self._post_token_request(url, headers, data)
            logger.info("Token refreshed successfully.")
            return RefreshTokenAuthModel(**json_response)
        except HTTPStatusError as e:
            logger.error(f"Error refreshing token: {e.response.text}")
            raise ValueError(f"Error refreshing token: {e.response.text}") from e
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise ValueError(f"An error occurred: {str(e)}") from e

    async def gen_oauth_data(self, code: str) -> AuthModel:

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {self._auth_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        json_response = await self._post_token_request(url, headers, data)
        return AuthModel(**json_response)


class OAuth(AuthAPIClient):
    _instance = None

    def __new__(cls):
        # Implementing singleton pattern to ensure a single instance of OAuth
        if not cls._instance:
            cls._instance = super(OAuth, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        # Initializing only once to set up client credentials
        if not hasattr(self, "initialized"):
            self.initialized = True

    async def get_access_token(self, r: redis.Redis) -> str:
        if not (token := await r.get("spotify:access_token")):
            token = await self._refresh_token(r)
        return token

    async def _refresh_token(self, r: redis.Redis) -> str:
        refresh_token_value = await r.get("spotify:refresh_token")
        if not refresh_token_value:
            logger.error("Refresh token not found.")
            raise ValueError("Refresh token not found.")
        data = await self._refresh_token_request(
            refresh=refresh_token_value,
            auth=self._auth_token,
        )
        await r.set("spotify:access_token", data.access_token, ex=data.expires_in)
        return data.access_token


oauth = OAuth()
