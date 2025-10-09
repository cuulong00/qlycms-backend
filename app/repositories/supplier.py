"""
Supplier repository.
Data access layer cho Supplier operations.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier import Supplier
from app.repositories.base import BaseRepository


class SupplierRepository(BaseRepository[Supplier]):
    """Repository for Supplier model.
    
    Provides data access methods specific to Supplier operations.
    Inherits CRUD operations from BaseRepository.
    """
    
    def __init__(self, session: AsyncSession):
        """Initialize repository with database session.
        
        Args:
            session: Async database session
        """
        super().__init__(Supplier, session)
    
    async def get_by_code(self, code: str) -> Optional[Supplier]:
        """Get supplier by code.
        
        Args:
            code: Supplier code (e.g., SUP001)
            
        Returns:
            Supplier if found, None otherwise
        """
        stmt = select(Supplier).where(
            Supplier.code == code,
            Supplier.is_deleted == False
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[Supplier]:
        """Get supplier by email.
        
        Args:
            email: Supplier email
            
        Returns:
            Supplier if found, None otherwise
        """
        stmt = select(Supplier).where(
            Supplier.email == email.lower(),
            Supplier.is_deleted == False
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_tax_code(self, tax_code: str) -> Optional[Supplier]:
        """Get supplier by tax code.
        
        Args:
            tax_code: Tax code
            
        Returns:
            Supplier if found, None otherwise
        """
        stmt = select(Supplier).where(
            Supplier.tax_code == tax_code,
            Supplier.is_deleted == False
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_active(self, skip: int = 0, limit: int = 100) -> list[Supplier]:
        """Get all active suppliers.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active suppliers
        """
        stmt = select(Supplier).where(
            Supplier.is_active == True,
            Supplier.is_deleted == False
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def search_by_name(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Supplier]:
        """Search suppliers by name.
        
        Args:
            search_term: Search term for name
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching suppliers
        """
        stmt = select(Supplier).where(
            Supplier.name.ilike(f"%{search_term}%"),
            Supplier.is_deleted == False
        ).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def exists_by_code(self, code: str, exclude_id: Optional[int] = None) -> bool:
        """Check if supplier with code exists.
        
        Args:
            code: Supplier code to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if exists, False otherwise
        """
        stmt = select(Supplier).where(
            Supplier.code == code,
            Supplier.is_deleted == False
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Supplier.id != exclude_id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if supplier with email exists.
        
        Args:
            email: Email to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if exists, False otherwise
        """
        stmt = select(Supplier).where(
            Supplier.email == email.lower(),
            Supplier.is_deleted == False
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Supplier.id != exclude_id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def exists_by_tax_code(
        self,
        tax_code: str,
        exclude_id: Optional[int] = None
    ) -> bool:
        """Check if supplier with tax code exists.
        
        Args:
            tax_code: Tax code to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if exists, False otherwise
        """
        if not tax_code:
            return False
        
        stmt = select(Supplier).where(
            Supplier.tax_code == tax_code,
            Supplier.is_deleted == False
        )
        
        if exclude_id is not None:
            stmt = stmt.where(Supplier.id != exclude_id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
