#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查 quiz_sessions 表結構，並添加 questions_json 欄位
"""
import sqlite3

def check_and_update_quiz_sessions_table():
    """檢查和更新 quiz_sessions 表結構"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 檢查現有表結構
    print("=== 檢查 quiz_sessions 表結構 ===")
    cursor.execute("PRAGMA table_info(quiz_sessions)")
    columns = cursor.fetchall()
    
    existing_columns = [col[1] for col in columns]
    print(f"現有欄位: {existing_columns}")
    
    # 檢查是否存在 questions_json 欄位
    if 'questions_json' not in existing_columns:
        print("\n=== 添加 questions_json 欄位 ===")
        try:
            cursor.execute("""
                ALTER TABLE quiz_sessions 
                ADD COLUMN questions_json TEXT
            """)
            conn.commit()
            print("✅ questions_json 欄位添加成功")
        except Exception as e:
            print(f"❌ 添加欄位失敗: {e}")
    else:
        print("✅ questions_json 欄位已存在")
    
    # 重新檢查表結構
    print("\n=== 更新後的表結構 ===")
    cursor.execute("PRAGMA table_info(quiz_sessions)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"{column[1]} ({column[2]}) - NOT NULL: {column[3]}, Default: {column[4]}")
    
    # 檢查現有記錄
    print(f"\n=== 檢查現有記錄 ===")
    cursor.execute("SELECT COUNT(*) FROM quiz_sessions")
    count = cursor.fetchone()[0]
    print(f"現有會話記錄數: {count}")
    
    if count > 0:
        cursor.execute("SELECT session_id, questions_json IS NOT NULL as has_questions FROM quiz_sessions LIMIT 5")
        records = cursor.fetchall()
        for record in records:
            print(f"會話 {record[0]}: 有題目JSON = {bool(record[1])}")
    
    conn.close()

if __name__ == "__main__":
    check_and_update_quiz_sessions_table()
