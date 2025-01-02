import logging
import base64
import aiohttp
import redis

from fastapi import Depends

from app.config import settings
from app.depends import get_redis
from app.spotify.models import AuthModel, RefreshTokenAuthModel

logger = logging.getLogger(__name__)


class OAuth:
    _instance = None

    def __new__(cls):
        # Implementing singleton pattern to ensure a single instance of OAuth
        if not cls._instance:
            cls._instance = super(OAuth, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initializing only once to set up client credentials
        if not hasattr(self, "initialized"):
            self.client_id = settings.spotify_client_id
            self.client_secret = settings.spotify_client_secret
            self.redirect_uri = settings.spotify_redirect_uri
            self.initialized = True

    @property
    def auth_token(self) -> str:
        """Generates the authorization token in base64 format."""
        token = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(token.encode()).decode()

    async def get_access_token(self, r: redis.Redis = Depends(get_redis)) -> str:
        access_token = await r.get("spotify:access_token")
        if not access_token:
            access_token = await self._refresh_token(r)
        return access_token

    async def _refresh_token(self, r: redis.Redis) -> str:
        """Refreshes the access token using the refresh token."""
        refresh_token = await r.get("spotify:refresh_token")

        if not refresh_token:
            logger.error("Refresh token not found.")
            raise ValueError("Refresh token not found.")

        try:
            async with aiohttp.ClientSession() as session:
                url = "https://accounts.spotify.com/api/token"
                headers = {
                    "Authorization": f"Basic {self.auth_token}",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
                data = {
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": self.client_id,
                }
                async with session.post(
                    url=url, headers=headers, data=data
                ) as response:
                    response.raise_for_status()
                    logger.info("Token refreshed successfully.")
                    json_response = await response.json()
                    token_data = RefreshTokenAuthModel(**json_response)

                    access_token = token_data.access_token
                    await r.set("spotify:access_token", access_token, ex=token_data.expires_in)

                    return access_token

        except aiohttp.ClientResponseError as e:
            logger.error(f"Error refreshing token: {e.message}")
            raise ValueError(f"Error refreshing token: {e.message}") from e
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise ValueError(f"An error occurred: {str(e)}") from e

    async def gen_auth_data(self, code: str) -> AuthModel:
        logger.info("Starting generate token")
        async with aiohttp.ClientSession() as session:

            url = "https://accounts.spotify.com/api/token"
            headers = {
                "Authorization": f"Basic {self.auth_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            }

            async with session.post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                json_response = await response.json()
                return AuthModel(**json_response)


oauth = OAuth()
