import logging

from yandex_music import Client

from app.config import settings

client = Client(settings.yandex_token).init()
logger = logging.getLogger(__name__)


def search(query):
    search_result = client.search(query)

    if search_result.best:
        if search_result.best.type in ["track"]:
            track_id = search_result.best.result.track_id
            return track_id
        return None


def add_tracks(tracks: list):
    queries = [f"{track.artists} - {track.name}" for track in tracks]
    track_ids = list(filter(None, [search(query) for query in queries]))
    try:
        client.users_likes_tracks_add(track_ids)
    except Exception as e:
        logger.error(f"Error when adding tracks: {e}")
