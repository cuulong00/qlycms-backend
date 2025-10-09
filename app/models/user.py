"""
User model với FastAPI-Users integration.
Hỗ trợ authentication, authorization, và user management cho YCMS.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
import enum

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.item import Item
    from app.models.supplier import Supplier


class UserType(str, enum.Enum):
    """User type enumeration.
    
    Attributes:
        ALADDIN: User là nhân viên của Aladdin Restaurant Chain
        SUPPLIER: User là nhân viên của nhà cung cấp
    """
    ALADDIN = "aladdin"
    SUPPLIER = "supplier"


class UserRole(str, enum.Enum):
    """User role enumeration.
    
    Defines các roles trong hệ thống với permissions khác nhau:
    - super_admin: Full access to everything
    - aladdin_admin: Quản lý toàn bộ YCMS và master data
    - aladdin_staff: Tạo YCMS, xác nhận giao hàng
    - supplier_admin: Quản lý YCMS và delivery notes của supplier
    - supplier_staff: Xem YCMS, cập nhật delivery status
    """
    SUPER_ADMIN = "super_admin"
    ALADDIN_ADMIN = "aladdin_admin"
    ALADDIN_STAFF = "aladdin_staff"
    SUPPLIER_ADMIN = "supplier_admin"
    SUPPLIER_STAFF = "supplier_staff"


class User(SQLAlchemyBaseUserTable[int], Base, TimestampMixin):
    """User model with FastAPI-Users and YCMS integration.
    
    Extends FastAPI-Users base table với các fields và business logic
    specific cho YCMS (Yêu Cầu Mua Sắm system).
    
    Attributes:
        id: Primary key, auto-increment
        email: Unique email for login
        hashed_password: BCrypt hashed password
        is_active: Account active status
        is_superuser: Superuser flag
        is_verified: Email verification status
        user_type: Type of user (aladdin/supplier)
        role: User role with specific permissions
        first_name: User's first name
        last_name: User's last name
        phone_number: Contact phone number
        avatar_url: Profile picture URL
        supplier_id: Foreign key to supplier (required for supplier users)
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    
    Relationships:
        supplier: Related supplier if user_type is SUPPLIER
        procurement_requests: YCMSs created by this user
        notifications: Notifications sent to this user
        audit_logs: Audit trail of user's actions
        items: Items created by user (legacy relationship)
    
    Business Methods:
        can_manage_all_ycms(): Check if user can manage all YCMSs
        can_create_ycms(): Check if user can create YCMS
        can_create_delivery_note(): Check if user can create delivery notes
    """
    __tablename__ = "users"
    
    # Explicitly declare primary key for SQLAlchemy 2.0 compatibility
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Inherited from SQLAlchemyBaseUserTable[int]:
    # - email: Mapped[str] (unique, indexed)
    # - hashed_password: Mapped[str]
    # - is_active: Mapped[bool] (default True)
    # - is_superuser: Mapped[bool] (default False)
    # - is_verified: Mapped[bool] (default False)
    
    # YCMS-specific fields
    user_type: Mapped[UserType] = mapped_column(
        SQLEnum(UserType, name="user_type_enum", create_constraint=True),
        nullable=False,
        index=True,
        comment="Type of user: aladdin or supplier"
    )
    
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum", create_constraint=True),
        nullable=False,
        index=True,
        comment="User role with specific permissions"
    )
    
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="User's first name"
    )
    
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="User's last name"
    )
    
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Contact phone number"
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Profile picture URL"
    )
    
    supplier_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("suppliers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Foreign key to supplier (required for supplier users)"
    )
    
    # Relationships
    supplier: Mapped[Optional["Supplier"]] = relationship(
        "Supplier",
        back_populates="users",
        lazy="selectin"
    )
    
    # procurement_requests: Mapped[list["ProcurementRequest"]] = relationship(
    #     "ProcurementRequest",
    #     back_populates="created_by_user",
    #     foreign_keys="[ProcurementRequest.created_by]",
    #     lazy="selectin"
    # )
    
    # notifications: Mapped[list["Notification"]] = relationship(
    #     "Notification",
    #     back_populates="user",
    #     lazy="selectin"
    # )
    
    # audit_logs: Mapped[list["AuditLog"]] = relationship(
    #     "AuditLog",
    #     back_populates="user",
    #     lazy="selectin"
    # )
    
    # Legacy relationship (kept for backward compatibility)
    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation of User."""
        return (
            f"<User(id={self.id}, email='{self.email}', "
            f"user_type={self.user_type}, role={self.role})>"
        )
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def can_manage_all_ycms(self) -> bool:
        """Check if user can manage all YCMSs across all suppliers.
        
        Returns:
            True if user is super_admin or aladdin_admin
        """
        return self.role in (UserRole.SUPER_ADMIN, UserRole.ALADDIN_ADMIN)
    
    def can_create_ycms(self) -> bool:
        """Check if user can create YCMS (Procurement Request).
        
        Returns:
            True if user is super_admin, aladdin_admin, or aladdin_staff
        """
        return self.role in (
            UserRole.SUPER_ADMIN,
            UserRole.ALADDIN_ADMIN,
            UserRole.ALADDIN_STAFF
        )
    
    def can_create_delivery_note(self) -> bool:
        """Check if user can create delivery notes.
        
        Returns:
            True if user is super_admin, aladdin_admin, aladdin_staff, or supplier_admin
        """
        return self.role in (
            UserRole.SUPER_ADMIN,
            UserRole.ALADDIN_ADMIN,
            UserRole.ALADDIN_STAFF,
            UserRole.SUPPLIER_ADMIN
        )
    
    def can_manage_supplier_ycms(self, supplier_id: int) -> bool:
        """Check if user can manage YCMSs for a specific supplier.
        
        Args:
            supplier_id: The supplier ID to check
            
        Returns:
            True if user can manage YCMSs for the specified supplier
        """
        # Super admin và aladdin admin có thể quản lý tất cả
        if self.can_manage_all_ycms():
            return True
        
        # Supplier admin/staff chỉ quản lý YCMSs của supplier mình
        if self.user_type == UserType.SUPPLIER and self.supplier_id == supplier_id:
            return self.role in (UserRole.SUPPLIER_ADMIN, UserRole.SUPPLIER_STAFF)
        
        return False
