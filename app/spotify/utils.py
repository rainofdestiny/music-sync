from app.utils import BaseHTTPClient


class HTTPClient(BaseHTTPClient):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("base_url", "https://api.spotify.com/v1/me")
        super().__init__(*args, **kwargs)
