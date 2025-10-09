"""Main router for API v1.

This module combines all v1 routes into a single router.
"""

from fastapi import APIRouter

from app.api.v1 import auth, health, items, suppliers, users
from app.core.constants import API_V1_PREFIX

# Create main router for v1
router = APIRouter(prefix=API_V1_PREFIX)

# Include auth routes (no prefix, auth routes have their own prefix)
router.include_router(auth.router)

# Include all route modules
router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

router.include_router(
    items.router,
    prefix="/items",
    tags=["Items"],
)

router.include_router(
    suppliers.router,
    prefix="/suppliers",
    tags=["Suppliers"],
)
