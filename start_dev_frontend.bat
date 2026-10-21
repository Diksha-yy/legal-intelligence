@echo off
title Legal Intelligence AI - Vite Frontend Dev
cd /d "%~dp0frontend"

echo =====================================================================
echo        LEGAL INTELLIGENCE AI - VITE FRONTEND (HOT RELOAD)
echo =====================================================================
echo.
echo Starting Vite dev server on http://localhost:5173/ ...
echo (Ensure backend server is running on http://localhost:8000/)
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:5173/"

npm run dev
pause
