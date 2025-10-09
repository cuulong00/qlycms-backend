"""Test configuration and fixtures."""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.session import get_db
from app.main import app
from app.models.base import Base
from app.models.user import User, UserRole, UserType

# Test database URL (SQLite in memory)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Create async engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session factory
    async_session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Yield session
    async with async_session_maker() as session:
        yield session
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
def client(test_db: AsyncSession) -> Generator[TestClient, None, None]:
    """Create test client with database override."""
    
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client."""
    from httpx import ASGITransport
    from app.api.deps import get_db_session
    
    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_db
    
    # Override get_db_session directly
    app.dependency_overrides[get_db_session] = override_get_db_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_aladdin_admin(test_db: AsyncSession) -> User:
    """Create sample Aladdin admin user for testing."""
    from app.core.security import get_password_hash
    
    user = User(
        email="admin@aladdin.com",
        hashed_password=get_password_hash("password123"),
        user_type=UserType.ALADDIN,
        role=UserRole.ALADDIN_ADMIN,
        first_name="Admin",
        last_name="User",
        is_active=True,
        is_verified=True,
    )
    
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    return user


@pytest_asyncio.fixture
async def sample_aladdin_staff(test_db: AsyncSession) -> User:
    """Create sample Aladdin staff user for testing."""
    from app.core.security import get_password_hash
    
    user = User(
        email="staff@aladdin.com",
        hashed_password=get_password_hash("password123"),
        user_type=UserType.ALADDIN,
        role=UserRole.ALADDIN_STAFF,
        first_name="Staff",
        last_name="User",
        is_active=True,
        is_verified=True,
    )
    
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    return user


@pytest_asyncio.fixture
async def sample_supplier_admin(test_db: AsyncSession, sample_supplier) -> User:
    """Create sample supplier admin user for testing."""
    from app.core.security import get_password_hash
    
    user = User(
        email="supplier@example.com",
        hashed_password=get_password_hash("password123"),
        user_type=UserType.SUPPLIER,
        role=UserRole.SUPPLIER_ADMIN,
        first_name="Supplier",
        last_name="Admin",
        supplier_id=sample_supplier.id,
        is_active=True,
        is_verified=True,
    )
    
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    
    return user


@pytest_asyncio.fixture
async def auth_headers_aladdin_admin(
    async_client: AsyncClient, sample_aladdin_admin: User
) -> dict[str, str]:
    """Get authentication headers for Aladdin admin."""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": sample_aladdin_admin.email,
            "password": "password123",
        },
    )
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def auth_headers_supplier_admin(
    async_client: AsyncClient, sample_supplier_admin: User
) -> dict[str, str]:
    """Get authentication headers for supplier admin."""
    response = await async_client.post(
        "/api/v1/auth/login",
        data={
            "username": sample_supplier_admin.email,
            "password": "password123",
        },
    )
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def sample_supplier(test_db: AsyncSession):
    """Create sample supplier for testing."""
    from app.models.supplier import Supplier
    
    supplier = Supplier(
        code="SUP001",
        name="Test Supplier Co., Ltd.",
        email="contact@testsupplier.com",
        phone="0123456789",
        tax_code="0123456789",
        address="123 Test Street, Test City",
        contact_person="John Doe",
        contact_phone="0987654321",
        contact_email="john@testsupplier.com",
        description="A test supplier for unit testing",
        is_active=True,
    )
    
    test_db.add(supplier)
    await test_db.commit()
    await test_db.refresh(supplier)
    
    return supplier


@pytest_asyncio.fixture
async def multiple_suppliers(test_db: AsyncSession):
    """Create multiple suppliers for pagination testing."""
    from app.models.supplier import Supplier
    
    suppliers = []
    for i in range(1, 11):  # Create 10 suppliers
        supplier = Supplier(
            code=f"SUP{i+100:03d}",
            name=f"Supplier {i}",
            email=f"supplier{i}@example.com",
            phone=f"012345678{i}",
            tax_code=f"TAX{i:09d}" if i % 2 == 0 else None,
            address=f"{i} Test Street",
            contact_person=f"Contact {i}",
            contact_phone=f"098765432{i}",
            contact_email=f"contact{i}@supplier{i}.com",
            is_active=i % 2 == 1,  # Odd numbers are active
        )
        test_db.add(supplier)
        suppliers.append(supplier)
    
    await test_db.commit()
    for supplier in suppliers:
        await test_db.refresh(supplier)
    
    return suppliers


@pytest_asyncio.fixture
async def sample_supplier_with_users(test_db: AsyncSession):
    """Create supplier with associated users for deletion testing."""
    from app.core.security import get_password_hash
    from app.models.supplier import Supplier
    
    supplier = Supplier(
        code="SUP200",
        name="Supplier with Users",
        email="withusers@supplier.com",
        is_active=True,
    )
    test_db.add(supplier)
    await test_db.flush()
    
    # Create a user for this supplier
    user = User(
        email="user@supplier200.com",
        hashed_password=get_password_hash("password123"),
        user_type=UserType.SUPPLIER,
        role=UserRole.SUPPLIER_ADMIN,
        first_name="Supplier",
        last_name="User",
        supplier_id=supplier.id,
        is_active=True,
        is_verified=True,
    )
    test_db.add(user)
    
    await test_db.commit()
    await test_db.refresh(supplier)
    await test_db.refresh(user)
    
    return supplier


@pytest_asyncio.fixture
async def inactive_supplier(test_db: AsyncSession):
    """Create inactive supplier for activation testing."""
    from app.models.supplier import Supplier
    
    supplier = Supplier(
        code="SUP999",
        name="Inactive Supplier",
        email="inactive@supplier.com",
        is_active=False,
    )
    
    test_db.add(supplier)
    await test_db.commit()
    await test_db.refresh(supplier)
    
    return supplier


@pytest_asyncio.fixture
async def admin_token_headers(
    async_client: AsyncClient,
    sample_aladdin_admin: User,
) -> dict[str, str]:
    """Get authentication headers for admin user."""
    from app.core.security import create_access_token
    
    token = create_access_token(subject=sample_aladdin_admin.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def user_token_headers(
    async_client: AsyncClient,
    sample_aladdin_staff: User,
) -> dict[str, str]:
    """Get authentication headers for regular user."""
    from app.core.security import create_access_token
    
    token = create_access_token(subject=sample_aladdin_staff.id)
    return {"Authorization": f"Bearer {token}"}
