"""
Supplier API endpoints.
Provides CRUD operations for supplier management in YCMS.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User, UserRole
from app.schemas.common import PaginatedResponse
from app.schemas.supplier import (
    SupplierCreate,
    SupplierList,
    SupplierRead,
    SupplierUpdate,
)
from app.services.supplier_service import SupplierService

router = APIRouter()


@router.post(
    "",
    response_model=SupplierRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create new supplier",
    description="Create a new supplier. Requires 'suppliers:create' permission.",
)
async def create_supplier(
    supplier_data: SupplierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SupplierRead:
    """
    Create a new supplier with the following information:
    
    - **code**: Unique supplier code (must start with 'SUP')
    - **name**: Supplier name
    - **email**: Contact email (unique)
    - **tax_code**: Tax identification number (unique)
    - **phone**: Contact phone number
    - **address**: Full address
    - **contact_person**: Contact person name
    - **contact_phone**: Contact person phone
    - **contact_email**: Contact person email
    
    Only users with 'suppliers:create' permission can create suppliers.
    """
    service = SupplierService(db)
    supplier = await service.create_supplier(supplier_data, current_user.id)
    return SupplierRead.model_validate(supplier)


@router.get(
    "",
    response_model=PaginatedResponse[SupplierList],
    summary="List suppliers",
    description="Get paginated list of suppliers with optional filtering.",
)
async def list_suppliers(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PaginatedResponse[SupplierList]:
    """
    List all suppliers with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 50, max: 100)
    - **is_active**: Optional filter by active status
    
    Returns paginated list with total count.
    """
    service = SupplierService(db)
    suppliers, total = await service.list_suppliers(
        skip=skip,
        limit=limit,
        is_active=is_active,
    )
    
    return PaginatedResponse(
        items=[SupplierList.model_validate(s) for s in suppliers],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/search",
    response_model=list[SupplierList],
    summary="Search suppliers",
    description="Search suppliers by name or code.",
)
async def search_suppliers(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[SupplierList]:
    """
    Search suppliers by name or code.
    
    - **q**: Search query (searches in name and code fields)
    - **limit**: Maximum number of results (default: 20, max: 100)
    
    Returns list of matching suppliers.
    """
    service = SupplierService(db)
    suppliers = await service.search_suppliers(q, limit=limit)
    return [SupplierList.model_validate(s) for s in suppliers]


@router.get(
    "/{supplier_id}",
    response_model=SupplierRead,
    summary="Get supplier by ID",
    description="Get detailed information about a specific supplier.",
)
async def get_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SupplierRead:
    """
    Get supplier details by ID.
    
    - **supplier_id**: ID of the supplier to retrieve
    
    Returns full supplier information including timestamps and audit fields.
    """
    service = SupplierService(db)
    supplier = await service.get_supplier(supplier_id)
    return SupplierRead.model_validate(supplier)


@router.patch(
    "/{supplier_id}",
    response_model=SupplierRead,
    summary="Update supplier",
    description="Update supplier information. Requires 'suppliers:update' permission.",
)
async def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SupplierRead:
    """
    Update supplier information.
    
    - **supplier_id**: ID of the supplier to update
    - **supplier_data**: Fields to update (all fields are optional)
    
    Only users with 'suppliers:update' permission can update suppliers.
    Validates uniqueness of code, email, and tax_code if changed.
    """
    service = SupplierService(db)
    supplier = await service.update_supplier(
        supplier_id, supplier_data, current_user.id
    )
    return SupplierRead.model_validate(supplier)


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete supplier",
    description="Soft delete a supplier. Requires 'suppliers:delete' permission.",
)
async def delete_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Soft delete a supplier.
    
    - **supplier_id**: ID of the supplier to delete
    
    Only users with 'suppliers:delete' permission can delete suppliers.
    Cannot delete suppliers that have active users associated with them.
    """
    service = SupplierService(db)
    await service.delete_supplier(supplier_id, current_user.id)


@router.post(
    "/{supplier_id}/activate",
    response_model=SupplierRead,
    summary="Activate supplier",
    description="Activate a deactivated supplier. Requires 'suppliers:update' permission.",
)
async def activate_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SupplierRead:
    """
    Activate a supplier.
    
    - **supplier_id**: ID of the supplier to activate
    
    Sets is_active to True for the specified supplier.
    Only users with 'suppliers:update' permission can activate suppliers.
    """
    service = SupplierService(db)
    supplier = await service.activate_supplier(supplier_id, current_user.id)
    return SupplierRead.model_validate(supplier)


@router.post(
    "/{supplier_id}/deactivate",
    response_model=SupplierRead,
    summary="Deactivate supplier",
    description="Deactivate a supplier. Requires 'suppliers:update' permission.",
)
async def deactivate_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SupplierRead:
    """
    Deactivate a supplier.
    
    - **supplier_id**: ID of the supplier to deactivate
    
    Sets is_active to False for the specified supplier.
    Only users with 'suppliers:update' permission can deactivate suppliers.
    """
    service = SupplierService(db)
    supplier = await service.deactivate_supplier(supplier_id, current_user.id)
    return SupplierRead.model_validate(supplier)
