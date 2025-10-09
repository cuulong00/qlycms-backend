# ĐẶC TẢ DỰ ÁN: HỆ THỐNG QUẢN LÝ YÊU CẦU MUA SẮM (YCMS)
## Procurement Management System for Aladdin Restaurant Chain

---

**Version**: 1.0  
**Last Updated**: 2025-10-08  
**Status**: ✅ Ready for Development  
**Author**: System Architect  

---

## 📋 1. TỔNG QUAN DỰ ÁN

### 1.1. Bối Cảnh (Context)

**Aladdin Restaurant Chain** là chuỗi nhà hàng với **100 cơ sở** trên toàn quốc, đang gặp phải các vấn đề sau:

#### 🔴 Vấn Đề Hiện Tại

1. **Quản lý thủ công**: Toàn bộ quy trình yêu cầu mua sắm (YCMS) và giao hàng đang được thực hiện thủ công
2. **Thiếu đồng nhất**: Mỗi nhà cung cấp có cách đặt tên sản phẩm, quy cách đóng gói khác nhau
3. **Khó kiểm soát**: Không có hệ thống tập trung để theo dõi phiếu YCMS và phiếu giao hàng
4. **Thiếu minh bạch**: User Aladdin và User nhà cung cấp không có công cụ để theo dõi trạng thái đơn hàng
5. **Lãng phí thời gian**: Việc bóc tách YCMS thành phiếu giao hàng mất nhiều thời gian

#### 🎯 Mục Tiêu Giải Quyết

- ✅ **Tự động hóa** quy trình tạo và quản lý YCMS
- ✅ **Đồng nhất** danh mục sản phẩm, đơn vị tính, giá cả giữa các nhà cung cấp
- ✅ **Minh bạch hóa** thông tin cho cả Aladdin và nhà cung cấp
- ✅ **Tăng hiệu quả** trong việc tạo và theo dõi phiếu giao hàng
- ✅ **Giảm sai sót** do nhập liệu thủ công

---

## 🎯 2. MỤC TIÊU VÀ PHẠM VI

### 2.1. Mục Tiêu Dự Án (Goals)

#### A. Mục Tiêu Nghiệp Vụ (Business Goals)
- Giảm 80% thời gian xử lý YCMS
- Tăng độ chính xác lên 95% (giảm sai sót do thủ công)
- Cung cấp khả năng theo dõi realtime cho cả 2 bên
- Đồng nhất 100% danh mục sản phẩm

#### B. Mục Tiêu Kỹ Thuật (Technical Goals)
- Xây dựng REST API chuẩn production với FastAPI
- Hỗ trợ 1000+ concurrent users
- Response time < 200ms cho 95% requests
- Uptime 99.9%
- Tích hợp email notification tự động

### 2.2. Phạm Vi Dự Án (Scope)

#### ✅ Trong Phạm Vi (In Scope)

1. **User Management**
   - Đăng ký, đăng nhập, phân quyền
   - 2 loại user: Aladdin Staff, Supplier Staff
   - RBAC với Casbin

2. **Quản Lý Danh Mục (Master Data)**
   - Quản lý danh sách sản phẩm (Product)
   - Quản lý nhà cung cấp (Supplier)
   - Quản lý nhà hàng/cơ sở (Restaurant)
   - Mapping sản phẩm giữa Aladdin và Supplier

3. **Quản Lý Phiếu Yêu Cầu Mua Sắm (YCMS)**
   - Tạo YCMS (Aladdin)
   - Xem danh sách YCMS
   - Cập nhật thông tin YCMS (Supplier)
   - Submit YCMS → Gửi email tự động
   - Theo dõi trạng thái YCMS

4. **Quản Lý Phiếu Giao Hàng (Delivery Note)**
   - Tạo phiếu giao hàng từ YCMS (Supplier)
   - Xem danh sách phiếu giao hàng
   - Cập nhật trạng thái giao hàng
   - Xác nhận nhận hàng (Aladdin)

5. **Notification System**
   - Email notification khi submit YCMS
   - Email notification khi tạo phiếu giao hàng
   - In-app notifications

6. **Reporting & Analytics**
   - Báo cáo YCMS theo nhà cung cấp
   - Báo cáo phiếu giao hàng theo nhà hàng
   - Dashboard tổng quan

#### ❌ Ngoài Phạm Vi (Out of Scope)

- Thanh toán online
- Quản lý kho (Inventory Management)
- Mobile app (Phase 2)
- Integration với ERP (Phase 2)
- Quản lý chất lượng sản phẩm

---

## 👥 3. CÁC BÊN LIÊN QUAN (STAKEHOLDERS)

### 3.1. User Personas

#### A. Aladdin Staff (Purchasing Manager)
**Vai trò**: Quản lý mua sắm của Aladdin  
**Quyền hạn**:
- Tạo và submit YCMS
- Xem tất cả YCMS của tất cả nhà cung cấp
- Xem tất cả phiếu giao hàng
- Xác nhận nhận hàng
- Quản lý danh mục sản phẩm
- Quản lý nhà cung cấp
- Quản lý nhà hàng

**Nhu cầu**:
- Tạo YCMS nhanh chóng cho nhiều nhà hàng
- Theo dõi trạng thái YCMS realtime
- Xem báo cáo tổng quan
- Nhận thông báo khi supplier cập nhật

#### B. Supplier Staff (Supplier Manager)
**Vai trò**: Nhân viên của nhà cung cấp  
**Quyền hạn**:
- Xem YCMS của công ty mình
- Cập nhật thông tin YCMS (giá, số lượng phê duyệt)
- Tạo phiếu giao hàng từ YCMS
- Xem phiếu giao hàng của công ty mình
- Cập nhật trạng thái giao hàng

**Nhu cầu**:
- Nhận notification khi có YCMS mới
- Xem YCMS một cách rõ ràng
- Dễ dàng tạo phiếu giao hàng từ YCMS
- Theo dõi trạng thái giao hàng

### 3.2. System Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| **Super Admin** | Quản trị hệ thống | Full access to all resources |
| **Aladdin Admin** | Quản lý Aladdin | Manage YCMS, view all, manage master data |
| **Aladdin Staff** | Nhân viên Aladdin | Create YCMS, view all, confirm delivery |
| **Supplier Admin** | Quản lý nhà cung cấp | Manage own YCMS, create delivery notes |
| **Supplier Staff** | Nhân viên nhà cung cấp | View own YCMS, update delivery status |

---

## 📊 4. YÊU CẦU PHI CHỨC NĂNG (NFRs)

### 4.1. Performance Requirements

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Response Time (95th percentile) | < 200ms | API monitoring |
| Response Time (99th percentile) | < 500ms | API monitoring |
| Throughput | 1000 req/s | Load testing |
| Concurrent Users | 1000+ | Load testing |
| Database Query Time | < 50ms | Query profiling |

### 4.2. Scalability Requirements

- **Horizontal Scaling**: Hỗ trợ scale out với load balancer
- **Database**: PostgreSQL with read replicas
- **Caching**: Redis cho session và frequently accessed data
- **Async Processing**: Celery cho email notifications

### 4.3. Security Requirements

- **Authentication**: JWT tokens với FastAPI-Users
- **Authorization**: RBAC với Casbin
- **Password**: Bcrypt hashing
- **HTTPS**: Bắt buộc trong production
- **CORS**: Whitelist origins
- **Rate Limiting**: 100 requests/minute/user
- **SQL Injection**: Protected by SQLAlchemy ORM
- **XSS**: Protected by Pydantic validation

### 4.4. Availability & Reliability

- **Uptime**: 99.9% (8.76 hours downtime/year)
- **Backup**: Daily automated backups, 30-day retention
- **Disaster Recovery**: RPO < 1 hour, RTO < 4 hours
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with ELK stack

### 4.5. Maintainability

- **Code Coverage**: > 80%
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Code Style**: Black formatter, Pylint
- **Type Hints**: 100% coverage
- **Git Flow**: Feature branches, PR reviews

---

## 🗓️ 5. TIMELINE & MILESTONES

### 5.1. Project Phases

```
Phase 1: Foundation (Week 1-2)
├── Sprint 1.1: Setup & Core Infrastructure (Week 1)
└── Sprint 1.2: Authentication & Authorization (Week 2)

Phase 2: Master Data (Week 3-4)
├── Sprint 2.1: Product & Supplier Management (Week 3)
└── Sprint 2.2: Restaurant & Product Mapping (Week 4)

Phase 3: YCMS Management (Week 5-7)
├── Sprint 3.1: YCMS CRUD Operations (Week 5)
├── Sprint 3.2: YCMS Workflow & Email (Week 6)
└── Sprint 3.3: YCMS Advanced Features (Week 7)

Phase 4: Delivery Note Management (Week 8-9)
├── Sprint 4.1: Delivery Note Creation (Week 8)
└── Sprint 4.2: Delivery Note Tracking (Week 9)

Phase 5: Notification & Reporting (Week 10-11)
├── Sprint 5.1: Notification System (Week 10)
└── Sprint 5.2: Reports & Dashboard (Week 11)

Phase 6: Testing & Deployment (Week 12)
├── Integration Testing
├── UAT
└── Production Deployment
```

### 5.2. Detailed Phase Breakdown

#### **PHASE 1: Foundation (Week 1-2)** ✅

**Sprint 1.1: Setup & Core Infrastructure (Week 1)**
- [ ] Setup project structure
- [ ] Configure FastAPI + SQLAlchemy 2.0
- [ ] Setup Alembic migrations
- [ ] Configure Pydantic V2 settings
- [ ] Docker + Docker Compose
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Health check endpoint

**Sprint 1.2: Authentication & Authorization (Week 2)**
- [ ] FastAPI-Users integration
- [ ] User model & schemas
- [ ] Login/Register endpoints
- [ ] JWT token strategy
- [ ] Casbin RBAC setup
- [ ] Role & permission management
- [ ] Unit tests for auth

**Deliverables**:
- Working auth system
- Docker environment
- CI/CD pipeline
- 80%+ test coverage

---

#### **PHASE 2: Master Data (Week 3-4)** 📦

**Sprint 2.1: Product & Supplier Management (Week 3)**
- [ ] Product model & CRUD
- [ ] Product category management
- [ ] Supplier model & CRUD
- [ ] Supplier-Product mapping
- [ ] API endpoints for products
- [ ] API endpoints for suppliers
- [ ] Unit tests

**Sprint 2.2: Restaurant & Product Mapping (Week 4)**
- [ ] Restaurant model & CRUD
- [ ] Department/Branch management
- [ ] Product unit conversion
- [ ] Supplier product catalog
- [ ] API endpoints for restaurants
- [ ] Integration tests

**Deliverables**:
- Complete master data APIs
- Product-Supplier mapping
- Swagger documentation
- Test coverage > 80%

---

#### **PHASE 3: YCMS Management (Week 5-7)** 📝

**Sprint 3.1: YCMS CRUD Operations (Week 5)**
- [ ] ProcurementRequest model (orders table)
- [ ] ProcurementRequestItem model (order_details)
- [ ] Create YCMS endpoint
- [ ] List YCMS endpoint (with filters)
- [ ] Get YCMS by ID
- [ ] Update YCMS endpoint
- [ ] Delete YCMS endpoint (soft delete)
- [ ] Aladdin vs Supplier view permissions
- [ ] Unit tests

**Sprint 3.2: YCMS Workflow & Email (Week 6)**
- [ ] YCMS status workflow (Draft → Submitted → Approved → Completed)
- [ ] Submit YCMS endpoint
- [ ] Email notification setup (Celery + Redis)
- [ ] Email template for YCMS submission
- [ ] Send email to suppliers
- [ ] YCMS approval flow
- [ ] Integration tests

**Sprint 3.3: YCMS Advanced Features (Week 7)**
- [ ] Bulk import YCMS from Excel
- [ ] YCMS validation rules
- [ ] YCMS versioning
- [ ] YCMS search & filters
- [ ] YCMS statistics
- [ ] Performance optimization
- [ ] Load testing

**Deliverables**:
- Complete YCMS management
- Email notification working
- Bulk import feature
- Performance tested

---

#### **PHASE 4: Delivery Note Management (Week 8-9)** 🚚

**Sprint 4.1: Delivery Note Creation (Week 8)**
- [ ] DeliveryNote model (receipts table)
- [ ] DeliveryNoteItem model (receipt_details)
- [ ] Create delivery note from YCMS
- [ ] Link delivery note to YCMS
- [ ] Multiple delivery notes per YCMS
- [ ] Delivery note validation
- [ ] API endpoints
- [ ] Unit tests

**Sprint 4.2: Delivery Note Tracking (Week 9)**
- [ ] Delivery status workflow
- [ ] Update delivery status
- [ ] Confirm delivery (Aladdin)
- [ ] Delivery note history
- [ ] Email notification for delivery
- [ ] Delivery note search & filters
- [ ] Integration tests

**Deliverables**:
- Complete delivery note system
- Status tracking
- Email notifications
- Test coverage > 80%

---

#### **PHASE 5: Notification & Reporting (Week 10-11)** 📊

**Sprint 5.1: Notification System (Week 10)**
- [ ] Notification model
- [ ] In-app notification
- [ ] Email notification queue
- [ ] Notification preferences
- [ ] Mark as read/unread
- [ ] Notification history
- [ ] Real-time notifications (WebSocket - optional)

**Sprint 5.2: Reports & Dashboard (Week 11)**
- [ ] YCMS report by supplier
- [ ] YCMS report by date range
- [ ] Delivery note report by restaurant
- [ ] Delivery status summary
- [ ] Dashboard statistics API
- [ ] Export to Excel/PDF
- [ ] Caching for reports

**Deliverables**:
- Working notification system
- Comprehensive reports
- Dashboard APIs
- Export functionality

---

#### **PHASE 6: Testing & Deployment (Week 12)** 🚀

**Sprint 6.1: Testing & Bug Fixing (Week 12)**
- [ ] Integration testing
- [ ] End-to-end testing
- [ ] Security testing (OWASP)
- [ ] Performance testing
- [ ] UAT with stakeholders
- [ ] Bug fixing
- [ ] Documentation

**Sprint 6.2: Production Deployment (Week 12)**
- [ ] Production environment setup
- [ ] Database migration
- [ ] SSL certificate setup
- [ ] Load balancer configuration
- [ ] Monitoring & alerting
- [ ] Backup & disaster recovery
- [ ] Go-live

**Deliverables**:
- Production-ready system
- Complete documentation
- Monitoring dashboard
- User training materials

---

## 🎓 6. TIÊU CHÍ THÀNH CÔNG (SUCCESS CRITERIA)

### 6.1. Technical Success Criteria

- [ ] All APIs documented with OpenAPI/Swagger
- [ ] Test coverage > 80%
- [ ] No critical security vulnerabilities
- [ ] Response time < 200ms (95th percentile)
- [ ] Zero downtime deployment
- [ ] Automated CI/CD pipeline

### 6.2. Business Success Criteria

- [ ] 100% YCMS processed through system
- [ ] 95%+ user satisfaction
- [ ] 80% reduction in processing time
- [ ] 95%+ data accuracy
- [ ] All suppliers onboarded

### 6.3. Acceptance Criteria

1. **Functional Requirements**
   - Aladdin can create and submit YCMS
   - Suppliers receive email notifications
   - Suppliers can create delivery notes
   - Aladdin can confirm deliveries
   - Reports are accurate

2. **Non-Functional Requirements**
   - System handles 1000 concurrent users
   - 99.9% uptime
   - All data encrypted in transit
   - Audit trail for all changes

3. **User Acceptance**
   - UAT signed off by stakeholders
   - Training completed for all users
   - User manual provided

---

## 📚 APPENDIX

### A. Glossary

| Term | Definition |
|------|------------|
| **YCMS** | Yêu Cầu Mua Sắm (Procurement Request) |
| **Aladdin** | The restaurant chain company |
| **Supplier** | Nhà cung cấp nguyên liệu, thực phẩm |
| **Restaurant** | Nhà hàng/cơ sở của Aladdin |
| **Delivery Note** | Phiếu giao hàng |
| **RBAC** | Role-Based Access Control |

### B. References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [FastAPI-Users Documentation](https://fastapi-users.github.io/fastapi-users/)
- [Casbin Documentation](https://casbin.org/docs/overview)

### C. Related Documents

- `ENTITY_SPECIFICATION.md` - Chi tiết về các entity và database schema
- `PROCESS_FLOW.md` - Luồng nghiệp vụ chi tiết
- `API_SPECIFICATION.md` - Chi tiết về API endpoints
- `SYSTEM_ARCHITECTURE.md` - Kiến trúc hệ thống

---

**Document Status**: ✅ Ready for Development  
**Next Action**: Review and approve → Start Phase 1  
**Owner**: Technical Lead  
**Last Review**: 2025-10-08

---

