import logging
import asyncio

from yandex_music import ClientAsync
from yandex_music.client_async import Search

from app.yandex.models import TrackModel, TrackIdsModel


logger = logging.getLogger(__name__)


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
