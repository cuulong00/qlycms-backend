"""Logging configuration for the application."""

import logging
import sys
from typing import Any

from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and redirect to loguru."""
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to loguru.
        
        Args:
            record: Log record to emit.
        """
        # Get corresponding loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        # Find caller from where the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_logging() -> None:
    """Configure application logging with loguru.
    
    This function:
    - Removes default loguru handlers
    - Configures format based on settings (JSON or text)
    - Sets log level from settings
    - Intercepts standard logging to redirect to loguru
    """
    # Remove default handler
    logger.remove()
    
    # Configure format based on settings
    if settings.LOG_FORMAT == "json":
        log_format = (
            "{"
            '"time": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
            '"level": "{level}", '
            '"logger": "{name}", '
            '"module": "{module}", '
            '"function": "{function}", '
            '"line": {line}, '
            '"message": "{message}"'
            "}"
        )
    else:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Add handler with configured format
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=settings.LOG_FORMAT == "text",
        backtrace=True,
        diagnose=True,
    )
    
    # Add file handler in production
    if settings.is_production:
        logger.add(
            "logs/app_{time:YYYY-MM-DD}.log",
            rotation="00:00",  # Rotate at midnight
            retention="30 days",  # Keep logs for 30 days
            compression="zip",  # Compress old logs
            format=log_format,
            level=settings.LOG_LEVEL,
            backtrace=True,
            diagnose=True,
        )
    
    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Set levels for specific loggers
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("fastapi").handlers = [InterceptHandler()]
    logging.getLogger("sqlalchemy.engine").handlers = [InterceptHandler()]


def get_logger(name: str) -> Any:
    """Get a logger instance.
    
    Args:
        name: Logger name (usually __name__).
        
    Returns:
        Logger instance.
    """
    return logger.bind(logger=name)
