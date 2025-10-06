"""User endpoints."""

from fastapi import APIRouter, status

from app.api.deps import CurrentAdmin, CurrentUser, UserSvc
from app.schemas.base import PaginatedResponse, PaginationParams
from app.schemas.common import Message
from app.schemas.user import UserListResponse, UserProfileUpdate, UserRead, UserRoleUpdate

router = APIRouter()


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get the currently authenticated user's profile",
)
async def get_current_user_profile(
    current_user: CurrentUser,
) -> UserRead:
    """Get current user profile.
    
    Args:
        current_user: Current authenticated user.
        
    Returns:
        UserRead: Current user data.
    """
    return UserRead.model_validate(current_user)


@router.patch(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
    description="Update the currently authenticated user's profile",
)
async def update_current_user_profile(
    profile_update: UserProfileUpdate,
    current_user: CurrentUser,
    service: UserSvc,
) -> UserRead:
    """Update current user profile.
    
    Args:
        profile_update: Profile update data.
        current_user: Current authenticated user.
        service: User service instance.
        
    Returns:
        UserRead: Updated user data.
    """
    updated_user = await service.update_profile(current_user.id, profile_update)
    return UserRead.model_validate(updated_user)


@router.get(
    "/",
    response_model=PaginatedResponse[UserListResponse],
    status_code=status.HTTP_200_OK,
    summary="List users",
    description="Get a paginated list of users (admin only)",
)
async def list_users(
    pagination: PaginationParams,
    current_admin: CurrentAdmin,
    service: UserSvc,
) -> PaginatedResponse[UserListResponse]:
    """List all users with pagination (admin only).
    
    Args:
        pagination: Pagination parameters.
        current_admin: Current admin user.
        service: User service instance.
        
    Returns:
        PaginatedResponse: Paginated list of users.
    """
    users, total = await service.get_users(
        skip=pagination.skip,
        limit=pagination.limit,
    )
    
    return PaginatedResponse[UserListResponse](
        items=[UserListResponse.model_validate(user) for user in users],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Get a specific user by ID (admin only)",
)
async def get_user(
    user_id: int,
    current_admin: CurrentAdmin,
    service: UserSvc,
) -> UserRead:
    """Get user by ID (admin only).
    
    Args:
        user_id: User ID.
        current_admin: Current admin user.
        service: User service instance.
        
    Returns:
        UserRead: User data.
    """
    user = await service.get_user(user_id)
    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}/role",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update user role",
    description="Update a user's role (admin only)",
)
async def update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    current_admin: CurrentAdmin,
    service: UserSvc,
) -> UserRead:
    """Update user role (admin only).
    
    Args:
        user_id: User ID.
        role_update: Role update data.
        current_admin: Current admin user.
        service: User service instance.
        
    Returns:
        UserRead: Updated user data.
    """
    updated_user = await service.update_role(user_id, role_update, current_admin)
    return UserRead.model_validate(updated_user)


@router.post(
    "/{user_id}/deactivate",
    response_model=Message,
    status_code=status.HTTP_200_OK,
    summary="Deactivate user",
    description="Deactivate a user account (admin only)",
)
async def deactivate_user(
    user_id: int,
    current_admin: CurrentAdmin,
    service: UserSvc,
) -> Message:
    """Deactivate user account (admin only).
    
    Args:
        user_id: User ID.
        current_admin: Current admin user.
        service: User service instance.
        
    Returns:
        Message: Success message.
    """
    await service.deactivate_user(user_id, current_admin)
    return Message(message="User deactivated successfully")


@router.post(
    "/{user_id}/activate",
    response_model=Message,
    status_code=status.HTTP_200_OK,
    summary="Activate user",
    description="Activate a user account (admin only)",
)
async def activate_user(
    user_id: int,
    current_admin: CurrentAdmin,
    service: UserSvc,
) -> Message:
    """Activate user account (admin only).
    
    Args:
        user_id: User ID.
        current_admin: Current admin user.
        service: User service instance.
        
    Returns:
        Message: Success message.
    """
    await service.activate_user(user_id, current_admin)
    return Message(message="User activated successfully")
