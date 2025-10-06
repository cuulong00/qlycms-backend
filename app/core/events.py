"""Application lifecycle events (startup, shutdown)."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.db.session import close_db, init_db

logger = get_logger(__name__)


async def on_startup() -> None:
    """Execute tasks on application startup.
    
    - Initialize logging
    - Connect to database
    - Initialize cache
    - Setup other services
    """
    logger.info("Starting application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Setup logging
    setup_logging()
    logger.info("Logging configured")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize cache if Redis is configured
    if settings.REDIS_URL:
        logger.info("Redis cache configured")
    
    logger.info("Application started successfully!")


async def on_shutdown() -> None:
    """Execute tasks on application shutdown.
    
    - Close database connections
    - Close cache connections
    - Cleanup resources
    """
    logger.info("Shutting down application...")
    
    # Close database
    await close_db()
    logger.info("Database connections closed")
    
    logger.info("Application shutdown complete")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for FastAPI application.
    
    This replaces the older on_event decorators and is the recommended
    way to handle startup and shutdown events in FastAPI.
    
    Args:
        app: FastAPI application instance.
        
    Yields:
        None
    """
    # Startup
    await on_startup()
    
    yield
    
    # Shutdown
    await on_shutdown()
