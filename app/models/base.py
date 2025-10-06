"""Base model classes and mixins for SQLAlchemy models.

This module provides base classes that all database models should inherit from:
- Base: Declarative base for all models
- IDMixin: Adds integer primary key
- TimestampMixin: Adds created_at and updated_at fields
- SoftDeleteMixin: Adds soft delete functionality
"""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.
    
    All models should inherit from this class.
    Provides common functionality and type hints support.
    """
    
    # Generate __tablename__ automatically from class name
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate table name from class name.
        
        Converts CamelCase to snake_case and pluralizes.
        Example: UserProfile -> user_profiles
        """
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        # Simple pluralization (add 's')
        if not name.endswith('s'):
            name += 's'
        return name
    
    def dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary.
        
        Returns:
            dict: Dictionary representation of model.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self) -> str:
        """String representation of model."""
        attrs = ", ".join(
            f"{col.name}={getattr(self, col.name)!r}"
            for col in self.__table__.columns
        )
        return f"{self.__class__.__name__}({attrs})"


class IDMixin:
    """Mixin that adds an integer primary key 'id' to models."""
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="Primary key",
    )


class TimestampMixin:
    """Mixin that adds timestamp fields to models.
    
    Adds:
    - created_at: Timestamp when record was created
    - updated_at: Timestamp when record was last updated
    """
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="Timestamp when record was created",
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when record was last updated",
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete functionality to models.
    
    Adds:
    - deleted_at: Timestamp when record was soft deleted
    - is_deleted: Boolean flag indicating if record is deleted
    
    Soft deleted records are not physically removed from database,
    but marked as deleted and filtered out in queries.
    """
    
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Timestamp when record was soft deleted",
    )
    
    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted.
        
        Returns:
            bool: True if record is deleted, False otherwise.
        """
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        """Mark record as deleted."""
        self.deleted_at = datetime.now(timezone.utc)
    
    def restore(self) -> None:
        """Restore soft deleted record."""
        self.deleted_at = None


class AuditMixin(TimestampMixin):
    """Mixin that adds audit fields to models.
    
    Extends TimestampMixin with additional audit information:
    - created_by: User ID who created the record
    - updated_by: User ID who last updated the record
    """
    
    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="User ID who created the record",
    )
    
    updated_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="User ID who last updated the record",
    )


# Commonly used base class combinations
class BaseModel(Base, IDMixin, TimestampMixin):
    """Base model with ID and timestamps.
    
    This is the most commonly used base class for models.
    Provides:
    - id: Primary key
    - created_at: Creation timestamp
    - updated_at: Update timestamp
    """
    __abstract__ = True


class BaseModelWithSoftDelete(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    """Base model with ID, timestamps, and soft delete.
    
    Use this for models that need soft delete functionality.
    """
    __abstract__ = True


class BaseModelWithAudit(Base, IDMixin, AuditMixin):
    """Base model with ID and full audit trail.
    
    Use this for models that need to track who created/updated records.
    """
    __abstract__ = True
