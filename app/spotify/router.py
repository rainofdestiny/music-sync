import logging
import aiohttp

from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException


from app.spotify.models import TrackModel, AuthorizeRequestModel
from app.spotify.oauth import oauth


router = APIRouter(prefix="/spotify")

logger = logging.getLogger(__name__)


@router.get("/auth", response_class=RedirectResponse)
def auth():
    logger.info("Redirecting to Spotify auth URL.")
    return AuthorizeRequestModel().url


@router.get("/callback", response_class=JSONResponse)
async def callback(code: str = Query()):
    try:
        await oauth.gen_token(code)
        logger.info("Token generated successfully.")
        return {"ok": True, "detail": "You can close this page"}
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed.")


@router.get("/get-liked-tracks")
async def get_liked_tracks(
    limit: int = Query(default=50, ge=1, le=50, strict=True),
    offset: int = Query(default=0, ge=0, strict=True),
):

    # todo: Попробовать обьеденить функции в 1

    @oauth
    async def get(access_token: str, *, limit=limit, offset=offset) -> list[str]:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}"
            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get(url=url, headers=headers) as response:
                response.raise_for_status()
                json_response = await response.json()
                items = json_response.get("items", [])
                tracks = [TrackModel(**track["track"]) for track in items]
                return [f"{track.artists} - {track.name}" for track in tracks]

    tracks = await get()
    return tracks
