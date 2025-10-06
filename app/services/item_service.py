"""Item service for business logic."""

from typing import Any

from fastapi import HTTPException, status

from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    """Service for item business logic.
    
    This service handles all item-related business logic including
    validation, authorization checks, and orchestrating repository calls.
    """
    
    def __init__(self, repository: ItemRepository):
        """Initialize service.
        
        Args:
            repository: Item repository instance.
        """
        self.repository = repository
    
    async def get_item(self, item_id: int, current_user: Any = None) -> Any:
        """Get item by ID.
        
        Args:
            item_id: Item ID.
            current_user: Current authenticated user (optional).
            
        Returns:
            Item instance.
            
        Raises:
            HTTPException: If item not found or access denied.
        """
        item = await self.repository.get(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found",
            )
        
        # Check ownership if user provided
        if current_user and item.owner_id != current_user.id:
            if current_user.role not in ["admin", "super_admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this item",
                )
        
        return item
    
    async def get_items(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> tuple[list[Any], int]:
        """Get list of items with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            active_only: If True, return only active items.
            
        Returns:
            Tuple of (list of items, total count).
        """
        if active_only:
            return await self.repository.get_active_items(skip=skip, limit=limit)
        return await self.repository.get_multi(skip=skip, limit=limit)
    
    async def get_user_items(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False,
    ) -> tuple[list[Any], int]:
        """Get items owned by a specific user.
        
        Args:
            user_id: Owner user ID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            active_only: If True, return only active items.
            
        Returns:
            Tuple of (list of items, total count).
        """
        return await self.repository.get_by_owner(
            owner_id=user_id,
            skip=skip,
            limit=limit,
            active_only=active_only,
        )
    
    async def create_item(
        self,
        item_create: ItemCreate,
        current_user: Any,
    ) -> Any:
        """Create a new item.
        
        Args:
            item_create: Item creation data.
            current_user: Current authenticated user.
            
        Returns:
            Created item instance.
            
        Raises:
            HTTPException: If item with title already exists.
        """
        # Check if item with same title exists
        existing_item = await self.repository.get_by_title(item_create.title)
        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this title already exists",
            )
        
        # Create item
        item_data = item_create.model_dump()
        item_data["owner_id"] = current_user.id
        
        item = await self.repository.create(item_data)
        return item
    
    async def update_item(
        self,
        item_id: int,
        item_update: ItemUpdate,
        current_user: Any,
    ) -> Any:
        """Update an existing item.
        
        Args:
            item_id: Item ID to update.
            item_update: Item update data.
            current_user: Current authenticated user.
            
        Returns:
            Updated item instance.
            
        Raises:
            HTTPException: If item not found or access denied.
        """
        # Get item and check ownership
        item = await self.get_item(item_id, current_user)
        
        # Only owner or admin can update
        if item.owner_id != current_user.id:
            if current_user.role not in ["admin", "super_admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this item",
                )
        
        # Check if new title conflicts with existing item
        if item_update.title and item_update.title != item.title:
            existing_item = await self.repository.get_by_title(item_update.title)
            if existing_item and existing_item.id != item_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Item with this title already exists",
                )
        
        # Update item
        update_data = item_update.model_dump(exclude_unset=True)
        updated_item = await self.repository.update(item_id, update_data)
        
        if updated_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found",
            )
        
        return updated_item
    
    async def delete_item(
        self,
        item_id: int,
        current_user: Any,
    ) -> bool:
        """Delete an item.
        
        Args:
            item_id: Item ID to delete.
            current_user: Current authenticated user.
            
        Returns:
            True if deleted successfully.
            
        Raises:
            HTTPException: If item not found or access denied.
        """
        # Get item and check ownership
        item = await self.get_item(item_id, current_user)
        
        # Only owner or admin can delete
        if item.owner_id != current_user.id:
            if current_user.role not in ["admin", "super_admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this item",
                )
        
        # Delete item
        success = await self.repository.delete(item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found",
            )
        
        return success
    
    async def toggle_item_active(
        self,
        item_id: int,
        current_user: Any,
    ) -> Any:
        """Toggle item active status.
        
        Args:
            item_id: Item ID.
            current_user: Current authenticated user.
            
        Returns:
            Updated item instance.
            
        Raises:
            HTTPException: If item not found or access denied.
        """
        # Get item and check ownership
        item = await self.get_item(item_id, current_user)
        
        # Only owner or admin can toggle
        if item.owner_id != current_user.id:
            if current_user.role not in ["admin", "super_admin"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to modify this item",
                )
        
        # Toggle active status
        updated_item = await self.repository.toggle_active(item_id)
        if updated_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found",
            )
        
        return updated_item
    
    async def search_items(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Any], int]:
        """Search items by title.
        
        Args:
            search_term: Search term to match against titles.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of items, total count).
        """
        return await self.repository.search_by_title(
            search_term=search_term,
            skip=skip,
            limit=limit,
        )
    
    async def get_item_stats(self, user_id: int | None = None) -> dict[str, Any]:
        """Get item statistics.
        
        Args:
            user_id: Optional user ID to filter stats.
            
        Returns:
            Dictionary with item statistics.
        """
        return await self.repository.get_stats(owner_id=user_id)
