# Kiến Trúc Hệ Thống (System Architecture)

## Tổng Quan
Tài liệu này mô tả kiến trúc tổng thể của hệ thống quản lý yêu cầu mua sắm (Procurement Management System) cho Aladdin.

---

## 1. Tổng Quan Kiến Trúc

### 1.1. Architecture Style
- **Monolithic** với khả năng scale horizontal
- **Layered Architecture**: Presentation → API → Business Logic → Data Access
- **RESTful API** cho client communication
- **Event-driven** cho notifications và background tasks

### 1.2. Technology Stack

#### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Message Queue**: Celery + Redis
- **Migration**: Alembic

#### Frontend (Separate Project)
- **Framework**: React 18+ / Vue 3+
- **State Management**: Redux / Pinia
- **UI Library**: Ant Design / Material-UI
- **Build Tool**: Vite

#### Infrastructure
- **Container**: Docker
- **Orchestration**: Docker Compose (dev), Kubernetes (prod)
- **Web Server**: Nginx
- **WSGI**: Uvicorn
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

---

## 2. High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Web Browser  │  │ Mobile App   │  │ Admin Portal │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Load Balancer │
                    │     (Nginx)     │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐      ┌─────▼─────┐     ┌─────▼─────┐
    │  API      │      │  API      │     │  API      │
    │  Server 1 │      │  Server 2 │     │  Server N │
    │ (FastAPI) │      │ (FastAPI) │     │ (FastAPI) │
    └─────┬─────┘      └─────┬─────┘     └─────┬─────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
          ┌──────────────────┼──────────────────────────────┐
          │                  │                              │
    ┌─────▼─────┐      ┌─────▼─────┐              ┌────────▼────────┐
    │ PostgreSQL│      │   Redis   │              │   Celery Worker │
    │ (Primary) │      │  (Cache)  │              │  (Background)   │
    └─────┬─────┘      └───────────┘              └────────┬────────┘
          │                                                 │
    ┌─────▼─────┐                                  ┌────────▼────────┐
    │PostgreSQL │                                  │   Redis Queue   │
    │ (Replica) │                                  │                 │
    └───────────┘                                  └─────────────────┘
          │
    ┌─────▼─────┐
    │  S3/Blob  │
    │  Storage  │
    └───────────┘
```

---

## 3. Application Architecture

### 3.1. Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ REST API   │  │  WebSocket   │  │  GraphQL     │        │
│  │ (FastAPI)  │  │  (Optional)  │  │  (Optional)  │        │
│  └────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    API Layer (app/api/)                     │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Routers    │  │ Dependencies │  │ Middlewares  │        │
│  │ (/v1/*)    │  │ (Auth, DB)   │  │ (CORS, etc)  │        │
│  └────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Service Layer (app/services/)              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Business Logic   │  │  Orchestration   │                │
│  │ - YCMS Service   │  │  - Workflows     │                │
│  │ - DN Service     │  │  - Validations   │                │
│  │ - User Service   │  │  - Calculations  │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│               Repository Layer (app/repositories/)          │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Data Access      │  │  Query Builders  │                │
│  │ - Base Repo      │  │  - Filters       │                │
│  │ - YCMS Repo      │  │  - Joins         │                │
│  │ - User Repo      │  │  - Aggregations  │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Data Layer (app/models/)                   │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ SQLAlchemy       │  │  Database        │                │
│  │ Models           │  │  Schema          │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                    ┌─────▼─────┐
                    │PostgreSQL │
                    └───────────┘
```

### 3.2. Component Details

#### 3.2.1. API Layer (`app/api/`)
```
api/
├── __init__.py
├── deps.py              # Dependency injection (DB session, current user)
├── errors/
│   ├── __init__.py
│   └── http_error.py    # Custom exceptions
└── v1/
    ├── __init__.py
    ├── router.py        # Main router aggregator
    ├── auth.py          # Authentication endpoints
    ├── procurement_requests.py
    ├── delivery_notes.py
    ├── products.py
    ├── suppliers.py
    ├── restaurants.py
    ├── notifications.py
    └── reports.py
```

**Responsibilities**:
- Request validation (Pydantic schemas)
- Response serialization
- Authentication & Authorization
- Error handling
- Rate limiting

#### 3.2.2. Service Layer (`app/services/`)
```
services/
├── __init__.py
├── procurement_request_service.py
├── delivery_note_service.py
├── user_service.py
├── supplier_service.py
├── product_service.py
├── notification_service.py
├── email_service.py
└── report_service.py
```

**Responsibilities**:
- Business logic implementation
- Transaction management
- Cross-entity operations
- Validation rules
- Event triggering

**Example**:
```python
class ProcurementRequestService:
    def __init__(self, repo: ProcurementRequestRepository):
        self.repo = repo
    
    def create_request(self, data: CreateRequestSchema, user: User):
        # Business logic
        # - Validate items
        # - Calculate totals
        # - Create request
        pass
    
    def submit_request(self, request_id: int, user: User):
        # Business logic
        # - Check permissions
        # - Change status
        # - Trigger notifications
        # - Send emails
        pass
```

#### 3.2.3. Repository Layer (`app/repositories/`)
```
repositories/
├── __init__.py
├── base.py              # Base repository with CRUD
├── procurement_request.py
├── delivery_note.py
├── user.py
├── supplier.py
├── product.py
└── notification.py
```

**Responsibilities**:
- Database queries
- Filtering, sorting, pagination
- Join operations
- Transaction handling (with service layer)

**Example**:
```python
class ProcurementRequestRepository(BaseRepository[ProcurementRequest]):
    def find_by_supplier(
        self, 
        supplier_id: int, 
        status: Optional[str] = None
    ) -> List[ProcurementRequest]:
        query = self.db.query(ProcurementRequest)
        query = query.join(ProcurementRequestItem)
        query = query.filter(ProcurementRequestItem.supplier_id == supplier_id)
        if status:
            query = query.filter(ProcurementRequest.status == status)
        return query.all()
```

#### 3.2.4. Model Layer (`app/models/`)
```
models/
├── __init__.py
├── base.py              # Base model with common fields
├── mixins.py            # Timestamp, soft delete mixins
├── user.py
├── supplier.py
├── restaurant.py
├── product.py
├── procurement_request.py
├── delivery_note.py
└── notification.py
```

**Responsibilities**:
- Database table definitions
- Relationships
- Constraints
- Indexes

---

## 4. Cross-Cutting Concerns

### 4.1. Authentication & Authorization

```
┌────────────────────────────────────────────────────────────┐
│                    Request Flow                            │
└────────────────────────────────────────────────────────────┘

Client Request
    │
    ├─ Header: Authorization: Bearer {token}
    │
    ▼
┌────────────────┐
│ Auth Middleware│
│ (JWT Verify)   │
└────────┬───────┘
         │
         ├─ Valid Token ─────────────────────┐
         │                                   │
         ▼                                   ▼
    ┌─────────┐                         ┌──────────┐
    │ Extract │                         │ Return   │
    │ User    │                         │ 401      │
    └────┬────┘                         └──────────┘
         │
         ▼
    ┌─────────────┐
    │ Load User   │
    │ from DB     │
    └────┬────────┘
         │
         ▼
    ┌─────────────────┐
    │ Check Permission│
    │ (Decorator)     │
    └────┬────────────┘
         │
         ├─ Has Permission ──────────────┐
         │                               │
         ▼                               ▼
    ┌─────────┐                     ┌──────────┐
    │ Execute │                     │ Return   │
    │ Handler │                     │ 403      │
    └─────────┘                     └──────────┘
```

**Implementation**:
```python
# app/api/deps.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Verify JWT
    # Load user from DB
    # Return user or raise 401
    pass

async def get_current_aladdin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.user_type != UserType.ALADDIN:
        raise HTTPException(status_code=403, detail="Aladdin user required")
    return current_user

# app/api/v1/procurement_requests.py
@router.post("/")
async def create_procurement_request(
    data: CreateRequestSchema,
    user: User = Depends(get_current_aladdin_user),
    db: Session = Depends(get_db)
):
    # Only Aladdin users can reach here
    pass
```

### 4.2. Validation

**Multi-level Validation**:

1. **Schema Level** (Pydantic):
   ```python
   class CreateRequestItemSchema(BaseModel):
       product_id: int = Field(gt=0)
       supplier_id: int = Field(gt=0)
       quantity_requested: Decimal = Field(gt=0, max_digits=15, decimal_places=3)
       expected_delivery_date: date
       
       @validator('expected_delivery_date')
       def validate_date(cls, v, values):
           if 'request_date' in values and v < values['request_date']:
               raise ValueError("expected_delivery_date must >= request_date")
           return v
   ```

2. **Business Logic Level** (Service):
   ```python
   def validate_procurement_request(self, data: CreateRequestSchema):
       # Check product-supplier mapping exists
       # Check restaurant exists
       # Check quantity constraints
       pass
   ```

3. **Database Level** (Constraints):
   ```sql
   ALTER TABLE procurement_request_items
   ADD CONSTRAINT check_quantity_positive
   CHECK (quantity_requested > 0);
   ```

### 4.3. Error Handling

**Global Exception Handler**:
```python
# app/api/errors/http_error.py
class BusinessException(Exception):
    def __init__(self, error_code: str, message: str, details: dict = None):
        self.error_code = error_code
        self.message = message
        self.details = details

# app/main.py
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=400,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 4.4. Logging

**Structured Logging**:
```python
# app/core/logging.py
import structlog

logger = structlog.get_logger()

# Usage
logger.info(
    "procurement_request_created",
    request_id=1,
    code="YCMS-20251006-0001",
    user_id=user.id,
    item_count=5
)
```

**Log Levels**:
- **DEBUG**: Detailed info for debugging
- **INFO**: General events (request created, email sent)
- **WARNING**: Something unexpected but handled
- **ERROR**: Error occurred but recoverable
- **CRITICAL**: System failure

### 4.5. Caching Strategy

**Cache Layers**:

1. **Application Cache** (Redis):
   ```python
   # Cache user permissions
   cache_key = f"user:{user_id}:permissions"
   permissions = redis.get(cache_key)
   if not permissions:
       permissions = load_permissions_from_db(user_id)
       redis.setex(cache_key, 3600, permissions)
   ```

2. **Query Result Cache**:
   ```python
   # Cache supplier's product list
   @cache(key="supplier:{supplier_id}:products", ttl=300)
   def get_supplier_products(supplier_id: int):
       return db.query(SupplierProduct).filter_by(supplier_id=supplier_id).all()
   ```

3. **HTTP Cache** (Nginx):
   - Static assets (CSS, JS, images)
   - Public API responses (products list)

**Cache Invalidation**:
```python
# When supplier product updated
redis.delete(f"supplier:{supplier_id}:products")
```

---

## 5. Database Design

### 5.1. Database Schema

**Core Tables**:
- `users`: Người dùng
- `suppliers`: Nhà cung cấp
- `restaurants`: Nhà hàng
- `products`: Sản phẩm chuẩn
- `product_categories`: Nhóm sản phẩm
- `supplier_products`: Mapping sản phẩm nhà cung cấp
- `procurement_requests`: Phiếu YCMS
- `procurement_request_items`: Chi tiết YCMS
- `delivery_notes`: Phiếu giao hàng
- `delivery_note_items`: Chi tiết phiếu giao hàng
- `notifications`: Thông báo
- `audit_logs`: Nhật ký hệ thống

**Indexes**:
```sql
-- Performance critical indexes
CREATE INDEX idx_pr_supplier_created ON procurement_request_items(supplier_id, created_at);
CREATE INDEX idx_pr_status ON procurement_requests(status);
CREATE INDEX idx_dn_delivery_date ON delivery_notes(delivery_date);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_supplier ON users(supplier_id) WHERE supplier_id IS NOT NULL;
```

**Partitioning** (Large tables):
```sql
-- Partition procurement_requests by request_date (monthly)
CREATE TABLE procurement_requests_2025_10 PARTITION OF procurement_requests
FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
```

### 5.2. Data Integrity

**Foreign Keys**:
```sql
ALTER TABLE procurement_request_items
ADD CONSTRAINT fk_pr_item_request
FOREIGN KEY (procurement_request_id) 
REFERENCES procurement_requests(id) 
ON DELETE CASCADE;
```

**Triggers** (Audit Trail):
```sql
CREATE TRIGGER trg_pr_audit
AFTER UPDATE ON procurement_requests
FOR EACH ROW
EXECUTE FUNCTION log_procurement_request_change();
```

**Views** (Complex Queries):
```sql
CREATE VIEW v_procurement_summary AS
SELECT 
    pr.id,
    pr.code,
    pr.status,
    COUNT(pri.id) as item_count,
    SUM(pri.total_amount) as total_amount,
    COUNT(DISTINCT pri.supplier_id) as supplier_count
FROM procurement_requests pr
LEFT JOIN procurement_request_items pri ON pr.id = pri.procurement_request_id
GROUP BY pr.id;
```

---

## 6. Background Jobs (Celery)

### 6.1. Task Types

**Periodic Tasks** (Celery Beat):
```python
# tasks/scheduled.py
@celery_app.task
def check_overdue_deliveries():
    # Run daily at 8 AM
    # Find overdue delivery notes
    # Send notifications
    pass

@celery_app.task
def generate_daily_report():
    # Run daily at 11 PM
    # Generate summary report
    # Send to managers
    pass
```

**Async Tasks**:
```python
# tasks/email.py
@celery_app.task(bind=True, max_retries=3)
def send_email_async(self, recipients: List[str], subject: str, body: str):
    try:
        send_email(recipients, subject, body)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)  # Retry after 1 min
```

**Long-Running Tasks**:
```python
# tasks/reports.py
@celery_app.task
def generate_monthly_report(month: str, year: int):
    # Heavy computation
    # Generate Excel file
    # Upload to S3
    # Send notification with download link
    pass
```

### 6.2. Task Monitoring

- **Flower**: Web UI for monitoring Celery tasks
- **Metrics**: Task success/failure rates, execution time
- **Alerts**: Failed tasks, long-running tasks

---

## 7. Security Architecture

### 7.1. Security Layers

```
┌────────────────────────────────────────────────────────────┐
│                    Security Layers                         │
└────────────────────────────────────────────────────────────┘

1. Network Layer
   ├─ Firewall rules
   ├─ VPN for admin access
   └─ Rate limiting (Nginx)

2. Application Layer
   ├─ HTTPS only (TLS 1.3)
   ├─ CORS policy
   ├─ JWT authentication
   ├─ Input validation (Pydantic)
   ├─ SQL injection prevention (ORM)
   └─ XSS protection

3. Data Layer
   ├─ Encryption at rest
   ├─ Password hashing (bcrypt)
   ├─ Database access control
   └─ Audit logging

4. Infrastructure Layer
   ├─ Container isolation
   ├─ Secret management (Vault/AWS Secrets)
   └─ Regular security updates
```

### 7.2. Authentication Flow

```
┌────────────────────────────────────────────────────────────┐
│                    JWT Authentication                      │
└────────────────────────────────────────────────────────────┘

1. Login
   User ──(username/password)──> API
   API ──(verify credentials)──> DB
   API ──(generate JWT)──> User
   
2. Subsequent Requests
   User ──(JWT in header)──> API
   API ──(verify JWT)──> Continue
   
3. Token Refresh
   User ──(refresh token)──> API
   API ──(verify refresh token)──> New JWT
```

### 7.3. Authorization Model

**Role-Based Access Control (RBAC)**:

| Role | Permissions |
|------|-------------|
| Aladdin Admin | Full access |
| Aladdin Manager | Create/view YCMS, view all reports |
| Aladdin Staff | View YCMS, confirm deliveries |
| Supplier Admin | Full access to own data |
| Supplier Staff | View/update own YCMS items, create delivery notes |

**Permission Decorators**:
```python
@require_permission("ycms.create")
async def create_procurement_request(...):
    pass

@require_permission("ycms.view_all")  # Aladdin only
async def get_all_procurement_requests(...):
    pass

@require_permission("ycms.view_own")  # Supplier only
async def get_supplier_procurement_requests(...):
    pass
```

---

## 8. Scalability & Performance

### 8.1. Horizontal Scaling

**Stateless API Servers**:
- No session state in memory
- JWT tokens (no server-side sessions)
- Can add/remove instances dynamically

**Load Balancing**:
```nginx
upstream api_backend {
    least_conn;  # Algorithm
    server api1:8000 weight=3;
    server api2:8000 weight=3;
    server api3:8000 weight=2;
}
```

### 8.2. Database Optimization

**Read Replicas**:
- Write to primary
- Read from replicas
- Use connection pools

```python
# app/db/session.py
primary_engine = create_engine(PRIMARY_DB_URL)
replica_engine = create_engine(REPLICA_DB_URL)

def get_db(read_only: bool = False):
    engine = replica_engine if read_only else primary_engine
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Query Optimization**:
- Eager loading (avoid N+1 queries)
- Pagination for large datasets
- Database indexes

```python
# Bad: N+1 queries
requests = db.query(ProcurementRequest).all()
for req in requests:
    print(req.items)  # Each iteration hits DB

# Good: Eager loading
requests = db.query(ProcurementRequest)\
    .options(joinedload(ProcurementRequest.items))\
    .all()
```

### 8.3. Caching Strategy

**Cache Hit Ratio Target**: > 80%

**What to Cache**:
- User permissions (1 hour TTL)
- Product list (5 min TTL)
- Supplier list (5 min TTL)
- Dashboard data (1 min TTL)
- Static data (category, etc) (1 day TTL)

**Cache Aside Pattern**:
```python
def get_product(product_id: int):
    cache_key = f"product:{product_id}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    product = db.query(Product).get(product_id)
    redis.setex(cache_key, 300, json.dumps(product))
    return product
```

---

## 9. Monitoring & Observability

### 9.1. Metrics (Prometheus)

**Application Metrics**:
- Request rate (req/sec)
- Response time (p50, p95, p99)
- Error rate (%)
- Active users
- Database connection pool usage

**Business Metrics**:
- YCMS created per day
- Delivery notes created per day
- Average delivery time
- Overdue rate

**Custom Metrics**:
```python
from prometheus_client import Counter, Histogram

request_counter = Counter(
    'ycms_requests_created_total',
    'Total YCMS requests created'
)

delivery_time = Histogram(
    'delivery_time_days',
    'Delivery time in days',
    buckets=[1, 2, 3, 5, 7, 10, 15]
)

# Usage
@router.post("/procurement-requests")
async def create_request(...):
    request_counter.inc()
    # ... logic
```

### 9.2. Logging (ELK Stack)

**Log Aggregation**:
```
Application Logs ──> Logstash ──> Elasticsearch ──> Kibana
```

**Log Format** (JSON):
```json
{
  "timestamp": "2025-10-06T10:00:00Z",
  "level": "INFO",
  "event": "procurement_request_created",
  "request_id": 1,
  "code": "YCMS-20251006-0001",
  "user_id": 1,
  "user_type": "ALADDIN",
  "duration_ms": 150
}
```

### 9.3. Distributed Tracing (Jaeger)

**Trace Requests Across Services**:
```
User Request
  └─ API Gateway (span)
      └─ Auth Service (span)
      └─ YCMS Service (span)
          └─ Database Query (span)
          └─ Email Service (span)
```

### 9.4. Health Checks

**Endpoints**:
```python
@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/health/detailed")
async def detailed_health_check():
    return {
        "status": "ok",
        "database": check_db_connection(),
        "redis": check_redis_connection(),
        "celery": check_celery_workers()
    }
```

---

## 10. Deployment Architecture

### 10.1. Development Environment

```
docker-compose.yml
├─ api (FastAPI)
├─ db (PostgreSQL)
├─ redis (Redis)
├─ celery-worker
└─ celery-beat
```

### 10.2. Production Environment (Kubernetes)

```
┌────────────────────────────────────────────────────────────┐
│                         Kubernetes Cluster                 │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                      Ingress                        │  │
│  │         (Load Balancer + TLS Termination)           │  │
│  └──────────────────────┬──────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼──────────────────────────────┐  │
│  │              API Deployment (3 replicas)            │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │ API Pod 1│  │ API Pod 2│  │ API Pod 3│          │  │
│  │  └──────────┘  └──────────┘  └──────────┘          │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │          Celery Worker Deployment (2 replicas)      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                 Redis StatefulSet                   │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘

External:
- PostgreSQL (AWS RDS / Azure Database)
- S3 / Blob Storage
- Email Service (SendGrid / SES)
```

### 10.3. CI/CD Pipeline

```
┌────────────────────────────────────────────────────────────┐
│                       CI/CD Pipeline                       │
└────────────────────────────────────────────────────────────┘

1. Code Push (GitHub)
   ↓
2. CI Triggered (GitHub Actions)
   ├─ Run Tests
   ├─ Run Linters (flake8, black, mypy)
   ├─ Security Scan (bandit)
   └─ Build Docker Image
   ↓
3. Push Image to Registry (Docker Hub / ECR)
   ↓
4. CD Triggered
   ├─ Dev Environment (auto-deploy)
   ├─ Staging Environment (auto-deploy)
   └─ Production Environment (manual approval)
   ↓
5. Deploy to Kubernetes
   ├─ Update Deployment
   ├─ Run Database Migrations
   └─ Health Check
   ↓
6. Notify Team (Slack)
```

**GitHub Actions Example**:
```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
      - name: Lint
        run: |
          flake8 app/
          black --check app/
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/api api=myapp:${{ github.sha }}
          kubectl rollout status deployment/api
```

---

## 11. Disaster Recovery

### 11.1. Backup Strategy

**Database**:
- Full backup: Daily at 2 AM
- Incremental backup: Every 6 hours
- Retention: 30 days
- Stored in: S3 with cross-region replication

**Files**:
- PDF files, uploads → S3 versioning enabled
- Retention: 90 days

**Configuration**:
- Environment variables → Secret manager
- Kubernetes manifests → Git repository

### 11.2. Recovery Plan

**RTO (Recovery Time Objective)**: 4 hours  
**RPO (Recovery Point Objective)**: 6 hours

**Recovery Steps**:
1. Restore database from backup
2. Restore Redis data (if cached)
3. Redeploy application
4. Run health checks
5. Notify team

---

## 12. Performance Targets

| Metric | Target |
|--------|--------|
| API Response Time (p95) | < 500ms |
| API Response Time (p99) | < 1s |
| Uptime | > 99.9% |
| Concurrent Users | 1000+ |
| Database Queries | < 100ms (p95) |
| Email Delivery | < 5min |
| Background Job Processing | < 10min |

---

**Version**: 1.0  
**Last Updated**: 2025-10-06  
**Author**: System Architect
