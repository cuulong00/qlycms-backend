"""Item repository for database operations."""

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.item import Item
from app.repositories.base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    """Repository for item database operations.
    
    Extends BaseRepository with item-specific queries.
    """
    
    def __init__(self, db: AsyncSession):
        """Initialize repository.
        
        Args:
            db: Database session.
        """
        super().__init__(Item, db)
    
    async def get_by_title(self, title: str) -> Item | None:
        """Get item by title.
        
        Args:
            title: Item title.
            
        Returns:
            Item instance or None if not found.
        """
        result = await self.db.execute(
            select(Item).where(Item.title == title)
        )
        return result.scalar_one_or_none()
    
    async def get_with_owner(self, item_id: int) -> Item | None:
        """Get item with owner information loaded.
        
        Args:
            item_id: Item ID.
            
        Returns:
            Item instance with owner or None if not found.
        """
        result = await self.db.execute(
            select(Item)
            .options(joinedload(Item.owner))
            .where(Item.id == item_id)
        )
        return result.unique().scalar_one_or_none()
    
    async def get_by_owner(
        self,
        owner_id: int,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> tuple[list[Item], int]:
        """Get items by owner with pagination.
        
        Args:
            owner_id: Owner user ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            active_only: If True, return only active items.
            
        Returns:
            Tuple of (list of items, total count).
        """
        query = select(Item).where(Item.owner_id == owner_id)
        count_query = select(func.count()).where(Item.owner_id == owner_id)
        
        if active_only:
            query = query.where(Item.is_active == True)
            count_query = count_query.where(Item.is_active == True)
        
        # Get total count
        total = await self.db.scalar(count_query) or 0
        
        # Add pagination and ordering
        query = query.order_by(Item.created_at.desc()).offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        items = list(result.scalars().all())
        
        return items, total
    
    async def get_active_items(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Item], int]:
        """Get all active items with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of items, total count).
        """
        query = select(Item).where(Item.is_active == True)
        
        # Get total count
        count_query = select(func.count()).where(Item.is_active == True)
        total = await self.db.scalar(count_query) or 0
        
        # Add pagination and ordering
        query = query.order_by(Item.created_at.desc()).offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        items = list(result.scalars().all())
        
        return items, total
    
    async def search_by_title(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Item], int]:
        """Search items by title (case-insensitive).
        
        Args:
            search_term: Search term to match against titles.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of items, total count).
        """
        search_pattern = f"%{search_term}%"
        query = select(Item).where(Item.title.ilike(search_pattern))
        
        # Get total count
        count_query = select(func.count()).where(Item.title.ilike(search_pattern))
        total = await self.db.scalar(count_query) or 0
        
        # Add pagination and ordering
        query = query.order_by(Item.created_at.desc()).offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        items = list(result.scalars().all())
        
        return items, total
    
    async def toggle_active(self, item_id: int) -> Item | None:
        """Toggle item active status.
        
        Args:
            item_id: Item ID.
            
        Returns:
            Updated item or None if not found.
        """
        item = await self.get(item_id)
        if item is None:
            return None
        
        item.is_active = not item.is_active
        await self.db.flush()
        await self.db.refresh(item)
        return item
    
    async def get_stats(self, owner_id: int | None = None) -> dict[str, Any]:
        """Get item statistics.
        
        Args:
            owner_id: Optional owner ID to filter stats.
            
        Returns:
            Dictionary with item statistics.
        """
        # Build base query
        if owner_id:
            total = await self.count(owner_id=owner_id)
            active = await self.count(owner_id=owner_id, is_active=True)
        else:
            total = await self.count()
            active = await self.count(is_active=True)
        
        # Items by owner
        items_by_owner_query = select(
            Item.owner_id,
            func.count(Item.id).label("count"),
        ).group_by(Item.owner_id)
        
        if owner_id:
            items_by_owner_query = items_by_owner_query.where(
                Item.owner_id == owner_id
            )
        
        result = await self.db.execute(items_by_owner_query)
        items_by_owner = {row.owner_id: row.count for row in result}
        
        return {
            "total_items": total,
            "active_items": active,
            "inactive_items": total - active,
            "items_by_owner": items_by_owner,
        }
