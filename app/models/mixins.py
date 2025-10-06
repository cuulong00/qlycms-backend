"""Model mixins for common functionality."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """Mixin that adds a UUID primary key instead of integer.
    
    Use this when you need globally unique identifiers.
    """
    
    import uuid
    from sqlalchemy.dialects.postgresql import UUID
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key (UUID)",
    )


class SlugMixin:
    """Mixin that adds a URL-friendly slug field.
    
    Useful for models that need SEO-friendly URLs.
    """
    
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="URL-friendly slug",
    )


class OrderMixin:
    """Mixin that adds ordering capability.
    
    Useful for sortable lists.
    """
    
    order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True,
        comment="Display order",
    )


class StatusMixin:
    """Mixin that adds status field with active/inactive flag.
    
    Common pattern for enabling/disabling records.
    """
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Active status",
    )


class PublishMixin(TimestampMixin):
    """Mixin for publishable content.
    
    Adds fields for draft/published workflow.
    """
    
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Published status",
    )
    
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Publication timestamp",
    )
    
    def publish(self) -> None:
        """Publish the content."""
        self.is_published = True
        self.published_at = datetime.now(timezone.utc)
    
    def unpublish(self) -> None:
        """Unpublish the content."""
        self.is_published = False
        self.published_at = None


class VersionMixin:
    """Mixin that adds version tracking.
    
    Useful for optimistic locking and versioning.
    """
    
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Record version",
    )


class MetadataMixin:
    """Mixin that adds a JSON metadata field.
    
    Useful for storing flexible, schema-less data.
    """
    
    from sqlalchemy import JSON
    
    metadata_: Mapped[dict[str, Any] | None] = mapped_column(
        "metadata",  # Column name in database
        JSON,
        nullable=True,
        comment="JSON metadata",
    )


# Import TimestampMixin for PublishMixin
from app.models.base import TimestampMixin  # noqa: E402
