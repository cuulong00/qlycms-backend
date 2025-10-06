"""Base schemas for common patterns."""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# Type variable for generic response
T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration.
    
    All schemas should inherit from this to get consistent configuration.
    """
    
    model_config = ConfigDict(
        from_attributes=True,  # Support ORM models
        populate_by_name=True,  # Allow population by field name
        use_enum_values=True,  # Use enum values instead of enum instances
        validate_assignment=True,  # Validate on assignment
        str_strip_whitespace=True,  # Strip whitespace from strings
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""
    
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ResponseSchema(BaseSchema, Generic[T]):
    """Generic response wrapper.
    
    Use this to wrap API responses with consistent structure.
    
    Example:
        ```python
        ResponseSchema[UserResponse](
            success=True,
            message="User created successfully",
            data=user
        )
        ```
    """
    
    success: bool = Field(default=True, description="Operation success status")
    message: str | None = Field(default=None, description="Response message")
    data: T | None = Field(default=None, description="Response data")


class ErrorResponse(BaseSchema):
    """Error response schema.
    
    Used for consistent error responses across the API.
    """
    
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error type/code")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(
        default=None,
        description="Additional error details",
    )


class PaginationParams(BaseSchema):
    """Pagination parameters for list endpoints."""
    
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of items per page",
    )
    
    @property
    def skip(self) -> int:
        """Calculate skip value for database query.
        
        Returns:
            int: Number of records to skip.
        """
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get limit value for database query.
        
        Returns:
            int: Maximum number of records to return.
        """
        return self.page_size


class PaginatedResponse(BaseSchema, Generic[T]):
    """Paginated response schema.
    
    Use this for endpoints that return paginated lists.
    
    Example:
        ```python
        PaginatedResponse[UserResponse](
            items=users,
            total=100,
            page=1,
            page_size=20
        )
        ```
    """
    
    items: list[T] = Field(default_factory=list, description="List of items")
    total: int = Field(..., ge=0, description="Total number of items")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Items per page")
    
    @property
    def total_pages(self) -> int:
        """Calculate total number of pages.
        
        Returns:
            int: Total pages.
        """
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size
    
    @property
    def has_next(self) -> bool:
        """Check if there are more pages.
        
        Returns:
            bool: True if there are more pages.
        """
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        """Check if there are previous pages.
        
        Returns:
            bool: True if there are previous pages.
        """
        return self.page > 1


class IDSchema(BaseSchema):
    """Schema with ID field."""
    
    id: int = Field(..., description="Unique identifier")


class StatusSchema(BaseSchema):
    """Schema with status field."""
    
    is_active: bool = Field(default=True, description="Active status")
