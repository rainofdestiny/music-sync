import logging

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from app.yandex.api import search, like
from app.yandex.models import TrackIdsModel, TrackModel
from app.yandex.depends import get_client


router = APIRouter(prefix="/yandex")

logger = logging.getLogger(__name__)


@router.post(
    "/tracks",
    response_class=JSONResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Yandex"],
)
async def add_tracks(tracks: list[TrackModel] = Body(...), client=Depends(get_client)):
    tracks_ids: list[TrackIdsModel] = await search(client, tracks)
    try:
        if not tracks_ids:
            logger.warning("No valid tracks found to add.")

            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "No valid tracks found to add."},
            )

        liked_tracks: list[int] = await like(client, [track.yandex_id for track in tracks_ids])  # type: ignore
    except Exception as e:
        logger.error(f"Error when adding tracks: {e}", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An error occurred while adding tracks."},
        )

    logger.info("Tracks successfully added.")
    result = [t_id.spotify for t_id in tracks_ids if t_id.yandex in liked_tracks]

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Tracks successfully added.", "tracks_ids": result},
    )
