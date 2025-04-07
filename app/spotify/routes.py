import logging
import redis

from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException

from app.spotify.client import client
from app.spotify.oauth import oauth
from app.spotify.models import TrackModel
from app.spotify.depends import get_access_token_dependency

from app.spotify import service

from app.depends import get_redis
from loguru import logger

router = APIRouter(prefix="/spotify", tags=["Spotify"])


@router.get(
    "/auth",
    response_class=RedirectResponse,
    description="Redirecting to Spotify auth URL.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    include_in_schema=False,
)
def auth():
    return oauth.authorize_url


@router.get(
    "/callback",
    response_class=JSONResponse,
    response_model=dict,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def callback(
    code: str = Query(..., description="Authorization code returned by Spotify"),
    r: redis.Redis = Depends(get_redis),
):

    try:
        tokens = await oauth.gen_oauth_data(code)
        await service.cache_tokens(r, tokens)

        logger.info("Token generated successfully.")

        return RedirectResponse("/spotify/me")

    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed.")


@router.get("/me")
async def get_me(access_token: str = Depends(get_access_token_dependency)):
    return await client.get_me(access_token)


@router.get(
    "/tracks",
    response_class=JSONResponse,
    response_model=list[TrackModel],
    status_code=status.HTTP_200_OK,
)
async def get_liked_tracks(
    limit: int = Query(default=50, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    exclude_saved: bool = Query(default=False),
    access_token: str = Depends(get_access_token_dependency),
):
    tracks: list[TrackModel] = await client.get_liked_tracks(
        access_token=access_token, limit=limit, offset=offset
    )

    db = None
    saved_tracks = await service.get_saved_tracks(db)

    if exclude_saved:
        return list(filter(lambda track: track not in saved_tracks, tracks))

    return tracks
