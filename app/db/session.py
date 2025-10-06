"""Database session management with async SQLAlchemy."""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool, QueuePool

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Global engine instance
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine_config() -> dict[str, Any]:
    """Get database engine configuration based on settings.
    
    Returns:
        dict: Engine configuration parameters.
    """
    config: dict[str, Any] = {
        "echo": settings.DATABASE_ECHO,
        "future": True,
    }
    
    # Use different pool settings for SQLite vs PostgreSQL
    if "sqlite" in settings.DATABASE_URL:
        # SQLite doesn't support connection pooling
        config["poolclass"] = NullPool
        config["connect_args"] = {"check_same_thread": False}
    else:
        # PostgreSQL with connection pooling
        config["poolclass"] = QueuePool
        config["pool_size"] = settings.DATABASE_POOL_SIZE
        config["max_overflow"] = settings.DATABASE_MAX_OVERFLOW
        config["pool_recycle"] = settings.DATABASE_POOL_RECYCLE
        config["pool_pre_ping"] = settings.DATABASE_POOL_PRE_PING
    
    return config


async def init_db() -> None:
    """Initialize database engine and session factory.
    
    Should be called on application startup.
    """
    global _engine, _session_factory
    
    if _engine is not None:
        logger.warning("Database engine already initialized")
        return
    
    logger.info(f"Initializing database: {settings.DATABASE_URL.split('@')[-1]}")
    
    # Create async engine
    engine_config = get_engine_config()
    _engine = create_async_engine(settings.DATABASE_URL, **engine_config)
    
    # Create session factory
    _session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    logger.info("Database engine initialized successfully")


async def close_db() -> None:
    """Close database engine and cleanup resources.
    
    Should be called on application shutdown.
    """
    global _engine, _session_factory
    
    if _engine is None:
        return
    
    logger.info("Closing database connections...")
    
    await _engine.dispose()
    _engine = None
    _session_factory = None
    
    logger.info("Database connections closed")


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get the session factory.
    
    Returns:
        async_sessionmaker: Session factory for creating database sessions.
        
    Raises:
        RuntimeError: If database is not initialized.
    """
    if _session_factory is None:
        raise RuntimeError(
            "Database not initialized. Call init_db() first."
        )
    return _session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection.
    
    This is the main function used with FastAPI's Depends() to inject
    database sessions into route handlers.
    
    Example:
        ```python
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass
        ```
    
    Yields:
        AsyncSession: Database session that will be automatically closed.
    """
    session_factory = get_session_factory()
    
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_context() -> AsyncSession:
    """Get database session for use outside of FastAPI dependency injection.
    
    Use this when you need a database session in background tasks,
    scripts, or other contexts where dependency injection isn't available.
    
    Example:
        ```python
        async with get_db_context() as session:
            # Use session here
            result = await session.execute(query)
        ```
    
    Returns:
        AsyncSession: Database session context manager.
    """
    session_factory = get_session_factory()
    return session_factory()


# Export for convenience
__all__ = [
    "init_db",
    "close_db",
    "get_db",
    "get_db_context",
    "get_session_factory",
]
