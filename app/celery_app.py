from celery import Celery

celery_app = Celery(
    "app",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.main"],
)
#
# celery_app = Celery(
#     "app",
#     broker="amqp://guest:guest@localhost:5672//",  # URL RabbitMQ
#     backend="rpc://",  # Используем RPC для получения результатов
# )

celery_app.conf.beat_schedule = {
    "sync-playlists-every-10-minutes": {
        "task": "sync",
        "schedule": 600.0,  # ever 10 minutes
    },
}

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_time_limit=300,
    task_soft_time_limit=240,
)
