-- =====================================================
-- ROLLBACK SCRIPT - Drop Users Table
-- =====================================================
-- Description: Script để xóa bảng users và các enums
-- CẢNH BÁO: Script này sẽ xóa toàn bộ dữ liệu users!
-- =====================================================

\echo '========================================='
\echo '⚠️  ROLLBACK: Dropping Users Table'
\echo '========================================='
\echo ''

-- Drop trigger first
\echo 'Dropping trigger...'
DROP TRIGGER IF EXISTS trigger_users_updated_at ON users;
\echo '✅ Trigger dropped'
\echo ''

-- Drop function
\echo 'Dropping function...'
DROP FUNCTION IF EXISTS update_updated_at_column();
\echo '✅ Function dropped'
\echo ''

-- Drop table
\echo 'Dropping users table...'
DROP TABLE IF EXISTS users CASCADE;
\echo '✅ Table dropped'
\echo ''

-- Drop enums
\echo 'Dropping enums...'
DROP TYPE IF EXISTS user_type_enum CASCADE;
DROP TYPE IF EXISTS user_role_enum CASCADE;
\echo '✅ Enums dropped'
\echo ''

-- Verify
\echo 'Verifying cleanup...'
SELECT 
    CASE 
        WHEN NOT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'users'
        ) 
        THEN '✅ Users table successfully removed'
        ELSE '❌ Table still exists'
    END as status;
\echo ''

\echo '========================================='
\echo '✅ Rollback complete!'
\echo '========================================='
\echo ''
\echo '⚠️  All user data has been deleted!'
\echo 'To recreate, run: create_users_table.sql'
