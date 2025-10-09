# Authentication & Authorization Implementation Guide

## Overview

Hệ thống YCMS sử dụng **FastAPI-Users** cho authentication và **Casbin** cho authorization (RBAC).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│  Auth Routes (/api/v1/auth)                                 │
│  ├── POST /register      - User registration                │
│  ├── POST /login         - Login with email/password        │
│  ├── POST /logout        - Logout (invalidate token)        │
│  ├── POST /forgot-password  - Request password reset        │
│  ├── POST /reset-password   - Reset password with token     │
│  ├── POST /request-verify-token  - Request email verify     │
│  ├── POST /verify        - Verify email with token          │
│  ├── GET  /users/me      - Get current user profile         │
│  └── PATCH /users/me     - Update current user profile      │
├─────────────────────────────────────────────────────────────┤
│  Authentication Layer (FastAPI-Users + JWT)                 │
│  ├── UserManager         - User lifecycle management        │
│  ├── JWT Strategy        - Token generation/validation      │
│  └── Auth Backend        - Bearer token transport           │
├─────────────────────────────────────────────────────────────┤
│  Authorization Layer (Casbin RBAC)                          │
│  ├── Enforcer            - Permission checking              │
│  ├── Policies            - Role-based permissions           │
│  └── Checkers            - Dependency injection helpers     │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                  │
│  ├── User Model          - SQLAlchemy model with enums      │
│  ├── User Schemas        - Pydantic validation              │
│  └── Database            - PostgreSQL with async support    │
└─────────────────────────────────────────────────────────────┘
```

## User Types & Roles

### User Types
- **ALADDIN**: Nhân viên của Aladdin Restaurant Chain
- **SUPPLIER**: Nhân viên của nhà cung cấp

### User Roles

#### Aladdin Roles
1. **super_admin**: Full access to everything
2. **aladdin_admin**: Quản lý toàn bộ YCMS và master data
3. **aladdin_staff**: Tạo YCMS, xác nhận giao hàng

#### Supplier Roles
4. **supplier_admin**: Quản lý YCMS và delivery notes của supplier
5. **supplier_staff**: Xem YCMS, cập nhật delivery status

## Files Created

### 1. Core Files

#### `app/core/users.py`
- **UserManager**: Quản lý user lifecycle
- Callbacks: `on_after_register`, `on_after_login`, `on_after_verify`, etc.
- Password validation logic
- Dependencies: `get_user_db`, `get_user_manager`

#### `app/core/auth.py`
- JWT Strategy configuration
- Auth Backend setup
- FastAPI-Users instance
- Auth dependencies: `current_active_user`, `current_verified_user`, `current_superuser`

#### `app/core/authorization.py`
- Casbin Enforcer setup
- RBAC policies for all roles
- `PermissionChecker` dependency
- `SupplierAccessChecker` dependency
- Helper functions: `check_supplier_access`, `require_permission`

#### `app/core/casbin_model.conf`
- Casbin RBAC model definition
- Matcher rules for permission checking

### 2. API Routes

#### `app/api/v1/auth.py`
- All authentication endpoints
- Integrates FastAPI-Users routers
- Routes for register, login, verify, reset password

### 3. Models & Schemas

#### `app/models/user.py`
- User model with FastAPI-Users integration
- `UserType` enum (aladdin, supplier)
- `UserRole` enum (5 roles)
- Business logic methods:
  - `can_manage_all_ycms()`
  - `can_create_ycms()`
  - `can_create_delivery_note()`
  - `can_manage_supplier_ycms(supplier_id)`

#### `app/schemas/user.py`
- `UserRead`: API response schema
- `UserCreate`: Registration schema with validation
- `UserUpdate`: Update schema with validation
- Field validators for `user_type` + `role` + `supplier_id` consistency

### 4. Database Migration

#### `alembic/versions/2025_10_08_0958-da5f0beeccb9_*.py`
- Create `user_type_enum` and `user_role_enum`
- Create `users` table with all fields
- Create indexes for performance
- Foreign key to `suppliers` table

### 5. Tests

#### `tests/test_auth.py`
- Registration tests (with validation)
- Login/logout tests
- Password reset tests
- Current user profile tests
- Authorization tests

#### `tests/conftest.py`
- Test fixtures for users
- Auth headers fixtures
- Async client fixture

## Usage Examples

### 1. User Registration

```python
# Register Aladdin Admin
POST /api/v1/auth/register
{
    "email": "admin@aladdin.com",
    "password": "SecurePass123!",
    "user_type": "aladdin",
    "role": "aladdin_admin",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "0123456789"
}

# Register Supplier Admin (requires supplier_id)
POST /api/v1/auth/register
{
    "email": "supplier@example.com",
    "password": "SecurePass123!",
    "user_type": "supplier",
    "role": "supplier_admin",
    "first_name": "Jane",
    "last_name": "Smith",
    "supplier_id": 1
}
```

### 2. Login

```python
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@aladdin.com&password=SecurePass123!

# Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### 3. Protected Endpoints

```python
# Get current user profile
GET /api/v1/auth/users/me
Authorization: Bearer {access_token}

# Update profile
PATCH /api/v1/auth/users/me
Authorization: Bearer {access_token}
{
    "first_name": "Updated Name",
    "phone_number": "9876543210"
}
```

### 4. Permission Checking in Routes

```python
from fastapi import APIRouter, Depends
from app.core.auth import current_active_user
from app.core.authorization import require_permission
from app.models.user import User

router = APIRouter()

@router.post("/suppliers")
async def create_supplier(
    supplier_data: SupplierCreate,
    user: User = Depends(current_active_user),
    _: None = Depends(require_permission("suppliers", "create"))
):
    """Create new supplier - requires 'suppliers:create' permission."""
    # Only super_admin and aladdin_admin can reach here
    ...

@router.get("/suppliers/{supplier_id}")
async def get_supplier(
    supplier_id: int,
    user: User = Depends(current_active_user),
    _: None = Depends(SupplierAccessChecker())
):
    """Get supplier - checks supplier-specific access."""
    # Super admin, aladdin roles can access all suppliers
    # Supplier users can only access their own supplier
    ...
```

### 5. Business Logic Methods

```python
# Check permissions programmatically
if user.can_create_ycms():
    # User can create procurement requests
    ...

if user.can_manage_all_ycms():
    # User can manage all suppliers' YCMSs
    query = select(ProcurementRequest)
else:
    # User can only see their supplier's YCMSs
    query = select(ProcurementRequest).where(
        ProcurementRequest.supplier_id == user.supplier_id
    )
```

## Permission Matrix

| Resource | Action | super_admin | aladdin_admin | aladdin_staff | supplier_admin | supplier_staff |
|----------|--------|-------------|---------------|---------------|----------------|----------------|
| suppliers | create | ✅ | ✅ | ❌ | ❌ | ❌ |
| suppliers | read | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) |
| suppliers | update | ✅ | ✅ | ❌ | ❌ | ❌ |
| suppliers | delete | ✅ | ✅ | ❌ | ❌ | ❌ |
| products | create | ✅ | ✅ | ❌ | ❌ | ❌ |
| products | read | ✅ | ✅ | ✅ | ✅ | ✅ |
| products | update | ✅ | ✅ | ❌ | ❌ | ❌ |
| products | delete | ✅ | ✅ | ❌ | ❌ | ❌ |
| procurement_requests | create | ✅ | ✅ | ✅ | ❌ | ❌ |
| procurement_requests | read | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) |
| procurement_requests | update | ✅ | ✅ | ❌ | ✅ (own) | ❌ |
| procurement_requests | delete | ✅ | ✅ | ❌ | ❌ | ❌ |
| delivery_notes | create | ✅ | ✅ | ✅ | ✅ | ❌ |
| delivery_notes | read | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) |
| delivery_notes | update | ✅ | ✅ | ✅ | ✅ (own) | ✅ (own) |
| delivery_notes | delete | ✅ | ✅ | ❌ | ❌ | ❌ |

## Testing

### Run All Auth Tests
```bash
pytest tests/test_auth.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_auth.py::TestUserRegistration -v
```

### Run with Coverage
```bash
pytest tests/test_auth.py --cov=app.core --cov=app.api.v1.auth
```

## Security Considerations

1. **Password Requirements**: Minimum 8 characters, cannot contain email/name
2. **Token Lifetime**: Access tokens expire after 1 hour
3. **Password Hashing**: BCrypt with automatic salt
4. **JWT Algorithm**: HS256
5. **Email Verification**: Optional but recommended
6. **Password Reset**: Secure token-based flow

## Next Steps

1. ✅ User model with enums
2. ✅ Pydantic schemas with validation
3. ✅ Database migration
4. ✅ FastAPI-Users integration
5. ✅ Casbin RBAC setup
6. ✅ Auth routes
7. ✅ Permission dependencies
8. ✅ Tests

### TODO:
- [ ] Email sending integration (SendGrid/AWS SES)
- [ ] Audit logging for user actions
- [ ] Rate limiting for auth endpoints
- [ ] OAuth integration (Google, GitHub)
- [ ] Two-factor authentication (2FA)
- [ ] Session management & revocation
- [ ] Admin panel for user management

## Troubleshooting

### Common Issues

1. **Import Error: fastapi_users**
   ```bash
   pip install fastapi-users[sqlalchemy]==14.0.1
   ```

2. **Import Error: casbin**
   ```bash
   pip install casbin==1.37.0
   ```

3. **Migration Error: suppliers table doesn't exist**
   - Supplier table will be created in next phase
   - Migration will fail until suppliers table exists
   - Can temporarily remove FK constraint for testing

4. **Test Error: async fixtures**
   ```bash
   pip install pytest-asyncio
   ```

## References

- [FastAPI-Users Documentation](https://fastapi-users.github.io/fastapi-users/)
- [Casbin Documentation](https://casbin.org/docs/overview)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
