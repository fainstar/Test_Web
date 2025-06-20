"""
應用程式入口點
啟動Flask應用程式
"""
import os
from app import create_app

# 創建應用程式實例
app = create_app()

if __name__ == '__main__':
    # 從環境變數獲取配置，Docker友好設定
    debug_mode = os.environ.get('FLASK_DEBUG', os.environ.get('FLASK_ENV', 'production') == 'development').lower() == 'true'
    port = int(os.environ.get('PORT', os.environ.get('APP_PORT', 5000)))
    host = os.environ.get('HOST', os.environ.get('APP_HOST', '0.0.0.0'))  # Docker中監聽所有介面
    
    print(f"🚀 啟動線上測驗系統...")
    print(f"📍 訪問地址: http://{host}:{port}")
    print(f"🔧 除錯模式: {'開啟' if debug_mode else '關閉'}")
    print(f"📊 管理面板: http://{host}:{port}/admin")
    print(f"🔌 API文檔: http://{host}:{port}/api")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        threaded=True
    )
