import logging
from typing import List
from app.spotify.models import TrackModel, UserProfileModel
from app.spotify.utils import HTTPClient


logger = logging.getLogger(__name__)


class Client:

    @staticmethod
    async def get_me(access_token: str) -> UserProfileModel:
        async with HTTPClient() as c:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = await c.get(url="", headers=headers)
            response.raise_for_status()
            user = response.json()
            return UserProfileModel(**user)

    @staticmethod
    async def get_liked_tracks(
        *, access_token: str, limit: int = 50, offset: int = 0
    ) -> List[TrackModel]:
        async with HTTPClient() as c:
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"limit": limit, "offset": offset}
            response = await c.get("/tracks", headers=headers, params=params)
            response.raise_for_status()
            json_response = response.json()
            items = json_response.get("items", [])
            return [TrackModel(**item["track"]) for item in items]


client = Client()
