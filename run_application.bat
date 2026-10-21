@echo off
title Legal Intelligence AI
cd /d "%~dp0"

echo =====================================================================
echo                LEGAL INTELLIGENCE AI - LAUNCHER
echo =====================================================================
echo.
echo Checking Python virtual environment...
if not exist ".venv\Scripts\python.exe" (
    echo Error: Python virtual environment (.venv) not found in %CD%
    pause
    exit /b 1
)

echo.
echo Clearing any previous process occupying port 8000...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }" >nul 2>&1

echo.
echo Starting unified server (FastAPI + React SPA Frontend)...
echo Website URL: http://localhost:8000/
echo Swagger API: http://localhost:8000/docs
echo.

:: Automatically open browser after 2 seconds
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8000/"

:: Start server
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
