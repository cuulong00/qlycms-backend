"""User model with FastAPI-Users integration."""

from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.item import Item


class User(SQLAlchemyBaseUserTable[int], Base, TimestampMixin):
    """User model with authentication support.
    
    Inherits from SQLAlchemyBaseUserTable which provides:
    - id: Integer primary key
    - email: Email address (unique, indexed)
    - hashed_password: Password hash
    - is_active: Account active status
    - is_superuser: Superuser status
    - is_verified: Email verification status
    
    Extends with additional fields:
    - first_name: User's first name
    - last_name: User's last name
    - role: User role for RBAC
    """
    
    __tablename__ = "users"
    
    # Additional user fields
    first_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="User's first name",
    )
    
    last_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="User's last name",
    )
    
    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
        nullable=False,
        index=True,
        comment="User role (user, admin, super_admin)",
    )
    
    # Phone number (optional)
    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="User's phone number",
    )
    
    # Last login tracking
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Last login timestamp",
    )
    
    # Profile information
    avatar_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        comment="Avatar image URL",
    )
    
    bio: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="User bio/description",
    )
    
    # OAuth provider information
    oauth_provider: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="OAuth provider (google, github, etc.)",
    )
    
    oauth_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="OAuth provider user ID",
    )
    
    # Relationships
    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    
    @property
    def full_name(self) -> str:
        """Get user's full name.
        
        Returns:
            str: Full name or email if name not set.
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email
    
    def __repr__(self) -> str:
        """String representation."""
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
