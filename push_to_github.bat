@echo off
title Push Legal Intelligence to GitHub
cd /d "%~dp0"

echo =====================================================================
echo                PUSH TO GITHUB (Diksha-yy/legal-intelligence)
echo =====================================================================
echo.
echo Please ensure you have created the empty repository on GitHub first:
echo https://github.com/new (Name: legal-intelligence)
echo.
echo Pushing commits, executables, AI modules, and evidence...
echo.

git push -u origin main

echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Your project has been pushed to GitHub successfully!
    echo View at: https://github.com/Diksha-yy/legal-intelligence
) else (
    echo [ERROR] Push failed. If the repository does not exist, create it at:
    echo https://github.com/new (Name: legal-intelligence)
)

echo.
pause
