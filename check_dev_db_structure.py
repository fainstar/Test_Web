import sqlite3

# 檢查資料庫結構
conn = sqlite3.connect('dev_quiz_database.db')
cursor = conn.cursor()

# 查看questions表的結構
cursor.execute("PRAGMA table_info(questions)")
columns = cursor.fetchall()
print("questions表的欄位:")
for col in columns:
    print(f"  {col[1]} {col[2]}")

# 查看前幾筆資料
print("\n前5筆題目資料:")
cursor.execute("SELECT * FROM questions LIMIT 5")
rows = cursor.fetchall()
for i, row in enumerate(rows):
    print(f"  {i+1}: {row[:3]}...")  # 只顯示前3個欄位

conn.close()
