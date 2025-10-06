# README - Tài Liệu Đặc Tả Hệ Thống

## Giới Thiệu

Thư mục này chứa toàn bộ tài liệu đặc tả cho **Hệ Thống Quản Lý Yêu Cầu Mua Sắm (Procurement Management System)** của Aladdin Restaurant Chain.

---

## Cấu Trúc Tài Liệu

### 📋 Tài Liệu Chính

| # | Tên File | Mô Tả | Dành Cho |
|---|----------|-------|----------|
| 1 | [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) | Tổng quan dự án, mục tiêu, phạm vi, timeline | Tất cả stakeholders |
| 2 | [ENTITY_SPECIFICATION.md](./ENTITY_SPECIFICATION.md) | Đặc tả chi tiết các thực thể, thuộc tính, quan hệ | Developers, Architects |
| 3 | [PROCESS_FLOW.md](./PROCESS_FLOW.md) | Luồng nghiệp vụ, use cases, sequence diagrams | Developers, BAs, QA |
| 4 | [API_SPECIFICATION.md](./API_SPECIFICATION.md) | API endpoints, request/response formats | Backend/Frontend Developers |
| 5 | [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md) | Kiến trúc hệ thống, technology stack | Architects, DevOps, Developers |
| 6 | [mota.md](./mota.md) | Mô tả ban đầu từ khách hàng | Reference |

---

## Đọc Theo Vai Trò

### 🎯 Product Owner / Business Analyst
**Đọc theo thứ tự**:
1. PROJECT_OVERVIEW.md - Hiểu tổng quan dự án
2. ENTITY_SPECIFICATION.md (Section 1-10) - Hiểu các thực thể nghiệp vụ
3. PROCESS_FLOW.md (Section 1-3) - Hiểu luồng nghiệp vụ

**Mục đích**: 
- Xác nhận requirements đúng với nhu cầu
- Chuẩn bị cho UAT

---

### 💻 Backend Developer
**Đọc theo thứ tự**:
1. PROJECT_OVERVIEW.md (Section 1-4) - Context
2. ENTITY_SPECIFICATION.md - Thiết kế database
3. API_SPECIFICATION.md - API cần implement
4. PROCESS_FLOW.md (Section 2-3) - Business logic
5. SYSTEM_ARCHITECTURE.md (Section 3-6) - Tech stack & patterns

**Mục đích**:
- Implement models, repositories, services, APIs
- Đảm bảo logic nghiệp vụ đúng

---

### 🎨 Frontend Developer
**Đọc theo thứ tự**:
1. PROJECT_OVERVIEW.md (Section 1-3, Appendix A) - Context & User personas
2. PROCESS_FLOW.md (Section 2-3) - Hiểu user flows
3. API_SPECIFICATION.md - API integration
4. SYSTEM_ARCHITECTURE.md (Section 3.2.1) - API authentication

**Mục đích**:
- Thiết kế UI/UX flows
- Integrate với backend APIs
- Implement user interactions

---

### 🏗️ System Architect / Tech Lead
**Đọc tất cả**, đặc biệt:
- SYSTEM_ARCHITECTURE.md (toàn bộ)
- ENTITY_SPECIFICATION.md (quan hệ, indexes)
- API_SPECIFICATION.md (scalability, security)

**Mục đích**:
- Đánh giá kiến trúc
- Đưa ra quyết định kỹ thuật
- Review code

---

### 🔧 DevOps Engineer
**Đọc theo thứ tự**:
1. PROJECT_OVERVIEW.md (Section 4) - NFRs
2. SYSTEM_ARCHITECTURE.md (Section 8-11) - Deployment, monitoring, DR

**Mục đích**:
- Setup infrastructure
- CI/CD pipeline
- Monitoring & alerting

---

### ✅ QA Engineer
**Đọc theo thứ tự**:
1. PROJECT_OVERVIEW.md (Section 6) - Success criteria
2. ENTITY_SPECIFICATION.md - Data validation rules
3. PROCESS_FLOW.md (Section 2-4) - Test scenarios
4. API_SPECIFICATION.md - API test cases

**Mục đích**:
- Viết test plans
- Test cases
- Automation tests

---

## Quick Reference

### 🔑 Key Entities
```
User → (Aladdin | Supplier)
    ↓
ProcurementRequest (YCMS)
    └→ ProcurementRequestItem
        ↓
    DeliveryNote
        └→ DeliveryNoteItem
```
👉 Chi tiết: [ENTITY_SPECIFICATION.md](./ENTITY_SPECIFICATION.md)

---

### 🔄 Main Process Flow
```
1. Aladdin tạo YCMS
2. Submit → Email to Suppliers
3. Supplier xem & cập nhật
4. Supplier tạo Delivery Note
5. Aladdin xác nhận nhận hàng
```
👉 Chi tiết: [PROCESS_FLOW.md](./PROCESS_FLOW.md)

---

### 🛠️ Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Queue**: Celery + Redis
- **Deployment**: Docker, Kubernetes

👉 Chi tiết: [SYSTEM_ARCHITECTURE.md](./SYSTEM_ARCHITECTURE.md)

---

### 📊 Core APIs
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/procurement-requests` - List YCMS
- `POST /api/v1/procurement-requests` - Create YCMS
- `POST /api/v1/procurement-requests/{id}/submit` - Submit YCMS
- `POST /api/v1/delivery-notes` - Create Delivery Note

👉 Chi tiết: [API_SPECIFICATION.md](./API_SPECIFICATION.md)

---

## How to Use This Documentation

### 1️⃣ For Initial Understanding
Read in this order:
1. PROJECT_OVERVIEW.md
2. PROCESS_FLOW.md (Section 1-2)
3. ENTITY_SPECIFICATION.md (Sơ đồ quan hệ)

### 2️⃣ For Development
- Keep API_SPECIFICATION.md open while coding
- Refer to ENTITY_SPECIFICATION.md for database schema
- Check PROCESS_FLOW.md for business logic

### 3️⃣ For Review
- ENTITY_SPECIFICATION.md: Database design review
- API_SPECIFICATION.md: API contract review
- SYSTEM_ARCHITECTURE.md: Architecture review

---

## Document Conventions

### 📝 Naming
- **Entities**: PascalCase (e.g., `ProcurementRequest`)
- **Fields**: snake_case (e.g., `created_at`)
- **APIs**: kebab-case (e.g., `/procurement-requests`)
- **Enums**: UPPERCASE (e.g., `SUBMITTED`)

### 🎨 Diagrams
- Use Mermaid syntax for sequence diagrams
- ASCII art for architecture diagrams
- Markdown tables for entity specifications

### 🔢 Versioning
- All documents have version number at the bottom
- Format: `Version: Major.Minor`
- Update "Last Updated" date when changed

---

## Frequently Asked Questions

### Q1: Tại sao cần nhiều tài liệu như vậy?
**A**: Mỗi tài liệu phục vụ một mục đích khác nhau:
- **PROJECT_OVERVIEW**: Cho management, stakeholders
- **ENTITY_SPECIFICATION**: Cho database design
- **PROCESS_FLOW**: Cho business logic implementation
- **API_SPECIFICATION**: Cho API contract
- **SYSTEM_ARCHITECTURE**: Cho technical decisions

### Q2: Tôi chỉ muốn implement một feature, đọc tài liệu nào?
**A**: 
1. Tìm feature trong PROCESS_FLOW.md → Hiểu business flow
2. Tìm entities liên quan trong ENTITY_SPECIFICATION.md
3. Tìm API endpoints trong API_SPECIFICATION.md
4. Implement theo SYSTEM_ARCHITECTURE.md (layered architecture)

### Q3: Tài liệu này có được cập nhật không?
**A**: Có, tài liệu là "living documents":
- Cập nhật khi có thay đổi requirements
- Cập nhật sau mỗi sprint review
- Version control bằng Git

### Q4: Làm sao biết phần nào quan trọng nhất?
**A**: Đọc phần "⭐ MUST READ" trong mỗi tài liệu hoặc follow guide "Đọc Theo Vai Trò" ở trên.

---

## Contributing

### Updating Documentation
1. **Tạo branch mới**: `git checkout -b docs/update-entity-spec`
2. **Chỉnh sửa tài liệu**: Markdown editors (VS Code, Typora)
3. **Commit & Push**: 
   ```bash
   git add .
   git commit -m "docs: update entity specification for audit log"
   git push origin docs/update-entity-spec
   ```
4. **Create Pull Request**: Yêu cầu review từ Tech Lead

### Documentation Standards
- ✅ Use clear, concise language
- ✅ Add examples where possible
- ✅ Keep diagrams up-to-date
- ✅ Version & date at the bottom
- ✅ Link between related sections
- ❌ Don't use jargon without explanation
- ❌ Don't make assumptions

---

## Getting Help

### 📧 Contact
- **Tech Lead**: [email@example.com]
- **Product Owner**: [email@example.com]
- **Slack Channel**: #pms-project

### 🐛 Found an Issue?
- Documentation error → Create issue on GitHub
- Clarification needed → Ask in Slack
- Major change → Schedule meeting

---

## Change Log

### Version 1.0 (2025-10-06)
- ✅ Initial documentation created
- ✅ All 5 main documents completed
- ✅ Review & approval by stakeholders

### Future Updates
- [ ] Add deployment guide (after setup)
- [ ] Add developer guide (after environment setup)
- [ ] Add user manuals (before UAT)
- [ ] Add API examples (during development)

---

## Document Status

| Document | Status | Last Review | Reviewer |
|----------|--------|-------------|----------|
| PROJECT_OVERVIEW.md | ✅ Approved | 2025-10-06 | Product Owner |
| ENTITY_SPECIFICATION.md | ✅ Approved | 2025-10-06 | Tech Lead |
| PROCESS_FLOW.md | ✅ Approved | 2025-10-06 | Business Analyst |
| API_SPECIFICATION.md | ✅ Approved | 2025-10-06 | Tech Lead |
| SYSTEM_ARCHITECTURE.md | ✅ Approved | 2025-10-06 | System Architect |

---

## Next Steps

### For Team
1. ✅ Read relevant documentation based on your role
2. ⏳ Set up development environment (see DEVELOPER_GUIDE.md - coming soon)
3. ⏳ Sprint 1 kickoff (Week 4)

### For Stakeholders
1. ✅ Review & approve documentation
2. ⏳ Prepare test data (products, suppliers, restaurants)
3. ⏳ Schedule training sessions

---

## Appendix: Document Map

```
specification/description/
│
├── README.md (this file) ...................... 📖 Start here
│
├── mota.md .................................... 📝 Original requirements
│
├── PROJECT_OVERVIEW.md ........................ 🎯 High-level overview
│   ├── Context & Problems
│   ├── Goals & Scope
│   ├── Timeline & Team
│   └── Success Criteria
│
├── ENTITY_SPECIFICATION.md .................... 🗄️ Database design
│   ├── User, Supplier, Restaurant
│   ├── Product, ProductCategory, SupplierProduct
│   ├── ProcurementRequest, ProcurementRequestItem
│   ├── DeliveryNote, DeliveryNoteItem
│   ├── Notification, AuditLog
│   └── Relationships & Constraints
│
├── PROCESS_FLOW.md ............................ 🔄 Business flows
│   ├── Main Flow (end-to-end)
│   ├── YCMS Management Flow
│   ├── Delivery Note Flow
│   ├── Notification Flow
│   └── Error Handling
│
├── API_SPECIFICATION.md ....................... 🔌 API contracts
│   ├── Authentication APIs
│   ├── YCMS APIs
│   ├── Delivery Note APIs
│   ├── Product/Supplier/Restaurant APIs
│   ├── Notification APIs
│   └── Report APIs
│
└── SYSTEM_ARCHITECTURE.md ..................... 🏗️ System design
    ├── Technology Stack
    ├── Layered Architecture
    ├── Database Design
    ├── Security
    ├── Scalability
    ├── Monitoring
    └── Deployment
```

---

**Tài liệu này được tạo bởi**: System Architect & Technical Writing Team  
**Ngày tạo**: 2025-10-06  
**Phiên bản**: 1.0  
**Trạng thái**: ✅ Approved for Development

---

**Happy Coding! 🚀**
