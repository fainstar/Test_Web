#!/usr/bin/env python3
import sqlite3
import json

def check_database():
    conn = sqlite3.connect('quiz_database.db')
    cursor = conn.cursor()

    # 查看表結構
    cursor.execute('PRAGMA table_info(questions)')
    columns = cursor.fetchall()
    print('表結構:')
    for col in columns:
        print(f'  {col[1]} {col[2]}')

    print('\n查看多選題數據:')

    # 查看一些多選題的數據
    cursor.execute('SELECT id, question_text, question_type, correct_answer, correct_answers FROM questions WHERE question_type = "multiple_choice" LIMIT 3')
    questions = cursor.fetchall()

    for q in questions:
        print(f'ID: {q[0]}')
        print(f'題目: {q[1][:50]}...')
        print(f'類型: {q[2]}')
        print(f'correct_answer: {repr(q[3])}')
        print(f'correct_answers: {repr(q[4])}')
        print('-' * 40)

    conn.close()

if __name__ == '__main__':
    check_database()
