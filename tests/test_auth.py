"""
Tests for authentication endpoints.
Test registration, login, logout, password reset, email verification.
"""

import pytest
from fastapi import status
from httpx import AsyncClient

from app.models.user import UserRole, UserType


@pytest.mark.asyncio
class TestUserRegistration:
    """Test user registration endpoint."""
    
    async def test_register_aladdin_admin_success(
        self, client: AsyncClient
    ) -> None:
        """Test successful registration of Aladdin admin user."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@aladdin.com",
                "password": "SecurePass123!",
                "user_type": UserType.ALADDIN.value,
                "role": UserRole.ALADDIN_ADMIN.value,
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0123456789",
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "admin@aladdin.com"
        assert data["user_type"] == UserType.ALADDIN.value
        assert data["role"] == UserRole.ALADDIN_ADMIN.value
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert "id" in data
        assert "hashed_password" not in data
    
    async def test_register_supplier_admin_success(
        self, client: AsyncClient, sample_supplier
    ) -> None:
        """Test successful registration of supplier admin user."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "supplier@example.com",
                "password": "SecurePass123!",
                "user_type": UserType.SUPPLIER.value,
                "role": UserRole.SUPPLIER_ADMIN.value,
                "first_name": "Jane",
                "last_name": "Smith",
                "supplier_id": sample_supplier.id,
            },
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "supplier@example.com"
        assert data["user_type"] == UserType.SUPPLIER.value
        assert data["role"] == UserRole.SUPPLIER_ADMIN.value
        assert data["supplier_id"] == sample_supplier.id
    
    async def test_register_supplier_without_supplier_id_fails(
        self, client: AsyncClient
    ) -> None:
        """Test that supplier registration fails without supplier_id."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "supplier@example.com",
                "password": "SecurePass123!",
                "user_type": UserType.SUPPLIER.value,
                "role": UserRole.SUPPLIER_ADMIN.value,
                "first_name": "Jane",
                "last_name": "Smith",
            },
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "supplier_id is required" in response.text.lower()
    
    async def test_register_aladdin_with_supplier_id_fails(
        self, client: AsyncClient, sample_supplier
    ) -> None:
        """Test that Aladdin registration fails with supplier_id."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@aladdin.com",
                "password": "SecurePass123!",
                "user_type": UserType.ALADDIN.value,
                "role": UserRole.ALADDIN_ADMIN.value,
                "first_name": "John",
                "last_name": "Doe",
                "supplier_id": sample_supplier.id,
            },
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "supplier_id must be none" in response.text.lower()
    
    async def test_register_invalid_role_for_user_type_fails(
        self, client: AsyncClient
    ) -> None:
        """Test that registration fails with invalid role for user type."""
        # Try to create Aladdin user with supplier role
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "admin@aladdin.com",
                "password": "SecurePass123!",
                "user_type": UserType.ALADDIN.value,
                "role": UserRole.SUPPLIER_ADMIN.value,  # Invalid for Aladdin
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "invalid role" in response.text.lower()
    
    async def test_register_duplicate_email_fails(
        self, client: AsyncClient
    ) -> None:
        """Test that duplicate email registration fails."""
        user_data = {
            "email": "duplicate@test.com",
            "password": "SecurePass123!",
            "user_type": UserType.ALADDIN.value,
            "role": UserRole.ALADDIN_STAFF.value,
            "first_name": "John",
            "last_name": "Doe",
        }
        
        # First registration
        response1 = await client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Duplicate registration
        response2 = await client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
class TestUserLogin:
    """Test user login endpoint."""
    
    async def test_login_success(
        self, client: AsyncClient, sample_aladdin_admin
    ) -> None:
        """Test successful login."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": sample_aladdin_admin.email,
                "password": "password123",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_login_wrong_password_fails(
        self, client: AsyncClient, sample_aladdin_admin
    ) -> None:
        """Test login with wrong password fails."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": sample_aladdin_admin.email,
                "password": "wrongpassword",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    async def test_login_nonexistent_user_fails(
        self, client: AsyncClient
    ) -> None:
        """Test login with non-existent user fails."""
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent@test.com",
                "password": "password123",
            },
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
class TestAuthenticatedEndpoints:
    """Test endpoints requiring authentication."""
    
    async def test_get_current_user(
        self, client: AsyncClient, auth_headers_aladdin_admin
    ) -> None:
        """Test getting current user profile."""
        response = await client.get(
            "/api/v1/auth/users/me",
            headers=auth_headers_aladdin_admin,
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "email" in data
        assert "role" in data
        assert "user_type" in data
    
    async def test_update_current_user(
        self, client: AsyncClient, auth_headers_aladdin_admin
    ) -> None:
        """Test updating current user profile."""
        response = await client.patch(
            "/api/v1/auth/users/me",
            headers=auth_headers_aladdin_admin,
            json={
                "first_name": "Updated",
                "phone_number": "9876543210",
            },
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["phone_number"] == "9876543210"
    
    async def test_access_without_token_fails(
        self, client: AsyncClient
    ) -> None:
        """Test that accessing protected endpoint without token fails."""
        response = await client.get("/api/v1/auth/users/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
class TestPasswordReset:
    """Test password reset flow."""
    
    async def test_request_password_reset(
        self, client: AsyncClient, sample_aladdin_admin
    ) -> None:
        """Test requesting password reset."""
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": sample_aladdin_admin.email},
        )
        
        assert response.status_code == status.HTTP_202_ACCEPTED
    
    async def test_request_password_reset_nonexistent_user(
        self, client: AsyncClient
    ) -> None:
        """Test password reset for non-existent user."""
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "nonexistent@test.com"},
        )
        
        # Should still return 202 to avoid user enumeration
        assert response.status_code == status.HTTP_202_ACCEPTED
