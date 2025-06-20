#!/bin/bash
# Docker部署腳本

set -e

echo "🚀 線上測驗系統 Docker 部署腳本"
echo "================================"

# 檢查Docker是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安裝，請先安裝Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安裝，請先安裝Docker Compose"
    exit 1
fi

# 創建必要的目錄
echo "📁 創建必要的目錄..."
mkdir -p volumes/database
mkdir -p volumes/logs
mkdir -p volumes/uploads
mkdir -p nginx/ssl

# 設置環境變數
if [ ! -f .env ]; then
    echo "📝 創建環境變數文件..."
    cp .env.docker.example .env
    echo "⚠️  請編輯 .env 文件並設置正確的環境變數"
fi

# 構建和啟動服務
echo "🔨 構建Docker映像..."
docker-compose build

echo "🚀 啟動服務..."
docker-compose up -d

# 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 10

# 檢查服務狀態
echo "🔍 檢查服務狀態..."
docker-compose ps

# 顯示訪問信息
echo ""
echo "✅ 部署完成！"
echo "📍 訪問地址: http://localhost:5000"
echo "📊 管理面板: http://localhost:5000/admin"
echo "🔌 API文檔: http://localhost:5000/api"
echo ""
echo "📝 查看日誌: docker-compose logs -f"
echo "🛑 停止服務: docker-compose down"
echo ""

# 可選：啟動帶Nginx的配置
read -p "🤔 是否要啟動Nginx反向代理？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 啟動Nginx..."
    docker-compose --profile with-nginx up -d nginx
    echo "✅ Nginx已啟動，HTTP訪問地址: http://localhost"
fi
