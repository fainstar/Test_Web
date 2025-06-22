import sqlite3
import os

# 使用絕對路徑
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dev_quiz_database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM questions")
total = cursor.fetchone()[0]
print(f'資料庫總題數: {total}')

cursor.execute("SELECT COUNT(*) FROM questions WHERE question_type = 'multiple_choice'")
multiple_count = cursor.fetchone()[0]
print(f'多選題數量: {multiple_count}')

cursor.execute("SELECT COUNT(*) FROM questions WHERE question_type = 'single_choice'")
single_count = cursor.fetchone()[0]
print(f'單選題數量: {single_count}')

print('\n多選題範例:')
cursor.execute("SELECT id, question_text, correct_answer FROM questions WHERE question_type = 'multiple_choice' LIMIT 3")
results = cursor.fetchall()
for row in results:
    print(f'ID:{row[0]}, 正確答案:{row[2]}')
    print(f'題目:{row[1][:80]}...')
    print()

conn.close()
