from typing import Annotated

from fastapi import Depends
from loguru import logger

from app.depends import RedisDep
from app.spotify import service
from app.spotify.client import Client
from app.spotify.exceptions import RefreshTokenNotFoundError
from app.spotify.oauth import OAuth


async def get_access_token(r: RedisDep) -> str:
    if not (token := await service.get_access_token(r)):
        if not (refresh_token := await service.get_refresh_token(r)):
            logger.error("Refresh token not found.")
            raise RefreshTokenNotFoundError()

        data = await OAuth().refresh_token(refresh_token=refresh_token)
        await service.set_access_token(r, data)
        token = data.access_token

    return token


AccessTokenDep = Annotated[str, Depends(get_access_token)]


async def get_client(access_token: AccessTokenDep) -> Client:
    return Client(access_token=access_token)


ClientDep = Annotated[Client, Depends(get_client)]
