"""
Application settings loaded from environment variables.
See .env.example for all configuration options.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

# Find .env in monorepo root (build/.env)
_env_file = Path(__file__).resolve().parents[4] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_env_file) if _env_file.exists() else ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────
    APP_NAME: str = "Process Catalogue"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "local", "test", "staging", "production"] = "development"
    DEBUG: bool = True

    # ── Database ─────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/process_catalogue"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    # ── Authentication (Passwordless Magic Links) ────
    SECRET_KEY: str = "change-me-in-production"
    MAGIC_LINK_SECRET: str = "change-me-to-a-different-random-string"
    ENCRYPTION_KEY: str = ""  # 32-byte Fernet key for encrypting sensitive data (API keys)
    MAGIC_LINK_EXPIRY_MINUTES: int = 15
    SESSION_EXPIRY_HOURS: int = 24
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MAGIC_LINK_RATE_LIMIT: int = 5  # per hour per email

    # ── Email ────────────────────────────────────────
    EMAIL_PROVIDER: Literal["resend", "sendgrid", "alibaba_dm", "console"] = "console"
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "noreply@processcatalogue.app"

    # ── CORS ─────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # ── Frontend ─────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:3000"

    # ── LLM ──────────────────────────────────────────
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "anthropic"
    DEFAULT_LLM_MODEL: str = "claude-sonnet-4-20250514"

    # ── Provider Abstractions (Global vs China) ──────
    STORAGE_PROVIDER: Literal["local", "r2", "oss"] = "local"
    CACHE_PROVIDER: Literal["memory", "redis"] = "memory"
    LLM_PROVIDER: Literal["mock", "anthropic", "openai", "qwen"] = "mock"

    # ── Object Storage (Cloudflare R2 - Global) ─────
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "process-catalogue"
    R2_ENDPOINT_URL: str = ""
    R2_PUBLIC_URL: str = ""

    # ── Object Storage (Alibaba OSS - China) ────────
    OSS_ACCESS_KEY_ID: str = ""
    OSS_SECRET_ACCESS_KEY: str = ""
    OSS_ENDPOINT: str = ""
    OSS_BUCKET_NAME: str = ""

    # ── Local Storage (Development) ─────────────────
    LOCAL_STORAGE_PATH: str = ""

    # ── Redis / Cache ────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379"

    # ── China LLM Providers ─────────────────────────
    DASHSCOPE_API_KEY: str = ""  # Alibaba Qwen

    # ── Monitoring ───────────────────────────────────
    SENTRY_DSN: str = ""

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
