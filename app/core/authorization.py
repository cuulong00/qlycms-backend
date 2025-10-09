"""
Casbin RBAC authorization configuration.
Định nghĩa model, policies, và permission checking cho YCMS.
"""

import logging
from pathlib import Path
from typing import Optional

import casbin
from fastapi import Depends, HTTPException, status

from app.core.auth import current_active_user
from app.models.user import User, UserRole, UserType

logger = logging.getLogger(__name__)

# Casbin model file path
CASBIN_MODEL_PATH = Path(__file__).parent / "casbin_model.conf"


def get_enforcer() -> casbin.Enforcer:
    """Get Casbin enforcer instance.
    
    Returns:
        Casbin enforcer with RBAC model loaded
        
    Note:
        In production, use CasbinAdapter with database storage
        For now, using in-memory adapter for development
    """
    if not CASBIN_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Casbin model file not found: {CASBIN_MODEL_PATH}"
        )
    
    # Create enforcer with model file
    enforcer = casbin.Enforcer(str(CASBIN_MODEL_PATH))
    
    # Load policies (in production, this would be from database)
    _load_policies(enforcer)
    
    return enforcer


def _load_policies(enforcer: casbin.Enforcer) -> None:
    """Load RBAC policies into Casbin enforcer.
    
    Defines permissions for each role:
    - super_admin: Full access to everything
    - aladdin_admin: Manage YCMS, suppliers, products, restaurants
    - aladdin_staff: Create YCMS, view data, confirm delivery
    - supplier_admin: Manage supplier's YCMS and delivery notes
    - supplier_staff: View supplier's YCMS, update delivery status
    
    Args:
        enforcer: Casbin enforcer instance
    """
    # Format: (role, resource, action)
    
    # Super Admin - Full access
    policies = [
        # Super admin has all permissions
        (UserRole.SUPER_ADMIN.value, "users", "create"),
        (UserRole.SUPER_ADMIN.value, "users", "read"),
        (UserRole.SUPER_ADMIN.value, "users", "update"),
        (UserRole.SUPER_ADMIN.value, "users", "delete"),
        (UserRole.SUPER_ADMIN.value, "suppliers", "create"),
        (UserRole.SUPER_ADMIN.value, "suppliers", "read"),
        (UserRole.SUPER_ADMIN.value, "suppliers", "update"),
        (UserRole.SUPER_ADMIN.value, "suppliers", "delete"),
        (UserRole.SUPER_ADMIN.value, "products", "create"),
        (UserRole.SUPER_ADMIN.value, "products", "read"),
        (UserRole.SUPER_ADMIN.value, "products", "update"),
        (UserRole.SUPER_ADMIN.value, "products", "delete"),
        (UserRole.SUPER_ADMIN.value, "restaurants", "create"),
        (UserRole.SUPER_ADMIN.value, "restaurants", "read"),
        (UserRole.SUPER_ADMIN.value, "restaurants", "update"),
        (UserRole.SUPER_ADMIN.value, "restaurants", "delete"),
        (UserRole.SUPER_ADMIN.value, "procurement_requests", "create"),
        (UserRole.SUPER_ADMIN.value, "procurement_requests", "read"),
        (UserRole.SUPER_ADMIN.value, "procurement_requests", "update"),
        (UserRole.SUPER_ADMIN.value, "procurement_requests", "delete"),
        (UserRole.SUPER_ADMIN.value, "delivery_notes", "create"),
        (UserRole.SUPER_ADMIN.value, "delivery_notes", "read"),
        (UserRole.SUPER_ADMIN.value, "delivery_notes", "update"),
        (UserRole.SUPER_ADMIN.value, "delivery_notes", "delete"),
        
        # Aladdin Admin - Manage master data and YCMS
        (UserRole.ALADDIN_ADMIN.value, "suppliers", "create"),
        (UserRole.ALADDIN_ADMIN.value, "suppliers", "read"),
        (UserRole.ALADDIN_ADMIN.value, "suppliers", "update"),
        (UserRole.ALADDIN_ADMIN.value, "suppliers", "delete"),
        (UserRole.ALADDIN_ADMIN.value, "products", "create"),
        (UserRole.ALADDIN_ADMIN.value, "products", "read"),
        (UserRole.ALADDIN_ADMIN.value, "products", "update"),
        (UserRole.ALADDIN_ADMIN.value, "products", "delete"),
        (UserRole.ALADDIN_ADMIN.value, "restaurants", "create"),
        (UserRole.ALADDIN_ADMIN.value, "restaurants", "read"),
        (UserRole.ALADDIN_ADMIN.value, "restaurants", "update"),
        (UserRole.ALADDIN_ADMIN.value, "restaurants", "delete"),
        (UserRole.ALADDIN_ADMIN.value, "procurement_requests", "create"),
        (UserRole.ALADDIN_ADMIN.value, "procurement_requests", "read"),
        (UserRole.ALADDIN_ADMIN.value, "procurement_requests", "update"),
        (UserRole.ALADDIN_ADMIN.value, "procurement_requests", "delete"),
        (UserRole.ALADDIN_ADMIN.value, "delivery_notes", "create"),
        (UserRole.ALADDIN_ADMIN.value, "delivery_notes", "read"),
        (UserRole.ALADDIN_ADMIN.value, "delivery_notes", "update"),
        (UserRole.ALADDIN_ADMIN.value, "delivery_notes", "delete"),
        (UserRole.ALADDIN_ADMIN.value, "users", "read"),  # View users
        (UserRole.ALADDIN_ADMIN.value, "users", "update"),  # Update users
        
        # Aladdin Staff - Create YCMS and confirm delivery
        (UserRole.ALADDIN_STAFF.value, "suppliers", "read"),
        (UserRole.ALADDIN_STAFF.value, "products", "read"),
        (UserRole.ALADDIN_STAFF.value, "restaurants", "read"),
        (UserRole.ALADDIN_STAFF.value, "procurement_requests", "create"),
        (UserRole.ALADDIN_STAFF.value, "procurement_requests", "read"),
        (UserRole.ALADDIN_STAFF.value, "delivery_notes", "create"),
        (UserRole.ALADDIN_STAFF.value, "delivery_notes", "read"),
        (UserRole.ALADDIN_STAFF.value, "delivery_notes", "update"),  # Confirm delivery
        
        # Supplier Admin - Manage supplier's YCMS
        (UserRole.SUPPLIER_ADMIN.value, "products", "read"),  # View products
        (UserRole.SUPPLIER_ADMIN.value, "procurement_requests", "read"),  # View own YCMS
        (UserRole.SUPPLIER_ADMIN.value, "procurement_requests", "update"),  # Update own YCMS
        (UserRole.SUPPLIER_ADMIN.value, "delivery_notes", "create"),  # Create delivery notes
        (UserRole.SUPPLIER_ADMIN.value, "delivery_notes", "read"),  # View own delivery notes
        (UserRole.SUPPLIER_ADMIN.value, "delivery_notes", "update"),  # Update delivery status
        (UserRole.SUPPLIER_ADMIN.value, "users", "read"),  # View supplier users
        
        # Supplier Staff - View and update delivery status
        (UserRole.SUPPLIER_STAFF.value, "products", "read"),
        (UserRole.SUPPLIER_STAFF.value, "procurement_requests", "read"),
        (UserRole.SUPPLIER_STAFF.value, "delivery_notes", "read"),
        (UserRole.SUPPLIER_STAFF.value, "delivery_notes", "update"),  # Update delivery status
    ]
    
    # Add all policies to enforcer
    for role, resource, action in policies:
        enforcer.add_policy(role, resource, action)
    
    logger.info(f"Loaded {len(policies)} Casbin policies")


class PermissionChecker:
    """Dependency for checking user permissions.
    
    Usage:
        @router.get("/suppliers")
        async def list_suppliers(
            user: User = Depends(current_active_user),
            _: None = Depends(PermissionChecker("suppliers", "read"))
        ):
            ...
    """
    
    def __init__(self, resource: str, action: str):
        """Initialize permission checker.
        
        Args:
            resource: Resource name (e.g., "suppliers", "products")
            action: Action name (e.g., "create", "read", "update", "delete")
        """
        self.resource = resource
        self.action = action
    
    async def __call__(
        self,
        user: User = Depends(current_active_user),
    ) -> None:
        """Check if user has permission.
        
        Args:
            user: Current authenticated user
            
        Raises:
            HTTPException: If user doesn't have permission
        """
        enforcer = get_enforcer()
        
        # Check permission
        has_permission = enforcer.enforce(
            user.role.value,  # subject (role)
            self.resource,    # object (resource)
            self.action,      # action
        )
        
        if not has_permission:
            logger.warning(
                f"Permission denied: User {user.id} ({user.role.value}) "
                f"attempted to {self.action} {self.resource}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions to {self.action} {self.resource}",
            )


def require_permission(resource: str, action: str):
    """Decorator-style permission checker.
    
    Args:
        resource: Resource name
        action: Action name
        
    Returns:
        PermissionChecker instance
        
    Example:
        async def create_supplier(
            user: User = Depends(current_active_user),
            _: None = Depends(require_permission("suppliers", "create"))
        ):
            ...
    """
    return PermissionChecker(resource, action)


async def check_supplier_access(
    user: User,
    supplier_id: int,
) -> bool:
    """Check if user can access specific supplier's data.
    
    Rules:
    - Super admin and aladdin admin can access all suppliers
    - Supplier users can only access their own supplier's data
    
    Args:
        user: Current user
        supplier_id: Supplier ID to check
        
    Returns:
        True if user can access, False otherwise
    """
    # Super admin and aladdin admin can access all
    if user.role in (UserRole.SUPER_ADMIN, UserRole.ALADDIN_ADMIN):
        return True
    
    # Supplier users can only access their own supplier
    if user.user_type == UserType.SUPPLIER:
        return user.supplier_id == supplier_id
    
    # Aladdin staff can view all suppliers
    if user.role == UserRole.ALADDIN_STAFF:
        return True
    
    return False


class SupplierAccessChecker:
    """Dependency for checking supplier-specific access.
    
    Usage:
        @router.get("/suppliers/{supplier_id}")
        async def get_supplier(
            supplier_id: int,
            user: User = Depends(current_active_user),
            _: None = Depends(SupplierAccessChecker())
        ):
            ...
    """
    
    def __init__(self, supplier_id_param: str = "supplier_id"):
        """Initialize supplier access checker.
        
        Args:
            supplier_id_param: Name of path parameter containing supplier_id
        """
        self.supplier_id_param = supplier_id_param
    
    async def __call__(
        self,
        supplier_id: int,
        user: User = Depends(current_active_user),
    ) -> None:
        """Check if user can access supplier.
        
        Args:
            supplier_id: Supplier ID from path parameter
            user: Current authenticated user
            
        Raises:
            HTTPException: If user cannot access supplier
        """
        has_access = await check_supplier_access(user, supplier_id)
        
        if not has_access:
            logger.warning(
                f"Supplier access denied: User {user.id} ({user.role.value}) "
                f"attempted to access supplier {supplier_id}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this supplier's data",
            )
