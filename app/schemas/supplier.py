"""
Supplier schemas.
Pydantic schemas cho Supplier CRUD operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import BaseSchema


class SupplierBase(BaseSchema):
    """Base supplier schema với shared fields."""
    
    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Mã nhà cung cấp (VD: SUP001)",
        examples=["SUP001", "SUP002"]
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Tên nhà cung cấp"
    )
    name_en: Optional[str] = Field(
        None,
        max_length=200,
        description="Tên tiếng Anh"
    )
    tax_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Mã số thuế"
    )
    email: EmailStr = Field(
        ...,
        description="Email liên hệ chính"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Số điện thoại liên hệ"
    )
    address: Optional[str] = Field(
        None,
        description="Địa chỉ đầy đủ"
    )
    contact_person: Optional[str] = Field(
        None,
        max_length=100,
        description="Tên người liên hệ"
    )
    contact_phone: Optional[str] = Field(
        None,
        max_length=20,
        description="SĐT người liên hệ"
    )
    contact_email: Optional[EmailStr] = Field(
        None,
        description="Email người liên hệ"
    )
    description: Optional[str] = Field(
        None,
        description="Mô tả về nhà cung cấp"
    )
    is_active: bool = Field(
        default=True,
        description="Trạng thái hoạt động"
    )


class SupplierCreate(SupplierBase):
    """Schema for creating supplier.
    
    Validates that supplier has at least one contact method.
    """
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: EmailStr) -> EmailStr:
        """Validate email is not empty."""
        if not v or not v.strip():
            raise ValueError("Email is required")
        return v.strip().lower()
    
    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate and normalize supplier code.
        
        - Must be uppercase
        - Must start with SUP
        - Can contain letters, numbers, and hyphens
        """
        v = v.strip().upper()
        
        if not v.startswith("SUP"):
            raise ValueError("Supplier code must start with 'SUP'")
        
        # Allow alphanumeric and hyphens only
        if not all(c.isalnum() or c == "-" for c in v):
            raise ValueError(
                "Supplier code can only contain letters, numbers, and hyphens"
            )
        
        return v


class SupplierUpdate(BaseSchema):
    """Schema for updating supplier.
    
    All fields are optional for partial updates.
    """
    
    code: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Mã nhà cung cấp"
    )
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Tên nhà cung cấp"
    )
    name_en: Optional[str] = Field(
        None,
        max_length=200,
        description="Tên tiếng Anh"
    )
    tax_code: Optional[str] = Field(
        None,
        max_length=50,
        description="Mã số thuế"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Email liên hệ chính"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Số điện thoại"
    )
    address: Optional[str] = Field(
        None,
        description="Địa chỉ"
    )
    contact_person: Optional[str] = Field(
        None,
        max_length=100,
        description="Tên người liên hệ"
    )
    contact_phone: Optional[str] = Field(
        None,
        max_length=20,
        description="SĐT người liên hệ"
    )
    contact_email: Optional[EmailStr] = Field(
        None,
        description="Email người liên hệ"
    )
    description: Optional[str] = Field(
        None,
        description="Mô tả"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Trạng thái hoạt động"
    )
    
    @field_validator("code")
    @classmethod
    def validate_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate supplier code if provided."""
        if v is None:
            return v
        
        v = v.strip().upper()
        
        if not v.startswith("SUP"):
            raise ValueError("Supplier code must start with 'SUP'")
        
        if not all(c.isalnum() or c == "-" for c in v):
            raise ValueError(
                "Supplier code can only contain letters, numbers, and hyphens"
            )
        
        return v


class SupplierRead(SupplierBase):
    """Schema for reading supplier data.
    
    Includes all fields plus timestamps and audit info.
    """
    
    id: int = Field(..., description="Supplier ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: Optional[int] = Field(None, description="Created by user ID")
    updated_by: Optional[int] = Field(None, description="Updated by user ID")
    is_deleted: bool = Field(False, description="Soft delete flag")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
    deleted_by: Optional[int] = Field(None, description="Deleted by user ID")
    
    class Config:
        from_attributes = True


class SupplierList(BaseSchema):
    """Schema for supplier in list responses (lighter)."""
    
    id: int
    code: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SupplierWithUsers(SupplierRead):
    """Schema for supplier with related users."""
    
    user_count: int = Field(0, description="Number of users")
    active_user_count: int = Field(0, description="Number of active users")
    
    class Config:
        from_attributes = True
