import logging
import asyncio

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from yandex_music import ClientAsync

from app.config import settings

client = asyncio.run(ClientAsync(settings.yandex_token).init())

router = APIRouter(prefix="/yandex")

logger = logging.getLogger(__name__)


@router.post("/add-tracks", response_model=JSONResponse)
async def add_tracks(tracks: list[str] = Body(...)):

    async def search(query: str) -> int | None:
        try:
            search_result = await client.search(query)
            if search_result and search_result.tracks and search_result.tracks.results:
                track = search_result.tracks.results[0]
                if hasattr(track, "id"):
                    return int(track.id)
            return None
        except Exception as e:
            logger.error(f"Error when searching for a track: {e}", exc_info=True)
            return None

    try:
        track_ids = list(
            filter(None, await asyncio.gather(*(search(track) for track in tracks)))
        )

        if not track_ids:
            logger.warning("No valid tracks found to add.")
            return JSONResponse(
                status_code=400,
                content={"message": "No valid tracks found to add."},
            )

        await client.users_likes_tracks_add(track_ids)
    except Exception as e:
        logger.error(f"Error when adding tracks: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred while adding tracks."},
        )

    logger.info("Tracks successfully added.")
    return JSONResponse(
        status_code=200,
        content={"message": "Tracks successfully added.", "track_ids": track_ids},
    )
