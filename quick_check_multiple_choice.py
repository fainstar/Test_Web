#!/usr/bin/env python3
"""
快速檢查多選題識別
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_check():
    """快速檢查多選題識別"""
    from app.services.question_service import QuestionService
    
    question_service = QuestionService()
    
    # 獲取所有題目
    result = question_service.get_questions(page=1, per_page=100)
    questions = result['questions']
    
    print(f"總共獲取 {len(questions)} 個題目")
    
    single_count = 0
    multiple_count = 0
    
    print("\n題目類型統計:")
    for q in questions:
        if q['type'] == 'single':
            single_count += 1
        elif q['type'] == 'multiple':
            multiple_count += 1
        else:
            print(f"未知類型: {q['type']} (題目 {q['id']})")
    
    print(f"單選題: {single_count}")
    print(f"多選題: {multiple_count}")
    
    # 檢查一些多選題範例
    print("\n多選題範例:")
    multiple_examples = [q for q in questions if q['type'] == 'multiple'][:5]
    for q in multiple_examples:
        print(f"題目 {q['id']}: {q['question'][:50]}...")
        print(f"  正確答案: {q['correct_answer']}")
        print(f"  選項數: {len(q['options'])}")
    
    # 檢查可能的問題
    print("\n檢查可能的識別問題:")
    issues = []
    for q in questions:
        # 檢查單選題是否有多個正確答案
        if q['type'] == 'single' and isinstance(q['correct_answer'], list) and len(q['correct_answer']) > 1:
            issues.append(f"題目 {q['id']}: 標記為單選但有多個答案 {q['correct_answer']}")
        
        # 檢查多選題是否只有一個正確答案
        if q['type'] == 'multiple' and (not isinstance(q['correct_answer'], list) or len(q['correct_answer']) <= 1):
            issues.append(f"題目 {q['id']}: 標記為多選但只有一個答案 {q['correct_answer']}")
    
    if issues:
        print(f"發現 {len(issues)} 個問題:")
        for issue in issues[:10]:
            print(f"  - {issue}")
    else:
        print("✅ 未發現類型識別問題")
    
    return len(issues)

if __name__ == "__main__":
    issues_count = quick_check()
    print(f"\n總結: {'發現問題' if issues_count > 0 else '無問題'}")
