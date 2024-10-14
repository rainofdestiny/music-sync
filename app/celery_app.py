from celery import Celery

celery_app = Celery(
    "music_sync",
    broker=f"redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.main"],
)  #


celery_app.conf.beat_schedule = {
    "sync-playlists-every-10-minutes": {
        "task": "sync",
        "schedule": 600.0,  # ever 10 minutes
    },
}
celery_app.conf.timezone = "UTC"
celery_app.conf.update(
    task_time_limit=300,
    task_soft_time_limit=240,
)
