from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str
    spotify_scope: str = (
        "user-read-currently-playing "
        "user-library-read "
        "user-read-private "
        "user-read-email"
    )

    yandex_token: str

    database_url: str

    # postgres_user: str
    # postgres_password: str
    # postgres_db: str

    rabbitmq_default_user: str
    rabbitmq_default_pass: str

    # @property
    # def database_url(self) -> str:
    #     return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@postgres:5432/{self.postgres_db}"

    @property
    def celery_broker_url(self) -> str:
        return f"amqp://{self.rabbitmq_default_user}:{self.rabbitmq_default_pass}@rabbitmq:5672"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()  # type: ignore
