from spotify.models import TrackModel


def exclude_repeated_tracks(tracks: list[TrackModel]) -> list[TrackModel]:
    ...