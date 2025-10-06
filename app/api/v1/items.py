"""Item endpoints."""

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentUser, ItemSvc
from app.schemas.base import PaginatedResponse, PaginationParams
from app.schemas.common import Message
from app.schemas.item import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[ItemListResponse],
    status_code=status.HTTP_200_OK,
    summary="List items",
    description="Get a paginated list of items",
)
async def list_items(
    pagination: PaginationParams,
    active_only: bool = Query(default=False, description="Return only active items"),
    service: ItemSvc = None,
) -> PaginatedResponse[ItemListResponse]:
    """List items with pagination.
    
    Args:
        pagination: Pagination parameters.
        active_only: Filter for active items only.
        service: Item service instance.
        
    Returns:
        PaginatedResponse: Paginated list of items.
    """
    items, total = await service.get_items(
        skip=pagination.skip,
        limit=pagination.limit,
        active_only=active_only,
    )
    
    return PaginatedResponse[ItemListResponse](
        items=[ItemListResponse.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/me",
    response_model=PaginatedResponse[ItemListResponse],
    status_code=status.HTTP_200_OK,
    summary="List my items",
    description="Get a paginated list of items owned by current user",
)
async def list_my_items(
    pagination: PaginationParams,
    active_only: bool = Query(default=False, description="Return only active items"),
    current_user: CurrentUser = None,
    service: ItemSvc = None,
) -> PaginatedResponse[ItemListResponse]:
    """List current user's items with pagination.
    
    Args:
        pagination: Pagination parameters.
        active_only: Filter for active items only.
        current_user: Current authenticated user.
        service: Item service instance.
        
    Returns:
        PaginatedResponse: Paginated list of items.
    """
    items, total = await service.get_user_items(
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit,
        active_only=active_only,
    )
    
    return PaginatedResponse[ItemListResponse](
        items=[ItemListResponse.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/search",
    response_model=PaginatedResponse[ItemListResponse],
    status_code=status.HTTP_200_OK,
    summary="Search items",
    description="Search items by title",
)
async def search_items(
    pagination: PaginationParams,
    q: str = Query(..., min_length=1, description="Search query"),
    service: ItemSvc = None,
) -> PaginatedResponse[ItemListResponse]:
    """Search items by title.
    
    Args:
        pagination: Pagination parameters.
        q: Search query.
        service: Item service instance.
        
    Returns:
        PaginatedResponse: Paginated list of matching items.
    """
    items, total = await service.search_items(
        search_term=q,
        skip=pagination.skip,
        limit=pagination.limit,
    )
    
    return PaginatedResponse[ItemListResponse](
        items=[ItemListResponse.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create item",
    description="Create a new item",
)
async def create_item(
    item_create: ItemCreate,
    current_user: CurrentUser = None,
    service: ItemSvc = None,
) -> ItemResponse:
    """Create a new item.
    
    Args:
        item_create: Item creation data.
        current_user: Current authenticated user.
        service: Item service instance.
        
    Returns:
        ItemResponse: Created item data.
    """
    item = await service.create_item(item_create, current_user)
    return ItemResponse.model_validate(item)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Get item",
    description="Get a specific item by ID",
)
async def get_item(
    item_id: int,
    current_user: CurrentUser = None,
    service: ItemSvc = None,
) -> ItemResponse:
    """Get item by ID.
    
    Args:
        item_id: Item ID.
        current_user: Current authenticated user.
        service: Item service instance.
        
    Returns:
        ItemResponse: Item data.
    """
    item = await service.get_item(item_id, current_user)
    return ItemResponse.model_validate(item)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update item",
    description="Update an existing item",
)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user: CurrentUser = None,
    service: ItemSvc = None,
) -> ItemResponse:
    """Update an existing item.
    
    Args:
        item_id: Item ID.
        item_update: Item update data.
        current_user: Current authenticated user.
        service: Item service instance.
        
    Returns:
        ItemResponse: Updated item data.
    """
    item = await service.update_item(item_id, item_update, current_user)
    return ItemResponse.model_validate(item)


@router.delete(
    "/{item_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
    summary="Delete item",
    description="Delete an existing item",
)
async def delete_item(
    item_id: int,
    current_user: CurrentUser = None,
    service: ItemSvc = None,
) -> Message:
    """Delete an existing item.
    
    Args:
        item_id: Item ID.
        current_user: Current authenticated user.
        service: Item service instance.
        
    Returns:
        Message: Success message.
    """
    await service.delete_item(item_id, current_user)
    return Message(message="Item deleted successfully")


@router.post(
    "/{item_id}/toggle-active",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle item active status",
    description="Toggle an item's active status",
)
async def toggle_item_active(
    item_id: int,
    current_user: CurrentUser = None,
    service: ItemSvc = None,
) -> ItemResponse:
    """Toggle item active status.
    
    Args:
        item_id: Item ID.
        current_user: Current authenticated user.
        service: Item service instance.
        
    Returns:
        ItemResponse: Updated item data.
    """
    item = await service.toggle_item_active(item_id, current_user)
    return ItemResponse.model_validate(item)
