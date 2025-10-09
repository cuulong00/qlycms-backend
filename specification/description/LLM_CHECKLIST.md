# LLM CHECKLIST - Danh Sách Kiểm Tra Cho LLM

## 🎯 Mục Đích
Checklist đơn giản để LLM verify code đã generate đúng chuẩn production.

---

## ✅ CHECKLIST TRƯỚC KHI BẮT ĐẦU

### 1. Đọc Tài Liệu
- [ ] Đã đọc README_LLM.md
- [ ] Đã đọc QUICK_START.md
- [ ] Đã đọc PROJECT_OVERVIEW.md (ít nhất Section 1-2)
- [ ] Đã đọc PHASE_IMPLEMENTATION_GUIDE.md (phase hiện tại)
- [ ] Đã đọc ENTITY_SPECIFICATION.md (entities liên quan)

### 2. Hiểu Requirements
- [ ] Hiểu bài toán cần giải quyết
- [ ] Hiểu tech stack (FastAPI, SQLAlchemy 2.0, Pydantic V2)
- [ ] Hiểu acceptance criteria của task
- [ ] Hiểu output expected

### 3. Môi Trường
- [ ] Python 3.11+ available
- [ ] PostgreSQL 15+ available
- [ ] Docker installed
- [ ] Git configured

---

## ✅ CHECKLIST KHI GENERATE CODE

### 1. File Structure
- [ ] Đúng vị trí trong folder structure
- [ ] Tên file theo convention (snake_case)
- [ ] __init__.py có trong mọi package

### 2. Imports
- [ ] Sắp xếp đúng thứ tự (standard → third-party → local)
- [ ] Không có unused imports
- [ ] Import chính xác (không import *)

### 3. Type Hints
- [ ] 100% functions có type hints
- [ ] 100% class attributes có type hints
- [ ] Return type được specify
- [ ] Optional[] cho nullable values
- [ ] List[], Dict[] thay vì list, dict

### 4. Docstrings
- [ ] Mọi module có docstring
- [ ] Mọi class có docstring
- [ ] Mọi function có docstring (Google style)
- [ ] Docstring mô tả rõ ràng purpose
- [ ] Docstring list các parameters
- [ ] Docstring mô tả return value

### 5. Models (SQLAlchemy)
- [ ] Extend từ Base
- [ ] Có __tablename__
- [ ] Tất cả columns có Mapped[] type hints
- [ ] Tất cả columns có comment
- [ ] Foreign keys có ondelete policy
- [ ] Relationships có back_populates
- [ ] Indexes được define
- [ ] __table_args__ có comment

### 6. Schemas (Pydantic)
- [ ] Có Base, Create, Update, Response schemas
- [ ] model_config = ConfigDict(from_attributes=True)
- [ ] Field() có description
- [ ] Validation rules đầy đủ
- [ ] @field_validator cho custom validation
- [ ] Không có circular imports

### 7. Repositories
- [ ] Extend từ BaseRepository
- [ ] Sử dụng async/await
- [ ] Type hints cho return types
- [ ] Error handling proper
- [ ] Close connections properly

### 8. Services
- [ ] Business logic rõ ràng
- [ ] Không có database calls trực tiếp (qua repository)
- [ ] Validation rules
- [ ] Error handling
- [ ] Transaction management

### 9. API Endpoints
- [ ] HTTP method đúng (GET, POST, PUT, DELETE)
- [ ] Path parameters đúng convention
- [ ] Response model được define
- [ ] Status code appropriate
- [ ] Dependencies đúng (authentication, authorization)
- [ ] Docstring cho endpoint
- [ ] Tags cho grouping

### 10. Tests
- [ ] Có test file cho mọi module
- [ ] Test coverage > 80%
- [ ] Test cases cover happy path
- [ ] Test cases cover error cases
- [ ] Test cases có docstrings
- [ ] Fixtures được reuse
- [ ] pytest.mark decorators đúng

---

## ✅ CHECKLIST SAU KHI GENERATE CODE

### 1. Code Quality
- [ ] Black formatted (max line length 88)
- [ ] No Pylint errors
- [ ] No Mypy errors
- [ ] No flake8 warnings

### 2. Functionality
- [ ] Code runs without errors
- [ ] All imports work
- [ ] Database migrations work
- [ ] API endpoints respond
- [ ] Tests pass

### 3. Documentation
- [ ] OpenAPI docs accessible
- [ ] Endpoints có descriptions
- [ ] Schemas có examples
- [ ] README updated (nếu cần)

### 4. Security
- [ ] No hardcoded secrets
- [ ] Passwords are hashed
- [ ] SQL injection protected (ORM)
- [ ] XSS protected (Pydantic validation)
- [ ] CORS configured properly
- [ ] Authentication required where needed
- [ ] Authorization checked

### 5. Performance
- [ ] N+1 queries avoided
- [ ] Proper indexes
- [ ] Async operations used
- [ ] Connection pooling configured

---

## ✅ CHECKLIST PHASE-SPECIFIC

### Phase 1: Foundation
- [ ] FastAPI app starts
- [ ] Database connects
- [ ] Health check works
- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens generated
- [ ] Protected endpoints work
- [ ] RBAC permissions work
- [ ] Docker containers run
- [ ] Tests pass > 80% coverage

### Phase 2: Master Data
- [ ] Supplier CRUD works
- [ ] Product CRUD works
- [ ] Restaurant CRUD works
- [ ] Product mapping works
- [ ] Pagination works
- [ ] Filters work
- [ ] All relationships work
- [ ] Tests pass > 80% coverage

### Phase 3: YCMS Management
- [ ] YCMS CRUD works
- [ ] YCMS workflow works
- [ ] Status transitions work
- [ ] Email notifications sent
- [ ] Permissions respected
- [ ] Bulk import works
- [ ] Tests pass > 80% coverage

### Phase 4: Delivery Note
- [ ] Delivery note creation works
- [ ] Link to YCMS works
- [ ] Status tracking works
- [ ] Email notifications sent
- [ ] Tests pass > 80% coverage

### Phase 5: Notification & Reports
- [ ] In-app notifications work
- [ ] Email notifications work
- [ ] Reports generate correctly
- [ ] Export works
- [ ] Tests pass > 80% coverage

### Phase 6: Testing & Deployment
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Security scan pass
- [ ] Performance tests pass
- [ ] Production deployment successful

---

## ✅ ACCEPTANCE CRITERIA CHECKLIST

### General
- [ ] Code follows PEP 8
- [ ] Type hints: 100%
- [ ] Docstrings: 100%
- [ ] Test coverage: > 80%
- [ ] No security vulnerabilities
- [ ] Response time < 200ms (95th percentile)

### User Registration
- [ ] Accepts valid email & password
- [ ] Validates email format
- [ ] Enforces password strength
- [ ] Returns 201 Created
- [ ] Returns user object with ID
- [ ] Password is hashed
- [ ] Duplicate email returns 400

### User Login
- [ ] Accepts email & password
- [ ] Returns JWT token
- [ ] Returns 401 for invalid credentials
- [ ] Token expires after configured time
- [ ] Updates last_login timestamp

### Protected Endpoints
- [ ] Requires Authorization header
- [ ] Validates JWT token
- [ ] Returns 401 if token invalid
- [ ] Returns 403 if permission denied
- [ ] Returns user info

### CRUD Operations
- [ ] Create: Returns 201 + created object
- [ ] Read: Returns 200 + object
- [ ] Read: Returns 404 if not found
- [ ] Update: Returns 200 + updated object
- [ ] Update: Returns 404 if not found
- [ ] Delete: Returns 204 No Content
- [ ] Delete: Returns 404 if not found
- [ ] List: Returns paginated results
- [ ] List: Supports filters
- [ ] List: Supports sorting

---

## 📝 VERIFICATION COMMANDS

### Run Tests
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
# Expected: >80% coverage, all tests pass
```

### Check Code Quality
```bash
black app/ tests/ --check
pylint app/
mypy app/
```

### Start Application
```bash
docker-compose up -d
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

### Check OpenAPI Docs
```bash
open http://localhost:8000/api/v1/docs
# Expected: Full API documentation visible
```

### Run Migrations
```bash
alembic upgrade head
# Expected: All migrations applied successfully
```

---

## 🚨 COMMON MISTAKES TO AVOID

### 1. Import Errors
❌ `from app.models import *`  
✅ `from app.models.user import User`

### 2. Type Hints
❌ `def get_user(id): ...`  
✅ `def get_user(id: int) -> Optional[User]: ...`

### 3. Async/Await
❌ `def get_user(id: int): ...`  
✅ `async def get_user(id: int) -> Optional[User]: ...`

### 4. SQLAlchemy 2.0
❌ `name = Column(String(50))`  
✅ `name: Mapped[str] = mapped_column(String(50))`

### 5. Pydantic V2
❌ `class Config: orm_mode = True`  
✅ `model_config = ConfigDict(from_attributes=True)`

### 6. Error Handling
❌ Return None without raising exception  
✅ Raise HTTPException with proper status code

### 7. Secrets
❌ `SECRET_KEY = "hardcoded-secret"`  
✅ `SECRET_KEY: str = Field(..., description="Secret key")`

### 8. Validation
❌ No validation on input  
✅ Use Pydantic Field() with constraints

---

## 🎯 FINAL VERIFICATION

Before marking task as complete:

1. **All Checkboxes Checked** ✅
2. **Tests Pass** ✅
3. **Code Quality Pass** ✅
4. **Acceptance Criteria Met** ✅
5. **Documentation Updated** ✅

If all ✅ → **TASK COMPLETE** 🎉

If any ❌ → **FIX & RECHECK**

---

## 📞 WHEN IN DOUBT

1. **Re-read specifications**
   - PHASE_IMPLEMENTATION_GUIDE.md
   - ENTITY_SPECIFICATION.md
   - PROJECT_OVERVIEW.md

2. **Check examples**
   - Look at existing code
   - Follow same patterns

3. **Verify with tests**
   - Write test first
   - Make test pass

4. **Ask for clarification**
   - Create issue
   - Request specification update

---

**Remember**: **Quality over Speed** 🎯

Production-ready code takes time. Better to do it right than fast.

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: ✅ Ready to Use

