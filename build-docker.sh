#!/bin/bash
# Docker構建和推送腳本

# 設置變數
IMAGE_NAME="oomaybeoo/test-web"
VERSION="v2.1.0"

echo "🐳 Docker構建腳本"
echo "=================="

# 檢查Docker是否運行
if ! docker info &> /dev/null; then
    echo "❌ Docker未運行，請啟動Docker Desktop"
    exit 1
fi

echo "🔨 構建Docker映像..."
docker build -t ${IMAGE_NAME}:${VERSION} -t ${IMAGE_NAME}:latest .

if [ $? -eq 0 ]; then
    echo "✅ 構建成功！"
    
    # 顯示映像大小
    echo "📦 映像信息:"
    docker images ${IMAGE_NAME}
    
    # 詢問是否推送到Docker Hub
    read -p "🤔 是否要推送映像到Docker Hub？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 推送映像到Docker Hub..."
        docker push ${IMAGE_NAME}:${VERSION}
        docker push ${IMAGE_NAME}:latest
        echo "✅ 推送完成！"
        echo "📍 映像地址: ${IMAGE_NAME}:${VERSION}"
    fi
    
    # 詢問是否本地測試
    read -p "🤔 是否要本地測試映像？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🧪 啟動本地測試..."
        docker run -d --name test-quiz-system -p 5000:5000 ${IMAGE_NAME}:latest
        echo "✅ 測試容器已啟動！"
        echo "📍 測試地址: http://localhost:5000"
        echo "🛑 停止測試: docker stop test-quiz-system && docker rm test-quiz-system"
    fi
    
else
    echo "❌ 構建失敗！"
    exit 1
fi
