#!/usr/bin/env python3
"""
最終多選題審計腳本 - 徹底檢查所有多選題識別問題
"""
import sqlite3
import json
from datetime import datetime

def get_db_connection():
    """獲取資料庫連接"""
    return sqlite3.connect('dev_quiz_database.db')

def check_database_raw_data():
    """檢查資料庫原始數據"""
    print("=" * 60)
    print("1. 檢查資料庫原始數據")
    print("=" * 60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
      # 檢查所有題目的基本信息
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers, options
        FROM questions 
        ORDER BY id
    """)
    
    questions = cursor.fetchall()
    print(f"總共找到 {len(questions)} 個題目")
    
    single_count = 0
    multiple_count = 0
    type_issues = []
    answer_issues = []
      for q_id, question, q_type, correct_answers, options in questions:
        # 解析正確答案
        try:
            if correct_answers:
                if correct_answers.startswith('[') and correct_answers.endswith(']'):
                    parsed_answers = json.loads(correct_answers)
                elif ',' in correct_answers:
                    parsed_answers = [int(x.strip()) for x in correct_answers.split(',')]
                else:
                    try:
                        parsed_answers = [int(correct_answers)]
                    except:
                        parsed_answers = []
            else:
                parsed_answers = []
        except Exception as e:
            answer_issues.append(f"題目 {q_id}: 解析答案失敗 - {e}")
            parsed_answers = []
        
        # 根據正確答案數量判斷應該的題目類型
        should_be_multiple = len(parsed_answers) > 1
        
        if q_type == 'single_choice':
            single_count += 1
            if should_be_multiple:
                type_issues.append(f"題目 {q_id}: 標記為單選但有多個正確答案 {parsed_answers}")
        elif q_type == 'multiple_choice':
            multiple_count += 1
            if not should_be_multiple:
                type_issues.append(f"題目 {q_id}: 標記為多選但只有一個正確答案 {parsed_answers}")
        else:
            type_issues.append(f"題目 {q_id}: 未知類型 '{q_type}'")
    
    print(f"單選題: {single_count}")
    print(f"多選題: {multiple_count}")
    
    if type_issues:
        print(f"\n發現 {len(type_issues)} 個類型問題:")
        for issue in type_issues[:10]:  # 只顯示前10個
            print(f"  - {issue}")
        if len(type_issues) > 10:
            print(f"  ... 還有 {len(type_issues) - 10} 個問題")
    
    if answer_issues:
        print(f"\n發現 {len(answer_issues)} 個答案解析問題:")
        for issue in answer_issues[:5]:
            print(f"  - {issue}")
        if len(answer_issues) > 5:
            print(f"  ... 還有 {len(answer_issues) - 5} 個問題")
    
    conn.close()
    return type_issues, answer_issues

def check_service_layer():
    """檢查服務層處理"""
    print("\n" + "=" * 60)
    print("2. 檢查服務層處理")
    print("=" * 60)
    
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from app.services.question_service import QuestionService
        question_service = QuestionService()
        
        # 獲取所有題目通過服務層
        result = question_service.get_questions(page=1, per_page=1000)
        questions = result['questions']
        
        print(f"服務層返回 {len(questions)} 個題目")
        
        service_single = 0
        service_multiple = 0
        service_issues = []
          for q in questions:
            if q['type'] == 'single_choice':
                service_single += 1
                # 檢查是否應該是多選
                if isinstance(q.get('correct_answer'), list) and len(q['correct_answer']) > 1:
                    service_issues.append(f"題目 {q['id']}: 服務層標記為單選但正確答案是列表 {q['correct_answer']}")
            elif q['type'] == 'multiple_choice':
                service_multiple += 1
                # 檢查是否應該是單選
                if not isinstance(q.get('correct_answer'), list) or len(q['correct_answer']) <= 1:
                    service_issues.append(f"題目 {q['id']}: 服務層標記為多選但正確答案不是多個 {q['correct_answer']}")
            else:
                service_issues.append(f"題目 {q['id']}: 服務層返回未知類型 '{q['type']}'")
        
        print(f"服務層 - 單選題: {service_single}")
        print(f"服務層 - 多選題: {service_multiple}")
        
        if service_issues:
            print(f"\n發現 {len(service_issues)} 個服務層問題:")
            for issue in service_issues[:10]:
                print(f"  - {issue}")
            if len(service_issues) > 10:
                print(f"  ... 還有 {len(service_issues) - 10} 個問題")
        
        return service_issues
        
    except Exception as e:
        print(f"檢查服務層失敗: {e}")
        return [f"服務層檢查失敗: {e}"]

def check_specific_samples():
    """檢查特定的樣本題目"""
    print("\n" + "=" * 60)
    print("3. 檢查特定樣本題目")
    print("=" * 60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查找一些關鍵詞的多選題
    keywords = ['選擇所有', '選擇全部', '下列哪些', '以下哪些', '多個', '全部', '所有']
    
    issues = []
    for keyword in keywords:        cursor.execute("""
            SELECT id, question_text, question_type, correct_answers, options
            FROM questions 
            WHERE question_text LIKE ? AND question_type = 'single_choice'
            LIMIT 5
        """, (f'%{keyword}%',))
        
        potential_multiples = cursor.fetchall()
        for q_id, question, q_type, correct_answers, options in potential_multiples:
            try:
                parsed_answers = json.loads(correct_answers) if correct_answers.startswith('[') else [int(correct_answers)]
                if len(parsed_answers) > 1:
                    issues.append(f"題目 {q_id}: 包含 '{keyword}' 但標記為單選，答案: {parsed_answers}")
                    print(f"可能的多選題 {q_id}: {question[:50]}...")
            except:
                pass
      # 檢查所有實際有多個正確答案但標記為單選的題目
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers, options
        FROM questions 
        WHERE question_type = 'single_choice' AND (
            correct_answers LIKE '[%,%]' OR 
            correct_answers LIKE '%,%'
        )
        LIMIT 10
    """)
    
    multi_answer_singles = cursor.fetchall()
    for q_id, question, q_type, correct_answers, options in multi_answer_singles:
        print(f"\n題目 {q_id} (標記為單選但有多答案):")
        print(f"  問題: {question[:100]}...")
        print(f"  正確答案: {correct_answers}")
        issues.append(f"題目 {q_id}: 單選題但有多個答案 {correct_answers}")
    
    conn.close()
    return issues

def fix_type_mismatches():
    """修正類型不匹配的問題"""
    print("\n" + "=" * 60)
    print("4. 自動修正類型不匹配")
    print("=" * 60)
    
    conn = get_db_connection()
    cursor = conn.cursor()
      # 查找需要修正的題目
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers, options
        FROM questions 
        ORDER BY id
    """)
    
    all_questions = cursor.fetchall()
    fixes_needed = []
    
    for q_id, question, q_type, correct_answers, options in all_questions:
        try:
            # 解析正確答案
            if correct_answers:
                if correct_answers.startswith('[') and correct_answers.endswith(']'):
                    parsed_answers = json.loads(correct_answers)
                elif ',' in correct_answers:
                    parsed_answers = [int(x.strip()) for x in correct_answers.split(',') if x.strip()]
                else:
                    try:
                        parsed_answers = [int(correct_answers)]
                    except:
                        continue
            else:
                continue
              # 判斷應該的類型
            should_be_multiple = len(parsed_answers) > 1
            current_is_multiple = q_type == 'multiple_choice'
            
            if should_be_multiple and not current_is_multiple:
                # 應該是多選但標記為單選
                fixes_needed.append((q_id, 'single_choice', 'multiple_choice', parsed_answers))
            elif not should_be_multiple and current_is_multiple:
                # 應該是單選但標記為多選
                fixes_needed.append((q_id, 'multiple_choice', 'single_choice', parsed_answers))
                
        except Exception as e:
            print(f"處理題目 {q_id} 時出錯: {e}")
            continue
    
    print(f"發現 {len(fixes_needed)} 個需要修正的題目")
    
    if fixes_needed:
        print("\n需要修正的題目:")
        for q_id, old_type, new_type, answers in fixes_needed[:10]:
            print(f"  題目 {q_id}: {old_type} -> {new_type} (答案: {answers})")
        
        if len(fixes_needed) > 10:
            print(f"  ... 還有 {len(fixes_needed) - 10} 個")
        
        # 詢問是否執行修正
        response = input(f"\n是否要修正這 {len(fixes_needed)} 個題目的類型? (y/n): ")
        if response.lower() == 'y':
            fixed_count = 0
            for q_id, old_type, new_type, answers in fixes_needed:
                try:                    cursor.execute("""
                        UPDATE questions 
                        SET question_type = ? 
                        WHERE id = ?
                    """, (new_type, q_id))
                    fixed_count += 1
                except Exception as e:
                    print(f"修正題目 {q_id} 失敗: {e}")
            
            conn.commit()
            print(f"成功修正 {fixed_count} 個題目")
        else:
            print("跳過修正")
    
    conn.close()
    return fixes_needed

def main():
    """主函數"""
    print("開始最終多選題審計...")
    print(f"時間: {datetime.now()}")
    
    # 1. 檢查資料庫原始數據
    type_issues, answer_issues = check_database_raw_data()
    
    # 2. 檢查服務層
    service_issues = check_service_layer()
    
    # 3. 檢查特定樣本
    sample_issues = check_specific_samples()
    
    # 4. 修正類型不匹配
    fixes_needed = fix_type_mismatches()
    
    # 總結
    print("\n" + "=" * 60)
    print("審計總結")
    print("=" * 60)
    
    total_issues = len(type_issues) + len(answer_issues) + len(service_issues) + len(sample_issues)
    print(f"總共發現 {total_issues} 個問題:")
    print(f"  - 資料庫類型問題: {len(type_issues)}")
    print(f"  - 答案解析問題: {len(answer_issues)}")
    print(f"  - 服務層問題: {len(service_issues)}")
    print(f"  - 樣本檢查問題: {len(sample_issues)}")
    print(f"  - 需要修正的題目: {len(fixes_needed)}")
    
    if total_issues > 0:
        print("\n建議:")
        print("1. 運行此腳本並選擇修正類型不匹配")
        print("2. 檢查答案解析問題")
        print("3. 重新測試前端顯示")
    else:
        print("\n沒有發現明顯的多選題識別問題！")

if __name__ == "__main__":
    main()
