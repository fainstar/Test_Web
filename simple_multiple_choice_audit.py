#!/usr/bin/env python3
"""
簡化版多選題識別審計腳本
"""
import sqlite3
import json
import sys
import os

# 添加應用路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_database_multiple_choice():
    """檢查資料庫中的多選題識別"""
    print("檢查資料庫多選題識別...")
    
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 獲取所有題目
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers, options
        FROM questions 
        ORDER BY id
    """)
    
    questions = cursor.fetchall()
    print(f"總共 {len(questions)} 個題目")
    
    # 統計
    single_count = 0
    multiple_count = 0
    issues = []
    
    for q_id, question_text, question_type, correct_answers, options in questions:
        # 解析正確答案
        try:
            if correct_answers:
                if correct_answers.startswith('[') and correct_answers.endswith(']'):
                    parsed_answers = json.loads(correct_answers)
                else:
                    parsed_answers = [int(correct_answers)]
            else:
                parsed_answers = []
        except Exception as e:
            issues.append(f"題目 {q_id}: 解析答案失敗 - {e}")
            continue
        
        # 判斷應該的類型
        should_be_multiple = len(parsed_answers) > 1
        
        if question_type == 'single_choice':
            single_count += 1
            if should_be_multiple:
                issues.append(f"題目 {q_id}: 標記為單選但有多個正確答案 {parsed_answers}")
                print(f"  問題題目: {question_text[:50]}...")
        elif question_type == 'multiple_choice':
            multiple_count += 1
            if not should_be_multiple:
                issues.append(f"題目 {q_id}: 標記為多選但只有一個正確答案 {parsed_answers}")
        else:
            issues.append(f"題目 {q_id}: 未知類型 '{question_type}'")
    
    print(f"單選題: {single_count}")
    print(f"多選題: {multiple_count}")
    print(f"問題數量: {len(issues)}")
    
    if issues:
        print("\n前10個問題:")
        for issue in issues[:10]:
            print(f"  - {issue}")
    
    conn.close()
    return issues

def check_service_layer():
    """檢查服務層"""
    print("\n檢查服務層...")
    
    try:
        from app.services.question_service import QuestionService
        question_service = QuestionService()
        
        result = question_service.get_questions(page=1, per_page=50)
        questions = result['questions']
        
        print(f"服務層返回 {len(questions)} 個題目")
        
        service_single = 0
        service_multiple = 0
        issues = []
          for q in questions:
            if q['type'] == 'single':
                service_single += 1
            elif q['type'] == 'multiple':
                service_multiple += 1
            else:
                issues.append(f"題目 {q['id']}: 服務層返回未知類型 '{q['type']}'")
        
        print(f"服務層 - 單選題: {service_single}")
        print(f"服務層 - 多選題: {service_multiple}")
        
        if issues:
            print("服務層問題:")
            for issue in issues[:5]:
                print(f"  - {issue}")
        
        return issues
        
    except Exception as e:
        print(f"檢查服務層失敗: {e}")
        return [f"服務層檢查失敗: {e}"]

def check_sample_questions():
    """檢查樣本題目"""
    print("\n檢查樣本題目...")
    
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 查找包含"選擇"、"哪些"等關鍵詞的題目
    keywords = ['選擇所有', '選擇全部', '下列哪些', '以下哪些']
    
    issues = []
    for keyword in keywords:
        cursor.execute("""
            SELECT id, question_text, question_type, correct_answers
            FROM questions 
            WHERE question_text LIKE ? AND question_type = 'single_choice'
            LIMIT 3
        """, (f'%{keyword}%',))
        
        results = cursor.fetchall()
        for q_id, question_text, question_type, correct_answers in results:
            try:
                parsed_answers = json.loads(correct_answers) if correct_answers.startswith('[') else [int(correct_answers)]
                if len(parsed_answers) > 1:
                    issues.append(f"題目 {q_id}: 包含 '{keyword}' 但標記為單選")
                    print(f"  可疑題目 {q_id}: {question_text[:60]}...")
                    print(f"    正確答案: {parsed_answers}")
            except:
                pass
    
    # 檢查實際有多個答案但標記為單選的題目
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers
        FROM questions 
        WHERE question_type = 'single_choice' AND correct_answers LIKE '[%,%]'
        LIMIT 5
    """)
    
    multi_answer_singles = cursor.fetchall()
    for q_id, question_text, question_type, correct_answers in multi_answer_singles:
        issues.append(f"題目 {q_id}: 單選但有多個答案")
        print(f"  題目 {q_id}: {question_text[:60]}...")
        print(f"    答案: {correct_answers}")
    
    conn.close()
    return issues

def fix_mismatched_types():
    """修正類型不匹配"""
    print("\n檢查需要修正的題目...")
    
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answers
        FROM questions 
        ORDER BY id
    """)
    
    questions = cursor.fetchall()
    fixes_needed = []
    
    for q_id, question_text, question_type, correct_answers in questions:
        try:
            if correct_answers:
                if correct_answers.startswith('[') and correct_answers.endswith(']'):
                    parsed_answers = json.loads(correct_answers)
                else:
                    parsed_answers = [int(correct_answers)]
            else:
                continue
            
            should_be_multiple = len(parsed_answers) > 1
            current_is_multiple = question_type == 'multiple_choice'
            
            if should_be_multiple and not current_is_multiple:
                fixes_needed.append((q_id, 'single_choice', 'multiple_choice', parsed_answers))
            elif not should_be_multiple and current_is_multiple:
                fixes_needed.append((q_id, 'multiple_choice', 'single_choice', parsed_answers))
                
        except:
            continue
    
    print(f"需要修正 {len(fixes_needed)} 個題目")
    
    if fixes_needed:
        print("\n需要修正的題目:")
        for q_id, old_type, new_type, answers in fixes_needed[:5]:
            print(f"  題目 {q_id}: {old_type} -> {new_type} (答案: {answers})")
        
        if len(fixes_needed) > 5:
            print(f"  ... 還有 {len(fixes_needed) - 5} 個")
        
        # 自動修正
        try:
            fixed_count = 0
            for q_id, old_type, new_type, answers in fixes_needed:
                cursor.execute("""
                    UPDATE questions 
                    SET question_type = ? 
                    WHERE id = ?
                """, (new_type, q_id))
                fixed_count += 1
            
            conn.commit()
            print(f"\n已自動修正 {fixed_count} 個題目")
        except Exception as e:
            print(f"修正失敗: {e}")
    
    conn.close()
    return fixes_needed

def main():
    """主函數"""
    print("=== 多選題識別審計 ===")
    
    # 1. 檢查資料庫
    db_issues = check_database_multiple_choice()
    
    # 2. 檢查服務層
    service_issues = check_service_layer()
    
    # 3. 檢查樣本
    sample_issues = check_sample_questions()
    
    # 4. 修正問題
    fixes = fix_mismatched_types()
    
    # 總結
    total_issues = len(db_issues) + len(service_issues) + len(sample_issues)
    print(f"\n=== 總結 ===")
    print(f"資料庫問題: {len(db_issues)}")
    print(f"服務層問題: {len(service_issues)}")
    print(f"樣本問題: {len(sample_issues)}")
    print(f"已修正: {len(fixes)}")
    print(f"總問題數: {total_issues}")
    
    if total_issues == 0 and len(fixes) == 0:
        print("\n✅ 未發現多選題識別問題!")
    else:
        print(f"\n⚠️ 發現 {total_issues} 個問題，已修正 {len(fixes)} 個")

if __name__ == "__main__":
    main()
