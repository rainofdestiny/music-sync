import redis

from app.spotify.models import AuthModel


async def cache_tokens(r: redis.Redis, data: AuthModel) -> None:
    await r.set("spotify:access_token", data.access_token, ex=data.expires_in)
    await r.set("spotify:refresh_token", data.refresh_token)
