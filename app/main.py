from fastapi import FastAPI, HTTPException
import logging

from app import spotify, yandex
from app.celery_app import celery_app

from fastapi.responses import RedirectResponse

app = FastAPI()

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


@app.get("/auth", response_class=RedirectResponse)
def auth():
    logger.info("Redirecting to Spotify auth URL.")
    return spotify.auth_url()


@app.get("/callback")
def callback(code: str):
    try:
        spotify.gen_token(code)
        logger.info("Token generated successfully.")
        return {"ok": True, "detail": "You can close this page"}
    except Exception as e:
        logger.error(f"Error generating token: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed.")


@app.get("/sync")
@celery_app.task(name="sync", expires=600)
def sync():
    logger.info("Starting sync from Spotify to Yandex Music...")

    try:
        tracks = spotify.get_liked_tracks()
        yandex.add_tracks(tracks)
        logger.info(f"Successfully synced {len(tracks)} tracks.")
    except Exception as e:
        logger.error(f"Error during sync: {e}")
        raise HTTPException(status_code=500, detail="Sync failed.")


@app.get("/sync-all")
def sync_all():
    offset = 0
    total_added = 0

    while tracks := spotify.get_liked_tracks(limit=50, offset=offset):
        if not tracks:
            break
        yandex.add_tracks(tracks)
        total_added += len(tracks)
        offset += 50
        logger.info(f"Added {len(tracks)} tracks from offset {offset - 50}.")

    logger.info(f"Sync completed. Total added tracks: {total_added}.")
    return {"ok": True, "detail": f"Total tracks added: {total_added}"}
