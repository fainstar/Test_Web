#!/usr/bin/env python3
"""
搜尋包含特定關鍵詞的題目
"""
import sqlite3
import json

def search_passport_question():
    """搜尋護照相關的題目"""
    print("搜尋護照/檔案智慧服務相關題目...")
    
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 搜尋包含關鍵詞的題目
    keywords = ['護照', '檔智慧', '身份證件', '哪兩個', '預先建置', 'passport', '名片模型', '發票模型']
    
    found_questions = []
    
    for keyword in keywords:
        cursor.execute("""
            SELECT id, question_text, question_type, correct_answer, correct_answers, options
            FROM questions 
            WHERE question_text LIKE ?
        """, (f'%{keyword}%',))
        
        results = cursor.fetchall()
        for result in results:
            if result not in found_questions:
                found_questions.append(result)
    
    print(f"找到 {len(found_questions)} 個相關題目:")
    
    for i, (q_id, question_text, question_type, correct_answer, correct_answers, options) in enumerate(found_questions):
        print(f"\n=== 題目 {q_id} ===")
        print(f"問題: {question_text[:100]}...")
        print(f"類型: {question_type}")
        print(f"correct_answer: {correct_answer}")
        print(f"correct_answers: {correct_answers}")
        
        # 解析正確答案
        try:
            if correct_answers:
                parsed_answers = json.loads(correct_answers)
                print(f"解析的正確答案: {parsed_answers}")
                print(f"正確答案數量: {len(parsed_answers)}")
                
                # 檢查是否應該是多選題
                if len(parsed_answers) > 1 and question_type == 'single_choice':
                    print("❌ 這應該是多選題！")
                elif len(parsed_answers) <= 1 and question_type == 'multiple_choice':
                    print("❌ 這應該是單選題！")
                else:
                    print("✅ 類型正確")
        except Exception as e:
            print(f"答案解析失敗: {e}")
        
        # 解析選項
        try:
            parsed_options = json.loads(options)
            print(f"選項:")
            for j, option in enumerate(parsed_options):
                print(f"  {j}: {option}")
        except:
            print("選項解析失敗")
    
    conn.close()
    return found_questions

def check_all_mismatched():
    """檢查所有類型不匹配的題目"""
    print("\n" + "="*60)
    print("檢查所有類型不匹配的題目...")
    
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers
        FROM questions 
        ORDER BY id
    """)
    
    all_questions = cursor.fetchall()
    mismatched = []
    
    for q_id, question_text, question_type, correct_answers in all_questions:
        try:
            if correct_answers:
                parsed_answers = json.loads(correct_answers)
                should_be_multiple = len(parsed_answers) > 1
                is_multiple = question_type == 'multiple_choice'
                
                if should_be_multiple and not is_multiple:
                    mismatched.append((q_id, question_text, 'should_be_multiple', parsed_answers))
                elif not should_be_multiple and is_multiple:
                    mismatched.append((q_id, question_text, 'should_be_single', parsed_answers))
        except:
            continue
    
    print(f"找到 {len(mismatched)} 個類型不匹配的題目:")
    
    for q_id, question_text, issue_type, answers in mismatched:
        print(f"\n題目 {q_id}: {issue_type}")
        print(f"  問題: {question_text[:80]}...")
        print(f"  正確答案: {answers}")
    
    conn.close()
    return mismatched

if __name__ == "__main__":
    found = search_passport_question()
    mismatched = check_all_mismatched()
