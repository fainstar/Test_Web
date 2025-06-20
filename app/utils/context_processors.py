"""
上下文處理器
提供模板全局變量和函數
"""
from datetime import datetime

def register_context_processors(app):
    """註冊上下文處理器"""
    
    @app.context_processor
    def inject_globals():
        """注入全局變量到模板"""
        return {
            'current_year': datetime.now().year,
            'app_name': '線上測驗系統',
            'app_version': '2.0.0'
        }
    
    @app.template_filter('datetime_format')
    def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
        """日期時間格式化過濾器"""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except:
                return value
        return value.strftime(format)
    
    @app.template_filter('percentage')
    def percentage_format(value, decimals=1):
        """百分比格式化過濾器"""
        try:
            return f"{float(value):.{decimals}f}%"
        except:
            return "0.0%"
    
    @app.template_filter('duration')
    def duration_format(minutes):
        """持續時間格式化過濾器"""
        try:
            minutes = float(minutes)
            if minutes < 1:
                return f"{int(minutes * 60)}秒"
            elif minutes < 60:
                return f"{minutes:.1f}分鐘"
            else:
                hours = int(minutes // 60)
                mins = int(minutes % 60)
                return f"{hours}小時{mins}分鐘"
        except:
            return "0分鐘"
