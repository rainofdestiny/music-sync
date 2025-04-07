import redis.asyncio as redis
from fastapi import Request
from loguru import logger


async def get_redis():
    pool = redis.ConnectionPool(
        host="redis", port=6379, db=0, decode_responses=True, max_connections=10
    )
    return redis.Redis(connection_pool=pool)


async def log_request_dependency(request: Request):
    logger.info(f"Incoming request: {request.method} {request.url}")
    return request
