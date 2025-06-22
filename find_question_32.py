#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找題目32在題目列表中的位置，以及檢查是否有序號問題
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services import QuestionService

def find_question_32_position():
    """查找題目32的位置"""
    question_service = QuestionService()
    
    # 獲取所有題目
    result = question_service.get_questions(page=1, per_page=1000)  # 獲取足夠多的題目
    
    print(f"=== 總共 {len(result['questions'])} 個題目 ===")
    
    # 查找題目32
    for i, question in enumerate(result['questions']):
        if question['id'] == 32:
            print(f"題目32在列表中的位置: 第 {i+1} 個")
            print(f"ID: {question['id']}")
            print(f"類型: {question['type']}")
            print(f"問題: {question['question']}")
            break
    else:
        print("未在前1000個題目中找到題目32")
    
    # 檢查前幾個題目，看是否有Azure相關的
    print(f"\n=== 檢查前50個題目中是否有Azure相關題目 ===")
    azure_questions = []
    
    for i, question in enumerate(result['questions'][:50]):
        if 'Azure' in question['question'] or 'Azure' in str(question['options']):
            azure_questions.append({
                'position': i + 1,
                'id': question['id'],
                'type': question['type'],
                'question': question['question'][:80] + '...'
            })
    
    for aq in azure_questions:
        print(f"位置 {aq['position']}: ID {aq['id']} ({aq['type']}) - {aq['question']}")
    
    # 特別檢查第2個題目
    if len(result['questions']) >= 2:
        second_question = result['questions'][1]  # 索引1是第2個題目
        print(f"\n=== 列表中第2個題目的詳細資訊 ===")
        print(f"ID: {second_question['id']}")
        print(f"類型: {second_question['type']}")
        print(f"問題: {second_question['question']}")
        print(f"選項: {second_question['options']}")
        print(f"正確答案: {second_question['correct_answer']}")

if __name__ == "__main__":
    find_question_32_position()
