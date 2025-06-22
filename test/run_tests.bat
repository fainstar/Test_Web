@echo off
echo 🚀 線上測驗系統 - 測試執行器 (Windows)
echo ======================================

cd /d "%~dp0"

echo.
echo 📋 執行測試清單:
echo   1. 多選題檢查
echo   2. 系統全面檢查
echo.

python run_all_tests.py

echo.
echo 📝 測試完成，按任意鍵關閉視窗...
pause >nul
