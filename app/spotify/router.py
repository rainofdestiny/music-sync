import logging
import redis

from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException

from app.spotify import api
from app.spotify import crud
from app.spotify.oauth import oauth
from app.spotify.models import TrackModel
from app.depends import get_redis

router = APIRouter(prefix="/spotify")

logger = logging.getLogger(__name__)


@router.get(
    "/auth",
    response_class=RedirectResponse,
    description="Redirecting to Spotify auth URL.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    include_in_schema=False,
)
def auth():
    return oauth.authorize_request


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
        auth = await oauth.gen_data(code)
        await crud.cache_tokens(r, auth)

        logger.info("Token generated successfully.")

        return {"ok": True, "detail": "You can close this page"}
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed.")


@router.get(
    "/get-liked-tracks",
    response_class=JSONResponse,
    response_model=list[TrackModel],
    status_code=status.HTTP_200_OK,
)
async def get_liked_tracks(
    limit: int = Query(default=50, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    access_token: str = Depends(oauth.get_access_token),
):
    return await api.get_liked_tracks(access_token, limit, offset)
