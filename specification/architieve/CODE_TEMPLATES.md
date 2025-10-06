# 🎨 CODE TEMPLATES - FastAPI Backend

This document contains ready-to-use code templates for common patterns in this FastAPI backend project. Copy and adapt these templates to avoid rewriting boilerplate code.

---

## 📋 TABLE OF CONTENTS

1. [Complete CRUD Feature](#complete-crud-feature)
2. [Pydantic Schemas](#pydantic-schemas)
3. [SQLAlchemy Models](#sqlalchemy-models)
4. [Repository Layer](#repository-layer)
5. [Service Layer](#service-layer)
6. [API Routes](#api-routes)
7. [Dependencies](#dependencies)
8. [Authentication](#authentication)
9. [Background Tasks](#background-tasks)
10. [Testing](#testing)
11. [Alembic Migrations](#alembic-migrations)
12. [Custom Exceptions](#custom-exceptions)

---

## 1. COMPLETE CRUD FEATURE

### Template: Complete Feature Set for "Product"

#### 1.1 Schema (app/schemas/product.py)

```python
"""Product schemas for request/response validation."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    """Base product schema with common fields."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Product name"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Product description"
    )
    price: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2,
        description="Product price"
    )
    stock: int = Field(
        default=0,
        ge=0,
        description="Available stock"
    )
    is_active: bool = Field(
        default=True,
        description="Product active status"
    )


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Validate name is not empty or whitespace."""
        if not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ProductListResponse(BaseModel):
    """Schema for product list response."""
    
    products: list[ProductResponse]
    total: int
    page: int
    page_size: int
    
    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        return (self.total + self.page_size - 1) // self.page_size
```

#### 1.2 Model (app/models/product.py)

```python
"""Product database model."""

from decimal import Decimal
from sqlalchemy import String, Text, Numeric, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, IDMixin, TimestampMixin


class Product(Base, IDMixin, TimestampMixin):
    """Product model."""
    
    __tablename__ = "products"
    
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Product name"
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        comment="Product description"
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        comment="Product price"
    )
    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Available stock"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Active status"
    )
    
    def __repr__(self) -> str:
        """String representation."""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
```

#### 1.3 Repository (app/repositories/product.py)

```python
"""Product repository for database operations."""

from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Repository for product database operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)
    
    async def get_by_name(self, name: str) -> Optional[Product]:
        """Get product by name."""
        result = await self.db.execute(
            select(Product).where(Product.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_active_products(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Product], int]:
        """Get all active products with pagination."""
        query = select(Product).where(Product.is_active == True)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Get products
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        products = result.scalars().all()
        
        return list(products), total or 0
    
    async def search_by_name(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Product], int]:
        """Search products by name."""
        query = select(Product).where(
            Product.name.ilike(f"%{search_term}%")
        )
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Get products
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        products = result.scalars().all()
        
        return list(products), total or 0
    
    async def update_stock(
        self,
        product_id: int,
        quantity: int
    ) -> Optional[Product]:
        """Update product stock."""
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        product.stock += quantity
        await self.db.flush()
        await self.db.refresh(product)
        return product
```

#### 1.4 Service (app/services/product_service.py)

```python
"""Product business logic service."""

from typing import List, Optional
from fastapi import HTTPException, status
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.common import PaginationParams
from app.repositories.product import ProductRepository
from app.core.logging import logger


class ProductService:
    """Service for product business logic."""
    
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    async def create_product(
        self,
        product_data: ProductCreate
    ) -> ProductResponse:
        """Create a new product."""
        # Check if product with same name exists
        existing = await self.repository.get_by_name(product_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with name '{product_data.name}' already exists"
            )
        
        # Create product
        product = await self.repository.create(product_data.model_dump())
        logger.info(f"Created product: {product.id} - {product.name}")
        
        return ProductResponse.model_validate(product)
    
    async def get_product(self, product_id: int) -> ProductResponse:
        """Get product by ID."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        return ProductResponse.model_validate(product)
    
    async def list_products(
        self,
        pagination: PaginationParams,
        active_only: bool = False
    ) -> tuple[List[ProductResponse], int]:
        """List all products with pagination."""
        if active_only:
            products, total = await self.repository.get_active_products(
                skip=pagination.skip,
                limit=pagination.limit
            )
        else:
            products, total = await self.repository.get_multi(
                skip=pagination.skip,
                limit=pagination.limit
            )
        
        return [
            ProductResponse.model_validate(p) for p in products
        ], total
    
    async def search_products(
        self,
        search_term: str,
        pagination: PaginationParams
    ) -> tuple[List[ProductResponse], int]:
        """Search products by name."""
        products, total = await self.repository.search_by_name(
            search_term=search_term,
            skip=pagination.skip,
            limit=pagination.limit
        )
        
        return [
            ProductResponse.model_validate(p) for p in products
        ], total
    
    async def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate
    ) -> ProductResponse:
        """Update an existing product."""
        # Check if product exists
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        # Check name uniqueness if name is being updated
        if product_data.name and product_data.name != product.name:
            existing = await self.repository.get_by_name(product_data.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with name '{product_data.name}' already exists"
                )
        
        # Update product
        update_data = product_data.model_dump(exclude_unset=True)
        updated_product = await self.repository.update(product_id, update_data)
        logger.info(f"Updated product: {product_id}")
        
        return ProductResponse.model_validate(updated_product)
    
    async def delete_product(self, product_id: int) -> bool:
        """Delete a product (soft delete by setting is_active=False)."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        # Soft delete
        await self.repository.update(product_id, {"is_active": False})
        logger.info(f"Deleted (deactivated) product: {product_id}")
        
        return True
    
    async def adjust_stock(
        self,
        product_id: int,
        quantity: int
    ) -> ProductResponse:
        """Adjust product stock."""
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        
        # Check if adjustment would result in negative stock
        new_stock = product.stock + quantity
        if new_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Current: {product.stock}, Requested: {abs(quantity)}"
            )
        
        # Update stock
        updated_product = await self.repository.update_stock(product_id, quantity)
        logger.info(f"Adjusted stock for product {product_id}: {quantity}")
        
        return ProductResponse.model_validate(updated_product)
```

#### 1.5 API Routes (app/api/v1/products.py)

```python
"""Product API endpoints."""

from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, status
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse
)
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.product_service import ProductService
from app.api.deps import get_product_service, get_current_active_user


router = APIRouter()


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Create a new product with the provided information"
)
async def create_product(
    product_data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> ProductResponse:
    """
    Create a new product.
    
    - **name**: Product name (required, 1-255 characters)
    - **description**: Product description (optional, max 2000 characters)
    - **price**: Product price (required, must be positive)
    - **stock**: Initial stock quantity (default: 0)
    - **is_active**: Active status (default: true)
    """
    return await service.create_product(product_data)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
    description="Retrieve a specific product by its ID"
)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)]
) -> ProductResponse:
    """Get a specific product by its ID."""
    return await service.get_product(product_id)


@router.get(
    "/",
    response_model=PaginatedResponse[ProductResponse],
    summary="List all products",
    description="Get a paginated list of products with optional filtering"
)
async def list_products(
    pagination: Annotated[PaginationParams, Depends()],
    service: Annotated[ProductService, Depends(get_product_service)],
    active_only: bool = Query(
        default=False,
        description="Filter only active products"
    )
) -> PaginatedResponse[ProductResponse]:
    """
    Get a paginated list of products.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **active_only**: If true, return only active products
    """
    products, total = await service.list_products(pagination, active_only)
    
    return PaginatedResponse(
        items=products,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit
    )


@router.get(
    "/search/",
    response_model=PaginatedResponse[ProductResponse],
    summary="Search products",
    description="Search products by name"
)
async def search_products(
    pagination: Annotated[PaginationParams, Depends()],
    service: Annotated[ProductService, Depends(get_product_service)],
    q: str = Query(
        ...,
        min_length=1,
        description="Search term for product name"
    )
) -> PaginatedResponse[ProductResponse]:
    """Search products by name."""
    products, total = await service.search_products(q, pagination)
    
    return PaginatedResponse(
        items=products,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    description="Update an existing product"
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> ProductResponse:
    """Update an existing product with new information."""
    return await service.update_product(product_id, product_data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
    description="Soft delete a product (deactivate)"
)
async def delete_product(
    product_id: int,
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> None:
    """Delete (deactivate) a product."""
    await service.delete_product(product_id)


@router.patch(
    "/{product_id}/stock",
    response_model=ProductResponse,
    summary="Adjust product stock",
    description="Increase or decrease product stock quantity"
)
async def adjust_stock(
    product_id: int,
    quantity: int = Query(
        ...,
        description="Quantity to add (positive) or remove (negative)"
    ),
    service: Annotated[ProductService, Depends(get_product_service)],
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> ProductResponse:
    """
    Adjust product stock.
    
    - **quantity**: Positive number to add stock, negative to remove
    """
    return await service.adjust_stock(product_id, quantity)
```

#### 1.6 Dependency (app/api/deps.py)

```python
# Add this to your existing deps.py

from app.services.product_service import ProductService
from app.repositories.product import ProductRepository


async def get_product_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> ProductService:
    """Get product service with dependencies."""
    repository = ProductRepository(db)
    return ProductService(repository)
```

#### 1.7 Migration

```bash
# Generate migration
alembic revision --autogenerate -m "Add products table"

# The migration file will be created in alembic/versions/
# Review and edit if necessary, then apply:
alembic upgrade head
```

#### 1.8 Tests (tests/integration/test_api/test_products.py)

```python
"""Integration tests for product API."""

import pytest
from decimal import Decimal
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_product(
    client: AsyncClient,
    auth_headers: dict
):
    """Test creating a new product."""
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": "29.99",
        "stock": 100
    }
    
    response = await client.post(
        "/api/v1/products/",
        json=product_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert Decimal(data["price"]) == Decimal(product_data["price"])
    assert data["stock"] == product_data["stock"]
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_product_duplicate_name(
    client: AsyncClient,
    auth_headers: dict
):
    """Test creating product with duplicate name."""
    product_data = {
        "name": "Duplicate Product",
        "price": "19.99"
    }
    
    # Create first product
    response1 = await client.post(
        "/api/v1/products/",
        json=product_data,
        headers=auth_headers
    )
    assert response1.status_code == 201
    
    # Try to create duplicate
    response2 = await client.post(
        "/api/v1/products/",
        json=product_data,
        headers=auth_headers
    )
    assert response2.status_code == 400


@pytest.mark.asyncio
async def test_get_product(client: AsyncClient, auth_headers: dict):
    """Test getting a product by ID."""
    # Create product
    product_data = {"name": "Get Test Product", "price": "15.99"}
    create_response = await client.post(
        "/api/v1/products/",
        json=product_data,
        headers=auth_headers
    )
    product_id = create_response.json()["id"]
    
    # Get product
    response = await client.get(f"/api/v1/products/{product_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    """Test getting non-existent product."""
    response = await client.get("/api/v1/products/999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_products(client: AsyncClient):
    """Test listing products with pagination."""
    response = await client.get("/api/v1/products/?skip=0&limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "skip" in data
    assert "limit" in data


@pytest.mark.asyncio
async def test_search_products(client: AsyncClient, auth_headers: dict):
    """Test searching products."""
    # Create test products
    await client.post(
        "/api/v1/products/",
        json={"name": "Search Test Widget", "price": "10.00"},
        headers=auth_headers
    )
    
    # Search
    response = await client.get("/api/v1/products/search/?q=Widget")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any("Widget" in item["name"] for item in data["items"])


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, auth_headers: dict):
    """Test updating a product."""
    # Create product
    create_response = await client.post(
        "/api/v1/products/",
        json={"name": "Update Test", "price": "20.00"},
        headers=auth_headers
    )
    product_id = create_response.json()["id"]
    
    # Update product
    update_data = {"name": "Updated Name", "price": "25.00"}
    response = await client.put(
        f"/api/v1/products/{product_id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert Decimal(data["price"]) == Decimal(update_data["price"])


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, auth_headers: dict):
    """Test deleting a product."""
    # Create product
    create_response = await client.post(
        "/api/v1/products/",
        json={"name": "Delete Test", "price": "30.00"},
        headers=auth_headers
    )
    product_id = create_response.json()["id"]
    
    # Delete product
    response = await client.delete(
        f"/api/v1/products/{product_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_adjust_stock(client: AsyncClient, auth_headers: dict):
    """Test adjusting product stock."""
    # Create product
    create_response = await client.post(
        "/api/v1/products/",
        json={"name": "Stock Test", "price": "10.00", "stock": 50},
        headers=auth_headers
    )
    product_id = create_response.json()["id"]
    
    # Add stock
    response = await client.patch(
        f"/api/v1/products/{product_id}/stock?quantity=25",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["stock"] == 75
    
    # Remove stock
    response = await client.patch(
        f"/api/v1/products/{product_id}/stock?quantity=-30",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["stock"] == 45


@pytest.mark.asyncio
async def test_adjust_stock_insufficient(
    client: AsyncClient,
    auth_headers: dict
):
    """Test adjusting stock with insufficient quantity."""
    # Create product with low stock
    create_response = await client.post(
        "/api/v1/products/",
        json={"name": "Low Stock", "price": "10.00", "stock": 5},
        headers=auth_headers
    )
    product_id = create_response.json()["id"]
    
    # Try to remove more than available
    response = await client.patch(
        f"/api/v1/products/{product_id}/stock?quantity=-10",
        headers=auth_headers
    )
    
    assert response.status_code == 400
```

---

## 2. PYDANTIC SCHEMAS

### Template: Base Schema with Validation

```python
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    HttpUrl,
    field_validator,
    model_validator
)


class MyBaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode for SQLAlchemy
        str_strip_whitespace=True,  # Strip whitespace from strings
        validate_assignment=True,  # Validate on assignment
        use_enum_values=True,  # Use enum values instead of enum objects
        populate_by_name=True,  # Allow population by field name
        json_schema_extra={  # Add example to OpenAPI
            "example": {
                "field": "value"
            }
        }
    )


class MyCreateSchema(MyBaseSchema):
    """Schema for creating a resource."""
    
    # Required fields
    email: EmailStr = Field(
        ...,
        description="User email address",
        max_length=255
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_-]+$",
        description="Username (alphanumeric, dash, underscore only)"
    )
    
    # Optional fields with defaults
    is_active: bool = Field(
        default=True,
        description="Active status"
    )
    
    # Field with custom validation
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Validate username is alphanumeric."""
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()


class MyUpdateSchema(BaseModel):
    """Schema for updating a resource (all fields optional)."""
    
    email: Optional[EmailStr] = Field(None, max_length=255)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None
    
    # Model validator for complex validation
    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "MyUpdateSchema":
        """Ensure at least one field is provided."""
        if not any(self.model_dump(exclude_unset=True).values()):
            raise ValueError("At least one field must be provided")
        return self


class MyResponseSchema(MyBaseSchema):
    """Schema for response."""
    
    id: int = Field(..., description="Resource ID", gt=0)
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

---

## 3. SQLALCHEMY MODELS

### Template: Model with Relationships

```python
from datetime import datetime
from sqlalchemy import (
    String,
    Text,
    Integer,
    Boolean,
    ForeignKey,
    Index,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, IDMixin, TimestampMixin


class User(Base, IDMixin, TimestampMixin):
    """User model."""
    
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_username", "username"),
        CheckConstraint("char_length(username) >= 3", name="check_username_length"),
    )
    
    # Basic fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Optional fields
    full_name: Mapped[str | None] = mapped_column(String(255))
    bio: Mapped[str | None] = mapped_column(Text)
    
    # Relationships
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"


class Post(Base, IDMixin, TimestampMixin):
    """Post model."""
    
    __tablename__ = "posts"
    __table_args__ = (
        Index("idx_post_author", "author_id"),
        Index("idx_post_published", "is_published"),
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Foreign key
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationship
    author: Mapped["User"] = relationship("User", back_populates="posts")
    
    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title='{self.title}')>"
```

---

## 4. REPOSITORY LAYER

### Template: Repository with Complex Queries

```python
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, Post
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with complex queries."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_with_posts(self, user_id: int) -> Optional[User]:
        """Get user with all posts (eager loading)."""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.posts))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def search_users(
        self,
        search_term: str,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[User], int]:
        """Search users with filters."""
        # Build base query
        query = select(User)
        filters = []
        
        # Add search filter
        if search_term:
            search_filter = or_(
                User.username.ilike(f"%{search_term}%"),
                User.email.ilike(f"%{search_term}%"),
                User.full_name.ilike(f"%{search_term}%")
            )
            filters.append(search_filter)
        
        # Add active filter
        if is_active is not None:
            filters.append(User.is_active == is_active)
        
        # Apply filters
        if filters:
            query = query.where(and_(*filters))
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Apply pagination and execute
        query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return list(users), total or 0
    
    async def get_active_users_count(self) -> int:
        """Get count of active users."""
        result = await self.db.execute(
            select(func.count()).select_from(User).where(User.is_active == True)
        )
        return result.scalar_one()
    
    async def bulk_update_status(
        self,
        user_ids: List[int],
        is_active: bool
    ) -> int:
        """Bulk update user status."""
        from sqlalchemy import update
        
        stmt = (
            update(User)
            .where(User.id.in_(user_ids))
            .values(is_active=is_active)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
```

---

[Continue in next part due to length limits...]

Would you like me to continue with the remaining templates (Service Layer, API Routes, Authentication, Background Tasks, Testing, etc.)?
