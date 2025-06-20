@echo off
REM Docker部署腳本 - Windows版本

echo 🚀 線上測驗系統 Docker 部署腳本
echo ================================

REM 檢查Docker是否安裝
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未安裝，請先安裝Docker Desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose未安裝，請先安裝Docker Compose
    pause
    exit /b 1
)

REM 創建必要的目錄
echo 📁 創建必要的目錄...
if not exist volumes mkdir volumes
if not exist volumes\database mkdir volumes\database
if not exist volumes\logs mkdir volumes\logs
if not exist volumes\uploads mkdir volumes\uploads
if not exist nginx\ssl mkdir nginx\ssl

REM 設置環境變數
if not exist .env (
    echo 📝 創建環境變數文件...
    copy .env.docker.example .env
    echo ⚠️  請編輯 .env 文件並設置正確的環境變數
)

REM 構建和啟動服務
echo 🔨 構建Docker映像...
docker-compose build

echo 🚀 啟動服務...
docker-compose up -d

REM 等待服務啟動
echo ⏳ 等待服務啟動...
timeout /t 10 /nobreak >nul

REM 檢查服務狀態
echo 🔍 檢查服務狀態...
docker-compose ps

REM 顯示訪問信息
echo.
echo ✅ 部署完成！
echo 📍 訪問地址: http://localhost:5000
echo 📊 管理面板: http://localhost:5000/admin
echo 🔌 API文檔: http://localhost:5000/api
echo.
echo 📝 查看日誌: docker-compose logs -f
echo 🛑 停止服務: docker-compose down
echo.

REM 可選：啟動帶Nginx的配置
set /p choice=🤔 是否要啟動Nginx反向代理？(y/n): 
if /i "%choice%"=="y" (
    echo 🌐 啟動Nginx...
    docker-compose --profile with-nginx up -d nginx
    echo ✅ Nginx已啟動，HTTP訪問地址: http://localhost
)

echo.
echo 按任意鍵退出...
pause >nul
