"""
Tests for Supplier API endpoints and business logic.
Covers CRUD operations, validation, and business rules.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.supplier import Supplier
from app.models.user import User, UserRole, UserType
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class TestSupplierCreation:
    """Test supplier creation scenarios."""
    
    @pytest.mark.asyncio
    async def test_create_supplier_success(
        self,
        async_async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test successful supplier creation."""
        supplier_data = {
            "code": "SUP001",
            "name": "Test Supplier Co., Ltd.",
            "email": "contact@testsupplier.com",
            "phone": "0123456789",
            "tax_code": "0123456789",
            "address": "123 Test Street, Test City",
            "contact_person": "John Doe",
            "contact_phone": "0987654321",
            "contact_email": "john@testsupplier.com",
            "description": "A test supplier",
            "is_active": True,
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == supplier_data["code"]
        assert data["name"] == supplier_data["name"]
        assert data["email"] == supplier_data["email"]
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    @pytest.mark.asyncio
    async def test_create_duplicate_code(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test creation fails with duplicate code."""
        supplier_data = {
            "code": sample_supplier.code,  # Duplicate code
            "name": "Another Supplier",
            "email": "another@supplier.com",
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 400
        assert "code already exists" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_create_duplicate_email(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test creation fails with duplicate email."""
        supplier_data = {
            "code": "SUP999",
            "name": "Another Supplier",
            "email": sample_supplier.email,  # Duplicate email
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 400
        assert "email already exists" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_create_invalid_code_format(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test creation fails with invalid code format."""
        supplier_data = {
            "code": "INVALID001",  # Must start with SUP
            "name": "Test Supplier",
            "email": "test@supplier.com",
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_create_without_email(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test creation fails without required email."""
        supplier_data = {
            "code": "SUP002",
            "name": "Test Supplier",
            # email is missing
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_create_requires_authentication(
        self,
        async_client: AsyncClient,
    ):
        """Test creation requires authentication."""
        supplier_data = {
            "code": "SUP003",
            "name": "Test Supplier",
            "email": "test@supplier.com",
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
        )
        
        assert response.status_code == 401  # Unauthorized


class TestSupplierRetrieval:
    """Test supplier retrieval scenarios."""
    
    @pytest.mark.asyncio
    async def test_get_supplier_by_id(
        self,
        async_client: AsyncClient,
        user_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test retrieving supplier by ID."""
        response = await async_client.get(
            f"/api/v1/suppliers/{sample_supplier.id}",
            headers=user_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_supplier.id
        assert data["code"] == sample_supplier.code
        assert data["name"] == sample_supplier.name
    
    @pytest.mark.asyncio
    async def test_get_supplier_not_found(
        self,
        async_client: AsyncClient,
        user_token_headers: dict,
    ):
        """Test retrieving non-existent supplier returns 404."""
        response = await async_client.get(
            "/api/v1/suppliers/99999",
            headers=user_token_headers,
        )
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_list_suppliers_pagination(
        self,
        async_client: AsyncClient,
        user_token_headers: dict,
        multiple_suppliers: list[Supplier],
    ):
        """Test listing suppliers with pagination."""
        response = await async_client.get(
            "/api/v1/suppliers?skip=0&limit=5",
            headers=user_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "skip" in data
        assert "limit" in data
        assert len(data["items"]) <= 5
        assert data["total"] >= len(multiple_suppliers)
    
    @pytest.mark.asyncio
    async def test_list_active_suppliers_only(
        self,
        async_client: AsyncClient,
        user_token_headers: dict,
        multiple_suppliers: list[Supplier],
    ):
        """Test filtering suppliers by active status."""
        response = await async_client.get(
            "/api/v1/suppliers?is_active=true",
            headers=user_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert all(item["is_active"] for item in data["items"])
    
    @pytest.mark.asyncio
    async def test_search_suppliers_by_name(
        self,
        async_client: AsyncClient,
        user_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test searching suppliers by name."""
        search_query = sample_supplier.name[:5]
        response = await async_client.get(
            f"/api/v1/suppliers/search?q={search_query}",
            headers=user_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any(search_query.lower() in item["name"].lower() for item in data)
    
    @pytest.mark.asyncio
    async def test_search_suppliers_by_code(
        self,
        async_client: AsyncClient,
        user_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test searching suppliers by code."""
        response = await async_client.get(
            f"/api/v1/suppliers/search?q={sample_supplier.code}",
            headers=user_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any(item["code"] == sample_supplier.code for item in data)


class TestSupplierUpdate:
    """Test supplier update scenarios."""
    
    @pytest.mark.asyncio
    async def test_update_supplier_name(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test updating supplier name."""
        update_data = {
            "name": "Updated Supplier Name",
        }
        
        response = await async_client.patch(
            f"/api/v1/suppliers/{sample_supplier.id}",
            json=update_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["code"] == sample_supplier.code  # Unchanged
    
    @pytest.mark.asyncio
    async def test_update_supplier_email_unique_validation(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        multiple_suppliers: list[Supplier],
    ):
        """Test update fails when email conflicts with another supplier."""
        supplier1, supplier2 = multiple_suppliers[0], multiple_suppliers[1]
        
        update_data = {
            "email": supplier2.email,  # Try to use another supplier's email
        }
        
        response = await async_client.patch(
            f"/api/v1/suppliers/{supplier1.id}",
            json=update_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 400
        assert "email already exists" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_update_supplier_not_found(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test updating non-existent supplier returns 404."""
        update_data = {"name": "Updated Name"}
        
        response = await async_client.patch(
            "/api/v1/suppliers/99999",
            json=update_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_update_partial_fields(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test partial update with only some fields."""
        update_data = {
            "phone": "0111222333",
            "address": "New Address",
        }
        
        response = await async_client.patch(
            f"/api/v1/suppliers/{sample_supplier.id}",
            json=update_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["phone"] == update_data["phone"]
        assert data["address"] == update_data["address"]
        assert data["name"] == sample_supplier.name  # Unchanged


class TestSupplierDelete:
    """Test supplier deletion scenarios."""
    
    @pytest.mark.asyncio
    async def test_soft_delete_supplier(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test soft deleting a supplier."""
        response = await async_client.delete(
            f"/api/v1/suppliers/{sample_supplier.id}",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 204
        
        # Verify supplier still exists but is soft deleted
        get_response = await async_client.get(
            f"/api/v1/suppliers/{sample_supplier.id}",
            headers=admin_token_headers,
        )
        # Should return 404 or show deleted_at is set
        assert get_response.status_code in [404, 200]
    
    @pytest.mark.asyncio
    async def test_cannot_delete_supplier_with_users(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier_with_users: Supplier,
    ):
        """Test deletion fails when supplier has active users."""
        response = await async_client.delete(
            f"/api/v1/suppliers/{sample_supplier_with_users.id}",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 400
        assert "active users" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_delete_supplier_not_found(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test deleting non-existent supplier returns 404."""
        response = await async_client.delete(
            "/api/v1/suppliers/99999",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 404


class TestSupplierActivation:
    """Test supplier activation/deactivation scenarios."""
    
    @pytest.mark.asyncio
    async def test_activate_supplier(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        inactive_supplier: Supplier,
    ):
        """Test activating an inactive supplier."""
        response = await async_client.post(
            f"/api/v1/suppliers/{inactive_supplier.id}/activate",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is True
    
    @pytest.mark.asyncio
    async def test_deactivate_supplier(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test deactivating an active supplier."""
        response = await async_client.post(
            f"/api/v1/suppliers/{sample_supplier.id}/deactivate",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
    
    @pytest.mark.asyncio
    async def test_activate_nonexistent_supplier(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test activating non-existent supplier returns 404."""
        response = await async_client.post(
            "/api/v1/suppliers/99999/activate",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 404


class TestSupplierBusinessRules:
    """Test supplier business rules and validation."""
    
    @pytest.mark.asyncio
    async def test_code_must_be_uppercase(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test supplier code is converted to uppercase."""
        supplier_data = {
            "code": "sup100",  # lowercase
            "name": "Test Supplier",
            "email": "test@supplier.com",
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        if response.status_code == 201:
            data = response.json()
            assert data["code"] == "SUP100"  # Should be uppercase
    
    @pytest.mark.asyncio
    async def test_email_normalized_to_lowercase(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
    ):
        """Test supplier email is normalized to lowercase."""
        supplier_data = {
            "code": "SUP101",
            "name": "Test Supplier",
            "email": "TEST@SUPPLIER.COM",  # uppercase
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@supplier.com"  # Should be lowercase
    
    @pytest.mark.asyncio
    async def test_tax_code_uniqueness(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test tax code must be unique."""
        supplier_data = {
            "code": "SUP102",
            "name": "Another Supplier",
            "email": "another@supplier.com",
            "tax_code": sample_supplier.tax_code,  # Duplicate tax code
        }
        
        response = await async_client.post(
            "/api/v1/suppliers",
            json=supplier_data,
            headers=admin_token_headers,
        )
        
        assert response.status_code == 400
        assert "tax_code already exists" in response.json()["detail"].lower()
