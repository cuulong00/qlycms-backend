# README - HƯỚNG DẪN SỬ DỤNG ĐẶC TẢ CHO LLM

## 🤖 Dành Cho LLM Auto-Coding

Thư mục này chứa **đặc tả đầy đủ** cho LLM có thể **tự động generate production-ready code** cho Hệ Thống Quản Lý Yêu Cầu Mua Sắm (YCMS).

---

## 🎯 MỤC TIÊU

✅ LLM có thể tự động code **toàn bộ backend** từ đầu đến cuối  
✅ Code generated phải đạt chuẩn **production-ready**  
✅ Bao gồm **models, schemas, APIs, tests, migrations**  
✅ Tuân thủ **best practices, security, performance**  

---

## 📚 CẤU TRÚC TÀI LIỆU (LLM Must Read)

### ⭐ BƯỚC 1: ĐỌC PROJECT OVERVIEW
**File**: [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)

**Mục đích**: Hiểu tổng quan dự án
- Bối cảnh & vấn đề cần giải quyết
- Mục tiêu & phạm vi dự án
- Timeline & phases (12 weeks)
- Stakeholders & user personas
- Success criteria

**Thời gian đọc**: 15 phút  
**Action**: Nắm được big picture trước khi code

---

### ⭐ BƯỚC 2: ĐỌC PHASE IMPLEMENTATION GUIDE
**File**: [PHASE_IMPLEMENTATION_GUIDE.md](./PHASE_IMPLEMENTATION_GUIDE.md)

**Mục đích**: Hướng dẫn từng bước code theo phase
- **Phase 1**: Foundation (Week 1-2)
  - Project setup
  - FastAPI + SQLAlchemy + Alembic
  - Authentication với FastAPI-Users
  - Authorization với Casbin
  - Docker & CI/CD
  
- **Phase 2**: Master Data (Week 3-4)
  - Supplier, Product, Restaurant CRUD
  - Product mapping
  
- **Phase 3**: YCMS Management (Week 5-7)
  - Procurement Request CRUD
  - Workflow & Email notifications
  
- **Phase 4**: Delivery Note (Week 8-9)
- **Phase 5**: Notification & Reports (Week 10-11)
- **Phase 6**: Testing & Deployment (Week 12)

**Thời gian đọc**: 30 phút  
**Action**: Follow từng task một để code

---

### ⭐ BƯỚC 3: ĐỌC ENTITY SPECIFICATION
**File**: [ENTITY_SPECIFICATION.md](./ENTITY_SPECIFICATION.md)

**Mục đích**: Chi tiết về database & models
- ER Diagram tổng quan
- Chi tiết từng entity:
  - User
  - Supplier
  - Product & ProductCategory
  - Restaurant
  - ProcurementRequest & Items
  - DeliveryNote & Items
  - Notification
  - AuditLog
- SQLAlchemy models với type hints
- Pydantic schemas
- Alembic migrations
- Relationships & constraints

**Thời gian đọc**: 45 phút  
**Action**: Copy-paste models & schemas vào code

---

### 📖 BƯỚC 4: THAM KHẢO KHÁC

**File**: [mota.md](./mota.md) - Mô tả gốc từ khách hàng (tham khảo nếu cần)

---

## 🚀 HƯỚNG DẪN SỬ DỤNG CHO LLM

### Workflow Để Generate Code

```
1. Đọc PROJECT_OVERVIEW.md 
   → Hiểu context, goals, timeline
   
2. Đọc PHASE_IMPLEMENTATION_GUIDE.md
   → Chọn phase cần code (bắt đầu từ Phase 1)
   
3. Đọc ENTITY_SPECIFICATION.md
   → Lấy models, schemas, migrations
   
4. Generate Code theo từng task trong Phase
   → Copy code templates
   → Customize theo requirements
   → Add tests
   
5. Verify với Acceptance Criteria
   → Check tất cả criteria pass
   → Run tests
   → Verify OpenAPI docs
   
6. Next Task/Phase
   → Tiếp tục với task tiếp theo
```

---

## 📝 TEMPLATE CODE MẪU

### Example: Generate User Model

**Input từ LLM:**
> Generate User model theo đặc tả ENTITY_SPECIFICATION.md section 1

**Output Expected:**

```python
# app/models/user.py
"""
User model với FastAPI-Users integration
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable

from app.models.base import Base, TimestampMixin
import enum


class UserType(str, enum.Enum):
    """User type enumeration"""
    ALADDIN = "aladdin"
    SUPPLIER = "supplier"


class UserRole(str, enum.Enum):
    """User role enumeration"""
    SUPER_ADMIN = "super_admin"
    ALADDIN_ADMIN = "aladdin_admin"
    ALADDIN_STAFF = "aladdin_staff"
    SUPPLIER_ADMIN = "supplier_admin"
    SUPPLIER_STAFF = "supplier_staff"


class User(SQLAlchemyBaseUserTable[int], Base, TimestampMixin):
    """User model"""
    
    __tablename__ = "users"
    
    # ... (rest of the code from ENTITY_SPECIFICATION.md)
```

**Verify:**
- [ ] Model có đầy đủ fields theo spec
- [ ] Type hints đầy đủ
- [ ] Relationships đúng
- [ ] Indexes đúng
- [ ] Comments đầy đủ

---

## ✅ ACCEPTANCE CRITERIA

### Phase 1 Completed Khi:
- [ ] All models created with type hints
- [ ] All schemas created with validation
- [ ] All migrations generated and applied
- [ ] All API endpoints working
- [ ] OpenAPI docs accessible
- [ ] All tests passing (>80% coverage)
- [ ] Docker containers running
- [ ] CI/CD pipeline working

### Code Quality Standards:
- [ ] Type hints: 100%
- [ ] Docstrings: 100%
- [ ] Tests coverage: >80%
- [ ] Black formatted
- [ ] Pylint score: >8.0
- [ ] No security vulnerabilities
- [ ] API response time: <200ms (95th percentile)

---

## 🔄 PROCESS FLOW

### Phase 1: Foundation

```
Week 1:
├── Day 1-2: Project Setup
│   ├── Create folder structure
│   ├── Setup dependencies
│   ├── Configure FastAPI
│   └── Setup Docker
├── Day 3-4: Database Setup
│   ├── SQLAlchemy config
│   ├── Alembic setup
│   └── Base models
└── Day 5: Testing & CI/CD
    ├── Pytest setup
    └── GitHub Actions

Week 2:
├── Day 1-2: User Model
│   ├── Create User model
│   ├── Create migration
│   └── Create schemas
├── Day 3-4: FastAPI-Users
│   ├── Setup FastAPI-Users
│   ├── Auth endpoints
│   └── JWT strategy
└── Day 5: Casbin Authorization
    ├── Setup Casbin
    ├── Define policies
    └── Create dependencies
```

---

## 📊 TECHNOLOGY STACK

```yaml
Language: Python 3.11+

Framework: FastAPI 0.118.0
ORM: SQLAlchemy 2.0.43 (async)
Migration: Alembic 1.16.5
Validation: Pydantic 2.11.10

Authentication: FastAPI-Users 14.0.1
Authorization: Casbin 1.37.6
Password: Passlib (bcrypt)
JWT: Python-JOSE

Database: PostgreSQL 15+
Cache: Redis 7+

Testing: Pytest 8.3.0
Coverage: Pytest-cov

Container: Docker + Docker Compose
CI/CD: GitHub Actions
```

---

## 🎯 SUCCESS METRICS

### Technical Metrics
- API Response Time: < 200ms (95th percentile)
- Test Coverage: > 80%
- Code Quality: Pylint > 8.0
- Type Coverage: 100%
- Uptime: 99.9%

### Business Metrics
- 100% YCMS processed through system
- 80% reduction in processing time
- 95%+ user satisfaction
- All suppliers onboarded

---

## 📞 SUPPORT

### For LLM Issues
1. Re-read specifications
2. Check code templates in docs
3. Verify with acceptance criteria
4. Run tests to validate

### For Human Developers
- **Tech Lead**: [email]
- **Product Owner**: [email]
- **Slack**: #ycms-project

---

## 🔗 QUICK LINKS

| Resource | Link |
|----------|------|
| **FastAPI Docs** | https://fastapi.tiangolo.com/ |
| **SQLAlchemy 2.0** | https://docs.sqlalchemy.org/en/20/ |
| **Pydantic V2** | https://docs.pydantic.dev/ |
| **FastAPI-Users** | https://fastapi-users.github.io/ |
| **Casbin** | https://casbin.org/ |

---

## 📅 CHANGE LOG

### Version 1.0 (2025-10-08)
- ✅ Initial specification complete
- ✅ PROJECT_OVERVIEW.md created
- ✅ PHASE_IMPLEMENTATION_GUIDE.md created
- ✅ ENTITY_SPECIFICATION.md (partial) created
- ✅ README for LLM created

### Next Updates
- [ ] Complete ENTITY_SPECIFICATION.md (all entities)
- [ ] Create PROCESS_FLOW.md
- [ ] Create API_SPECIFICATION.md
- [ ] Add more code examples

---

## 🎓 LLM CODING CHECKLIST

### Before Starting
- [ ] Read PROJECT_OVERVIEW.md
- [ ] Read PHASE_IMPLEMENTATION_GUIDE.md
- [ ] Read ENTITY_SPECIFICATION.md

### During Coding
- [ ] Follow phase-by-phase approach
- [ ] Copy code templates
- [ ] Add type hints
- [ ] Add docstrings
- [ ] Write tests
- [ ] Run tests
- [ ] Check coverage

### After Completing Task
- [ ] Verify acceptance criteria
- [ ] Run all tests
- [ ] Check OpenAPI docs
- [ ] Commit code
- [ ] Move to next task

---

**Ready to Code?** 🚀

Start with: **[PHASE_IMPLEMENTATION_GUIDE.md](./PHASE_IMPLEMENTATION_GUIDE.md) → Phase 1 → Sprint 1.1**

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: ✅ Ready for LLM Auto-Coding  
**Target Audience**: LLM, Developers, Tech Leads

