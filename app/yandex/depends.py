from fastapi import Request
from yandex_music import ClientAsync


async def get_client(request: Request) -> ClientAsync:
    """
    Зависимость для получения Yandex Music Client из app.state.
    """
    client = getattr(request.app.state, "client", None)
    if not client:
        raise RuntimeError("Yandex Music client is not initialized")
    return client
