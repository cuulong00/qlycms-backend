# QUICK START - Bắt Đầu Nhanh Cho LLM

## 🚀 Mục Tiêu

Hướng dẫn LLM **bắt đầu code ngay** trong 5 phút.

---

## ⚡ CÁC BƯỚC THỰC HIỆN

### BƯỚC 1: Đọc Context (2 phút)
```
📖 Đọc: README_LLM.md → Hiểu cấu trúc tài liệu
📖 Đọc: PROJECT_OVERVIEW.md (Section 1-2) → Hiểu bài toán
```

**TL;DR**:
- **Dự án**: Hệ thống quản lý yêu cầu mua sắm (YCMS) cho chuỗi nhà hàng 100 cơ sở
- **Tech Stack**: FastAPI + SQLAlchemy 2.0 + PostgreSQL + Pydantic V2
- **Timeline**: 12 weeks, 6 phases
- **Mục tiêu**: LLM tự động code production-ready

---

### BƯỚC 2: Chọn Phase & Task (1 phút)
```
📖 Đọc: PHASE_IMPLEMENTATION_GUIDE.md
👉 Bắt đầu: Phase 1 → Sprint 1.1 → Task 1.1.1
```

---

### BƯỚC 3: Generate Code (10 phút - 1 giờ tùy task)

#### Task 1.1.1: Project Initialization

**Mục tiêu**: Setup project structure

**Code cần generate**:

1️⃣ **requirements.txt**
```txt
fastapi[standard]==0.118.0
pydantic==2.11.10
sqlalchemy[asyncio]==2.0.43
alembic==1.16.5
asyncpg==0.30.0
fastapi-users[sqlalchemy]==14.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytest==8.3.0
pytest-asyncio==0.24.0
```

2️⃣ **app/core/config.py**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "YCMS Backend"
    SECRET_KEY: str
    DATABASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

3️⃣ **app/main.py**
```python
from fastapi import FastAPI

app = FastAPI(title="YCMS Backend")

@app.get("/")
async def root():
    return {"message": "YCMS API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

4️⃣ **docker-compose.yml**
```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ycms_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  
  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
```

**Verify**:
```bash
# Test
docker-compose up -d
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

---

### BƯỚC 4: Test & Verify (2 phút)

**Checklist**:
- [ ] Code runs without errors
- [ ] Health endpoint returns 200
- [ ] OpenAPI docs accessible at `/docs`
- [ ] Docker containers start successfully

---

## 📋 CHECKLIST TỪNG PHASE

### ✅ Phase 1: Foundation (Week 1-2)

**Sprint 1.1: Core Infrastructure**
- [ ] Project structure created
- [ ] FastAPI running
- [ ] Database connected
- [ ] Docker setup
- [ ] Health check working

**Sprint 1.2: Authentication**
- [ ] User model created
- [ ] Register endpoint
- [ ] Login endpoint
- [ ] JWT working
- [ ] Casbin RBAC

**Files to generate**:
```
app/
├── core/
│   ├── config.py           ✅ Settings
│   ├── security.py         ✅ JWT, password
│   └── users.py           ✅ FastAPI-Users setup
├── models/
│   ├── base.py            ✅ Base model
│   └── user.py            ✅ User model
├── schemas/
│   └── user.py            ✅ User schemas
├── db/
│   └── session.py         ✅ Database session
└── api/v1/
    └── auth.py            ✅ Auth endpoints
```

---

### ⏳ Phase 2: Master Data (Week 3-4)

**Entities to create**:
- [ ] Supplier (nhà cung cấp)
- [ ] Product & ProductCategory (sản phẩm)
- [ ] Restaurant (nhà hàng)
- [ ] SupplierProduct (mapping)

**Code pattern**:
```python
# For each entity:
1. app/models/{entity}.py     → SQLAlchemy model
2. app/schemas/{entity}.py    → Pydantic schemas
3. app/repositories/{entity}.py → Repository
4. app/services/{entity}.py   → Service
5. app/api/v1/{entity}s.py   → API endpoints
6. tests/test_{entity}.py    → Tests
7. alembic revision          → Migration
```

---

### ⏳ Phase 3: YCMS Management (Week 5-7)

**Main entities**:
- [ ] ProcurementRequest (phiếu YCMS)
- [ ] ProcurementRequestItem (chi tiết YCMS)
- [ ] Email notification system

---

## 🎯 LLM PROMPTS MẪU

### Prompt 1: Generate User Model
```
Based on ENTITY_SPECIFICATION.md section 1, generate:
1. User model (app/models/user.py) with FastAPI-Users
2. User schemas (app/schemas/user.py) with Pydantic V2
3. Alembic migration for users table

Include:
- Type hints
- Docstrings
- Relationships
- Enums for UserType and UserRole
- Validation in schemas
```

### Prompt 2: Generate Auth Endpoints
```
Based on PHASE_IMPLEMENTATION_GUIDE.md Task 1.2.1, generate:
1. FastAPI-Users setup (app/core/users.py)
2. Auth routes (app/api/v1/auth.py)
3. Tests (tests/test_auth.py)

Include:
- Register endpoint
- Login endpoint
- JWT strategy
- Current user dependency
```

### Prompt 3: Generate Supplier CRUD
```
Based on ENTITY_SPECIFICATION.md section 2, generate complete CRUD for Supplier:
1. Model (app/models/supplier.py)
2. Schemas (app/schemas/supplier.py)
3. Repository (app/repositories/supplier.py)
4. Service (app/services/supplier_service.py)
5. API (app/api/v1/suppliers.py)
6. Tests (tests/test_supplier.py)
7. Migration

Include pagination, filters, and RBAC permissions.
```

---

## 🔥 TIPS CHO LLM

### 1. Luôn Bao Gồm
- ✅ Type hints (Python 3.11+)
- ✅ Docstrings (Google style)
- ✅ Error handling
- ✅ Validation (Pydantic)
- ✅ Tests (>80% coverage)

### 2. Naming Conventions
```python
# Models: PascalCase
class User(Base): ...

# Fields: snake_case
created_at: Mapped[datetime] = ...

# Functions: snake_case
async def get_user_by_id(id: int): ...

# Constants: UPPER_CASE
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 3. Code Structure
```python
# Always follow this order
1. Imports (standard → third-party → local)
2. Constants/Enums
3. Models/Schemas
4. Functions/Methods
5. Main execution
```

---

## 📖 TÀI LIỆU THAM KHẢO NHANH

| Cần Gì | Đọc File Nào | Section |
|--------|-------------|---------|
| User model | ENTITY_SPECIFICATION.md | Section 1 |
| Supplier model | ENTITY_SPECIFICATION.md | Section 2 |
| Product model | ENTITY_SPECIFICATION.md | Section 3 |
| Auth setup | PHASE_IMPLEMENTATION_GUIDE.md | Task 1.2.1 |
| RBAC setup | PHASE_IMPLEMENTATION_GUIDE.md | Task 1.2.2 |
| Overall flow | PROJECT_OVERVIEW.md | Section 5 |

---

## ✅ ACCEPTANCE CRITERIA MẪU

### User Registration
```python
# Test case
response = client.post("/api/v1/auth/register", json={
    "email": "test@example.com",
    "password": "SecurePass123",
    "user_type": "aladdin",
    "role": "aladdin_staff",
    "first_name": "Test",
    "last_name": "User"
})

# Expected
assert response.status_code == 201
assert response.json()["email"] == "test@example.com"
assert "id" in response.json()
```

---

## 🎯 OUTPUT EXPECTED

### Phase 1 Completed
```
✅ FastAPI app running
✅ PostgreSQL connected
✅ User registration working
✅ User login working
✅ JWT tokens issued
✅ RBAC permissions working
✅ OpenAPI docs accessible
✅ Docker containers running
✅ Tests passing (>80% coverage)
```

---

## 🚀 BẮT ĐẦU NGAY

**Prompt cho LLM**:
```
Based on the specifications in:
- README_LLM.md
- PHASE_IMPLEMENTATION_GUIDE.md
- ENTITY_SPECIFICATION.md

Generate code for Phase 1, Sprint 1.1, Task 1.1.1 (Project Initialization).

Include:
1. Project structure
2. requirements.txt
3. app/core/config.py
4. app/db/session.py
5. app/models/base.py
6. app/main.py
7. docker-compose.yml
8. Dockerfile
9. alembic.ini
10. pytest.ini

Make sure all code is production-ready with type hints, docstrings, and follows best practices.
```

---

**Ready? GO! 🚀**

**Next**: [PHASE_IMPLEMENTATION_GUIDE.md](./PHASE_IMPLEMENTATION_GUIDE.md) → Start Phase 1

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: ✅ Ready to Use
