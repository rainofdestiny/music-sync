import base64
from typing import Any
from urllib.parse import urlencode

from httpx import AsyncClient, HTTPStatusError
from loguru import logger

from app.config import settings
from app.spotify.schemas import AuthSchema, RefreshTokenAuthSchema


class OAuth:

    def __init__(self) -> None:
        self.client_id: str = settings.spotify_client_id
        self.client_secret: str = settings.spotify_client_secret
        self.redirect_uri: str = settings.spotify_redirect_uri
        self.scope: str = settings.spotify_scope

    @property
    def _basic_auth(self) -> str:
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

    async def _token_request(self, data: dict[str, str]) -> dict[str, Any]:
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {self._basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with AsyncClient(
            headers=headers, http2=True, timeout=10.0
        ) as client:
            response = await client.post(url, data=data)

            try:
                response.raise_for_status()
            except HTTPStatusError as e:
                match e.response.status_code:
                    case 401:
                        pass  # todo do smth
                    case _:
                        pass
            return response.json()

    async def refresh_token(self, refresh_token: str) -> RefreshTokenAuthSchema:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }
        try:
            response = await self._token_request(data)
            logger.info("Token refreshed successfully.")
            return RefreshTokenAuthSchema(**response)
        except HTTPStatusError as e:
            logger.error(f"Error refreshing token: {e.response.text}")
            raise ValueError(
                f"Error refreshing token: {e.response.text}"
            ) from e
        except Exception as e:
            logger.error(f"An error occurred: {e!s}")
            raise ValueError(f"An error occurred: {e!s}") from e

    async def gen_tokens(self, code: str) -> AuthSchema:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        response = await self._token_request(data)
        return AuthSchema(**response)
