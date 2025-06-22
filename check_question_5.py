#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查題目5的資料狀況
"""
import sqlite3
import json

def check_question_5():
    """檢查題目5的完整資料"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 查詢題目5的完整資料
    cursor.execute("SELECT * FROM questions WHERE id = 5")
    result = cursor.fetchone()
    
    if result:
        columns = [description[0] for description in cursor.description]
        question_data = dict(zip(columns, result))
        
        print("=== 題目 5 完整資料 ===")
        for key, value in question_data.items():
            print(f"{key}: {value}")
        
        print("\n=== 選項解析 ===")
        if question_data['options']:
            try:
                options = json.loads(question_data['options'])
                for i, option in enumerate(options):
                    print(f"選項 {i}: {option}")
            except:
                print(f"選項資料無法解析: {question_data['options']}")
        
        print("\n=== 正確答案解析 ===")
        print(f"正確答案原始資料: {question_data['correct_answer']}")
        print(f"正確答案型態: {type(question_data['correct_answer'])}")
        
        # 嘗試解析正確答案
        try:
            if question_data['type'] == 'single':
                correct_idx = int(question_data['correct_answer'])
                options = json.loads(question_data['options'])
                if 0 <= correct_idx < len(options):
                    print(f"正確答案選項: {options[correct_idx]}")
                else:
                    print(f"正確答案索引 {correct_idx} 超出範圍")
            else:
                correct_indices = json.loads(question_data['correct_answer'])
                options = json.loads(question_data['options'])
                correct_options = [options[i] for i in correct_indices if 0 <= i < len(options)]
                print(f"正確答案選項: {correct_options}")
        except Exception as e:
            print(f"解析正確答案失敗: {e}")
    else:
        print("未找到題目5")
    
    conn.close()

if __name__ == "__main__":
    check_question_5()
