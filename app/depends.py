import redis.asyncio as redis
from fastapi import Depends


async def get_redis_pool():
    pool = redis.ConnectionPool(
        host="localhost", port=6379, db=0, decode_responses=True, max_connections=10
    )
    return pool


async def get_redis(pool=Depends(get_redis_pool)):
    return redis.Redis(connection_pool=pool)
