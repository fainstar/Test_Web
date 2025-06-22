import sqlite3

# 檢查資料庫
try:
    conn = sqlite3.connect('quiz_database.db')
    cursor = conn.cursor()
    
    # 查看所有資料表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("資料表:", tables)
    
    # 如果有questions表，查看資料
    if ('questions',) in tables:
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        print(f"題目總數: {count}")
        
        # 查看多選題數量
        cursor.execute("SELECT COUNT(*) FROM questions WHERE type='multiple'")
        multiple_count = cursor.fetchone()[0]
        print(f"多選題數量: {multiple_count}")
    
    conn.close()
    print("✅ 資料庫檢查完成")
    
except Exception as e:
    print(f"❌ 資料庫檢查失敗: {e}")
