from fastapi import APIRouter
from loguru import logger

from app.spotify.depends import ClientDep as SpotifyClientDep
from app.yandex.depends import ClientDep as YandexClientDep

router = APIRouter(prefix="/sync")


@router.post("/")
async def sync(spotify: SpotifyClientDep, yandex: YandexClientDep):  # noqa

    # todo это все надо делать в tasks
    logger.info("Syncing liked tracks")
    # ask что делать с треками,
    #  которых нет в yandex music,
    #  либо находит другой по схожему названию?

    # todo проходиться по все трекам если all=true
    # todo добавить last_liked_track_by_stofy_id,
    #  если он есть в списке и стоит all=false,
    #  то словарь обрезается и остаются только новые треки

    # spotify_tracks = await spotify.get_liked_tracks()

    # todo убрать все треки с id которые сохранены в базе данных
    # todo каждый трек ищем в яндекс музыке
    #  и сохраняем только id в словаре dict[spotify, yandex]

    # yandex_liked_tracks_id: set[int] = set(
    #     await yandex.get_id_of_liked_tracks()
    # )

    # tracks: list[int] = (
    #     list(  # Исключаем треки, которые уже сохранены в yanex music
    #         filter(lambda i: i not in yandex_liked_tracks_id, spotify_tracks)
    #     )
    # )

    # todo Отправить трек на лайк в yandex music через rabbitmq


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
