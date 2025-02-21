from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    backend_url: str = "http://127.0.0.1:8000/api/v1"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
