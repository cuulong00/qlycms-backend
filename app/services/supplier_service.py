"""
Supplier service.
Business logic layer cho Supplier operations.
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier import Supplier
from app.repositories.supplier import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    """Service for supplier business logic.
    
    Handles validation, business rules, and orchestrates
    repository operations for suppliers.
    """
    
    def __init__(self, session: AsyncSession):
        """Initialize service with database session.
        
        Args:
            session: Async database session
        """
        self.repository = SupplierRepository(session)
        self.session = session
    
    async def create_supplier(
        self,
        supplier_data: SupplierCreate,
        created_by: Optional[int] = None
    ) -> Supplier:
        """Create new supplier.
        
        Args:
            supplier_data: Supplier data from request
            created_by: User ID who is creating the supplier
            
        Returns:
            Created supplier
            
        Raises:
            HTTPException: If validation fails or code/email already exists
        """
        # Check if code already exists
        if await self.repository.exists_by_code(supplier_data.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Supplier with code '{supplier_data.code}' already exists"
            )
        
        # Check if email already exists
        if await self.repository.exists_by_email(supplier_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Supplier with email '{supplier_data.email}' already exists"
            )
        
        # Check if tax code already exists (if provided)
        if supplier_data.tax_code:
            if await self.repository.exists_by_tax_code(supplier_data.tax_code):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Supplier with tax code '{supplier_data.tax_code}' already exists"
                )
        
        # Create supplier
        supplier = Supplier(**supplier_data.model_dump())
        
        if created_by is not None:
            supplier.created_by = created_by
            supplier.updated_by = created_by
        
        created_supplier = await self.repository.create(supplier)
        await self.session.commit()
        await self.session.refresh(created_supplier)
        
        return created_supplier
    
    async def get_supplier(self, supplier_id: int) -> Supplier:
        """Get supplier by ID.
        
        Args:
            supplier_id: Supplier ID
            
        Returns:
            Supplier
            
        Raises:
            HTTPException: If supplier not found
        """
        supplier = await self.repository.get(supplier_id)
        
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Supplier with ID {supplier_id} not found"
            )
        
        return supplier
    
    async def get_supplier_by_code(self, code: str) -> Supplier:
        """Get supplier by code.
        
        Args:
            code: Supplier code
            
        Returns:
            Supplier
            
        Raises:
            HTTPException: If supplier not found
        """
        supplier = await self.repository.get_by_code(code)
        
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Supplier with code '{code}' not found"
            )
        
        return supplier
    
    async def list_suppliers(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> list[Supplier]:
        """List suppliers with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            active_only: Only return active suppliers
            
        Returns:
            List of suppliers
        """
        if active_only:
            return await self.repository.get_active(skip, limit)
        
        return await self.repository.get_all(skip, limit)
    
    async def search_suppliers(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Supplier]:
        """Search suppliers by name.
        
        Args:
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching suppliers
        """
        return await self.repository.search_by_name(search_term, skip, limit)
    
    async def update_supplier(
        self,
        supplier_id: int,
        supplier_data: SupplierUpdate,
        updated_by: Optional[int] = None
    ) -> Supplier:
        """Update supplier.
        
        Args:
            supplier_id: Supplier ID
            supplier_data: Updated supplier data
            updated_by: User ID who is updating
            
        Returns:
            Updated supplier
            
        Raises:
            HTTPException: If supplier not found or validation fails
        """
        # Get existing supplier
        supplier = await self.get_supplier(supplier_id)
        
        # Check code uniqueness if being updated
        if supplier_data.code and supplier_data.code != supplier.code:
            if await self.repository.exists_by_code(supplier_data.code, exclude_id=supplier_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Supplier with code '{supplier_data.code}' already exists"
                )
        
        # Check email uniqueness if being updated
        if supplier_data.email and supplier_data.email != supplier.email:
            if await self.repository.exists_by_email(supplier_data.email, exclude_id=supplier_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Supplier with email '{supplier_data.email}' already exists"
                )
        
        # Check tax code uniqueness if being updated
        if supplier_data.tax_code and supplier_data.tax_code != supplier.tax_code:
            if await self.repository.exists_by_tax_code(supplier_data.tax_code, exclude_id=supplier_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Supplier with tax code '{supplier_data.tax_code}' already exists"
                )
        
        # Update supplier
        update_data = supplier_data.model_dump(exclude_unset=True)
        
        if updated_by is not None:
            update_data["updated_by"] = updated_by
        
        updated_supplier = await self.repository.update(supplier_id, update_data)
        await self.session.commit()
        await self.session.refresh(updated_supplier)
        
        return updated_supplier
    
    async def delete_supplier(
        self,
        supplier_id: int,
        deleted_by: Optional[int] = None,
        hard_delete: bool = False
    ) -> bool:
        """Delete supplier (soft or hard delete).
        
        Args:
            supplier_id: Supplier ID
            deleted_by: User ID who is deleting
            hard_delete: If True, permanently delete; if False, soft delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            HTTPException: If supplier not found or cannot be deleted
        """
        # Get supplier
        supplier = await self.get_supplier(supplier_id)
        
        # Check if can be deleted
        can_delete, reason = supplier.can_be_deleted()
        if not can_delete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=reason or "Cannot delete supplier"
            )
        
        # Delete supplier
        if hard_delete:
            success = await self.repository.delete(supplier_id)
        else:
            success = await self.repository.soft_delete(supplier_id, deleted_by)
        
        await self.session.commit()
        
        return success
    
    async def activate_supplier(
        self,
        supplier_id: int,
        updated_by: Optional[int] = None
    ) -> Supplier:
        """Activate supplier.
        
        Args:
            supplier_id: Supplier ID
            updated_by: User ID who is activating
            
        Returns:
            Updated supplier
        """
        return await self.update_supplier(
            supplier_id,
            SupplierUpdate(is_active=True),
            updated_by
        )
    
    async def deactivate_supplier(
        self,
        supplier_id: int,
        updated_by: Optional[int] = None
    ) -> Supplier:
        """Deactivate supplier.
        
        Args:
            supplier_id: Supplier ID
            updated_by: User ID who is deactivating
            
        Returns:
            Updated supplier
        """
        return await self.update_supplier(
            supplier_id,
            SupplierUpdate(is_active=False),
            updated_by
        )
