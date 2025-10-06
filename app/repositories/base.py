"""Base repository with common CRUD operations.

This module provides a generic repository pattern implementation that can be
inherited by specific repositories to get common CRUD functionality.
"""

from typing import Any, Generic, TypeVar

from sqlalchemy import Select, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

# Type variable for model class
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository providing common CRUD operations.
    
    This generic repository can be inherited by specific repositories
    to get basic CRUD operations for free.
    
    Example:
        ```python
        class UserRepository(BaseRepository[User]):
            def __init__(self, db: AsyncSession):
                super().__init__(User, db)
        ```
    """
    
    def __init__(self, model: type[ModelType], db: AsyncSession):
        """Initialize repository.
        
        Args:
            model: SQLAlchemy model class.
            db: Database session.
        """
        self.model = model
        self.db = db
    
    async def get(self, id: int) -> ModelType | None:
        """Get a single record by ID.
        
        Args:
            id: Record ID.
            
        Returns:
            Model instance or None if not found.
        """
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: Any = None,
    ) -> tuple[list[ModelType], int]:
        """Get multiple records with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            order_by: Column to order by.
            
        Returns:
            Tuple of (list of records, total count).
        """
        # Build base query
        query = select(self.model)
        
        # Add ordering
        if order_by is not None:
            query = query.order_by(order_by)
        else:
            query = query.order_by(self.model.id)
        
        # Get total count
        count_query = select(func.count()).select_from(self.model)
        total = await self.db.scalar(count_query) or 0
        
        # Add pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        items = list(result.scalars().all())
        
        return items, total
    
    async def create(self, obj_in: dict[str, Any]) -> ModelType:
        """Create a new record.
        
        Args:
            obj_in: Dictionary of field values.
            
        Returns:
            Created model instance.
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        id: int,
        obj_in: dict[str, Any],
    ) -> ModelType | None:
        """Update an existing record.
        
        Args:
            id: Record ID to update.
            obj_in: Dictionary of fields to update.
            
        Returns:
            Updated model instance or None if not found.
        """
        # Check if record exists
        db_obj = await self.get(id)
        if db_obj is None:
            return None
        
        # Update fields
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def delete(self, id: int) -> bool:
        """Delete a record by ID.
        
        Args:
            id: Record ID to delete.
            
        Returns:
            True if deleted, False if not found.
        """
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        return result.rowcount > 0
    
    async def exists(self, id: int) -> bool:
        """Check if a record exists.
        
        Args:
            id: Record ID to check.
            
        Returns:
            True if exists, False otherwise.
        """
        result = await self.db.execute(
            select(func.count()).where(self.model.id == id)
        )
        count = result.scalar_one()
        return count > 0
    
    async def count(self, **filters: Any) -> int:
        """Count records with optional filters.
        
        Args:
            **filters: Keyword arguments for filtering.
            
        Returns:
            Number of records matching filters.
        """
        query = select(func.count()).select_from(self.model)
        
        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def bulk_create(self, objs_in: list[dict[str, Any]]) -> list[ModelType]:
        """Create multiple records in bulk.
        
        Args:
            objs_in: List of dictionaries with field values.
            
        Returns:
            List of created model instances.
        """
        db_objs = [self.model(**obj) for obj in objs_in]
        self.db.add_all(db_objs)
        await self.db.flush()
        
        # Refresh all objects
        for obj in db_objs:
            await self.db.refresh(obj)
        
        return db_objs
    
    async def bulk_update(self, updates: list[dict[str, Any]]) -> int:
        """Update multiple records in bulk.
        
        Each dict in updates must contain 'id' field.
        
        Args:
            updates: List of dictionaries with 'id' and fields to update.
            
        Returns:
            Number of records updated.
        """
        if not updates:
            return 0
        
        result = await self.db.execute(
            update(self.model),
            updates,
        )
        return result.rowcount
    
    async def bulk_delete(self, ids: list[int]) -> int:
        """Delete multiple records by IDs.
        
        Args:
            ids: List of record IDs to delete.
            
        Returns:
            Number of records deleted.
        """
        if not ids:
            return 0
        
        result = await self.db.execute(
            delete(self.model).where(self.model.id.in_(ids))
        )
        return result.rowcount
    
    def _build_query(self, **filters: Any) -> Select:
        """Build a base query with filters.
        
        Args:
            **filters: Keyword arguments for filtering.
            
        Returns:
            SQLAlchemy Select query.
        """
        query = select(self.model)
        
        for key, value in filters.items():
            if hasattr(self.model, key):
                if value is None:
                    query = query.where(getattr(self.model, key).is_(None))
                else:
                    query = query.where(getattr(self.model, key) == value)
        
        return query
