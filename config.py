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

    # Gemini (used by every agent via ADK, and for the MVP builder)
    gemini_api_key: str = ""

    # Reddit API
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "product-ideas-agent/1.0"


settings = Settings()
