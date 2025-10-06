"""Core configuration module."""

from functools import lru_cache
from typing import Any, Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support.
    
    All settings can be overridden via environment variables.
    Example: APP_NAME="My App" in .env file or environment.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    APP_NAME: str = Field(default="Chatbot Manager API", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    APP_DESCRIPTION: str = Field(
        default="Production-ready FastAPI backend with Clean Architecture",
        description="Application description",
    )
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Environment",
    )
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")
    WORKERS: int = Field(default=4, description="Number of worker processes")
    
    # Security
    SECRET_KEY: str = Field(
        default="change-me-in-production-must-be-at-least-32-characters-long",
        min_length=32,
        description="Secret key for JWT encoding",
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration in minutes",
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration in days",
    )
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./test.db",
        description="Database connection URL",
    )
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries")
    DATABASE_POOL_SIZE: int = Field(default=5, description="Database pool size")
    DATABASE_MAX_OVERFLOW: int = Field(
        default=10,
        description="Database max overflow",
    )
    DATABASE_POOL_RECYCLE: int = Field(
        default=3600,
        description="Database pool recycle time in seconds",
    )
    DATABASE_POOL_PRE_PING: bool = Field(
        default=True,
        description="Test connections before using",
    )
    
    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="Allow credentials in CORS",
    )
    CORS_ALLOW_METHODS: list[str] = Field(
        default=["*"],
        description="Allowed HTTP methods",
    )
    CORS_ALLOW_HEADERS: list[str] = Field(
        default=["*"],
        description="Allowed HTTP headers",
    )
    
    # Redis (Optional)
    REDIS_URL: str | None = Field(
        default=None,
        description="Redis connection URL",
    )
    REDIS_CACHE_TTL: int = Field(default=3600, description="Redis cache TTL")
    
    # Email (Optional)
    SMTP_HOST: str | None = Field(default=None, description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USER: str | None = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: str | None = Field(default=None, description="SMTP password")
    SMTP_FROM: str | None = Field(default=None, description="SMTP from address")
    SMTP_TLS: bool = Field(default=True, description="Use TLS for SMTP")
    
    # OAuth2 Providers (Optional)
    GOOGLE_CLIENT_ID: str | None = Field(default=None, description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: str | None = Field(
        default=None,
        description="Google OAuth client secret",
    )
    GITHUB_CLIENT_ID: str | None = Field(default=None, description="GitHub OAuth client ID")
    GITHUB_CLIENT_SECRET: str | None = Field(
        default=None,
        description="GitHub OAuth client secret",
    )
    
    # Celery (Optional)
    CELERY_BROKER_URL: str | None = Field(
        default=None,
        description="Celery broker URL",
    )
    CELERY_RESULT_BACKEND: str | None = Field(
        default=None,
        description="Celery result backend",
    )
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Requests per minute per IP",
    )
    
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    LOG_FORMAT: Literal["json", "text"] = Field(
        default="json",
        description="Log format",
    )
    
    # Sentry (Optional)
    SENTRY_DSN: str | None = Field(default=None, description="Sentry DSN")
    SENTRY_ENVIRONMENT: str | None = Field(
        default=None,
        description="Sentry environment",
    )
    SENTRY_TRACES_SAMPLE_RATE: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Sentry traces sample rate",
    )
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v:
            raise ValueError("DATABASE_URL cannot be empty")
        return v
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info: Any) -> str:
        """Validate secret key in production."""
        environment = info.data.get("ENVIRONMENT", "development")
        if environment == "production" and "change-me" in v.lower():
            raise ValueError(
                "SECRET_KEY must be changed in production environment"
            )
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"
    
    @property
    def database_url_async(self) -> str:
        """Get async database URL."""
        return self.DATABASE_URL
    
    @property
    def database_url_sync(self) -> str:
        """Get sync database URL for Alembic migrations."""
        # Convert async driver to sync for Alembic
        url = self.DATABASE_URL
        if "asyncpg" in url:
            url = url.replace("postgresql+asyncpg", "postgresql+psycopg2")
        elif "aiosqlite" in url:
            url = url.replace("sqlite+aiosqlite", "sqlite")
        return url


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.
    
    Using lru_cache ensures we only create one Settings instance
    and reuse it for better performance.
    
    Returns:
        Settings: Application settings instance.
    """
    return Settings()


# Global settings instance
settings = get_settings()
