"""
裝飾器工具
提供常用的裝飾器功能
"""
from functools import wraps
from flask import current_app

def ensure_services(f):
    """
    確保服務已初始化的裝飾器
    在路由函數執行前自動初始化服務
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 在應用程式上下文中初始化服務
        if hasattr(current_app, '_services_initialized'):
            return f(*args, **kwargs)
        
        # 標記服務已初始化
        current_app._services_initialized = True
        return f(*args, **kwargs)
    
    return decorated_function
