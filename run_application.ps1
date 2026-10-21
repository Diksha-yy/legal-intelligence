# Legal Intelligence AI — PowerShell One-Click Launcher
Set-Location -Path $PSScriptRoot

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "                LEGAL INTELLIGENCE AI - LAUNCHER" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Free port 8000 if occupied
$existing = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Clearing previous process occupying port 8000..." -ForegroundColor Yellow
    $existing | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 1
}

Write-Host "Unified Server (FastAPI + React Production Frontend): http://localhost:8000/" -ForegroundColor Green
Write-Host "Interactive API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""

# Open default browser
Start-Process "http://localhost:8000/"

# Launch uvicorn
& "$PSScriptRoot\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
