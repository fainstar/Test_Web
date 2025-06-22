#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索包含「臉部識別」的所有題目
"""
import sqlite3
import json

def search_face_recognition():
    """搜索包含臉部識別的題目"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 搜索問題文字或選項中包含「臉部識別」的題目
    cursor.execute("""
        SELECT id, question_text, question_type, options, correct_answer, correct_answers 
        FROM questions 
        WHERE question_text LIKE '%臉部識別%' OR options LIKE '%臉部識別%'
    """)
    
    results = cursor.fetchall()
    
    print(f"=== 找到 {len(results)} 個包含「臉部識別」的題目 ===")
    
    for result in results:
        print(f"\nID {result[0]} ({result[2]}):")
        print(f"問題: {result[1]}")
        
        try:
            options = json.loads(result[3])
            print(f"選項: {options}")
            
            # 檢查選項中的臉部識別
            for i, option in enumerate(options):
                if '臉部識別' in option:
                    print(f"  選項 {i}: {option} ← 包含「臉部識別」")
            
            print(f"正確答案: {result[4]}")
            print(f"正確答案們: {result[5]}")
            
            # 解析正確答案
            if result[2] == 'single_choice':
                try:
                    correct_idx = int(result[4])
                    if 0 <= correct_idx < len(options):
                        print(f"正確答案選項: {options[correct_idx]}")
                except:
                    pass
            else:
                try:
                    correct_answers = json.loads(result[5]) if result[5] else []
                    correct_options = []
                    for idx in correct_answers:
                        if 0 <= int(idx) < len(options):
                            correct_options.append(options[int(idx)])
                    print(f"正確答案選項: {correct_options}")
                except:
                    pass
                    
        except Exception as e:
            print(f"解析失敗: {e}")
    
    # 也搜索所有關於臉部的題目
    print(f"\n=== 所有包含「臉部」的題目 ID ===")
    cursor.execute("SELECT id, question_text FROM questions WHERE question_text LIKE '%臉部%' OR options LIKE '%臉部%' ORDER BY id")
    all_face_results = cursor.fetchall()
    
    for result in all_face_results:
        print(f"ID {result[0]}: {result[1][:50]}...")
    
    conn.close()

if __name__ == "__main__":
    search_face_recognition()
