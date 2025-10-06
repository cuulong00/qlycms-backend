"""User schemas for FastAPI-Users integration."""

from datetime import datetime

from fastapi_users import schemas
from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema, IDSchema, TimestampSchema


class UserRead(schemas.BaseUser[int], TimestampSchema):
    """User read schema - returned in responses.
    
    Inherits from FastAPI-Users BaseUser which includes:
    - id: User ID
    - email: Email address
    - is_active: Active status
    - is_superuser: Superuser status
    - is_verified: Email verification status
    
    Extended with custom fields.
    """
    
    first_name: str | None = Field(None, max_length=50, description="First name")
    last_name: str | None = Field(None, max_length=50, description="Last name")
    role: str = Field(default="user", description="User role")
    phone_number: str | None = Field(None, max_length=20, description="Phone number")
    last_login_at: datetime | None = Field(None, description="Last login timestamp")
    avatar_url: str | None = Field(None, max_length=255, description="Avatar URL")
    bio: str | None = Field(None, max_length=500, description="User bio")
    oauth_provider: str | None = Field(None, description="OAuth provider")


class UserCreate(schemas.BaseUserCreate):
    """User creation schema - for registration.
    
    Inherits from FastAPI-Users BaseUserCreate which includes:
    - email: Email address (required)
    - password: Password (required)
    - is_active: Active status (optional)
    - is_superuser: Superuser status (optional)
    - is_verified: Verification status (optional)
    """
    
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    phone_number: str | None = Field(None, max_length=20)


class UserUpdate(schemas.BaseUserUpdate):
    """User update schema - for profile updates.
    
    All fields are optional to allow partial updates.
    """
    
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    phone_number: str | None = Field(None, max_length=20)
    avatar_url: str | None = Field(None, max_length=255)
    bio: str | None = Field(None, max_length=500)


class UserProfileUpdate(BaseSchema):
    """Schema for user profile update (simplified)."""
    
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    phone_number: str | None = Field(None, max_length=20)
    bio: str | None = Field(None, max_length=500)


class UserRoleUpdate(BaseSchema):
    """Schema for updating user role (admin only)."""
    
    role: str = Field(..., description="New user role")


class ChangePassword(BaseSchema):
    """Schema for changing password."""
    
    current_password: str = Field(..., min_length=8, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")


class PasswordReset(BaseSchema):
    """Schema for password reset request."""
    
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirm(BaseSchema):
    """Schema for password reset confirmation."""
    
    token: str = Field(..., description="Reset token from email")
    new_password: str = Field(..., min_length=8, description="New password")


class UserListResponse(BaseSchema):
    """Schema for user in list responses."""
    
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime


class UserStats(BaseSchema):
    """User statistics schema."""
    
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    verified_users: int = Field(..., description="Number of verified users")
    new_users_today: int = Field(..., description="New users registered today")
    new_users_this_week: int = Field(..., description="New users this week")
    new_users_this_month: int = Field(..., description="New users this month")
