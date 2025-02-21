from backend.base.schemas import BaseSettings


class AuthSettings(BaseSettings):
    auth_secret: str = "changethis"
    auth_token_lifetime: int = 3600
