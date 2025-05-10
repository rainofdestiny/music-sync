from typing import Any, Literal

from httpx import AsyncClient
from loguru import logger

from app.config import settings
from app.yandex.schemas import TrackSchema


class Client:
    _instance = None

    def __new__(cls) -> "Client":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._token = settings.yandex_token
            self._uid: int | None = None
            self._initialized = True

    @classmethod
    async def init(cls) -> "Client":
        instance = cls()
        # Если uid еще не установлен, выполняем запрос к API
        if instance._uid is None:
            instance._uid = await instance._get_uid()
        return instance

    async def _request(
        self, method: Literal["GET", "POST"], url: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        headers = {
            "X-Yandex-Music-Client": "YandexMusicAndroid/24023621",
            "Accept-Language": "ru",
            "Authorization": f"OAuth {self._token}",
        }
        api_url = "https://api.music.yandex.net"
        async with AsyncClient(
            base_url=api_url, http2=True, timeout=10.0, headers=headers
        ) as client:
            response = await client.request(method, url, **kwargs)

            try:
                response.raise_for_status()
            except Exception as e:
                logger.error("HTTP Error %s", e)
                return {"error": e}

            try:
                data = response.json()
            except Exception as e:
                logger.error("JSON error %s", e)
                return {"error": e}

            return data

    async def _get_uid(self) -> int | None:
        data = await self._request("GET", "/account/status")

        if uid := data.get("result", {}).get("account", {}).get("uid"):
            return uid

    async def get_id_of_liked_tracks(self) -> list[int]:
        # todo посмотреть есть ли возможность в API в запросе указать limit, offset
        data = await self._request("GET", f"/users/{self._uid}/likes/tracks")
        tracks = data.get("result", {}).get("library", {}).get("tracks", [])
        return [track.get("id") for track in tracks]

    async def get_track_by_id(
        self, track_ids: list[int] | int
    ) -> list[TrackSchema] | TrackSchema:
        data = await self._request(
            "POST", "tracks", data={"track-ids": track_ids}
        )
        return [TrackSchema(**track) for track in data.get("result", {})]

    async def get_liked_tracks(
        self, limit: int, offset: int
    ) -> list[TrackSchema] | TrackSchema | None:
        tracks_ids = await self.get_id_of_liked_tracks()
        tracks = await self.get_track_by_id(tracks_ids[offset : limit + offset])
        return tracks

    async def like(self, track_id: int):
        data = await self._request(
            "POST",
            f"/users/{self._uid}/likes/tracks/add-multiple",
            data={"tracks-ids": track_id},
        )
        return data

    async def search(self, query: str) -> TrackSchema:
        data = await self._request(
            "GET", "/search/suggest", params={"part": query}
        )
        return TrackSchema(
            **data.get("result", {}).get("best", {}).get("result", {})
        )


"""
async def search(client: ClientAsync, tracks: list[TrackModel]) -> list[TrackIdsModel]:
    result = []

    async def search_track(track: TrackModel) -> TrackIdsModel | None:

        try:
            search_result: Search | None = await client.search(track.full_title)

            if (
                not search_result
                or not search_result.best
                or search_result.best.type != "track"
            ):
                return None

            best_track = search_result.best.result

            return (
                TrackIdsModel(
                    s=track.id,
                    y=int(best_track.id),  # type: ignore
                )
                if best_track and best_track.id  # type: ignore
                else None
            )

        except Exception as e:
            logger.error(
                f"Ошибка при поиске трека '{track.full_title}': {e}", exc_info=True
            )
            return None

    track_ids = await asyncio.gather(*(search_track(track) for track in tracks))
    result = list(filter(None, track_ids))

    return result


async def like(client: ClientAsync, tracks_ids: list[int]) -> list[int]:
    return await asyncio.gather(  # type: ignore
        *(  # type: ignore
            track_id
            for track_id in tracks_ids
            if await client.users_likes_tracks_add(track_id)
        )
    )
"""
