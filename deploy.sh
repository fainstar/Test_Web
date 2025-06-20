#!/bin/bash

# 線上測驗系統 Docker 部署腳本
# 使用方法: ./deploy.sh [dev|prod]

set -e

ENVIRONMENT=${1:-dev}
PROJECT_NAME="online-quiz-system"

echo "🚀 開始部署線上測驗系統 - 環境: $ENVIRONMENT"

# 檢查Docker是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ 錯誤: Docker未安裝"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 錯誤: Docker Compose未安裝"
    exit 1
fi

# 停止現有容器
echo "🛑 停止現有容器..."
docker-compose -p $PROJECT_NAME down 2>/dev/null || echo "沒有運行中的容器"

# 清理舊映像（可選）
read -p "是否清理舊的Docker映像? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 清理舊映像..."
    docker image prune -f
    docker system prune -f
fi

# 建構映像
echo "🔨 建構Docker映像..."
docker-compose -p $PROJECT_NAME build

# 根據環境啟動服務
if [ "$ENVIRONMENT" = "prod" ]; then
    echo "🌐 啟動生產環境 (包含Nginx)..."
    docker-compose -p $PROJECT_NAME --profile with-nginx up -d
else
    echo "🔧 啟動開發環境..."
    docker-compose -p $PROJECT_NAME up -d
fi

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 10

# 檢查服務狀態
echo "📊 檢查服務狀態..."
docker-compose -p $PROJECT_NAME ps

# 顯示日誌
echo "📝 顯示服務日誌 (Ctrl+C 退出)..."
docker-compose -p $PROJECT_NAME logs -f

echo "✅ 部署完成!"
if [ "$ENVIRONMENT" = "prod" ]; then
    echo "🌐 應用程式地址: http://localhost"
    echo "📊 管理面板: http://localhost/admin"
else
    echo "🌐 應用程式地址: http://localhost:5000"
    echo "📊 管理面板: http://localhost:5000/admin"
fi
