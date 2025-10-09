-- =====================================================
-- CREATE USERS TABLE FOR YCMS (Clean version for Python)
-- Database: portal
-- Description: Bảng user với FastAPI-Users integration
-- Version: 1.0
-- Created: 2025-10-09
-- =====================================================

-- Drop existing types if exists (for clean recreation)
DROP TYPE IF EXISTS user_type_enum CASCADE;
DROP TYPE IF EXISTS user_role_enum CASCADE;

-- Drop table if exists
DROP TABLE IF EXISTS users CASCADE;

-- =====================================================
-- CREATE ENUMS
-- =====================================================

-- User Type Enum
CREATE TYPE user_type_enum AS ENUM (
    'aladdin',
    'supplier'
);

-- User Role Enum
CREATE TYPE user_role_enum AS ENUM (
    'super_admin',
    'aladdin_admin',
    'aladdin_staff',
    'supplier_admin',
    'supplier_staff'
);

-- =====================================================
-- CREATE USERS TABLE
-- =====================================================

CREATE TABLE users (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- FastAPI-Users required fields
    email VARCHAR(320) NOT NULL UNIQUE,
    hashed_password VARCHAR(1024) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- YCMS-specific fields
    user_type user_type_enum NOT NULL,
    role user_role_enum NOT NULL,
    
    -- Personal Information
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    avatar_url VARCHAR(500),
    
    -- Supplier relationship
    supplier_id INTEGER,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT users_email_check CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    CONSTRAINT users_phone_check CHECK (phone_number IS NULL OR phone_number ~* '^\+?[0-9]{9,15}$')
);

-- =====================================================
-- CREATE INDEXES
-- =====================================================

CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_user_type ON users(user_type);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_supplier_id ON users(supplier_id) WHERE supplier_id IS NOT NULL;
CREATE INDEX idx_users_is_active ON users(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_users_type_role ON users(user_type, role);

-- =====================================================
-- CREATE TRIGGER FOR UPDATED_AT
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ADD COMMENTS
-- =====================================================

COMMENT ON TABLE users IS 'Bảng user hệ thống với FastAPI-Users integration';
COMMENT ON COLUMN users.id IS 'Primary key, auto-increment';
COMMENT ON COLUMN users.email IS 'Email đăng nhập (unique)';
COMMENT ON COLUMN users.hashed_password IS 'Password đã hash với Bcrypt';
COMMENT ON COLUMN users.is_active IS 'Trạng thái kích hoạt tài khoản';
COMMENT ON COLUMN users.is_superuser IS 'Superuser flag (full access)';
COMMENT ON COLUMN users.is_verified IS 'Email đã được xác thực';
COMMENT ON COLUMN users.user_type IS 'Loại user: aladdin hoặc supplier';
COMMENT ON COLUMN users.role IS 'Role của user';
COMMENT ON COLUMN users.first_name IS 'Tên';
COMMENT ON COLUMN users.last_name IS 'Họ';
COMMENT ON COLUMN users.phone_number IS 'Số điện thoại liên hệ';
COMMENT ON COLUMN users.avatar_url IS 'URL ảnh đại diện';
COMMENT ON COLUMN users.supplier_id IS 'Foreign key tới bảng suppliers';
COMMENT ON COLUMN users.created_at IS 'Thời điểm tạo tài khoản';
COMMENT ON COLUMN users.updated_at IS 'Thời điểm cập nhật cuối cùng';
COMMENT ON COLUMN users.last_login IS 'Thời điểm đăng nhập cuối cùng';

-- =====================================================
-- INSERT SAMPLE DATA
-- =====================================================

INSERT INTO users (
    email,
    hashed_password,
    is_active,
    is_superuser,
    is_verified,
    user_type,
    role,
    first_name,
    last_name,
    phone_number
) VALUES 
(
    'admin@aladdin.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5uXN9rnwQvBZO',
    TRUE,
    TRUE,
    TRUE,
    'aladdin',
    'super_admin',
    'Admin',
    'System',
    '+84901234567'
),
(
    'manager@aladdin.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5uXN9rnwQvBZO',
    TRUE,
    FALSE,
    TRUE,
    'aladdin',
    'aladdin_admin',
    'Nguyen',
    'Manager',
    '+84912345678'
),
(
    'staff@aladdin.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5uXN9rnwQvBZO',
    TRUE,
    FALSE,
    TRUE,
    'aladdin',
    'aladdin_staff',
    'Tran',
    'Staff',
    '+84923456789'
);

-- =====================================================
-- GRANT PERMISSIONS
-- =====================================================

GRANT SELECT, INSERT, UPDATE, DELETE ON users TO portal;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO portal;
