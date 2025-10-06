"""User repository for database operations."""

from datetime import datetime, timezone
from typing import Any

from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for user database operations.
    
    Extends BaseRepository with user-specific queries.
    """
    
    def __init__(self, db: AsyncSession):
        """Initialize repository.
        
        Args:
            db: Database session.
        """
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email address.
        
        Args:
            email: User email address.
            
        Returns:
            User instance or None if not found.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_oauth(
        self,
        provider: str,
        oauth_id: str,
    ) -> User | None:
        """Get user by OAuth provider and ID.
        
        Args:
            provider: OAuth provider name (google, github, etc.).
            oauth_id: OAuth provider user ID.
            
        Returns:
            User instance or None if not found.
        """
        result = await self.db.execute(
            select(User).where(
                User.oauth_provider == provider,
                User.oauth_id == oauth_id,
            )
        )
        return result.scalar_one_or_none()
    
    async def get_active_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[User], int]:
        """Get all active users with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of users, total count).
        """
        query = select(User).where(User.is_active == True)
        
        # Get total count
        count_query = select(func.count()).where(User.is_active == True)
        total = await self.db.scalar(count_query) or 0
        
        # Add pagination and ordering
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        users = list(result.scalars().all())
        
        return users, total
    
    async def get_by_role(
        self,
        role: str,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[User], int]:
        """Get users by role with pagination.
        
        Args:
            role: User role to filter by.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            Tuple of (list of users, total count).
        """
        query = select(User).where(User.role == role)
        
        # Get total count
        count_query = select(func.count()).where(User.role == role)
        total = await self.db.scalar(count_query) or 0
        
        # Add pagination and ordering
        query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        users = list(result.scalars().all())
        
        return users, total
    
    async def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp.
        
        Args:
            user_id: User ID.
            
        Returns:
            True if updated, False if user not found.
        """
        user = await self.get(user_id)
        if user is None:
            return False
        
        user.last_login_at = datetime.now(timezone.utc)
        await self.db.flush()
        return True
    
    async def update_role(self, user_id: int, new_role: str) -> User | None:
        """Update user's role.
        
        Args:
            user_id: User ID.
            new_role: New role name.
            
        Returns:
            Updated user or None if not found.
        """
        return await self.update(user_id, {"role": new_role})
    
    async def deactivate(self, user_id: int) -> bool:
        """Deactivate a user account.
        
        Args:
            user_id: User ID.
            
        Returns:
            True if deactivated, False if user not found.
        """
        user = await self.get(user_id)
        if user is None:
            return False
        
        user.is_active = False
        await self.db.flush()
        return True
    
    async def activate(self, user_id: int) -> bool:
        """Activate a user account.
        
        Args:
            user_id: User ID.
            
        Returns:
            True if activated, False if user not found.
        """
        user = await self.get(user_id)
        if user is None:
            return False
        
        user.is_active = True
        await self.db.flush()
        return True
    
    async def get_stats(self) -> dict[str, Any]:
        """Get user statistics.
        
        Returns:
            Dictionary with user statistics.
        """
        # Total users
        total = await self.count()
        
        # Active users
        active = await self.count(is_active=True)
        
        # Verified users
        verified = await self.count(is_verified=True)
        
        # Users by role
        roles_query = select(
            User.role,
            func.count(User.id).label("count"),
        ).group_by(User.role)
        roles_result = await self.db.execute(roles_query)
        users_by_role = {row.role: row.count for row in roles_result}
        
        return {
            "total_users": total,
            "active_users": active,
            "verified_users": verified,
            "users_by_role": users_by_role,
        }


def get_user_db(session: AsyncSession) -> SQLAlchemyUserDatabase:
    """Get FastAPI-Users database adapter.
    
    This is used by FastAPI-Users for authentication operations.
    
    Args:
        session: Database session.
        
    Returns:
        SQLAlchemyUserDatabase instance.
    """
    return SQLAlchemyUserDatabase(session, User)
