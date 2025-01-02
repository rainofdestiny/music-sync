from fastapi import FastAPI
import logging

from app.spotify.router import router as spotify_router

app = FastAPI()

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app.include_router(spotify_router)
