#!/usr/bin/env python3
"""
搜尋包含臉部識別的題目
"""
import sys
from pathlib import Path
import sqlite3
import json

# 添加專案根目錄到Python路徑
sys.path.insert(0, str(Path(__file__).parent))

def search_face_question():
    """搜尋包含臉部相關的題目"""
    print("🔍 搜尋包含臉部相關的題目...")
    
    try:
        conn = sqlite3.connect('dev_quiz_database.db')
        cursor = conn.cursor()
        
        # 搜尋題目內容包含"臉部"或"Azure AI 臉部"的題目
        cursor.execute("SELECT * FROM questions WHERE question_text LIKE '%臉部%' OR question_text LIKE '%Azure AI 臉部%'")
        rows = cursor.fetchall()
        
        print(f"找到 {len(rows)} 個相關題目:")
        
        for row in rows:
            print(f"\n--- 題目ID: {row[0]} ---")
            print(f"題目: {row[2][:100]}...")
            print(f"題型: {row[3]}")
            
            # 解析選項
            options = json.loads(row[4])
            print("選項:")
            for i, option in enumerate(options):
                print(f"  {i}: {option}")
            
            print(f"正確答案: {row[5]}")
            if row[5].isdigit():
                idx = int(row[5])
                if 0 <= idx < len(options):
                    print(f"正確選項: {options[idx]}")
                else:
                    print("❌ 索引超出範圍!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def search_by_options():
    """搜尋選項中包含臉部識別的題目"""
    print("\n🔍 搜尋選項中包含'臉部識別'的題目...")
    
    try:
        conn = sqlite3.connect('dev_quiz_database.db')
        cursor = conn.cursor()
        
        # 獲取所有題目
        cursor.execute("SELECT * FROM questions")
        rows = cursor.fetchall()
        
        for row in rows:
            try:
                options = json.loads(row[4])
                for i, option in enumerate(options):
                    if "臉部識別" in option:
                        print(f"\n--- 題目ID: {row[0]} ---")
                        print(f"題目: {row[2][:100]}...")
                        print("選項:")
                        for j, opt in enumerate(options):
                            marker = " (正確答案)" if str(j) == row[5] else ""
                            print(f"  {j}: {opt}{marker}")
                        print(f"正確答案索引: {row[5]}")
                        break
            except:
                continue
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == '__main__':
    search_face_question()
    search_by_options()
