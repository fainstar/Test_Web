#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜尋 Azure AI 視覺特製化領域模型的題目
"""
import sqlite3
import json

def search_azure_vision_question():
    """搜尋 Azure AI 視覺相關題目"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 搜尋包含 Azure AI 視覺、特製化、領域模型的題目
    search_terms = ['Azure AI 視覺', '特製化', '領域模型', '脫口秀', '地標']
    
    for term in search_terms:
        print(f"\n=== 搜尋包含「{term}」的題目 ===")
        cursor.execute("""
            SELECT id, question_text, question_type, options, correct_answer, correct_answers 
            FROM questions 
            WHERE question_text LIKE ? OR options LIKE ?
        """, (f'%{term}%', f'%{term}%'))
        
        results = cursor.fetchall()
        for result in results:
            print(f"ID {result[0]} ({result[2]}): {result[1][:60]}...")
            
            try:
                options = json.loads(result[3])
                print(f"  選項: {options}")
                print(f"  正確答案: {result[4]}")
                print(f"  正確答案們: {result[5]}")
                
                # 檢查是否包含搜尋詞
                for i, option in enumerate(options):
                    if term in option:
                        print(f"    選項 {i}: {option} ← 包含「{term}」")
            except:
                pass
    
    # 特別搜尋包含「脫口秀」的題目
    print(f"\n=== 特別搜尋「脫口秀」題目 ===")
    cursor.execute("""
        SELECT id, question_text, question_type, options, correct_answer, correct_answers 
        FROM questions 
        WHERE options LIKE '%脫口秀%'
    """)
    
    results = cursor.fetchall()
    if results:
        for result in results:
            print(f"\n找到包含「脫口秀」的題目：")
            print(f"ID: {result[0]}")
            print(f"類型: {result[2]}")
            print(f"問題: {result[1]}")
            
            try:
                options = json.loads(result[3])
                print(f"選項: {options}")
                print(f"正確答案: {result[4]}")
                print(f"正確答案們: {result[5]}")
                
                # 檢查題目描述是否暗示多選
                if '每個正確答案' in result[1] or '都各自提供' in result[1]:
                    print(">>> 這個題目描述暗示為多選題!")
                
                # 檢查正確答案數量
                if result[5]:
                    try:
                        correct_list = json.loads(result[5])
                        if isinstance(correct_list, list) and len(correct_list) > 1:
                            print(f">>> 正確答案有 {len(correct_list)} 個，應該是多選題!")
                    except:
                        pass
                        
                if ',' in str(result[4]):
                    print(">>> correct_answer 包含逗號，可能是多選題!")
                    
            except Exception as e:
                print(f"解析失敗: {e}")
    else:
        print("未找到包含「脫口秀」的題目")
    
    conn.close()

if __name__ == "__main__":
    search_azure_vision_question()
