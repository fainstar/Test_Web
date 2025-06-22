#!/usr/bin/env python3
"""
創建一個包含題目36的測驗並檢查前端渲染
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_quiz_with_question_36():
    """創建包含題目36的測驗"""
    from app.services.question_service import QuestionService
    from app.services.quiz_service import QuizService
    
    question_service = QuestionService()
    quiz_service = QuizService()
    
    # 獲取題目36
    question = question_service.get_question(36)
    if not question:
        print("找不到題目36")
        return None
    
    print("=== 創建包含題目36的測驗 ===")
    print(f"題目類型: {question['type']}")
    print(f"題目內容: {question['question'][:80]}...")
    
    # 創建只包含題目36的測驗
    test_questions = [question]
    quiz_config = {'question_count': 1}
    session_id = quiz_service.create_session(test_questions, quiz_config)
    
    print(f"測驗會話ID: {session_id}")
    print(f"訪問URL: http://localhost:5000/quiz/{session_id}/0")
    
    # 檢查測驗中的題目
    quiz_question = quiz_service.get_current_question(session_id, 0)
    print(f"\n測驗中的題目詳情:")
    print(f"  ID: {quiz_question['id']}")
    print(f"  類型: {quiz_question['type']}")
    print(f"  選項數: {len(quiz_question['options'])}")
    print(f"  正確答案: {quiz_question['correct_answer']}")
    
    return session_id

def check_random_quiz_questions():
    """檢查隨機測驗中是否包含多選題"""
    from app.services.question_service import QuestionService
    
    question_service = QuestionService()
    
    # 獲取隨機題目
    questions = question_service.get_random_questions(count=10)
    
    print(f"\n=== 檢查隨機測驗題目 ===")
    print(f"總共獲取 {len(questions)} 個題目")
    
    single_count = 0
    multiple_count = 0
    
    for i, q in enumerate(questions):
        if q['type'] == 'single':
            single_count += 1
        elif q['type'] == 'multiple':
            multiple_count += 1
            print(f"  題目 {q['id']} (第{i+1}題): 多選題 - {q['question'][:50]}...")
        else:
            print(f"  題目 {q['id']} (第{i+1}題): 未知類型 '{q['type']}'")
    
    print(f"\n類型統計:")
    print(f"  單選題: {single_count}")
    print(f"  多選題: {multiple_count}")
    
    if multiple_count == 0:
        print("❌ 隨機測驗中沒有多選題！這可能是為什麼用戶看不到多選題的原因。")
    else:
        print("✅ 隨機測驗中包含多選題")

def check_specific_question_type():
    """檢查特定題目的類型"""
    from app.services.question_service import QuestionService
    
    question_service = QuestionService()
    
    # 您提到的題目5，讓我們檢查一下
    question_5 = question_service.get_question(5)
    if question_5:
        print(f"\n=== 題目5詳情 ===")
        print(f"內容: {question_5['question'][:80]}...")
        print(f"類型: {question_5['type']}")
        print(f"正確答案: {question_5['correct_answer']}")
    
    # 檢查包含"哪兩個"的題目
    result = question_service.get_questions(page=1, per_page=100)
    questions = result['questions']
    
    print(f"\n=== 包含'哪兩個'關鍵詞的題目 ===")
    for q in questions:
        if '哪兩個' in q['question'] or '哪三個' in q['question']:
            print(f"題目 {q['id']}: {q['type']} - {q['question'][:60]}...")
            if q['type'] == 'single':
                print(f"  ❌ 這個題目應該是多選題但標記為單選！")

if __name__ == "__main__":
    session_id = create_test_quiz_with_question_36()
    check_random_quiz_questions()
    check_specific_question_type()
    
    if session_id:
        print(f"\n=== 測試建議 ===")
        print(f"1. 訪問 http://localhost:5000/quiz/{session_id}/0 查看題目36是否正確顯示為多選題")
        print(f"2. 檢查瀏覽器開發者工具的網路標籤，確認沒有緩存問題")
        print(f"3. 如果還是顯示為單選題，請清除瀏覽器緩存後重試")
