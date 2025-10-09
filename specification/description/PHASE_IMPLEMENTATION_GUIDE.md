# HƯỚNG DẪN TRIỂN KHAI THEO PHASE
## Phase-by-Phase Implementation Guide for LLM Auto-Coding

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Purpose**: Guide LLM để tự động code theo từng phase  
**Target**: Production-ready code  

---

## 🎯 MỤC TIÊU TỔNG THỂ

Đặc tả này được thiết kế để **LLM có thể tự động generate code production-ready** cho toàn bộ hệ thống YCMS. Mỗi phase được chia nhỏ thành các task cụ thể với:

✅ **Input rõ ràng**: Những gì cần có trước khi bắt đầu  
✅ **Output cụ thể**: Những gì cần tạo ra  
✅ **Acceptance Criteria**: Tiêu chí để verify code đúng  
✅ **Code Templates**: Mẫu code chuẩn để follow  
✅ **Test Cases**: Test cases phải pass  

---

## 📦 STRUCTURE & DEPENDENCIES

### Technology Stack
```yaml
Backend:
  Framework: FastAPI 0.118.0
  ORM: SQLAlchemy 2.0.43 (async)
  Migration: Alembic 1.16.5
  Validation: Pydantic 2.11.10
  Auth: FastAPI-Users 14.0.1
  Authorization: Casbin 1.37.6
  
Database:
  Primary: PostgreSQL 15+
  Cache: Redis 7+
  
Testing:
  Framework: Pytest 8.3.0
  Async: Pytest-asyncio 0.24.0
  Coverage: > 80%
  
Code Quality:
  Formatter: Black
  Linter: Pylint
  Type Checker: Mypy
  
DevOps:
  Container: Docker + Docker Compose
  CI/CD: GitHub Actions
```

### Project Structure Reference
```
app/
├── api/               # API Routes (Presentation Layer)
│   ├── deps.py       # Dependencies
│   ├── errors/       # Error handlers
│   └── v1/           # API v1
│       ├── router.py
│       ├── auth.py
│       ├── users.py
│       └── ...
├── core/             # Core configuration
│   ├── config.py     # Settings
│   ├── security.py   # JWT, password
│   └── events.py     # Lifecycle
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── repositories/     # Data access layer
├── services/         # Business logic
└── db/              # Database config
```

---

## 🚀 PHASE 1: FOUNDATION (Week 1-2)

### Objectives
- Setup project structure chuẩn production
- Configure FastAPI + SQLAlchemy 2.0 + Alembic
- Implement authentication với FastAPI-Users
- Setup authorization với Casbin
- Docker environment
- CI/CD pipeline

---

### SPRINT 1.1: Core Infrastructure Setup (Week 1)

#### Task 1.1.1: Project Initialization

**Input Requirements:**
- Python 3.11+
- PostgreSQL 15+
- Redis 7+ (optional for this sprint)

**Expected Output:**
```
backend/
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── pytest.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   └── services/
├── alembic/
│   ├── env.py
│   └── versions/
└── tests/
    ├── conftest.py
    └── test_health.py
```

**Code Generation Instructions:**

1. **Create requirements.txt**
```plaintext
# Core
fastapi[standard]==0.118.0
pydantic==2.11.10
pydantic-settings==2.7.0
sqlalchemy[asyncio]==2.0.43
alembic==1.16.5
uvicorn[standard]==0.37.0

# Database drivers
asyncpg==0.30.0
psycopg2-binary==2.9.9

# Authentication & Authorization
fastapi-users[sqlalchemy]==14.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-casbin==1.37.6
casbin-sqlalchemy-adapter==1.5.0

# Utilities
python-multipart==0.0.17
email-validator==2.2.0
httpx==0.28.0

# Development
pytest==8.3.0
pytest-asyncio==0.24.0
pytest-cov==4.1.0
black==24.4.2
pylint==3.2.0
mypy==1.10.0
```

2. **Create .env.example**
```env
# Application
PROJECT_NAME=YCMS Backend
VERSION=1.0.0
API_V1_PREFIX=/api/v1
DEBUG=true

# Server
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-secret-key-here-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=ycms_db

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

3. **Create app/core/config.py**
```python
"""
Application configuration using Pydantic Settings
Auto-loads from .env file
"""

from typing import List, Optional
from pydantic import Field, PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Project
    PROJECT_NAME: str = Field(default="YCMS Backend")
    VERSION: str = Field(default="1.0.0")
    API_V1_PREFIX: str = Field(default="/api/v1")
    DEBUG: bool = Field(default=False)
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # Security
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Database
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_NAME: str = Field(...)
    DB_ECHO: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)
    
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v, info: ValidationInfo):
        if isinstance(v, str):
            return v
        values = info.data
        return (
            f"postgresql+asyncpg://{values.get('DB_USER')}:"
            f"{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:"
            f"{values.get('DB_PORT')}/{values.get('DB_NAME')}"
        )


settings = Settings()
```

4. **Create app/db/session.py**
```python
"""
SQLAlchemy 2.0 async session configuration
"""

from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config import settings


# Create async engine
engine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

5. **Create app/models/base.py**
```python
"""
SQLAlchemy base model with common mixins
"""

from datetime import datetime
from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """Base class for all models"""
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class IDMixin:
    """Mixin for ID field"""
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )


class TimestampMixin:
    """Mixin for timestamp fields"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
```

6. **Create app/main.py**
```python
"""
FastAPI application factory
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    yield
    # Shutdown
    print("Shutting down...")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_application()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
```

7. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ycms_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_NAME=ycms_db
      - SECRET_KEY=your-secret-key-change-in-production-min-32-chars
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

8. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

9. **Create alembic.ini**
```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/ycms_db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
```

10. **Create alembic/env.py**
```python
"""
Alembic migration environment
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.config import settings
from app.models.base import Base

# Import all models
from app.models import *  # noqa

config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in async mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Acceptance Criteria:**
- [ ] Project structure matches specification
- [ ] All dependencies installed successfully
- [ ] FastAPI app starts without errors
- [ ] Health check endpoint returns 200
- [ ] Docker containers start successfully
- [ ] Database connection successful
- [ ] OpenAPI docs accessible at `/api/v1/docs`

**Testing:**
```bash
# Test locally
python -m pytest tests/ -v

# Test with Docker
docker-compose up -d
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/docs
```

**Success Metrics:**
- All tests pass
- Health check returns `{"status": "healthy"}`
- OpenAPI docs load successfully
- Zero warnings in logs

---

### SPRINT 1.2: Authentication & Authorization (Week 2)

#### Task 1.2.1: User Model & FastAPI-Users Integration

**Objective**: Implement complete authentication system với FastAPI-Users

**Code Generation Instructions:**

1. **Create app/models/user.py**

*(Xem file ENTITY_SPECIFICATION.md section 1 để lấy full code)*

Key points:
- Extend `SQLAlchemyBaseUserTable[int]`
- Add custom fields: `user_type`, `role`, `supplier_id`, etc.
- Add enums: `UserType`, `UserRole`
- Add relationships

2. **Create migration**

```bash
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

3. **Create app/schemas/user.py**

*(Xem file ENTITY_SPECIFICATION.md section 1)*

4. **Create app/core/users.py - FastAPI-Users setup**

```python
"""
FastAPI-Users configuration
"""

from typing import Optional
from fastapi import Depends, Request
from fastapi_users import FastAPIUsers, BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db_session
from app.models.user import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User manager"""
    
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
    
    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[None] = None,
    ):
        """Update last_login timestamp"""
        from datetime import datetime
        user.last_login = datetime.utcnow()


async def get_user_db(session: AsyncSession = Depends(get_db_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


bearer_transport = BearerTransport(tokenUrl="auth/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
```

5. **Create app/api/v1/auth.py**

```python
"""
Authentication routes
"""

from fastapi import APIRouter
from app.core.users import auth_backend, fastapi_users
from app.schemas.user import UserRead, UserCreate, UserUpdate

router = APIRouter()

# Auth routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

# Register routes
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# User management
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
```

6. **Update app/api/v1/router.py**

```python
"""
Main API router
"""

from fastapi import APIRouter
from app.api.v1 import auth

api_router = APIRouter()

api_router.include_router(auth.router)
```

7. **Update app/main.py to include router**

```python
# Add after creating app
from app.api.v1.router import api_router

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
```

8. **Create tests/test_auth.py**

```python
"""
Test authentication endpoints
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123",
            "user_type": "aladdin",
            "role": "aladdin_staff",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Test user login"""
    # First register
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "SecurePass123",
            "user_type": "aladdin",
            "role": "aladdin_staff",
            "first_name": "Login",
            "last_name": "Test",
        },
    )
    
    # Then login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "SecurePass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_headers):
    """Test getting current user"""
    response = await client.get(
        "/api/v1/users/me",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "id" in data
```

**Acceptance Criteria:**
- [ ] User can register with valid data
- [ ] User can login and receive JWT token
- [ ] Protected endpoints require authentication
- [ ] Invalid credentials return 401
- [ ] Password is hashed in database
- [ ] All tests pass (> 80% coverage)

---

#### Task 1.2.2: Casbin RBAC Authorization

**Objective**: Implement role-based access control với Casbin

**Code Generation Instructions:**

1. **Create app/core/casbin/model.conf**

```ini
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

2. **Create app/core/authorization.py**

```python
"""
Casbin authorization
"""

import casbin
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.users import current_active_user
from app.db.session import get_db_session
from app.models.user import User


# Initialize enforcer (simplified, in production use adapter)
def get_enforcer():
    """Get Casbin enforcer"""
    enforcer = casbin.Enforcer("app/core/casbin/model.conf")
    
    # Load policies (in production, load from database)
    # Format: role, resource, action
    enforcer.add_policy("super_admin", "*", "*")
    enforcer.add_policy("aladdin_admin", "procurement_requests", "*")
    enforcer.add_policy("aladdin_admin", "delivery_notes", "read")
    enforcer.add_policy("aladdin_staff", "procurement_requests", "create")
    enforcer.add_policy("aladdin_staff", "procurement_requests", "read")
    enforcer.add_policy("supplier_admin", "procurement_requests", "read")
    enforcer.add_policy("supplier_admin", "delivery_notes", "*")
    enforcer.add_policy("supplier_staff", "procurement_requests", "read")
    enforcer.add_policy("supplier_staff", "delivery_notes", "read")
    
    # Add role inheritance
    enforcer.add_role_for_user("1", "super_admin")  # User ID 1 is super admin
    
    return enforcer


def require_permission(resource: str, action: str):
    """Dependency to check permission"""
    async def check_permission(
        user: User = Depends(current_active_user),
        enforcer: casbin.Enforcer = Depends(get_enforcer)
    ):
        # Super admin bypass
        if user.is_superuser:
            return user
        
        # Check permission
        allowed = enforcer.enforce(user.role.value, resource, action)
        
        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have permission to {action} {resource}"
            )
        
        return user
    
    return check_permission
```

3. **Create example protected endpoint**

```python
# app/api/v1/protected_example.py
"""
Example protected endpoints
"""

from fastapi import APIRouter, Depends
from app.core.authorization import require_permission
from app.models.user import User

router = APIRouter()


@router.get("/procurement-requests")
async def list_procurement_requests(
    user: User = Depends(require_permission("procurement_requests", "read"))
):
    """List procurement requests - requires read permission"""
    return {
        "message": "List of procurement requests",
        "user": user.email
    }


@router.post("/procurement-requests")
async def create_procurement_request(
    user: User = Depends(require_permission("procurement_requests", "create"))
):
    """Create procurement request - requires create permission"""
    return {
        "message": "Procurement request created",
        "user": user.email
    }
```

**Acceptance Criteria:**
- [ ] Different roles have different permissions
- [ ] Super admin can access everything
- [ ] Aladdin staff can create/read YCMS
- [ ] Supplier staff can only read YCMS
- [ ] Unauthorized access returns 403
- [ ] All permission tests pass

---

## 📈 PROGRESS TRACKING

### Phase 1 Checklist

**Sprint 1.1: Core Infrastructure** ✅ / ⏳
- [ ] Project structure created
- [ ] FastAPI application running
- [ ] Database connection working
- [ ] Docker environment setup
- [ ] Health check endpoint
- [ ] OpenAPI docs accessible

**Sprint 1.2: Authentication** ✅ / ⏳
- [ ] User model created
- [ ] FastAPI-Users integrated
- [ ] Register endpoint working
- [ ] Login endpoint working
- [ ] JWT tokens issued
- [ ] Protected endpoints working
- [ ] Casbin RBAC setup
- [ ] Permission checks working
- [ ] All tests passing (>80% coverage)

---

## 🎯 NEXT STEPS

Sau khi hoàn thành Phase 1, tiếp tục với:

1. **Phase 2: Master Data** (Week 3-4)
   - Supplier management
   - Product management
   - Restaurant management
   - Product mapping

2. **Phase 3: YCMS Management** (Week 5-7)
   - YCMS CRUD operations
   - YCMS workflow
   - Email notifications

*(Chi tiết trong file PHASE_2_MASTER_DATA.md)*

---

**Document Status**: ✅ Phase 1 Complete  
**Next Document**: PHASE_2_MASTER_DATA.md  
**Version**: 1.0  
**Last Updated**: 2025-10-08
