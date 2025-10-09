"""Common schemas used across the application."""

from typing import Any, Generic, TypeVar

from pydantic import Field

from app.schemas.base import BaseSchema

# Type variable for generic paginated response
T = TypeVar("T")


class HealthCheck(BaseSchema):
    """Health check response schema."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment name")
    database: str = Field(..., description="Database status")
    cache: str | None = Field(None, description="Cache status")


class Message(BaseSchema):
    """Simple message response schema."""
    
    message: str = Field(..., description="Message content")


class Token(BaseSchema):
    """JWT token response schema."""
    
    access_token: str = Field(..., description="Access token")
    refresh_token: str | None = Field(None, description="Refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int | None = Field(None, description="Token expiration in seconds")


class TokenPayload(BaseSchema):
    """JWT token payload schema."""
    
    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    type: str = Field(..., description="Token type (access/refresh)")


class ErrorDetail(BaseSchema):
    """Detailed error information."""
    
    loc: list[str | int] = Field(..., description="Error location")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ValidationError(BaseSchema):
    """Validation error response."""
    
    detail: list[ErrorDetail] = Field(..., description="Validation errors")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response schema.
    
    Provides pagination metadata along with items.
    Type parameter T represents the type of items in the list.
    
    Attributes:
        items: List of items for current page
        total: Total number of items across all pages
        skip: Number of items skipped
        limit: Maximum number of items per page
        has_more: Whether there are more items after current page
    """
    
    items: list[T] = Field(..., description="List of items for current page")
    total: int = Field(..., ge=0, description="Total number of items")
    skip: int = Field(..., ge=0, description="Number of items skipped")
    limit: int = Field(..., ge=1, description="Maximum items per page")
    
    @property
    def has_more(self) -> bool:
        """Check if there are more items after current page.
        
        Returns:
            bool: True if there are more items, False otherwise
        """
        return self.skip + self.limit < self.total
