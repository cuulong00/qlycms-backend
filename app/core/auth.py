"""
Authentication backend configuration cho FastAPI-Users.
Định nghĩa JWT strategy và authentication backends.
"""

from typing import Optional

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.core.config import settings
from app.core.users import get_user_manager
from app.models.user import User

# Bearer token transport (Authorization: Bearer <token>)
bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    """Get JWT authentication strategy.
    
    Returns:
        JWTStrategy instance configured with app settings
        
    JWT Configuration:
        - Secret: From settings.SECRET_KEY
        - Lifetime: 1 hour (3600 seconds)
        - Algorithm: HS256
        - Token URL: auth/login
    """
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=3600,  # 1 hour
        algorithm="HS256",
    )


# Authentication backend combining transport + strategy
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


# FastAPI-Users instance - main entry point for auth
fastapi_users = FastAPIUsers[User, int](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)


# Dependency for getting current active user
current_active_user = fastapi_users.current_user(active=True)


# Dependency for getting current verified user
current_verified_user = fastapi_users.current_user(active=True, verified=True)


# Dependency for getting current superuser
current_superuser = fastapi_users.current_user(active=True, superuser=True)


# Optional current user (returns None if not authenticated)
optional_current_user = fastapi_users.current_user(active=True, optional=True)
