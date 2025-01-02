import logging
import aiohttp
import redis

from fastapi import APIRouter, Query, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException


from app.spotify.models import TrackModel, AuthorizeRequestModel
from app.spotify.oauth import oauth
from app.depends import get_redis


router = APIRouter(prefix="/spotify")

logger = logging.getLogger(__name__)


@router.get("/auth", response_class=RedirectResponse)
def auth():
    logger.info("Redirecting to Spotify auth URL.")
    return AuthorizeRequestModel().url


@router.get("/callback", response_class=JSONResponse)
async def callback(
    code: str = Query(..., description="Authorization code returned by Spotify"),
    r: redis.Redis = Depends(get_redis),
):
    try:
        auth = await oauth.gen_auth_data(code)

        await r.set("spotify:access_token", auth.access_token, ex=auth.expires_in)
        await r.set("spotify:refresh_token", auth.refresh_token)

        logger.info("Token generated successfully.")

        return {"ok": True, "detail": "You can close this page"}
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed.")


@router.get("/get-liked-tracks", response_class=JSONResponse)
async def get_liked_tracks(
    limit: int = Query(default=50, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    access_token: str = Depends(oauth.get_access_token),
):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.get(url=url, headers=headers) as response:
            response.raise_for_status()
            json_response = await response.json()
            items = json_response.get("items", [])
            return [TrackModel(**track["track"]) for track in items]
