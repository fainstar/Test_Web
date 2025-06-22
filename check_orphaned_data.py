#!/usr/bin/env python3
"""
檢查外鍵約束問題
"""
import sqlite3

def check_user_answers_references():
    """檢查 user_answers 表是否引用了不存在的題目"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 檢查是否有孤立的 user_answers 記錄
    cursor.execute("""
        SELECT ua.question_id, COUNT(*) as count
        FROM user_answers ua
        LEFT JOIN questions q ON ua.question_id = q.id
        WHERE q.id IS NULL
        GROUP BY ua.question_id
    """)
    
    orphaned_answers = cursor.fetchall()
    if orphaned_answers:
        print("發現孤立的 user_answers 記錄:")
        for record in orphaned_answers:
            print(f"  題目ID {record[0]}: {record[1]} 條記錄")
    else:
        print("沒有孤立的 user_answers 記錄")
    
    # 檢查 user_answers 總數
    cursor.execute("SELECT COUNT(*) FROM user_answers")
    total_answers = cursor.fetchone()[0]
    print(f"user_answers 總記錄數: {total_answers}")
    
    # 檢查 questions 總數
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]
    print(f"questions 總記錄數: {total_questions}")
    
    conn.close()

def clean_orphaned_answers():
    """清理孤立的 user_answers 記錄"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 刪除孤立的記錄
    cursor.execute("""
        DELETE FROM user_answers 
        WHERE question_id NOT IN (SELECT id FROM questions)
    """)
    
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"清理了 {deleted_count} 條孤立的 user_answers 記錄")

if __name__ == "__main__":
    check_user_answers_references()
    clean_orphaned_answers()
    check_user_answers_references()
