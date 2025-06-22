#!/usr/bin/env python3
"""
Docker 環境檢查腳本
檢查 Docker 容器中的權限和路徑設置
"""
import os
import sys
from pathlib import Path

def check_environment():
    """檢查環境設置"""
    print("=== Docker 環境檢查 ===")
    
    # 檢查環境變數
    print("\n1. 環境變數檢查:")
    flask_env = os.environ.get('FLASK_ENV', 'not set')
    database_path = os.environ.get('DATABASE_PATH', 'not set')
    print(f"   FLASK_ENV: {flask_env}")
    print(f"   DATABASE_PATH: {database_path}")
    
    # 檢查路徑權限
    print("\n2. 路徑權限檢查:")
    paths_to_check = [
        '/app',
        '/app/volumes',
        '/app/volumes/database',
        '/data'
    ]
    
    for path in paths_to_check:
        path_obj = Path(path)
        exists = path_obj.exists()
        writable = path_obj.is_dir() and os.access(path, os.W_OK) if exists else False
        print(f"   {path}: 存在={exists}, 可寫={writable}")
    
    # 測試創建目錄
    print("\n3. 目錄創建測試:")
    test_paths = [
        '/app/volumes/database/test',
        '/data/test'
    ]
    
    for test_path in test_paths:
        try:
            Path(test_path).mkdir(parents=True, exist_ok=True)
            Path(test_path).rmdir()  # 清理測試目錄
            print(f"   {test_path}: 創建成功 ✓")
        except Exception as e:
            print(f"   {test_path}: 創建失敗 ✗ ({e})")
    
    # 檢查用戶權限
    print("\n4. 用戶權限檢查:")
    print(f"   當前用戶: {os.getuid() if hasattr(os, 'getuid') else 'N/A'}")
    print(f"   當前工作目錄: {os.getcwd()}")
    print(f"   家目錄權限: {oct(os.stat(os.path.expanduser('~')).st_mode)[-3:] if os.path.exists(os.path.expanduser('~')) else 'N/A'}")

if __name__ == "__main__":
    check_environment()
