import logging
import base64
import redis

from fastapi import Depends

from app.config import settings
from app.depends import get_redis
from app.spotify.models import AuthModel
from app.spotify.api import gen_oauth_data, refresh_token

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

    @property
    def authorize_request(self) -> str:
        data = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": settings.spotify_scope,
            "redirect_uri": self.redirect_uri,
        }
        query = "&".join([f"{k}={v}" for k, v in data.items()])
        return f"https://accounts.spotify.com/authorize?{query}"

    async def get_access_token(self, r: redis.Redis = Depends(get_redis)) -> str:
        access_token = await r.get("spotify:access_token")
        if not access_token:
            access_token = await self._refresh_token(r)
        return access_token

    async def _refresh_token(self, r: redis.Redis) -> str:
        """Refreshes the access token using the refresh token."""
        _refresh_token = await r.get("spotify:refresh_token")

        if not _refresh_token:
            logger.error("Refresh token not found.")
            raise ValueError("Refresh token not found.")

        data = await refresh_token(
            refresh_token=_refresh_token,
            auth_token=self.auth_token,
            client_id=self.client_id,
        )
        await r.set("spotify:access_token", data.access_token, ex=data.expires_in)

        return data.access_token

    async def gen_data(self, code: str) -> AuthModel:
        logger.info("Starting generate token")
        auth_data = await gen_oauth_data(
            auth_token=self.auth_token, redirect_uri=self.redirect_uri, code=code
        )
        return auth_data


oauth = OAuth()
