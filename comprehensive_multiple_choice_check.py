#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面檢查多選題識別問題
"""
import sqlite3
import json

def comprehensive_multiple_choice_check():
    """全面檢查多選題識別問題"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    print("=== 1. 檢查資料庫中標記為多選題的題目 ===")
    cursor.execute("""
        SELECT id, question_text, question_type, options, correct_answer, correct_answers 
        FROM questions 
        WHERE question_type = 'multiple_choice'
        ORDER BY id
    """)
    
    multiple_choice_questions = cursor.fetchall()
    print(f"找到 {len(multiple_choice_questions)} 個標記為多選題的題目")
    
    problems = []
    
    for q in multiple_choice_questions:
        print(f"\nID {q[0]}: {q[1][:60]}...")
        print(f"  類型: {q[2]}")
        print(f"  正確答案: {q[4]}")
        print(f"  正確答案們: {q[5]}")
        
        try:
            options = json.loads(q[3])
            print(f"  選項數: {len(options)}")
            
            # 檢查正確答案格式
            correct_answer = q[4]
            correct_answers = q[5]
            
            # 分析正確答案
            if correct_answers:
                try:
                    parsed_answers = json.loads(correct_answers)
                    if isinstance(parsed_answers, list) and len(parsed_answers) > 1:
                        print(f"  ✅ 確實是多選題，有 {len(parsed_answers)} 個正確答案")
                    elif isinstance(parsed_answers, list) and len(parsed_answers) == 1:
                        print(f"  ⚠️  只有1個正確答案，可能應該是單選題")
                        problems.append(f"ID {q[0]}: 只有1個正確答案但標記為多選題")
                    else:
                        print(f"  ❌ 正確答案格式異常: {parsed_answers}")
                        problems.append(f"ID {q[0]}: 正確答案格式異常")
                except:
                    print(f"  ❌ 無法解析正確答案: {correct_answers}")
                    problems.append(f"ID {q[0]}: 無法解析正確答案")
            elif ',' in str(correct_answer):
                print(f"  ⚠️  correct_answer 包含逗號，但 correct_answers 為空")
                problems.append(f"ID {q[0]}: correct_answer有逗號但correct_answers為空")
            else:
                print(f"  ❌ 沒有多個正確答案")
                problems.append(f"ID {q[0]}: 沒有多個正確答案")
                
        except Exception as e:
            print(f"  ❌ 解析失敗: {e}")
            problems.append(f"ID {q[0]}: 解析失敗")
    
    print(f"\n=== 2. 檢查可能被誤標為單選題的多選題 ===")
    cursor.execute("""
        SELECT id, question_text, question_type, options, correct_answer, correct_answers 
        FROM questions 
        WHERE question_type = 'single_choice' 
        AND (correct_answer LIKE '%,%' OR question_text LIKE '%每個正確答案%' OR question_text LIKE '%都各自提供%')
        ORDER BY id
    """)
    
    potential_multiple = cursor.fetchall()
    print(f"找到 {len(potential_multiple)} 個可能被誤標的多選題")
    
    for q in potential_multiple:
        print(f"\nID {q[0]}: {q[1][:60]}...")
        print(f"  目前類型: {q[2]} ← 可能應該是多選題")
        print(f"  正確答案: {q[4]}")
        print(f"  正確答案們: {q[5]}")
        
        # 檢查題目描述
        if '每個正確答案' in q[1] or '都各自提供' in q[1]:
            print(f"  ⚠️  題目描述暗示多選題")
            problems.append(f"ID {q[0]}: 題目描述暗示多選題但標記為單選題")
        
        if ',' in str(q[4]):
            print(f"  ⚠️  correct_answer 包含逗號")
            problems.append(f"ID {q[0]}: correct_answer包含逗號但標記為單選題")
    
    print(f"\n=== 3. 檢查 QuestionService 格式化結果 ===")
    # 測試幾個有問題的題目的格式化結果
    from app.services import QuestionService
    question_service = QuestionService()
    
    test_ids = [32, 35, 39]  # 已知的多選題
    for test_id in test_ids:
        question = question_service.get_question(test_id)
        if question:
            print(f"\nID {test_id} QuestionService 結果:")
            print(f"  類型: {question['type']}")
            print(f"  正確答案: {question['correct_answer']} (型態: {type(question['correct_answer'])})")
        else:
            print(f"\nID {test_id}: 無法獲取")
    
    print(f"\n=== 問題總結 ===")
    if problems:
        for problem in problems:
            print(f"❌ {problem}")
    else:
        print("✅ 沒有發現明顯問題")
    
    conn.close()

if __name__ == "__main__":
    comprehensive_multiple_choice_check()
