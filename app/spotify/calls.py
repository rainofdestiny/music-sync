import httpx

from app.spotify.models import TrackModel, AuthModel, AuthorizeRequestModel
from app.spotify.oauth import oauth
from app.spotify.depends import r


def auth_url() -> str:
    return AuthorizeRequestModel().url


def gen_token(code: str) -> None:
    with httpx.Client() as client:
        response = client.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {oauth.auth_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": oauth.redirect_uri,
            },
        )
        response.raise_for_status()
        auth_data = AuthModel(**response.json())

    r.set("spotify:access_token", auth_data.access_token, ex=auth_data.expires_in)
    r.set("spotify:refresh_token", auth_data.refresh_token)


@oauth
def get_liked_tracks(access_token: str, *, limit=50, offset=0) -> list[TrackModel]:
    with httpx.Client() as client:
        response = client.get(
            f"https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        items = response.json().get("items", [])
        return [TrackModel(**track["track"]) for track in items]
