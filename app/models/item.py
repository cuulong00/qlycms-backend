"""Item model - example domain model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IDMixin, StatusMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Item(Base, IDMixin, TimestampMixin, StatusMixin):
    """Item model - example entity for demonstration.
    
    This is a sample model to demonstrate the architecture.
    Replace with your actual domain models.
    """
    
    __tablename__ = "items"
    
    # Item fields
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Item title",
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Item description",
    )
    
    # Foreign key to user
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Owner user ID",
    )
    
    # Relationships
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="items",
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"<Item(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"
