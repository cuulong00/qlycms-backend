"""Item schemas - example domain schemas."""

from datetime import datetime

from pydantic import Field

from app.schemas.base import BaseSchema, IDSchema, StatusSchema, TimestampSchema


class ItemBase(BaseSchema):
    """Base item schema with common fields."""
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Item title",
    )
    description: str | None = Field(
        None,
        max_length=2000,
        description="Item description",
    )
    is_active: bool = Field(
        default=True,
        description="Item active status",
    )


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    
    pass


class ItemUpdate(BaseSchema):
    """Schema for updating an existing item.
    
    All fields are optional to allow partial updates.
    """
    
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=2000)
    is_active: bool | None = None


class ItemResponse(ItemBase, IDSchema, TimestampSchema):
    """Schema for item response."""
    
    owner_id: int = Field(..., description="Owner user ID")


class ItemWithOwner(ItemResponse):
    """Schema for item with owner information."""
    
    owner_email: str = Field(..., description="Owner email address")
    owner_name: str | None = Field(None, description="Owner full name")


class ItemListResponse(BaseSchema):
    """Schema for item in list responses."""
    
    id: int
    title: str
    is_active: bool
    owner_id: int
    created_at: datetime


class ItemStats(BaseSchema):
    """Item statistics schema."""
    
    total_items: int = Field(..., description="Total number of items")
    active_items: int = Field(..., description="Number of active items")
    items_created_today: int = Field(..., description="Items created today")
    items_by_user: dict[int, int] = Field(
        default_factory=dict,
        description="Items count by user ID",
    )
