# 🚀 Quick Start Snippets for LLM Assistants

## Creating a New CRUD Resource

When user asks: "Create CRUD endpoints for {resource_name}"

### Step 1: Schema (app/schemas/{resource_name}.py)

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class {ResourceName}Base(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class {ResourceName}Create({ResourceName}Base):
    pass

class {ResourceName}Update(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

class {ResourceName}Response({ResourceName}Base):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
```

### Step 2: Model (app/models/{resource_name}.py)

```python
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, IDMixin, TimestampMixin

class {ResourceName}(Base, IDMixin, TimestampMixin):
    __tablename__ = "{resource_name}s"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
```

### Step 3: Repository (app/repositories/{resource_name}.py)

```python
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.{resource_name} import {ResourceName}
from app.repositories.base import BaseRepository

class {ResourceName}Repository(BaseRepository[{ResourceName}]):
    def __init__(self, db: AsyncSession):
        super().__init__({ResourceName}, db)
    
    async def get_by_name(self, name: str) -> Optional[{ResourceName}]:
        result = await self.db.execute(
            select({ResourceName}).where({ResourceName}.name == name)
        )
        return result.scalar_one_or_none()
```

### Step 4: Service (app/services/{resource_name}_service.py)

```python
from typing import List
from fastapi import HTTPException, status
from app.schemas.{resource_name} import {ResourceName}Create, {ResourceName}Update, {ResourceName}Response
from app.schemas.common import PaginationParams
from app.repositories.{resource_name} import {ResourceName}Repository

class {ResourceName}Service:
    def __init__(self, repository: {ResourceName}Repository):
        self.repository = repository
    
    async def create(self, data: {ResourceName}Create) -> {ResourceName}Response:
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="{ResourceName} already exists"
            )
        item = await self.repository.create(data.model_dump())
        return {ResourceName}Response.model_validate(item)
    
    async def get(self, id: int) -> {ResourceName}Response:
        item = await self.repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="{ResourceName} not found"
            )
        return {ResourceName}Response.model_validate(item)
    
    async def list(self, pagination: PaginationParams) -> tuple[List[{ResourceName}Response], int]:
        items, total = await self.repository.get_multi(
            skip=pagination.skip, limit=pagination.limit
        )
        return [{ResourceName}Response.model_validate(item) for item in items], total
    
    async def update(self, id: int, data: {ResourceName}Update) -> {ResourceName}Response:
        item = await self.repository.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="{ResourceName} not found"
            )
        updated = await self.repository.update(id, data.model_dump(exclude_unset=True))
        return {ResourceName}Response.model_validate(updated)
    
    async def delete(self, id: int) -> bool:
        deleted = await self.repository.delete(id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="{ResourceName} not found"
            )
        return True
```

### Step 5: API Routes (app/api/v1/{resource_name}s.py)

```python
from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.schemas.{resource_name} import {ResourceName}Create, {ResourceName}Update, {ResourceName}Response
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.{resource_name}_service import {ResourceName}Service
from app.api.deps import get_{resource_name}_service, get_current_active_user

router = APIRouter()

@router.post("/", response_model={ResourceName}Response, status_code=status.HTTP_201_CREATED)
async def create_{resource_name}(
    data: {ResourceName}Create,
    service: Annotated[{ResourceName}Service, Depends(get_{resource_name}_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> {ResourceName}Response:
    """Create a new {resource_name}."""
    return await service.create(data)

@router.get("/{{{resource_name}_id}}", response_model={ResourceName}Response)
async def get_{resource_name}(
    {resource_name}_id: int,
    service: Annotated[{ResourceName}Service, Depends(get_{resource_name}_service)]
) -> {ResourceName}Response:
    """Get {resource_name} by ID."""
    return await service.get({resource_name}_id)

@router.get("/", response_model=PaginatedResponse[{ResourceName}Response])
async def list_{resource_name}s(
    pagination: Annotated[PaginationParams, Depends()],
    service: Annotated[{ResourceName}Service, Depends(get_{resource_name}_service)]
) -> PaginatedResponse[{ResourceName}Response]:
    """List all {resource_name}s."""
    items, total = await service.list(pagination)
    return PaginatedResponse(items=items, total=total, skip=pagination.skip, limit=pagination.limit)

@router.put("/{{{resource_name}_id}}", response_model={ResourceName}Response)
async def update_{resource_name}(
    {resource_name}_id: int,
    data: {ResourceName}Update,
    service: Annotated[{ResourceName}Service, Depends(get_{resource_name}_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> {ResourceName}Response:
    """Update {resource_name}."""
    return await service.update({resource_name}_id, data)

@router.delete("/{{{resource_name}_id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{resource_name}(
    {resource_name}_id: int,
    service: Annotated[{ResourceName}Service, Depends(get_{resource_name}_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> None:
    """Delete {resource_name}."""
    await service.delete({resource_name}_id)
```

### Step 6: Dependency (app/api/deps.py)

Add this function:

```python
from app.services.{resource_name}_service import {ResourceName}Service
from app.repositories.{resource_name} import {ResourceName}Repository

async def get_{resource_name}_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> {ResourceName}Service:
    """Get {resource_name} service."""
    repository = {ResourceName}Repository(db)
    return {ResourceName}Service(repository)
```

### Step 7: Register Router (app/api/v1/router.py)

```python
from app.api.v1 import {resource_name}s

api_router.include_router(
    {resource_name}s.router,
    prefix="/{resource_name}s",
    tags=["{resource_name}s"]
)
```

### Step 8: Migration

```bash
# Generate migration
alembic revision --autogenerate -m "Add {resource_name}s table"

# Apply migration
alembic upgrade head
```

---

## Quick Database Query Snippets

### Get Single Item

```python
result = await db.execute(select(Model).where(Model.id == id))
item = result.scalar_one_or_none()
```

### Get Multiple Items

```python
result = await db.execute(select(Model).limit(limit).offset(skip))
items = result.scalars().all()
```

### Get with Relationship (Eager Loading)

```python
result = await db.execute(
    select(User).options(selectinload(User.posts)).where(User.id == id)
)
user = result.scalar_one_or_none()
```

### Search with LIKE

```python
result = await db.execute(
    select(Model).where(Model.name.ilike(f"%{search_term}%"))
)
items = result.scalars().all()
```

### Count

```python
total = await db.scalar(select(func.count()).select_from(Model))
```

### Create

```python
item = Model(**data)
db.add(item)
await db.flush()
await db.refresh(item)
return item
```

### Update

```python
result = await db.execute(
    update(Model).where(Model.id == id).values(**data).returning(Model)
)
await db.commit()
return result.scalar_one_or_none()
```

### Delete

```python
result = await db.execute(delete(Model).where(Model.id == id))
await db.commit()
return result.rowcount > 0
```

---

## Quick Test Snippets

### Basic Test

```python
@pytest.mark.asyncio
async def test_create_{resource_name}(client: AsyncClient, auth_headers: dict):
    data = {"name": "Test", "description": "Test description"}
    response = await client.post("/api/v1/{resource_name}s/", json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
```

### Test Not Found

```python
@pytest.mark.asyncio
async def test_get_{resource_name}_not_found(client: AsyncClient):
    response = await client.get("/api/v1/{resource_name}s/999999")
    assert response.status_code == 404
```

### Test Validation Error

```python
@pytest.mark.asyncio
async def test_create_{resource_name}_invalid_data(client: AsyncClient, auth_headers: dict):
    data = {"name": ""}  # Invalid: name too short
    response = await client.post("/api/v1/{resource_name}s/", json=data, headers=auth_headers)
    assert response.status_code == 422
```

---

## Common Pydantic Validators

### Email Validation

```python
from pydantic import EmailStr, Field

email: EmailStr = Field(..., description="Email address")
```

### String Length

```python
username: str = Field(..., min_length=3, max_length=50)
```

### Number Range

```python
age: int = Field(..., ge=0, le=150)  # Greater than or equal, less than or equal
price: float = Field(..., gt=0)  # Greater than
```

### Regex Pattern

```python
phone: str = Field(..., pattern=r"^\+?1?\d{9,15}$")
```

### Custom Validator

```python
from pydantic import field_validator

@field_validator("username")
@classmethod
def username_alphanumeric(cls, v: str) -> str:
    if not v.isalnum():
        raise ValueError("must be alphanumeric")
    return v
```

### Model Validator

```python
from pydantic import model_validator

@model_validator(mode="after")
def check_passwords_match(self) -> "UserCreate":
    if self.password != self.password_confirm:
        raise ValueError("passwords do not match")
    return self
```

---

## SQLAlchemy Relationships

### One-to-Many

```python
# Parent
class User(Base):
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="author")

# Child
class Post(Base):
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
```

### Many-to-Many

```python
# Association table
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True)
)

# Models
class User(Base):
    roles: Mapped[List["Role"]] = relationship(secondary=user_role, back_populates="users")

class Role(Base):
    users: Mapped[List["User"]] = relationship(secondary=user_role, back_populates="roles")
```

---

## Authentication Snippets

### Protected Endpoint

```python
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
) -> UserResponse:
    """Get current authenticated user info."""
    return current_user
```

### Admin Only

```python
async def get_current_admin_user(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)]
) -> UserResponse:
    """Verify user is admin."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user
```

---

## Background Task Snippet

```python
from fastapi import BackgroundTasks

async def send_email(email: str, message: str):
    """Send email in background."""
    # Email sending logic here
    pass

@router.post("/send-email/")
async def trigger_email(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Hello!")
    return {"message": "Email queued"}
```

---

## File Upload Snippet

```python
from fastapi import UploadFile, File

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    current_user: Annotated[dict, Depends(get_current_active_user)]
):
    contents = await file.read()
    # Process file
    return {"filename": file.filename, "size": len(contents)}
```

---

## Pagination Helper

```python
from app.schemas.common import PaginationParams, PaginatedResponse

async def paginate(
    items: list,
    total: int,
    pagination: PaginationParams
) -> PaginatedResponse:
    return PaginatedResponse(
        items=items,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit
    )
```

---

**Use these snippets as templates and customize them for your specific needs!** 🚀
