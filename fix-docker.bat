@echo off
REM Docker問題修復腳本

echo 🔧 Docker問題修復腳本
echo ====================

echo 1. 清理Docker緩存...
docker builder prune -f
docker system prune -f

echo 2. 檢查requirements.txt...
findstr "sqlite3" requirements.txt >nul
if not errorlevel 1 (
    echo ❌ 發現sqlite3在requirements.txt中，正在移除...
    powershell -Command "(Get-Content requirements.txt) | Where-Object {$_ -notmatch 'sqlite3'} | Set-Content requirements.txt"
    echo ✅ 已移除sqlite3
)

echo 3. 檢查Docker是否運行...
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未運行，請啟動Docker Desktop
    pause
    exit /b 1
) else (
    echo ✅ Docker運行正常
)

echo 4. 重新構建映像...
docker build -t oomaybeoo/test-web .

if %errorlevel% equ 0 (
    echo ✅ 構建成功！
    echo 📍 可以使用以下命令測試:
    echo docker run -d -p 5000:5000 oomaybeoo/test-web:latest
) else (
    echo ❌ 構建失敗，請檢查錯誤信息
)

pause
