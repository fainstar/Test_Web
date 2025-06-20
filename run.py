"""
應用程式入口點
啟動Flask應用程式
"""
import os
from app import create_app

# 創建應用程式實例
app = create_app()

if __name__ == '__main__':
    # 開發環境設定
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
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
