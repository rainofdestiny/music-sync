from redis.asyncio import Redis

from app.spotify.schemas import AuthSchema, RefreshTokenAuthSchema


async def cache_tokens(r: Redis, auth: AuthSchema) -> None:
    await r.set("spotify:access_token", auth.access_token, ex=auth.expires_in)
    await r.set("spotify:refresh_token", auth.refresh_token)


async def get_refresh_token(r: Redis) -> str | None:
    if token := await r.get("spotify:refresh_token"):
        return token
    return None


async def get_access_token(r: Redis) -> str | None:
    if token := await r.get("spotify:access_token"):
        return token
    return None


async def set_access_token(r: Redis, data: RefreshTokenAuthSchema) -> None:
    await r.set("spotify:access_token", data.access_token, ex=data.expires_in)
