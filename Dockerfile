# 使用Python 3.11官方基礎映像
FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    DEBIAN_FRONTEND=noninteractive

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 複製requirements.txt並安裝Python依賴
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 創建非root用戶
RUN adduser --disabled-password --gecos '' appuser

# 複製應用程式代碼
COPY . .

# 創建必要的目錄並設置權限
RUN mkdir -p /app/volumes/database /app/volumes/logs /app/static/uploads && \
    chown -R appuser:appuser /app

# 切換到非root用戶
USER appuser

# 初始化資料庫（如果不存在）
RUN python init_db.py || echo "Database initialization completed or skipped"

# 暴露端口
EXPOSE 5000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/api || exit 1

# 啟動命令 - 使用gunicorn生產環境服務器
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--keep-alive", "5", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
