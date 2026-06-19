"""Centralized, typed configuration loaded from the environment / .env file."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Populate os.environ from .env so Google ADK / google-genai picks up GEMINI_API_KEY.
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Gemini (used by every agent via ADK). The Hacker News source needs no keys.
    gemini_api_key: str = ""


settings = Settings()
