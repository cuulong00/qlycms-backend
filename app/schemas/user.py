"""
User schemas với FastAPI-Users integration.
Định nghĩa các Pydantic schemas cho User CRUD operations.
"""

from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, Field, field_validator

from app.models.user import UserRole, UserType


class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data.
    
    Extends FastAPI-Users BaseUser với YCMS-specific fields.
    Used for API responses.
    
    Attributes:
        id: User ID
        email: User email
        is_active: Account active status
        is_superuser: Superuser status
        is_verified: Email verification status
        user_type: Type of user (aladdin/supplier)
        role: User role
        first_name: User's first name
        last_name: User's last name
        phone_number: Contact phone
        avatar_url: Profile picture URL
        supplier_id: Related supplier ID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    user_type: UserType
    role: UserRole
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    supplier_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating new user.
    
    Extends FastAPI-Users BaseUserCreate với YCMS-specific fields và validation.
    
    Attributes:
        email: User email (required, unique)
        password: Plain password (required, will be hashed)
        user_type: Type of user (required)
        role: User role (required)
        first_name: First name (required)
        last_name: Last name (required)
        phone_number: Contact phone (optional)
        avatar_url: Profile picture URL (optional)
        supplier_id: Related supplier ID (required if user_type is SUPPLIER)
        is_active: Account active status (default True)
        is_superuser: Superuser status (default False)
        is_verified: Email verification status (default False)
    """
    user_type: UserType
    role: UserRole
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)
    supplier_id: Optional[int] = None

    @field_validator("supplier_id")
    @classmethod
    def validate_supplier_id(cls, v: Optional[int], info) -> Optional[int]:
        """Validate supplier_id based on user_type.
        
        Rules:
        - If user_type is SUPPLIER, supplier_id is required
        - If user_type is ALADDIN, supplier_id must be None
        
        Args:
            v: supplier_id value
            info: Validation context with other field values
            
        Returns:
            Validated supplier_id
            
        Raises:
            ValueError: If validation fails
        """
        user_type = info.data.get("user_type")
        
        if user_type == UserType.SUPPLIER and v is None:
            raise ValueError(
                "supplier_id is required for SUPPLIER user type"
            )
        
        if user_type == UserType.ALADDIN and v is not None:
            raise ValueError(
                "supplier_id must be None for ALADDIN user type"
            )
        
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: UserRole, info) -> UserRole:
        """Validate role based on user_type.
        
        Rules:
        - ALADDIN users can only have: super_admin, aladdin_admin, aladdin_staff
        - SUPPLIER users can only have: supplier_admin, supplier_staff
        
        Args:
            v: role value
            info: Validation context with other field values
            
        Returns:
            Validated role
            
        Raises:
            ValueError: If validation fails
        """
        user_type = info.data.get("user_type")
        
        aladdin_roles = {
            UserRole.SUPER_ADMIN,
            UserRole.ALADDIN_ADMIN,
            UserRole.ALADDIN_STAFF,
        }
        supplier_roles = {UserRole.SUPPLIER_ADMIN, UserRole.SUPPLIER_STAFF}
        
        if user_type == UserType.ALADDIN and v not in aladdin_roles:
            raise ValueError(
                f"Invalid role for ALADDIN user. Must be one of: "
                f"{', '.join([r.value for r in aladdin_roles])}"
            )
        
        if user_type == UserType.SUPPLIER and v not in supplier_roles:
            raise ValueError(
                f"Invalid role for SUPPLIER user. Must be one of: "
                f"{', '.join([r.value for r in supplier_roles])}"
            )
        
        return v


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user.
    
    Extends FastAPI-Users BaseUserUpdate với YCMS-specific fields.
    All fields are optional for partial updates.
    
    Attributes:
        email: New email (optional)
        password: New password (optional, will be hashed)
        user_type: New user type (optional)
        role: New role (optional)
        first_name: New first name (optional)
        last_name: New last name (optional)
        phone_number: New phone (optional)
        avatar_url: New avatar URL (optional)
        supplier_id: New supplier ID (optional)
        is_active: New active status (optional)
        is_superuser: New superuser status (optional)
        is_verified: New verified status (optional)
    """
    user_type: Optional[UserType] = None
    role: Optional[UserRole] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)
    supplier_id: Optional[int] = None

    @field_validator("supplier_id")
    @classmethod
    def validate_supplier_id(cls, v: Optional[int], info) -> Optional[int]:
        """Validate supplier_id based on user_type if both are provided.
        
        Args:
            v: supplier_id value
            info: Validation context
            
        Returns:
            Validated supplier_id
            
        Raises:
            ValueError: If validation fails
        """
        user_type = info.data.get("user_type")
        
        # Only validate if user_type is also being updated
        if user_type is not None:
            if user_type == UserType.SUPPLIER and v is None:
                raise ValueError(
                    "supplier_id is required for SUPPLIER user type"
                )
            
            if user_type == UserType.ALADDIN and v is not None:
                raise ValueError(
                    "supplier_id must be None for ALADDIN user type"
                )
        
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[UserRole], info) -> Optional[UserRole]:
        """Validate role based on user_type if both are provided.
        
        Args:
            v: role value
            info: Validation context
            
        Returns:
            Validated role
            
        Raises:
            ValueError: If validation fails
        """
        if v is None:
            return v
        
        user_type = info.data.get("user_type")
        
        # Only validate if user_type is also being updated
        if user_type is not None:
            aladdin_roles = {
                UserRole.SUPER_ADMIN,
                UserRole.ALADDIN_ADMIN,
                UserRole.ALADDIN_STAFF,
            }
            supplier_roles = {UserRole.SUPPLIER_ADMIN, UserRole.SUPPLIER_STAFF}
            
            if user_type == UserType.ALADDIN and v not in aladdin_roles:
                raise ValueError(
                    f"Invalid role for ALADDIN user. Must be one of: "
                    f"{', '.join([r.value for r in aladdin_roles])}"
                )
            
            if user_type == UserType.SUPPLIER and v not in supplier_roles:
                raise ValueError(
                    f"Invalid role for SUPPLIER user. Must be one of: "
                    f"{', '.join([r.value for r in supplier_roles])}"
                )
        
        return v


class UserProfileUpdate(schemas.BaseModel):
    """Schema for updating user profile (non-security fields).
    
    Used for users updating their own profile.
    Does not include security-sensitive fields like role, user_type, or is_superuser.
    
    Attributes:
        first_name: New first name (optional)
        last_name: New last name (optional)
        phone_number: New phone (optional)
        avatar_url: New avatar URL (optional)
    """
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)

    class Config:
        from_attributes = True


class UserRoleUpdate(schemas.BaseModel):
    """Schema for updating user role.
    
    Used by administrators to change user roles.
    Requires appropriate permissions.
    
    Attributes:
        role: New role (required)
    """
    role: UserRole

    @field_validator("role")
    @classmethod
    def validate_role_change(cls, v: UserRole) -> UserRole:
        """Validate role change.
        
        Additional validation logic can be added here based on
        business rules (e.g., certain roles can only be set by super_admin).
        
        Args:
            v: new role value
            
        Returns:
            Validated role
        """
        # Add any role-specific validation here
        return v

    class Config:
        from_attributes = True


class UserList(schemas.BaseModel):
    """Schema for user list item (lightweight).
    
    Used in list views where full user details are not needed.
    
    Attributes:
        id: User ID
        email: User email
        first_name: User's first name
        last_name: User's last name
        user_type: Type of user
        role: User role
        is_active: Account active status
    """
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    user_type: UserType
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class UserListResponse(schemas.BaseModel):
    """Schema for paginated user list response.
    
    Attributes:
        users: List of users
        total: Total number of users
        skip: Number of users skipped
        limit: Maximum number of users per page
    """
    users: list[UserList]
    total: int
    skip: int
    limit: int

    class Config:
        from_attributes = True
