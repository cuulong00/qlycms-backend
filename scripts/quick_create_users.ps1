# =====================================================
# QUICK RUN SCRIPT - Create Users Table
# =====================================================
# Usage: .\scripts\quick_create_users.ps1
# =====================================================

$env:PGPASSWORD = "portal"

Write-Host "🚀 Creating users table..." -ForegroundColor Cyan

psql -h localhost -p 5432 -U portal -d portal -f .\scripts\create_users_table.sql

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Success! Users table created." -ForegroundColor Green
    Write-Host "📧 Sample users:" -ForegroundColor Cyan
    Write-Host "   - admin@aladdin.com" -ForegroundColor Gray
    Write-Host "   - manager@aladdin.com" -ForegroundColor Gray
    Write-Host "   - staff@aladdin.com" -ForegroundColor Gray
    Write-Host "🔑 Password: Admin@123" -ForegroundColor Yellow
} else {
    Write-Host "❌ Failed!" -ForegroundColor Red
}

Remove-Item Env:\PGPASSWORD
