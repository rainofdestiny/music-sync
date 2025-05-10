from fastapi import APIRouter, Query, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from loguru import logger

from app.depends import PaginationDep, RedisDep
from app.spotify.depends import ClientDep
from app.spotify.oauth import OAuth
from app.spotify.schemas import TrackSchema, UserProfileSchema
from app.spotify.service import cache_tokens

__all__ = ["router"]

router = APIRouter(prefix="/spotify", tags=["Spotify"])


@router.get(
    "/auth",
    response_class=RedirectResponse,
    description="Redirecting to Spotify auth URL.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    include_in_schema=False,
)
def auth() -> RedirectResponse:
    return RedirectResponse(OAuth().authorize_url)


@router.get(
    "/callback",
    response_class=RedirectResponse,
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    include_in_schema=False,
)
async def callback(
    r: RedisDep,
    code: str = Query(
        ..., description="Authorization code returned by Spotify"
    ),
) -> RedirectResponse:
    try:
        auth_data = await OAuth().gen_tokens(code)
        await cache_tokens(r=r, auth=auth_data)
        logger.info("Token generated successfully.")
        return RedirectResponse("/spotify/me")
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(
            status_code=500, detail="Token generation failed."
        ) from e


@router.get("/me")
async def get_me(client: ClientDep) -> UserProfileSchema:
    return await client.get_me()


@router.get(
    "/tracks",
    response_class=JSONResponse,
    response_model=list[TrackSchema],
    status_code=status.HTTP_200_OK,
)
async def get_liked_tracks(
    client: ClientDep, pagination: PaginationDep
) -> list[TrackSchema]:
    return await client.get_liked_tracks(
        limit=pagination.limit, offset=pagination.offset
    )
