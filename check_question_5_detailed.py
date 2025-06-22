#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查資料庫 schema 和題目5的詳細資料
"""
import sqlite3
import json

def check_database_schema():
    """檢查資料庫 schema"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    print("=== 資料庫 Schema ===")
    cursor.execute("PRAGMA table_info(questions)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"{column[1]} ({column[2]}) - NOT NULL: {column[3]}, Default: {column[4]}")
    
    print("\n=== 檢查題目5是否存在 ===")
    cursor.execute("SELECT id, question_text FROM questions WHERE id = 5")
    result = cursor.fetchone()
    if result:
        print(f"題目5存在: {result[1][:50]}...")
    else:
        print("題目5不存在")
    
    print("\n=== 檢查所有題目ID ===")
    cursor.execute("SELECT id, question_text FROM questions ORDER BY id LIMIT 10")
    results = cursor.fetchall()
    for result in results:
        print(f"ID {result[0]}: {result[1][:30]}...")
    
    conn.close()

def check_question_5_detailed():
    """詳細檢查題目5"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM questions WHERE id = 5")
    result = cursor.fetchone()
    
    if result:
        columns = [description[0] for description in cursor.description]
        question_data = dict(zip(columns, result))
        
        print("\n=== 題目 5 詳細分析 ===")
        print(f"題目類型: {question_data.get('question_type', 'N/A')}")
        print(f"選項: {question_data.get('options', 'N/A')}")
        print(f"正確答案: {question_data.get('correct_answer', 'N/A')}")
        print(f"正確答案們: {question_data.get('correct_answers', 'N/A')}")
        
        # 測試解析邏輯
        try:
            options = json.loads(question_data['options'])
            correct_answer = question_data['correct_answer']
            
            print(f"\n選項列表: {options}")
            print(f"正確答案原始值: '{correct_answer}' (型態: {type(correct_answer)})")
            
            # 嘗試轉換為整數
            try:
                correct_idx = int(correct_answer)
                if 0 <= correct_idx < len(options):
                    print(f"正確答案選項: {options[correct_idx]}")
                else:
                    print(f"索引 {correct_idx} 超出範圍")
            except ValueError:
                print(f"無法將 '{correct_answer}' 轉換為整數")
                
        except Exception as e:
            print(f"解析失敗: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_database_schema()
    check_question_5_detailed()
