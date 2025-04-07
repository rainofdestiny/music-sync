import httpx


class BaseHTTPClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("timeout", 10.0)
        kwargs.setdefault("http2", True)
        kwargs.setdefault("base_url", "http://localhost:8000")
        super().__init__(*args, **kwargs)
