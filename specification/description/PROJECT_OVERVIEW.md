# Tổng Quan Dự Án (Project Overview)

## Thông Tin Chung

**Tên Dự Án**: Hệ Thống Quản Lý Yêu Cầu Mua Sắm - Procurement Management System (PMS)  
**Khách Hàng**: Aladdin Restaurant Chain  
**Phạm Vi**: 100 nhà hàng trên toàn quốc  
**Mục Tiêu**: Số hóa và đồng nhất hóa quy trình mua sắm giữa Aladdin và các nhà cung cấp

---

## 1. Bối Cảnh Dự Án (Project Context)

### 1.1. Vấn Đề Hiện Tại

Aladdin hiện đang vận hành 100 nhà hàng trên toàn quốc và phải quản lý việc mua sắm nguyên liệu, thực phẩm từ nhiều nhà cung cấp khác nhau. Quy trình hiện tại hoàn toàn thủ công và gặp các vấn đề sau:

#### Vấn Đề 1: Thiếu Đồng Nhất Dữ Liệu
- **Quy cách đóng gói khác nhau**: Mỗi nhà cung cấp có cách đóng gói riêng (bao 50kg, thùng 25kg...)
- **Tên sản phẩm khác nhau**: Cùng một sản phẩm nhưng mỗi nhà cung cấp đặt tên khác nhau
- **Đơn vị tính không thống nhất**: kg, bao, thùng, cái...
- **Hậu quả**: Khó khăn trong việc so sánh giá, quản lý kho, báo cáo

#### Vấn Đề 2: Quy Trình Thủ Công
- **Tạo phiếu yêu cầu mua sắm**: Thủ công qua Excel/Email
- **Gửi cho nhà cung cấp**: Email riêng lẻ, dễ bị sót
- **Nhà cung cấp phản hồi**: Qua email/điện thoại, khó theo dõi
- **Tạo phiếu giao hàng**: Nhà cung cấp tự làm, không có chuẩn
- **Theo dõi giao hàng**: Không có công cụ, phụ thuộc vào email/điện thoại
- **Đối soát**: Thủ công, tốn thời gian

#### Vấn Đề 3: Thiếu Minh Bạch
- Aladdin không biết nhà cung cấp đã xem phiếu yêu cầu chưa
- Không biết trạng thái xử lý (đang chuẩn bị, đang giao, đã giao)
- Khó theo dõi lịch sử giao dịch
- Không có báo cáo tự động

### 1.2. Mục Tiêu Dự Án

#### Mục Tiêu Chính
1. **Số hóa quy trình mua sắm**: Từ tạo yêu cầu đến nhận hàng
2. **Đồng nhất dữ liệu**: Tạo danh mục sản phẩm chuẩn, mapping với sản phẩm nhà cung cấp
3. **Tăng tính minh bạch**: Theo dõi được toàn bộ quy trình real-time
4. **Tiết kiệm thời gian**: Tự động hóa các công việc thủ công
5. **Cải thiện quản lý**: Báo cáo, phân tích dữ liệu

#### Mục Tiêu Cụ Thể
- Giảm 70% thời gian tạo và xử lý phiếu yêu cầu mua sắm
- Tăng 50% tốc độ phản hồi của nhà cung cấp
- Giảm 80% lỗi trong đối soát
- 100% phiếu yêu cầu được theo dõi trạng thái real-time
- Tạo được báo cáo tự động hàng ngày/tuần/tháng

---

## 2. Phạm Vi Dự Án (Project Scope)

### 2.1. Trong Phạm Vi (In Scope)

#### Chức Năng Core
1. **Quản lý Người Dùng**
   - Đăng ký, đăng nhập (Aladdin & Nhà cung cấp)
   - Phân quyền theo vai trò
   - Quản lý profile

2. **Quản lý Danh Mục**
   - Sản phẩm chuẩn (Aladdin)
   - Nhà cung cấp
   - Nhà hàng
   - Mapping sản phẩm nhà cung cấp

3. **Phiếu Yêu Cầu Mua Sắm (YCMS)**
   - Tạo, sửa, xóa phiếu YCMS (Aladdin)
   - Submit phiếu YCMS → Gửi email tự động cho nhà cung cấp
   - Xem danh sách phiếu YCMS (filter theo quyền)
   - Cập nhật thông tin items (Nhà cung cấp)
   - Xác nhận items

4. **Phiếu Giao Hàng**
   - Tạo phiếu giao hàng từ YCMS (Nhà cung cấp)
   - Bóc tách theo nhà hàng & ngày giao
   - Submit phiếu giao hàng → Thông báo Aladdin
   - Cập nhật trạng thái giao hàng
   - Xác nhận nhận hàng (Aladdin)
   - Ghi nhận số lượng thực nhận

5. **Thông Báo**
   - Email notification (phiếu mới, cập nhật, trễ hạn)
   - In-app notification
   - Đánh dấu đã đọc

6. **Báo Cáo**
   - Tổng quan mua sắm (theo thời gian, nhà cung cấp, nhà hàng)
   - Hiệu suất giao hàng (đúng hạn, trễ, chênh lệch số lượng)
   - So sánh giá sản phẩm giữa các nhà cung cấp
   - Dashboard tổng quan

7. **Audit & Logging**
   - Ghi log tất cả thay đổi quan trọng
   - Lịch sử thay đổi trạng thái
   - Truy vết người thực hiện

#### Công Nghệ
- Backend API: FastAPI + PostgreSQL
- Authentication: JWT
- Email: SMTP/SendGrid
- Background jobs: Celery + Redis
- Deployment: Docker + Docker Compose (Dev), Kubernetes (Prod)

### 2.2. Ngoài Phạm Vi (Out of Scope) - Phase 1

1. **Quản lý Kho**
   - Nhập/xuất kho
   - Tồn kho
   - Inventory management

2. **Thanh Toán**
   - Tích hợp payment gateway
   - Hóa đơn điện tử
   - Công nợ

3. **Logistics**
   - Theo dõi xe giao hàng real-time
   - GPS tracking
   - Route optimization

4. **Mobile App**
   - Native iOS/Android app
   - (Chỉ có web responsive)

5. **AI/ML Features**
   - Dự đoán nhu cầu mua hàng
   - Gợi ý nhà cung cấp
   - Phát hiện gian lận

6. **Tích Hợp ERP**
   - SAP, Oracle, etc.

### 2.3. Future Enhancements (Phase 2+)

1. Quản lý kho cơ bản
2. Thanh toán online
3. Mobile app
4. Tích hợp với hệ thống kế toán
5. AI gợi ý mua hàng
6. Chatbot hỗ trợ

---

## 3. Stakeholders

### 3.1. Người Dùng Chính

#### 1. Aladdin Users
**a. Aladdin Admin**
- Vai trò: Quản trị hệ thống
- Quyền hạn: Full access
- Số lượng: 2-3 người

**b. Aladdin Manager (Quản lý mua hàng)**
- Vai trò: Tạo và quản lý phiếu YCMS
- Quyền hạn: Tạo/sửa/submit YCMS, xem tất cả báo cáo
- Số lượng: 5-10 người

**c. Aladdin Staff (Nhân viên kho)**
- Vai trò: Xác nhận nhận hàng
- Quyền hạn: Xem YCMS, cập nhật phiếu giao hàng (nhận hàng)
- Số lượng: 100 người (1 người/nhà hàng)

#### 2. Supplier Users
**a. Supplier Admin**
- Vai trò: Quản lý thông tin công ty, nhân viên
- Quyền hạn: Xem/cập nhật profile, quản lý mapping sản phẩm
- Số lượng: ~50 nhà cung cấp × 1 = 50 người

**b. Supplier Staff**
- Vai trò: Xử lý phiếu YCMS, tạo phiếu giao hàng
- Quyền hạn: Xem YCMS của mình, cập nhật, tạo phiếu giao hàng
- Số lượng: ~50 nhà cung cấp × 2-3 = 100-150 người

### 3.2. Stakeholders Khác

1. **Ban Giám Đốc Aladdin**: Xem báo cáo tổng thể
2. **IT Department**: Vận hành, bảo trì hệ thống
3. **Kế Toán**: Sử dụng dữ liệu để đối soát, thanh toán (gián tiếp)
4. **Kho Trung Tâm**: Theo dõi tổng nhu cầu mua hàng

---

## 4. Yêu Cầu Phi Chức Năng (Non-Functional Requirements)

### 4.1. Performance
- **Response Time**: API < 500ms (p95), < 1s (p99)
- **Throughput**: Hỗ trợ 1000+ concurrent users
- **Database Query**: < 100ms (p95)
- **Email Delivery**: < 5 phút
- **Background Job**: < 10 phút

### 4.2. Availability
- **Uptime**: 99.9% (downtime < 8.76 giờ/năm)
- **Maintenance Window**: Chủ nhật 2-4 AM
- **Backup**: Hàng ngày, retention 30 ngày
- **RTO**: 4 giờ
- **RPO**: 6 giờ

### 4.3. Scalability
- **User Growth**: Hỗ trợ tăng lên 200 nhà hàng
- **Data Growth**: 10 triệu records/năm
- **Horizontal Scaling**: Có thể thêm API servers
- **Database**: Read replicas, partitioning

### 4.4. Security
- **Authentication**: JWT with expiry
- **Authorization**: Role-based access control (RBAC)
- **Data Encryption**: TLS 1.3 (in transit), AES-256 (at rest)
- **Password Policy**: Min 8 chars, complexity rules
- **Audit Log**: Tất cả thay đổi quan trọng
- **Rate Limiting**: 100 req/min/user

### 4.5. Usability
- **Responsive**: Hoạt động tốt trên desktop, tablet, mobile
- **Browser Support**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Ngôn ngữ**: Tiếng Việt (primary)
- **Accessibility**: WCAG 2.1 Level AA

### 4.6. Maintainability
- **Code Quality**: Linters (flake8, black, mypy)
- **Test Coverage**: > 80%
- **Documentation**: Code comments, API docs (OpenAPI)
- **Logging**: Structured logging (JSON)
- **Monitoring**: Metrics, alerts, dashboards

### 4.7. Reliability
- **Error Rate**: < 0.1%
- **Data Integrity**: Foreign keys, constraints, transactions
- **Retry Mechanism**: Cho email, background jobs
- **Graceful Degradation**: Hệ thống vẫn hoạt động nếu 1 service down (e.g., email)

---

## 5. Assumptions & Constraints

### 5.1. Assumptions (Giả Định)

1. **Kết Nối Internet**
   - Tất cả users có internet ổn định
   - Không cần offline mode

2. **User Knowledge**
   - Users biết sử dụng web browser cơ bản
   - Có training cho users trước khi go-live

3. **Data Quality**
   - Aladdin sẽ cung cấp danh sách nhà hàng, sản phẩm ban đầu
   - Nhà cung cấp sẽ cung cấp thông tin sản phẩm của mình

4. **Email Delivery**
   - Email service (SendGrid/SES) hoạt động bình thường
   - Users kiểm tra email thường xuyên

5. **Business Process**
   - Aladdin có quy trình mua sắm định kỳ (tuần/tháng)
   - Nhà cung cấp phản hồi trong vòng 24-48h

### 5.2. Constraints (Ràng Buộc)

1. **Thời Gian**
   - Phase 1: 3 tháng (development + testing)
   - Go-live: Quý 1/2026

2. **Ngân Sách**
   - Budget cho infrastructure: Cloud hosting, services
   - Team size: 3-5 developers, 1 QA, 1 DevOps

3. **Kỹ Thuật**
   - Phải sử dụng Python (requirement từ team Aladdin)
   - Database: PostgreSQL (already used in company)
   - Deploy trên AWS/Azure (company policy)

4. **Quy Định**
   - Tuân thủ PDPA (Personal Data Protection Act) - Việt Nam
   - Lưu trữ dữ liệu trong nước (data residency)

5. **Tích Hợp**
   - Không tích hợp với hệ thống cũ (nếu có) trong Phase 1
   - Chỉ tích hợp email

---

## 6. Success Criteria (Tiêu Chí Thành Công)

### 6.1. Business Metrics

| Metric | Baseline (Hiện Tại) | Target (6 tháng sau go-live) |
|--------|---------------------|------------------------------|
| Thời gian tạo phiếu YCMS | 2 giờ/phiếu | 20 phút/phiếu (↓ 83%) |
| Thời gian phản hồi của NCC | 48 giờ | 24 giờ (↓ 50%) |
| Lỗi đối soát | 20%/tháng | 4%/tháng (↓ 80%) |
| Số phiếu xử lý/tháng | 200 | 300 (↑ 50%) |
| User satisfaction | N/A | 4/5 |

### 6.2. Technical Metrics

| Metric | Target |
|--------|--------|
| System Uptime | ≥ 99.9% |
| API Response Time (p95) | ≤ 500ms |
| Page Load Time | ≤ 2s |
| Error Rate | ≤ 0.1% |
| Test Coverage | ≥ 80% |

### 6.3. User Adoption

| Milestone | Target Date | Target |
|-----------|-------------|--------|
| Training Completed | M+1 | 100% users trained |
| First YCMS Created | M+1 | 10 phiếu |
| Active Users (Aladdin) | M+2 | 80% |
| Active Suppliers | M+3 | 70% |
| Full Adoption | M+6 | 95% |

(M = Go-live month)

---

## 7. Risks & Mitigation (Rủi Ro & Giải Pháp)

### 7.1. Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Database performance issues | High | Medium | - Proper indexing<br>- Query optimization<br>- Read replicas |
| Email delivery failure | Medium | Low | - Retry mechanism<br>- Multiple email providers<br>- In-app notification backup |
| Security breach | High | Low | - Security audit<br>- Penetration testing<br>- Regular updates |
| System downtime | High | Low | - High availability setup<br>- Auto-scaling<br>- Disaster recovery plan |

### 7.2. Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low user adoption | High | Medium | - Extensive training<br>- User-friendly UI<br>- Dedicated support |
| Supplier resistance | Medium | Medium | - Incentives for early adopters<br>- Demonstrate value<br>- Pilot with willing suppliers |
| Data quality issues | Medium | Medium | - Data validation<br>- Data cleansing before migration<br>- Guided data entry |
| Scope creep | High | High | - Strict change control<br>- Prioritization (MoSCoW)<br>- Phase 2 for new features |

### 7.3. Project Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Delay in development | Medium | Medium | - Agile methodology<br>- Regular sprint reviews<br>- Buffer time |
| Key person unavailability | High | Low | - Knowledge sharing<br>- Documentation<br>- Backup resources |
| Budget overrun | Medium | Low | - Regular cost tracking<br>- Cloud cost optimization<br>- Contingency budget |

---

## 8. Project Timeline

### 8.1. High-Level Milestones

| Phase | Duration | Start | End | Deliverables |
|-------|----------|-------|-----|--------------|
| Requirements & Design | 3 weeks | Week 1 | Week 3 | - Spec documents<br>- Database design<br>- API design |
| Development - Sprint 1 | 2 weeks | Week 4 | Week 5 | - User management<br>- Authentication |
| Development - Sprint 2 | 2 weeks | Week 6 | Week 7 | - Product management<br>- Supplier/Restaurant CRUD |
| Development - Sprint 3 | 2 weeks | Week 8 | Week 9 | - YCMS creation & listing |
| Development - Sprint 4 | 2 weeks | Week 10 | Week 11 | - Supplier YCMS update<br>- Notifications |
| Development - Sprint 5 | 2 weeks | Week 12 | Week 13 | - Delivery notes |
| Development - Sprint 6 | 2 weeks | Week 14 | Week 15 | - Reports & Dashboard |
| Testing & Bug Fixing | 2 weeks | Week 16 | Week 17 | - Test reports<br>- Bug fixes |
| UAT | 2 weeks | Week 18 | Week 19 | - UAT sign-off |
| Deployment & Training | 1 week | Week 20 | Week 20 | - Production deployment<br>- User training |
| Go-Live | Week 21 | Week 21 | Week 21 | - System live |
| Post-Launch Support | 4 weeks | Week 21 | Week 24 | - Bug fixes<br>- Optimizations |

**Total Duration**: ~6 months (24 weeks)

### 8.2. Detailed Sprint Plan (Example - Sprint 3)

**Sprint 3: YCMS Creation & Listing (Week 8-9)**

**Goals**:
- Aladdin users can create procurement requests
- List and view procurement requests

**User Stories**:
1. As an Aladdin manager, I want to create a new YCMS so that I can request products from suppliers
2. As an Aladdin manager, I want to add items to YCMS so that I can specify products and quantities
3. As an Aladdin manager, I want to save YCMS as draft so that I can edit it later
4. As an Aladdin user, I want to view list of all YCMS so that I can track requests
5. As a Supplier user, I want to view list of YCMS for my company so that I can see what's requested

**Tasks**:
- [ ] Backend: ProcurementRequest model & repository
- [ ] Backend: ProcurementRequestItem model & repository
- [ ] Backend: YCMS service (create, list, get detail)
- [ ] Backend: API endpoints (POST, GET list, GET detail)
- [ ] Frontend: YCMS creation form
- [ ] Frontend: YCMS listing page
- [ ] Frontend: YCMS detail page
- [ ] Tests: Unit tests, integration tests
- [ ] Documentation: API docs

**Definition of Done**:
- All tasks completed
- Tests passed (> 80% coverage)
- Code reviewed & merged
- Demo to stakeholders

---

## 9. Team Structure

### 9.1. Development Team

**1. Tech Lead / Backend Lead**
- Responsibilities: Architecture, backend development, code review
- Skills: Python, FastAPI, PostgreSQL, Docker

**2. Backend Developer (×2)**
- Responsibilities: Backend development, API implementation
- Skills: Python, FastAPI, SQLAlchemy

**3. Frontend Developer**
- Responsibilities: Frontend development, UI/UX implementation
- Skills: React/Vue, TypeScript, REST API integration

**4. DevOps Engineer**
- Responsibilities: CI/CD, deployment, infrastructure
- Skills: Docker, Kubernetes, AWS/Azure, monitoring

**5. QA Engineer**
- Responsibilities: Testing, bug tracking, test automation
- Skills: Test automation, API testing, Selenium

**6. Product Owner (Aladdin side)**
- Responsibilities: Requirements, priorities, UAT
- Part-time

**7. Scrum Master**
- Responsibilities: Sprint planning, daily standups, retrospectives
- Can be Tech Lead or dedicated person

### 9.2. Communication

**Daily**:
- Daily standup (15 min)
- Slack/Teams for async communication

**Weekly**:
- Sprint planning (Monday)
- Sprint review & demo (Friday)
- Sprint retrospective (Friday)

**Monthly**:
- Stakeholder demo & feedback
- Roadmap review

---

## 10. Documentation Deliverables

### 10.1. Technical Documentation

1. **This Document**: Project Overview
2. **ENTITY_SPECIFICATION.md**: Database schema, entity details
3. **PROCESS_FLOW.md**: Business flows, use cases, sequence diagrams
4. **API_SPECIFICATION.md**: API endpoints, request/response formats
5. **SYSTEM_ARCHITECTURE.md**: System architecture, technology stack
6. **DEPLOYMENT_GUIDE.md**: How to deploy the system
7. **DEVELOPER_GUIDE.md**: How to set up dev environment, coding standards

### 10.2. User Documentation

1. **User Manual (Aladdin)**: How to use the system (Aladdin users)
2. **User Manual (Supplier)**: How to use the system (Supplier users)
3. **FAQ**: Frequently asked questions
4. **Video Tutorials**: Screen recordings for common tasks

### 10.3. Project Management Documents

1. **Project Charter**: High-level overview, goals, stakeholders
2. **Sprint Plans**: Detailed sprint goals, user stories, tasks
3. **Test Plans**: Test cases, test results
4. **UAT Report**: User acceptance testing results
5. **Go-Live Checklist**: Pre-deployment checklist

---

## 11. Next Steps

### 11.1. Immediate Actions (Week 1-2)

1. **Kick-off Meeting**
   - Introduce team
   - Align on goals, timeline
   - Q&A session

2. **Requirements Gathering**
   - Interview stakeholders (Aladdin managers, suppliers)
   - Document detailed requirements
   - Prioritize features (MoSCoW)

3. **Design**
   - Finalize database schema
   - Design UI/UX mockups
   - Get stakeholder approval

4. **Environment Setup**
   - Set up development environment
   - Set up CI/CD pipeline
   - Set up project management tools (Jira, GitHub)

### 11.2. Development Kickoff (Week 3)

1. Sprint 1 planning
2. Start backend skeleton (FastAPI project structure)
3. Start frontend skeleton (React/Vue project)
4. Set up PostgreSQL database
5. Implement authentication (Login/Logout)

---

## 12. Glossary

| Term | Definition |
|------|------------|
| YCMS | Yêu Cầu Mua Sắm - Procurement Request |
| DN | Delivery Note - Phiếu Giao Hàng |
| NCC | Nhà Cung Cấp - Supplier |
| RTO | Recovery Time Objective - Thời gian phục hồi |
| RPO | Recovery Point Objective - Điểm phục hồi dữ liệu |
| UAT | User Acceptance Testing |
| RBAC | Role-Based Access Control |
| CRUD | Create, Read, Update, Delete |
| API | Application Programming Interface |
| JWT | JSON Web Token |
| TLS | Transport Layer Security |

---

## 13. References

1. **FastAPI Documentation**: https://fastapi.tiangolo.com/
2. **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
3. **PostgreSQL Documentation**: https://www.postgresql.org/docs/
4. **Docker Documentation**: https://docs.docker.com/
5. **Kubernetes Documentation**: https://kubernetes.io/docs/

---

## Appendix A: User Personas

### Persona 1: Nguyễn Văn A - Aladdin Manager

**Demographics**:
- Age: 35
- Role: Quản lý mua hàng
- Experience: 10 năm trong ngành F&B
- Tech-savvy: Trung bình

**Goals**:
- Tạo phiếu YCMS nhanh chóng
- Theo dõi được trạng thái các phiếu
- Có báo cáo để ra quyết định

**Pain Points**:
- Mất nhiều thời gian tạo phiếu thủ công
- Khó theo dõi nhiều nhà cung cấp
- Không có dữ liệu để so sánh giá

**How PMS Helps**:
- Tạo phiếu YCMS trong 20 phút
- Dashboard tổng quan real-time
- Báo cáo so sánh giá tự động

### Persona 2: Trần Thị B - Supplier Staff

**Demographics**:
- Age: 28
- Role: Nhân viên bán hàng (Nhà cung cấp)
- Experience: 3 năm
- Tech-savvy: Cao

**Goals**:
- Nhận được yêu cầu mua hàng ngay lập tức
- Phản hồi nhanh cho khách hàng
- Quản lý được các đơn hàng của mình

**Pain Points**:
- Email dễ bị sót
- Không biết được tổng quan đơn hàng
- Khó tạo phiếu giao hàng theo từng nhà hàng

**How PMS Helps**:
- Notification real-time khi có YCMS mới
- Dashboard hiển thị tất cả YCMS pending
- Tạo phiếu giao hàng tự động từ YCMS

---

**Version**: 1.0  
**Last Updated**: 2025-10-06  
**Author**: Product Owner & System Architect  
**Status**: Draft → For Review → **Approved**
