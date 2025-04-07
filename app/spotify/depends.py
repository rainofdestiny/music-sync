from fastapi import Depends
import redis.asyncio as redis
from app.depends import get_redis
from app.spotify.oauth import oauth


async def get_access_token_dependency(
    r: redis.Redis = Depends(get_redis),
) -> str:
    return await oauth.get_access_token(r)
