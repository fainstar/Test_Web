"""
應用程式工廠模組
使用工廠模式創建Flask應用程式實例
"""
from flask import Flask
from config.config import get_config
import os

def create_app(config_name=None):
    """
    應用程式工廠函數
    
    Args:
        config_name: 配置名稱 ('development', 'production', 'testing')
    
    Returns:
        Flask: 配置好的Flask應用程式實例    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # 載入配置
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # 註冊藍圖
    register_blueprints(app)
    
    # 初始化擴展
    init_extensions(app)
    
    # 註冊錯誤處理器
    register_error_handlers(app)
    
    # 註冊上下文處理器
    register_context_processors(app)
    
    return app

def register_blueprints(app):
    """註冊所有藍圖"""
    from app.routes.main import main_bp
    from app.routes.quiz import quiz_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

def init_extensions(app):
    """初始化Flask擴展"""
    # 這裡可以初始化其他擴展，如Flask-SQLAlchemy, Flask-Login等
    pass

def register_error_handlers(app):
    """註冊錯誤處理器"""
    from app.utils.error_handlers import register_error_handlers as reg_handlers
    reg_handlers(app)

def register_context_processors(app):
    """註冊上下文處理器"""
    from app.utils.context_processors import register_context_processors as reg_processors
    reg_processors(app)
