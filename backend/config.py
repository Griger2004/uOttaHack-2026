import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Force load .env
backend_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)


class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = ""
    yellowcake_api_key: str = ""
    serper_api_key: str = ""

    # App Settings
    app_name: str = "Agentic Fake News Detector"
    debug: bool = False

    # External APIs
    serper_endpoint: str = "https://google.serper.dev/search"
    # --- FIX 1: Correct URL (.dev and /extract-stream) ---
    yellowcake_endpoint: str = "https://api.yellowcake.dev/v1/extract-stream"

    # Content Settings
    max_content_per_source: int = 2000
    search_results_limit: int = 3
    request_timeout: int = 30  # Increased for streaming

    gemini_model: str = "gemini-3-flash-preview"

    class Config:
        env_file = env_path
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
