#!/usr/bin/env python3
"""
測試執行器
一鍵執行所有測試腳本
"""
import os
import sys
import subprocess
from pathlib import Path

def run_test(script_name, description):
    """執行單個測試腳本"""
    print(f"\n{'='*60}")
    print(f"🧪 執行測試: {description}")
    print(f"📄 腳本: {script_name}")
    print(f"{'='*60}")
    
    try:
        # 切換到test目錄執行
        script_path = Path(__file__).parent / script_name
        result = subprocess.run(
            [sys.executable, str(script_path)], 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        
        print(result.stdout)
        if result.stderr:
            print("⚠️ 錯誤輸出:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ 測試通過")
        else:
            print("❌ 測試失敗")
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 執行失敗: {e}")
        return False

def main():
    """主執行函數"""
    print("🚀 線上測驗系統 - 測試執行器")
    print("=" * 60)
    
    # 檢查是否在正確的目錄中
    if not Path("system_check.py").exists():
        print("❌ 請在 test 目錄中執行此腳本")
        return 1
    
    # 定義測試腳本列表
    tests = [
        ("check_multiple_choice.py", "多選題檢查"),
        ("system_check.py", "系統全面檢查"),
    ]
    
    passed = 0
    failed = 0
    
    # 執行每個測試
    for script, description in tests:
        if Path(script).exists():
            if run_test(script, description):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠️ 跳過 {script} (檔案不存在)")
    
    # 顯示測試結果摘要
    print(f"\n{'='*60}")
    print("📊 測試結果摘要")
    print(f"{'='*60}")
    print(f"✅ 通過: {passed}")
    print(f"❌ 失敗: {failed}")
    print(f"📝 總計: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 所有測試都通過了！")
        return 0
    else:
        print(f"\n⚠️ 有 {failed} 個測試失敗，請檢查輸出信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
