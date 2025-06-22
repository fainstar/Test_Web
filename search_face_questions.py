#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜尋包含「臉部」的題目
"""
import sqlite3
import json

def search_face_questions():
    """搜尋包含臉部的題目"""
    conn = sqlite3.connect('dev_quiz_database.db')
    cursor = conn.cursor()
    
    # 搜尋問題文字中包含「臉部」的題目
    cursor.execute("SELECT id, question_text, options, correct_answer FROM questions WHERE question_text LIKE '%臉部%'")
    text_results = cursor.fetchall()
    
    print("=== 問題文字中包含「臉部」的題目 ===")
    for result in text_results:
        print(f"ID {result[0]}: {result[1][:50]}...")
        try:
            options = json.loads(result[2])
            correct_answer = result[3]
            print(f"  選項: {options}")
            print(f"  正確答案: {correct_answer}")
            if correct_answer.isdigit():
                idx = int(correct_answer)
                if 0 <= idx < len(options):
                    print(f"  正確答案選項: {options[idx]}")
        except:
            pass
        print()
    
    # 搜尋選項中包含「臉部」的題目
    cursor.execute("SELECT id, question_text, options, correct_answer FROM questions WHERE options LIKE '%臉部%'")
    option_results = cursor.fetchall()
    
    print("=== 選項中包含「臉部」的題目 ===")
    for result in option_results:
        print(f"ID {result[0]}: {result[1][:50]}...")
        try:
            options = json.loads(result[2])
            correct_answer = result[3]
            print(f"  選項: {options}")
            print(f"  正確答案: {correct_answer}")
            if correct_answer.isdigit():
                idx = int(correct_answer)
                if 0 <= idx < len(options):
                    print(f"  正確答案選項: {options[idx]}")
        except:
            pass
        print()
    
    conn.close()

if __name__ == "__main__":
    search_face_questions()
