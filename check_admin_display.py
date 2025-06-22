#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查管理後台的多選題顯示
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services import QuestionService

def check_admin_display():
    """檢查管理後台的題目顯示"""
    question_service = QuestionService()
    
    print("=== 檢查管理後台題目列表顯示 ===")
    
    # 獲取題目列表（和管理後台相同的方法）
    result = question_service.get_questions(page=1, per_page=50)
    
    multiple_choice_found = []
    single_choice_found = []
    
    for i, question in enumerate(result['questions']):
        if question['type'] == 'multiple':
            multiple_choice_found.append({
                'position': i + 1,
                'id': question['id'],
                'question': question['question'][:50],
                'correct_answer': question['correct_answer']
            })
        else:
            single_choice_found.append({
                'position': i + 1,
                'id': question['id'],
                'question': question['question'][:50],
                'correct_answer': question['correct_answer']
            })
    
    print(f"在前50個題目中找到:")
    print(f"  多選題: {len(multiple_choice_found)} 個")
    print(f"  單選題: {len(single_choice_found)} 個")
    
    print(f"\n多選題列表:")
    for mc in multiple_choice_found:
        print(f"  位置 {mc['position']}: ID {mc['id']} - {mc['question']}...")
        print(f"    正確答案: {mc['correct_answer']}")
    
    # 檢查特定的已知多選題是否在列表中
    known_multiple_ids = [16, 18, 22, 27, 28, 32, 35, 36, 37, 39]
    print(f"\n=== 檢查已知多選題在列表中的狀態 ===")
    
    for known_id in known_multiple_ids:
        found = False
        for mc in multiple_choice_found:
            if mc['id'] == known_id:
                print(f"✅ ID {known_id}: 在列表第 {mc['position']} 位，正確顯示為多選題")
                found = True
                break
        
        if not found:
            # 檢查是否被錯誤顯示為單選題
            for sc in single_choice_found:
                if sc['id'] == known_id:
                    print(f"❌ ID {known_id}: 在列表第 {sc['position']} 位，但錯誤顯示為單選題！")
                    found = True
                    break
        
        if not found:
            print(f"⚠️  ID {known_id}: 不在前50個題目中")
    
    # 測試編輯功能的題目格式化
    print(f"\n=== 測試編輯功能的題目格式化 ===")
    test_edit_id = 32  # 測試題目32的編輯
    
    question = question_service.get_question(test_edit_id)
    if question:
        # 模擬管理後台編輯時的格式化
        question_data = {
            'id': question['id'],
            'question': question['question'],
            'type': question['type'],
            'options': question['options'],
            'correct_answer': question['correct_answer'],
            'category': question.get('category', '一般'),
            'difficulty': question.get('difficulty', '中等'),
            'explanation': question.get('explanation', '')
        }
        
        print(f"編輯模式格式化結果 (ID {test_edit_id}):")
        for key, value in question_data.items():
            print(f"  {key}: {value} (型態: {type(value)})")

if __name__ == "__main__":
    check_admin_display()
