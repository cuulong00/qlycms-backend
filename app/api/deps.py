"""Dependency injection for FastAPI routes.

This module provides dependency injection functions for:
- Database sessions
- Current user authentication
- Service instances
- Repository instances
- Permission checks
"""

from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.services.item_service import ItemService
from app.services.user_service import UserService

# Security scheme for JWT Bearer token
security = HTTPBearer()


# Database dependencies
async def get_db_session() -> AsyncSession:
    """Get database session dependency.
    
    This is a wrapper around get_db for clearer naming.
    
    Yields:
        AsyncSession: Database session.
    """
    async for session in get_db():
        yield session


DBSession = Annotated[AsyncSession, Depends(get_db_session)]


# Repository dependencies
def get_user_repository(db: DBSession) -> UserRepository:
    """Get user repository dependency.
    
    Args:
        db: Database session.
        
    Returns:
        UserRepository instance.
    """
    return UserRepository(db)


def get_item_repository(db: DBSession) -> ItemRepository:
    """Get item repository dependency.
    
    Args:
        db: Database session.
        
    Returns:
        ItemRepository instance.
    """
    return ItemRepository(db)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
ItemRepo = Annotated[ItemRepository, Depends(get_item_repository)]


# Service dependencies
def get_user_service(repository: UserRepo) -> UserService:
    """Get user service dependency.
    
    Args:
        repository: User repository instance.
        
    Returns:
        UserService instance.
    """
    return UserService(repository)


def get_item_service(repository: ItemRepo) -> ItemService:
    """Get item service dependency.
    
    Args:
        repository: Item repository instance.
        
    Returns:
        ItemService instance.
    """
    return ItemService(repository)


UserSvc = Annotated[UserService, Depends(get_user_service)]
ItemSvc = Annotated[ItemService, Depends(get_item_service)]


# Authentication dependencies
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    repository: UserRepo,
) -> Any:
    """Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials with JWT token.
        repository: User repository instance.
        
    Returns:
        Current user instance.
        
    Raises:
        HTTPException: If token is invalid or user not found.
    """
    try:
        # Decode and verify token
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = await repository.get(int(user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )
        
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


async def get_current_active_user(
    current_user: Annotated[Any, Depends(get_current_user)],
) -> Any:
    """Get current active user.
    
    Args:
        current_user: Current user from get_current_user.
        
    Returns:
        Current active user instance.
        
    Raises:
        HTTPException: If user is not active.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


async def get_current_superuser(
    current_user: Annotated[Any, Depends(get_current_user)],
) -> Any:
    """Get current superuser.
    
    Args:
        current_user: Current user from get_current_user.
        
    Returns:
        Current superuser instance.
        
    Raises:
        HTTPException: If user is not a superuser.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )
    return current_user


async def get_current_admin(
    current_user: Annotated[Any, Depends(get_current_user)],
) -> Any:
    """Get current admin user (admin or super_admin role).
    
    Args:
        current_user: Current user from get_current_user.
        
    Returns:
        Current admin user instance.
        
    Raises:
        HTTPException: If user is not an admin.
    """
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


# Type aliases for dependency injection
CurrentUser = Annotated[Any, Depends(get_current_user)]
CurrentActiveUser = Annotated[Any, Depends(get_current_active_user)]
CurrentSuperUser = Annotated[Any, Depends(get_current_superuser)]
CurrentAdmin = Annotated[Any, Depends(get_current_admin)]


# Optional current user (for endpoints that can work with or without auth)
async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        HTTPBearer(auto_error=False)
    ),
    repository: UserRepo = Depends(get_user_repository),
) -> Any | None:
    """Get current user if authenticated, None otherwise.
    
    Use this for endpoints that can work with or without authentication.
    
    Args:
        credentials: HTTP Bearer credentials (optional).
        repository: User repository instance.
        
    Returns:
        Current user instance or None.
    """
    if credentials is None:
        return None
    
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if user_id is None:
            return None
        
        user = await repository.get(int(user_id))
        return user if user and user.is_active else None
        
    except Exception:
        return None


CurrentUserOptional = Annotated[Any | None, Depends(get_current_user_optional)]
