@echo off
REM 線上測驗系統 Docker 部署腳本 (Windows版本)
REM 使用方法: deploy.bat [dev|prod]

setlocal EnableDelayedExpansion

set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=dev
set PROJECT_NAME=online-quiz-system

echo 🚀 開始部署線上測驗系統 - 環境: %ENVIRONMENT%

REM 檢查Docker是否安裝
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Docker未安裝
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: Docker Compose未安裝
    exit /b 1
)

REM 停止現有容器
echo 🛑 停止現有容器...
docker-compose -p %PROJECT_NAME% down 2>nul || echo 沒有運行中的容器

REM 詢問是否清理舊映像
set /p CLEANUP="是否清理舊的Docker映像? (y/N): "
if /i "%CLEANUP%"=="y" (
    echo 🧹 清理舊映像...
    docker image prune -f
    docker system prune -f
)

REM 建構映像
echo 🔨 建構Docker映像...
docker-compose -p %PROJECT_NAME% build

REM 根據環境啟動服務
if "%ENVIRONMENT%"=="prod" (
    echo 🌐 啟動生產環境 (包含Nginx)...
    docker-compose -p %PROJECT_NAME% --profile with-nginx up -d
) else (
    echo 🔧 啟動開發環境...
    docker-compose -p %PROJECT_NAME% up -d
)

REM 等待服務啟動
echo ⏳ 等待服務啟動...
timeout /t 10 /nobreak >nul

REM 檢查服務狀態
echo 📊 檢查服務狀態...
docker-compose -p %PROJECT_NAME% ps

echo ✅ 部署完成!
if "%ENVIRONMENT%"=="prod" (
    echo 🌐 應用程式地址: http://localhost
    echo 📊 管理面板: http://localhost/admin
) else (
    echo 🌐 應用程式地址: http://localhost:5000
    echo 📊 管理面板: http://localhost:5000/admin
)

echo.
echo 💡 使用以下命令查看日誌:
echo docker-compose -p %PROJECT_NAME% logs -f

pause
