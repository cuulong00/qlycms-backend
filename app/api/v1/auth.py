"""
Authentication routes.
Cung cấp các endpoints cho register, login, logout, verify email, forgot password.
"""

from fastapi import APIRouter

from app.core.auth import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Register routes (POST /auth/register)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

# Login/Logout routes
# POST /auth/login - Login with email and password
# POST /auth/logout - Logout (invalidate token)
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

# Verify email routes
# POST /auth/request-verify-token - Request verification email
# POST /auth/verify - Verify email with token
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

# Password reset routes
# POST /auth/forgot-password - Request password reset
# POST /auth/reset-password - Reset password with token
router.include_router(
    fastapi_users.get_reset_password_router(),
)

# User management routes
# GET /auth/me - Get current user
# PATCH /auth/me - Update current user
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)
