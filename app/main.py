from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager
from app.config import settings
from yandex_music.client_async import ClientAsync
from app.spotify.router import router as spotify_router
from app.yandex.router import router as yandex_router


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация ресурса (Yandex Music Client)
    client = await ClientAsync(settings.yandex_token).init()
    app.state.client = client  # Сохраняем клиента в app.state
    try:
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)

app.include_router(spotify_router)
app.include_router(yandex_router)
