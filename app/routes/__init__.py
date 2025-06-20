"""
路由初始化文件
導出所有藍圖
"""
from .main import main_bp
from .quiz import quiz_bp
from .admin import admin_bp
from .api import api_bp

__all__ = ['main_bp', 'quiz_bp', 'admin_bp', 'api_bp']
