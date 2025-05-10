from typing import Annotated

from fastapi import Depends
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.schemas import PaginationSchema


async def get_redis() -> Redis:
    pool = ConnectionPool(
        host="redis", port=6379, db=0, decode_responses=True, max_connections=10
    )
    return Redis(connection_pool=pool)


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
RedisDep = Annotated[Redis, Depends(get_redis)]
PaginationDep = Annotated[PaginationSchema, Depends(PaginationSchema)]
