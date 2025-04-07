from fastapi import Depends, FastAPI, status
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager

from app.config import settings
from yandex_music.client_async import ClientAsync
from app.spotify.routes import router as spotify_router
from app.yandex.router import router as yandex_router
from app.depends import log_request_dependency

from app.logger import Logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await ClientAsync(settings.yandex_token).init()
    app.state.client = client

    try:
        yield
    finally:
        pass


Logger()

app = FastAPI(dependencies=[Depends(log_request_dependency)], lifespan=lifespan)

app.include_router(spotify_router)
app.include_router(yandex_router)


@app.get(
    "/",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    include_in_schema=False,
)
def auth_redirect():
    return RedirectResponse("/spotify/auth")
