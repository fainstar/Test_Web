"""
配置文件模組
包含應用程式的所有配置設定
"""
import os
from datetime import timedelta
from pathlib import Path

class Config:
    """基礎配置類"""
    
    # Flask基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
      # 數據庫配置
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'quiz_database.db'
    
    @classmethod
    def init_app(cls, app):
        """初始化應用程式配置"""
        # 確保數據庫目錄存在
        db_path = Path(cls.DATABASE_PATH)
        if db_path.parent != Path('.'):
            try:
                db_path.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                # 如果權限不足，嘗試記錄錯誤但不停止應用
                print(f"Warning: Cannot create directory {db_path.parent}, using current directory")
                # 回退到當前目錄
                cls.DATABASE_PATH = db_path.name
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False  # 開發環境設為False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 測驗配置
    DEFAULT_QUESTION_COUNT = 10
    MIN_QUESTION_COUNT = 1
    MAX_QUESTION_COUNT = 50
    
    # 文件上傳配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'json', 'txt'}
    
    # 分頁配置
    QUESTIONS_PER_PAGE = 20
    
    # 快取配置
    CACHE_TIMEOUT = 300  # 5分鐘

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    TESTING = False
    
    # 開發環境數據庫
    DATABASE_PATH = 'dev_quiz_database.db'

class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    TESTING = False
    
    # 安全配置
    SESSION_COOKIE_SECURE = True
    
    # 生產環境數據庫
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or '/app/volumes/database/quiz_database.db'

class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    DEBUG = True
    
    # 測試數據庫
    DATABASE_PATH = ':memory:'  # 使用內存數據庫

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """獲取當前配置"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, DevelopmentConfig)
