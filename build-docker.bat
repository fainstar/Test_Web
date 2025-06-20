@echo off
REM Docker構建和推送腳本 - Windows版本

REM 設置變數
set IMAGE_NAME=oomaybeoo/test-web
set VERSION=v2.1.0

echo 🐳 Docker構建腳本
echo ==================

REM 檢查Docker是否運行
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未運行，請啟動Docker Desktop
    pause
    exit /b 1
)

echo 🔨 構建Docker映像...
docker build -t %IMAGE_NAME%:%VERSION% -t %IMAGE_NAME%:latest .

if %errorlevel% equ 0 (
    echo ✅ 構建成功！
    
    REM 顯示映像大小
    echo 📦 映像信息:
    docker images %IMAGE_NAME%
    
    REM 詢問是否推送到Docker Hub
    set /p choice=🤔 是否要推送映像到Docker Hub？(y/n): 
    if /i "%choice%"=="y" (
        echo 🚀 推送映像到Docker Hub...
        docker push %IMAGE_NAME%:%VERSION%
        docker push %IMAGE_NAME%:latest
        echo ✅ 推送完成！
        echo 📍 映像地址: %IMAGE_NAME%:%VERSION%
    )
    
    REM 詢問是否本地測試
    set /p choice2=🤔 是否要本地測試映像？(y/n): 
    if /i "%choice2%"=="y" (
        echo 🧪 啟動本地測試...
        docker run -d --name test-quiz-system -p 5000:5000 %IMAGE_NAME%:latest
        echo ✅ 測試容器已啟動！
        echo 📍 測試地址: http://localhost:5000
        echo 🛑 停止測試: docker stop test-quiz-system ^&^& docker rm test-quiz-system
    )
    
) else (
    echo ❌ 構建失敗！
    pause
    exit /b 1
)

echo.
echo 按任意鍵退出...
pause >nul
