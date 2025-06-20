# Docker 部署指南

## 🐳 Docker 容器化部署

線上測驗系統已完全支援Docker容器化部署，提供簡單、可靠的部署方案。

## 📋 前置需求

- Docker Engine 20.10+
- Docker Compose 2.0+
- 最少 1GB RAM
- 最少 2GB 磁碟空間

## 🚀 快速啟動

### 方法一：使用部署腳本（推薦）

**Windows:**
```cmd
# 開發環境
deploy.bat dev

# 生產環境（包含Nginx）
deploy.bat prod
```

**Linux/macOS:**
```bash
# 給予執行權限
chmod +x deploy.sh

# 開發環境
./deploy.sh dev

# 生產環境（包含Nginx）  
./deploy.sh prod
```

### 方法二：手動Docker Compose

```bash
# 開發環境（僅應用程式）
docker-compose up -d

# 生產環境（包含Nginx反向代理）
docker-compose --profile with-nginx up -d

# 建構並啟動
docker-compose up --build -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

## 🔧 環境配置

### 環境變數

複製 `.env.docker` 為 `.env` 並修改配置：

```bash
cp .env.docker .env
```

主要配置項：
- `SECRET_KEY`: Flask密鑰（生產環境務必更改）
- `FLASK_ENV`: 環境模式（development/production）
- `DATABASE_PATH`: 資料庫檔案路徑
- `APP_HOST`: 監聽地址（Docker中為0.0.0.0）
- `APP_PORT`: 監聽端口

### 資料持久化

系統使用Docker卷來持久化數據：
- `quiz_data`: 資料庫檔案和用戶數據
- `quiz_base`: 題庫檔案

## 🌐 訪問地址

### 開發環境
- **應用程式**: http://localhost:5000
- **管理面板**: http://localhost:5000/admin
- **API文檔**: http://localhost:5000/api

### 生產環境（含Nginx）
- **應用程式**: http://localhost
- **管理面板**: http://localhost/admin
- **API文檔**: http://localhost/api

## 📊 監控和維護

### 查看容器狀態
```bash
docker-compose ps
```

### 查看日誌
```bash
# 所有服務日誌
docker-compose logs -f

# 特定服務日誌
docker-compose logs -f quiz-app
docker-compose logs -f nginx
```

### 進入容器
```bash
# 進入應用容器
docker-compose exec quiz-app bash

# 進入資料庫初始化
docker-compose exec quiz-app python init_db.py
```

### 備份資料
```bash
# 備份資料庫
docker-compose exec quiz-app cp /app/data/quiz_database.db /tmp/
docker cp $(docker-compose ps -q quiz-app):/tmp/quiz_database.db ./backup_$(date +%Y%m%d).db
```

### 更新應用
```bash
# 停止服務
docker-compose down

# 拉取最新代碼
git pull

# 重新建構並啟動
docker-compose up --build -d
```

## 🔒 安全配置

### 生產環境安全檢查清單

- [ ] 更改預設的 `SECRET_KEY`
- [ ] 設定 `FLASK_ENV=production`
- [ ] 配置適當的 `ALLOWED_HOSTS`
- [ ] 啟用HTTPS（如果需要）
- [ ] 設定防火牆規則
- [ ] 定期備份資料庫
- [ ] 監控容器資源使用

### HTTPS配置（可選）

如需HTTPS，請：
1. 將SSL證書放在 `./ssl/` 目錄
2. 取消註解 `nginx.conf` 中的HTTPS配置
3. 修改 `server_name` 為你的域名

## 🐛 故障排除

### 常見問題

**Q: 容器啟動失敗**
```bash
# 檢查日誌
docker-compose logs quiz-app

# 檢查資源使用
docker stats

# 清理並重新啟動
docker-compose down
docker system prune -f
docker-compose up --build -d
```

**Q: 無法訪問應用程式**
```bash
# 檢查端口是否被占用
netstat -tulpn | grep :5000

# 檢查容器網路
docker network ls
docker network inspect online-quiz-system_quiz_network
```

**Q: 資料庫初始化失敗**
```bash
# 手動初始化
docker-compose exec quiz-app python init_db.py

# 檢查資料庫檔案權限
docker-compose exec quiz-app ls -la /app/data/
```

**Q: 題目導入失敗**
```bash
# 檢查題庫檔案
docker-compose exec quiz-app ls -la /app/base/

# 手動導入
docker-compose exec quiz-app python -c "
from app import create_app
from app.services.question_service import QuestionService
app = create_app()
with app.app_context():
    service = QuestionService()
    # 執行導入邏輯
"
```

## 📈 性能優化

### 資源限制
在 `docker-compose.yml` 中添加資源限制：

```yaml
services:
  quiz-app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

### 健康檢查
系統已內建健康檢查，會自動重啟不健康的容器。

### 日誌輪轉
建議配置日誌輪轉避免日誌檔案過大：

```yaml
services:
  quiz-app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🌍 多環境部署

### 開發環境
- 啟用除錯模式
- 即時代碼重載
- 詳細錯誤訊息

### 測試環境
- 生產模式配置
- 測試數據初始化
- 性能監控

### 生產環境
- Nginx反向代理
- SSL/TLS加密
- 性能優化
- 日誌記錄
- 監控告警

## 📞 技術支援

如有Docker部署相關問題，請：
1. 檢查日誌輸出
2. 確認環境配置
3. 查閱故障排除章節
4. 提交詳細的錯誤報告
