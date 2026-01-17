"""
Application configuration and settings.
Loads API keys from environment variables.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    gemini_api_key: str = ""
    yellowcake_api_key: str = ""
    serper_api_key: str = ""

    # Application Settings
    app_name: str = "Agentic Fake News Detector"
    debug: bool = False

    # External API Endpoints
    serper_endpoint: str = "https://google.serper.dev/search"
    yellowcake_endpoint: str = "https://api.yellowcake.ai/v1/extract"

    # Content Settings
    max_content_per_source: int = 2000
    search_results_limit: int = 3
    request_timeout: int = 15

    # Gemini Settings
    gemini_model: str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reading env vars on every call.
    """
    return Settings()


# Convenience accessor
settings = get_settings()
