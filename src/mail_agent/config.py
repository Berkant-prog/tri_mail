"""Application settings loaded from environment variables and an optional .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the API, model provider, Gmail, and tracing."""

    postgres_dsn: str = "postgresql://postgres:postgres@localhost:5432/mail_agent"
    google_client_secret_file: str = "credentials.json"
    google_token_file: str = "token.json"
    openai_api_key: str | None = None
    langsmith_api_key: str | None = None
    langsmith_tracing: bool = False
    langsmith_project: str = "mail-agent"
    langsmith_endpoint: str = "https://eu.api.smith.langchain.com"
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""

    return Settings()