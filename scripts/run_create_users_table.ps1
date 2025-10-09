# =====================================================
# POWERSHELL SCRIPT TO CREATE USERS TABLE
# =====================================================
# Description: Script để chạy create_users_table.sql
# Database: portal
# User: portal
# Password: portal
# =====================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Creating Users Table in PostgreSQL  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Database connection parameters
$DB_HOST = "localhost"
$DB_PORT = "5432"
$DB_NAME = "portal"
$DB_USER = "portal"
$DB_PASSWORD = "portal"
$SCRIPT_PATH = ".\scripts\create_users_table.sql"

# Set PostgreSQL password environment variable
$env:PGPASSWORD = $DB_PASSWORD

Write-Host "📋 Configuration:" -ForegroundColor Yellow
Write-Host "   Host: $DB_HOST" -ForegroundColor Gray
Write-Host "   Port: $DB_PORT" -ForegroundColor Gray
Write-Host "   Database: $DB_NAME" -ForegroundColor Gray
Write-Host "   User: $DB_USER" -ForegroundColor Gray
Write-Host "   Script: $SCRIPT_PATH" -ForegroundColor Gray
Write-Host ""

# Check if psql is available
Write-Host "🔍 Checking PostgreSQL client..." -ForegroundColor Yellow
try {
    $psqlVersion = psql --version 2>&1
    Write-Host "   ✅ Found: $psqlVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error: psql not found in PATH" -ForegroundColor Red
    Write-Host "   Please install PostgreSQL client or add to PATH" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if SQL file exists
Write-Host "🔍 Checking SQL script..." -ForegroundColor Yellow
if (-Not (Test-Path $SCRIPT_PATH)) {
    Write-Host "   ❌ Error: $SCRIPT_PATH not found" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Script found" -ForegroundColor Green
Write-Host ""

# Test database connection
Write-Host "🔍 Testing database connection..." -ForegroundColor Yellow
try {
    $testConnection = psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Connection successful" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Connection failed" -ForegroundColor Red
        Write-Host "   Error: $testConnection" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   ❌ Connection failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Ask for confirmation
Write-Host "⚠️  WARNING: This will DROP and RECREATE the users table!" -ForegroundColor Red
Write-Host "⚠️  All existing user data will be lost!" -ForegroundColor Red
Write-Host ""
$confirmation = Read-Host "Do you want to continue? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "❌ Operation cancelled by user" -ForegroundColor Yellow
    exit 0
}
Write-Host ""

# Execute SQL script
Write-Host "🚀 Executing SQL script..." -ForegroundColor Yellow
Write-Host "   Creating users table..." -ForegroundColor Gray

try {
    # Run the SQL script
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $SCRIPT_PATH
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  ✅ SUCCESS!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Users table created successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Sample users inserted:" -ForegroundColor Cyan
        Write-Host "   1. admin@aladdin.com (super_admin)" -ForegroundColor Gray
        Write-Host "   2. manager@aladdin.com (aladdin_admin)" -ForegroundColor Gray
        Write-Host "   3. staff@aladdin.com (aladdin_staff)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "🔑 Default password: Admin@123" -ForegroundColor Yellow
        Write-Host "⚠️  Remember to change passwords in production!" -ForegroundColor Red
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "❌ Failed to execute SQL script" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error executing SQL script" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# Clean up environment variable
Remove-Item Env:\PGPASSWORD

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Script completed successfully!  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
