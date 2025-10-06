"""Health check endpoints."""

from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.common import HealthCheck

router = APIRouter()


@router.get(
    "/",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is running and healthy",
)
async def health_check() -> HealthCheck:
    """Health check endpoint.
    
    Returns basic information about the service status.
    
    Returns:
        HealthCheck: Service health information.
    """
    return HealthCheck(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database="connected",  # TODO: Add actual database health check
        cache="connected" if settings.REDIS_URL else None,
    )


@router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
    summary="Ping",
    description="Simple ping endpoint",
)
async def ping() -> dict[str, str]:
    """Simple ping endpoint.
    
    Returns:
        dict: Pong response.
    """
    return {"message": "pong"}
