from collections.abc import Sequence
from typing import Literal

from backend.auth.config import AuthSettings
from backend.base.schemas import BaseSettings
from backend.security.config import SecuritySettings


class CORSSettings(BaseSettings):
    cors_headers: Sequence[str] = ("*",)
    cors_methods: Sequence[str] = ("*",)
    cors_origins: Sequence[str] = ("*",)
    cors_origin_regex: str | None = None


class Settings(BaseSettings):
    app_name: str = "fastapiapp"
    app_display_name: str = "FastAPI App"
    app_version: str = "0.1.0"
    app_env: Literal["dev", "prod"] = "dev"
    app_debug: bool = False
    app_root_path: str = "/api/v1"

    app: AuthSettings = AuthSettings()
    security: SecuritySettings = SecuritySettings()
    cors: CORSSettings = CORSSettings()


settings = Settings()
