from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+pysqlite:///:memory:"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    youtube_api_key: Optional[str] = None
    google_trends_api_key: Optional[str] = None
    serp_api_key: Optional[str] = None
    listen_notes_api_key: Optional[str] = None
    next_public_api_base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
