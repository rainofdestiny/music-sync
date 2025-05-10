from fastapi import APIRouter, Body, Depends, Path, Query, status
from fastapi.responses import JSONResponse

from app.depends import PaginationDep
from app.yandex.client import Client
from app.yandex.depends import ClientDep, get_client
from app.yandex.schemas import TrackSchema

router = APIRouter(prefix="/yandex", tags=["Yandex"])


@router.get("/tracks")
async def get_tracks(client: ClientDep, pagination: PaginationDep):
    return await client.get_liked_tracks(
        limit=pagination.limit, offset=pagination.offset
    )


@router.get("/tracks/{track_id}")
async def get_track_by_id(client: ClientDep, track_id: int = Path(..., ge=1)):
    return await client.get_track_by_id(track_id)


@router.get("/search")
async def search_tracks(
    client: ClientDep, query: str = Query(default="", min_length=1)
):
    return await client.search(query=query)


@router.post(
    "/add-tracks",
    response_class=JSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_tracks(
    tracks: list[TrackSchema] = Body(...), client: Client = Depends(get_client)
):
    ...
    # tracks_ids: list[TrackIdsModel] = await search(client, tracks)
    # try:
    #     if not tracks_ids:
    #         logger.warning("No valid tracks found to add.")
    #
    #         return JSONResponse(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             content={"message": "No valid tracks found to add."},
    #         )
    #
    #     liked_tracks: list[int] = await like(client, [track.yandex_id for track in tracks_ids])  # type: ignore
    # except Exception as e:
    #     logger.error(f"Error when adding tracks: {e}", exc_info=True)
    #
    #     return JSONResponse(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         content={"message": "An error occurred while adding tracks."},
    #     )
    #
    # logger.info("Tracks successfully added.")
    # result = [t_id.spotify for t_id in tracks_ids if t_id.yandex in liked_tracks]
    #
    # return JSONResponse(
    #     status_code=status.HTTP_201_CREATED,
    #     content={"message": "Tracks successfully added.", "tracks_ids": result},
    # )
