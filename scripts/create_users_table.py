"""
Python script to create users table in PostgreSQL
Usage: python scripts/create_users_table.py
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncpg


async def create_users_table():
    """Create users table with all enums, indexes, and sample data."""
    
    # Database connection parameters
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "portal"
    DB_USER = "portal"
    DB_PASSWORD = "portal"
    
    print("=" * 60)
    print("  Creating Users Table in PostgreSQL")
    print("=" * 60)
    print()
    print(f"📋 Configuration:")
    print(f"   Host: {DB_HOST}")
    print(f"   Port: {DB_PORT}")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print()
    
    try:
        # Connect to database
        print("🔌 Connecting to database...")
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("   ✅ Connected successfully")
        print()
        
        # Read SQL script
        sql_file = Path(__file__).parent / "create_users_table_clean.sql"
        print(f"📖 Reading SQL script: {sql_file.name}")
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        print("   ✅ Script loaded")
        print()
        
        # Execute SQL script
        print("🚀 Executing SQL script...")
        print("   - Dropping existing tables and enums...")
        print("   - Creating enums (user_type_enum, user_role_enum)...")
        print("   - Creating users table...")
        print("   - Creating indexes...")
        print("   - Creating triggers...")
        print("   - Inserting sample data...")
        print()
        
        # Split and execute statements
        await conn.execute(sql_script)
        
        print("=" * 60)
        print("  ✅ SUCCESS!")
        print("=" * 60)
        print()
        print("✅ Users table created successfully!")
        print()
        print("📊 Sample users inserted:")
        print("   1. admin@aladdin.com (super_admin)")
        print("   2. manager@aladdin.com (aladdin_admin)")
        print("   3. staff@aladdin.com (aladdin_staff)")
        print()
        print("🔑 Default password: Admin@123")
        print("⚠️  Remember to change passwords in production!")
        print()
        
        # Verify by counting users
        count = await conn.fetchval("SELECT COUNT(*) FROM users")
        print(f"📈 Total users in database: {count}")
        print()
        
        # List all users
        users = await conn.fetch("""
            SELECT id, email, user_type, role, first_name, last_name
            FROM users
            ORDER BY id
        """)
        
        print("👥 Users list:")
        for user in users:
            print(f"   {user['id']}. {user['email']:30} | {user['user_type']:10} | {user['role']:15} | {user['first_name']} {user['last_name']}")
        print()
        
        # Close connection
        await conn.close()
        print("=" * 60)
        print("  Script completed successfully!")
        print("=" * 60)
        
        return True
        
    except FileNotFoundError:
        print("❌ Error: SQL script file not found")
        print(f"   Please ensure 'create_users_table.sql' exists in {Path(__file__).parent}")
        return False
        
    except asyncpg.PostgresError as e:
        print(f"❌ Database Error: {e}")
        print()
        print("Common issues:")
        print("  - Check if PostgreSQL is running")
        print("  - Verify connection parameters (host, port, user, password)")
        print("  - Ensure user has CREATE TABLE permissions")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


async def verify_users_table():
    """Verify that users table was created correctly."""
    
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "portal"
    DB_USER = "portal"
    DB_PASSWORD = "portal"
    
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        print("\n🔍 Running verification...")
        print()
        
        # Check table exists
        exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            )
        """)
        
        if exists:
            print("✅ Users table exists")
            
            # Count columns
            columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'users'
                ORDER BY ordinal_position
            """)
            print(f"✅ Table has {len(columns)} columns")
            
            # Count indexes
            indexes = await conn.fetch("""
                SELECT COUNT(*) as count
                FROM pg_indexes
                WHERE tablename = 'users'
            """)
            print(f"✅ Table has {indexes[0]['count']} indexes")
            
            # Check enums
            user_types = await conn.fetch("""
                SELECT enumlabel
                FROM pg_enum
                JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
                WHERE pg_type.typname = 'user_type_enum'
            """)
            print(f"✅ user_type_enum has {len(user_types)} values: {', '.join(row['enumlabel'] for row in user_types)}")
            
            user_roles = await conn.fetch("""
                SELECT enumlabel
                FROM pg_enum
                JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
                WHERE pg_type.typname = 'user_role_enum'
            """)
            print(f"✅ user_role_enum has {len(user_roles)} values")
            
            print()
            print("✅ All verifications passed!")
            
        else:
            print("❌ Users table does not exist")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")


if __name__ == "__main__":
    print()
    success = asyncio.run(create_users_table())
    
    if success:
        asyncio.run(verify_users_table())
        sys.exit(0)
    else:
        sys.exit(1)
