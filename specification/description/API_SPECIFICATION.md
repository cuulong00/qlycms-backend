# Đặc Tả API (API Specification)

## Tổng Quan
Tài liệu này mô tả chi tiết các API endpoints cho hệ thống quản lý yêu cầu mua sắm của Aladdin.

---

## Base Information

- **Base URL**: `/api/v1`
- **Authentication**: JWT Bearer Token
- **Content-Type**: `application/json`
- **Charset**: `UTF-8`

---

## 1. Authentication APIs

### 1.1. Login

**Endpoint**: `POST /auth/login`

**Mô tả**: Đăng nhập và nhận JWT token

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "john.doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "user_type": "ALADDIN",
    "supplier_id": null
  }
}
```

**Errors**:
- 401: Invalid credentials
- 400: Missing required fields

---

### 1.2. Logout

**Endpoint**: `POST /auth/logout`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

---

### 1.3. Refresh Token

**Endpoint**: `POST /auth/refresh`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "access_token": "new_token",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

### 1.4. Get Current User

**Endpoint**: `GET /auth/me`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "john.doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "user_type": "ALADDIN",
  "supplier_id": null,
  "phone_number": "0123456789",
  "last_login": "2025-10-06T10:30:00Z"
}
```

---

## 2. Procurement Request APIs (YCMS)

### 2.1. List Procurement Requests

**Endpoint**: `GET /procurement-requests`

**Headers**: `Authorization: Bearer {token}`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Items per page (default: 20, max: 100) |
| status | string | No | Filter by status (DRAFT, SUBMITTED, etc.) |
| supplier_id | integer | No | Filter by supplier (Aladdin only) |
| restaurant_id | integer | No | Filter by restaurant |
| date_from | date | No | Filter from date (request_date) |
| date_to | date | No | Filter to date (request_date) |
| search | string | No | Search by code or title |
| sort_by | string | No | Sort field (default: created_at) |
| sort_order | string | No | asc/desc (default: desc) |

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 1,
      "code": "YCMS-20251006-0001",
      "title": "Yêu cầu mua sắm tuần 41",
      "request_date": "2025-10-06",
      "status": "SUBMITTED",
      "total_amount": 50000000,
      "item_count": 25,
      "supplier_count": 5,
      "created_by": {
        "id": 1,
        "full_name": "Nguyễn Văn A"
      },
      "created_at": "2025-10-06T08:00:00Z",
      "submitted_at": "2025-10-06T09:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

**Notes**:
- User Supplier chỉ thấy YCMS có items của mình (auto-filter)
- User Aladdin thấy tất cả

---

### 2.2. Get Procurement Request Detail

**Endpoint**: `GET /procurement-requests/{id}`

**Headers**: `Authorization: Bearer {token}`

**Path Parameters**:
- `id`: Procurement Request ID

**Response** (200 OK):
```json
{
  "id": 1,
  "code": "YCMS-20251006-0001",
  "title": "Yêu cầu mua sắm tuần 41",
  "request_date": "2025-10-06",
  "status": "SUBMITTED",
  "notes": "Gấp, cần giao trước 15/10",
  "created_by": {
    "id": 1,
    "full_name": "Nguyễn Văn A",
    "email": "nguyen.a@aladdin.com"
  },
  "submitted_at": "2025-10-06T09:30:00Z",
  "created_at": "2025-10-06T08:00:00Z",
  "updated_at": "2025-10-06T09:30:00Z",
  "items": [
    {
      "id": 101,
      "product": {
        "id": 50,
        "code": "GAO-ST25",
        "name": "Gạo ST25"
      },
      "supplier": {
        "id": 10,
        "code": "NCC-001",
        "name": "Công ty Gạo Việt"
      },
      "restaurant": {
        "id": 5,
        "code": "NH-HN-001",
        "name": "Nhà hàng Hà Nội 1"
      },
      "quantity_requested": 500,
      "unit": "kg",
      "unit_price": 25000,
      "total_amount": 12500000,
      "delivery_address": "123 Đường ABC, Hà Nội",
      "expected_delivery_date": "2025-10-15",
      "status": "PENDING",
      "notes": ""
    }
  ],
  "delivery_notes": [
    {
      "id": 201,
      "code": "DN-20251007-0001",
      "supplier": {
        "id": 10,
        "name": "Công ty Gạo Việt"
      },
      "restaurant": {
        "id": 5,
        "name": "Nhà hàng Hà Nội 1"
      },
      "delivery_date": "2025-10-15",
      "status": "CONFIRMED",
      "total_amount": 12500000
    }
  ],
  "statistics": {
    "total_amount": 50000000,
    "item_count": 25,
    "supplier_count": 5,
    "pending_items": 10,
    "confirmed_items": 15,
    "cancelled_items": 0
  }
}
```

**Errors**:
- 404: Procurement request not found
- 403: User không có quyền xem (supplier khác)

---

### 2.3. Create Procurement Request

**Endpoint**: `POST /procurement-requests`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Request Body**:
```json
{
  "title": "Yêu cầu mua sắm tuần 41",
  "request_date": "2025-10-06",
  "notes": "Gấp, cần giao trước 15/10",
  "items": [
    {
      "product_id": 50,
      "supplier_id": 10,
      "restaurant_id": 5,
      "quantity_requested": 500,
      "unit": "kg",
      "unit_price": 25000,
      "delivery_address": "123 Đường ABC, Hà Nội",
      "expected_delivery_date": "2025-10-15",
      "notes": ""
    }
  ]
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "code": "YCMS-20251006-0001",
  "status": "DRAFT",
  "message": "Tạo phiếu YCMS thành công"
}
```

**Validation**:
- `items` không được rỗng
- `quantity_requested` > 0
- `expected_delivery_date` >= `request_date`
- `product_id`, `supplier_id`, `restaurant_id` phải tồn tại
- Product-Supplier mapping phải tồn tại

**Errors**:
- 400: Validation error
- 403: Permission denied (not Aladdin user)

---

### 2.4. Update Procurement Request

**Endpoint**: `PUT /procurement-requests/{id}`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only, status = DRAFT

**Request Body**: Tương tự Create

**Response** (200 OK):
```json
{
  "id": 1,
  "code": "YCMS-20251006-0001",
  "message": "Cập nhật phiếu YCMS thành công"
}
```

**Errors**:
- 400: Cannot update non-draft request
- 403: Permission denied
- 404: Not found

---

### 2.5. Submit Procurement Request

**Endpoint**: `POST /procurement-requests/{id}/submit`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only, status = DRAFT

**Response** (200 OK):
```json
{
  "id": 1,
  "code": "YCMS-20251006-0001",
  "status": "SUBMITTED",
  "submitted_at": "2025-10-06T09:30:00Z",
  "message": "Submit phiếu YCMS thành công. Email đã được gửi đến nhà cung cấp.",
  "notifications_sent": [
    {
      "supplier_id": 10,
      "supplier_name": "Công ty Gạo Việt",
      "email_count": 2
    }
  ]
}
```

**Side Effects**:
- Status: DRAFT → SUBMITTED
- Gửi email đến tất cả suppliers
- Tạo in-app notifications

**Errors**:
- 400: No items or already submitted
- 403: Permission denied

---

### 2.6. Cancel Procurement Request

**Endpoint**: `POST /procurement-requests/{id}/cancel`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Request Body**:
```json
{
  "reason": "Thay đổi kế hoạch mua sắm"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "status": "CANCELLED",
  "message": "Hủy phiếu YCMS thành công"
}
```

**Side Effects**:
- Status → CANCELLED
- Hủy các delivery notes chưa giao
- Gửi notification cho suppliers

---

### 2.7. Update Procurement Request Item (Supplier)

**Endpoint**: `PUT /procurement-requests/{pr_id}/items/{item_id}`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Supplier only, item thuộc supplier, status = SUBMITTED/CONFIRMED

**Request Body**:
```json
{
  "quantity_requested": 450,
  "unit_price": 26000,
  "expected_delivery_date": "2025-10-16",
  "status": "CONFIRMED",
  "notes": "Đã xác nhận, sẽ giao đúng hạn"
}
```

**Response** (200 OK):
```json
{
  "id": 101,
  "status": "CONFIRMED",
  "message": "Cập nhật item thành công"
}
```

**Side Effects**:
- Gửi notification cho Aladdin về thay đổi

**Errors**:
- 403: Not your item
- 400: Invalid status transition

---

## 3. Delivery Note APIs

### 3.1. List Delivery Notes

**Endpoint**: `GET /delivery-notes`

**Headers**: `Authorization: Bearer {token}`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number |
| limit | integer | No | Items per page |
| status | string | No | Filter by status |
| supplier_id | integer | No | Filter by supplier (Aladdin only) |
| restaurant_id | integer | No | Filter by restaurant |
| procurement_request_id | integer | No | Filter by YCMS |
| delivery_date_from | date | No | From delivery date |
| delivery_date_to | date | No | To delivery date |
| search | string | No | Search by code |

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 201,
      "code": "DN-20251007-0001",
      "procurement_request": {
        "id": 1,
        "code": "YCMS-20251006-0001"
      },
      "supplier": {
        "id": 10,
        "name": "Công ty Gạo Việt"
      },
      "restaurant": {
        "id": 5,
        "name": "Nhà hàng Hà Nội 1"
      },
      "delivery_date": "2025-10-15",
      "status": "CONFIRMED",
      "total_amount": 12500000,
      "item_count": 5,
      "created_at": "2025-10-07T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 50,
    "total_pages": 3
  }
}
```

---

### 3.2. Get Delivery Note Detail

**Endpoint**: `GET /delivery-notes/{id}`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "id": 201,
  "code": "DN-20251007-0001",
  "procurement_request": {
    "id": 1,
    "code": "YCMS-20251006-0001",
    "title": "Yêu cầu mua sắm tuần 41"
  },
  "supplier": {
    "id": 10,
    "code": "NCC-001",
    "name": "Công ty Gạo Việt",
    "phone": "0901234567"
  },
  "restaurant": {
    "id": 5,
    "code": "NH-HN-001",
    "name": "Nhà hàng Hà Nội 1",
    "address": "123 Đường ABC, Hà Nội"
  },
  "delivery_date": "2025-10-15",
  "delivery_address": "123 Đường ABC, Hà Nội",
  "status": "CONFIRMED",
  "total_amount": 12500000,
  "created_by": {
    "id": 20,
    "full_name": "Nguyễn Văn B"
  },
  "confirmed_by": null,
  "confirmed_at": null,
  "delivered_at": null,
  "notes": "",
  "created_at": "2025-10-07T10:00:00Z",
  "updated_at": "2025-10-07T10:30:00Z",
  "items": [
    {
      "id": 301,
      "procurement_request_item_id": 101,
      "product": {
        "id": 50,
        "code": "GAO-ST25",
        "name": "Gạo ST25"
      },
      "product_code": "GAO-ST25",
      "product_name": "Gạo ST25",
      "quantity_ordered": 500,
      "quantity_delivered": null,
      "unit": "kg",
      "unit_price": 25000,
      "total_amount": 12500000,
      "notes": ""
    }
  ]
}
```

---

### 3.3. Create Delivery Note

**Endpoint**: `POST /delivery-notes`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Supplier only

**Request Body**:
```json
{
  "procurement_request_id": 1,
  "restaurant_id": 5,
  "delivery_date": "2025-10-15",
  "delivery_address": "123 Đường ABC, Hà Nội",
  "notes": "",
  "items": [
    {
      "procurement_request_item_id": 101,
      "quantity_ordered": 500
    }
  ]
}
```

**Response** (201 Created):
```json
{
  "id": 201,
  "code": "DN-20251007-0001",
  "status": "DRAFT",
  "message": "Tạo phiếu giao hàng thành công"
}
```

**Validation**:
- `procurement_request_item_id` phải thuộc supplier của user
- Tổng `quantity_ordered` <= `quantity_requested` trong YCMS
- `delivery_date` >= current date

**Errors**:
- 400: Validation error (exceed quantity, wrong supplier...)
- 403: Permission denied

---

### 3.4. Submit Delivery Note

**Endpoint**: `POST /delivery-notes/{id}/submit`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Supplier only, owner, status = DRAFT

**Response** (200 OK):
```json
{
  "id": 201,
  "code": "DN-20251007-0001",
  "status": "CONFIRMED",
  "message": "Submit phiếu giao hàng thành công. Email đã gửi đến Aladdin."
}
```

**Side Effects**:
- Status: DRAFT → CONFIRMED
- Gửi email cho Aladdin
- Tạo notification

---

### 3.5. Update Delivery Status

**Endpoint**: `POST /delivery-notes/{id}/update-status`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Supplier or Aladdin

**Request Body**:
```json
{
  "status": "IN_TRANSIT",
  "notes": "Xe đã xuất kho lúc 8h sáng"
}
```

**Response** (200 OK):
```json
{
  "id": 201,
  "status": "IN_TRANSIT",
  "message": "Cập nhật trạng thái thành công"
}
```

**Valid Transitions**:
- CONFIRMED → IN_TRANSIT (Supplier)
- IN_TRANSIT → DELIVERED (Supplier or Aladdin)
- Any → CANCELLED (with reason)

---

### 3.6. Confirm Received (Aladdin)

**Endpoint**: `POST /delivery-notes/{id}/receive`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Request Body**:
```json
{
  "items": [
    {
      "id": 301,
      "quantity_delivered": 495,
      "notes": "Thiếu 5kg, bị vỡ bao"
    }
  ],
  "notes": "Đã nhận hàng lúc 10h"
}
```

**Response** (200 OK):
```json
{
  "id": 201,
  "status": "DELIVERED",
  "delivered_at": "2025-10-15T10:00:00Z",
  "message": "Xác nhận nhận hàng thành công",
  "discrepancy": {
    "has_discrepancy": true,
    "items": [
      {
        "product_name": "Gạo ST25",
        "ordered": 500,
        "delivered": 495,
        "difference": -5
      }
    ]
  }
}
```

**Side Effects**:
- Status → DELIVERED
- Update `quantity_delivered` cho từng item
- Tính toán `total_amount` thực tế
- Gửi notification cho supplier nếu có chênh lệch

---

### 3.7. Generate PDF

**Endpoint**: `GET /delivery-notes/{id}/pdf`

**Headers**: `Authorization: Bearer {token}`

**Response**: PDF file (Content-Type: application/pdf)

**Errors**:
- 404: Not found
- 403: Permission denied

---

## 4. Product APIs

### 4.1. List Products

**Endpoint**: `GET /products`

**Headers**: `Authorization: Bearer {token}`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number |
| limit | integer | No | Items per page |
| category_id | integer | No | Filter by category |
| search | string | No | Search by code or name |
| is_active | boolean | No | Filter active/inactive |

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 50,
      "code": "GAO-ST25",
      "name": "Gạo ST25",
      "category": {
        "id": 5,
        "name": "Gạo"
      },
      "base_unit": "kg",
      "is_active": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 500,
    "total_pages": 25
  }
}
```

---

### 4.2. Get Product Detail

**Endpoint**: `GET /products/{id}`

**Response** (200 OK):
```json
{
  "id": 50,
  "code": "GAO-ST25",
  "name": "Gạo ST25",
  "category": {
    "id": 5,
    "code": "GAO",
    "name": "Gạo"
  },
  "base_unit": "kg",
  "description": "Gạo ST25 loại 1",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00Z",
  "supplier_mappings": [
    {
      "supplier": {
        "id": 10,
        "name": "Công ty Gạo Việt"
      },
      "supplier_product_code": "GAO-ST25-BAO50",
      "supplier_product_name": "Gạo ST25 bao 50kg",
      "supplier_unit": "bao",
      "conversion_factor": 50,
      "unit_price": 1250000
    }
  ]
}
```

---

### 4.3. Create/Update/Delete Product

**Permission**: Aladdin Admin only

*APIs tương tự, bỏ qua chi tiết*

---

## 5. Supplier APIs

### 5.1. List Suppliers

**Endpoint**: `GET /suppliers`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Query Parameters**: page, limit, search, is_active

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 10,
      "code": "NCC-001",
      "name": "Công ty Gạo Việt",
      "contact_person": "Nguyễn Văn C",
      "phone": "0901234567",
      "email": "contact@gaoviet.com",
      "is_active": true
    }
  ],
  "pagination": {...}
}
```

---

### 5.2. Supplier Product Mapping

**Endpoint**: `GET /suppliers/{id}/products`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "supplier": {
    "id": 10,
    "name": "Công ty Gạo Việt"
  },
  "products": [
    {
      "id": 100,
      "supplier_product_code": "GAO-ST25-BAO50",
      "supplier_product_name": "Gạo ST25 bao 50kg",
      "supplier_unit": "bao",
      "conversion_factor": 50,
      "unit_price": 1250000,
      "product": {
        "id": 50,
        "code": "GAO-ST25",
        "name": "Gạo ST25",
        "base_unit": "kg"
      },
      "is_active": true
    }
  ]
}
```

---

### 5.3. Create Supplier Product Mapping

**Endpoint**: `POST /suppliers/{id}/products`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Supplier (own products) or Aladdin Admin

**Request Body**:
```json
{
  "product_id": 50,
  "supplier_product_code": "GAO-ST25-BAO50",
  "supplier_product_name": "Gạo ST25 bao 50kg",
  "supplier_unit": "bao",
  "conversion_factor": 50,
  "unit_price": 1250000
}
```

**Response** (201 Created):
```json
{
  "id": 100,
  "message": "Tạo mapping thành công"
}
```

**Validation**:
- `conversion_factor` > 0
- `supplier_product_code` unique cho supplier

---

## 6. Restaurant APIs

### 6.1. List Restaurants

**Endpoint**: `GET /restaurants`

**Headers**: `Authorization: Bearer {token}`

**Query Parameters**: page, limit, search, province, is_active

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 5,
      "code": "NH-HN-001",
      "name": "Nhà hàng Hà Nội 1",
      "address": "123 Đường ABC, Hà Nội",
      "province": "Hà Nội",
      "phone": "0241234567",
      "is_active": true
    }
  ],
  "pagination": {...}
}
```

---

## 7. Notification APIs

### 7.1. List Notifications

**Endpoint**: `GET /notifications`

**Headers**: `Authorization: Bearer {token}`

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number |
| limit | integer | No | Items per page |
| is_read | boolean | No | Filter read/unread |
| type | string | No | Filter by type |

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": 1000,
      "type": "NEW_REQUEST",
      "title": "Phiếu yêu cầu mua sắm mới",
      "message": "Có phiếu YCMS-20251006-0001 mới được tạo",
      "reference_type": "ProcurementRequest",
      "reference_id": 1,
      "is_read": false,
      "sent_at": "2025-10-06T09:30:00Z"
    }
  ],
  "pagination": {...},
  "unread_count": 5
}
```

---

### 7.2. Mark as Read

**Endpoint**: `POST /notifications/{id}/read`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "id": 1000,
  "is_read": true,
  "read_at": "2025-10-06T10:00:00Z"
}
```

---

### 7.3. Mark All as Read

**Endpoint**: `POST /notifications/read-all`

**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "message": "Đánh dấu tất cả đã đọc",
  "count": 5
}
```

---

## 8. Report APIs

### 8.1. Procurement Summary Report

**Endpoint**: `GET /reports/procurement-summary`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| date_from | date | Yes | From date |
| date_to | date | Yes | To date |
| supplier_id | integer | No | Filter by supplier |
| restaurant_id | integer | No | Filter by restaurant |

**Response** (200 OK):
```json
{
  "period": {
    "from": "2025-10-01",
    "to": "2025-10-31"
  },
  "summary": {
    "total_requests": 50,
    "total_amount": 500000000,
    "completed_requests": 45,
    "pending_requests": 3,
    "cancelled_requests": 2
  },
  "by_supplier": [
    {
      "supplier_id": 10,
      "supplier_name": "Công ty Gạo Việt",
      "request_count": 30,
      "total_amount": 250000000,
      "completion_rate": 0.95
    }
  ],
  "by_restaurant": [
    {
      "restaurant_id": 5,
      "restaurant_name": "Nhà hàng Hà Nội 1",
      "request_count": 25,
      "total_amount": 150000000
    }
  ]
}
```

---

### 8.2. Delivery Performance Report

**Endpoint**: `GET /reports/delivery-performance`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Query Parameters**: date_from, date_to, supplier_id

**Response** (200 OK):
```json
{
  "summary": {
    "total_deliveries": 120,
    "on_time_deliveries": 110,
    "late_deliveries": 8,
    "cancelled_deliveries": 2,
    "on_time_rate": 0.917
  },
  "by_supplier": [
    {
      "supplier_id": 10,
      "supplier_name": "Công ty Gạo Việt",
      "total_deliveries": 50,
      "on_time": 48,
      "late": 1,
      "cancelled": 1,
      "on_time_rate": 0.96,
      "avg_delivery_time_days": 2.5
    }
  ],
  "discrepancy_summary": {
    "total_items": 500,
    "items_with_discrepancy": 25,
    "discrepancy_rate": 0.05,
    "total_short": 150,
    "total_over": 50
  }
}
```

---

### 8.3. Product Price Comparison

**Endpoint**: `GET /reports/product-price-comparison`

**Headers**: `Authorization: Bearer {token}`

**Permission**: Aladdin only

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| product_id | integer | No | Specific product (or all) |
| date_from | date | No | From date |
| date_to | date | No | To date |

**Response** (200 OK):
```json
{
  "products": [
    {
      "product_id": 50,
      "product_code": "GAO-ST25",
      "product_name": "Gạo ST25",
      "base_unit": "kg",
      "suppliers": [
        {
          "supplier_id": 10,
          "supplier_name": "Công ty Gạo Việt",
          "current_price": 25000,
          "avg_price_30d": 24500,
          "min_price_30d": 24000,
          "max_price_30d": 26000,
          "price_trend": "up"
        },
        {
          "supplier_id": 11,
          "supplier_name": "Công ty Gạo Đồng Bằng",
          "current_price": 24500,
          "avg_price_30d": 24000,
          "min_price_30d": 23500,
          "max_price_30d": 24500,
          "price_trend": "up"
        }
      ],
      "lowest_supplier": {
        "supplier_id": 11,
        "supplier_name": "Công ty Gạo Đồng Bằng",
        "price": 24500
      }
    }
  ]
}
```

---

## 9. Dashboard API

### 9.1. Get Dashboard Data

**Endpoint**: `GET /dashboard`

**Headers**: `Authorization: Bearer {token}`

**Response for Aladdin** (200 OK):
```json
{
  "user_type": "ALADDIN",
  "statistics": {
    "pending_requests": 5,
    "pending_delivery_confirmations": 10,
    "overdue_deliveries": 2,
    "total_amount_this_month": 500000000
  },
  "recent_requests": [
    {
      "id": 1,
      "code": "YCMS-20251006-0001",
      "title": "Yêu cầu mua sắm tuần 41",
      "status": "SUBMITTED",
      "created_at": "2025-10-06T08:00:00Z"
    }
  ],
  "recent_deliveries": [
    {
      "id": 201,
      "code": "DN-20251007-0001",
      "supplier_name": "Công ty Gạo Việt",
      "status": "CONFIRMED",
      "delivery_date": "2025-10-15"
    }
  ],
  "alerts": [
    {
      "type": "OVERDUE",
      "message": "Có 2 phiếu giao hàng trễ hạn",
      "severity": "high",
      "link": "/delivery-notes?status=overdue"
    }
  ]
}
```

**Response for Supplier** (200 OK):
```json
{
  "user_type": "SUPPLIER",
  "supplier_id": 10,
  "supplier_name": "Công ty Gạo Việt",
  "statistics": {
    "pending_confirmations": 3,
    "deliveries_this_week": 8,
    "total_amount_this_month": 150000000
  },
  "pending_requests": [
    {
      "id": 1,
      "code": "YCMS-20251006-0001",
      "item_count": 5,
      "total_amount": 50000000,
      "request_date": "2025-10-06"
    }
  ],
  "upcoming_deliveries": [
    {
      "id": 201,
      "code": "DN-20251007-0001",
      "restaurant_name": "Nhà hàng Hà Nội 1",
      "delivery_date": "2025-10-15",
      "status": "CONFIRMED"
    }
  ]
}
```

---

## 10. Common Responses

### Success Response Format

```json
{
  "data": {...},
  "message": "Operation successful",
  "timestamp": "2025-10-06T10:00:00Z"
}
```

### Error Response Format

```json
{
  "error_code": "YCMS_001",
  "message": "Phiếu YCMS phải có ít nhất 1 sản phẩm",
  "details": {
    "field": "items",
    "reason": "empty_list"
  },
  "timestamp": "2025-10-06T10:00:00Z"
}
```

### Pagination Format

```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 11. HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, POST (non-creation) |
| 201 | Created | Successful POST (creation) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error, invalid input |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Not authorized (authenticated but no permission) |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate, state conflict |
| 422 | Unprocessable Entity | Semantic error (e.g., invalid state transition) |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Temporary unavailable (maintenance) |

---

## 12. Rate Limiting

- **Default**: 100 requests / minute / user
- **Email endpoints**: 10 requests / minute / user
- **Report endpoints**: 20 requests / minute / user

**Response when rate limited** (429):
```json
{
  "error_code": "RATE_LIMIT",
  "message": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

---

## 13. Versioning

- Current version: `v1`
- Version in URL: `/api/v1/...`
- Breaking changes → new version (v2)
- Old versions supported for 6 months

---

## 14. Security

### Authentication

- JWT Token in `Authorization` header
- Token expiry: 1 hour
- Refresh token expiry: 7 days

### Password Policy

- Min 8 characters
- Must contain: uppercase, lowercase, number, special char
- Password hashing: bcrypt

### API Keys (Future)

- For system-to-system integration
- Format: `X-API-Key: {key}`

---

## 15. Webhooks (Future)

**Events**:
- `procurement_request.submitted`
- `procurement_request.completed`
- `delivery_note.created`
- `delivery_note.delivered`

**Payload Example**:
```json
{
  "event": "procurement_request.submitted",
  "timestamp": "2025-10-06T09:30:00Z",
  "data": {
    "id": 1,
    "code": "YCMS-20251006-0001",
    ...
  }
}
```

---

**Version**: 1.0  
**Last Updated**: 2025-10-06  
**Author**: API Architect
