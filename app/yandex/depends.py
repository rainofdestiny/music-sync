from typing import Annotated

from fastapi import Depends

from app.yandex.client import Client


async def get_client() -> Client:
    return await Client.init()


ClientDep = Annotated[Client, Depends(get_client)]
