#!/usr/bin/env python3
"""
檢查並修復題目5的正確答案
"""
import sys
from pathlib import Path
import sqlite3

# 添加專案根目錄到Python路徑
sys.path.insert(0, str(Path(__file__).parent))

def check_question_5():
    """檢查題目5的詳細信息"""
    print("🔍 檢查題目5...")
    
    try:
        conn = sqlite3.connect('dev_quiz_database.db')
        cursor = conn.cursor()
        
        # 獲取題目5的詳細信息
        cursor.execute("SELECT * FROM questions WHERE id = 5")
        row = cursor.fetchone()
        
        if row:
            print(f"ID: {row[0]}")
            print(f"題目: {row[2][:100]}...")
            print(f"題型: {row[3]}")
            print(f"選項: {row[4]}")
            print(f"正確答案: {row[5]}")
            print(f"正確答案列表: {row[6]}")
            
            # 解析選項
            import json
            options = json.loads(row[4])
            print("\n選項列表:")
            for i, option in enumerate(options):
                print(f"  {i}: {option}")
            
            # 檢查正確答案索引
            correct_answer = row[5]
            print(f"\n正確答案索引: {correct_answer}")
            if correct_answer.isdigit():
                idx = int(correct_answer)
                if 0 <= idx < len(options):
                    print(f"對應選項: {options[idx]}")
                else:
                    print("❌ 索引超出範圍!")
            else:
                print("❌ 正確答案不是數字索引!")
        else:
            print("❌ 找不到題目5")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def fix_question_5():
    """修復題目5的正確答案"""
    print("\n🔧 修復題目5...")
    
    try:
        conn = sqlite3.connect('dev_quiz_database.db')
        cursor = conn.cursor()
        
        # 獲取題目5的選項
        cursor.execute("SELECT options FROM questions WHERE id = 5")
        row = cursor.fetchone()
        
        if row:
            import json
            options = json.loads(row[0])
            
            # 找到"臉部識別"選項的索引
            for i, option in enumerate(options):
                if "臉部識別" in option:
                    print(f"找到正確選項: {i} - {option}")
                    
                    # 更新正確答案
                    cursor.execute("UPDATE questions SET correct_answer = ? WHERE id = 5", (str(i),))
                    conn.commit()
                    print(f"✅ 已更新題目5的正確答案為索引 {i}")
                    break
            else:
                print("❌ 找不到包含'臉部識別'的選項")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 修復失敗: {e}")

if __name__ == '__main__':
    check_question_5()
    fix_question_5()
    print("\n驗證修復結果:")
    check_question_5()
