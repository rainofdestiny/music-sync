from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str
    yandex_token: str

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
