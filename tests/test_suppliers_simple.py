"""
Simple Supplier API tests to verify basic functionality.
"""

import pytest
from httpx import AsyncClient

from app.models.supplier import Supplier


class TestSupplierCreation:
    """Test supplier creation scenarios."""
    
    @pytest.mark.asyncio
    async def test_create_supplier_success(
        self,
        async_client: AsyncClient,
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


class TestSupplierRetrieval:
    """Test supplier retrieval scenarios."""
    
    @pytest.mark.asyncio
    async def test_get_supplier_by_id(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        sample_supplier: Supplier,
    ):
        """Test get supplier by ID."""
        response = await async_client.get(
            f"/api/v1/suppliers/{sample_supplier.id}",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_supplier.id
        assert data["code"] == sample_supplier.code
        assert data["name"] == sample_supplier.name
    
    @pytest.mark.asyncio
    async def test_list_suppliers(
        self,
        async_client: AsyncClient,
        admin_token_headers: dict,
        multiple_suppliers: list[Supplier],
    ):
        """Test list suppliers with pagination."""
        response = await async_client.get(
            "/api/v1/suppliers?limit=5",
            headers=admin_token_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] == 10
        assert len(data["items"]) == 5
