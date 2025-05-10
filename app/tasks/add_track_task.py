from typing import Any

from celery import Task
from celery_app import celery_app

from app.yandex.depends import get_client as get_yandex_client

"""TODO
1. Получить список пользователей
2. Получить список треков для каждого пользователя
3. Получить список лайков для каждого пользователя из Spotify
4. Получить список лайков для каждого пользователя из Яндекс.Музыки
5. Офильтровать треки
6. Лайкнуть треки
"""


@celery_app.task()
async def get_users():
    """Получить список пользователей
    Получить список лайкнутых треков для каждого пользователя в Яндекс и Спотифай

    """
    ...


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)  # type: ignore
async def like_track(self: Task, track_id: int) -> dict[str, Any]:
    client = await get_yandex_client()

    try:
        # Здесь логика обращения к API Яндекс.Музыки
        response = await client.like(track_id)
        return response
    except Exception as exc:
        # Логируем и повторяем попытку через указанное время
        raise self.retry(exc=exc) from exc
