from celery import Celery

from app.config import settings

celery_app = Celery(
    "app",
    broker=settings.celery_broker_url,
    backend="rpc://",  # Используем RPC для получения результатов
)

celery_app.conf.beat_schedule = {  # type: ignore
    "sync-playlists-every-10-minutes": {
        "task": "sync",
        "schedule": 600.0,  # ever 10 minutes
    }
}

celery_app.conf.update(  # type: ignore
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_time_limit=300,
    task_soft_time_limit=240,
)
