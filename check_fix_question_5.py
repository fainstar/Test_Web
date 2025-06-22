#!/usr/bin/env python3
"""
檢查題目5的詳細信息
"""
import sqlite3
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_question_5():
    """檢查題目5的詳細信息"""
    print("檢查題目5的詳細信息...")
    
    # 檢查資料庫原始數據
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answer, correct_answers, options
        FROM questions 
        WHERE id = 5
    """)
    
    result = cursor.fetchone()
    if result:
        q_id, question_text, question_type, correct_answer, correct_answers, options = result
        print(f"題目ID: {q_id}")
        print(f"問題文字: {question_text}")
        print(f"題目類型: {question_type}")
        print(f"correct_answer 欄位: {correct_answer}")
        print(f"correct_answers 欄位: {correct_answers}")
        print(f"選項: {options}")
        
        # 解析選項
        try:
            parsed_options = json.loads(options)
            print(f"\n解析後的選項:")
            for i, option in enumerate(parsed_options):
                print(f"  {i}: {option}")
        except:
            print("選項解析失敗")
        
        # 分析正確答案
        if correct_answers:
            try:
                parsed_correct_answers = json.loads(correct_answers)
                print(f"\n正確答案解析: {parsed_correct_answers}")
                print(f"正確答案數量: {len(parsed_correct_answers)}")
                if len(parsed_correct_answers) > 1:
                    print("❌ 這應該是多選題但標記為: " + question_type)
                else:
                    print("✅ 單選題標記正確")
            except Exception as e:
                print(f"正確答案解析失敗: {e}")
    else:
        print("找不到題目5")
    
    conn.close()
    
    # 檢查服務層返回
    print("\n" + "="*50)
    print("檢查服務層返回...")
    
    try:
        from app.services.question_service import QuestionService
        question_service = QuestionService()
        
        question = question_service.get_question(5)
        if question:
            print(f"服務層返回:")
            print(f"  ID: {question['id']}")
            print(f"  類型: {question['type']}")
            print(f"  問題: {question['question'][:60]}...")
            print(f"  正確答案: {question['correct_answer']}")
            print(f"  正確答案類型: {type(question['correct_answer'])}")
            
            if question['type'] == 'single' and isinstance(question['correct_answer'], list) and len(question['correct_answer']) > 1:
                print("❌ 服務層錯誤：標記為單選但有多個正確答案")
            elif question['type'] == 'multiple' and (not isinstance(question['correct_answer'], list) or len(question['correct_answer']) <= 1):
                print("❌ 服務層錯誤：標記為多選但只有一個正確答案")
            else:
                print("✅ 服務層類型正確")
        else:
            print("服務層找不到題目5")
    except Exception as e:
        print(f"服務層檢查失敗: {e}")

def fix_question_5():
    """修正題目5的類型"""
    print("\n" + "="*50)
    print("修正題目5...")
    
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 檢查當前狀態
    cursor.execute("""
        SELECT question_type, correct_answers
        FROM questions 
        WHERE id = 5
    """)
    
    result = cursor.fetchone()
    if result:
        current_type, correct_answers = result
        
        try:
            parsed_answers = json.loads(correct_answers) if correct_answers else []
            if len(parsed_answers) > 1 and current_type != 'multiple_choice':
                print(f"需要修正：當前類型 {current_type}，正確答案數量 {len(parsed_answers)}")
                
                # 更新為多選題
                cursor.execute("""
                    UPDATE questions 
                    SET question_type = 'multiple_choice'
                    WHERE id = 5
                """)
                conn.commit()
                print("✅ 已將題目5修正為多選題")
                
                # 驗證修正結果
                cursor.execute("""
                    SELECT question_type, correct_answers
                    FROM questions 
                    WHERE id = 5
                """)
                new_result = cursor.fetchone()
                print(f"修正後類型: {new_result[0]}")
                
            else:
                print("題目5類型已正確，無需修正")
        except Exception as e:
            print(f"修正失敗: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_question_5()
    fix_question_5()
    
    print("\n" + "="*50)
    print("重新檢查題目5...")
    check_question_5()
