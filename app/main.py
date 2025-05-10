from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

# from httpx import HTTPStatusError, RequestError, TimeoutException
# from app.exception_handlers import (
#     http_status_error_handler,
#     request_error_handler,
#     timeout_exception_handler,
# )
from app.logger import Logger
from app.middlewares import LoggerMiddleware

# from app.spotify.exception_handlers import (
#     refresh_token_not_found_exception_handler,
# )
# from app.spotify.exceptions import RefreshTokenNotFoundError
from app.spotify.routes import router as spotify_router
from app.users.routes import router as users_router
from app.yandex.routes import router as yandex_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    try:
        yield
    finally:
        pass


Logger()

app = FastAPI(lifespan=lifespan)

app.include_router(spotify_router)
app.include_router(yandex_router)
app.include_router(users_router)

app.add_middleware(LoggerMiddleware)

# app.add_exception_handler(TimeoutException, timeout_exception_handler)
# app.add_exception_handler(RequestError, request_error_handler)
# app.add_exception_handler(HTTPStatusError, http_status_error_handler)

# app.add_exception_handler(
#     RefreshTokenNotFoundError, refresh_token_not_found_exception_handler
# )


@app.get(
    "/",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    include_in_schema=False,
)
def auth_redirect() -> RedirectResponse:
    return RedirectResponse("/spotify/auth")
