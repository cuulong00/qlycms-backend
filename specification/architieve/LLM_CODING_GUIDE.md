# 🤖 LLM Coding Assistant Instructions
# Universal instructions for AI coding assistants (Cursor, GitHub Copilot, ChatGPT, Claude, etc.)

## 📋 Project Context

This is a **production-ready FastAPI backend** following **Clean Architecture** principles with:

- **FastAPI 0.115+** - Modern async web framework
- **SQLAlchemy 2.0** - Async ORM with type safety  
- **Pydantic V2** - Data validation (5-50x faster with Rust core)
- **Alembic 1.16+** - Database migrations
- **Python 3.11+** - Latest Python features

---

## 🎯 Core Principles

When assisting with this codebase, ALWAYS:

1. ✅ **Follow Clean Architecture** - Respect layer boundaries
2. ✅ **Use async/await** - All I/O operations must be async
3. ✅ **Type Everything** - No `Any`, use proper type hints
4. ✅ **Inject Dependencies** - Use FastAPI's `Depends()`
5. ✅ **Validate with Pydantic** - Never trust user input
6. ✅ **Test Your Code** - Write tests for new features
7. ✅ **Document APIs** - Add docstrings and OpenAPI examples
8. ✅ **Handle Errors Properly** - Use appropriate HTTP status codes
9. ✅ **Keep It DRY** - Don't repeat code, use base classes
10. ✅ **Security First** - Never expose sensitive data

---

## 📁 Architecture Layers

```
┌─────────────────────────────────────────┐
│   API Layer (app/api/)                  │  ← FastAPI routes, deps, middleware
├─────────────────────────────────────────┤
│   Service Layer (app/services/)         │  ← Business logic ONLY
├─────────────────────────────────────────┤
│   Domain Layer (app/domain/)            │  ← Entities, interfaces
├─────────────────────────────────────────┤
│   Repository Layer (app/repositories/)  │  ← Database operations ONLY
├─────────────────────────────────────────┤
│   Model Layer (app/models/)             │  ← SQLAlchemy models
└─────────────────────────────────────────┘
```

### Layer Responsibilities

**API Layer** (`app/api/`)
- Handle HTTP requests/responses
- Input validation (Pydantic)
- Authentication/Authorization
- Dependency injection
- ❌ NO business logic here!

**Service Layer** (`app/services/`)
- Business logic and rules
- Orchestrate multiple repositories
- Transaction management
- ✅ This is where logic lives!

**Repository Layer** (`app/repositories/`)
- Database queries ONLY
- CRUD operations
- Complex queries
- ❌ NO business logic here!

**Model Layer** (`app/models/`)
- SQLAlchemy ORM models
- Database schema definition
- Relationships

---

## 🔧 Code Patterns

### Pattern 1: API Endpoint (app/api/v1/resources.py)

```python
from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.schemas.resource import ResourceCreate, ResourceResponse
from app.services.resource_service import ResourceService
from app.api.deps import get_resource_service, get_current_user

router = APIRouter()

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    data: ResourceCreate,  # Pydantic validation
    service: Annotated[ResourceService, Depends(get_resource_service)],  # DI
    current_user: Annotated[dict, Depends(get_current_user)]  # Auth
) -> ResourceResponse:
    """Create a new resource."""
    return await service.create(data)
```

### Pattern 2: Service (app/services/resource_service.py)

```python
from fastapi import HTTPException, status
from app.schemas.resource import ResourceCreate, ResourceResponse
from app.repositories.resource import ResourceRepository

class ResourceService:
    def __init__(self, repository: ResourceRepository):
        self.repository = repository
    
    async def create(self, data: ResourceCreate) -> ResourceResponse:
        # Business logic here
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resource already exists"
            )
        
        resource = await self.repository.create(data.model_dump())
        return ResourceResponse.model_validate(resource)
```

### Pattern 3: Repository (app/repositories/resource.py)

```python
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.resource import Resource
from app.repositories.base import BaseRepository

class ResourceRepository(BaseRepository[Resource]):
    def __init__(self, db: AsyncSession):
        super().__init__(Resource, db)
    
    async def get_by_name(self, name: str) -> Optional[Resource]:
        result = await self.db.execute(
            select(Resource).where(Resource.name == name)
        )
        return result.scalar_one_or_none()
```

### Pattern 4: Pydantic Schema (app/schemas/resource.py)

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ResourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)

class ResourceResponse(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
```

### Pattern 5: SQLAlchemy Model (app/models/resource.py)

```python
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, IDMixin, TimestampMixin

class Resource(Base, IDMixin, TimestampMixin):
    __tablename__ = "resources"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
```

---

## 🚫 Anti-Patterns to AVOID

### ❌ DON'T: Put business logic in routes

```python
# BAD ❌
@router.post("/users/")
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Business logic in route - BAD!
    if await db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(400, "Email exists")
    
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    return user
```

```python
# GOOD ✅
@router.post("/users/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)]
):
    return await service.create_user(user_data)
```

### ❌ DON'T: Use synchronous code

```python
# BAD ❌
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
```

```python
# GOOD ✅
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### ❌ DON'T: Skip type hints

```python
# BAD ❌
async def create_user(data, db):
    user = User(**data)
    db.add(user)
    await db.commit()
    return user
```

```python
# GOOD ✅
async def create_user(
    data: UserCreate,
    db: AsyncSession
) -> User:
    user = User(**data.model_dump())
    db.add(user)
    await db.commit()
    return user
```

### ❌ DON'T: Use Pydantic V1 syntax

```python
# BAD ❌ (Pydantic V1)
class User(BaseModel):
    name: str
    
    class Config:
        orm_mode = True
```

```python
# GOOD ✅ (Pydantic V2)
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
```

### ❌ DON'T: Use SQLAlchemy 1.x syntax

```python
# BAD ❌ (SQLAlchemy 1.x)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
```

```python
# GOOD ✅ (SQLAlchemy 2.0)
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
```

---

## 📝 Quick Reference

### Common Imports

```python
# FastAPI
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

# SQLAlchemy 2.0
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Pydantic V2
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Project
from app.core.config import settings
from app.api.deps import get_db, get_current_user
```

### Status Codes

```python
status.HTTP_200_OK              # GET success
status.HTTP_201_CREATED         # POST success
status.HTTP_204_NO_CONTENT      # DELETE success
status.HTTP_400_BAD_REQUEST     # Validation error
status.HTTP_401_UNAUTHORIZED    # Not authenticated
status.HTTP_403_FORBIDDEN       # Not authorized
status.HTTP_404_NOT_FOUND       # Resource not found
status.HTTP_409_CONFLICT        # Duplicate/conflict
status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation error
status.HTTP_500_INTERNAL_SERVER_ERROR  # Server error
```

### Database Operations

```python
# Get one
result = await db.execute(select(Model).where(Model.id == id))
item = result.scalar_one_or_none()

# Get many
result = await db.execute(select(Model).limit(10))
items = result.scalars().all()

# Create
item = Model(**data)
db.add(item)
await db.flush()
await db.refresh(item)

# Update
result = await db.execute(
    update(Model).where(Model.id == id).values(**data)
)
await db.commit()

# Delete
result = await db.execute(delete(Model).where(Model.id == id))
await db.commit()
```

### Alembic Commands

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Show current
alembic current

# Show history
alembic history
```

---

## 🎯 When Creating New Features

Follow this checklist:

1. **Schema First** (`app/schemas/`) - Define DTOs
2. **Model** (`app/models/`) - Define database table (if new)
3. **Migration** - Run `alembic revision --autogenerate`
4. **Repository** (`app/repositories/`) - Implement data access
5. **Service** (`app/services/`) - Implement business logic
6. **API** (`app/api/v1/`) - Create endpoints
7. **Dependency** (`app/api/deps.py`) - Add DI function
8. **Tests** (`tests/`) - Write integration tests
9. **Documentation** - Update README/docs if needed

---

## 💡 Pro Tips

### Tip 1: Use Base Classes

Don't repeat common CRUD operations. Use `BaseRepository` and `BaseService`.

### Tip 2: Eager Load Relationships

```python
# Use selectinload for better performance
result = await db.execute(
    select(User).options(selectinload(User.posts))
)
```

### Tip 3: Pagination

```python
# Always paginate list endpoints
from app.schemas.common import PaginationParams, PaginatedResponse

async def list_items(
    pagination: Annotated[PaginationParams, Depends()]
):
    items, total = await service.list_items(pagination)
    return PaginatedResponse(items=items, total=total, ...)
```

### Tip 4: Logging

```python
from app.core.logging import logger

logger.info(f"User {user_id} created")
logger.error(f"Failed to process: {error}")
```

### Tip 5: Environment Variables

```python
# Never hardcode, use settings
from app.core.config import settings

database_url = settings.DATABASE_URL
secret_key = settings.SECRET_KEY
```

---

## 🧪 Testing

### Test Structure

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_resource(client: AsyncClient, auth_headers: dict):
    """Test creating a resource."""
    # Arrange
    data = {"name": "Test", "description": "Test desc"}
    
    # Act
    response = await client.post("/api/v1/resources/", json=data, headers=auth_headers)
    
    # Assert
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == data["name"]
    assert "id" in result
```

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/integration/test_api/test_users.py::test_create_user

# With markers
pytest -m unit
pytest -m integration
```

---

## 🔐 Security Checklist

- [ ] Never commit `.env` files
- [ ] Always hash passwords (`passlib[bcrypt]`)
- [ ] Use JWT tokens with expiration
- [ ] Validate ALL user input (Pydantic)
- [ ] Use parameterized queries (SQLAlchemy handles this)
- [ ] Implement rate limiting
- [ ] Use HTTPS in production
- [ ] Set proper CORS policies
- [ ] Sanitize error messages in production
- [ ] Use `Depends(get_current_user)` for auth

---

## 📚 Documentation

- Document all public APIs with docstrings
- Add examples to Pydantic schemas
- Use FastAPI's automatic OpenAPI docs
- Keep README.md updated
- Document non-obvious business logic

---

## 🆘 Common Issues & Solutions

### Issue: "RuntimeError: asyncio.run() cannot be called from a running event loop"

**Solution:** Use `async with` context managers, don't mix sync and async.

### Issue: "DetachedInstanceError"

**Solution:** Use `expire_on_commit=False` in session config or refresh objects.

### Issue: "PendingRollbackError"

**Solution:** Properly handle exceptions with try/except and rollback.

### Issue: Import errors

**Solution:** Check Python path and use absolute imports from `app.*`.

---

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)

---

## 🤝 Collaboration Guidelines

### When Suggesting Code:

1. **Follow existing patterns** - Check how it's done elsewhere
2. **Be complete** - Don't suggest fragments, provide working code
3. **Add type hints** - Always include proper types
4. **Include error handling** - Don't forget edge cases
5. **Write tests** - Suggest tests for new features
6. **Document** - Add docstrings and comments
7. **Explain** - Tell WHY, not just WHAT

### When Refactoring:

1. **Keep tests passing** - Don't break existing functionality
2. **One thing at a time** - Don't mix refactoring with new features
3. **Maintain patterns** - Keep consistency with existing code
4. **Test thoroughly** - Ensure nothing breaks

---

## ✨ Code Quality Standards

- **Black** formatter (line length: 88)
- **isort** for import sorting
- **mypy** for type checking
- **pylint** for linting
- **pytest** for testing (80%+ coverage target)

---

**Remember: Clean code is NOT about being clever, it's about being CLEAR and MAINTAINABLE! 🚀**
