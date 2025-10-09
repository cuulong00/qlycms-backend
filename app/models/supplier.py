"""
Supplier model.
Quản lý thông tin nhà cung cấp trong hệ thống YCMS.
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, AuditMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User
    # from app.models.product import Product
    # from app.models.procurement_request import ProcurementRequest


class Supplier(Base, SoftDeleteMixin, AuditMixin):
    """Supplier model - Nhà cung cấp.
    
    Lưu trữ thông tin về các nhà cung cấp cung cấp nguyên vật liệu
    cho hệ thống nhà hàng Aladdin.
    
    Attributes:
        id: Primary key, auto-increment
        code: Mã nhà cung cấp (unique, VD: SUP001)
        name: Tên nhà cung cấp
        name_en: Tên tiếng Anh (optional)
        tax_code: Mã số thuế
        email: Email liên hệ chính
        phone: Số điện thoại liên hệ
        address: Địa chỉ đầy đủ
        contact_person: Tên người liên hệ
        contact_phone: SĐT người liên hệ
        contact_email: Email người liên hệ
        description: Mô tả về nhà cung cấp
        is_active: Trạng thái hoạt động
        
        # Audit fields (from AuditMixin)
        created_by: User ID who created
        updated_by: User ID who last updated
        
        # Soft delete (from SoftDeleteMixin)
        is_deleted: Soft delete flag
        deleted_at: Deletion timestamp
        deleted_by: User ID who deleted
        
        # Timestamps (from TimestampMixin)
        created_at: Creation timestamp
        updated_at: Last update timestamp
    
    Relationships:
        users: List of users working for this supplier
        products: List of products supplied by this supplier
        procurement_requests: List of YCMSs for this supplier
    
    Business Rules:
        - Supplier code must be unique
        - Email must be unique
        - Tax code should be unique (but nullable)
        - At least one contact method required (email or phone)
        - Cannot delete supplier with active procurement requests
    """
    __tablename__ = "suppliers"
    
    # Explicitly declare primary key for SQLAlchemy 2.0 compatibility
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Basic Information
    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Mã nhà cung cấp (VD: SUP001)"
    )
    
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
        comment="Tên nhà cung cấp"
    )
    
    name_en: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="Tên tiếng Anh"
    )
    
    tax_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        index=True,
        comment="Mã số thuế"
    )
    
    # Contact Information
    email: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        unique=True,
        index=True,
        comment="Email liên hệ chính"
    )
    
    phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Số điện thoại liên hệ"
    )
    
    address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Địa chỉ đầy đủ"
    )
    
    # Contact Person
    contact_person: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Tên người liên hệ"
    )
    
    contact_phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="SĐT người liên hệ"
    )
    
    contact_email: Mapped[Optional[str]] = mapped_column(
        String(320),
        nullable=True,
        comment="Email người liên hệ"
    )
    
    # Additional Info
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Mô tả về nhà cung cấp"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Trạng thái hoạt động"
    )
    
    # Relationships
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="supplier",
        foreign_keys="[User.supplier_id]",
        lazy="selectin"
    )
    
    # products: Mapped[list["Product"]] = relationship(
    #     "Product",
    #     back_populates="supplier",
    #     lazy="selectin"
    # )
    
    # procurement_requests: Mapped[list["ProcurementRequest"]] = relationship(
    #     "ProcurementRequest",
    #     back_populates="supplier",
    #     lazy="selectin"
    # )

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"<Supplier(id={self.id}, code='{self.code}', "
            f"name='{self.name}', is_active={self.is_active})>"
        )
    
    @property
    def display_name(self) -> str:
        """Get display name with code."""
        return f"[{self.code}] {self.name}"
    
    def has_active_users(self) -> bool:
        """Check if supplier has any active users.
        
        Returns:
            True if supplier has active users
        """
        return any(user.is_active for user in self.users)
    
    def can_be_deleted(self) -> tuple[bool, Optional[str]]:
        """Check if supplier can be deleted.
        
        Returns:
            Tuple of (can_delete, reason_if_not)
        """
        # Check if already deleted
        if self.is_deleted:
            return False, "Supplier is already deleted"
        
        # Check for active users
        if self.has_active_users():
            return False, "Cannot delete supplier with active users"
        
        # TODO: Check for active procurement requests
        # if self.has_active_procurement_requests():
        #     return False, "Cannot delete supplier with active procurement requests"
        
        # TODO: Check for products
        # if self.products:
        #     return False, "Cannot delete supplier with products"
        
        return True, None
    
    def get_primary_contact(self) -> dict[str, Optional[str]]:
        """Get primary contact information.
        
        Returns:
            Dictionary with contact details
        """
        return {
            "person": self.contact_person,
            "phone": self.contact_phone or self.phone,
            "email": self.contact_email or self.email,
        }
