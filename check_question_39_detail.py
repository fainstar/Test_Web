#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查題目39的詳細資料 (Azure AI 臉部服務題目)
"""
import sqlite3
import json

def check_question_39():
    """檢查題目39"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM questions WHERE id = 39")
    result = cursor.fetchone()
    
    if result:
        columns = [description[0] for description in cursor.description]
        question_data = dict(zip(columns, result))
        
        print("=== 題目 39 詳細資料 ===")
        print(f"問題: {question_data['question_text']}")
        print(f"類型: {question_data['question_type']}")
        
        try:
            options = json.loads(question_data['options'])
            print(f"選項:")
            for i, option in enumerate(options):
                print(f"  {i}: {option}")
        except:
            print(f"選項解析失敗: {question_data['options']}")
        
        print(f"正確答案原始資料: {question_data['correct_answer']}")
        print(f"正確答案們: {question_data['correct_answers']}")
        
        # 測試格式化邏輯
        if question_data['question_type'] == 'multiple_choice':
            try:
                if question_data['correct_answers']:
                    correct_answer_data = json.loads(question_data['correct_answers'])
                    if isinstance(correct_answer_data, list):
                        correct_answer = [int(x) for x in correct_answer_data if isinstance(x, (int, str)) and str(x).isdigit()]
                    else:
                        correct_answer = []
                else:
                    if question_data['correct_answer'] and ',' in str(question_data['correct_answer']):
                        correct_answer = [int(x.strip()) for x in str(question_data['correct_answer']).split(',')]
                    else:
                        correct_answer = []
                
                print(f"解析後的正確答案: {correct_answer}")
                
                # 顯示正確答案選項
                options = json.loads(question_data['options'])
                correct_options = []
                for idx in correct_answer:
                    if 0 <= idx < len(options):
                        correct_options.append(options[idx])
                print(f"正確答案選項: {correct_options}")
                
            except Exception as e:
                print(f"解析失敗: {e}")
    else:
        print("未找到題目39")
    
    conn.close()

if __name__ == "__main__":
    check_question_39()
