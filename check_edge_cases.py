#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
檢查可能導致多選題識別問題的邊界情況
"""
import sqlite3
import json

def check_edge_cases():
    """檢查邊界情況"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    print("=== 1. 檢查可能的數據不一致問題 ===")
    
    # 檢查 correct_answer 和 correct_answers 不一致的情況
    cursor.execute("""
        SELECT id, question_text, question_type, correct_answer, correct_answers
        FROM questions 
        WHERE question_type = 'multiple_choice'
    """)
    
    multiple_questions = cursor.fetchall()
    problems = []
    
    for q in multiple_questions:
        qid, text, qtype, ca, cas = q
        
        try:
            # 解析 correct_answers
            if cas:
                parsed_cas = json.loads(cas)
            else:
                parsed_cas = []
            
            # 檢查 correct_answer 和 correct_answers 是否一致
            if ca and ',' in str(ca):
                # correct_answer 包含逗號，應該和 correct_answers 一致
                ca_list = [int(x.strip()) for x in str(ca).split(',')]
                if ca_list != parsed_cas:
                    problems.append(f"ID {qid}: correct_answer ({ca_list}) 與 correct_answers ({parsed_cas}) 不一致")
            
            # 檢查是否真的是多選題
            if len(parsed_cas) <= 1:
                problems.append(f"ID {qid}: 標記為多選題但只有 {len(parsed_cas)} 個正確答案")
                
        except Exception as e:
            problems.append(f"ID {qid}: 解析錯誤 - {e}")
    
    if problems:
        print("發現問題:")
        for problem in problems:
            print(f"  ❌ {problem}")
    else:
        print("✅ 沒有發現數據不一致問題")
    
    print(f"\n=== 2. 檢查可能被錯誤標記的題目 ===")
    
    # 檢查標記為單選題但可能是多選題的情況
    cursor.execute("""
        SELECT id, question_text, question_type, options, correct_answer, correct_answers
        FROM questions 
        WHERE question_type = 'single_choice'
        AND (
            question_text LIKE '%哪兩個%'
            OR question_text LIKE '%哪三個%' 
            OR question_text LIKE '%哪四個%'
            OR question_text LIKE '%兩項%'
            OR question_text LIKE '%三項%'
            OR question_text LIKE '%多個%'
            OR question_text LIKE '%每個正確答案%'
            OR question_text LIKE '%都各自提供%'
            OR question_text LIKE '%都代表%'
        )
    """)
    
    potential_multiple = cursor.fetchall()
    
    if potential_multiple:
        print(f"找到 {len(potential_multiple)} 個可能被錯誤標記為單選題的題目:")
        for q in potential_multiple:
            print(f"\nID {q[0]}: {q[1][:80]}...")
            print(f"  目前類型: {q[2]}")
            print(f"  正確答案: {q[4]}")
            print(f"  正確答案們: {q[5]}")
            
            # 檢查選項和題目描述
            try:
                options = json.loads(q[3])
                print(f"  選項數: {len(options)}")
                
                # 分析是否應該是多選題
                should_be_multiple = False
                reasons = []
                
                if any(keyword in q[1] for keyword in ['哪兩個', '哪三個', '哪四個', '兩項', '三項']):
                    should_be_multiple = True
                    reasons.append("題目詢問多個答案")
                
                if '每個正確答案' in q[1] or '都各自提供' in q[1]:
                    should_be_multiple = True
                    reasons.append("題目描述暗示多個正確答案")
                
                if ',' in str(q[4]):
                    should_be_multiple = True
                    reasons.append("correct_answer 包含逗號")
                
                if should_be_multiple:
                    print(f"  ⚠️  可能應該是多選題: {', '.join(reasons)}")
                else:
                    print(f"  ✅ 可能確實是單選題")
                    
            except Exception as e:
                print(f"  ❌ 解析失敗: {e}")
    else:
        print("✅ 沒有發現被錯誤標記的題目")
    
    print(f"\n=== 3. 檢查最近導入的題目 ===")
    
    # 檢查最近導入的題目是否有問題
    cursor.execute("""
        SELECT id, question_text, question_type, created_at
        FROM questions 
        ORDER BY created_at DESC 
        LIMIT 10
    """)
    
    recent_questions = cursor.fetchall()
    
    print("最近10個題目:")
    for q in recent_questions:
        print(f"  ID {q[0]} ({q[2]}): {q[1][:50]}... (創建時間: {q[3]})")
        
        if q[2] == 'multiple_choice':
            # 檢查多選題是否正確
            cursor.execute("SELECT correct_answers FROM questions WHERE id = ?", (q[0],))
            cas_result = cursor.fetchone()
            if cas_result and cas_result[0]:
                try:
                    parsed_cas = json.loads(cas_result[0])
                    print(f"    ✅ 多選題，{len(parsed_cas)} 個正確答案")
                except:
                    print(f"    ❌ 多選題，但正確答案解析失敗")
    
    conn.close()

def check_specific_issues():
    """檢查用戶可能遇到的特定問題"""
    print(f"\n=== 檢查用戶可能遇到的特定問題 ===")
    
    # 可能的問題場景
    print("可能的問題場景:")
    print("1. 前端JavaScript錯誤導致多選題顯示為單選題")
    print("2. 瀏覽器緩存問題")
    print("3. 特定題目在特定條件下出現問題")
    print("4. 測驗流程中的隨機選擇問題")
    print("5. 模板渲染問題")
    
    print(f"\n建議的調試步驟:")
    print("1. 在瀏覽器中打開開發者工具，檢查控制台錯誤")
    print("2. 檢查網路請求，確保API返回正確的題目類型")
    print("3. 清除瀏覽器緩存並重新加載")
    print("4. 檢查特定題目ID的詳細信息")
    print("5. 在測驗過程中記錄每個題目的ID和類型")

if __name__ == "__main__":
    check_edge_cases()
    check_specific_issues()
