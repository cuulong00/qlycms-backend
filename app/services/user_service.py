"""User service for business logic."""

from typing import Any

from fastapi import HTTPException, status

from app.core.security import get_password_hash, verify_password
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserProfileUpdate, UserRoleUpdate, UserUpdate


class UserService:
    """Service for user business logic.
    
    This service handles all user-related business logic including
    validation, authorization checks, and orchestrating repository calls.
    """
    
    def __init__(self, repository: UserRepository):
        """Initialize service.
        
        Args:
            repository: User repository instance.
        """
        self.repository = repository
    
    async def get_user(self, user_id: int) -> Any:
        """Get user by ID.
        
        Args:
            user_id: User ID.
            
        Returns:
            User instance.
            
        Raises:
            HTTPException: If user not found.
        """
        user = await self.repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    
    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Any], int]:
        """Get list of users with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of users, total count).
        """
        return await self.repository.get_multi(skip=skip, limit=limit)
    
    async def get_active_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Any], int]:
        """Get list of active users.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of active users, total count).
        """
        return await self.repository.get_active_users(skip=skip, limit=limit)
    
    async def update_profile(
        self,
        user_id: int,
        profile_update: UserProfileUpdate,
    ) -> Any:
        """Update user profile.
        
        Args:
            user_id: User ID.
            profile_update: Profile update data.
            
        Returns:
            Updated user instance.
            
        Raises:
            HTTPException: If user not found.
        """
        # Get user
        user = await self.get_user(user_id)
        
        # Update fields
        update_data = profile_update.model_dump(exclude_unset=True)
        updated_user = await self.repository.update(user_id, update_data)
        
        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return updated_user
    
    async def update_role(
        self,
        user_id: int,
        role_update: UserRoleUpdate,
        current_user: Any,
    ) -> Any:
        """Update user role (admin only).
        
        Args:
            user_id: User ID.
            role_update: Role update data.
            current_user: Current authenticated user.
            
        Returns:
            Updated user instance.
            
        Raises:
            HTTPException: If not authorized or user not found.
        """
        # Check if current user is admin
        if current_user.role not in ["admin", "super_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update user roles",
            )
        
        # Prevent users from changing their own role
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change your own role",
            )
        
        # Update role
        updated_user = await self.repository.update_role(
            user_id,
            role_update.role,
        )
        
        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return updated_user
    
    async def deactivate_user(
        self,
        user_id: int,
        current_user: Any,
    ) -> bool:
        """Deactivate a user account (admin only).
        
        Args:
            user_id: User ID to deactivate.
            current_user: Current authenticated user.
            
        Returns:
            True if deactivated successfully.
            
        Raises:
            HTTPException: If not authorized or user not found.
        """
        # Check if current user is admin
        if current_user.role not in ["admin", "super_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to deactivate users",
            )
        
        # Prevent users from deactivating themselves
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account",
            )
        
        # Deactivate user
        success = await self.repository.deactivate(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return success
    
    async def activate_user(
        self,
        user_id: int,
        current_user: Any,
    ) -> bool:
        """Activate a user account (admin only).
        
        Args:
            user_id: User ID to activate.
            current_user: Current authenticated user.
            
        Returns:
            True if activated successfully.
            
        Raises:
            HTTPException: If not authorized or user not found.
        """
        # Check if current user is admin
        if current_user.role not in ["admin", "super_admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to activate users",
            )
        
        # Activate user
        success = await self.repository.activate(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return success
    
    async def get_user_stats(self) -> dict[str, Any]:
        """Get user statistics.
        
        Returns:
            Dictionary with user statistics.
        """
        return await self.repository.get_stats()
    
    async def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
    ) -> bool:
        """Change user password.
        
        Args:
            user_id: User ID.
            current_password: Current password.
            new_password: New password.
            
        Returns:
            True if password changed successfully.
            
        Raises:
            HTTPException: If current password is incorrect.
        """
        # Get user
        user = await self.get_user(user_id)
        
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password",
            )
        
        # Update password
        new_hashed_password = get_password_hash(new_password)
        await self.repository.update(
            user_id,
            {"hashed_password": new_hashed_password},
        )
        
        return True
