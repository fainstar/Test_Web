#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度檢查多選題可能出現問題的場景
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services import QuestionService, QuizService

def deep_check_scenarios():
    """深度檢查可能出現問題的場景"""
    question_service = QuestionService()
    quiz_service = QuizService()
    
    print("=== 1. 檢查所有題目的類型一致性 ===")
    
    # 獲取所有題目，檢查是否有不一致
    all_questions = question_service.get_questions(page=1, per_page=1000)
    
    inconsistent_questions = []
    
    for question in all_questions['questions']:
        # 檢查格式化結果和原始資料是否一致
        raw_question = question_service.get_question(question['id'])
        
        if raw_question['type'] != question['type']:
            inconsistent_questions.append({
                'id': question['id'],
                'list_type': question['type'],
                'raw_type': raw_question['type']
            })
    
    if inconsistent_questions:
        print(f"發現 {len(inconsistent_questions)} 個類型不一致的題目:")
        for iq in inconsistent_questions:
            print(f"  ID {iq['id']}: 列表顯示 {iq['list_type']}, 單獨獲取 {iq['raw_type']}")
    else:
        print("✅ 所有題目類型一致")
    
    print(f"\n=== 2. 檢查測驗結果顯示中的多選題 ===")
    
    # 模擬一個包含多選題的測驗結果
    test_answers = [
        {
            'question_id': 32,
            'question_text': '分類影像時，Azure AI 視覺支援哪兩個特製化領域模型？',
            'type': 'multiple',
            'options': ['脫口秀', '影像類型', '地標', '人們', '人群'],
            'correct_answers': [0, 2],
            'user_answer': [0],  # 用戶只選了一個
            'is_correct': False
        },
        {
            'question_id': 39,
            'question_text': '使用 Azure AI 臉部服務時，您應該使用什麼來執行一對多或一對一臉部比對？',
            'type': 'multiple',
            'options': ['自定義視覺', '臉部屬性', '臉部識別', '臉部驗證', '尋找類似的臉部'],
            'correct_answers': [2, 3],
            'user_answer': [2, 3],  # 用戶選對了
            'is_correct': True
        }
    ]
    
    # 測試結果格式化
    formatted_results = quiz_service._format_detailed_results(test_answers)
    
    for i, result in enumerate(formatted_results):
        print(f"\n測驗結果 {i+1}:")
        print(f"  題目類型: {result['type']}")
        print(f"  用戶答案: {result['user_answer']}")
        print(f"  正確答案 (single): {result['correct_answer']}")
        print(f"  正確答案 (multiple): {result['correct_answers']}")
        print(f"  是否正確: {result['is_correct']}")
        
        # 檢查多選題結果格式化是否正確
        if 'multiple' in result['type']:
            if not isinstance(result['correct_answers'], list) or len(result['correct_answers']) < 2:
                print(f"  ❌ 多選題正確答案格式錯誤!")
            else:
                print(f"  ✅ 多選題正確答案格式正確")
    
    print(f"\n=== 3. 檢查特定模板顯示邏輯 ===")
    
    # 模擬模板中的條件判斷
    test_question = {
        'type': 'multiple',
        'correct_answer': [0, 2]
    }
    
    # 測試 quiz.html 中的條件
    if test_question['type'] == 'multiple':
        badge_text = "多選題"
        input_type = "checkbox"
    else:
        badge_text = "單選題"
        input_type = "radio"
    
    print(f"模板邏輯測試:")
    print(f"  題目類型: {test_question['type']}")
    print(f"  顯示徽章: {badge_text}")
    print(f"  輸入類型: {input_type}")
    
    # 測試 results.html 中的條件
    test_result = {
        'type': 'multiple_choice',
        'correct_answers': ['脫口秀', '地標']
    }
    
    if test_result['type'] == 'single_choice':
        display_mode = "單一答案"
    else:
        display_mode = "多個答案徽章"
    
    print(f"\n結果頁面邏輯測試:")
    print(f"  結果類型: {test_result['type']}")
    print(f"  顯示模式: {display_mode}")
    print(f"  正確答案: {test_result['correct_answers']}")
    
    print(f"\n=== 4. 檢查最近的測驗會話 ===")
    
    # 檢查最近的測驗會話中是否有多選題問題
    recent_sessions = quiz_service.get_recent_sessions(limit=5)
    
    if recent_sessions:
        print(f"最近 {len(recent_sessions)} 個測驗會話:")
        for session in recent_sessions:
            print(f"  會話 {session['session_id'][:8]}...: 得分 {session.get('score_percentage', 'N/A')}%")
    else:
        print("沒有最近的測驗會話")

if __name__ == "__main__":
    deep_check_scenarios()
