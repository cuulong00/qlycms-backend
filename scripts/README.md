# DATABASE SETUP SCRIPTS

## 📁 Files trong thư mục này

- `create_users_table.sql` - SQL script tạo bảng users
- `run_create_users_table.ps1` - PowerShell script với validation đầy đủ
- `quick_create_users.ps1` - Quick run script (không có confirmation)

---

## 🚀 CÁCH SỬ DỤNG

### Option 1: Chạy Script PowerShell (Recommended)

Script này có validation và confirmation:

```powershell
# Từ thư mục root của project
.\scripts\run_create_users_table.ps1
```

Script sẽ:
- ✅ Kiểm tra psql có sẵn
- ✅ Kiểm tra file SQL tồn tại
- ✅ Test kết nối database
- ⚠️ Xác nhận trước khi chạy
- 🚀 Thực thi SQL script
- ✅ Hiển thị kết quả

### Option 2: Quick Run (Không confirmation)

```powershell
# Từ thư mục root của project
.\scripts\quick_create_users.ps1
```

### Option 3: Chạy trực tiếp với psql

```powershell
# Set password
$env:PGPASSWORD = "portal"

# Run SQL script
psql -h localhost -p 5432 -U portal -d portal -f .\scripts\create_users_table.sql

# Clean up
Remove-Item Env:\PGPASSWORD
```

### Option 4: Chạy từ command line (CMD/PowerShell)

```bash
psql -h localhost -p 5432 -U portal -d portal -f scripts\create_users_table.sql
```

---

## 📋 YÊU CẦU

### 1. PostgreSQL Client (psql)

Kiểm tra đã cài đặt:
```powershell
psql --version
```

Nếu chưa có, download tại: https://www.postgresql.org/download/

### 2. Database đã tồn tại

```sql
-- Tạo database nếu chưa có
CREATE DATABASE portal;
```

### 3. User có quyền

User `portal` cần có quyền:
- CREATE TABLE
- CREATE TYPE
- CREATE INDEX
- CREATE TRIGGER
- INSERT, SELECT, UPDATE, DELETE

---

## 📊 BẢNG USERS ĐƯỢC TẠO

### Cấu trúc

```sql
Table: users
├── id (SERIAL PRIMARY KEY)
├── email (VARCHAR(320) UNIQUE)
├── hashed_password (VARCHAR(1024))
├── is_active (BOOLEAN)
├── is_superuser (BOOLEAN)
├── is_verified (BOOLEAN)
├── user_type (user_type_enum: 'aladdin' | 'supplier')
├── role (user_role_enum)
├── first_name (VARCHAR(100))
├── last_name (VARCHAR(100))
├── phone_number (VARCHAR(20))
├── avatar_url (VARCHAR(500))
├── supplier_id (INTEGER)
├── created_at (TIMESTAMP WITH TIME ZONE)
├── updated_at (TIMESTAMP WITH TIME ZONE)
└── last_login (TIMESTAMP WITH TIME ZONE)
```

### Enums

**user_type_enum:**
- `aladdin` - Nhân viên Aladdin Restaurant Chain
- `supplier` - Nhân viên nhà cung cấp

**user_role_enum:**
- `super_admin` - Full access to everything
- `aladdin_admin` - Quản lý toàn bộ YCMS và master data
- `aladdin_staff` - Tạo YCMS, xác nhận giao hàng
- `supplier_admin` - Quản lý YCMS và delivery notes của supplier
- `supplier_staff` - Xem YCMS, cập nhật delivery status

### Indexes

- `idx_users_email` - UNIQUE index trên email
- `idx_users_user_type` - Index trên user_type
- `idx_users_role` - Index trên role
- `idx_users_supplier_id` - Index trên supplier_id
- `idx_users_is_active` - Partial index cho active users
- `idx_users_type_role` - Composite index

### Triggers

- `trigger_users_updated_at` - Auto update `updated_at` khi record thay đổi

---

## 👥 SAMPLE DATA

Script tự động tạo 3 sample users để test:

### 1. Super Admin
```
Email: admin@aladdin.com
Password: Admin@123
Type: aladdin
Role: super_admin
```

### 2. Aladdin Admin
```
Email: manager@aladdin.com
Password: Admin@123
Type: aladdin
Role: aladdin_admin
```

### 3. Aladdin Staff
```
Email: staff@aladdin.com
Password: Admin@123
Type: aladdin
Role: aladdin_staff
```

⚠️ **Lưu ý**: Đổi password trong production!

---

## 🔍 VERIFICATION

Sau khi chạy script, verify bằng các query:

### 1. Kiểm tra bảng đã tạo

```sql
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;
```

### 2. Kiểm tra indexes

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';
```

### 3. Kiểm tra sample users

```sql
SELECT 
    id,
    email,
    user_type,
    role,
    is_active
FROM users;
```

### 4. Count users by type and role

```sql
SELECT 
    user_type,
    role,
    COUNT(*) as total
FROM users
GROUP BY user_type, role;
```

---

## ⚠️ CẢNH BÁO

### Script này sẽ:
- ✅ DROP existing `users` table (nếu có)
- ✅ DROP existing enums: `user_type_enum`, `user_role_enum`
- ✅ XÓA TẤT CẢ DỮ LIỆU CŨ

### Trước khi chạy trong Production:
- 🔴 Backup database
- 🔴 Test trên staging environment trước
- 🔴 Đổi sample passwords
- 🔴 Remove sample users nếu không cần

---

## 🐛 TROUBLESHOOTING

### Lỗi: psql not found

**Solution:**
1. Install PostgreSQL client
2. Add to PATH: `C:\Program Files\PostgreSQL\16\bin`
3. Restart PowerShell

### Lỗi: Connection refused

**Solution:**
1. Check PostgreSQL service đang chạy
2. Check host, port, username, password
3. Check pg_hba.conf cho phép connection

### Lỗi: Permission denied

**Solution:**
1. User cần quyền CREATE TABLE
2. Grant permissions:
```sql
GRANT ALL PRIVILEGES ON DATABASE portal TO portal;
```

### Lỗi: Database does not exist

**Solution:**
```sql
-- Connect to postgres database
psql -U postgres

-- Create database
CREATE DATABASE portal;

-- Create user
CREATE USER portal WITH PASSWORD 'portal';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE portal TO portal;
```

---

## 📚 REFERENCES

- [FastAPI-Users Documentation](https://fastapi-users.github.io/fastapi-users/)
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- Project Docs: `specification/description/ENTITY_SPECIFICATION.md`

---

## 📝 NOTES

- Script tương thích với SQLAlchemy models trong `app/models/user.py`
- Password hash format: Bcrypt (`$2b$12$...`)
- Timezone-aware timestamps (WITH TIME ZONE)
- Auto-update trigger cho `updated_at`
- Email validation regex trong constraint
- Phone validation regex trong constraint

---

**Last Updated**: 2025-10-09  
**Version**: 1.0  
**Status**: ✅ Ready to use
