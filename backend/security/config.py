from backend.base.schemas import BaseSettings


class SecuritySettings(BaseSettings):
    encryption_secret: str = "changethis"
