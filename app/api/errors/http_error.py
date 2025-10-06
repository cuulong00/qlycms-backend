"""HTTP error handlers for FastAPI."""

from fastapi import Request, status
from fastapi.responses import JSONResponse


async def http_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle HTTP exceptions.
    
    Args:
        request: FastAPI request object.
        exc: Exception instance.
        
    Returns:
        JSON response with error details.
    """
    return JSONResponse(
        status_code=getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={
            "success": False,
            "error": exc.__class__.__name__,
            "message": str(exc),
            "detail": getattr(exc, "detail", None),
        },
    )


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle validation errors from Pydantic.
    
    Args:
        request: FastAPI request object.
        exc: RequestValidationError exception.
        
    Returns:
        JSON response with validation error details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "ValidationError",
            "message": "Validation error occurred",
            "details": getattr(exc, "errors", lambda: [])(),
        },
    )
