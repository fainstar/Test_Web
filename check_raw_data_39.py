#!/usr/bin/env python3
"""
檢查題目39的資料庫原始數據
"""
import sqlite3
import json

def check_raw_data():
    """檢查原始資料庫數據"""
    print("🔍 檢查題目39的原始數據...")
    
    try:
        conn = sqlite3.connect('dev_quiz_database.db')
        cursor = conn.cursor()
        
        # 獲取原始數據
        cursor.execute("SELECT * FROM questions WHERE id = 39")
        row = cursor.fetchone()
        
        if row:
            print("原始數據:")
            print(f"ID: {row[0]}")
            print(f"question_hash: {row[1]}")
            print(f"question_text: {row[2][:100]}...")
            print(f"question_type: {row[3]}")
            print(f"options: {row[4]}")
            print(f"correct_answer: {row[5]}")
            print(f"correct_answers: {row[6]}")
            print(f"category: {row[7]}")
            print(f"difficulty: {row[8]}")
            print(f"explanation: {row[9]}")
            
            # 解析選項
            options = json.loads(row[4])
            print(f"\n解析的選項 (共{len(options)}個):")
            for i, option in enumerate(options):
                print(f"  索引{i}: {option}")
            
            # 解析正確答案
            correct_answer = row[5]  # correct_answer 字段
            correct_answers = row[6]  # correct_answers 字段
            
            print(f"\ncorrect_answer 字段: '{correct_answer}' (類型: {type(correct_answer)})")
            print(f"correct_answers 字段: '{correct_answers}' (類型: {type(correct_answers)})")
            
            # 嘗試解析 correct_answer
            if correct_answer:
                if ',' in str(correct_answer):
                    indices = [int(x.strip()) for x in str(correct_answer).split(',')]
                    print(f"解析的正確答案索引: {indices}")
                    print("對應的選項:")
                    for idx in indices:
                        if 0 <= idx < len(options):
                            print(f"  {idx}: {options[idx]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_raw_data()
