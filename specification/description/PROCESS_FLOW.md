# Đặc Tả Luồng Chương Trình (Process Flow Specification)

## Tổng Quan
Tài liệu này mô tả chi tiết các luồng nghiệp vụ (business flows) trong hệ thống quản lý yêu cầu mua sắm của Aladdin.

---

## 1. Luồng Chính (Main Flow)

### 1.1. Tổng Quan Luồng

```
[User Aladdin] 
    ↓
[Tạo Phiếu YCMS] 
    ↓
[Submit Phiếu YCMS] 
    ↓
[Gửi Email đến Nhà Cung Cấp]
    ↓
[User Nhà Cung Cấp Đăng Nhập]
    ↓
[Xem & Cập Nhật Phiếu YCMS]
    ↓
[Tạo Phiếu Giao Hàng]
    ↓
[User Aladdin Xác Nhận]
    ↓
[Giao Hàng & Cập Nhật]
```

---

## 2. Luồng Chi Tiết

### 2.1. Luồng 1: Tạo và Quản Lý Phiếu YCMS (Procurement Request Management)

#### 2.1.1. Khởi Tạo Phiếu YCMS

**Actor**: User Aladdin (quản lý mua hàng)

**Tiền Điều Kiện**:
- User đã đăng nhập với quyền Aladdin
- Danh sách nhà hàng, sản phẩm, nhà cung cấp đã được thiết lập

**Các Bước**:

1. **User Aladdin truy cập màn hình tạo phiếu YCMS**
   - Hệ thống hiển thị form tạo mới
   - Load danh sách nhà hàng, sản phẩm, nhà cung cấp

2. **Nhập thông tin header phiếu YCMS**
   - Tiêu đề phiếu
   - Ngày đề nghị
   - Ghi chú (optional)

3. **Thêm chi tiết sản phẩm**
   - Chọn sản phẩm từ danh mục chuẩn
   - Chọn nhà cung cấp
   - Chọn nhà hàng nhận
   - Nhập số lượng yêu cầu
   - Chọn đơn vị tính
   - Nhập/hiển thị giá (từ SupplierProduct)
   - Nhập địa điểm giao (mặc định từ Restaurant)
   - Chọn ngày muốn nhận
   - Thêm ghi chú (optional)

4. **Lưu nháp**
   - Status = DRAFT
   - Có thể chỉnh sửa, xóa
   - Tự động sinh mã phiếu: `YCMS-YYYYMMDD-XXXX`

5. **Validate dữ liệu**
   - Kiểm tra số lượng > 0
   - Kiểm tra ngày muốn nhận >= ngày đề nghị
   - Kiểm tra mapping sản phẩm - nhà cung cấp hợp lệ

**Kết Quả**:
- Phiếu YCMS được lưu với status DRAFT
- User có thể tiếp tục chỉnh sửa hoặc submit

#### 2.1.2. Submit Phiếu YCMS

**Actor**: User Aladdin

**Tiền Điều Kiện**:
- Phiếu YCMS ở trạng thái DRAFT
- Có ít nhất 1 chi tiết sản phẩm

**Các Bước**:

1. **User click "Submit"**
   - Hệ thống hiển thị confirm dialog
   - Tóm tắt thông tin: số lượng items, tổng giá trị, số nhà cung cấp

2. **Confirm submit**
   - Status chuyển: DRAFT → SUBMITTED
   - Lưu thời gian submit
   - Lock chỉnh sửa

3. **Tự động phân phối cho nhà cung cấp**
   - Group các items theo supplier_id
   - Tạo danh sách nhà cung cấp cần thông báo

4. **Gửi email thông báo**
   - Đến tất cả users của mỗi supplier
   - Nội dung:
     * Tiêu đề: "Phiếu yêu cầu mua sắm mới: [Mã YCMS]"
     * Link trực tiếp đến phiếu YCMS
     * Tóm tắt: số lượng items, ngày muốn nhận
   - Log notification vào database

5. **Tạo in-app notification**
   - Notification cho mỗi supplier
   - Type: NEW_REQUEST

**Kết Quả**:
- Phiếu YCMS status = SUBMITTED
- Email đã gửi đến nhà cung cấp
- Notification xuất hiện trong hệ thống

**Luồng Thay Thế**:
- Nếu gửi email thất bại: Log error nhưng vẫn chuyển status
- User có thể resend email thủ công

#### 2.1.3. Xem và Tìm Kiếm Phiếu YCMS

**Actor**: User Aladdin hoặc User Supplier

**Case A: User Aladdin**

1. **Truy cập danh sách YCMS**
   - Hiển thị tất cả phiếu YCMS
   - Không giới hạn theo supplier

2. **Bộ lọc**:
   - Theo trạng thái (DRAFT, SUBMITTED, CONFIRMED...)
   - Theo ngày tạo
   - Theo nhà cung cấp
   - Theo mã phiếu
   - Theo nhà hàng

3. **Xem chi tiết**
   - Thông tin header
   - Danh sách items (tất cả)
   - Danh sách phiếu giao hàng đã tạo (nếu có)
   - Lịch sử thay đổi (audit log)

**Case B: User Supplier**

1. **Truy cập danh sách YCMS**
   - Chỉ hiển thị phiếu có items của supplier mình
   - Filter tự động: `supplier_id = current_user.supplier_id`

2. **Bộ lọc**:
   - Theo trạng thái
   - Theo ngày tạo
   - Theo mã phiếu
   - Theo nhà hàng

3. **Xem chi tiết**
   - Thông tin header
   - Chỉ hiển thị items của supplier mình
   - Không thấy items của supplier khác
   - Danh sách phiếu giao hàng của mình

**Kết Quả**:
- User xem được thông tin phù hợp với quyền hạn

---

### 2.2. Luồng 2: Nhà Cung Cấp Cập Nhật Phiếu YCMS

#### 2.2.1. Login và Nhận Thông Báo

**Actor**: User Supplier

**Các Bước**:

1. **Nhận email thông báo**
   - Click link trong email
   - Redirect đến trang login (nếu chưa login)

2. **Đăng nhập**
   - Username/password
   - Xác thực user thuộc supplier đúng

3. **Xem notification**
   - Badge hiển thị số notification chưa đọc
   - List notifications theo thời gian

4. **Click vào notification**
   - Đánh dấu đã đọc
   - Navigate đến phiếu YCMS tương ứng

**Kết Quả**:
- User đăng nhập thành công
- Xem được phiếu YCMS của mình

#### 2.2.2. Cập Nhật Thông Tin Phiếu YCMS

**Actor**: User Supplier

**Tiền Điều Kiện**:
- Phiếu YCMS ở trạng thái SUBMITTED hoặc CONFIRMED

**Các Bước**:

1. **Xem chi tiết phiếu YCMS**
   - Hiển thị các items của supplier
   - Mỗi item có thể chỉnh sửa

2. **Cập nhật từng item**
   - Xác nhận số lượng có thể cung cấp
   - Cập nhật giá (nếu thay đổi)
   - Cập nhật ngày giao dự kiến (nếu khác yêu cầu)
   - Thêm ghi chú

3. **Đánh dấu item status**
   - CONFIRMED: Xác nhận có thể cung cấp
   - CANCELLED: Không thể cung cấp (ghi rõ lý do)

4. **Lưu thay đổi**
   - Validate dữ liệu
   - Update database
   - Log audit trail
   - Gửi notification cho Aladdin về thay đổi

5. **Confirm toàn bộ phiếu** (optional)
   - Khi đã xác nhận tất cả items
   - Status của những items đã confirm: PENDING → CONFIRMED

**Kết Quả**:
- Thông tin phiếu YCMS được cập nhật
- User Aladdin nhận notification về thay đổi
- Sẵn sàng để tạo phiếu giao hàng

**Luồng Thay Thế**:
- Nếu một số items không thể cung cấp:
  * Đánh dấu CANCELLED
  * Ghi rõ lý do
  * Aladdin có thể tìm supplier khác

---

### 2.3. Luồng 3: Tạo Phiếu Giao Hàng (Delivery Note Creation)

#### 2.3.1. Bóc Tách Phiếu YCMS thành Phiếu Giao Hàng

**Actor**: User Supplier

**Tiền Điều Kiện**:
- Items trong phiếu YCMS đã được confirm
- Items có cùng supplier_id với user

**Các Bước**:

1. **Truy cập màn hình tạo phiếu giao hàng**
   - Từ phiếu YCMS, click "Tạo Phiếu Giao Hàng"
   - Hệ thống hiển thị các items chưa được tạo phiếu giao hàng đủ

2. **Chọn tiêu chí bóc tách**
   - Theo nhà hàng (restaurant_id)
   - Theo ngày giao (delivery_date)
   - Có thể group nhiều items vào 1 phiếu

3. **Tự động gợi ý group**
   ```
   Ví dụ:
   YCMS-001 có 10 items cho Supplier A:
   - 3 items giao cho Restaurant 1 vào 15/10
   - 2 items giao cho Restaurant 1 vào 16/10
   - 5 items giao cho Restaurant 2 vào 15/10
   
   Hệ thống gợi ý tạo 3 phiếu:
   DN-001: Restaurant 1, 15/10 (3 items)
   DN-002: Restaurant 1, 16/10 (2 items)
   DN-003: Restaurant 2, 15/10 (5 items)
   ```

4. **Xác nhận và tạo phiếu**
   - Nhập thông tin header:
     * Mã phiếu giao hàng (auto-generate): `DN-YYYYMMDD-XXXX`
     * Ngày giao
     * Địa điểm giao (default từ Restaurant)
     * Ghi chú
   
   - Chi tiết items:
     * Copy từ ProcurementRequestItem
     * Số lượng yêu cầu
     * Đơn vị tính
     * Đơn giá
     * Tính tổng tiền

5. **Validate**
   - Tổng quantity_ordered của các DN items <= quantity_requested trong YCMS item
   - Ngày giao hợp lý (>= current date)
   - Cùng supplier và restaurant

6. **Lưu phiếu giao hàng**
   - Status = DRAFT
   - Link đến procurement_request_item_id

**Kết Quả**:
- Phiếu giao hàng được tạo với status DRAFT
- Items trong YCMS được đánh dấu đã có phiếu giao hàng (partial hoặc full)

#### 2.3.2. Submit Phiếu Giao Hàng

**Actor**: User Supplier

**Các Bước**:

1. **Review phiếu giao hàng**
   - Kiểm tra thông tin
   - Có thể chỉnh sửa nếu còn DRAFT

2. **Submit phiếu**
   - Status: DRAFT → CONFIRMED
   - Gửi notification cho Aladdin
   - Gửi email thông báo có phiếu giao hàng mới

3. **Print phiếu giao hàng** (optional)
   - Generate PDF
   - Có thể in hoặc download

**Kết Quả**:
- Phiếu giao hàng status = CONFIRMED
- Aladdin nhận được thông báo

---

### 2.4. Luồng 4: Theo Dõi và Nhận Hàng

#### 2.4.1. Aladdin Xem Phiếu Giao Hàng

**Actor**: User Aladdin

**Các Bước**:

1. **Nhận notification**
   - Thông báo có phiếu giao hàng mới
   - Click để xem chi tiết

2. **Review phiếu giao hàng**
   - Thông tin header
   - Danh sách items
   - So sánh với YCMS gốc

3. **Xác nhận phiếu** (optional)
   - Nếu đúng, có thể approve
   - Nếu sai, yêu cầu supplier chỉnh sửa

**Kết Quả**:
- Phiếu giao hàng được xác nhận hoặc yêu cầu sửa

#### 2.4.2. Cập Nhật Trạng Thái Giao Hàng

**Actor**: User Supplier hoặc User Aladdin

**Case A: Supplier cập nhật**

1. **Đang vận chuyển**
   - Status: CONFIRMED → IN_TRANSIT
   - Nhập thời gian xuất hàng

2. **Đã giao hàng**
   - Status: IN_TRANSIT → DELIVERED
   - Nhập thời gian giao
   - Nhập số lượng thực giao (cho từng item)

**Case B: Aladdin xác nhận nhận hàng**

1. **Xem phiếu giao hàng**
   - Nhà hàng báo đã nhận
   
2. **Cập nhật số lượng thực nhận**
   - Nhập `quantity_delivered` cho từng item
   - Có thể khác `quantity_ordered` (thiếu, thừa, hỏng)
   - Ghi chú lý do chênh lệch

3. **Confirm đã nhận**
   - Status: DELIVERED
   - Lưu thời gian
   - Tính toán tổng tiền thực tế

4. **Đối soát**
   - So sánh quantity_ordered vs quantity_delivered
   - Generate báo cáo chênh lệch
   - Xử lý thanh toán

**Kết Quả**:
- Phiếu giao hàng hoàn tất
- Dữ liệu thực nhận được cập nhật
- YCMS item status: DELIVERED

#### 2.4.3. Hoàn Tất Phiếu YCMS

**Tự động trigger khi**:
- Tất cả items trong YCMS có status = DELIVERED hoặc CANCELLED

**Hệ thống tự động**:
1. Cập nhật status YCMS: PROCESSING → COMPLETED
2. Gửi notification tổng kết
3. Archive phiếu (có thể xem nhưng không chỉnh sửa)

---

## 3. Luồng Phụ (Sub-Flows)

### 3.1. Quản Lý Mapping Sản Phẩm

**Mục đích**: Đồng nhất danh mục sản phẩm giữa Aladdin và Supplier

**Actor**: Admin Aladdin hoặc Supplier Admin

**Các Bước**:

1. **Supplier upload danh sách sản phẩm**
   - File Excel/CSV
   - Cột: Mã SP nhà cung cấp, Tên SP, Đơn vị, Giá

2. **Hệ thống đề xuất mapping**
   - Dùng AI/fuzzy matching để map với Product chuẩn
   - Hiển thị độ tin cậy (confidence score)

3. **User xác nhận/điều chỉnh mapping**
   - Chọn sản phẩm chuẩn đúng
   - Nhập hệ số quy đổi
   - Ví dụ: "Gạo ST25 bao 50kg" → Product: "Gạo ST25" (kg), conversion = 50

4. **Lưu SupplierProduct**
   - Tạo record mapping
   - Dùng cho YCMS sau này

**Kết Quả**:
- Danh mục sản phẩm được đồng nhất
- Dễ dàng tạo YCMS với giá và đơn vị chuẩn

### 3.2. Báo Cáo và Thống Kê

**Actor**: User Aladdin (Manager)

**Các loại báo cáo**:

1. **Báo cáo YCMS**
   - Theo thời gian: tổng số phiếu, tổng giá trị
   - Theo nhà cung cấp: số lượng, giá trị, tỷ lệ hoàn thành
   - Theo nhà hàng: nhu cầu mua hàng

2. **Báo cáo Giao Hàng**
   - Tỷ lệ giao đúng hạn
   - Chênh lệch số lượng (ordered vs delivered)
   - Nhà cung cấp có vấn đề

3. **Báo cáo Sản Phẩm**
   - Top sản phẩm mua nhiều nhất
   - Giá theo thời gian
   - So sánh giá giữa các nhà cung cấp

4. **Dashboard**
   - Tổng quan tình hình mua sắm
   - Phiếu YCMS đang pending
   - Phiếu giao hàng cần xác nhận

---

## 4. Luồng Xử Lý Ngoại Lệ

### 4.1. Supplier Không Thể Cung Cấp

**Scenario**: Supplier báo không đủ hàng hoặc không cung cấp được

**Xử Lý**:

1. Supplier đánh dấu item status = CANCELLED trong YCMS
2. Ghi rõ lý do (hết hàng, giá thay đổi...)
3. Aladdin nhận notification
4. Aladdin có thể:
   - Tìm supplier khác (tạo YCMS mới)
   - Giảm số lượng
   - Hủy yêu cầu

### 4.2. Giao Hàng Sai Hoặc Thiếu

**Scenario**: Số lượng thực nhận khác số lượng order

**Xử Lý**:

1. Aladdin nhập `quantity_delivered` khác `quantity_ordered`
2. Ghi rõ lý do (thiếu, thừa, hỏng)
3. Hệ thống tự động:
   - Tính toán chênh lệch
   - Cập nhật giá trị thanh toán
   - Tạo issue để xử lý (hoàn tiền, giao bù...)
4. Notification cho supplier
5. Có thể tạo phiếu giao bù (nếu thiếu)

### 4.3. Hủy Phiếu YCMS

**Actor**: User Aladdin

**Điều kiện**: Chỉ hủy khi chưa có phiếu giao hàng DELIVERED

**Xử Lý**:

1. User click "Hủy phiếu"
2. Nhập lý do hủy
3. Confirm
4. Status: → CANCELLED
5. Gửi notification cho tất cả suppliers liên quan
6. Các phiếu giao hàng DRAFT/CONFIRMED cũng bị hủy

### 4.4. Trễ Hạn Giao Hàng

**Scenario**: Quá ngày `expected_delivery_date` nhưng chưa giao

**Xử Lý**:

1. Hệ thống tự động check hàng ngày (cron job)
2. Tìm các DeliveryNote có:
   - `delivery_date` < current_date
   - Status != DELIVERED
3. Đánh dấu cảnh báo (flag)
4. Gửi notification cho Aladdin và Supplier
5. Hiển thị trên dashboard
6. Có thể escalate nếu trễ quá X ngày

---

## 5. Luồng Tích Hợp Email

### 5.1. Email Templates

**Template 1: Phiếu YCMS Mới**
```
Subject: [YCMS] Phiếu yêu cầu mua sắm mới: {code}

Kính gửi {supplier_name},

Aladdin vừa tạo phiếu yêu cầu mua sắm mới:
- Mã phiếu: {code}
- Ngày đề nghị: {request_date}
- Số lượng sản phẩm: {item_count}
- Tổng giá trị dự kiến: {total_amount}

Vui lòng đăng nhập hệ thống để xem chi tiết và xác nhận:
{link_to_ycms}

Trân trọng,
Hệ thống quản lý mua sắm Aladdin
```

**Template 2: Phiếu Giao Hàng Mới**
```
Subject: [Delivery] Phiếu giao hàng mới: {code}

Kính gửi Aladdin,

{supplier_name} vừa tạo phiếu giao hàng:
- Mã phiếu: {code}
- Nhà hàng: {restaurant_name}
- Ngày giao: {delivery_date}
- Số lượng items: {item_count}
- Tổng giá trị: {total_amount}

Xem chi tiết: {link_to_delivery_note}

Trân trọng,
Hệ thống quản lý mua sắm Aladdin
```

**Template 3: Cập Nhật Phiếu**
```
Subject: [Update] Cập nhật phiếu {code}

Kính gửi {recipient},

Có cập nhật mới trên phiếu {code}:
{changes_summary}

Xem chi tiết: {link}

Trân trọng,
Hệ thống quản lý mua sắm Aladdin
```

### 5.2. Email Sending Logic

**Trigger Events**:
1. YCMS submitted → Email to suppliers
2. YCMS updated by supplier → Email to Aladdin
3. DeliveryNote created → Email to Aladdin
4. DeliveryNote status changed → Email to relevant party
5. Overdue delivery → Reminder email

**Implementation**:
- Dùng queue system (Celery) để gửi async
- Retry mechanism nếu thất bại
- Log email sent status
- Unsubscribe option

---

## 6. Luồng Permission & Authorization

### 6.1. User Aladdin Permissions

**Có quyền**:
- Xem tất cả YCMS, DeliveryNote
- Tạo, sửa, xóa, submit YCMS
- Xác nhận DeliveryNote
- Cập nhật quantity_delivered
- Xem tất cả suppliers, restaurants
- Quản lý master data (Product, Category...)
- Xem tất cả reports

**Không có quyền**:
- Tạo DeliveryNote (chỉ supplier mới tạo)
- Sửa giá của supplier (chỉ xem)

### 6.2. User Supplier Permissions

**Có quyền**:
- Xem YCMS có items của supplier mình
- Cập nhật thông tin items trong YCMS của mình
- Tạo, sửa, submit DeliveryNote của mình
- Cập nhật status DeliveryNote của mình
- Quản lý SupplierProduct của mình
- Xem reports liên quan đến mình

**Không có quyền**:
- Xem YCMS của supplier khác
- Tạo YCMS
- Xem tất cả restaurants (chỉ xem restaurant có trong YCMS của mình)
- Sửa master data Product
- Xem reports tổng thể

### 6.3. Implementation

**Middleware/Decorator**:
```python
@require_permission("ycms.view_all")
def get_all_ycms():
    # Aladdin only
    pass

@require_permission("ycms.view_own")
def get_supplier_ycms():
    # Filter by supplier_id
    pass
```

**Row-Level Security**:
- Supplier user chỉ query được records có `supplier_id` = user's supplier
- Implement ở Repository layer

---

## 7. State Diagram

### 7.1. ProcurementRequest States

```
        [DRAFT]
           ↓ (submit)
      [SUBMITTED]
           ↓ (supplier confirms)
      [CONFIRMED]
           ↓ (delivery notes created)
     [PROCESSING]
           ↓ (all items delivered/cancelled)
      [COMPLETED]
      
      [CANCELLED] ← (can cancel from any state)
```

### 7.2. DeliveryNote States

```
        [DRAFT]
           ↓ (submit)
      [CONFIRMED]
           ↓ (ship out)
      [IN_TRANSIT]
           ↓ (received)
      [DELIVERED]
      
      [CANCELLED] ← (can cancel before delivered)
```

---

## 8. Sequence Diagrams

### 8.1. Tạo và Submit YCMS

```
User(Aladdin)    API           Database      EmailService    User(Supplier)
     |            |                |                |              |
     |--POST /ycms--------------->|                |              |
     |            |--insert YCMS-->|                |              |
     |            |--insert items->|                |              |
     |<--201 Created--------------|                |              |
     |            |                |                |              |
     |--PUT /ycms/{id}/submit---->|                |              |
     |            |--update status->|               |              |
     |            |--get suppliers->|               |              |
     |            |---send_email(supplier_list)---->|              |
     |            |                |                |--email------>|
     |            |--create notification----------->|              |
     |<--200 OK-------------------|                |              |
```

### 8.2. Tạo Delivery Note

```
User(Supplier)   API           Database      EmailService    User(Aladdin)
     |            |                |                |              |
     |--GET /ycms/{id}----------->|                |              |
     |<--return YCMS items--------|                |              |
     |            |                |                |              |
     |--POST /delivery-notes----->|                |              |
     |            |--insert DN---->|                |              |
     |            |--insert items->|                |              |
     |            |--update YCMS item status------->|              |
     |<--201 Created--------------|                |              |
     |            |                |                |              |
     |--PUT /delivery-notes/{id}/submit---------->|               |
     |            |--update status->|               |              |
     |            |---send_email(aladdin_users)---->|              |
     |            |                |                |--email------>|
     |<--200 OK-------------------|                |              |
```

---

## 9. Business Rules Summary

### 9.1. Validation Rules

1. **YCMS Creation**:
   - Phải có ít nhất 1 item
   - `quantity_requested` > 0
   - `expected_delivery_date` >= `request_date`
   - Product-Supplier mapping phải tồn tại

2. **Delivery Note Creation**:
   - Chỉ tạo được từ YCMS items đã CONFIRMED
   - Tổng `quantity_ordered` trong tất cả DN <= `quantity_requested` trong YCMS
   - `delivery_date` >= current_date
   - Supplier của DN phải match supplier của items

3. **Receiving Goods**:
   - `quantity_delivered` >= 0
   - Có thể khác `quantity_ordered` nhưng phải có ghi chú

### 9.2. Business Logic

1. **Auto-calculation**:
   - `total_amount` = `quantity` * `unit_price`
   - YCMS total = sum of all items
   - DN total = sum of delivered items

2. **Status Auto-update**:
   - YCMS item status = DELIVERED khi tất cả DN items delivered
   - YCMS status = COMPLETED khi tất cả items delivered/cancelled

3. **Notification Triggers**:
   - YCMS submitted → Notify suppliers
   - YCMS item updated → Notify Aladdin
   - DN created → Notify Aladdin
   - DN delivered → Notify Aladdin
   - Overdue → Notify both parties

---

## 10. Error Handling

### 10.1. Common Errors

| Error Code | Scenario | HTTP Status | Message |
|------------|----------|-------------|---------|
| YCMS_001 | No items in YCMS | 400 | "Phiếu YCMS phải có ít nhất 1 sản phẩm" |
| YCMS_002 | Invalid quantity | 400 | "Số lượng phải lớn hơn 0" |
| YCMS_003 | Already submitted | 400 | "Phiếu đã được submit, không thể chỉnh sửa" |
| DN_001 | Exceed YCMS quantity | 400 | "Số lượng giao vượt quá yêu cầu" |
| DN_002 | Wrong supplier | 403 | "Bạn không có quyền tạo phiếu giao hàng cho nhà cung cấp này" |
| AUTH_001 | Unauthorized | 401 | "Vui lòng đăng nhập" |
| AUTH_002 | Forbidden | 403 | "Bạn không có quyền truy cập" |

### 10.2. Error Response Format

```json
{
  "error_code": "YCMS_001",
  "message": "Phiếu YCMS phải có ít nhất 1 sản phẩm",
  "details": {
    "field": "items",
    "reason": "empty_list"
  },
  "timestamp": "2025-10-06T10:30:00Z"
}
```

---

## 11. Performance Considerations

### 11.1. Query Optimization

1. **Large YCMS List**:
   - Pagination: 20 items per page
   - Eager load relationships (items, supplier, restaurant)
   - Index on (supplier_id, created_at)

2. **Supplier Filter**:
   - Pre-filter at database level
   - Cache supplier's YCMS list (Redis, 5 min TTL)

3. **Dashboard Aggregation**:
   - Pre-calculate daily aggregates (cron job)
   - Cache dashboard data

### 11.2. Scalability

1. **Email Queue**:
   - Async processing with Celery
   - Bulk email sending (group recipients)

2. **File Storage**:
   - PDF files → S3/Cloud Storage
   - CDN for static assets

3. **Database**:
   - Partition large tables by date
   - Archive old YCMS (> 1 year)

---

## 12. Integration Points

### 12.1. External Systems

1. **Email Service**:
   - SMTP / SendGrid / AWS SES
   - Template engine: Jinja2

2. **SMS (Future)**:
   - Twilio for urgent notifications

3. **Payment System (Future)**:
   - Integration với hệ thống kế toán
   - Auto-create payment records

4. **ERP (Future)**:
   - Sync inventory
   - Sync orders

---

**Version**: 1.0  
**Last Updated**: 2025-10-06  
**Author**: System Architect
