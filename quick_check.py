import sqlite3

print("檢查 dev_quiz_database.db...")
try:
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 查看表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"資料表: {tables}")
    
    if ('questions',) in tables:
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        print(f"題目總數: {count}")
        
        cursor.execute("SELECT COUNT(*) FROM questions WHERE question_type='multiple_choice'")
        multiple_count = cursor.fetchone()[0]
        print(f"多選題數量: {multiple_count}")
    
    conn.close()
    print("✅ 檢查完成")
except Exception as e:
    print(f"❌ 錯誤: {e}")
