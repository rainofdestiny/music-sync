from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.spotify.exceptions import RefreshTokenNotFoundError


async def refresh_token_not_found_exception_handler(
    request: Request, exc: RefreshTokenNotFoundError
) -> JSONResponse:
    logger.error(
        f"Refresh token not found in {request.method} {request.url.path}"
    )
    return JSONResponse(
        content="Refresh token not found. Please visit /spotify/auth/",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
