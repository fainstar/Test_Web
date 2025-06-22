#!/usr/bin/env python3
"""
檢查資料庫結構
"""
import sqlite3

def check_database_structure():
    """檢查資料庫結構"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 獲取所有表格
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("資料庫中的表格:")
    for table in tables:
        print(f"  - {table[0]}")
    
    print("\n" + "="*50)
    
    # 檢查 questions 表格結構
    if ('questions',) in tables:
        cursor.execute("PRAGMA table_info(questions);")
        columns = cursor.fetchall()
        print("questions 表格結構:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - 主鍵: {col[5]}, 非空: {col[3]}, 預設: {col[4]}")
        
        # 檢查一些範例數據
        cursor.execute("SELECT * FROM questions LIMIT 3;")
        samples = cursor.fetchall()
        print(f"\n範例數據 (前3筆):")
        for i, sample in enumerate(samples):
            print(f"  第{i+1}筆: {sample}")
    
    # 檢查 quiz_sessions 表格結構
    if ('quiz_sessions',) in tables:
        print("\n" + "="*50)
        cursor.execute("PRAGMA table_info(quiz_sessions);")
        columns = cursor.fetchall()
        print("quiz_sessions 表格結構:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - 主鍵: {col[5]}, 非空: {col[3]}, 預設: {col[4]}")
    
    conn.close()

if __name__ == "__main__":
    check_database_structure()
