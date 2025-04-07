import logging

from fastapi import APIRouter, Query

from app.celery_app import celery_app


router = APIRouter(prefix="/sync")

logger = logging.getLogger(__name__)


@router.post("/")
@celery_app.task(name="sync", expires=600)
def sync(all: bool = Query(default=False, strict=True)):
    pass


"""
    if all:
        offset = 0
        total_added = 0
        
        # while tracks := spotify.get_liked_tracks(limit=50, offset=offset):
            if not tracks:
                break
            yandex.add_tracks(tracks)
            total_added += len(tracks)
            offset += 50
            logger.info(f"Added {len(tracks)} tracks from offset {offset - 50}.")

        logger.info(f"Sync completed. Total added tracks: {total_added}.")
        return {"ok": True, "detail": f"Total tracks added: {total_added}"}
    else:
        logger.info("Starting sync from Spotify to Yandex Music...")

        try:
            tracks = spotify.get_liked_tracks()
            yandex.add_tracks(tracks)
            logger.info(f"Successfully synced {len(tracks)} tracks.")
        except Exception as e:
            logger.error(f"Error during sync: {e}")
            raise HTTPException(status_code=500, detail="Sync failed.")
"""
