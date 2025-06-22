#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查題目39的資料庫狀態和格式化結果
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
import json
from app.models.question import Question

def check_question_39_complete():
    """完整檢查題目39"""
    
    # 1. 直接從資料庫檢查
    print("=== 1. 資料庫原始資料 ===")
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = 39")
    result = cursor.fetchone()
    
    if result:
        columns = [description[0] for description in cursor.description]
        question_data = dict(zip(columns, result))
        
        print(f"ID: {question_data['id']}")
        print(f"問題文字: {question_data['question_text']}")
        print(f"題目類型: {question_data['question_type']}")
        print(f"選項: {question_data['options']}")
        print(f"正確答案: {question_data['correct_answer']}")
        print(f"正確答案們: {question_data['correct_answers']}")
    
    conn.close()
      # 2. 通過 Question 模型檢查
    print("\n=== 2. Question 模型格式化結果 ===")
    from config.config import Config
    config = Config()
    question_model = Question(config.DATABASE_PATH)
    
    # 直接獲取原始數據
    raw_data = question_model.execute_query("SELECT * FROM questions WHERE id = 39")
    if raw_data:
        raw_question = raw_data[0]
        formatted_question = question_model._format_question(raw_question)
        
        print(f"格式化後的題目:")
        for key, value in formatted_question.items():
            print(f"  {key}: {value} (型態: {type(value)})")
    
    # 3. 通過 QuestionService 檢查
    print("\n=== 3. QuestionService 結果 ===")
    from app.services import QuestionService
    question_service = QuestionService()
    
    question_39 = question_service.get_question(39)
    if question_39:
        print(f"QuestionService 結果:")
        for key, value in question_39.items():
            print(f"  {key}: {value} (型態: {type(value)})")

if __name__ == "__main__":
    check_question_39_complete()
