import aiohttp
import logging
from app.spotify.models import AuthModel, TrackModel, RefreshTokenAuthModel


logger = logging.getLogger(__name__)


async def get_liked_tracks(access_token: str, limit: int, offset: int):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.get(url=url, headers=headers) as response:
            response.raise_for_status()
            json_response = await response.json()
            items = json_response.get("items", [])
            return [TrackModel(**item["track"]) for item in items]


async def refresh_token(refresh_token, auth_token, client_id):
    async with aiohttp.ClientSession() as session:
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
        }
        try:
            async with session.post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                logger.info("Token refreshed successfully.")
                json_response = await response.json()
                token_data = RefreshTokenAuthModel(**json_response)

                return token_data
        except aiohttp.ClientResponseError as e:
            logger.error(f"Error refreshing token: {e.message}")
            raise ValueError(f"Error refreshing token: {e.message}") from e
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise ValueError(f"An error occurred: {str(e)}") from e


async def gen_oauth_data(auth_token: str, redirect_uri: str, code: str) -> AuthModel:
    async with aiohttp.ClientSession() as session:

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        async with session.post(url=url, headers=headers, data=data) as response:
            response.raise_for_status()
            json_response = await response.json()
            return AuthModel(**json_response)
