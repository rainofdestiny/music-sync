from collections.abc import Generator, Mapping
from typing import Any, TypedDict, Unpack

from httpx import AsyncClient, Auth, Request, Response

from app.spotify.schemas import TrackSchema, UserProfileSchema


class BearerAuth(Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request: Request) -> Generator[Request, Response]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class RequestKwargs(TypedDict, total=False):
    params: Mapping[str, str | int]
    follow_redirects: bool
    auth: tuple[str, str] | None


class Client:

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def _request(
        self, url: str = "", **kwargs: Unpack[RequestKwargs]
    ) -> dict[Any, Any]:
        api_url = "https://api.spotify.com/v1/me/"
        auth = BearerAuth(self.access_token)

        async with AsyncClient(
            base_url=api_url, http2=True, timeout=10.0, auth=auth
        ) as client:
            response = await client.get(url, **kwargs)
            data = response.json()
            return data

    async def get_me(self) -> UserProfileSchema:
        data = await self._request()
        return UserProfileSchema(**data)

    async def get_liked_tracks(
        self, *, limit: int = 50, offset: int = 0
    ) -> list[TrackSchema]:
        params = {"limit": limit, "offset": offset}
        data = await self._request("/tracks", params=params)
        items = data.get("items", [])
        return [TrackSchema(**item["track"]) for item in items]
