"""
FastAPI-Users configuration và UserManager.
Quản lý user authentication, registration, và user lifecycle events.
"""

import logging
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User manager for handling user operations.
    
    Extends FastAPI-Users BaseUserManager với custom logic cho YCMS:
    - Password reset
    - Email verification
    - User registration validation
    - Audit logging for user events
    
    Attributes:
        reset_password_token_secret: Secret for password reset tokens
        verification_token_secret: Secret for email verification tokens
        reset_password_token_lifetime_seconds: Token lifetime (1 hour)
        verification_token_lifetime_seconds: Token lifetime (24 hours)
    """
    
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY
    reset_password_token_lifetime_seconds = 3600  # 1 hour
    verification_token_lifetime_seconds = 86400  # 24 hours

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """Callback after successful user registration.
        
        Args:
            user: The newly registered user
            request: The HTTP request (optional)
        """
        logger.info(
            f"User {user.id} ({user.email}) has registered. "
            f"User type: {user.user_type}, Role: {user.role}"
        )
        
        # TODO: Send welcome email
        # TODO: Create audit log entry
        # TODO: Send notification to admins for supplier user registration

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        """Callback after forgot password request.
        
        Args:
            user: The user requesting password reset
            token: The reset token
            request: The HTTP request (optional)
        """
        logger.info(f"User {user.id} ({user.email}) has requested password reset")
        
        # TODO: Send password reset email with token
        # TODO: Create audit log entry

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        """Callback after email verification request.
        
        Args:
            user: The user requesting email verification
            token: The verification token
            request: The HTTP request (optional)
        """
        logger.info(
            f"User {user.id} ({user.email}) has requested email verification"
        )
        
        # TODO: Send verification email with token
        # TODO: Create audit log entry

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """Callback after successful email verification.
        
        Args:
            user: The user who verified their email
            request: The HTTP request (optional)
        """
        logger.info(f"User {user.id} ({user.email}) has verified their email")
        
        # TODO: Send welcome email
        # TODO: Create audit log entry

    async def on_after_update(
        self,
        user: User,
        update_dict: dict,
        request: Optional[Request] = None,
    ) -> None:
        """Callback after user profile update.
        
        Args:
            user: The updated user
            update_dict: Dictionary of updated fields
            request: The HTTP request (optional)
        """
        logger.info(
            f"User {user.id} ({user.email}) has been updated. "
            f"Updated fields: {', '.join(update_dict.keys())}"
        )
        
        # TODO: Create audit log entry with changes
        # TODO: Send notification if critical fields changed (email, role, etc.)

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response = None,
    ) -> None:
        """Callback after successful login.
        
        Args:
            user: The user who logged in
            request: The HTTP request (optional)
            response: The HTTP response (optional)
        """
        logger.info(
            f"User {user.id} ({user.email}) has logged in. "
            f"User type: {user.user_type}, Role: {user.role}"
        )
        
        # TODO: Update last_login_at timestamp
        # TODO: Create audit log entry
        # TODO: Check for pending notifications

    async def validate_password(
        self, password: str, user: User
    ) -> None:
        """Validate password strength.
        
        Args:
            password: The password to validate
            user: The user (to check against user info)
            
        Raises:
            InvalidPasswordException: If password is invalid
        """
        # Call parent validation first
        await super().validate_password(password, user)
        
        # Additional YCMS-specific validation
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        if password.lower() in user.email.lower():
            raise ValueError("Password cannot contain email address")
        
        if user.first_name and password.lower() in user.first_name.lower():
            raise ValueError("Password cannot contain first name")
        
        if user.last_name and password.lower() in user.last_name.lower():
            raise ValueError("Password cannot contain last name")


async def get_user_db(
    session = Depends(lambda: None)  # Will be replaced with actual session dependency
) -> SQLAlchemyUserDatabase:
    """Get SQLAlchemy user database instance.
    
    Args:
        session: Database session from dependency injection
        
    Yields:
        SQLAlchemyUserDatabase instance
    """
    # Import here to avoid circular dependency
    from app.db.session import get_db
    
    async for db_session in get_db():
        yield SQLAlchemyUserDatabase(db_session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> UserManager:
    """Get UserManager instance.
    
    Args:
        user_db: User database from dependency injection
        
    Yields:
        UserManager instance
    """
    yield UserManager(user_db)
