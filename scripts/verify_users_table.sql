-- =====================================================
-- VERIFY USERS TABLE
-- Quick verification script
-- =====================================================

\echo '========================================='
\echo '  Verifying Users Table'
\echo '========================================='
\echo ''

-- 1. Check table exists
\echo '1. Checking if users table exists...'
SELECT 
    CASE 
        WHEN EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'users'
        ) 
        THEN '✅ Table exists'
        ELSE '❌ Table NOT found'
    END as status;
\echo ''

-- 2. Check columns
\echo '2. Table structure:'
SELECT 
    column_name as "Column",
    data_type as "Type",
    CASE WHEN is_nullable = 'NO' THEN 'NOT NULL' ELSE 'NULL' END as "Nullable",
    column_default as "Default"
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;
\echo ''

-- 3. Check indexes
\echo '3. Indexes:'
SELECT 
    indexname as "Index Name",
    indexdef as "Definition"
FROM pg_indexes
WHERE tablename = 'users';
\echo ''

-- 4. Check enums
\echo '4. User Type Enum values:'
SELECT 
    enumlabel as "Value"
FROM pg_enum
JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
WHERE pg_type.typname = 'user_type_enum'
ORDER BY enumsortorder;
\echo ''

\echo '5. User Role Enum values:'
SELECT 
    enumlabel as "Value"
FROM pg_enum
JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
WHERE pg_type.typname = 'user_role_enum'
ORDER BY enumsortorder;
\echo ''

-- 5. Count users
\echo '6. User statistics:'
SELECT 
    user_type as "Type",
    role as "Role",
    COUNT(*) as "Count"
FROM users
GROUP BY user_type, role
ORDER BY user_type, role;
\echo ''

-- 6. List all users
\echo '7. All users:'
SELECT 
    id as "ID",
    email as "Email",
    user_type as "Type",
    role as "Role",
    first_name || ' ' || last_name as "Name",
    is_active as "Active",
    is_verified as "Verified",
    created_at as "Created"
FROM users
ORDER BY id;
\echo ''

\echo '========================================='
\echo '✅ Verification complete!'
\echo '========================================='
