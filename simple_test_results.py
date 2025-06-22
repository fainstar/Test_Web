#!/usr/bin/env python3
"""
簡單測試結果頁面的多選題顯示
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simple_test():
    """簡單測試"""
    from app.services.question_service import QuestionService
    from app.services.quiz_service import QuizService
    from datetime import datetime
    
    question_service = QuestionService()
    quiz_service = QuizService()
    
    # 獲取題目36
    question = question_service.get_question(36)
    if not question:
        print("找不到題目36")
        return
    
    print(f"題目36類型: {question['type']}")
    print(f"正確答案: {question['correct_answer']}")
    
    # 創建會話
    test_questions = [question]
    quiz_config = {'question_count': 1}
    session_id = quiz_service.create_session(test_questions, quiz_config)
    
    # 提交答案
    quiz_service.submit_answer(session_id, 36, [1, 2])  # 正確答案
    
    # 完成測驗
    start_time = datetime.now().isoformat()
    result = quiz_service.complete_quiz(session_id, start_time)
    
    if result['success']:
        detailed = result['results']['detailed_results']
        if detailed:
            first_result = detailed[0]
            print(f"\n結果中的類型: {first_result.get('type')}")
            print(f"結果中的正確答案: {first_result.get('correct_answer')}")
            print(f"結果中的用戶答案: {first_result.get('user_answer')}")
            
            # 這就是模板會收到的數據格式
            if first_result.get('type') == 'multiple':
                print("✅ 結果正確標記為多選題")
            else:
                print(f"❌ 結果錯誤標記為: {first_result.get('type')}")
        else:
            print("沒有詳細結果")
    else:
        print(f"測驗完成失敗: {result['message']}")
    
    return session_id

if __name__ == "__main__":
    session_id = simple_test()
    print(f"\n測試完成，會話ID: {session_id}")
    print("可以訪問:")
    print(f"http://localhost:5000/quiz/results/{session_id}")
