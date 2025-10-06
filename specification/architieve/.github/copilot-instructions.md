# GitHub Copilot Instructions - FastAPI Backend Project

## Project Overview
This is a production-ready FastAPI backend using Clean Architecture with:
- **FastAPI 0.115+** - Modern Python web framework
- **SQLAlchemy 2.0** - Async ORM with type safety
- **Pydantic V2** - Data validation with Rust-powered performance
- **Alembic** - Database migration tool
- **Python 3.11+** - Latest Python features

## Code Generation Guidelines

### 1. Always Follow Clean Architecture
When generating code, respect these layers:
- **API Layer** (`app/api/`) - Only handle HTTP concerns
- **Service Layer** (`app/services/`) - Business logic lives here
- **Repository Layer** (`app/repositories/`) - Data access only
- **Model Layer** (`app/models/`) - Database schema definitions

### 2. Type Hints Are Mandatory
```python
# ✅ DO THIS
async def get_user(user_id: int, db: AsyncSession) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# ❌ DON'T DO THIS
async def get_user(user_id, db):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### 3. Use Async/Await Everywhere
```python
# ✅ DO THIS - Async database operations
async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

# ❌ DON'T DO THIS - Synchronous operations
def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    db.add(user)
    db.flush()
    db.refresh(user)
    return user
```

### 4. Pydantic V2 Syntax
```python
# ✅ DO THIS - Pydantic V2
from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True
    )
    
    email: str = Field(..., max_length=255)
    username: str = Field(..., min_length=3, max_length=50)

# ❌ DON'T DO THIS - Pydantic V1 (deprecated)
class UserCreate(BaseModel):
    email: str
    username: str
    
    class Config:
        orm_mode = True
```

### 5. SQLAlchemy 2.0 Style
```python
# ✅ DO THIS - SQLAlchemy 2.0
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

# ❌ DON'T DO THIS - SQLAlchemy 1.x style
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
```

### 6. FastAPI Route Pattern
```python
# ✅ DO THIS - With dependency injection and proper types
from typing import Annotated
from fastapi import APIRouter, Depends, status

router = APIRouter()

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    """Create a new user."""
    return await service.create_user(user_data)

# ❌ DON'T DO THIS - No dependency injection, no types
@router.post("/users/")
async def create_user(user_data: UserCreate):
    # Business logic directly in route
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    return user
```

### 7. Repository Pattern
```python
# ✅ DO THIS - Separate repository with interface
from typing import Protocol, Optional

class IUserRepository(Protocol):
    async def get_by_id(self, user_id: int) -> Optional[User]: ...
    async def get_by_email(self, email: str) -> Optional[User]: ...
    async def create(self, user_data: dict) -> User: ...

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

### 8. Service Layer Pattern
```python
# ✅ DO THIS - Business logic in service
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Validate business rules
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = hashed_password
        del user_dict["password"]
        
        user = await self.repository.create(user_dict)
        return UserResponse.model_validate(user)
```

## Common Code Snippets

### Creating a New CRUD Endpoint Set

**1. Schema (app/schemas/item.py):**
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
```

**2. Model (app/models/item.py):**
```python
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, IDMixin, TimestampMixin

class Item(Base, IDMixin, TimestampMixin):
    __tablename__ = "items"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
```

**3. Repository (app/repositories/item.py):**
```python
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.repositories.base import BaseRepository

class ItemRepository(BaseRepository[Item]):
    def __init__(self, db: AsyncSession):
        super().__init__(Item, db)
    
    async def get_by_name(self, name: str) -> Optional[Item]:
        result = await self.db.execute(
            select(Item).where(Item.name == name)
        )
        return result.scalar_one_or_none()
```

**4. Service (app/services/item_service.py):**
```python
from typing import Optional, List
from fastapi import HTTPException, status
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.schemas.common import PaginationParams
from app.repositories.item import ItemRepository

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository
    
    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        # Check if item with same name exists
        existing = await self.repository.get_by_name(item_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item with this name already exists"
            )
        
        item = await self.repository.create(item_data.model_dump())
        return ItemResponse.model_validate(item)
    
    async def get_item(self, item_id: int) -> ItemResponse:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        return ItemResponse.model_validate(item)
    
    async def list_items(
        self, 
        pagination: PaginationParams
    ) -> tuple[List[ItemResponse], int]:
        items, total = await self.repository.get_multi(
            skip=pagination.skip,
            limit=pagination.limit
        )
        return [ItemResponse.model_validate(item) for item in items], total
    
    async def update_item(
        self, 
        item_id: int, 
        item_data: ItemUpdate
    ) -> ItemResponse:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        
        update_data = item_data.model_dump(exclude_unset=True)
        updated_item = await self.repository.update(item_id, update_data)
        return ItemResponse.model_validate(updated_item)
    
    async def delete_item(self, item_id: int) -> bool:
        deleted = await self.repository.delete(item_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        return True
```

**5. API Routes (app/api/v1/items.py):**
```python
from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.item_service import ItemService
from app.api.deps import get_item_service, get_current_active_user

router = APIRouter()

@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item"
)
async def create_item(
    item_data: ItemCreate,
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> ItemResponse:
    """Create a new item with the provided data."""
    return await service.create_item(item_data)

@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID"
)
async def get_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_item_service)]
) -> ItemResponse:
    """Get a specific item by its ID."""
    return await service.get_item(item_id)

@router.get(
    "/",
    response_model=PaginatedResponse[ItemResponse],
    summary="List all items"
)
async def list_items(
    pagination: Annotated[PaginationParams, Depends()],
    service: Annotated[ItemService, Depends(get_item_service)]
) -> PaginatedResponse[ItemResponse]:
    """Get a paginated list of all items."""
    items, total = await service.list_items(pagination)
    return PaginatedResponse(
        items=items,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit
    )

@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update item"
)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> ItemResponse:
    """Update an existing item."""
    return await service.update_item(item_id, item_data)

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item"
)
async def delete_item(
    item_id: int,
    service: Annotated[ItemService, Depends(get_item_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> None:
    """Delete an item by its ID."""
    await service.delete_item(item_id)
```

**6. Dependency (app/api/deps.py):**
```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.repositories.item import ItemRepository
from app.services.item_service import ItemService

async def get_item_service(
    db: Annotated[AsyncSession, Depends(get_db_session)]
) -> ItemService:
    """Get item service with dependencies."""
    repository = ItemRepository(db)
    return ItemService(repository)
```

## Migration Commands

```bash
# Create new migration
alembic revision --autogenerate -m "Add items table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current version
alembic current

# Show history
alembic history --verbose
```

## Testing Pattern

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, db_session: AsyncSession):
    """Test creating a new item."""
    # Arrange
    item_data = {
        "name": "Test Item",
        "description": "Test Description"
    }
    
    # Act
    response = await client.post("/api/v1/items/", json=item_data)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient):
    """Test getting non-existent item."""
    response = await client.get("/api/v1/items/999999")
    assert response.status_code == 404
```

## Remember These Key Points

1. **Always use async/await** for database operations
2. **Type everything** - use type hints for all functions and variables
3. **Separate concerns** - Keep layers independent
4. **Use Pydantic V2 syntax** - `model_config`, `model_validate`, etc.
5. **Use SQLAlchemy 2.0 syntax** - `Mapped`, `mapped_column`, `select()`
6. **Inject dependencies** - Use FastAPI's `Depends()`
7. **Handle errors properly** - Use appropriate HTTP status codes
8. **Write tests** - For every new feature
9. **Document APIs** - Use docstrings and FastAPI's documentation features
10. **Follow the existing patterns** - Consistency is key

## When Suggesting Code

- Always check the existing codebase patterns first
- Suggest complete implementations, not fragments
- Include proper error handling
- Add type hints
- Include docstrings
- Suggest tests when appropriate
- Follow the Clean Architecture layers
- Use async/await
- Use the latest syntax for all libraries
