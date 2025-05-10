class RefreshTokenNotFoundError(Exception):
    def __init__(self, message: str = "Refresh token not found.") -> None:
        super().__init__(message)
