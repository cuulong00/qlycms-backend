# 🔐 SECURITY ARCHITECTURE GUIDE
## Kiến Trúc Bảo Mật Toàn Diện cho FastAPI Backend

---

**Phiên bản:** 1.0.0  
**Ngày tạo:** 6 Tháng 10, 2025  
**Mục đích:** Hướng dẫn chi tiết về security implementation  

---

## 📋 MỤC LỤC

1. [Tổng Quan Security Stack](#tổng-quan-security-stack)
2. [Authentication (Xác Thực)](#authentication-xác-thực)
3. [Authorization (Phân Quyền)](#authorization-phân-quyền)
4. [Data Validation (Xác Thực Dữ Liệu)](#data-validation-xác-thực-dữ-liệu)
5. [Security Best Practices](#security-best-practices)
6. [Common Security Scenarios](#common-security-scenarios)

---

## 🎯 TỔNG QUAN SECURITY STACK

### Stack Components

| Layer | Component | Version | Purpose |
|-------|-----------|---------|---------|
| **Authentication** | FastAPI-Users | 14.0.1 | User management, login/register, OAuth |
| **Authentication** | Authlib | 1.6.5 | OAuth 2.0 provider/client, JWT |
| **Authorization** | Python-Casbin | 1.37.6 | RBAC/ABAC/ACL policies |
| **Token Handling** | Python-JOSE | 3.3.0 | JWT creation & validation |
| **Password Security** | Passlib | 1.7.4 | Bcrypt hashing |
| **Data Validation** | Pydantic V2 | 2.11.10 | Request/response validation |

### Security Flow Diagram

```
┌────────────────────────────────────────────────────────────┐
│                        CLIENT                               │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: AUTHENTICATION (Who are you?)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ FastAPI-Users + Authlib                              │   │
│  │ ✓ Email/Password Login                               │   │
│  │ ✓ OAuth2 Social Login (Google, GitHub)              │   │
│  │ ✓ JWT Token Generation                               │   │
│  │ ✓ Token Refresh                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: AUTHORIZATION (What can you do?)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Casbin Policy Engine                                 │   │
│  │ ✓ Role-Based Access Control (RBAC)                  │   │
│  │ ✓ Attribute-Based Access Control (ABAC)             │   │
│  │ ✓ Resource-Level Permissions                        │   │
│  │ ✓ Dynamic Policy Loading                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: DATA VALIDATION (Is input safe?)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Pydantic V2 Validation                               │   │
│  │ ✓ Type Checking                                      │   │
│  │ ✓ Custom Validators                                  │   │
│  │ ✓ Sanitization                                       │   │
│  │ ✓ Data Transformation                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬──────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 AUTHENTICATION (Xác Thực)

### 1. FastAPI-Users Integration

#### Features
- ✅ **Email/Password Authentication**
- ✅ **Email Verification**
- ✅ **Password Reset**
- ✅ **OAuth2 Social Login** (Google, GitHub, Facebook, etc.)
- ✅ **Multiple Authentication Backends** (JWT, Cookie)
- ✅ **User Management APIs**

#### Quick Setup

**Step 1: Install Dependencies**
```bash
pip install fastapi-users[sqlalchemy]==14.0.1
pip install authlib==1.6.5
```

**Step 2: User Model**
```python
from fastapi_users.db import SQLAlchemyBaseUserTable
from app.models.base import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    # FastAPI-Users handles: id, email, hashed_password, 
    # is_active, is_superuser, is_verified
    
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
```

**Step 3: Authentication Backend**
```python
from fastapi_users.authentication import (
    JWTStrategy,
    BearerTransport,
    AuthenticationBackend
)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=3600
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
```

**Step 4: Register Routes**
```python
from fastapi import FastAPI
from app.core.users import fastapi_users, auth_backend

app = FastAPI()

# Auth routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Register route
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Password reset routes
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
```

### 2. OAuth 2.0 Social Login

#### Supported Providers
- Google
- GitHub
- Facebook
- Twitter
- LinkedIn
- Microsoft

#### Example: Google OAuth Setup

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get('/auth/google/login')
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth/google/callback')
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    # Create or update user in database
    # Return JWT token
```

### 3. JWT Token Strategy

#### Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1696598400,
  "iat": 1696594800,
  "type": "access"
}
```

#### Token Lifecycle
1. **Login** → Generate access token (short-lived, 30 min)
2. **Refresh** → Generate new access token using refresh token
3. **Logout** → Revoke tokens (blacklist in Redis)

#### Implementation
```python
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(user_id: int, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
```

---

## 🛡️ AUTHORIZATION (Phân Quyền)

### 1. Casbin Policy Engine

#### Supported Models
- **RBAC (Role-Based Access Control)** - Phân quyền theo vai trò
- **ABAC (Attribute-Based Access Control)** - Phân quyền theo thuộc tính
- **ACL (Access Control List)** - Danh sách kiểm soát truy cập

#### Casbin Model Configuration

**RBAC Model** (`casbin_model.conf`):
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

#### Policy Examples

**Roles and Permissions:**
```
p, admin, posts, create
p, admin, posts, read
p, admin, posts, update
p, admin, posts, delete
p, admin, users, *

p, editor, posts, create
p, editor, posts, read
p, editor, posts, update

p, viewer, posts, read
p, viewer, users, read
```

**User-Role Assignments:**
```
g, alice, admin
g, bob, editor
g, charlie, viewer
```

#### Usage in FastAPI

**Dependency for Permission Check:**
```python
from fastapi import Depends, HTTPException, status
import casbin

async def require_permission(
    resource: str,
    action: str
):
    async def permission_checker(
        user: User = Depends(current_active_user),
        enforcer: casbin.Enforcer = Depends(get_enforcer)
    ):
        if not enforcer.enforce(str(user.id), resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No permission to {action} {resource}"
            )
        return user
    
    return permission_checker
```

**Route Protection:**
```python
@router.post("/posts")
async def create_post(
    post_data: PostCreate,
    user: User = Depends(require_permission("posts", "create"))
):
    # Only users with "create" permission on "posts" can access
    return {"message": "Post created"}

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    user: User = Depends(require_permission("posts", "delete"))
):
    # Only users with "delete" permission on "posts" can access
    return {"message": "Post deleted"}
```

### 2. Role Management API

```python
from fastapi import APIRouter, Depends
from app.services.permission_service import PermissionService

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/users/{user_id}/roles/{role}")
async def assign_role(
    user_id: int,
    role: str,
    current_user: User = Depends(require_permission("roles", "assign")),
    permission_service: PermissionService = Depends()
):
    """Assign role to user"""
    success = await permission_service.add_role_to_user(user_id, role)
    return {"success": success}

@router.get("/users/{user_id}/roles")
async def get_user_roles(
    user_id: int,
    current_user: User = Depends(current_active_user),
    permission_service: PermissionService = Depends()
):
    """Get all roles for user"""
    roles = await permission_service.get_user_roles(user_id)
    return {"roles": roles}

@router.post("/roles/{role}/permissions")
async def add_permission_to_role(
    role: str,
    resource: str,
    action: str,
    current_user: User = Depends(require_permission("roles", "manage")),
    permission_service: PermissionService = Depends()
):
    """Add permission to role"""
    success = await permission_service.add_permission(role, resource, action)
    return {"success": success}
```

### 3. Dynamic Permission Checking

```python
@router.get("/posts/{post_id}")
async def get_post(
    post_id: int,
    user: User = Depends(current_active_user),
    enforcer: casbin.Enforcer = Depends(get_enforcer)
):
    """Get post with dynamic permission check"""
    post = await post_service.get_by_id(post_id)
    
    # Check if user is owner or has read permission
    is_owner = post.author_id == user.id
    has_permission = enforcer.enforce(str(user.id), "posts", "read")
    
    if not (is_owner or has_permission):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return post
```

---

## ✅ DATA VALIDATION (Xác Thực Dữ Liệu)

### 1. Pydantic V2 Advanced Validation

#### Built-in Validators
```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl, constr, conint

class UserCreate(BaseModel):
    # Email validation
    email: EmailStr
    
    # String constraints
    username: constr(min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9_]+$')
    
    # Integer constraints
    age: conint(ge=18, le=120)
    
    # URL validation
    website: Optional[HttpUrl] = None
    
    # Field with metadata
    password: str = Field(..., min_length=8, max_length=100)
```

#### Custom Validators
```python
from pydantic import field_validator, model_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    
    @field_validator('email')
    @classmethod
    def email_must_be_lowercase(cls, v: str) -> str:
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain a number')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain an uppercase letter')
        return v
    
    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
```

#### Sanitization
```python
from pydantic import field_validator
import bleach

class PostCreate(BaseModel):
    title: str
    content: str
    
    @field_validator('content')
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        # Remove potentially dangerous HTML/JavaScript
        allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li']
        return bleach.clean(v, tags=allowed_tags, strip=True)
```

### 2. Request Validation

```python
from fastapi import APIRouter, Body, Query, Path
from pydantic import BaseModel, Field

router = APIRouter()

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=1000000)
    tags: List[str] = Field(default_factory=list, max_items=10)

@router.post("/items")
async def create_item(
    item: ItemCreate = Body(...),
    category: str = Query(..., min_length=1, max_length=50),
    user_id: int = Path(..., gt=0)
):
    # All inputs are validated automatically
    return {"item": item, "category": category, "user_id": user_id}
```

### 3. Response Validation

```python
from fastapi import APIRouter
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await user_service.get_by_id(user_id)
    # Pydantic validates and serializes the response
    return user
```

---

## 🔒 SECURITY BEST PRACTICES

### 1. Password Security

#### Requirements
- ✅ Minimum 8 characters
- ✅ At least 1 uppercase letter
- ✅ At least 1 lowercase letter
- ✅ At least 1 number
- ✅ At least 1 special character (optional but recommended)

#### Implementation
```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Higher = more secure but slower
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### 2. Token Security

#### Best Practices
- ✅ Use HTTPS only in production
- ✅ Short-lived access tokens (15-30 minutes)
- ✅ Longer-lived refresh tokens (7 days)
- ✅ Store tokens in httpOnly cookies (not localStorage)
- ✅ Implement token blacklist for logout
- ✅ Rotate refresh tokens

#### Token Blacklist (Redis)
```python
from redis.asyncio import Redis
from datetime import timedelta

async def blacklist_token(token: str, expires_in: int):
    """Add token to blacklist"""
    redis = await get_redis()
    await redis.setex(f"blacklist:{token}", expires_in, "1")

async def is_token_blacklisted(token: str) -> bool:
    """Check if token is blacklisted"""
    redis = await get_redis()
    return await redis.exists(f"blacklist:{token}")
```

### 3. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: Request, credentials: OAuth2PasswordRequestForm):
    # Login logic
    pass
```

### 4. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests
)
```

### 5. SQL Injection Prevention

✅ **Already protected** with SQLAlchemy ORM:
```python
# ✅ SAFE - SQLAlchemy uses parameterized queries
result = await session.execute(
    select(User).where(User.email == user_email)
)

# ❌ NEVER DO THIS - Vulnerable to SQL injection
result = await session.execute(
    f"SELECT * FROM users WHERE email = '{user_email}'"
)
```

### 6. XSS Prevention

```python
from pydantic import field_validator
import html

class PostCreate(BaseModel):
    content: str
    
    @field_validator('content')
    @classmethod
    def escape_html(cls, v: str) -> str:
        return html.escape(v)
```

---

## 📝 COMMON SECURITY SCENARIOS

### Scenario 1: User Registration with Email Verification

```python
from fastapi_users import FastAPIUsers

@router.post("/register")
async def register(user_data: UserCreate):
    # 1. Validate input (Pydantic handles this)
    # 2. Check if email exists
    # 3. Hash password
    # 4. Create user
    # 5. Send verification email
    user = await user_manager.create(user_data)
    await send_verification_email(user.email, verification_token)
    return {"message": "Check your email for verification"}
```

### Scenario 2: Login with Multiple Authentication Methods

```python
@router.post("/login")
async def login(
    email: str,
    password: str,
    provider: Optional[str] = None  # "local", "google", "github"
):
    if provider == "local":
        # Email/password authentication
        user = await authenticate_user(email, password)
    elif provider == "google":
        # OAuth2 Google authentication
        user = await authenticate_with_google(token)
    
    # Generate JWT token
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}
```

### Scenario 3: Protected Endpoint with Role Check

```python
@router.get("/admin/dashboard")
async def admin_dashboard(
    user: User = Depends(require_role("admin"))
):
    # Only users with "admin" role can access
    return {"message": "Admin dashboard"}
```

### Scenario 4: Resource Owner Check

```python
@router.put("/posts/{post_id}")
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user: User = Depends(current_active_user)
):
    post = await post_service.get_by_id(post_id)
    
    # Check if user is owner or has admin role
    if post.author_id != user.id and not user.is_superuser:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return await post_service.update(post_id, post_data)
```

### Scenario 5: API Key Authentication

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key from header"""
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@router.get("/external-api")
async def external_api(api_key: str = Depends(verify_api_key)):
    return {"message": "API key validated"}
```

---

## 🎯 SECURITY CHECKLIST

### Production Deployment

- [ ] All passwords are hashed with bcrypt
- [ ] JWT tokens have expiration times
- [ ] HTTPS is enforced (no HTTP)
- [ ] CORS is configured with specific origins
- [ ] Rate limiting is enabled
- [ ] SQL injection protection (using ORM)
- [ ] XSS prevention (HTML escaping)
- [ ] CSRF protection (for cookie-based auth)
- [ ] Security headers configured
- [ ] Environment variables for secrets
- [ ] Token blacklist for logout
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Logging for security events
- [ ] Regular security audits

---

## 📚 ADDITIONAL RESOURCES

### Official Documentation
- [FastAPI-Users](https://fastapi-users.github.io/fastapi-users/)
- [Authlib](https://docs.authlib.org/)
- [Casbin](https://casbin.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [OWASP Security Guide](https://owasp.org/)

### Security Standards
- OAuth 2.0: RFC 6749
- JWT: RFC 7519
- OpenID Connect 1.0
- RBAC: NIST RBAC Model

---

**🔐 Secure coding is not optional - it's a requirement!**

*Document created by Senior Security Architect*
