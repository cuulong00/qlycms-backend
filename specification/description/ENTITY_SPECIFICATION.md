# Đặc Tả Thực Thể (Entity Specification)

## Tổng Quan
Tài liệu này mô tả chi tiết các thực thể (entities) trong hệ thống quản lý yêu cầu mua sắm (Procurement Management System) của Aladdin.

---

## 1. User (Người Dùng)

### 1.1. Mô Tả
Đại diện cho người dùng trong hệ thống, bao gồm nhân viên Aladdin và đối tác nhà cung cấp.

### 1.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | UUID/Integer | Yes | Khóa chính, định danh duy nhất |
| username | String(100) | Yes | Tên đăng nhập, unique |
| email | String(255) | Yes | Email người dùng, unique |
| full_name | String(255) | Yes | Họ và tên đầy đủ |
| password_hash | String(255) | Yes | Mật khẩu đã mã hóa |
| user_type | Enum | Yes | Loại user: ALADDIN, SUPPLIER |
| supplier_id | Integer | No | ID nhà cung cấp (null nếu là user Aladdin) |
| is_active | Boolean | Yes | Trạng thái kích hoạt |
| phone_number | String(20) | No | Số điện thoại |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |
| last_login | DateTime | No | Lần đăng nhập cuối |

### 1.3. Ràng Buộc
- `username` và `email` phải unique
- `user_type` = SUPPLIER thì `supplier_id` phải có giá trị
- `user_type` = ALADDIN thì `supplier_id` phải null

### 1.4. Quan Hệ
- Belongs to: `Supplier` (nếu user_type = SUPPLIER)
- Has many: `ProcurementRequest` (người tạo)
- Has many: `DeliveryNote` (người tạo/cập nhật)

---

## 2. Supplier (Nhà Cung Cấp)

### 2.1. Mô Tả
Đại diện cho các đối tác nhà cung cấp của Aladdin.

### 2.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| code | String(50) | Yes | Mã nhà cung cấp, unique |
| name | String(255) | Yes | Tên nhà cung cấp |
| tax_code | String(50) | No | Mã số thuế |
| address | Text | No | Địa chỉ |
| phone | String(20) | No | Số điện thoại |
| email | String(255) | No | Email liên hệ |
| contact_person | String(255) | No | Người liên hệ |
| is_active | Boolean | Yes | Trạng thái hoạt động |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 2.3. Ràng Buộc
- `code` phải unique
- `email` phải unique nếu có giá trị

### 2.4. Quan Hệ
- Has many: `User` (nhân viên nhà cung cấp)
- Has many: `ProcurementRequestItem` (các yêu cầu)
- Has many: `SupplierProduct` (sản phẩm)

---

## 3. Restaurant (Nhà Hàng)

### 3.1. Mô Tả
Đại diện cho các nhà hàng trong hệ thống Aladdin (100 nhà hàng toàn quốc).

### 3.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| code | String(50) | Yes | Mã nhà hàng, unique |
| name | String(255) | Yes | Tên nhà hàng |
| address | Text | Yes | Địa chỉ giao hàng |
| province | String(100) | No | Tỉnh/thành phố |
| district | String(100) | No | Quận/huyện |
| phone | String(20) | No | Số điện thoại |
| manager_name | String(255) | No | Tên quản lý |
| is_active | Boolean | Yes | Trạng thái hoạt động |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 3.3. Ràng Buộc
- `code` phải unique

### 3.4. Quan Hệ
- Has many: `ProcurementRequestItem` (các yêu cầu mua hàng)
- Has many: `DeliveryNote` (các phiếu giao hàng)

---

## 4. Product (Sản Phẩm)

### 4.1. Mô Tả
Danh mục sản phẩm chuẩn hóa trong hệ thống Aladdin.

### 4.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| code | String(50) | Yes | Mã sản phẩm chuẩn, unique |
| name | String(255) | Yes | Tên sản phẩm chuẩn |
| category_id | Integer | No | ID danh mục sản phẩm |
| base_unit | String(50) | Yes | Đơn vị tính cơ bản (kg, lit, cái...) |
| description | Text | No | Mô tả sản phẩm |
| is_active | Boolean | Yes | Trạng thái hoạt động |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 4.3. Ràng Buộc
- `code` phải unique

### 4.4. Quan Hệ
- Belongs to: `ProductCategory`
- Has many: `SupplierProduct` (mapping với sản phẩm nhà cung cấp)
- Has many: `ProcurementRequestItem`

---

## 5. ProductCategory (Nhóm Sản Phẩm)

### 5.1. Mô Tả
Phân loại sản phẩm theo nhóm (nhóm nguyên liệu, thực phẩm...).

### 5.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| code | String(50) | Yes | Mã nhóm, unique |
| name | String(255) | Yes | Tên nhóm |
| parent_id | Integer | No | ID nhóm cha (phân cấp) |
| description | Text | No | Mô tả |
| is_active | Boolean | Yes | Trạng thái |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 5.3. Quan Hệ
- Has many: `Product`
- Self-referencing: `parent_id` -> `id` (phân cấp nhóm)

---

## 6. SupplierProduct (Sản Phẩm Nhà Cung Cấp)

### 6.1. Mô Tả
Mapping giữa sản phẩm chuẩn và sản phẩm của từng nhà cung cấp (để giải quyết vấn đề quy cách đóng gói, tên gọi khác nhau).

### 6.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| supplier_id | Integer | Yes | ID nhà cung cấp |
| product_id | Integer | Yes | ID sản phẩm chuẩn |
| supplier_product_code | String(100) | Yes | Mã sản phẩm của nhà cung cấp |
| supplier_product_name | String(255) | Yes | Tên sản phẩm của nhà cung cấp |
| supplier_unit | String(50) | Yes | Đơn vị tính của nhà cung cấp |
| conversion_factor | Decimal(10,4) | Yes | Hệ số quy đổi sang đơn vị chuẩn |
| unit_price | Decimal(15,2) | No | Đơn giá |
| is_active | Boolean | Yes | Trạng thái |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 6.3. Ràng Buộc
- Unique constraint: (`supplier_id`, `supplier_product_code`)
- `conversion_factor` > 0

### 6.4. Quan Hệ
- Belongs to: `Supplier`
- Belongs to: `Product`

### 6.5. Ví Dụ
```
Sản phẩm chuẩn: Gạo ST25 (đơn vị: kg)
Nhà cung cấp A: Gạo ST25 bao 50kg (conversion_factor = 50)
Nhà cung cấp B: Gạo ST25 thùng 25kg (conversion_factor = 25)
```

---

## 7. ProcurementRequest (Phiếu Yêu Cầu Mua Sắm - YCMS)

### 7.1. Mô Tả
Phiếu yêu cầu mua sắm tổng hợp cho nhiều nhà hàng và nhiều nhà cung cấp.

### 7.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| code | String(50) | Yes | Mã phiếu YCMS, unique |
| title | String(255) | Yes | Tiêu đề phiếu |
| request_date | Date | Yes | Ngày đề nghị |
| status | Enum | Yes | Trạng thái: DRAFT, SUBMITTED, CONFIRMED, PROCESSING, COMPLETED, CANCELLED |
| created_by | Integer | Yes | User tạo phiếu (Aladdin) |
| submitted_at | DateTime | No | Thời gian submit |
| notes | Text | No | Ghi chú |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 7.3. Ràng Buộc
- `code` phải unique
- `created_by` phải là user Aladdin
- Status transition rules apply (DRAFT -> SUBMITTED -> CONFIRMED...)

### 7.4. Quan Hệ
- Belongs to: `User` (created_by)
- Has many: `ProcurementRequestItem`

### 7.5. Vòng Đời Trạng Thái
```
DRAFT (Nháp) 
  -> SUBMITTED (Đã gửi) 
  -> CONFIRMED (Đã xác nhận - nhà cung cấp xác nhận)
  -> PROCESSING (Đang xử lý - tạo phiếu giao hàng)
  -> COMPLETED (Hoàn thành)
  -> CANCELLED (Hủy - có thể hủy từ bất kỳ trạng thái nào)
```

---

## 8. ProcurementRequestItem (Chi Tiết Phiếu YCMS)

### 8.1. Mô Tả
Chi tiết từng dòng sản phẩm trong phiếu yêu cầu mua sắm.

### 8.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| procurement_request_id | Integer | Yes | ID phiếu YCMS |
| product_id | Integer | Yes | ID sản phẩm chuẩn |
| supplier_id | Integer | Yes | ID nhà cung cấp |
| restaurant_id | Integer | Yes | ID nhà hàng nhận |
| quantity_requested | Decimal(15,3) | Yes | Số lượng yêu cầu |
| unit | String(50) | Yes | Đơn vị tính |
| unit_price | Decimal(15,2) | No | Đơn giá |
| total_amount | Decimal(15,2) | No | Thành tiền (tính toán) |
| delivery_address | Text | Yes | Địa điểm giao hàng |
| expected_delivery_date | Date | Yes | Ngày muốn nhận |
| notes | Text | No | Ghi chú |
| status | Enum | Yes | Trạng thái: PENDING, CONFIRMED, DELIVERED, CANCELLED |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 8.3. Ràng Buộc
- `quantity_requested` > 0
- `total_amount` = `quantity_requested` * `unit_price`
- `expected_delivery_date` >= `procurement_request.request_date`

### 8.4. Quan Hệ
- Belongs to: `ProcurementRequest`
- Belongs to: `Product`
- Belongs to: `Supplier`
- Belongs to: `Restaurant`
- Has many: `DeliveryNoteItem` (được tách thành nhiều phiếu giao hàng)

---

## 9. DeliveryNote (Phiếu Giao Hàng)

### 9.1. Mô Tả
Phiếu giao hàng được tách ra từ phiếu YCMS, theo từng ngày và từng nhà hàng.

### 9.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| code | String(50) | Yes | Mã phiếu giao hàng, unique |
| procurement_request_id | Integer | Yes | ID phiếu YCMS gốc |
| supplier_id | Integer | Yes | ID nhà cung cấp |
| restaurant_id | Integer | Yes | ID nhà hàng nhận |
| delivery_date | Date | Yes | Ngày giao hàng |
| delivery_address | Text | Yes | Địa điểm giao hàng |
| status | Enum | Yes | Trạng thái: DRAFT, CONFIRMED, IN_TRANSIT, DELIVERED, CANCELLED |
| total_amount | Decimal(15,2) | No | Tổng tiền (tính toán) |
| created_by | Integer | Yes | User tạo (supplier) |
| confirmed_by | Integer | No | User xác nhận (Aladdin) |
| confirmed_at | DateTime | No | Thời gian xác nhận |
| delivered_at | DateTime | No | Thời gian giao hàng |
| notes | Text | No | Ghi chú |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 9.3. Ràng Buộc
- `code` phải unique
- `created_by` phải là user của `supplier_id` tương ứng
- `delivery_date` phải nằm trong khoảng thời gian hợp lý

### 9.4. Quan Hệ
- Belongs to: `ProcurementRequest`
- Belongs to: `Supplier`
- Belongs to: `Restaurant`
- Belongs to: `User` (created_by, confirmed_by)
- Has many: `DeliveryNoteItem`

### 9.5. Vòng Đời Trạng Thái
```
DRAFT (Nháp) 
  -> CONFIRMED (Đã xác nhận)
  -> IN_TRANSIT (Đang vận chuyển)
  -> DELIVERED (Đã giao)
  -> CANCELLED (Hủy)
```

---

## 10. DeliveryNoteItem (Chi Tiết Phiếu Giao Hàng)

### 10.1. Mô Tả
Chi tiết từng dòng sản phẩm trong phiếu giao hàng.

### 10.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| delivery_note_id | Integer | Yes | ID phiếu giao hàng |
| procurement_request_item_id | Integer | Yes | ID chi tiết YCMS gốc |
| product_id | Integer | Yes | ID sản phẩm |
| product_code | String(50) | Yes | Mã sản phẩm |
| product_name | String(255) | Yes | Tên sản phẩm |
| quantity_ordered | Decimal(15,3) | Yes | Số lượng yêu cầu |
| quantity_delivered | Decimal(15,3) | No | Số lượng thực nhận |
| unit | String(50) | Yes | Đơn vị tính |
| unit_price | Decimal(15,2) | Yes | Đơn giá |
| total_amount | Decimal(15,2) | No | Tổng tiền (tính toán) |
| notes | Text | No | Ghi chú |
| created_at | DateTime | Yes | Thời gian tạo |
| updated_at | DateTime | Yes | Thời gian cập nhật |

### 10.3. Ràng Buộc
- `quantity_ordered` > 0
- `quantity_delivered` >= 0
- `total_amount` = `quantity_delivered` * `unit_price` (nếu đã giao)
- Sum of `quantity_ordered` for same `procurement_request_item_id` <= original `quantity_requested`

### 10.4. Quan Hệ
- Belongs to: `DeliveryNote`
- Belongs to: `ProcurementRequestItem`
- Belongs to: `Product`

---

## 11. AuditLog (Nhật Ký Hệ Thống)

### 11.1. Mô Tả
Ghi lại các thay đổi quan trọng trong hệ thống.

### 11.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| user_id | Integer | Yes | User thực hiện |
| entity_type | String(100) | Yes | Loại thực thể (ProcurementRequest, DeliveryNote...) |
| entity_id | Integer | Yes | ID thực thể |
| action | Enum | Yes | Hành động: CREATE, UPDATE, DELETE, STATUS_CHANGE |
| old_value | JSON | No | Giá trị cũ |
| new_value | JSON | No | Giá trị mới |
| ip_address | String(50) | No | Địa chỉ IP |
| created_at | DateTime | Yes | Thời gian |

---

## 12. Notification (Thông Báo)

### 12.1. Mô Tả
Thông báo gửi cho người dùng (email, in-app).

### 12.2. Thuộc Tính

| Tên Trường | Kiểu Dữ Liệu | Bắt Buộc | Mô Tả |
|------------|--------------|----------|-------|
| id | Integer | Yes | Khóa chính |
| user_id | Integer | No | User nhận (null = all users của supplier) |
| supplier_id | Integer | No | Nhà cung cấp nhận |
| type | Enum | Yes | Loại: NEW_REQUEST, REQUEST_UPDATED, DELIVERY_CONFIRMED |
| title | String(255) | Yes | Tiêu đề |
| message | Text | Yes | Nội dung |
| reference_type | String(100) | No | Loại tham chiếu |
| reference_id | Integer | No | ID tham chiếu |
| is_read | Boolean | Yes | Đã đọc |
| sent_at | DateTime | Yes | Thời gian gửi |
| read_at | DateTime | No | Thời gian đọc |

---

## Sơ Đồ Quan Hệ Tổng Quan

```
User ──────┬──> Supplier
           │
           └──> ProcurementRequest ──> ProcurementRequestItem ──┬──> Product ──> ProductCategory
                                                                  │
                                                                  ├──> Supplier ──> SupplierProduct
                                                                  │
                                                                  ├──> Restaurant
                                                                  │
                                                                  └──> DeliveryNoteItem <── DeliveryNote
                                                                            │
                                                                            └──> Supplier
                                                                            └──> Restaurant
```

---

## Lưu Ý Kỹ Thuật

1. **Soft Delete**: Tất cả entities nên hỗ trợ soft delete (thêm trường `deleted_at`)
2. **Indexing**: 
   - Index trên các trường `code`, `email`, foreign keys
   - Composite index trên (`supplier_id`, `created_at`) cho truy vấn theo supplier
3. **Validation**: Implement validation ở cả API level và Database level
4. **Audit Trail**: Sử dụng database triggers hoặc application-level hooks để ghi audit log
5. **Concurrency**: Sử dụng optimistic locking (version field) cho các entities quan trọng

---

**Version**: 1.0  
**Last Updated**: 2025-10-06  
**Author**: System Architect
